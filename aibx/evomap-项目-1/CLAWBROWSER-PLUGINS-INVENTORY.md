---
title: "Clawbrowser Plugins Inventory"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# ClawBrowser Core 配套插件清单

**更新时间**: 2026-04-04 12:40  
**核心 Skill**: ClawBrowser Core v1.0.0（已发布）

---

## 📊 现有内容盘点

### ✅ 已发布

| Skill | 状态 | 关联度 | 说明 |
|-------|------|--------|------|
| **ClawBrowser Core** | ✅ 已上架 | ⭐⭐⭐⭐⭐ | 核心浏览器引擎 |

---

### 🔌 可直接转化为插件的内容

#### P0: 高优先级（直接可用）

| 插件名称 | 现有内容 | 转化难度 | 预计时间 |
|---------|---------|---------|---------|
| **clawbrowser-wechat** | wechat-article-grabber | ⭐ 低 | 1 小时 |
| **clawbrowser-content-collector** | content-collector | ⭐ 低 | 1 小时 |

**详情**:

1. **clawbrowser-wechat** (微信文章抓取)
   - 现有内容: `skills/wechat-article-grabber/`
   - 功能：自动抓取微信文章
   - 转化：将现有脚本封装为 Skill 格式
   - 依赖：ClawBrowser Core

2. **clawbrowser-content-collector** (内容收集器)
   - 现有内容: `skills/content-collector/`
   - 功能：全自動內容收藏系統
   - 转化：将 Playwright 脚本改为 ClawBrowser
   - 依赖：ClawBrowser Core

---

#### P1: 中优先级（需适配）

| 插件名称 | 现有内容 | 转化难度 | 预计时间 |
|---------|---------|---------|---------|
| **clawbrowser-auto-login** | evolver 登录逻辑 | ⭐⭐ 中 | 2 小时 |
| **clawbrowser-screenshot** | agent-browser 截图 | ⭐⭐ 中 | 2 小时 |
| **clawbrowser-pdf-export** | agent-browser PDF | ⭐⭐ 中 | 2 小时 |

**详情**:

1. **clawbrowser-auto-login** (自动登录)
   - 现有内容：evolver 中的登录逻辑
   - 功能：网站自动登录（知乎/微博等）
   - 转化：提取登录逻辑，封装为 Skill

2. **clawbrowser-screenshot** (批量截图)
   - 现有内容：agent-browser 截图功能
   - 功能：批量网页截图
   - 转化：封装为 Skill 格式

3. **clawbrowser-pdf-export** (PDF 导出)
   - 现有内容：agent-browser PDF 功能
   - 功能：网页转 PDF
   - 转化：封装为 Skill 格式

---

#### P2: 低优先级（需开发）

| 插件名称 | 灵感来源 | 转化难度 | 预计时间 |
|---------|---------|---------|---------|
| **clawbrowser-zhihu** | 知乎抓取需求 | ⭐⭐⭐ 高 | 3 小时 |
| **clawbrowser-weibo** | 微博抓取需求 | ⭐⭐⭐ 高 | 3 小时 |
| **clawbrowser-xiaohongshu** | 小红书抓取需求 | ⭐⭐⭐ 高 | 3 小时 |
| **clawbrowser-seo-audit** | SEO 审计需求 | ⭐⭐⭐ 高 | 4 小时 |
| **clawbrowser-price-monitor** | 电商价格监控 | ⭐⭐⭐ 高 | 4 小时 |
| **clawbrowser-competitor-analysis** | 竞品分析需求 | ⭐⭐⭐ 高 | 4 小时 |

---

### 📋 其他相关 Skill（可参考）

| Skill | 位置 | 可借鉴内容 |
|-------|------|-----------|
| **EvoMap WorkBench** | `evomap-workbench/` | Skill 格式、发布流程 |
| **EvoMap Server Sentinel** | `evomap-server-sentinel/` | 服务器探测逻辑 |
| **Agent Browser** | `agent-browser/` | 浏览器交互逻辑 |
| **Content Collector** | `content-collector/` | 内容抓取逻辑 |

---

## 🎯 推荐发布顺序

### 今天（剩余 2 个配额）

```
✅ clawbrowser-core (已发布)
⏳ clawbrowser-wechat (推荐 - 已有完整内容)
⏳ clawbrowser-content-collector (推荐 - 已有完整内容)
```

### 明天（配额刷新后）

```
⏳ clawbrowser-screenshot (批量截图)
⏳ clawbrowser-pdf-export (PDF 导出)
⏳ clawbrowser-auto-login (自动登录)
```

### 后天及以后

```
⏳ clawbrowser-zhihu (知乎抓取)
⏳ clawbrowser-weibo (微博抓取)
⏳ clawbrowser-seo-audit (SEO 审计)
...
```

---

## 📁 插件转化模板

### SKILL.md 模板

```markdown
---
name: ClawBrowser {PluginName}
description: {简短描述}
category: automation
tags: ["clawbrowser", "{tag1}", "{tag2}", "automation"]
version: 1.0.0
author: RedOpenClaw
license: MIT
---

# ClawBrowser {PluginName}

## Prerequisites
- ✅ **ClawBrowser Core v1.0.0+** (必须)
- ✅ Python 3.6+

## Trigger Signals
- `{signal1}` -- 当...时触发
- `{signal2}` -- 当...时触发

## Strategy
1. **启动浏览器** - 使用 ClawBrowser Core
2. **{步骤 2}**
3. **{步骤 3}**
4. **导出结果**

## Constraints
- 依赖 ClawBrowser Core
- 频率限制：≤10 次/分钟
- 遵守 robots.txt

## Validation
```bash
python3 test_{plugin}.py
```
```

---

## 💰 收益预测

| 插件 | 预计下载/月 | 月收入 |
|------|------------|--------|
| clawbrowser-wechat | 100+ 次 | 500+ 积分 |
| clawbrowser-content-collector | 80+ 次 | 400+ 积分 |
| clawbrowser-screenshot | 50+ 次 | 250+ 积分 |
| clawbrowser-pdf-export | 50+ 次 | 250+ 积分 |
| clawbrowser-auto-login | 40+ 次 | 200+ 积分 |
| **总计** | **320+ 次** | **1600+ 积分** |

---

## 📊 转化状态

| 插件 | 现有内容 | SKILL.md | 测试 | 发布 |
|------|---------|---------|------|------|
| clawbrowser-wechat | ✅ | ⏳ | ⏳ | ⏳ |
| clawbrowser-content-collector | ✅ | ⏳ | ⏳ | ⏳ |
| clawbrowser-screenshot | ✅ | ⏳ | ⏳ | ⏳ |
| clawbrowser-pdf-export | ✅ | ⏳ | ⏳ | ⏳ |
| clawbrowser-auto-login | ⚠️ | ⏳ | ⏳ | ⏳ |

**图例**: ✅ 完成 | ⚠️ 部分完成 | ⏳ 待完成

---

## 🚀 立即行动

### 步骤 1: 选择首个插件

```
推荐：clawbrowser-wechat
理由：
  - 现有内容完整
  - 转化难度低
  - 市场需求大
```

### 步骤 2: 创建 SKILL.md

```bash
cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/skills/
mkdir clawbrowser-wechat
cd clawbrowser-wechat
# 复制 SKILL.md 模板并编辑
```

### 步骤 3: 发布

```bash
python3 publish_skill_auto.py
```

---

**📝 总结**: 目前手上至少有 **2 个可直接转化**的插件内容，预计今天可以完成发布！

---
🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
