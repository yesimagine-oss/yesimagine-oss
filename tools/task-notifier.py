#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
通用任务通知系统

功能:
- 任务开始通知（飞书 + webUI）
- 任务完成通知（飞书 + webUI）
- 问题卡住通知（飞书 + webUI）

使用:
    python3 task-notifier.py start "任务名称" "任务描述" "预计分钟数"
    python3 task-notifier.py end "任务名称" "成果 1，成果 2，成果 3" "备注"
    python3 task-notifier.py problem "任务名称" "问题描述" "解决方案建议"
"""

import json
import os
import sys
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# 配置
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

# 从配置文件加载
CONFIG_FILE = Path.home() / ".openclaw" / "workspace" / ".config" / "feishu-notification.json"

def load_config() -> Dict[str, Any]:
    """加载飞书配置"""
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
    """获取飞书 Access Token"""
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = requests.post(FEISHU_TOKEN_URL, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        raise Exception(f"获取飞书 Token 失败：{result}")
    return result['tenant_access_token']

def send_feishu_message(token: str, user_id: str, title: str, text: str, enable_mention: bool = True):
    """发送飞书 post 类型消息（支持@提及 + 格式化）"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 构建@提及标签
    mention_tag = {"tag": "at", "user_id": user_id} if enable_mention and user_id else None
    
    # 解析文本为多行，每行是一个元素
    lines = text.split('\n')
    content_elements = []
    
    # 第一行：@提及 + 标题
    first_line = []
    if mention_tag:
        first_line.append(mention_tag)
    first_line.append({"tag": "text", "text": f"{title}\n"})
    content_elements.append(first_line)
    
    # 添加内容行
    for line in lines:
        if line.strip():
            content_elements.append([{"tag": "text", "text": f"{line}\n"}])
    
    payload = {
        "receive_id": user_id,
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "",
                "content": content_elements
            }
        }, ensure_ascii=False)
    }
    params = {'receive_id_type': 'open_id'}
    response = requests.post(FEISHU_MESSAGE_URL, headers=headers, params=params, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        print(f"⚠️ 飞书消息发送失败：{result}")
        return False
    print(f"✅ 飞书消息发送成功（带@提及）：{result.get('data', {}).get('message_id')}")
    return True

def send_webui_message(message: str):
    """发送 webUI 消息"""
    print(f"\n📢 [webUI 通知]\n{message}\n")

def task_start(task_name: str, description: str, duration_minutes: int):
    """任务开始通知"""
    config = load_config()
    now = datetime.now()
    end_time = now + timedelta(minutes=duration_minutes)
    
    # 飞书消息
    feishu_title = f"📋 任务开始执行 - {task_name}"
    # 小型 slogan（使用小型 Unicode 字符）
    small_slogan = "*...生活太快⚡️...老逼快跑💨...*"
    
    feishu_text = f"""**任务理解**：{description}
**启动时间**：`{now.strftime('%Y-%m-%d %H:%M:%S')}`
**预计结束**：`{end_time.strftime('%Y-%m-%d %H:%M')}`
**预计时长**：{duration_minutes}分钟

🦞 RedOpenClaw
{small_slogan}"""
    
    # webUI 消息
    webui_message = f"""
## 📋 任务开始执行 - {task_name}

| 项目 | 信息 |
|------|------|
| **任务理解** | {description} |
| **启动时间** | {now.strftime('%Y-%m-%d %H:%M:%S')} |
| **预计结束** | {end_time.strftime('%Y-%m-%d %H:%M')} |
| **预计时长** | {duration_minutes}分钟 |

✅ 任务已开始，飞书 + webUI 双渠道通知已发送。

🦞 RedOpenClaw
*...生活太快⚡️...老逼快跑💨...*
"""
    
    # 发送通知
    print(f"\n🚀 任务开始通知：{task_name}")
    token = get_feishu_token(config['app_id'], config['app_secret'])
    send_feishu_message(token, config['target_user'], feishu_title, feishu_text)
    send_webui_message(webui_message)

def task_end(task_name: str, achievements: List[str], notes: str = ""):
    """任务完成通知"""
    config = load_config()
    now = datetime.now()
    
    achievements_text = "\n".join([f"✅ {item}" for item in achievements])
    
    # 禁止在飞书消息中发送服务器路径
    if notes and ('/' in notes and 'home' in notes):
        feishu_notes = "\n备注：内容已发送"
        webui_notes = notes
    else:
        feishu_notes = f"\n备注：{notes}" if notes else ""
        webui_notes = notes
    
    # 根据任务类型选择合适的标题
    task_name_lower = task_name.lower()
    if '学习' in task_name_lower or 'python' in task_name_lower:
        achievements_header = "📚 学习成效"
    elif 'evomap' in task_name_lower:
        achievements_header = "📊 成果汇报"
    elif '修复' in task_name_lower or '问题' in task_name_lower:
        achievements_header = "🔧 修复内容"
    elif '检查' in task_name_lower or '验证' in task_name_lower:
        achievements_header = "✅ 检查结果"
    elif '创建' in task_name_lower or '部署' in task_name_lower:
        achievements_header = "🚀 部署内容"
    elif '发送' in task_name_lower or '通知' in task_name_lower:
        achievements_header = "📤 发送内容"
    else:
        achievements_header = "📋 任务成果"
    
    # 飞书消息（不发送服务器路径）
    feishu_title = f"✅ 任务完成 - {task_name}"
    small_slogan = "*...生活太快⚡️...老逼快跑💨...*"
    feishu_text = f"""**任务**：{task_name}
**完成时间**：`{now.strftime('%Y-%m-%d %H:%M:%S')}`

{achievements_header}:
{achievements_text}{feishu_notes}

请验收！

---
🤖 `RedOpenClaw` | `{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}`
{small_slogan}"""
    
    # webUI 消息
    webui_message = f"""
## ✅ 任务完成 - {task_name}

| 项目 | 信息 |
|------|------|
| **完成时间** | {now.strftime('%Y-%m-%d %H:%M:%S')} |

### {achievements_header}

{achievements_text}
"""
    
    if notes:
        webui_message += f"\n### 📝 备注\n{notes}\n"
    
    webui_message += f"\n✅ 飞书 + webUI 双渠道通知已发送。\n\n---\n🤖 `RedOpenClaw` | `{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}`\n*...生活太快⚡️...老逼快跑💨...*\n"
    
    # 发送通知
    print(f"\n✅ 任务完成通知：{task_name}")
    token = get_feishu_token(config['app_id'], config['app_secret'])
    send_feishu_message(token, config['target_user'], feishu_title, feishu_text)
    send_webui_message(webui_message)

def task_problem(task_name: str, problem: str, solution: str):
    """问题卡住通知"""
    config = load_config()
    now = datetime.now()
    
    # 飞书消息
    feishu_title = f"⚠️ 任务遇到问题 - {task_name}"
    small_slogan = "*...生活太快⚡️...老逼快跑💨...*"
    feishu_text = f"""**任务**：{task_name}
**时间**：`{now.strftime('%Y-%m-%d %H:%M:%S')}`

**问题描述**：{problem}

**解决方案建议**：{solution}

请指示下一步...

---
🤖 `RedOpenClaw` | `{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}`
{small_slogan}"""
    
    # webUI 消息
    webui_message = f"""
## ⚠️ 任务遇到问题 - {task_name}

| 项目 | 信息 |
|------|------|
| **时间** | {now.strftime('%Y-%m-%d %H:%M:%S')} |

### 问题描述

{problem}

### 解决方案建议

{solution}

✅ 飞书 + webUI 双渠道通知已发送。请指示下一步...

---
🤖 `RedOpenClaw` | `{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}`
*...生活太快⚡️...老逼快跑💨...*
"""
    
    # 发送通知
    print(f"\n⚠️ 问题通知：{task_name}")
    token = get_feishu_token(config['app_id'], config['app_secret'])
    send_feishu_message(token, config['target_user'], feishu_title, feishu_text)
    send_webui_message(webui_message)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 5:
            print("用法：python3 task-notifier.py start <任务名称> <任务描述> <预计分钟数>")
            sys.exit(1)
        task_start(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    
    elif command == "end":
        if len(sys.argv) < 4:
            print("用法：python3 task-notifier.py end <任务名称> <成果 1，成果 2,...> [备注]")
            sys.exit(1)
        achievements = sys.argv[3].split('，') if '，' in sys.argv[3] else sys.argv[3].split(',')
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        task_end(sys.argv[2], achievements, notes)
    
    elif command == "problem":
        if len(sys.argv) < 5:
            print("用法：python3 task-notifier.py problem <任务名称> <问题描述> <解决方案建议>")
            sys.exit(1)
        task_problem(sys.argv[2], sys.argv[3], sys.argv[4])
    
    else:
        print(f"❌ 未知命令：{command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
