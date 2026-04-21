# 🤖 飞书通知机器人

**版本**: v1.0  
**创建时间**: 2026-03-13  
**作者**: OpenClaw Agent

---

## 📋 项目概述

飞书通知机器人是一个基于飞书开放平台的消息通知工具，支持定时发送、多种消息类型、发送记录追踪等功能。

### 功能特性

- ✅ 定时发送通知（日报/周报等）
- ✅ 支持多种消息类型（文本/富文本/卡片）
- ✅ 消息模板管理（日报/会议提醒/告警）
- ✅ 发送记录追踪（SQLite 数据库）
- ✅ 错误重试机制（指数退避）
- ✅ 完整的日志记录

### 技术栈

- **语言**: Python 3.11+
- **飞书 SDK**: requests
- **定时任务**: APScheduler
- **数据库**: SQLite
- **配置管理**: python-dotenv

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd feishu-notification-bot

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
```

### 3. 获取飞书应用配置

```
1. 访问 https://open.feishu.cn/
2. 注册/登录开发者账号
3. 创建应用
4. 获取 App ID 和 App Secret
5. 填写到 .env 文件
```

### 4. 运行机器人

```bash
# 运行主程序
python bot.py

# 选择操作
1. 测试发送文本消息
2. 测试发送卡片消息
3. 启动定时任务
4. 查看统计信息
5. 退出
```

---

## 📖 使用说明

### 测试发送消息

```bash
# 运行程序
python bot.py

# 选择 1: 测试发送文本消息
# 或选择 2: 测试发送卡片消息
```

### 启动定时任务

```bash
# 运行程序
python bot.py

# 选择 3: 启动定时任务
# 默认每天早上 9 点发送日报
# 按 Ctrl+C 停止
```

### 查看统计信息

```bash
# 运行程序
python bot.py

# 选择 4: 查看统计信息
# 显示发送总数、成功数、失败率等
```

---

## 🛠️ 自定义配置

### 修改日报时间

编辑 `bot.py` 中的 `start_scheduler` 方法：

```python
def start_scheduler(self):
    # 修改为每天 10 点发送
    self.scheduler.add_daily_report(self.user_id, hour=10, minute=0)
```

### 添加新的定时任务

```python
def start_scheduler(self):
    # 添加小时任务
    self.scheduler.add_interval_notification(
        self.user_id, 
        "定时测试消息", 
        seconds=3600  # 每 1 小时
    )
```

### 自定义消息模板

编辑 `MessageTemplates` 类：

```python
@staticmethod
def custom_template(title: str, content: str) -> Dict:
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "#3370ff",
            "title": {"tag": "plain_text", "content": title}
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": content}
            }
        ]
    }
```

---

## 📊 项目结构

```
feishu-notification-bot/
├── bot.py                 # 主程序
├── .env                   # 环境变量配置
├── .env.example           # 环境配置示例
├── requirements.txt       # 依赖包
├── README.md              # 项目说明
├── logs/                  # 日志目录
│   └── bot_YYYYMMDD.log
└── notifications.db       # 数据库文件
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

### 2. 消息发送器

```python
class MessageSender:
    """消息发送器"""
    
    def send_text(self, receive_id: str, text: str) -> bool:
        # 发送文本消息
        pass
    
    def send_card(self, receive_id: str, card_content: Dict) -> bool:
        # 发送卡片消息
        pass
    
    def send_with_retry(self, receive_id: str, text: str, max_retries: int = 3) -> bool:
        # 带重试的发送
        pass
```

### 3. 消息模板

```python
class MessageTemplates:
    """消息模板"""
    
    @staticmethod
    def daily_report(title: str, content: str) -> Dict:
        # 日报模板
        pass
    
    @staticmethod
    def meeting_reminder(meeting_title: str, start_time: str) -> Dict:
        # 会议提醒模板
        pass
    
    @staticmethod
    def alert_message(alert_level: str, title: str, content: str) -> Dict:
        # 告警消息模板
        pass
```

### 4. 定时任务调度器

```python
class NotificationScheduler:
    """通知调度器"""
    
    def add_daily_report(self, receive_id: str, hour: int = 9, minute: int = 0):
        # 添加日报任务
        pass
    
    def add_interval_notification(self, receive_id: str, text: str, seconds: int = 3600):
        # 添加间隔通知任务
        pass
```

---

## 📝 日志说明

### 日志位置

```
logs/bot_YYYYMMDD.log
```

### 日志级别

- **INFO**: 正常操作日志
- **WARNING**: 警告信息
- **ERROR**: 错误信息

### 查看日志

```bash
# 实时查看日志
tail -f logs/bot_$(date +%Y%m%d).log

# 查看错误日志
grep ERROR logs/bot_*.log
```

---

## ⚠️ 常见问题

### Q1: Token 获取失败？

**A**: 检查 App ID 和 App Secret 是否正确

```bash
# 检查 .env 文件
cat .env

# 确保没有空格和引号
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

### Q2: 消息发送失败？

**A**: 检查用户 ID 是否正确，应用权限是否配置

```
1. 检查 FEISHU_USER_ID 是否正确
2. 开发者后台 → 应用权限 → 添加"发送消息"权限
3. 检查网络连接
```

### Q3: 定时任务不执行？

**A**: 检查调度器是否启动，时区是否正确

```python
# 确保调用了 start_scheduler()
# 检查系统时区是否正确
```

---

## 📈 性能优化

### 1. 连接池

```python
# 使用 requests.Session
session = requests.Session()
```

### 2. 批量发送

```python
# 批量发送消息
for user_id in user_ids:
    sender.send_text(user_id, text)
```

### 3. 错误重试

```python
# 使用指数退避
sender.send_with_retry(user_id, text, max_retries=3)
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

- **总行数**: 600+ 行
- **核心模块**: 6 个
- **消息模板**: 3 个
- **定时任务**: 2 种

### 功能统计

- **消息类型**: 3 种（文本/富文本/卡片）
- **模板类型**: 3 种（日报/会议/告警）
- **定时任务**: 2 种（日报/间隔）

---

## 🎯 下一步计划

### 功能扩展

- [ ] 添加 Web 管理界面
- [ ] 添加用户管理
- [ ] 添加消息队列
- [ ] 添加多应用支持

### 性能优化

- [ ] 添加缓存层
- [ ] 添加异步支持
- [ ] 添加监控告警

---

## 📝 更新日志

### v1.0 (2026-03-13)

- ✅ 初始版本
- ✅ 基础消息发送
- ✅ 定时任务支持
- ✅ 日志记录
- ✅ 错误重试

---

## 📞 获取帮助

### 文档

- 飞书开放平台：https://open.feishu.cn/
- API 文档：https://open.feishu.cn/document

### 问题反馈

- 查看日志：`logs/bot_*.log`
- 查看 FAQ：飞书开发 FAQ.md

---

**项目版本**: v1.0  
**最后更新**: 2026-03-13  
**Python 版本**: 3.11+

🤖 **飞书通知机器人项目已创建！开始实际项目开发！**
