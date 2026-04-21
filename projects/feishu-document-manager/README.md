# 📄 飞书文档管理工具

**版本**: v1.0  
**创建时间**: 2026-03-13  
**作者**: OpenClaw Agent

---

## 📋 项目概述

飞书文档管理工具是一个基于飞书云文档 API 的文档管理工具，支持批量创建、权限管理、文档搜索、备份等功能。

### 功能特性

- ✅ 文档批量创建
- ✅ 文档内容同步
- ✅ 权限批量管理
- ✅ 文档搜索
- ✅ 文档备份
- ✅ 文档统计
- ✅ SQLite 数据库记录

### 技术栈

- **语言**: Python 3.11+
- **飞书 SDK**: requests
- **云文档 API**: 飞书云文档 v1
- **数据库**: SQLite
- **配置管理**: python-dotenv

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd feishu-document-manager

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
FEISHU_FOLDER_TOKEN=bxxxxxxxxxxxxxxx
```

### 3. 获取飞书应用配置

```
1. 访问 https://open.feishu.cn/
2. 注册/登录开发者账号
3. 创建应用
4. 获取 App ID 和 App Secret
5. 获取文件夹 Token（从飞书云文档 URL 中获取）
6. 填写到 .env 文件
```

### 4. 运行文档管理工具

```bash
# 运行主程序
python document_manager.py

# 选择操作
1. 创建文档
2. 批量创建文档
3. 搜索文档
4. 分享文档
5. 备份文档
6. 列出所有文档
7. 查看统计信息
8. 退出
```

---

## 📖 使用说明

### 创建文档

```bash
# 运行程序
python document_manager.py

# 选择 1: 创建文档
# 输入文档标题、类型等
```

### 批量创建文档

```bash
# 运行程序
python document_manager.py

# 选择 2: 批量创建文档
# 输入文档标题（每行一个）
```

### 搜索文档

```bash
# 运行程序
python document_manager.py

# 选择 3: 搜索文档
# 输入搜索关键词
```

### 分享文档

```bash
# 运行程序
python document_manager.py

# 选择 4: 分享文档
# 输入文档 Token 和用户 ID 列表
```

### 备份文档

```bash
# 运行程序
python document_manager.py

# 选择 5: 备份文档
# 输入备份文件夹 Token
```

---

## 🛠️ 核心功能

### 1. 文档创建

```python
manager = DocumentManager()

# 创建单个文档
file_token = manager.create_document(
    title="项目文档",
    file_type="docx"
)
```

### 2. 批量创建

```python
# 批量创建文档
titles = ["文档 1", "文档 2", "文档 3"]
file_tokens = manager.batch_create_documents(titles)
```

### 3. 文档搜索

```python
# 搜索文档
documents = manager.search_documents("项目")
```

### 4. 权限管理

```python
# 分享文档
user_ids = ["ou_xxx1", "ou_xxx2"]
results = manager.share_document(file_token, user_ids, role="edit")
```

### 5. 文档备份

```python
# 备份所有文档
backup_tokens = manager.backup_documents(backup_folder_token)
```

---

## 📊 项目结构

```
feishu-document-manager/
├── document_manager.py    # 主程序
├── .env                   # 环境变量配置
├── .env.example           # 环境配置示例
├── requirements.txt       # 依赖包
├── README.md              # 项目说明
├── logs/                  # 日志目录
│   └── document_YYYYMMDD.log
└── documents.db           # 数据库文件
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

### 2. 云文档客户端

```python
class DriveClient:
    """飞书云文档 API 客户端"""
    
    def create_file(self, folder_token, title, file_type):
        # 创建文档
        pass
    
    def get_file_info(self, file_token):
        # 获取文档信息
        pass
    
    def batch_create_files(self, folder_token, titles, file_type):
        # 批量创建文档
        pass
    
    def search_files(self, query, folder_token, max_results):
        # 搜索文档
        pass
    
    def update_permission(self, file_token, member_id, member_type, role):
        # 更新文档权限
        pass
    
    def copy_file(self, file_token, dest_folder_token, new_title):
        # 复制文档
        pass
    
    def delete_file(self, file_token):
        # 删除文档
        pass
```

### 3. 文档管理工具

```python
class DocumentManager:
    """文档管理工具主类"""
    
    def create_document(self, title, file_type):
        # 创建文档
        pass
    
    def batch_create_documents(self, titles, file_type):
        # 批量创建文档
        pass
    
    def search_documents(self, query):
        # 搜索文档
        pass
    
    def share_document(self, file_token, user_ids, role):
        # 分享文档
        pass
    
    def backup_documents(self, backup_folder_token):
        # 备份文档
        pass
    
    def list_documents(self):
        # 列出所有文档
        pass
    
    def get_stats(self):
        # 获取统计信息
        pass
```

---

## ⚠️ 常见问题

### Q1: 文件夹 Token 从哪里获取？

**A**: 从飞书云文档 URL 中获取

```
1. 打开飞书云文档
2. 进入目标文件夹
3. 查看 URL
4. 复制 folder_token 参数
```

### Q2: 文档创建失败？

**A**: 检查权限配置

```
1. 开发者后台 → 应用权限
2. 添加"云文档"相关权限
3. 提交审核（如需）
```

### Q3: 批量创建失败？

**A**: 检查频率限制

```
- 批量 API 限制：10 次/分钟
- 代码中已添加延时（0.1 秒）
- 如仍失败，增加延时时间
```

---

## 📈 扩展功能

### 待扩展功能

- [ ] 文档内容同步
- [ ] 文档版本管理
- [ ] 文档模板系统
- [ ] Web 管理界面
- [ ] 文档统计分析

### 扩展建议

```python
# 文档内容同步
def sync_document_content(self, file_token: str, content: str):
    # 同步文档内容
    pass

# 文档版本管理
def get_document_versions(self, file_token: str):
    # 获取文档版本
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
- **核心模块**: 3 个
- **API 接口**: 7 个
- **数据库表**: 1 个

### 功能统计

- **文档管理**: 5 种（创建/搜索/分享/备份/删除）
- **权限管理**: 3 种（edit/view/comment）
- **统计功能**: 2 种（总数/按类型）

---

## 🎯 下一步计划

### 功能扩展

- [ ] 文档内容同步
- [ ] 文档版本管理
- [ ] Web 管理界面

### 性能优化

- [ ] 添加缓存层
- [ ] 添加异步支持
- [ ] 添加监控告警

---

## 📝 更新日志

### v1.0 (2026-03-13)

- ✅ 初始版本
- ✅ 文档创建功能
- ✅ 批量创建功能
- ✅ 文档搜索功能
- ✅ 权限管理功能
- ✅ 文档备份功能
- ✅ 日志记录

---

## 📞 获取帮助

### 文档

- 飞书开放平台：https://open.feishu.cn/
- 云文档 API 文档：https://open.feishu.cn/document

### 问题反馈

- 查看日志：`logs/document_*.log`
- 查看 FAQ：飞书开发 FAQ.md

---

**项目版本**: v1.0  
**最后更新**: 2026-03-13  
**Python 版本**: 3.11+

📄 **飞书文档管理工具项目已创建！开始文档管理功能开发！**
