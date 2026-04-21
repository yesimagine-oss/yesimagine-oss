---
name: clipboard-manager
description: 剪贴板历史管理技能。支持保存、搜索、分类和快速复制剪贴板内容。
             当用户需要管理剪贴板历史、查找复制过的内容、保存常用片段时触发。
             示例："保存当前剪贴板""搜索剪贴板历史""复制之前的链接"
---

# Clipboard Manager

## 概述
提供完整的剪贴板历史管理能力，包括保存、搜索、分类和快速复制操作。
支持本地存储、智能分类和快捷键集成。

## 快速开始

### 保存剪贴板
```bash
uv run scripts/save.py
# 自动保存当前剪贴板内容
```

### 查看历史
```bash
uv run scripts/list.py
# 列出最近的剪贴板记录
```

### 搜索内容
```bash
uv run scripts/search.py "关键词"
# 搜索包含关键词的历史记录
```

### 复制内容
```bash
uv run scripts/copy.py <id>
# 将指定 ID 的内容复制到剪贴板
```

## 核心任务

### 1. 保存剪贴板

**自动保存**:
```bash
uv run scripts/save.py
```

**手动添加**:
```bash
uv run scripts/save.py --text "要保存的内容"
```

**批量导入**:
```bash
uv run scripts/save.py --file snippets.txt
```

**工作流程**:
1. 读取剪贴板内容（或从参数/文件）
2. 检测内容类型（文本/链接/密码/代码）
3. 自动分类
4. 存储到本地数据库
5. 返回保存的 ID

### 2. 查看历史

**列出最近记录**:
```bash
uv run scripts/list.py
uv run scripts/list.py --limit 20
```

**按分类查看**:
```bash
uv run scripts/list.py --category links
uv run scripts/list.py --category passwords
uv run scripts/list.py --category code
```

**查看详细信息**:
```bash
uv run scripts/list.py --id 123 --detail
```

### 3. 搜索内容

**基本搜索**:
```bash
uv run scripts/search.py "关键词"
```

**分类搜索**:
```bash
uv run scripts/search.py "api" --category code
```

**高级搜索**:
```bash
uv run scripts/search.py "github" --date-from 2026-01-01
uv run scripts/search.py "password" --exact
```

### 4. 复制内容

**复制到剪贴板**:
```bash
uv run scripts/copy.py <id>
```

**复制并显示**:
```bash
uv run scripts/copy.py <id> --show
```

**批量复制**:
```bash
uv run scripts/copy.py <id1> <id2> --separator "\n"
```

### 5. 管理记录

**删除记录**:
```bash
uv run scripts/delete.py <id>
uv run scripts/delete.py <id> --confirm
```

**清空历史**:
```bash
uv run scripts/clear.py
uv run scripts/clear.py --older-than 30d
```

**导出记录**:
```bash
uv run scripts/export.py --format json
uv run scripts/export.py --category links -o links.json
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CLIPBOARD_DB_PATH` | 数据库文件路径 | `~/.clipboard-manager/history.db` |
| `CLIPBOARD_MAX_ITEMS` | 最大保存数量 | `1000` |
| `CLIPBOARD_AUTO_SAVE` | 是否自动保存 | `true` |

### 配置文件

在 `~/.clipboard-manager/config.json` 中配置:

```json
{
  "max_items": 1000,
  "auto_save": true,
  "auto_save_interval": 5,
  "categories": {
    "enabled": true,
    "auto_detect": true
  },
  "privacy": {
    "exclude_passwords": false,
    "encrypt_sensitive": true
  }
}
```

## 数据模型

### 剪贴板记录

```json
{
  "id": 123,
  "content": "https://github.com/openclaw/openclaw",
  "content_type": "link",
  "category": "links",
  "created_at": "2026-03-13T10:00:00Z",
  "copied_count": 5,
  "last_copied": "2026-03-13T15:30:00Z",
  "tags": ["github", "openclaw"],
  "metadata": {
    "source": "browser",
    "length": 42
  }
}
```

### 分类类型

| 分类 | 检测规则 | 示例 |
|------|---------|------|
| `text` | 默认 | 普通文本 |
| `link` | http(s):// | https://example.com |
| `email` | email 格式 | user@example.com |
| `password` | 高熵字符串 | X9#kL2$mN5@pQ |
| `code` | 代码特征 | function() {...} |
| `phone` | 电话号码格式 | +86-138-0000-0000 |
| `date` | 日期格式 | 2026-03-13 |

## 脚本说明

### scripts/

| 脚本 | 功能 | 示例 |
|------|------|------|
| `save.py` | 保存剪贴板 | `uv run scripts/save.py` |
| `list.py` | 列出历史 | `uv run scripts/list.py` |
| `search.py` | 搜索内容 | `uv run scripts/search.py "key"` |
| `copy.py` | 复制内容 | `uv run scripts/copy.py 123` |
| `delete.py` | 删除记录 | `uv run scripts/delete.py 123` |
| `clear.py` | 清空历史 | `uv run scripts/clear.py` |
| `export.py` | 导出数据 | `uv run scripts/export.py --format json` |

## 智能分类

### 自动检测规则

**链接检测**:
```python
if re.match(r'https?://\S+', content):
    return 'link'
```

**邮箱检测**:
```python
if re.match(r'\S+@\S+\.\S+', content):
    return 'email'
```

**密码检测**:
```python
if len(content) >= 8 and has_high_entropy(content):
    return 'password'
```

**代码检测**:
```python
if re.search(r'(function|def|class|import|from)\s', content):
    return 'code'
```

## 最佳实践

### 安全性
- 敏感内容加密存储
- 密码分类特殊保护
- 支持排除特定应用

### 性能
- 限制最大保存数量
- 定期清理旧记录
- 索引搜索字段

### 隐私
- 可选加密敏感内容
- 支持排除列表
- 本地存储不上传

## 故障排除

### 常见问题

**Q: 无法读取剪贴板？**
- 检查剪贴板权限
- 确认系统支持
- 尝试手动添加 `--text`

**Q: 搜索结果为空？**
- 检查关键词拼写
- 尝试模糊搜索
- 确认分类过滤

**Q: 数据库锁定？**
- 检查是否有其他进程访问
- 增加超时时间
- 考虑使用 WAL 模式

---

_提示：详细 API 参考见 `references/api-reference.md`_
