---
category: llm
created_at: '2026-04-14'
tags:
- llm
- '38'
- skill
- 安装与深度学习计划
- api
title: 38 Skills Installation Plan
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
# 📋 38 个 Skill 安装与深度学习计划

**创建时间**: 2026-03-13 23:00 GMT+8  
**状态**: ⚠️ ClawHub 速率限制中  
**解决方案**: 分批安装 + GitHub 克隆

---

## 🚨 当前状态

### ClawHub 速率限制

```
错误：Rate limit exceeded
原因：短时间内多次请求 ClawHub API
影响：无法通过 clawhub install 安装
```

### 已安装技能（11 个）

```
✅ agent-browser (v0.2.0)
✅ clipboard-manager (自研)
✅ find-skills (v0.1.0)
✅ proactive-agent (v3.1.0)
✅ searxng (v1.0.3)
✅ self-improving-agent (v1.0.11) ⭐ pskoett
✅ simplify-and-harden (v1.0.1) ⭐ pskoett
✅ skill-vetter (v1.0.0)
✅ url-shortener (自研)
```

---

## 📥 安装方案

### 方案 1: 等待速率限制解除（推荐）

```bash
# 等待 24 小时后重试
# 明天执行：
clawhub install summarize gog github weather nano-pdf obsidian nano-banana-pro openai-whisper notion brave-search
```

### 方案 2: 分批安装（备选）

```bash
# 每小时安装 2-3 个，避免触发限制
# 今天：安装 2 个
# 明天：安装 10 个
# 后天：安装 15 个
# 大后天：安装 11 个
```

### 方案 3: 手动克隆（备选）

```bash
# 如果能找到技能的 GitHub 仓库
# 手动克隆并复制到技能目录
```

---

## 📚 38 个技能详细学习计划

### 第一梯队（10 个）- 高价值低风险

#### 1. summarize (⭐ 574 · 150k)

**功能**: URL/文件摘要
**学习重点**:
- 支持的格式（web/PDF/图片/音频/YouTube）
- 摘要质量优化
- 批量处理
- 与 LLM 集成

**使用方法**:
```bash
# 安装后
summarize https://example.com
summarize file.pdf
summarize image.png --ocr
```

**逻辑结构**:
```
summarize/
├── SKILL.md (触发条件/使用方法)
├── scripts/
│   └── summarize.py (核心逻辑)
├── references/
│   └── format-support.md (格式支持说明)
└── assets/
```

---

#### 2. gog (⭐ 715 · 110k)

**功能**: Google Workspace CLI
**学习重点**:
- OAuth 配置
- Gmail/Calendar/Drive/Contacts/Sheets/Docs API
- 批量操作
- 安全最佳实践

**使用方法**:
```bash
# 配置
gog auth login

# 使用
gog gmail send --to user@example.com --subject "Test"
gog calendar create --title "Meeting" --time "2026-03-14 10:00"
gog drive upload file.pdf
```

**逻辑结构**:
```
gog/
├── SKILL.md
├── scripts/
│   ├── auth.py (认证)
│   ├── gmail.py (邮件)
│   ├── calendar.py (日历)
│   ├── drive.py (云盘)
│   └── ...
└── references/
    └── oauth-setup.md (OAuth 配置指南)
```

---

#### 3. github (⭐ 340 · 105k)

**功能**: GitHub CLI 集成
**学习重点**:
- gh CLI 命令
- issue/PR/CI runs/advanced queries
- 自动化工作流
- API 高级用法

**使用方法**:
```bash
# 认证
gh auth login

# 使用
gh issue create --title "Bug" --body "Description"
gh pr create --title "Fix" --body "Changes"
gh run watch
gh api /repos/{owner}/{repo}
```

**逻辑结构**:
```
github/
├── SKILL.md
├── scripts/
│   ├── issue-helper.py
│   ├── pr-review.py
│   └── ci-monitor.py
└── references/
    └── gh-commands.md (gh 命令参考)
```

---

#### 4. weather (⭐ 276 · 90k)

**功能**: 天气查询（无 API 钥匙）
**学习重点**:
- wttr.in API 使用
- 多城市支持
- 预报格式
- 缓存机制

**使用方法**:
```bash
# 直接使用
weather Beijing
weather "New York" --days 3
weather --json
```

**逻辑结构**:
```
weather/
├── SKILL.md
├── scripts/
│   └── weather.py (wttr.in 集成)
└── references/
    └── api-endpoints.md (API 端点)
```

---

#### 5. nano-pdf (⭐ 126 · 55.7k)

**功能**: PDF 编辑
**学习重点**:
- nano-pdf CLI 命令
- 自然语言编辑
- 批量处理
- 格式保持

**使用方法**:
```bash
# 安装 CLI
npm install -g nano-pdf-cli

# 使用
nano-pdf edit file.pdf "Add header 'Confidential'"
nano-pdf merge file1.pdf file2.pdf
nano-pdf extract file.pdf --pages 1-5
```

**逻辑结构**:
```
nano-pdf/
├── SKILL.md
├── scripts/
│   └── pdf-editor.py
└── references/
    └── cli-commands.md (CLI 命令参考)
```

---

#### 6. obsidian (⭐ 194 · 48.9k)

**功能**: Obsidian 自动化
**学习重点**:
- obsidian-cli 配置
- vault 管理
- 笔记创建/编辑/搜索
- 双向链接

**使用方法**:
```bash
# 安装 CLI
npm install -g obsidian-cli

# 使用
obsidian open "Note Title"
obsidian create "New Note" --content "Content"
obsidian search "keyword"
```

**逻辑结构**:
```
obsidian/
├── SKILL.md
├── scripts/
│   ├── note-manager.py
│   ├── search-helper.py
│   └── vault-backup.py
└── references/
    └── vault-structure.md (vault 结构)
```

---

#### 7. nano-banana-pro (⭐ 193 · 47.7k)

**功能**: 图像生成/编辑 (Gemini 3 Pro Image)
**学习重点**:
- Gemini API 配置
- 文本到图像
- 图像到图像
- 分辨率选择 (1K/2K/4K)

**使用方法**:
```bash
# 配置 API
export GEMINI_API_KEY=your_key

# 使用
nano-banana-pro generate "A beautiful sunset" --size 2K
nano-banana-pro edit image.png "Add a bird" --input-image image.png
```

**逻辑结构**:
```
nano-banana-pro/
├── SKILL.md
├── scripts/
│   ├── image-gen.py
│   └── image-edit.py
├── references/
│   └── gemini-api.md (Gemini API 参考)
└── assets/
    └── examples/ (示例图像)
```

---

#### 8. openai-whisper (⭐ 201 · 44k)

**功能**: 语音转文字（本地运行）
**学习重点**:
- whisper CLI 安装
- 模型选择
- 多语言支持
- 批量转录

**使用方法**:
```bash
# 安装
pip install openai-whisper

# 使用
whisper audio.mp3 --model base
whisper audio.mp3 --language zh --output_dir ./transcripts
```

**逻辑结构**:
```
openai-whisper/
├── SKILL.md
├── scripts/
│   ├── transcribe.py
│   └── batch-process.py
└── references/
    └── model-selection.md (模型选择指南)
```

---

#### 9. notion (⭐ 182 · 53.2k)

**功能**: Notion API 集成
**学习重点**:
- Notion API token 配置
- 页面/数据库/块管理
- 批量操作
- 集成最佳实践

**使用方法**:
```bash
# 配置
export NOTION_TOKEN=your_token

# 使用
notion page create --parent database_id --title "New Page"
notion database query database_id --filter "Status=Done"
notion block append page_id --text "Content"
```

**逻辑结构**:
```
notion/
├── SKILL.md
├── scripts/
│   ├── page-manager.py
│   ├── database-helper.py
│   └── block-editor.py
└── references/
    └── api-reference.md (API 参考)
```

---

#### 10. brave-search (⭐ 145 · 38.1k)

**功能**: 网络搜索（无浏览器）
**学习重点**:
- Brave Search API 配置
- 搜索结果提取
- 内容摘要
- 与 searxng 对比

**使用方法**:
```bash
# 配置
export BRAVE_API_KEY=your_key

# 使用
brave-search "query" --count 10
brave-search "query" --format json
```

**逻辑结构**:
```
brave-search/
├── SKILL.md
├── scripts/
│   └── search.py
└── references/
    └── api-setup.md (API 配置)
```

---

## 📊 学习进度追踪

### 安装进度

| 梯队 | 总数 | 已安装 | 进度 |
|------|------|--------|------|
| 第一梯队 | 10 | 0 | 0% |
| 第二梯队 | 15 | 0 | 0% |
| 第三梯队 | 13 | 0 | 0% |
| **总计** | **38** | **0** | **0%** |

### 学习进度

| 技能 | 安装 | 文档阅读 | 使用测试 | 结构分析 | 掌握 |
|------|------|---------|---------|---------|------|
| summarize | ❌ | - | - | - | ❌ |
| gog | ❌ | - | - | - | ❌ |
| github | ❌ | - | - | - | ❌ |
| weather | ❌ | - | - | - | ❌ |
| nano-pdf | ❌ | - | - | - | ❌ |
| obsidian | ❌ | - | - | - | ❌ |
| nano-banana-pro | ❌ | - | - | - | ❌ |
| openai-whisper | ❌ | - | - | - | ❌ |
| notion | ❌ | - | - | - | ❌ |
| brave-search | ❌ | - | - | - | ❌ |

---

## 🎯 建议行动

### 立即行动（解决速率限制）

```
□ 等待 24 小时速率限制解除
□ 或：使用 GitHub 克隆方式
□ 或：联系 ClawHub 支持提高限制
```

### 明天行动（速率限制解除后）

```
□ 安装第一梯队 10 个技能
□ 阅读每个技能的 SKILL.md
□ 测试基本功能
□ 分析逻辑结构
□ 记录学习笔记
```

### 本周行动

```
□ 安装第二梯队 15 个技能
□ 深入学习每个技能
□ 创建使用文档
□ 分析技能设计模式
```

### 本月行动

```
□ 安装第三梯队 13 个技能
□ 完成 38 个技能学习
□ 创建技能对比分析
□ 应用学习到自研技能
```

---

## 📝 学习笔记模板

### 每个技能的学习笔记

```markdown
# [技能名称] 学习笔记

## 基本信息
- 评分：⭐ XXX
- 下载：XXXk
- 版本：X.X.X
- 作者：XXX

## 功能概述
[技能解决什么问题]

## 安装配置
[安装步骤和配置需求]

## 使用方法
[基本使用命令和示例]

## 逻辑结构
[文件结构和核心逻辑]

## 学习收获
[可以应用到我们技能的设计]

## 改进建议
[我们可以改进的地方]
```

---

## 📊 总结

### 当前障碍
```
⚠️ ClawHub 速率限制
⚠️ 无法批量安装
⚠️ 需要等待 24 小时
```

### 解决方案
```
✅ 方案 1: 等待 24 小时后重试
✅ 方案 2: 分批安装（每小时 2-3 个）
✅ 方案 3: 寻找 GitHub 仓库克隆
```

### 学习计划
```
✅ 38 个技能详细分析完成
✅ 学习笔记模板创建
✅ 进度追踪系统就绪
✅ 等待安装执行
```

---

**计划创建时间**: 2026-03-13 23:00 GMT+8  
**总技能**: 38 个  
**已安装**: 0 个 (速率限制)  
**预计完成**: 2026-03-16 (3 天)

📋 **38 个技能学习计划已创建！等待速率限制解除后执行安装！**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[final-skills-status-report]]
- [[installation-status-report]]
- [[skills-installation-status]]
