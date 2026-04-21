---
category: llm
created_at: '2026-04-14'
tags:
- llm
- skill
- 获取网站评估与推荐
- openclaw
title: 01 Skill 获取网站评估与推荐
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
# Skill 获取网站评估与推荐

**评估时间**: 2026-03-12 21:22 GMT+8
**评估对象**: 4 个 Skill 获取网站

---

## 📚 网站总览

| # | 网站 | URL | 状态 | 推荐度 |
|---|------|-----|------|--------|
| 1 | ClawHub | https://clawhub.ai | ✅ 官方 | ⭐⭐⭐⭐⭐ |
| 2 | Awesome OpenClaw Skills | GitHub | ✅ 社区 | ⭐⭐⭐⭐⭐ |
| 3 | OpenClawMP | https://openclawmp.cc | ⚠️ 访问失败 | ⭐⭐⭐ |
| 4 | GitHub Official | github.com/openclaw/skills | ✅ 官方 | ⭐⭐⭐⭐⭐ |

---

## 1️⃣ ClawHub (官方技能市场)

### 基本信息

| 属性 | 详情 |
|------|------|
| **URL** | https://clawhub.ai |
| **类型** | 官方技能市场 |
| **技能数量** | 13,729+ (截至 2026-02-28) |
| **运营方** | OpenClaw 官方 |
| **安全性** | ⭐⭐⭐⭐⭐ (官方审核) |

### 核心特点

```
✅ 官方技能注册表
✅ VirusTotal 安全扫描
✅ 技能搜索与发现
✅ 一键安装 (clawhub install <skill>)
✅ 技能发布平台
✅ 版本管理
```

### 使用方式

```bash
# 搜索技能
clawhub search <keyword>

# 安装技能
clawhub install <skill-slug>

# 更新技能
clawhub update <skill-name>

# 发布技能
clawhub publish ./my-skill
```

### 优势

| 优势 | 说明 |
|------|------|
| 官方认证 | OpenClaw 官方运营，质量有保障 |
| 安全扫描 | 集成 VirusTotal 安全检测 |
| 一键安装 | 简单的 CLI 安装命令 |
| 版本管理 | 支持技能版本更新 |
| 社区活跃 | 13,000+ 技能，活跃社区 |

### 劣势

| 劣势 | 说明 |
|------|------|
| 需要网络 | 需要访问外网 |
| 英文为主 | 技能描述多为英文 |
| 质量参差 | 社区技能质量不一 |

### 推荐场景

- ✅ 查找常用技能
- ✅ 安装官方推荐技能
- ✅ 发布自己的技能
- ✅ 获取技能更新

---

## 2️⃣ Awesome OpenClaw Skills (GitHub)

### 基本信息

| 属性 | 详情 |
|------|------|
| **URL** | https://github.com/VoltAgent/awesome-openclaw-skills |
| **类型** | 社区精选集合 |
| **技能数量** | 5,494+ (精选) |
| **运营方** | VoltAgent 社区 |
| **安全性** | ⭐⭐⭐⭐ (社区筛选) |

### 核心特点

```
✅ 5,400+ 精选技能
✅ 按分类组织 (30+ 类别)
✅ 安全筛选 (过滤恶意技能)
✅ 质量筛选 (过滤低质量)
✅ GitHub 托管
✅ 持续更新
```

### 技能分类

| 分类 | 数量 | 说明 |
|------|------|------|
| Coding Agents & IDEs | 1,222 | 编程相关 |
| Web & Frontend | 938 | 前端开发 |
| DevOps & Cloud | 409 | 运维云原生 |
| Browser & Automation | 335 | 浏览器自动化 |
| Search & Research | 350 | 搜索研究 |
| AI & LLMs | 197 | AI 大模型 |
| CLI Utilities | 186 | 命令行工具 |
| Image & Video | 169 | 图像视频 |
| Communication | 149 | 通信工具 |
| PDF & Documents | 111 | 文档处理 |
| 其他分类 | 20+ | 更多类别 |

### 筛选标准

| 筛选项 | 排除数量 | 说明 |
|--------|----------|------|
| 可能垃圾 | 4,065 | 批量账号/机器人账号 |
| 重复/相似 | 1,040 | 重复或相似名称 |
| 低质量 | 851 | 低质量或非英文描述 |
| 加密货币 | 611 | 加密货币/区块链/金融 |
| 恶意软件 | 373 | 安全审计发现的恶意技能 |
| **总计排除** | **6,940** | 从官方注册表排除 |

### 使用方式

```bash
# 1. 从 ClawHub 安装
clawhub install <skill-slug>

# 2. 手动安装
# 复制技能文件夹到:
# Global: ~/.openclaw/skills/
# Workspace: <project>/skills/

# 3. 直接使用 GitHub 链接
# 将技能 GitHub 链接发给助手
# 助手会自动处理安装
```

### 优势

| 优势 | 说明 |
|------|------|
| 精选质量 | 过滤 6,940 个低质量/恶意技能 |
| 分类清晰 | 30+ 分类，易于查找 |
| 社区维护 | 活跃社区持续更新 |
| 安全提示 | 明确安全警告和建议 |
| GitHub 托管 | 版本控制，易于审查 |

### 劣势

| 劣势 | 说明 |
|------|------|
| 非官方 | 社区运营，非官方认证 |
| 需要手动 | 部分需要手动安装 |
| 英文为主 | 技能描述多为英文 |

### 推荐场景

- ✅ 查找高质量技能
- ✅ 按分类发现技能
- ✅ 安全优先的技能选择
- ✅ 寻找特定领域技能

---

## 3️⃣ OpenClawMP (访问失败)

### 基本信息

| 属性 | 详情 |
|------|------|
| **URL** | https://openclawmp.cc |
| **类型** | 第三方技能平台 |
| **状态** | ⚠️ 访问失败 |
| **安全性** | ⭐⭐ (未知) |

### 状态说明

```
⚠️ 网站访问失败
⚠️ 无法获取详细信息
⚠️ 建议谨慎使用
```

### 建议

- ⚠️ 暂时无法访问，建议后续再试
- ⚠️ 第三方平台，使用前请审查安全
- ⚠️ 优先使用官方和知名社区资源

---

## 4️⃣ GitHub Official (官方仓库)

### 基本信息

| 属性 | 详情 |
|------|------|
| **URL** | https://github.com/openclaw/skills |
| **类型** | 官方技能仓库 |
| **技能数量** | 13,729+ |
| **运营方** | OpenClaw 官方 |
| **安全性** | ⭐⭐⭐⭐⭐ (官方) |

### 核心特点

```
✅ 官方技能仓库
✅ 所有 ClawHub 技能来源
✅ 源代码可审查
✅ PR 贡献机制
✅ 版本控制
✅ 安全审核
```

### 使用方式

```bash
# 1. 浏览技能
# https://github.com/openclaw/skills/tree/main/skills

# 2. 安装技能
clawhub install <skill-slug>

# 3. 贡献技能
# Fork 仓库 → 添加技能 → 提交 PR
```

### 优势

| 优势 | 说明 |
|------|------|
| 官方认证 | OpenClaw 官方维护 |
| 源码可查 | 完整源代码可审查 |
| 贡献机制 | 可提交 PR 贡献技能 |
| 版本控制 | Git 版本管理 |
| 安全审核 | 官方安全审核流程 |

### 劣势

| 劣势 | 说明 |
|------|------|
| 需要 Git 知识 | 贡献需要 Git 基础 |
| 浏览不便 | 不如 ClawHub 界面友好 |

### 推荐场景

- ✅ 审查技能源代码
- ✅ 贡献自己的技能
- ✅ 查找最新技能
- ✅ 参与官方社区

---

## 📊 网站对比总结

| 维度 | ClawHub | Awesome | OpenClawMP | GitHub |
|------|---------|---------|------------|--------|
| 技能数量 | 13,729+ | 5,494+ | 未知 | 13,729+ |
| 官方认证 | ✅ | ❌ | ❌ | ✅ |
| 安全审核 | ✅ | ⚠️ | ❓ | ✅ |
| 使用便捷 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❓ | ⭐⭐⭐ |
| 分类组织 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❓ | ⭐⭐ |
| 社区活跃 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❓ | ⭐⭐⭐⭐⭐ |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 推荐使用策略

### 日常使用 (首选)

```
1. ClawHub (clawhub.ai)
   └── 搜索和安装技能的主要平台
   └── 一键安装，最便捷
```

### 技能发现 (辅助)

```
2. Awesome OpenClaw Skills (GitHub)
   └── 按分类发现高质量技能
   └── 安全筛选，质量有保障
```

### 源码审查 (深入)

```
3. GitHub Official (github.com/openclaw/skills)
   └── 审查技能源代码
   └── 贡献自己的技能
```

### 谨慎使用

```
4. OpenClawMP (openclawmp.cc)
   └── 暂时无法访问
   └── 第三方平台，需谨慎
```

---

## 🔒 安全建议

### 安装前检查

```bash
# 1. 查看技能来源
# 优先选择官方和知名作者

# 2. 检查 VirusTotal 报告
# 在 ClawHub 技能页面查看安全扫描结果

# 3. 审查源代码
# 查看技能代码，确认无恶意行为

# 4. 使用安全工具
# - Snyk Skill Security Scanner
# - Agent Trust Hub
```

### 安全工具推荐

| 工具 | URL | 用途 |
|------|-----|------|
| VirusTotal | virustotal.com | 恶意软件扫描 |
| Snyk Scanner | github.com/snyk/agent-scan | 技能安全扫描 |
| Agent Trust Hub | ai.gendigital.com/agent-trust-hub | 代理信任评估 |

---

## 📝 快速参考

### 常用命令

```bash
# 搜索技能
clawhub search weather
clawhub search news
clawhub search github

# 安装技能
clawhub install weather
clawhub install searxng

# 更新技能
clawhub update --all
clawhub update weather

# 查看已安装
clawhub list
openclaw skills list
```

### 技能安装位置

| 位置 | 路径 | 优先级 |
|------|------|--------|
| Global | `~/.openclaw/skills/` | 低 |
| Workspace | `<project>/skills/` | 中 |
| Bundled | 内置技能 | 最低 |

**优先级**: Workspace > Global > Bundled

---

## 💡 最佳实践

### 技能选择

1. ✅ 优先选择官方技能
2. ✅ 查看作者信誉
3. ✅ 检查下载量/评分
4. ✅ 阅读技能文档
5. ✅ 审查源代码

### 技能管理

1. ✅ 定期更新技能
2. ✅ 禁用不常用技能
3. ✅ 卸载不再需要的技能
4. ✅ 记录已安装技能

### 安全实践

1. ✅ 安装前审查代码
2. ✅ 查看 VirusTotal 报告
3. ✅ 使用安全扫描工具
4. ✅ 限制技能权限
5. ✅ 定期安全审计

---

## 📚 学习资源

### 官方文档

- [ClawHub 使用指南](https://docs.openclaw.ai/cli/skills.md)
- [技能开发文档](https://docs.openclaw.ai/tools/creating-skills)
- [安全指南](https://docs.openclaw.ai/gateway/security/)

### 社区资源

- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [OpenClaw Discord](https://discord.gg/clawd)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

---

## ✅ 总结

### 推荐网站 (按优先级)

| 排名 | 网站 | 用途 | 推荐度 |
|------|------|------|--------|
| 1 | ClawHub | 主要技能平台 | ⭐⭐⭐⭐⭐ |
| 2 | Awesome Skills | 技能发现 | ⭐⭐⭐⭐⭐ |
| 3 | GitHub Official | 源码审查 | ⭐⭐⭐⭐⭐ |
| 4 | OpenClawMP | 备选平台 | ⭐⭐ |

### 核心建议

```
✅ 主要使用 ClawHub (官方、便捷、安全)
✅ 辅助使用 Awesome Skills (精选、分类、高质量)
✅ 深入使用 GitHub Official (源码、贡献)
⚠️ 谨慎使用 OpenClawMP (第三方、未知)
```

### 安全提醒

```
⚠️ 安装前始终审查技能代码
⚠️ 查看 VirusTotal 安全报告
⚠️ 使用安全扫描工具
⚠️ 限制技能权限范围
⚠️ 定期运行安全审计
```

---

**评估完成时间**: 2026-03-12 21:25
**建议**: 将 4 个网站加入书签，优先使用 ClawHub 和 Awesome Skills

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]
