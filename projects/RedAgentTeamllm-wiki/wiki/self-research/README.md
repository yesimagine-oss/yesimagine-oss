# 自研项目知识库

**创建时间**: 2026-04-22  
**维护者**: Red Agent Team  
**版本**: v1.0.0

---

## 🎯 定位

存放 Red Agent Team 自研项目的**核心基因**（非代码）。

**基因** = 设计思想 + 演化记录 + 能力胶囊 + 事故复盘

**代码** = 仍在原目录 (`goEX/`, `goToken/`)

---

## 📁 目录结构

```
self-research/
├── index.md              # 知识库索引
├── README.md             # 本说明
├── genes/                # 基因库
│   ├── goEX/
│   │   ├── design-gene.md      # 设计思想
│   │   ├── evolution-gene.md   # 演化记录
│   │   └── accident-gene.md    # 事故复盘
│   └── goToken/
│       ├── design-gene.md      # 缓存设计
│       └── monitoring-gene.md  # 监控数据
├── projects/             # 项目文档（可选）
│   ├── goEX/
│   └── goToken/
└── capsules/             # 可复用能力胶囊（未来扩展）
```

---

## 🧬 基因提取原则

### ✅ 应该提取

- 设计思想（为什么这样设计）
- 演化记录（关键决策点）
- 事故复盘（教训 + 预防机制）
- 监控数据（运行基准）
- 最佳实践（SOP、规范）

### ❌ 不应提取

- 源代码（在 `goEX/`、`goToken/`）
- 配置文件（在项目目录）
- 临时日志（在 `logs/`）

---

## 📊 当前项目

| 项目 | 基因数 | 状态 |
|------|--------|------|
| goEX | 3 | ✅ v0.5.0 |
| goToken | 2 | ✅ 运行中 |

---

## 🔗 相关链接

| 链接 | 说明 |
|------|------|
| [索引](./index.md) | 自研项目知识库索引 |
| [OpenClaw 知识库](../openclaw/index.md) | OpenClaw 官方文档 |
| [goEX 代码](../../goEX/) | goEX 源代码 |
| [goToken 代码](../../goToken/) | goToken 源代码 |

---

**最后更新**: 2026-04-22  
**状态**: ✅ 创建完成
