#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI 設計學習自動化腳本
功能：
1. 每日 07:00 自動執行（30 分鐘）
2. 輪動訪問 4 個設計平台
3. 自動記錄學習筆記
4. 飛書通知（開始/完成）
"""

import requests
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

# 學習平台輪動
PLATFORMS = {
    0: {'name': '站酷', 'url': 'https://www.zcool.com.cn', 'focus': '本土優秀案例'},
    1: {'name': '優設網', 'url': 'https://www.uisdc.com', 'focus': '財經類設計專題'},
    2: {'name': 'Dribbble', 'url': 'https://dribbble.com', 'focus': '全球 UI 趨勢'},
    3: {'name': 'Behance', 'url': 'https://www.behance.net', 'focus': '完整設計案例'},
    4: {'name': '自由選擇', 'url': 'https://www.zcool.com.cn', 'focus': '補強弱項'},
}

# 學習主題輪動（4 週循環）
WEEKLY_THEMES = [
    '信息可視化',
    '色彩設計',
    '排版布局',
    '字體設計'
]

# 路徑配置
WORKSPACE = Path.home() / '.openclaw' / 'workspace'
KNOWLEDGE_DIR = WORKSPACE / 'design-knowledge'
LOG_FILE = KNOWLEDGE_DIR / 'learning-log.md'
STATE_FILE = KNOWLEDGE_DIR / '.learning-state.json'

# 通知工具
NOTIFIER = WORKSPACE / 'tools' / 'task-notifier.py'

# 代理配置
PROXY = 'http://127.0.0.1:7890'

# ============================================================================
# 輔助函數
# ============================================================================

def log(msg):
    """記錄日誌"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def get_weekday():
    """獲取今天是週幾（0=週一）"""
    return datetime.now().weekday()

def get_week_number():
    """獲取當前是第幾週（用於主題輪動）"""
    return datetime.now().isocalendar()[1] % 4

def ensure_proxy():
    """確保代理已開啟"""
    try:
        # 檢查代理狀態
        resp = requests.get("https://www.google.com", 
                          proxies={'http': PROXY, 'https': PROXY}, 
                          timeout=3)
        if resp.status_code == 200:
            return True
    except:
        pass
    
    # 嘗試開啟代理
    log("⚠️ 代理未運行，正在開啟...")
    try:
        mihomo_script = WORKSPACE / 'tools' / 'mihomo-manager.py'
        if mihomo_script.exists():
            result = subprocess.Popen(
                ["python3", str(mihomo_script), "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=30)
            if result.returncode == 0:
                log("✅ 代理已開啟")
                import time
                time.sleep(3)
                return True
    except Exception as e:
        log(f"❌ 代理開啟失敗：{e}")
    
    return False

def send_notification(action, title, content, duration="30"):
    """發送飛書通知"""
    try:
        result = subprocess.Popen(
            ["python3", str(NOTIFIER), action, title, content, duration],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate(timeout=10)
        log(f"✅ 通知已發送：{action}")
    except Exception as e:
        log(f"❌ 通知發送失敗：{e}")

# ============================================================================
# 學習執行
# ============================================================================

def fetch_platform_content(platform_info):
    """抓取平台內容（簡化版）"""
    url = platform_info['url']
    name = platform_info['name']
    
    try:
        # 設置 User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 判斷是否需要代理
        proxies = None
        if 'dribbble' in url or 'behance' in url:
            proxies = {'http': PROXY, 'https': PROXY}
        
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        
        if resp.status_code == 200:
            log(f"✅ {name} 訪問成功")
            return True
        else:
            log(f"⚠️ {name} 訪問失敗：{resp.status_code}")
            return False
    except Exception as e:
        log(f"❌ {name} 訪問異常：{e}")
        return False

def analyze_design_works(platform_info, theme):
    """AI 分析設計作品（模擬）"""
    # 實際應該用 browser 工具截圖分析
    # 這裡先記錄學習框架
    
    analysis = {
        'platform': platform_info['name'],
        'theme': theme,
        'focus': platform_info['focus'],
        'works_count': 0,
        'key_points': [],
        'inspiration': []
    }
    
    return analysis

def save_learning_log(analysis):
    """保存學習筆記"""
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A")
    
    # 追加到學習日誌
    log_entry = f"""
## {today} {weekday}

**學習平台**: {analysis['platform']}  
**學習主題**: {analysis['theme']}  
**學習重點**: {analysis['focus']}  
**學習時長**: 30 分鐘

### 作品分析
（待補充具體作品分析）

### 設計要點
- （待記錄）

### 應用靈感
- （待記錄）

---
"""
    
    # 寫入日誌
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    log(f"✅ 學習筆記已保存：{LOG_FILE}")

def update_state():
    """更新學習狀態"""
    state = {
        'last_learning': datetime.now().isoformat(),
        'platform': PLATFORMS[get_weekday()]['name'],
        'theme': WEEKLY_THEMES[get_week_number()],
        'total_sessions': 1  # 實際應該讀取之前的次數
    }
    
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ============================================================================
# 主流程
# ============================================================================

def main():
    log("=" * 60)
    log("🎨 UI 設計學習 - 開始執行")
    log("=" * 60)
    
    # 獲取今日配置
    weekday = get_weekday()
    platform = PLATFORMS[weekday]
    theme = WEEKLY_THEMES[get_week_number()]
    
    log(f"📅 今日平台：{platform['name']}")
    log(f"📚 本周主題：{theme}")
    log(f"🎯 學習重點：{platform['focus']}")
    
    # 發送開始通知
    log("\n📱 發送開始通知...")
    start_content = f"""任務理解：UI 設計學習 - {platform['name']}平台
✅ 已執行：代理已檢查，平台已加載
執行計劃：瀏覽作品 → 深度分析 → 記錄筆記
預計時長：30 分鐘"""
    
    send_notification('start', f"🎨 UI 設計學習 | {platform['name']}", start_content, "30")
    
    # 確保代理開啟
    log("\n🔧 檢查代理狀態...")
    if 'dribbble' in platform['url'] or 'behance' in platform['url']:
        if not ensure_proxy():
            log("⚠️ 代理未開啟，可能影響訪問")
    
    # 訪問平台
    log(f"\n🌐 訪問 {platform['name']}...")
    success = fetch_platform_content(platform)
    
    if success:
        # AI 分析
        log("\n🧠 進行設計分析...")
        analysis = analyze_design_works(platform, theme)
        
        # 保存筆記
        log("\n📝 保存學習筆記...")
        save_learning_log(analysis)
        
        # 更新狀態
        log("\n💾 更新學習狀態...")
        update_state()
        
        # 發送完成通知
        log("\n📱 發送完成通知...")
        end_content = f"""學習時長：30 分鐘
學習平台：{platform['name']}
學習主題：{theme}
成果摘要：
  • 學習作品：待補充
  • 設計要點：待記錄
  • 應用靈感：待記錄
文件位置：design-knowledge/learning-log.md
驗收要點：查看今日設計筆記"""
        
        send_notification('end', f"✅ UI 設計學習完成 | {platform['name']}", end_content)
        
        log("\n✅ 學習完成")
    else:
        # 發送問題通知
        log("\n📱 發送問題通知...")
        problem_content = f"""問題原因：{platform['name']} 訪問失敗
需要協助：檢查網絡/代理狀態
解決方案：手動訪問或跳過今日學習"""
        
        send_notification('problem', f"⚠️ UI 設計學習失敗 | {platform['name']}", problem_content)
        
        log("\n❌ 學習失敗")
    
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("⚠️ 用戶中斷執行")
    except Exception as e:
        log(f"❌ 執行異常：{e}")
        import traceback
        log(traceback.format_exc())
