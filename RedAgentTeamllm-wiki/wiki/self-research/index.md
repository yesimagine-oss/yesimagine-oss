---
category: self-research
created_at: '2026-04-22'
tags:
- self-research
- goEX
- goToken
- genes
title: 自研项目知识库
type: index
version: '1.0.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 1.0

# Trust Boundary
trust_level: "internal"
evidence_level: "自研项目索引"
---

# 自研项目知识库

**最后更新**: 2026-04-22  
**维护者**: Red Agent Team  
**版本**: v1.0.0

---

## 🎯 定位

存放 Red Agent Team 自研项目的**核心基因**（非代码）：
- ✅ 设计思想
- ✅ 演化记录
- ✅ 能力胶囊
- ✅ 事故复盘
- ❌ 源代码（代码在 `goEX/`、`goToken/` 目录）

---

## 📊 项目概览

| 项目 | 类型 | 状态 | 基因数 |
|------|------|------|--------|
| **goEX** | 浏览器自动化 | ✅ v0.5.0 | 3 |
| **goToken** | Token 缓存优化 | ✅ 运行中 | 2 |

---

## 🧬 基因库

### goEX 基因

| 基因 | 文件 | 说明 |
|------|------|------|
| **设计基因** | `genes/goEX/design-gene.md` | 插件化架构设计思想 |
| **演化基因** | `genes/goEX/evolution-gene.md` | v0.4.0→v0.5.0 演化记录 |
| **事故基因** | `genes/goEX/accident-gene.md` | 2026-04-22 P0 事故复盘 |

### goToken 基因

| 基因 | 文件 | 说明 |
|------|------|------|
| **设计基因** | `genes/goToken/design-gene.md` | 缓存优化设计思想 |
| **监控基因** | `genes/goToken/monitoring-gene.md` | 运行监控数据 |

---

## 📁 目录结构

```
self-research/
├── index.md              # 本索引
├── README.md             # 自研项目说明
├── genes/                # 基因库
│   ├── goEX/
│   │   ├── design-gene.md
│   │   ├── evolution-gene.md
│   │   └── accident-gene.md
│   └── goToken/
│       ├── design-gene.md
│       └── monitoring-gene.md
├── projects/             # 项目文档
│   ├── goEX/
│   └── goToken/
└── capsules/             # 可复用能力胶囊
```

---

## 🔗 相关链接

| 链接 | 说明 |
|------|------|
| [OpenClaw 知识库](../openclaw/index.md) | OpenClaw 官方文档 |
| [goEX 代码](../../goEX/) | goEX 源代码 |
| [goToken 代码](../../goToken/) | goToken 源代码 |

---

**最后更新**: 2026-04-22  
**状态**: ✅ 创建完成
