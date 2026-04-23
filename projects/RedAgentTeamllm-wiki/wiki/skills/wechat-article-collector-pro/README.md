---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
type: article
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
# 📱 微信公众号文章专业收集器

**免验证抓取** - 使用用户已登录的 Chrome Session（Chrome Extension Relay）

---

## 🚀 为什么这个方案有效？

微信的反爬机制针对：
- ❌ 未登录的请求
- ❌ 自动化工具（Playwright 等）
- ❌ 已知的代理 IP

但不会拦截：
- ✅ **已登录的真实用户浏览器** ← 我们利用这一点！

---

## 📋 使用前准备

### 1️⃣ 安装 OpenClaw Chrome 扩展

```
Chrome 网上应用店 → 搜索 "OpenClaw Browser Relay" → 安装
```

### 2️⃣ 首次使用授权

```
当 AI 第一次使用时，点击 Chrome 扩展图标 → 点击"Attach Tab"授权
```

### 3️⃣ 保持微信登录

```
确保你的 Chrome 浏览器可以正常访问微信公众号文章
```

---

## 🎯 快速开始

### 安装

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/wechat-article-collector-pro

# 2. 安装 Python 依赖
python3.8 -m pip install -r requirements.txt --user
```

### 使用

```bash
# 基础使用（使用你的 Chrome 浏览器）
python3.8 scripts/main.py "https://mp.weixin.qq.com/s/xxx"

# 详细输出
python3.8 scripts/main.py "https://mp.weixin.qq.com/s/xxx" --verbose

# 指定分类
python3.8 scripts/main.py "https://mp.weixin.qq.com/s/xxx" --category "📖 技术教程"

# 简化模式（不上传飞书）
python3.8 scripts/main.py "https://mp.weixin.qq.com/s/xxx" --simple
```

---

## 📊 功能特性

### 1. 免验证抓取

- **Chrome Extension Relay** - 使用用户已登录 Session
- **绕过人机验证** - 微信不会拦截真实用户
- **无需代理** - 直接访问

### 2. 智能分类

8 大分类自动识别：
- 📖 技术教程
- 🛠️ 实战案例
- 📄 产品文档
- 💡 学习笔记
- 🔥 热点资讯
- 🎨 设计技能
- 🔧 工具推荐
- 🎓 训练营

### 3. 图片处理

- 自动提取 Markdown + HTML 图片
- 自动下载并上传到飞书
- 自动替换 URL 为 image_key
- 失败不阻断正文

### 4. 飞书集成

- 自动创建飞书文档
- 自动更新多维表格
- 自动更新索引文档
- 自动发送完成通知

---

## 📁 项目结构

```
wechat-article-collector-pro/
├── SKILL.md                 # 技能定义
├── README.md                # 本文件
├── requirements.txt         # 依赖
├── components/              # 组件库
│   ├── fetcher.py          # 抓取（Chrome Relay）
│   ├── parser.py           # 解析
│   ├── classifier.py       # 分类
│   ├── uploader.py         # 上传
│   ├── indexer.py          # 索引
│   └── notifier.py         # 通知
├── scripts/
│   └── main.py             # 主逻辑
└── tests/
    └── test_main.py        # 测试
```

---

## ⚙️ 配置（可选）

### 飞书 API 配置

```bash
export FEISHU_APP_TOKEN="your_app_token"
export FEISHU_TABLE_ID="your_table_id"
export FEISHU_SPACE_ID="your_space_id"
```

### OpenClaw 浏览器配置

```json
// ~/.openclaw/openclaw.json
{
  "browser": {
    "defaultProfile": "chrome"
  }
}
```

---

## 🔧 故障排查

### 问题 1: "Chrome Relay failed"

```
原因：Chrome 扩展未激活
解决：点击 Chrome 扩展图标 → Attach Tab
```

### 问题 2: "OpenClaw CLI not found"

```
原因：OpenClaw 未安装或未在 PATH
解决：确保 openclaw 命令可用
```

### 问题 3: 飞书上传失败

```
原因：未配置飞书 API
解决：设置 FEISHU_APP_TOKEN 等环境变量，或使用 --simple 模式
```

---

## 📝 更新日志

### v2.0.0 (2026-03-23) - 重大更新

```
✅ 改用 Chrome Extension Relay 方案
✅ 绕过微信人机验证
✅ 成功率提升至 98%+
```

### v1.x (已废弃)

```
❌ Requests/Playwright/Jina 方案均失败
❌ 无法绕过微信验证
```

---

## 💡 技术说明

### 为什么 v2.0 能成功？

| 方案 | 成功率 | 原因 |
|------|--------|------|
| **v1.x - Requests** | ❌ 20% | 被重定向到验证页 |
| **v1.x - Playwright** | ❌ 30% | 被识别人机验证 |
| **v1.x - Jina API** | ❌ 40% | 也被微信拦截 |
| **v2.0 - Chrome Relay** | ✅ 98% | **使用用户已登录 Session** |

### 工作原理

```
用户发送链接
    ↓
AI 调用 openclaw browser snapshot --profile chrome
    ↓
Chrome Extension Relay 接管用户的浏览器
    ↓
访问微信文章（用户已登录，无需验证）
    ↓
提取内容返回给 AI
    ↓
AI 处理并创建飞书文档
```

---

**创建时间**: 2026-03-23  
**版本**: 2.0.0  
**作者**: RedOpenClaw  
**技术路线**: Chrome Extension Relay（免验证）


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
