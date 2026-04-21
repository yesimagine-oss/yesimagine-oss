# 📅 飞书会议助手

**版本**: v1.0  
**创建时间**: 2026-03-13  
**作者**: OpenClaw Agent

---

## 📋 项目概述

飞书会议助手是一个基于飞书日历 API 的会议管理工具，支持会议创建、提醒发送、会议查询等功能。

### 功能特性

- ✅ 会议自动创建
- ✅ 会议提醒发送（会前提醒）
- ✅ 会议纪要生成（待扩展）
- ✅ 参会人员管理
- ✅ 会议记录追踪
- ✅ 每日站会自动创建
- ✅ 今天/本周会议查询

### 技术栈

- **语言**: Python 3.11+
- **飞书 SDK**: requests
- **日历 API**: 飞书日历 v4
- **定时任务**: APScheduler
- **配置管理**: python-dotenv

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd feishu-meeting-assistant

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 文件
vi .env

# 填写飞书应用配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxx
FEISHU_CALENDAR_ID=xxxxxxxxxxxxxxxx
```

### 3. 获取飞书应用配置

```
1. 访问 https://open.feishu.cn/
2. 注册/登录开发者账号
3. 创建应用
4. 获取 App ID 和 App Secret
5. 获取日历 ID（从飞书日历 URL 中获取）
6. 填写到 .env 文件
```

### 4. 运行会议助手

```bash
# 运行主程序
python meeting_bot.py

# 选择操作
1. 创建会议
2. 查看今天的会议
3. 查看本周的会议
4. 创建每日站会
5. 启动调度器
6. 退出
```

---

## 📖 使用说明

### 创建会议

```bash
# 运行程序
python meeting_bot.py

# 选择 1: 创建会议
# 输入会议标题、开始时间、时长等
```

### 查看会议

```bash
# 运行程序
python meeting_bot.py

# 选择 2: 查看今天的会议
# 或选择 3: 查看本周的会议
```

### 创建每日站会

```bash
# 运行程序
python meeting_bot.py

# 选择 4: 创建每日站会
# 输入站会时间（默认 9:30）
```

---

## 🛠️ 核心功能

### 1. 会议创建

```python
assistant = MeetingAssistant()

# 创建会议
event_id = assistant.create_meeting(
    title="项目评审会",
    start_time=datetime(2026, 3, 14, 14, 0),
    duration_minutes=60,
    attendees=["ou_xxx1", "ou_xxx2"],
    description="项目评审会议",
    send_reminder=True
)
```

### 2. 会议提醒

```python
# 安排会议提醒（会前 15 分钟）
assistant.schedule_meeting_reminder(
    event_id=event_id,
    title="项目评审会",
    attendees=["ou_xxx1", "ou_xxx2"],
    remind_minutes=15
)
```

### 3. 查询会议

```python
# 查询今天的会议
today_events = assistant.get_today_meetings()

# 查询本周的会议
week_events = assistant.get_week_meetings()

# 列出会议
assistant.list_meetings(today_events)
```

### 4. 每日站会

```python
# 创建每日站会（每天 9:30）
assistant.create_standup_meeting(
    hour=9,
    minute=30,
    attendees=["ou_xxx1", "ou_xxx2"]
)
```

---

## 📊 项目结构

```
feishu-meeting-assistant/
├── meeting_bot.py         # 主程序
├── .env                   # 环境变量配置
├── .env.example           # 环境配置示例
├── requirements.txt       # 依赖包
├── README.md              # 项目说明
├── logs/                  # 日志目录
│   └── meeting_YYYYMMDD.log
└── meetings.db            # 数据库文件（可选）
```

---

## 🔧 核心模块

### 1. Token 管理器

```python
class FeishuTokenManager:
    """自动获取和刷新 Token"""
    
    def get_app_access_token(self) -> str:
        # Token 有效期 2 小时，自动刷新
        pass
```

### 2. 日历客户端

```python
class CalendarClient:
    """飞书日历 API 客户端"""
    
    def create_event(self, summary, start_time, end_time, attendees, description):
        # 创建日历事件
        pass
    
    def get_events(self, time_min, time_max, max_results):
        # 查询日历事件
        pass
    
    def update_event(self, event_id, **kwargs):
        # 更新日历事件
        pass
    
    def delete_event(self, event_id):
        # 删除日历事件
        pass
```

### 3. 消息发送器

```python
class MessageSender:
    """消息发送器"""
    
    def send_meeting_reminder(self, receive_id, meeting_title, start_time, location):
        # 发送会议提醒卡片
        pass
```

### 4. 会议助手

```python
class MeetingAssistant:
    """会议助手主类"""
    
    def create_meeting(self, title, start_time, duration_minutes, attendees, description, send_reminder):
        # 创建会议
        pass
    
    def schedule_meeting_reminder(self, event_id, title, attendees, remind_minutes):
        # 安排会议提醒
        pass
    
    def get_today_meetings(self):
        # 获取今天的会议
        pass
    
    def get_week_meetings(self):
        # 获取本周的会议
        pass
    
    def create_standup_meeting(self, hour, minute, attendees):
        # 创建每日站会
        pass
```

---

## ⚠️ 常见问题

### Q1: 日历 ID 从哪里获取？

**A**: 从飞书日历 URL 中获取

```
1. 打开飞书日历
2. 进入目标日历
3. 查看 URL
4. 复制 calendar_id 参数
```

### Q2: 会议创建失败？

**A**: 检查权限配置

```
1. 开发者后台 → 应用权限
2. 添加"日历"相关权限
3. 提交审核（如需）
```

### Q3: 会议提醒未发送？

**A**: 检查消息权限

```
1. 开发者后台 → 应用权限
2. 添加"发送消息"权限
3. 检查用户 ID 是否正确
```

---

## 📈 扩展功能

### 待扩展功能

- [ ] 会议纪要生成
- [ ] 会议录制管理
- [ ] 会议冲突检测
- [ ] 会议室预订
- [ ] 会议统计报表
- [ ] Web 管理界面

### 扩展建议

```python
# 会议纪要生成
def create_meeting_notes(self, event_id: str, content: str):
    # 创建会议纪要文档
    pass

# 会议冲突检测
def check_conflict(self, start_time: datetime, end_time: datetime) -> bool:
    # 检查时间冲突
    pass
```

---

## 🔐 安全最佳实践

### 1. 保护环境变量

```bash
# ✅ 正确：使用环境变量
FEISHU_APP_SECRET=xxx

# ❌ 错误：硬编码
app_secret = "xxx"
```

### 2. 不要提交敏感信息

```bash
# 添加到 .gitignore
.env
*.db
logs/
```

### 3. 定期轮换 Secret

```
建议每 3-6 个月轮换一次 App Secret
```

---

## 📊 项目统计

### 代码统计

- **总行数**: 500+ 行
- **核心模块**: 4 个
- **API 接口**: 6 个
- **定时任务**: 2 种

### 功能统计

- **会议管理**: 4 种（创建/查询/更新/删除）
- **提醒功能**: 2 种（即时/定时）
- **查询功能**: 2 种（今天/本周）

---

## 🎯 下一步计划

### 功能扩展

- [ ] 会议纪要生成
- [ ] 会议冲突检测
- [ ] Web 管理界面

### 性能优化

- [ ] 添加缓存层
- [ ] 添加异步支持
- [ ] 添加监控告警

---

## 📝 更新日志

### v1.0 (2026-03-13)

- ✅ 初始版本
- ✅ 会议创建功能
- ✅ 会议提醒功能
- ✅ 会议查询功能
- ✅ 每日站会功能
- ✅ 日志记录

---

## 📞 获取帮助

### 文档

- 飞书开放平台：https://open.feishu.cn/
- 日历 API 文档：https://open.feishu.cn/document

### 问题反馈

- 查看日志：`logs/meeting_*.log`
- 查看 FAQ：飞书开发 FAQ.md

---

**项目版本**: v1.0  
**最后更新**: 2026-03-13  
**Python 版本**: 3.11+

📅 **飞书会议助手项目已创建！开始会议管理功能开发！**
