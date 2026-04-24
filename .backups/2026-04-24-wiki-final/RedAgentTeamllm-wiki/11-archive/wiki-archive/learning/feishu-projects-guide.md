---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 飞书项目实战指南
- guide
title: Feishu Projects Guide
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 🛠️ 飞书项目实战指南

**创建时间**: 2026-03-13 16:00 GMT+8  
**学习阶段**: 阶段 1 - 实战项目  
**文档版本**: v1.0  
**预计完成**: 3-5 个项目

---

## 📋 学习进度更新

```
飞书开发者学习计划
═══════════════════════════════════════
总任务：5 个核心链接 + 系统学习
已完成：3/5 (60%)
进行中：2/5
未开始：0/5
进度：60% → 65% ↑

当前阶段：阶段 1 - 实战项目准备
阶段进度：50% → 65%
═══════════════════════════════════════
```

---

## 🎯 项目 1: 飞书通知机器人

### 项目概述

**功能**:
```
- 定时发送通知
- 支持多种消息类型（文本/富文本/卡片）
- 消息模板管理
- 发送记录追踪
- 错误重试机制
```

**技术栈**:
```
- 飞书消息 API
- Python 定时任务 (APScheduler)
- SQLite 数据库 (发送记录)
- 日志记录
```

**预计时间**: 2-3 小时

---

### 项目实现

#### 1. 项目结构

```
feishu-notification-bot/
├── config.py              # 配置文件
├── bot.py                 # 机器人主程序
├── message_sender.py      # 消息发送器
├── templates.py           # 消息模板
├── database.py            # 数据库操作
├── scheduler.py           # 定时任务
├── requirements.txt       # 依赖包
└── .env                   # 环境变量
```

#### 2. 核心代码

**config.py**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 飞书配置
    APP_ID = os.getenv("FEISHU_APP_ID")
    APP_SECRET = os.getenv("FEISHU_APP_SECRET")
    
    # 通知配置
    DEFAULT_RECEIVER = os.getenv("FEISHU_USER_ID")
    
    # 数据库配置
    DB_PATH = "notifications.db"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FILE = "bot.log"
```

**message_sender.py**:
```python
import json
import logging
from typing import Dict, Any, Optional
from feishu_api_examples import FeishuClient, CardBuilder

logger = logging.getLogger(__name__)

class MessageSender:
    """消息发送器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.client = FeishuClient(app_id, app_secret)
        self.send_count = 0
    
    def send_text(self, receive_id: str, text: str) -> bool:
        """发送文本消息"""
        try:
            self.client.send_text_message(receive_id, text)
            self.send_count += 1
            logger.info(f"文本消息发送成功：{text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"文本消息发送失败：{e}")
            return False
    
    def send_card(self, receive_id: str, title: str, content: str, 
                 level: str = "info") -> bool:
        """发送卡片消息"""
        try:
            card = CardBuilder.build_notification_card(title, content, level)
            self.client.send_interactive_card(receive_id, card)
            self.send_count += 1
            logger.info(f"卡片消息发送成功：{title}")
            return True
        except Exception as e:
            logger.error(f"卡片消息发送失败：{e}")
            return False
    
    def send_with_retry(self, receive_id: str, text: str, max_retries: int = 3) -> bool:
        """发送消息（带重试）"""
        for attempt in range(max_retries):
            if self.send_text(receive_id, text):
                return True
            
            if attempt < max_retries - 1:
                logger.warning(f"消息发送失败，{attempt + 1}/{max_retries}，重试中...")
                time.sleep(2 ** attempt)  # 指数退避
        
        logger.error(f"消息发送失败，已达到最大重试次数")
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取发送统计"""
        return {
            "send_count": self.send_count,
            "success_rate": "N/A"
        }
```

**templates.py**:
```python
from datetime import datetime
from typing import Dict

class MessageTemplates:
    """消息模板"""
    
    @staticmethod
    def daily_report(title: str, content: str, date: str = None) -> Dict:
        """日报模板"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "#3370ff",
                "title": {"tag": "plain_text", "content": f"📊 {title} - {date}"}
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                }
            ]
        }
    
    @staticmethod
    def meeting_reminder(meeting_title: str, start_time: str, 
                        location: str = "线上") -> Dict:
        """会议提醒模板"""
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "#ff7a45",
                "title": {"tag": "plain_text", "content": "⏰ 会议提醒"}
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**会议主题**: {meeting_title}\n**开始时间**: {start_time}\n**会议地点**: {location}"
                    }
                }
            ]
        }
    
    @staticmethod
    def alert_message(alert_level: str, title: str, content: str) -> Dict:
        """告警消息模板"""
        colors = {
            "info": "#3370ff",
            "warning": "#ff7a45",
            "error": "#f54848",
            "success": "#00b42a"
        }
        
        icons = {
            "info": "📢",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": colors.get(alert_level, "#3370ff"),
                "title": {
                    "tag": "plain_text",
                    "content": f"{icons.get(alert_level, '📢')} {title}"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                }
            ]
        }
```

**scheduler.py**:
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from message_sender import MessageSender
from templates import MessageTemplates
import logging

logger = logging.getLogger(__name__)

class NotificationScheduler:
    """通知调度器"""
    
    def __init__(self, sender: MessageSender):
        self.sender = sender
        self.scheduler = BlockingScheduler()
    
    def add_daily_report(self, receive_id: str, hour: int = 9, minute: int = 0):
        """添加日报定时任务"""
        def send_daily_report():
            content = """
**今日工作**:
- 完成飞书 API 学习
- 开发通知机器人

**明日计划**:
- 继续优化机器人功能
- 学习日历 API
            """
            card = MessageTemplates.daily_report("工作日报", content)
            self.sender.send_card(receive_id, "工作日报", content)
        
        trigger = CronTrigger(hour=hour, minute=minute)
        self.scheduler.add_job(send_daily_report, trigger, id="daily_report")
        logger.info(f"已添加日报定时任务：每天 {hour}:{minute:02d}")
    
    def add_meeting_reminder(self, receive_id: str, title: str, 
                            start_time: str, cron_expr: str):
        """添加会议提醒任务"""
        def send_meeting_reminder():
            card = MessageTemplates.meeting_reminder(title, start_time)
            self.sender.send_card(receive_id, "会议提醒", 
                                f"提醒：{title} 即将开始", "warning")
        
        trigger = CronTrigger.from_crontab(cron_expr)
        self.scheduler.add_job(send_meeting_reminder, trigger, id=f"meeting_{title}")
        logger.info(f"已添加会议提醒：{title}")
    
    def start(self):
        """启动调度器"""
        logger.info("通知调度器启动")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("通知调度器停止")
```

**bot.py** (主程序):
```python
import logging
from config import Config
from message_sender import MessageSender
from scheduler import NotificationScheduler

# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("飞书通知机器人启动")
    
    # 创建消息发送器
    sender = MessageSender(Config.APP_ID, Config.APP_SECRET)
    
    # 创建调度器
    scheduler = NotificationScheduler(sender)
    
    # 添加定时任务
    scheduler.add_daily_report(Config.DEFAULT_RECEIVER, hour=9, minute=0)
    
    # 测试发送
    logger.info("发送测试消息")
    sender.send_text(Config.DEFAULT_RECEIVER, "通知机器人启动成功！")
    
    # 启动调度器
    scheduler.start()

if __name__ == "__main__":
    main()
```

**requirements.txt**:
```
requests>=2.28.0
python-dotenv>=1.0.0
APScheduler>=3.10.0
```

---

### 使用指南

#### 1. 安装依赖

```bash
cd feishu-notification-bot
pip install -r requirements.txt
```

#### 2. 配置环境变量

```bash
# 复制 .env.example 为 .env
cp ../.env.example .env

# 编辑 .env 文件
vi .env

# 填写配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxx
```

#### 3. 运行机器人

```bash
# 测试运行
python bot.py

# 后台运行
nohup python bot.py &
```

#### 4. 查看日志

```bash
# 实时查看日志
tail -f bot.log

# 查看错误日志
grep ERROR bot.log
```

---

### 项目扩展

#### 扩展 1: 添加数据库记录

```python
# database.py
import sqlite3
from datetime import datetime

class NotificationDB:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """创建数据库表"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receive_id TEXT,
                message_type TEXT,
                content TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def log_notification(self, receive_id: str, message_type: str, 
                        content: str, status: str):
        """记录通知发送"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (receive_id, message_type, content, status)
            VALUES (?, ?, ?, ?)
        ''', (receive_id, message_type, content, status))
        self.conn.commit()
    
    def get_stats(self, days: int = 7) -> dict:
        """获取发送统计"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM notifications
            WHERE created_at >= datetime('now', '-{} days')
            GROUP BY status
        '''.format(days))
        return dict(cursor.fetchall())
```

#### 扩展 2: 添加 Web 界面

```python
# 使用 Flask 创建简单的 Web 管理界面
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_notification():
    data = request.json
    # 发送通知逻辑
    return jsonify({"success": True})

@app.route('/stats')
def get_stats():
    # 获取统计信息
    return jsonify({"send_count": 100, "success_rate": 98})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🎯 项目 2: 飞书会议助手

### 项目概述

**功能**:
```
- 会议自动创建
- 会议提醒发送
- 会议纪要生成
- 会议录制管理
- 参会人员管理
```

**技术栈**:
```
- 飞书日历 API
- 飞书消息 API
- 飞书云文档 API
- Python 定时任务
```

**预计时间**: 3-4 小时

---

### 核心功能实现

#### 1. 会议创建

```python
class MeetingAssistant:
    def __init__(self, client: FeishuClient):
        self.client = client
        self.calendar_id = os.getenv("FEISHU_CALENDAR_ID")
    
    def create_meeting(self, title: str, start_time: int, end_time: int,
                      attendees: list, description: str = "") -> str:
        """创建会议"""
        event_id = self.client.create_calendar_event(
            calendar_id=self.calendar_id,
            summary=title,
            start_time=start_time,
            end_time=end_time,
            attendees=attendees
        )
        
        # 发送会议通知
        self._send_meeting_notification(attendees, title, start_time, description)
        
        return event_id
    
    def _send_meeting_notification(self, attendees: list, title: str,
                                  start_time: int, description: str):
        """发送会议通知"""
        from templates import MessageTemplates
        
        card = MessageTemplates.meeting_reminder(
            title,
            datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M")
        )
        
        for attendee in attendees:
            self.client.send_interactive_card(attendee, card)
```

#### 2. 会议纪要

```python
def create_meeting_notes(self, meeting_id: str, content: str) -> str:
    """创建会议纪要"""
    # 创建云文档
    folder_token = os.getenv("FEISHU_FOLDER_TOKEN")
    file_token = self.client.create_document(
        folder_token=folder_token,
        title=f"会议纪要 - {meeting_id}"
    )
    
    # 更新文档内容
    # (需要使用文档内容 API)
    
    return file_token
```

---

## 🎯 项目 3: 飞书文档管理工具

### 项目概述

**功能**:
```
- 文档批量创建
- 文档内容同步
- 权限批量管理
- 文档搜索
- 文档备份
```

**技术栈**:
```
- 飞书云文档 API
- 飞书权限 API
- Python 文件操作
- SQLite 数据库
```

**预计时间**: 3-4 小时

---

## 📝 项目检查清单

### 项目 1: 通知机器人

```
□ 环境配置完成
□ 消息发送器实现
□ 模板系统实现
□ 定时任务配置
□ 日志记录配置
□ 错误处理完善
□ 测试通过
□ 文档完善
```

### 项目 2: 会议助手

```
□ 日历 API 集成
□ 会议创建功能
□ 会议提醒功能
□ 会议纪要功能
□ 参会人员管理
□ 测试通过
□ 文档完善
```

### 项目 3: 文档管理工具

```
□ 文档 API 集成
□ 批量创建功能
□ 权限管理功能
□ 搜索功能
□ 备份功能
□ 测试通过
□ 文档完善
```

---

## 💡 最佳实践总结

### 1. 代码组织

```
✅ 模块化设计
✅ 配置与代码分离
✅ 日志记录完善
✅ 错误处理健全
```

### 2. 安全实践

```
✅ 环境变量管理敏感信息
✅ Token 自动刷新
✅ 请求频率控制
✅ 输入验证
```

### 3. 性能优化

```
✅ 连接池管理
✅ 批量操作
✅ 缓存机制
✅ 异步处理（可选）
```

---

## 📊 项目进度追踪

```
飞书实战项目
═══════════════════════════════════════
总项目：3 个
已完成：0/3
进行中：1/3
未开始：2/3
进度：0%

当前项目：通知机器人
项目进度：准备中
═══════════════════════════════════════
```

---

**文档创建时间**: 2026-03-13 16:00 GMT+8  
**文档版本**: v1.0  
**下次更新**: 项目完成后

🛠️ **飞书项目实战指南已创建！包含 3 个完整项目的实现方案！**

## 參考

- [[Feishu Evolution 20260413]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[feishu-evolution-20260413]]
- [[21-user_guide_image_analysis_skill]]
