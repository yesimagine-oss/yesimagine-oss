#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "watchdog"]
# ///
"""
學習文件監控自動通知系統

功能:
- 監控 learning/ 目錄文件變更
- 檢測到新學習內容自動補發通知
- 每 30 分鐘檢查一次

使用:
    python3 learning-watcher.py start    # 啟動監控（後台）
    python3 learning-watcher.py stop     # 停止監控
    python3 learning-watcher.py status   # 查看狀態
    python3 learning-watcher.py check    # 立即檢查一次
"""

import json
import os
import sys
import time
import hashlib
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# 配置
WATCH_DIR = Path.home() / ".openclaw" / "workspace" / "learning"
STATE_FILE = Path.home() / ".openclaw" / "workspace" / "tools" / ".learning-watcher-state.json"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "logs" / "learning-watcher.log"
CHECK_INTERVAL = 1800  # 30 分鐘

# 通知工具路徑
NOTIFIER_PATH = Path.home() / ".openclaw" / "workspace" / "tools" / "task-notifier.py"

# 飛書配置
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
CONFIG_FILE = Path.home() / ".openclaw" / "workspace" / ".config" / "feishu-notification.json"


def load_config() -> Dict[str, Any]:
    """加載飛書配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return {
                'app_id': config.get('app', {}).get('appId', 'cli_a929676f8bf81cc7'),
                'app_secret': config.get('app', {}).get('appSecret', 'xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs'),
                'target_user': config.get('pythonLearning', {}).get('targetId', 'ou_f4919832188bcc630f8f257497fa93a4')
            }
    return {
        'app_id': 'cli_a929676f8bf81cc7',
        'app_secret': 'xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs',
        'target_user': 'ou_f4919832188bcc630f8f257497fa93a4'
    }


def get_feishu_token(app_id: str, app_secret: str) -> str:
    """獲取飛書 Access Token"""
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(FEISHU_TOKEN_URL, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        raise Exception(f"獲取飛書 Token 失敗：{result}")
    return result['tenant_access_token']


def send_feishu_message(token: str, user_id: str, title: str, text: str):
    """發送飛書文本消息"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps({"title": title, "text": text}, ensure_ascii=False)
    }
    params = {'receive_id_type': 'open_id'}
    response = requests.post(FEISHU_MESSAGE_URL, headers=headers, params=params, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        log(f"⚠️ 飛書消息發送失敗：{result}")
        return False
    log(f"✅ 飛書消息發送成功：{result.get('data', {}).get('message_id')}")
    return True


def log(message: str):
    """日誌記錄"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # 寫入日誌文件
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')


def get_file_hash(file_path: Path) -> str:
    """計算文件哈希"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def load_state() -> Dict[str, Any]:
    """加載狀態"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'files': {},
        'last_check': None,
        'running': False
    }


def save_state(state: Dict[str, Any]):
    """保存狀態"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_learning_files() -> Dict[str, Dict[str, Any]]:
    """獲取學習文件列表"""
    files = {}
    
    if not WATCH_DIR.exists():
        return files
    
    for file_path in WATCH_DIR.glob('*.md'):
        # 跳過索引文件
        if 'INDEX' in file_path.name or 'REPORT' in file_path.name:
            continue
        
        stat = file_path.stat()
        files[str(file_path)] = {
            'mtime': stat.st_mtime,
            'size': stat.st_size,
            'hash': get_file_hash(file_path)
        }
    
    return files


def extract_task_info(file_path: Path, content: str) -> Dict[str, Any]:
    """從文件內容中提取任務信息"""
    info = {
        'task_name': file_path.stem,
        'start_time': None,
        'end_time': None,
        'status': 'unknown',
        'achievements': []
    }
    
    # 嘗試提取狀態
    if '✅' in content or '完成' in content:
        info['status'] = 'completed'
    elif '🔄' in content or '進行中' in content:
        info['status'] = 'in_progress'
    
    # 嘗試提取時間
    lines = content.split('\n')
    for line in lines[:50]:  # 只檢查前 50 行
        if '學習時間' in line or '完成時間' in line:
            # 提取日期
            import re
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', line)
            if date_match:
                info['end_time'] = date_match.group()
        
        if '狀態' in line and '✅' in line:
            info['status'] = 'completed'
    
    # 嘗試提取成果
    if '✅' in content:
        achievements = [line.strip() for line in content.split('\n') if '✅' in line and len(line.strip()) < 100]
        info['achievements'] = achievements[:5]  # 最多 5 個
    
    return info


def send_completion_notification(file_path: Path, file_info: Dict[str, Any]):
    """發送完成通知"""
    try:
        # 讀取文件內容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()[:5000]  # 限制長度
        
        # 提取任務信息
        task_info = extract_task_info(file_path, content)
        
        # 構建任務名稱
        task_name = task_info['task_name'].replace('aliyun-', '阿里雲-').replace('-', ' ')
        task_name = task_name.title()
        
        # 構建成果列表
        achievements = task_info['achievements'] if task_info['achievements'] else [
            f"完成 {task_name} 學習",
            f"生成筆記文件：{file_path.name}"
        ]
        
        # 調用通知工具
        achievements_str = '，'.join(achievements[:3])
        notes = f"文件大小：{file_info['size']/1024:.1f}KB，狀態：{task_info['status']}"
        
        log(f"📢 發送完成通知：{task_name}")
        
        # 使用 task-notifier.py 發送
        cmd = [
            'python3', str(NOTIFIER_PATH), 'end',
            task_name,
            achievements_str,
            notes
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
        
        if result.returncode == 0:
            log(f"✅ 通知發送成功")
        else:
            log(f"⚠️ 通知發送失敗：{result.stderr}")
        
        return True
    
    except Exception as e:
        log(f"❌ 發送通知失敗：{e}")
        return False


def check_new_files():
    """檢查新文件"""
    log("🔍 開始檢查學習文件...")
    
    state = load_state()
    current_files = get_learning_files()
    old_files = state.get('files', {})
    
    new_files = []
    modified_files = []
    
    # 檢測新增和修改
    for file_path, file_info in current_files.items():
        if file_path not in old_files:
            new_files.append((file_path, file_info))
            log(f"🆕 發現新文件：{file_path}")
        elif file_info['hash'] != old_files[file_path].get('hash'):
            modified_files.append((file_path, file_info))
            log(f"🔄 發現修改文件：{file_path}")
    
    # 發送通知
    notifications_sent = 0
    
    for file_path, file_info in new_files + modified_files:
        # 檢查是否是學習文件（阿里雲、AI 相關）
        file_name = Path(file_path).name.lower()
        
        # 學習內容關鍵詞
        keywords = ['aliyun', 'ai-', 'study', 'learning', 'note', 'test']
        
        # 排除系統報告（不發送自動通知）
        exclude_keywords = [
            'system-health',        # 系統健康報告
            'model-performance',    # 模型性能報告
            'verification-report',  # 驗證報告
            'correction-report',    # 糾正報告
            'assessment-report',    # 評估報告
            'health-report',        # 健康報告
            'fix-report',          # 修復報告
            'performance-analysis', # 性能分析
            'analysis-report',      # 分析報告
            'server-and-model',     # 服務器與模型報告
            'endpoint-report',      # 端點報告
            'monitor-filter'        # 監控過濾報告
        ]
        
        # 檢查是否匹配學習關鍵詞
        is_learning = any(keyword in file_name for keyword in keywords)
        
        # 檢查是否應該排除
        is_excluded = any(exclude in file_name for exclude in exclude_keywords)
        
        # 發送通知（是學習內容且不在排除列表）
        if is_learning and not is_excluded:
            if send_completion_notification(Path(file_path), file_info):
                notifications_sent += 1
    
    # 更新狀態
    state['files'] = current_files
    state['last_check'] = datetime.now().isoformat()
    save_state(state)
    
    log(f"✅ 檢查完成，新增 {len(new_files)} 個文件，修改 {len(modified_files)} 個文件，發送 {notifications_sent} 個通知")
    
    return {
        'new': len(new_files),
        'modified': len(modified_files),
        'notifications': notifications_sent
    }


def start_watcher():
    """啟動監控（後台）"""
    log("🚀 啟動學習文件監控...")
    
    # 檢查是否已在運行
    state = load_state()
    if state.get('running'):
        log("⚠️ 監控已在運行中")
        return
    
    # 標記為運行中
    state['running'] = True
    state['pid'] = os.getpid()
    state['start_time'] = datetime.now().isoformat()
    save_state(state)
    
    # 首次檢查
    check_new_files()
    
    # 進入監控循環
    log(f"📡 監控已啟動，每 {CHECK_INTERVAL/60:.0f} 分鐘檢查一次")
    
    while True:
        time.sleep(CHECK_INTERVAL)
        check_new_files()


def stop_watcher():
    """停止監控"""
    log("🛑 停止學習文件監控...")
    
    state = load_state()
    state['running'] = False
    if 'pid' in state:
        del state['pid']
    save_state(state)
    
    log("✅ 監控已停止")


def show_status():
    """顯示狀態"""
    state = load_state()
    
    print("\n📊 學習文件監控狀態")
    print("=" * 50)
    print(f"運行狀態：{'✅ 運行中' if state.get('running') else '❌ 已停止'}")
    print(f"監控目錄：{WATCH_DIR}")
    print(f"檢查間隔：{CHECK_INTERVAL/60:.0f} 分鐘")
    print(f"最後檢查：{state.get('last_check', '從未')}")
    print(f"監控文件：{len(state.get('files', {}))} 個")
    
    if state.get('running') and state.get('start_time'):
        try:
            start_time = datetime.fromisoformat(state['start_time'])
        except AttributeError:
            # Python 3.6 兼容性
            start_time = datetime.strptime(state['start_time'].replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S.%f')
        duration = datetime.now() - start_time
        print(f"運行時長：{duration}")
    
    print("=" * 50)


def main():
    """主函數"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_watcher()
    elif command == 'stop':
        stop_watcher()
    elif command == 'status':
        show_status()
    elif command == 'check':
        result = check_new_files()
        print(f"\n檢查結果：新增 {result['new']} 個，修改 {result['modified']} 個，通知 {result['notifications']} 個")
    else:
        print(f"❌ 未知命令：{command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
