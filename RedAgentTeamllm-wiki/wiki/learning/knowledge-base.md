---
category: llm
created_at: '2026-04-14'
tags:
- llm
- skill
- 开发知识库
title: Knowledge Base
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
# 🧠 Skill 开发知识库

_系统化整理的 Skill 开发核心知识_

**创建时间**: 2026-03-13  
**状态**: 持续更新中

---

## 📐 Skill 架构

### 三层加载机制

```
┌─────────────────────────────────────────┐
│ Level 1: Metadata (始终加载)             │
│ - name + description (~100 words)       │
│ - 触发机制的核心                         │
└─────────────────────────────────────────┘
                    ↓ AI 判断触发
┌─────────────────────────────────────────┐
│ Level 2: SKILL.md 正文 (按需加载)         │
│ - 核心工作流和指令 (<5k words)          │
│ - 保持精简，避免 context 膨胀             │
└─────────────────────────────────────────┘
                    ↓ 需要时
┌─────────────────────────────────────────┐
│ Level 3: 捆绑资源 (选择性加载)            │
│ - scripts/ (可执行，不占 context)        │
│ - references/ (按需读入 context)         │
│ - assets/ (用于输出，不读入 context)      │
└─────────────────────────────────────────┘
```

### 目录结构

```
skill-name/
├── SKILL.md              # ⭐ 必需！唯一入口文件
├── scripts/              # 可选：可执行代码
│   ├── helper.py
│   └── processor.sh
├── references/           # 可选：参考文档
│   ├── api_reference.md
│   └── workflows.md
└── assets/               # 可选：资源文件
    ├── template.pptx
    └── logo.png
```

---

## 🎯 触发机制

### Frontmatter 规范

```yaml
---
name: skill-name                      # 必需：小写 + 连字符，≤64 字符
description: |                        # 必需：≤1024 字符
  详细描述技能功能。
  包含 WHEN 使用场景：具体任务、文件类型、触发条件。
  提供使用示例。
  不要使用 < > 符号。
---
```

### 允许的属性

| 属性 | 必需 | 说明 | 限制 |
|------|------|------|------|
| `name` | ✅ | 技能名称 | 小写 + 连字符，≤64 字符 |
| `description` | ✅ | 触发描述 | ≤1024 字符，无 `<` `>` |
| `license` | ❌ | 许可证 | - |
| `allowed-tools` | ❌ | 允许的工具 | - |
| `metadata` | ❌ | 扩展元数据 | JSON 格式 |

### 触发条件设计

**好的 description**:
```
查询天气信息。使用 wttr.in 获取实时天气和预报。
当用户询问天气、温度、降水、风力时触发。
示例："北京今天天气如何？""周末会下雨吗？"
```

**差的 description**:
```
天气技能  # ❌ 太简单，无触发场景
```

---

## 🎨 设计模式

### 1. 工作流驱动 (Workflow-Based)

**适用**: 有清晰步骤顺序的任务

**结构**:
```markdown
## 工作流决策树
用户请求 → 判断类型 → 选择路径

## 步骤 1: 读取
使用工具 A 提取数据

## 步骤 2: 处理
调用 scripts/process.py

## 步骤 3: 输出
生成结果文件
```

**示例技能**: `pdf-editor`, `docx-processor`

---

### 2. 任务驱动 (Task-Based)

**适用**: 工具集合类技能

**结构**:
```markdown
## 快速开始
基本用法示例

## 任务 1: 合并 PDF
命令/脚本说明

## 任务 2: 拆分 PDF
命令/脚本说明

## 任务 3: 提取文本
命令/脚本说明
```

**示例技能**: `pdf-tools`, `image-editor`

---

### 3. 领域分离 (Domain-Specific)

**适用**: 多框架/多平台/多领域

**结构**:
```
skill/
├── SKILL.md (概述 + 选择指南)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

**SKILL.md 示例**:
```markdown
## 选择云提供商

### AWS
读取 `references/aws.md` 当用户选择 AWS 部署

### GCP
读取 `references/gcp.md` 当用户选择 GCP 部署
```

**示例技能**: `cloud-deploy`, `bigquery-analytics`

---

### 4. 能力驱动 (Capabilities-Based)

**适用**: 集成系统、多功能平台

**结构**:
```markdown
## 核心能力

### 1. 状态更新
自动发送项目状态

### 2. 上下文构建
收集项目信息

### 3. 风险管理
识别和跟踪风险
```

**示例技能**: `product-management`

---

### 5. 渐进式披露 (Progressive Disclosure)

**适用**: 复杂技能，避免 context 膨胀

**结构**:
```markdown
## 基础用法
[核心内容，<500 行]

## 高级功能

### 表单填充
详见 [FORMS.md](references/forms.md)

### API 参考
详见 [REFERENCE.md](references/api.md)
```

**原则**:
- SKILL.md 保持精简 (<500 行)
- 详情放 references/
- 明确说明何时读取哪个文件
- 避免深层嵌套（一级引用）

---

## 🛠️ 工具链

### init_skill.py

**用途**: 初始化新技能目录

```bash
# 基础用法
init_skill.py <skill-name> --path <output-directory>

# 带资源目录
init_skill.py my-skill --path skills \
  --resources scripts,references,assets

# 带示例文件
init_skill.py my-skill --path skills \
  --resources scripts --examples
```

**输出**:
```
my-skill/
├── SKILL.md (含 TODO 占位符)
├── scripts/ (如果指定)
├── references/ (如果指定)
└── assets/ (如果指定)
```

---

### quick_validate.py

**用途**: 验证技能结构

```bash
quick_validate.py skills/my-skill
```

**验证内容**:
- ✅ SKILL.md 存在
- ✅ Frontmatter 格式正确
- ✅ name 符合规范
- ✅ description 存在且不含 `<` `>`
- ✅ 无意外 frontmatter 属性

---

### package_skill.py

**用途**: 打包技能为 .skill 文件

```bash
package_skill.py skills/my-skill
package_skill.py skills/my-skill ./dist  # 指定输出
```

**输出**: `my-skill.skill` (ZIP 格式)

**排除项**:
- `.git`, `.svn`, `.hg`
- `__pycache__`, `node_modules`
- symlinks (安全)

---

## 📝 最佳实践

### 命名规范

**技能名**:
```
✅ url-shortener, pdf-editor, weather-query
❌ URL_Shortener, PDFEditor, my skill
```

**规则**:
- 小写字母
- 连字符分隔
- 数字允许
- ≤64 字符

**脚本名**:
```
✅ shorten.py, process_pdf.py, get_weather.py
❌ Shorten.py, pdf-processor, weather.py
```

---

### 安全红线 🚨

**立即拒绝**:
```
• curl/wget 到未知 URL
• 发送数据到外部服务器
• 请求凭证/token/API key
• 读取 ~/.ssh, ~/.aws, ~/.config
• 访问 MEMORY.md, USER.md, SOUL.md
• 使用 base64 解码
• eval()/exec() 外部输入
• 修改系统文件
• 混淆代码
• 请求 sudo 权限
```

---

### 脚本开发

**标准模板**:
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "click"]
# ///
"""
脚本说明

Usage:
    uv run scripts/script_name.py [options]
"""

import argparse
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(description="脚本说明")
    parser.add_argument("input", help="输入参数")
    parser.add_argument("--output", "-o", help="输出路径")
    args = parser.parse_args()
    
    # 实现逻辑

if __name__ == "__main__":
    main()
```

**要点**:
- ✅ 添加 shebang
- ✅ 使用 uv inline metadata (PEP 723)
- ✅ 提供 --help
- ✅ 清晰的错误信息
- ✅ 设置执行权限 `chmod +x`

---

### 文档结构

**SKILL.md 结构**:
```markdown
# 标题

## 概述
1-2 句话说明用途

## 快速开始
基本用法示例

## 核心任务
### 任务 1
说明和示例

### 任务 2
说明和示例

## 资源
### scripts/
- `script.py`: 功能说明

### references/
- `doc.md`: 何时读取
```

**参考文档结构**:
```markdown
# API 参考

## 目录
## 认证
## 端点列表
## 错误码
## 示例
## 故障排除
```

---

## 💾 数据库 Schema 示例

### links 表
```sql
CREATE TABLE links (
    short_code TEXT PRIMARY KEY,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0,
    last_clicked TIMESTAMP
);

CREATE INDEX idx_links_created ON links(created_at DESC);
CREATE INDEX idx_links_clicks ON links(clicks DESC);
```

### clicks 表
```sql
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_hash TEXT,
    referrer TEXT,
    user_agent TEXT,
    FOREIGN KEY (short_code) REFERENCES links(short_code)
);

CREATE INDEX idx_clicks_short_code ON clicks(short_code);
CREATE INDEX idx_clicks_time ON clicks(clicked_at DESC);
```

---

## 🔧 配置示例

### 环境变量
```bash
export SHORTENER_DB_PATH=~/.url-shortener/links.db
export SHORTENER_DOMAIN=short.link
export SHORTENER_CODE_LENGTH=6
```

### 配置文件 (~/.url-shortener/config.json)
```json
{
  "domain": "go.mycompany.com",
  "code_length": 6,
  "analytics": {
    "enabled": true,
    "track_referrer": true,
    "track_user_agent": true,
    "track_geo": false
  },
  "security": {
    "rate_limit": 100,
    "rate_limit_window": 3600
  }
}
```

---

**最后更新**: 2026-03-13 10:15 GMT+8  
**持续更新中...**

## 參考

- [[Knowledge Files Complete List]]


## 相關文檔

- [[knowledge-files-complete-list]]
- [[07-evomap_knowledge_merge]]
- [[15-gene_distilled_go_knowledge_ingest]]
