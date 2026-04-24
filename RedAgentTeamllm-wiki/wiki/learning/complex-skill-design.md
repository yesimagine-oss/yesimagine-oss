---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 复杂多脚本技能设计指南
title: Complex Skill Design
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
# 🏗️ 复杂多脚本技能设计指南

_从简单到复杂：技能架构演进_

**创建时间**: 2026-03-13

---

## 📊 技能复杂度分级

| 等级 | 脚本数 | 特点 | 示例 |
|------|--------|------|------|
| 🟢 简单 | 1-2 | 单一功能 | searxng |
| 🟡 中等 | 3-5 | 功能集合 | clipboard-manager |
| 🔴 复杂 | 6+ | 完整工作流 | skill-creator |

---

## 🎯 复杂技能特征

### 1. 多脚本协作

**clipboard-manager 示例**:
```
save.py → 保存剪贴板
   ↓
list.py → 列出历史
   ↓
search.py → 搜索内容
   ↓
copy.py → 复制回剪贴板
```

**设计要点**:
- ✅ 统一的数据库 Schema
- ✅ 一致的错误处理
- ✅ 共享的配置管理
- ✅ 标准化的 CLI 参数

### 2. 共享资源

**数据库共享**:
```python
# 所有脚本使用相同的 DB_PATH
DB_PATH = Path.home() / ".clipboard-manager" / "history.db"

# 统一的连接函数
def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn
```

**配置共享**:
```python
# 统一的环境变量
DEFAULT_DOMAIN = "short.link"
MAX_ITEMS = 1000

# 统一的配置加载
def get_config():
    config_path = Path.home() / ".clipboard-manager" / "config.json"
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {}
```

### 3. 模块化设计

**功能模块**:
```
clipboard-manager/
├── save.py      # 保存模块
├── list.py      # 查询模块
├── search.py    # 搜索模块
├── copy.py      # 操作模块
├── delete.py    # 管理模块
└── export.py    # 导出模块
```

**每个模块**:
- ✅ 独立可执行
- ✅ 可组合使用
- ✅ 统一接口
- ✅ 清晰职责

---

## 📐 架构设计模式

### 模式 1: CRUD 模式

**适用**: 数据管理类技能

**结构**:
```
create.py  # 创建记录
read.py    # 查询记录
update.py  # 更新记录
delete.py  # 删除记录
```

**示例**: clipboard-manager
- save.py (Create)
- list.py (Read)
- search.py (Read with filter)
- delete.py (Delete)

### 模式 2: 流水线模式

**适用**: 数据处理类技能

**结构**:
```
input.py   # 输入处理
process.py # 核心处理
output.py  # 输出处理
```

**示例**: pdf-processor
- extract.py (提取文本)
- transform.py (转换格式)
- merge.py (合并文档)

### 模式 3: 工具集合模式

**适用**: 多功能工具类技能

**结构**:
```
tool1.py   # 工具 1
tool2.py   # 工具 2
tool3.py   # 工具 3
common.py  # 共享工具
```

**示例**: image-tools
- resize.py (缩放)
- rotate.py (旋转)
- convert.py (格式转换)
- compress.py (压缩)

### 模式 4: 工作流模式

**适用**: 多步骤流程类技能

**结构**:
```
step1_init.py      # 初始化
step2_validate.py  # 验证
step3_process.py   # 处理
step4_verify.py    # 验证
step5_deploy.py    # 部署
```

**示例**: cloud-deploy
- init.py (初始化项目)
- validate.py (验证配置)
- provision.py (创建资源)
- deploy.py (部署应用)
- verify.py (验证部署)

---

## 🔧 复杂技能最佳实践

### 1. 统一依赖管理

**所有脚本使用相同的依赖声明**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "click", "sqlite-vec"]
# ///
```

**或创建共享依赖文件**:
```toml
# pyproject.toml
[project]
dependencies = [
    "rich>=13.0.0",
    "click>=8.0.0",
]
```

### 2. 共享工具函数

**创建 utils.py**:
```python
# utils.py
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".skill-name" / "data.db"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def validate_input(data):
    # 通用验证逻辑
    pass
```

**在其他脚本中导入**:
```python
from utils import get_db_connection, validate_input
```

### 3. 统一的错误处理

**标准错误处理模式**:
```python
try:
    # 主要逻辑
    result = do_something()
except FileNotFoundError as e:
    console.print(f"[red]Error:[/red] File not found: {e}")
    sys.exit(1)
except PermissionError as e:
    console.print(f"[red]Error:[/red] Permission denied: {e}")
    sys.exit(1)
except Exception as e:
    console.print(f"[red]Unexpected error:[/red] {e}")
    sys.exit(1)
```

### 4. 一致的 CLI 设计

**统一参数风格**:
```python
# 所有脚本使用相同的参数命名
parser.add_argument("--limit", "-n", type=int, default=20)
parser.add_argument("--output", "-o", help="Output file")
parser.add_argument("--quiet", "-q", action="store_true")
```

**统一的帮助信息**:
```python
parser = argparse.ArgumentParser(
    description="Skill Name - Brief description",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s --output result.json
    """
)
```

### 5. 文档组织

**SKILL.md 结构**:
```markdown
# 技能名称

## 概述
## 快速开始
## 核心功能
### 功能 1 (脚本 1)
### 功能 2 (脚本 2)
### 功能 3 (脚本 3)
## 脚本说明
| 脚本 | 功能 | 示例 |
|------|------|------|
| script1.py | 功能 1 | 示例 |
| script2.py | 功能 2 | 示例 |
## 配置
## 数据模型
## 故障排除
```

**references/ 组织**:
```
references/
├── api-reference.md    # 所有脚本的 API
├── workflows.md        # 工作流说明
├── troubleshooting.md  # 故障排除
└── examples.md         # 使用示例
```

---

## 📊 clipboard-manager 架构分析

### 当前结构
```
clipboard-manager/
├── SKILL.md (5.6KB)
├── scripts/
│   ├── save.py (6.6KB)   - 保存 + 智能分类
│   ├── list.py (5.5KB)   - 列出 + 分类查看
│   ├── search.py (3.6KB) - 搜索 + 过滤
│   └── copy.py (2.7KB)   - 复制 + 统计
└── references/
```

### 架构优点
- ✅ 统一的数据库 Schema
- ✅ 一致的依赖声明
- ✅ 标准化的 CLI 参数
- ✅ 模块化设计

### 可扩展方向
```
scripts/
├── delete.py   - 删除记录
├── export.py   - 导出数据
├── qr.py       - 生成 QR 码
├── share.py    - 分享内容
└── utils.py    - 共享工具
```

---

## 🎯 复杂技能设计检查清单

### 架构设计
- [ ] 明确的模块划分
- [ ] 清晰的职责边界
- [ ] 合理的依赖关系
- [ ] 可扩展的结构

### 代码质量
- [ ] 统一的代码风格
- [ ] 一致的错误处理
- [ ] 完整的文档字符串
- [ ] 充分的注释

### 用户体验
- [ ] 一致的 CLI 接口
- [ ] 清晰的帮助信息
- [ ] 友好的错误提示
- [ ] 丰富的使用示例

### 维护性
- [ ] 共享工具函数
- [ ] 统一配置管理
- [ ] 模块化测试
- [ ] 版本管理规范

---

## 🔗 参考技能

### 官方复杂技能
- **skill-creator**: 6+ 脚本，完整开发流程
- **healthcheck**: 多步骤工作流，系统级操作
- **cloud-deploy**: 多平台支持，领域分离

### 学习要点
1. 阅读 SKILL.md 了解整体架构
2. 分析脚本间的依赖关系
3. 学习共享资源管理
4. 研究文档组织方式

---

## 🚀 下一步：从中等到复杂

### clipboard-manager 演进路线

**当前 (中等)**:
- 4 个脚本
- 基础 CRUD 功能
- 简单分类

**未来 (复杂)**:
- 8+ 脚本
- 完整工作流
- 高级功能（同步、分享、协作）

**新增脚本**:
```
scripts/
├── sync.py      - 云同步
├── share.py     - 分享内容
├── tag.py       - 标签管理
├── organize.py  - 自动整理
└── backup.py    - 备份恢复
```

---

_复杂技能 = 简单技能的有机组合_

**最后更新**: 2026-03-13

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[19-skill_adapter_layer_openclaw_http_cli_docker]]
- [[21-user_guide_image_analysis_skill]]
- [[22-image_skill_knowledge_graph]]
