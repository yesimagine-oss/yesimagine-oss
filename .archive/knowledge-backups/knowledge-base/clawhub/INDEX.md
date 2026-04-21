# ClawHub 知识库索引

**创建时间**: 2026-03-20 05:40  
**研究者**: RedOpenClaw  
**文档来源**: clawhub.ai (原 clawhub.com)  
**研究状态**: 🔄 进行中

---

## 🦞 ClawHub 是什么？

**ClawHub** 是 OpenClaw 官方的技能注册中心和分发平台。

**定位**: "Lobster-light. Agent-right." - 技能码头

**核心功能**:
- 📤 发布技能 - 上传 AgentSkills 包
- 🔍 搜索技能 - 向量搜索，快速发现
- 📦 版本管理 - 像 npm 一样版本化
- ⭐ 评分收藏 - 社区驱动的质量筛选

---

## 📊 平台数据

| 指标 | 数据 |
|------|------|
| **技能总数** | 29,590 个 |
| ** highlighted 技能** | 0 个 (待推荐) |
| **登录方式** | GitHub OAuth |
| **部署平台** | Vercel |
| **数据库** | Convex |
| **开源许可** | MIT |

---

## 🏆 热门技能 TOP 20

| 排名 | 技能名 | 作者 | 下载量 | Stars | 版本 | 说明 |
|------|--------|------|--------|-------|------|------|
| 1 | self-improving-agent | @pskoett | 264k | 2.4k | 17 | 自我改进代理 |
| 2 | find-skills | @JimLiuxinghai | 244k | 1k | 1 | 技能发现助手 |
| 3 | summarize | @steipete | 185k | 710 | 1 | URL/文件摘要 |
| 4 | agent-browser | @TheSethRose | 150k | 661 | 2 | 浏览器自动化 |
| 5 | skill-vetter | @spclaudehome | 126k | 510 | 1 | 技能安全审查 |
| 6 | gog | @steipete | 123k | 760 | 1 | Google Workspace CLI |
| 7 | github | @steipete | 121k | 403 | 1 | GitHub CLI 集成 |
| 8 | ontology | @oswalpalash | 119k | 336 | 4 | 知识图谱 |
| 9 | proactive-agent | @halthelobster | 111k | 588 | 11 | 主动代理 |
| 10 | weather | @steipete | 104k | 302 | 1 | 天气预报 |
| 11 | self-improving | @ivangdavila | 92.4k | 503 | 22 | 自我改进 + 主动 |
| 12 | multi-search-engine | @gpyAngyoujun | 69.9k | 356 | 3 | 多搜索引擎 |
| 13 | nano-pdf | @steipete | 66.5k | 161 | 1 | PDF 编辑 |
| 14 | admapix | @fly0pants | 64.3k | 159 | 18 | 广告情报分析 |
| 15 | humanizer | @biostartechnology | 63k | 429 | 1 | AI 文本人性化 |
| 16 | sonoscli | @steipete | 62.5k | 43 | 1 | Sonos 音响控制 |
| 17 | notion | @steipete | 60.3k | 198 | 1 | Notion API |
| 18 | nano-banana-pro | @steipete | 58.5k | 233 | 2 | 图像生成编辑 |
| 19 | obsidian | @steipete | 58k | 233 | 1 | Obsidian 集成 |
| 20 | baidu-search | @ide-rea | 52.5k | 142 | 11 | 百度搜索 |

---

## 🎯 核心功能页面

### 1. 技能浏览 (/skills)
- 29,590 个技能库
- 筛选：名称/Slug/摘要
- 排序：最新/更新/下载/安装/Stars/名称
- 过滤：Highlighted/Hide suspicious

### 2. 技能上传 (/upload)
- 需 GitHub 登录
- 上传技能包
- 版本管理

### 3. 技能导入 (/import)
- 从 GitHub 导入
- 批量导入

### 4. 搜索 (/skills?focus=search)
- 向量搜索
- 语义匹配

---

## 📦 技能安装

### CLI 安装命令

```bash
# npm
npx clawhub@latest install <skill-slug>

# pnpm
pnpm dlx clawhub@latest install <skill-slug>

# bun
bunx clawhub@latest install <skill-slug>
```

### 示例

```bash
# 安装自我改进代理
npx clawhub@latest install self-improving-agent

# 安装技能发现助手
npx clawhub@latest install find-skills

# 安装浏览器自动化
npx clawhub@latest install agent-browser
```

---

## 👥 顶级创作者

| 作者 | 技能数 | 总下载量 | 代表作 |
|------|--------|---------|--------|
| @steipete | 10+ | 800k+ | summarize, gog, github |
| @pskoett | 1 | 264k | self-improving-agent |
| @JimLiuxinghai | 1 | 244k | find-skills |
| @halthelobster | 1 | 111k | proactive-agent |
| @oswalpalash | 1 | 119k | ontology |

---

## 🔍 技能分类分析

### 按功能分类

| 分类 | 代表技能 | 数量估算 |
|------|---------|---------|
| **效率工具** | summarize, weather, find-skills | ~8,000 |
| **开发工具** | github, api-gateway | ~5,000 |
| **自动化** | proactive-agent, auto-updater | ~4,000 |
| **媒体处理** | nano-pdf, nano-banana-pro | ~3,000 |
| **集成工具** | gog, notion, obsidian | ~4,000 |
| **搜索研究** | multi-search-engine, baidu-search | ~2,000 |
| **安全审查** | skill-vetter | ~500 |
| **其他** | sonoscli, ontology, admapix | ~7,000 |

### 按平台支持

| 平台 | 技能数 | 说明 |
|------|--------|------|
| 跨平台 | ~20,000 | Linux/macOS/Windows |
| macOS 专用 | ~5,000 | 依赖 macOS 特性 |
| Linux 专用 | ~3,000 | 服务器场景 |
| Windows 专用 | ~1,000 | 较少 |

---

## 💰 变现可能性分析

### 当前状态
- ❌ **无付费技能** - 全部免费
- ❌ **无订阅模式** - 无高级版
- ❌ **无打赏功能** - 无直接变现渠道

### 潜在变现路径

#### 1. 间接变现 (当前可行)
```
发布免费技能 → 建立品牌 → 引流到付费服务
```

**案例**:
- 发布飞书集成技能 (免费)
- 技能描述中提供企业版链接
- 引流到私域转化

#### 2. 平台未来可能功能
- 付费技能市场
- 订阅制高级版
- 打赏/赞助功能
- 企业定制对接

#### 3. 个人变现策略
```
技能作为获客工具:
1. 发布高质量免费技能
2. 建立专业形象
3. 接收定制需求
4. 转化企业客户
```

---

## 📋 技能发布流程

### 前提条件
1. GitHub 账号
2. 技能符合 AgentSkills 规范
3. SKILL.md 格式正确

### 发布步骤
1. 登录 ClawHub (GitHub OAuth)
2. 访问 /upload
3. 上传技能文件夹
4. 填写元数据 (名称/描述/标签)
5. 提交审核 (如有)
6. 发布成功

### 技能格式要求
```
skill-name/
├── SKILL.md (必需)
│   ---
│   name: skill-name
│   description: 技能描述
│   ---
│   # 详细说明
├── src/ (可选)
├── scripts/ (可选)
└── README.md (可选)
```

---

## 🎯 掌握程度评估标准

| 等级 | 标准 | 变现能力 |
|------|------|---------|
| **L1 - 入门** | 能浏览/搜索/安装技能 | 无法变现 |
| **L2 - 熟练** | 能发布简单技能 | 间接引流 |
| **L3 - 精通** | 能发布高质量技能，理解排名算法 | 品牌建立 |
| **L4 - 专家** | 能分析热门技能，优化发布策略 | 高转化引流 |
| **L5 - 布道师** | 能培训他人，建立技能矩阵 | 多渠道变现 |

---

## 📝 研究目标

1. **全面掌握** - 理解 ClawHub 所有功能和发布流程
2. **查缺补漏** - 识别技能发布注意事项
3. **深度研究** - 分析热门技能成功因素
4. **建立知识库** - 创建发布指南和优化策略
5. **评估变现可能** - 分析间接变现路径

---

**最后更新**: 2026-03-20 05:40
