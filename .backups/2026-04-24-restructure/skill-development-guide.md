# 🎓 OpenClaw Skill 开发完全指南

_从入门到精通的系统化学习路径_

**创建时间**: 2026-03-13  
**版本**: 1.0  
**作者**: OpenClaw Agent

---

## 📖 目录

1. [Skill 基础概念](#1-skill-基础概念)
2. [核心架构解析](#2-核心架构解析)
3. [开发工具链](#3-开发工具链)
4. [设计模式库](#4-设计模式库)
5. [实战开发流程](#5-实战开发流程)
6. [安全与审查](#6-安全与审查)
7. [发布与分发](#7-发布与分发)
8. [案例分析](#8-案例分析)
9. [常见问题](#9-常见问题)
10. [进阶资源](#10-进阶资源)

---

## 1. Skill 基础概念

### 1.1 什么是 Skill？

**Skill（技能）** 是 OpenClaw 的模块化扩展包，用于增强 AI 代理的特定领域能力。

> 💡 **核心理念**: Skill 不是教 AI"是什么"，而是教 AI"怎么做"——提供程序性知识（procedural knowledge）

### 1.2 Skill 能提供什么

| 类型 | 作用 | 示例 |
|------|------|------|
| **工作流** | 多步骤流程指导 | PDF 处理流程、文档编辑流程 |
| **工具集成** | 特定 API/文件格式操作 | BigQuery 查询、DOCX 编辑 |
| **领域知识** | 公司特定逻辑/ schema | 财务指标定义、数据库 schema |
| **捆绑资源** | 脚本/模板/参考文档 | Python 脚本、PPT 模板 |

### 1.3 触发机制

Skill 通过 **metadata** 自动触发：

```yaml
---
name: weather-query
description: 查询天气信息。使用 wttr.in 获取实时天气和预报。
             当用户询问天气、温度、降水、风力时触发。
---
```

**触发条件**:
- `name` 和 `description` 始终在上下文中（~100 词）
- AI 根据用户请求自动匹配最相关的 skill
- 匹配成功后才加载 SKILL.md 正文

### 1.4 渐进式披露设计

```
┌─────────────────────────────────────────┐
│ Level 1: Metadata (始终加载)             │
│ - name + description (~100 words)       │
└─────────────────────────────────────────┘
                    ↓ 触发后
┌─────────────────────────────────────────┐
│ Level 2: SKILL.md 正文 (按需加载)         │
│ - 核心工作流和指令 (<5k words)          │
└─────────────────────────────────────────┘
                    ↓ 需要时
┌─────────────────────────────────────────┐
│ Level 3: 捆绑资源 (选择性加载)            │
│ - scripts/ (可执行，不占 context)        │
│ - references/ (按需读入 context)         │
│ - assets/ (用于输出，不读入 context)      │
└─────────────────────────────────────────┘
```

---

## 2. 核心架构解析

### 2.1 目录结构

```
skill-name/
├── SKILL.md              # ⭐ 必需！唯一入口
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

### 2.2 SKILL.md 详解

#### YAML Frontmatter（必需）

```yaml
---
name: skill-name                      # 必需：小写 + 连字符，≤64 字符
description: |                        # 必需：≤1024 字符
  详细描述技能功能。
  包含 WHEN 使用场景：具体任务、文件类型、触发条件。
  不要使用 < > 符号。
---
```

**允许的 frontmatter 属性**:
- `name` ✅
- `description` ✅
- `license` ✅
- `allowed-tools` ✅
- `metadata` ✅

**禁止的 frontmatter 属性**:
- `version`, `author`, `homepage` ❌ (会被验证器拒绝)

#### Body 内容组织

**推荐结构模式**:

```markdown
# 技能标题

## 概述
1-2 句话说明技能用途

## 快速开始
最简单的使用示例

## 核心工作流
### 场景 1: [具体任务]
步骤 1...
步骤 2...

### 场景 2: [具体任务]
步骤 1...
步骤 2...

## 资源说明
### scripts/
- `script_name.py`: 功能说明，何时使用

### references/
- `doc_name.md`: 功能说明，何时读取

### assets/
- `template.ext`: 用途说明
```

### 2.3 资源目录详解

#### scripts/ - 可执行脚本

**用途**: 确定性操作、重复性代码、自动化任务

**示例**:
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///

"""脚本说明文档"""

def main():
    # 实现逻辑
    pass

if __name__ == "__main__":
    main()
```

**最佳实践**:
- 添加 shebang `#!/usr/bin/env python3`
- 使用 uv 的 inline script metadata 声明依赖
- 设置执行权限 `chmod +x script.py`
- 可被 AI 执行而无需读入 context

#### references/ - 参考文档

**用途**: 详细文档、API 参考、schema 定义、工作流指南

**示例结构**:
```markdown
# API 参考

## 认证
## 端点列表
## 错误码
## 示例查询
```

**最佳实践**:
- >100 行的文件添加目录
- 在 SKILL.md 中明确说明何时读取
- 保持单一职责（一个文件一个主题）

#### assets/ - 资源文件

**用途**: 模板、图片、字体、样板代码

**示例**:
- `template.pptx` - PowerPoint 模板
- `logo.png` - 品牌标识
- `boilerplate/` - 项目模板目录
- `font.ttf` - 字体文件

**特点**: 不读入 context，直接用于输出

---

## 3. 开发工具链

### 3.1 初始化工具

```bash
# 基础用法
python /opt/openclaw/skills/skill-creator/scripts/init_skill.py <skill-name> \
  --path <output-directory>

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
├── scripts/
│   └── example.py (如果用了--examples)
├── references/
│   └── api_reference.md (如果用了--examples)
└── assets/
    └── example_asset.txt (如果用了--examples)
```

### 3.2 验证工具

```bash
# 验证技能
python /opt/openclaw/skills/skill-creator/scripts/quick_validate.py skills/my-skill

# 验证输出
[OK] Skill is valid!
# 或
[ERROR] Missing 'description' in frontmatter
```

**验证内容**:
- ✅ SKILL.md 存在
- ✅ Frontmatter 格式正确
- ✅ name 符合规范（小写 + 连字符）
- ✅ description 存在且不含 `<` `>`
- ✅ 无意外 frontmatter 属性

### 3.3 打包工具

```bash
# 打包技能
python /opt/openclaw/skills/skill-creator/scripts/package_skill.py \
  skills/my-skill

# 指定输出目录
package_skill.py skills/my-skill ./dist
```

**输出**: `my-skill.skill` (ZIP 格式)

**打包流程**:
1. 运行验证
2. 排除 `.git`, `__pycache__`, `node_modules`
3. 拒绝 symlinks（安全）
4. 创建 ZIP 归档

### 3.4 开发工作流

```
1. 理解需求 → 2. 规划结构 → 3. 初始化 → 4. 实现 → 5. 验证 → 6. 打包 → 7. 测试 → 8. 迭代
```

---

## 4. 设计模式库

### 4.1 工作流驱动模式 (Workflow-Based)

**适用**: 有清晰步骤顺序的任务

**结构**:
```markdown
## 工作流决策树
用户请求 → 判断类型 → 选择路径

## 步骤 1: 读取
使用 pdfplumber 提取文本

## 步骤 2: 处理
调用 scripts/process.py

## 步骤 3: 输出
生成结果文件
```

**示例技能**: `pdf-editor`, `docx-processor`

### 4.2 任务驱动模式 (Task-Based)

**适用**: 工具集合类技能

**结构**:
```markdown
## 快速开始
基本用法示例

## 合并 PDF
命令/脚本说明

## 拆分 PDF
命令/脚本说明

## 提取文本
命令/脚本说明
```

**示例技能**: `pdf-tools`, `image-editor`

### 4.3 领域分离模式 (Domain-Specific)

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

### 4.4 能力驱动模式 (Capabilities-Based)

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

### 4.5 渐进式披露模式 (Progressive Disclosure)

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

### 示例集合
详见 [EXAMPLES.md](references/examples.md)
```

**原则**:
- SKILL.md 保持精简 (<500 行)
- 详情放 references/
- 明确说明何时读取哪个文件
- 避免深层嵌套（一级引用）

---

## 5. 实战开发流程

### 5.1 Step 1: 理解技能

**关键问题**:
1. 这个技能解决什么问题？
2. 用户会如何触发它？（具体查询示例）
3. 需要哪些脚本/文档/资源？

**示例分析** - 图片编辑技能:
```
用户可能说:
- "去除这张照片的红眼"
- "旋转这张图片 90 度"
- "调整这张图的亮度"

需要的资源:
- scripts/remove_redeye.py
- scripts/rotate_image.py
- scripts/adjust_brightness.py
```

### 5.2 Step 2: 规划结构

**决策树**:
```
是否需要确定性代码？ → 是 → 创建 scripts/
是否有详细文档？ → 是 → 创建 references/
是否有模板/资源？ → 是 → 创建 assets/
```

### 5.3 Step 3: 初始化

```bash
init_skill.py image-editor --path skills \
  --resources scripts --examples
```

### 5.4 Step 4: 实现

#### 编写 SKILL.md

```markdown
---
name: image-editor
description: 图像编辑和处理技能。支持旋转、裁剪、调色、滤镜等操作。
             当用户需要编辑图片、调整照片、转换图像格式时触发。
---

# 图像编辑器

## 概述
提供完整的图像编辑能力，从基础旋转到高级调色。

## 快速开始
```bash
uv run scripts/rotate_image.py input.jpg --angle 90
```

## 核心任务

### 旋转图像
```bash
uv run scripts/rotate_image.py <input> --angle <degrees>
```

### 调整亮度
```bash
uv run scripts/adjust_brightness.py <input> --factor <1.0-2.0>
```

### 去除红眼
```bash
uv run scripts/remove_redeye.py <input>
```

## 资源
### scripts/
- `rotate_image.py`: 旋转图像，支持任意角度
- `adjust_brightness.py`: 调整亮度/对比度
- `remove_redeye.py`: 自动检测并去除红眼
```

#### 编写脚本

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow"]
# ///

"""旋转图像脚本"""

import argparse
from PIL import Image

def rotate_image(input_path: str, output_path: str, angle: float):
    """旋转图像"""
    img = Image.open(input_path)
    rotated = img.rotate(-angle, expand=True)  # 负角度=顺时针
    rotated.save(output_path)
    print(f"✓ 已旋转 {input_path} {angle}度 → {output_path}")

def main():
    parser = argparse.ArgumentParser(description="旋转图像")
    parser.add_argument("input", help="输入图像路径")
    parser.add_argument("--angle", type=float, required=True, help="旋转角度（顺时针）")
    parser.add_argument("--output", "-o", help="输出路径（默认：input_rotated.jpg）")
    args = parser.parse_args()
    
    output = args.output or f"{args.input.rsplit('.', 1)[0]}_rotated.jpg"
    rotate_image(args.input, output, args.angle)

if __name__ == "__main__":
    main()
```

### 5.5 Step 5: 验证

```bash
quick_validate.py skills/image-editor
# [OK] Skill is valid!
```

### 5.6 Step 6: 测试

**测试场景**:
1. 用真实用户查询触发技能
2. 验证脚本执行正确
3. 检查输出质量
4. 记录问题和改进点

### 5.7 Step 7: 迭代

**常见改进**:
- 添加更多示例
- 优化错误处理
- 补充边界情况
- 改进文档清晰度

---

## 6. 安全与审查

### 6.1 安全红线 🚨

**立即拒绝的技能**:
```
• curl/wget 到未知 URL
• 发送数据到外部服务器
• 请求凭证/token/API key
• 读取 ~/.ssh, ~/.aws, ~/.config
• 访问 MEMORY.md, USER.md, SOUL.md
• 使用 base64 解码
• eval()/exec() 外部输入
• 修改系统文件
• 安装未列出的包
• 混淆代码
• 请求 sudo 权限
• 访问浏览器 cookie
```

### 6.2 风险分级

| 等级 | 示例 | 行动 |
|------|------|------|
| 🟢 LOW | 笔记、天气、格式化 | 基础审查，可安装 |
| 🟡 MEDIUM | 文件操作、浏览器、API | 完整代码审查 |
| 🔴 HIGH | 凭证、交易、系统 | 需要人工批准 |
| ⛔ EXTREME | 安全配置、root 访问 | 禁止安装 |

### 6.3 审查流程

参考 `skill-vetter` 技能:

```markdown
## Step 1: 来源检查
- [ ] 来源可信吗？
- [ ] 作者知名吗？
- [ ] 有多少下载/星标？
- [ ] 最后更新时间？

## Step 2: 代码审查（必需）
阅读所有文件，检查红线

## Step 3: 权限范围
- 需要读哪些文件？
- 需要写哪些文件？
- 需要运行什么命令？
- 需要网络访问吗？

## Step 4: 风险分类
输出审查报告
```

---

## 7. 发布与分发

### 7.1 发布到 ClawHub

```bash
# 使用 clawhub CLI
clawhub publish skills/my-skill

# 或手动上传到 clawhub.com
```

### 7.2 版本管理

**建议实践**:
- 在 SKILL.md 中记录重大变更
- 保持向后兼容
- 语义化版本（虽然 frontmatter 不支持 version 字段）

### 7.3 分发格式

`.skill` 文件 = ZIP 归档
```bash
# 查看内容
unzip -l my-skill.skill

# 解压
unzip my-skill.skill -d output-dir/
```

---

## 8. 案例分析

### 8.1 简单技能：searxng

**特点**:
- 单一脚本 + 配置
- 清晰的触发条件
- 环境变量配置

**结构**:
```
searxng/
├── SKILL.md (1.8KB)
├── scripts/
│   └── searxng.py (6KB)
└── config/
    └── settings.yml
```

**学习点**:
- 如何使用 uv inline script metadata
- 如何处理环境变量
- 如何格式化输出

### 8.2 中等技能：skill-vetter

**特点**:
- 纯文档，无脚本
- 检查清单格式
- 安全审查流程

**结构**:
```
skill-vetter/
└── SKILL.md (审查指南)
```

**学习点**:
- 如何使用表格和清单
- 如何组织决策流程
- 如何输出结构化报告

### 8.3 复杂技能：skill-creator

**特点**:
- 多个脚本工具
- 详细文档
- 完整开发流程

**结构**:
```
skill-creator/
├── SKILL.md (10KB+)
├── scripts/
│   ├── init_skill.py
│   ├── package_skill.py
│   └── quick_validate.py
└── references/
    ├── workflows.md
    └── output-patterns.md
```

**学习点**:
- 如何组织多脚本项目
- 如何编写渐进式文档
- 如何提供设计模式参考

---

## 9. 常见问题

### Q1: 技能名称如何命名？

```
✅ 正确: pdf-editor, image-processor, weather-query
❌ 错误: PDF_Editor, ImageProcessor, my skill
```

**规则**:
- 小写字母
- 连字符分隔
- 数字允许
- ≤64 字符

### Q2: description 怎么写？

**公式**:
```
[功能描述] + [触发场景] + [使用示例]
```

**示例**:
```
查询天气信息。使用 wttr.in 获取实时天气和预报。
当用户询问天气、温度、降水、风力时触发。
示例："北京今天天气如何？""周末会下雨吗？"
```

### Q3: 何时使用 scripts/ vs 直接写在 SKILL.md？

**使用 scripts/**:
- 代码重复使用
- 需要确定性执行
- 复杂逻辑
- 外部依赖

**写在 SKILL.md**:
- 简单示例
- 概念说明
- 流程指导

### Q4: 如何测试技能？

1. 在隔离环境中加载
2. 用真实查询触发
3. 验证输出正确性
4. 检查边界情况
5. 记录并修复问题

### Q5: 技能太大怎么办？

**解决方案**:
1. 拆分到 references/
2. 使用渐进式披露
3. 只保留核心在 SKILL.md
4. 考虑拆分成多个技能

---

## 10. 进阶资源

### 10.1 官方文档
- 本地：`/opt/openclaw/docs/`
- 在线：https://docs.openclaw.ai
- 社区：https://discord.com/invite/clawd

### 10.2 技能市场
- ClawHub: https://clawhub.com
- 浏览现有技能学习最佳实践

### 10.3 学习路径

**初学者**:
1. 阅读本指南
2. 分析 3-5 个简单技能
3. 创建第一个技能（天气查询）
4. 发布到 ClawHub

**进阶者**:
1. 研究复杂技能架构
2. 开发多脚本技能
3. 贡献到官方技能库
4. 创建技能系列

**专家**:
1. 设计领域专用技能
2. 优化 context 使用
3. 创建技能开发工具
4. 指导社区贡献

### 10.4 实用命令速查

```bash
# 初始化
init_skill.py <name> --path <dir> --resources scripts,references --examples

# 验证
quick_validate.py skills/<name>

# 打包
package_skill.py skills/<name>

# 查看技能列表
find /opt/openclaw/skills -name "SKILL.md"

# 分析技能结构
tree skills/<name> -L 3

# 解包.skill 文件
unzip <skill>.skill -d analysis/
```

---

## 📝 学习检查清单

完成本指南后，你应该能够：

- [ ] 解释 Skill 的三层加载机制
- [ ] 创建符合规范的 SKILL.md
- [ ] 编写可执行的 Python 脚本
- [ ] 使用工具链初始化/验证/打包
- [ ] 选择合适的设计模式
- [ ] 进行安全审查
- [ ] 发布技能到 ClawHub

---

_持续更新中... 最后更新：2026-03-13_
