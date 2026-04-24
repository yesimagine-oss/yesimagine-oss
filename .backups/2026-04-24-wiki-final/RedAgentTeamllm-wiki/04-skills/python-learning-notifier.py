#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
Python 學習自動化通知系統

功能:
1. 學習開始通知 (飛書 + webUI)
2. 學習結束通知 (飛書 + webUI)
3. 停滯超時警告 (飛書 + webUI)
4. 雙渠道同步通知

Usage:
    python python-learning-notifier.py start          # 開始學習
    python python-learning-notifier.py end            # 結束學習
    python python-learning-notifier.py check-stall    # 檢查停滯
    python python-learning-notifier.py status         # 查看狀態
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

# 配置路徑
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / ".config"
STATE_FILE = CONFIG_DIR / "python-learning-state.json"
NOTIFICATION_CONFIG = CONFIG_DIR / "feishu-notification.json"

# 飛書 API
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


class LearningNotifier:
    def __init__(self):
        self.state = self._load_state()
        self.config = self._load_notification_config()
        
    def _load_state(self) -> Dict[str, Any]:
        """加載學習狀態"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": 1,
            "currentSession": None,
            "config": {
                "expectedDuration": 10800,  # 3 小時
                "stallThreshold": 3600,      # 1 小時
                "checkInterval": 300         # 5 分鐘
            },
            "sessions": []
        }
    
    def _save_state(self):
        """保存學習狀態"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def _load_notification_config(self) -> Dict[str, Any]:
        """加載通知配置"""
        if NOTIFICATION_CONFIG.exists():
            with open(NOTIFICATION_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_feishu_token(self) -> str:
        """獲取飛書 Access Token"""
        app_id = self.config.get('app', {}).get('appId', 'cli_a929676f8bf81cc7')
        app_secret = self.config.get('app', {}).get('appSecret', 'xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs')
        
        payload = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(FEISHU_TOKEN_URL, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') != 0:
            raise Exception(f"獲取飛書 Token 失敗：{result}")
        
        return result['tenant_access_token']
    
    def _send_feishu_message(self, msg_type: str, content: Dict[str, Any]):
        """發送飛書消息"""
        token = self._get_feishu_token()
        user_id = self.config.get('pythonLearning', {}).get('targetId', 'ou_f4919832188bcc630f8f257497fa93a4')
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "receive_id": user_id,
            "msg_type": msg_type,
            "content": json.dumps(content, ensure_ascii=False)
        }
        
        params = {'receive_id_type': 'open_id'}
        response = requests.post(FEISHU_MESSAGE_URL, headers=headers, params=params, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') != 0:
            print(f"⚠️ 飛書消息發送失敗：{result}")
        else:
            print(f"✅ 飛書消息發送成功：{result.get('data', {}).get('message_id')}")
        
        return result
    
    def _send_webui_message(self, message: str):
        """發送 webUI 消息 (通過 stdout)"""
        print(f"\n📢 [webUI 通知]\n{message}\n")
    
    def start_learning(self, day: str, content: str, expected_duration: int = 10800):
        """開始學習通知"""
        now = datetime.now()
        end_time = now + timedelta(seconds=expected_duration)
        
        session = {
            "id": f"day_{day}_{int(now.timestamp())}",
            "day": day,
            "content": content,
            "startTime": now.isoformat(),
            "expectedEndTime": end_time.isoformat(),
            "expectedDuration": expected_duration,
            "status": "in_progress",
            "lastActivity": now.isoformat()
        }
        
        self.state['currentSession'] = session
        self.state['sessions'].append(session)
        self._save_state()
        
        # 飛書消息內容 (富文本格式)
        feishu_content = {
            "title": f"🐍 Python 學習任務啟動 - Day {day}",
            "text": f"學習內容：{content}\n啟動時間：{now.strftime('%Y-%m-%d %H:%M')}\n預計結束：{end_time.strftime('%Y-%m-%d %H:%M')}\n預計時長：{expected_duration // 3600}小時\n\n查看學習計劃：https://www.python.org"
        }
        
        # webUI 消息
        webui_message = f"""
## 🐍 Python 學習任務啟動 - Day {day}

| 項目 | 信息 |
|------|------|
| **學習內容** | {content} |
| **啟動時間** | {now.strftime('%Y-%m-%d %H:%M')} |
| **預計結束** | {end_time.strftime('%Y-%m-%d %H:%M')} |
| **預計時長** | {expected_duration // 3600}小時 |

✅ 學習已開始，系統將自動監控進度並發送通知。
"""
        
        # 發送通知
        print(f"\n🚀 開始學習通知 (Day {day})")
        self._send_feishu_message("text", feishu_content)
        self._send_webui_message(webui_message)
        
        return session
    
    def end_learning(self, actual_content: str, achievements: list, notes: str = ""):
        """結束學習通知"""
        if not self.state['currentSession']:
            print("⚠️ 沒有進行中的學習會話")
            return
        
        session = self.state['currentSession']
        now = datetime.now()
        start_time_str = session['startTime'].replace('Z', '+00:00') if session['startTime'].endswith('Z') else session['startTime']
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except AttributeError:
            from datetime import datetime as dt
            import re
            start_time = dt.strptime(re.sub(r'\+08:00$', '', start_time_str), '%Y-%m-%dT%H:%M:%S.%f')
        actual_duration = (now - start_time).total_seconds()
        
        # 更新會話狀態
        session['endTime'] = now.isoformat()
        session['actualDuration'] = actual_duration
        session['actualContent'] = actual_content
        session['achievements'] = achievements
        session['notes'] = notes
        session['status'] = 'completed'
        
        self.state['currentSession'] = None
        self._save_state()
        
        # 飛書消息內容 (富文本格式)
        achievements_text = "\n".join([f"✅ {item}" for item in achievements])
        notes_text = f"\n備註：{notes}" if notes else ""
        
        feishu_content = {
            "title": f"🐍 Python 學習任務完成 - Day {session['day']}",
            "text": f"學習內容：{actual_content}\n學習時長：{actual_duration // 3600}小時{int((actual_duration % 3600) / 60)}分鐘\n完成時間：{now.strftime('%Y-%m-%d %H:%M')}\n\n學習成效:\n{achievements_text}{notes_text}"
        }
        
        # webUI 消息
        webui_message = f"""
## 🐍 Python 學習任務完成 - Day {session['day']}

| 項目 | 信息 |
|------|------|
| **學習內容** | {actual_content} |
| **學習時長** | {actual_duration // 3600}小時{int((actual_duration % 3600) / 60)}分鐘 |
| **完成時間** | {now.strftime('%Y-%m-%d %H:%M')} |

### 📊 學習成效

{achievements_text}
"""
        
        if notes:
            webui_message += f"\n### 📝 備註\n{notes}\n"
        
        # 發送通知
        print(f"\n✅ 結束學習通知 (Day {session['day']})")
        self._send_feishu_message("text", feishu_content)
        self._send_webui_message(webui_message)
        
        return session
    
    def check_stall(self):
        """檢查學習停滯"""
        if not self.state['currentSession']:
            print("ℹ️ 沒有進行中的學習會話")
            return
        
        session = self.state['currentSession']
        now = datetime.now()
        last_activity_str = session['lastActivity'].replace('Z', '+00:00') if session['lastActivity'].endswith('Z') else session['lastActivity']
        try:
            last_activity = datetime.fromisoformat(last_activity_str)
        except AttributeError:
            from datetime import datetime as dt
            import re
            last_activity = dt.strptime(re.sub(r'\+08:00$', '', last_activity_str), '%Y-%m-%dT%H:%M:%S.%f')
        stall_duration = (now - last_activity).total_seconds()
        stall_threshold = self.state['config'].get('stallThreshold', 3600)
        
        if stall_duration > stall_threshold:
            # 發送停滯警告 (富文本格式)
            feishu_content = {
                "title": f"⚠️ Python 學習停滯提醒 - Day {session['day']}",
                "text": f"學習內容：{session['content']}\n停滯時長：{stall_duration // 60}分鐘\n最後活動：{last_activity.strftime('%Y-%m-%d %H:%M')}\n\n遇到問題了嗎？需要幫助嗎？\n請告訴我具體卡住的地方，我會提供解決方案建議。"
            }
            
            webui_message = f"""
## ⚠️ Python 學習停滯提醒 - Day {session['day']}

| 項目 | 信息 |
|------|------|
| **學習內容** | {session['content']} |
| **停滯時長** | {stall_duration // 60}分鐘 |
| **最後活動** | {last_activity.strftime('%Y-%m-%d %H:%M')} |

🤔 遇到問題了嗎？

請告訴我：
1. 具體卡在哪個知識點？
2. 遇到了什麼錯誤或困惑？
3. 已經嘗試過哪些方法？

我會立即提供解決方案建議！
"""
            
            print(f"\n⚠️ 檢測到學習停滯 ({stall_duration // 60}分鐘)")
            self._send_feishu_message("text", feishu_content)
            self._send_webui_message(webui_message)
        else:
            print(f"✅ 學習正常進行中 (距最後活動 {stall_duration // 60}分鐘)")
    
    def status(self):
        """查看當前狀態"""
        if not self.state['currentSession']:
            print("ℹ️ 當前沒有進行中的學習會話")
            return
        
        session = self.state['currentSession']
        now = datetime.now()
        start_time_str = session['startTime'].replace('Z', '+00:00') if session['startTime'].endswith('Z') else session['startTime']
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except AttributeError:
            from datetime import datetime as dt
            import re
            start_time = dt.strptime(re.sub(r'\+08:00$', '', start_time_str), '%Y-%m-%dT%H:%M:%S.%f')
        elapsed = (now - start_time).total_seconds()
        expected = session.get('expectedDuration', 10800)
        progress = min(100, int(elapsed / expected * 100))
        
        print(f"""
## 🐍 Python 學習進度 - Day {session['day']}

| 項目 | 信息 |
|------|------|
| **學習內容** | {session['content']} |
| **已用時長** | {elapsed // 60}分鐘 |
| **預計時長** | {expected // 60}分鐘 |
| **進度** | {progress}% |
| **狀態** | {session['status']} |
| **最後活動** | {session['lastActivity']} |
""")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    notifier = LearningNotifier()
    command = sys.argv[1]
    
    if command == "start":
        day = sys.argv[2] if len(sys.argv) > 2 else "1"
        content = sys.argv[3] if len(sys.argv) > 3 else "Python 基礎語法"
        duration = int(sys.argv[4]) if len(sys.argv) > 4 else 10800
        notifier.start_learning(day, content, duration)
    
    elif command == "end":
        content = sys.argv[2] if len(sys.argv) > 2 else "Python 基礎語法"
        achievements = sys.argv[3].split(',') if len(sys.argv) > 3 else ["完成學習內容"]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        notifier.end_learning(content, achievements, notes)
    
    elif command == "check-stall":
        notifier.check_stall()
    
    elif command == "status":
        notifier.status()
    
    elif command == "update-activity":
        if notifier.state['currentSession']:
            notifier.state['currentSession']['lastActivity'] = datetime.now().isoformat()
            notifier._save_state()
            print("✅ 活動時間已更新")
        else:
            print("⚠️ 沒有進行中的學習會話")
    
    else:
        print(f"❌ 未知命令：{command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
