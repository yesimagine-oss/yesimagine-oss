# 📦 ClawHub 技能安装清单

**创建时间**: 2026-03-22 08:45 GMT+8  
**数据来源**: ClawHub.ai 实时抓取  
**状态**: 待安装（速率限制中）

---

## 🎯 高优先级技能（10 个）

### 1. Gog ⭐⭐⭐⭐⭐

**ClawHub**: `steipete/gog`  
**下载量**: 127k | **Stars**: 769 | **版本**: 1

#### 功能用途
- **Google Workspace CLI** - Gmail, Calendar, Drive, Contacts, Sheets, Docs
- 通过命令行管理所有 Google 服务
- 无需打开网页即可完成操作

#### 解决痛点
- ❌ 手动登录 Gmail 查看邮件效率低
- ❌ 日历安排需要多次点击
- ❌ Google Drive 文件管理繁琐
- ✅ **一键查询/操作，提升 10 倍效率**

#### 技术栈
- **语言**: Python + Bash
- **依赖**: `gogcli` (Go 语言编写)
- **平台**: Linux/macOS/Windows

#### 结构逻辑
```
gog/
├── SKILL.md              # 触发条件/使用方法
├── scripts/
│   ├── gog-gmail.sh      # Gmail 操作
│   ├── gog-calendar.sh   # 日历管理
│   ├── gog-drive.sh      # Drive 文件
│   └── gog-contacts.sh   # 联系人
├── references/
│   └── setup-guide.md    # 配置指南
└── assets/
    └── templates/        # 邮件模板
```

#### 安装方法

**方法 1: GitHub 克隆（推荐）**
```bash
cd /tmp
git clone https://github.com/steipete/gog.git
cp -r gog ~/.openclaw/workspace/skills/
```

**方法 2: ClawHub（速率限制）**
```bash
clawhub install gog
```

**配置步骤**:
```bash
# 1. 安装 gogcli
curl -sSL https://gogcli.dev/install | bash

# 2. 授权 Google 账号
gogcli auth

# 3. 测试
gogcli gmail list --max 5
```

---

### 2. Github ⭐⭐⭐⭐⭐

**ClawHub**: `steipete/github`  
**下载量**: 125k | **Stars**: 416 | **版本**: 1

#### 功能用途
- 使用 `gh` CLI 与 GitHub 交互
- 管理 Issues, PRs, CI Runs, API 查询

#### 解决痛点
- ❌ 手动打开 GitHub 网页查看 Issues
- ❌ PR 审查需要多次点击
- ❌ CI 状态检查繁琐
- ✅ **命令行一键操作，开发者必备**

#### 技术栈
- **语言**: Bash + Shell
- **依赖**: `gh` CLI (GitHub 官方工具)
- **平台**: 全平台

#### 结构逻辑
```
github/
├── SKILL.md
├── scripts/
│   ├── gh-issue.sh       # Issue 管理
│   ├── gh-pr.sh          # PR 操作
│   ├── gh-run.sh         # CI 查询
│   └── gh-api.sh         # API 调用
└── references/
    └── gh-cheatsheet.md  # 命令速查
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/github.git
cp -r github ~/.openclaw/workspace/skills/
```

**方法 2: ClawHub**
```bash
clawhub install github
```

**配置步骤**:
```bash
# 1. 安装 gh CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh -y

# 2. 认证
gh auth login

# 3. 测试
gh issue list
```

---

### 3. Notion ⭐⭐⭐⭐☆

**ClawHub**: `steipete/notion`  
**下载量**: 62.2k | **Stars**: 202 | **版本**: 1

#### 功能用途
- Notion API 集成
- 创建/管理 Pages, Databases, Blocks

#### 解决痛点
- ❌ 手动创建 Notion 页面效率低
- ❌ 数据库操作需要多次点击
- ❌ 无法批量处理内容
- ✅ **API 自动化，批量操作**

#### 技术栈
- **语言**: Python + Node.js
- **依赖**: `notion-client` (官方 SDK)
- **平台**: 全平台

#### 结构逻辑
```
notion/
├── SKILL.md
├── scripts/
│   ├── notion-page.py    # 页面管理
│   ├── notion-db.py      # 数据库操作
│   └── notion-block.py   # Block 编辑
├── references/
│   └── api-examples.md   # API 示例
└── assets/
    └── templates/        # 页面模板
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/notion.git
cp -r notion ~/.openclaw/workspace/skills/
```

**配置步骤**:
```bash
# 1. 获取 Notion API Token
# 访问：https://www.notion.so/my-integrations

# 2. 安装依赖
pip install notion-client

# 3. 配置 Token
export NOTION_TOKEN="secret_xxx"
export NOTION_DATABASE_ID="xxx"

# 4. 测试
python3 notion-page.py --list
```

---

### 4. Weather ⭐⭐⭐⭐☆

**ClawHub**: `steipete/weather`  
**下载量**: 107k | **Stars**: 312 | **版本**: 1

#### 功能用途
- 获取当前天气和预报
- **无需 API Key**（使用免费数据源）

#### 解决痛点
- ❌ 需要注册天气 API
- ❌ 免费额度有限
- ❌ 多个城市查询麻烦
- ✅ **开箱即用，无配置**

#### 技术栈
- **语言**: Bash + curl
- **依赖**: 无（使用 wttr.in 免费 API）
- **平台**: 全平台

#### 结构逻辑
```
weather/
├── SKILL.md
├── scripts/
│   └── weather.sh        # 天气查询
└── references/
    └── locations.md      # 城市列表
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/weather.git
cp -r weather ~/.openclaw/workspace/skills/
```

**使用示例**:
```bash
# 查询北京天气
weather beijing

# 查询 7 天预报
weather beijing --forecast

# 使用示例
python3 -c "from weather import get_weather; print(get_weather('beijing'))"
```

---

### 5. Nano Pdf ⭐⭐⭐⭐☆

**ClawHub**: `steipete/nano-pdf`  
**下载量**: 69.2k | **Stars**: 166 | **版本**: 1

#### 功能用途
- 使用自然语言编辑 PDF
- 合并/分割/转换/提取

#### 解决痛点
- ❌ PDF 编辑需要专业软件
- ❌ Adobe Acrobat 昂贵
- ❌ 在线工具隐私风险
- ✅ **命令行编辑，隐私安全**

#### 技术栈
- **语言**: Rust
- **依赖**: `nano-pdf` CLI
- **平台**: Linux/macOS/Windows

#### 结构逻辑
```
nano-pdf/
├── SKILL.md
├── scripts/
│   └── nano-pdf-wrapper.sh
├── references/
│   └── examples.md       # 使用示例
└── assets/
    └── presets/          # 预设配置
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/nano-pdf.git
cp -r nano-pdf ~/.openclaw/workspace/skills/
```

**配置步骤**:
```bash
# 1. 安装 nano-pdf
curl -sSL https://nano-pdf.dev/install | bash

# 2. 测试
nano-pdf merge file1.pdf file2.pdf -o output.pdf
```

---

### 6. Obsidian ⭐⭐⭐⭐☆

**ClawHub**: `steipete/obsidian`  
**下载量**: 60.2k | **Stars**: 247 | **版本**: 1

#### 功能用途
- 管理 Obsidian 知识库
- 自动化笔记操作

#### 解决痛点
- ❌ 手动管理大量笔记
- ❌ 无法批量操作
- ❌ 知识关联困难
- ✅ **自动化管理，智能关联**

#### 技术栈
- **语言**: Bash + Python
- **依赖**: `obsidian-cli`
- **平台**: 全平台

#### 结构逻辑
```
obsidian/
├── SKILL.md
├── scripts/
│   ├── obsidian-search.py   # 搜索笔记
│   ├── obsidian-link.py     # 创建链接
│   └── obsidian-tag.py      # 标签管理
└── references/
    └── vault-structure.md
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/obsidian.git
cp -r obsidian ~/.openclaw/workspace/skills/
```

---

### 7. Openai Whisper ⭐⭐⭐⭐☆

**ClawHub**: `steipete/openai-whisper`  
**下载量**: 53.4k | **Stars**: 234 | **版本**: 1

#### 功能用途
- 本地语音转文字
- **无需 API Key**（本地运行）

#### 解决痛点
- ❌ 语音转录需要付费 API
- ❌ 隐私数据上传云端
- ❌ 多语言支持差
- ✅ **本地运行，隐私安全**

#### 技术栈
- **语言**: Python
- **依赖**: `openai-whisper` (OpenAI 开源)
- **平台**: Linux/macOS/Windows

#### 结构逻辑
```
openai-whisper/
├── SKILL.md
├── scripts/
│   └── whisper-transcribe.py
├── references/
│   └── models.md         # 模型选择
└── assets/
    └── languages/        # 语言配置
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/openai-whisper.git
cp -r openai-whisper ~/.openclaw/workspace/skills/
```

**配置步骤**:
```bash
# 1. 安装 whisper
pip install openai-whisper

# 2. 测试
whisper audio.mp3 --model base
```

---

### 8. Nano Banana Pro ⭐⭐⭐⭐☆

**ClawHub**: `steipete/nano-banana-pro`  
**下载量**: 61.6k | **Stars**: 244 | **版本**: 2

#### 功能用途
- 生成/编辑图片（Gemini 3 Pro Image）
- 文生图 + 图生图
- 支持 1K/2K/4K 分辨率

#### 解决痛点
- ❌ Midjourney 需要订阅
- ❌ DALL-E 3 质量不稳定
- ❌ 图片编辑复杂
- ✅ **高质量生成，编辑一体**

#### 技术栈
- **语言**: Python + Node.js
- **依赖**: `nano-banana-pro` CLI
- **平台**: 全平台

#### 结构逻辑
```
nano-banana-pro/
├── SKILL.md
├── scripts/
│   ├── generate.py       # 图片生成
│   └── edit.py           # 图片编辑
├── references/
│   └── prompts.md        # 提示词库
└── assets/
    └── styles/           # 风格预设
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/nano-banana-pro.git
cp -r nano-banana-pro ~/.openclaw/workspace/skills/
```

---

### 9. Brave Search ⭐⭐⭐⭐☆

**ClawHub**: `steipete/brave-search`  
**下载量**: 未知 | **Stars**: 未知 | **版本**: 1

#### 功能用途
- 隐私搜索引擎
- 替代 Google Search

#### 解决痛点
- ❌ Google 追踪隐私
- ❌ 搜索结果广告多
- ❌ 需要 API Key
- ✅ **隐私保护，无追踪**

#### 技术栈
- **语言**: Python + Bash
- **依赖**: Brave Search API
- **平台**: 全平台

#### 结构逻辑
```
brave-search/
├── SKILL.md
├── scripts/
│   └── brave-search.py
└── references/
    └── api-guide.md
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/brave-search.git
cp -r brave-search ~/.openclaw/workspace/skills/
```

---

### 10. Summarize ⭐⭐⭐⭐⭐

**ClawHub**: `steipete/summarize`  
**下载量**: 192k | **Stars**: 738 | **版本**: 1

#### 功能用途
- URL/文件摘要（web/PDF/图片/音频/YouTube）
- 支持多种格式

#### 解决痛点
- ❌ 长文章阅读耗时
- ❌ PDF 内容提取困难
- ❌ 视频无法快速浏览
- ✅ **一键摘要，节省 80% 时间**

#### 技术栈
- **语言**: Python + Node.js
- **依赖**: 多种解析库
- **平台**: 全平台

#### 结构逻辑
```
summarize/
├── SKILL.md
├── scripts/
│   ├── summarize-web.py   # 网页摘要
│   ├── summarize-pdf.py   # PDF 摘要
│   ├── summarize-image.py # 图片 OCR
│   └── summarize-audio.py # 音频转录
├── references/
│   └── format-support.md
└── assets/
    └── templates/
```

#### 安装方法

**方法 1: GitHub 克隆**
```bash
cd /tmp
git clone https://github.com/steipete/summarize.git
cp -r summarize ~/.openclaw/workspace/skills/
```

---

## 📊 技能对比表

| 技能 | 下载量 | Stars | 语言 | 依赖 | 难度 | 优先级 |
|------|--------|-------|------|------|------|--------|
| **gog** | 127k | 769 | Python+Go | gogcli | ⭐⭐⭐ | P0 |
| **github** | 125k | 416 | Bash | gh CLI | ⭐⭐ | P0 |
| **notion** | 62.2k | 202 | Python | notion-client | ⭐⭐⭐ | P1 |
| **weather** | 107k | 312 | Bash | 无 | ⭐ | P1 |
| **nano-pdf** | 69.2k | 166 | Rust | nano-pdf | ⭐⭐⭐ | P1 |
| **obsidian** | 60.2k | 247 | Bash+Python | obsidian-cli | ⭐⭐ | P2 |
| **openai-whisper** | 53.4k | 234 | Python | whisper | ⭐⭐⭐⭐ | P2 |
| **nano-banana-pro** | 61.6k | 244 | Python+Node | nano-banana | ⭐⭐⭐⭐ | P2 |
| **brave-search** | - | - | Python | Brave API | ⭐⭐ | P2 |
| **summarize** | 192k | 738 | Python+Node | 多种 | ⭐⭐⭐⭐ | P0 |

---

## 🎯 推荐安装顺序

### 第一批（今天）- P0 高优先级
1. ✅ **gog** - Google Workspace 必备
2. ✅ **github** - 开发者必备
3. ✅ **summarize** - 效率提升

### 第二批（明天）- P1 中优先级
4. **weather** - 无配置即用
5. **notion** - 知识库管理
6. **nano-pdf** - PDF 编辑

### 第三批（后天）- P2 低优先级
7. **obsidian** - 笔记管理
8. **openai-whisper** - 语音转录
9. **nano-banana-pro** - 图片生成
10. **brave-search** - 隐私搜索

---

## 📋 批量安装脚本

```bash
#!/bin/bash
# 批量安装技能脚本

skills=(
    "gog"
    "github"
    "summarize"
    "weather"
    "notion"
    "nano-pdf"
    "obsidian"
    "openai-whisper"
    "nano-banana-pro"
    "brave-search"
)

for skill in "${skills[@]}"; do
    echo "[$(date)] 安装：$skill"
    
    # 方法 1: GitHub 克隆
    cd /tmp
    if git clone "https://github.com/steipete/$skill.git" 2>/dev/null; then
        cp -r "$skill" ~/.openclaw/workspace/skills/
        echo "[$(date)] ✅ $skill 安装成功（GitHub）"
    else
        # 方法 2: ClawHub
        if clawhub install "$skill" 2>/dev/null; then
            echo "[$(date)] ✅ $skill 安装成功（ClawHub）"
        else
            echo "[$(date)] ❌ $skill 安装失败"
        fi
    fi
    
    # 等待 1 小时
    sleep 3600
done
```

---

## 🔗 GitHub 仓库汇总

所有技能均由 **@steipete** 开发，仓库地址：

```
https://github.com/steipete/gog
https://github.com/steipete/github
https://github.com/steipete/notion
https://github.com/steipete/weather
https://github.com/steipete/nano-pdf
https://github.com/steipete/obsidian
https://github.com/steipete/openai-whisper
https://github.com/steipete/nano-banana-pro
https://github.com/steipete/brave-search
https://github.com/steipete/summarize
```

**统一克隆命令**:
```bash
for skill in gog github notion weather nano-pdf obsidian openai-whisper nano-banana-pro brave-search summarize; do
    git clone "https://github.com/steipete/$skill.git" /tmp/$skill
    cp -r /tmp/$skill ~/.openclaw/workspace/skills/
done
```

---

**清单创建时间**: 2026-03-22 08:45 GMT+8  
**数据来源**: ClawHub.ai 实时抓取  
**下次更新**: 安装完成后
