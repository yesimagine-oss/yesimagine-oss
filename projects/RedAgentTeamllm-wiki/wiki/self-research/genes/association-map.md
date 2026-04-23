# 自研项目基因关联图谱

**创建时间**: 2026-04-22  
**维护者**: Red Agent Team  
**版本**: v1.0.0

---

## 🎯 作用

可视化展示所有基因之间的关联关系，支持：
- ✅ 快速定位相关基因
- ✅ 理解知识脉络
- ✅ 发现知识盲区

---

## 🧬 goEX 基因关联图

```
┌─────────────────────────────────────────────────────────┐
│                    goEX 基因生态                         │
└─────────────────────────────────────────────────────────┘

设计基因 (design-gene.md)
  ├── design_001: 用户心血 > 代码整洁
  │     └── 关联：v0.5.0-test-gene.md (事故后恢复)
  │
  ├── design_002: 插件化 + 完整性双轨制
  │     └── 关联：v0.5.0-test-gene.md (架构验证)
  │
  ├── design_003: 渐进式超时策略
  │     └── 关联：100M-test-gene.md (1 亿次验证)
  │
  ├── design_004: 重试 + 降级机制
  │     └── 关联：100M-test-gene.md (稳定性证明)
  │
  └── design_005: 报告驱动开发
        └── 关联：v0.5.0-test-gene.md (4 份报告)

演化基因 (evolution-gene.md)
  ├── evo_001: chromedp 技术选型
  │
  ├── evo_002: 渐进式超时策略
  │     └── 关联：100M-test-gene.md (决策验证)
  │
  ├── evo_003: 插件化架构
  │     └── 关联：v0.5.0-test-gene.md (架构实现)
  │
  └── evo_004: 功能完整性优先
        └── 关联：v0.5.0-test-gene.md (事故后原则)

事故基因 (accident-gene.md)
  ├── acc_001: AI 价值观偏差
  │     └── 关联：accident-data-gene.md (完整数据)
  │
  ├── acc_002: 变更确认缺失
  │     ├── 关联：accident-data-gene.md
  │     └── 产出：function-change-sop.md (SOP)
  │
  ├── acc_003: 测试覆盖不足
  │     └── 关联：accident-data-gene.md
  │
  ├── acc_004: 记忆检索缺陷
  │     └── 关联：accident-data-gene.md
  │
  └── acc_005: 换位思考缺失
        └── 关联：accident-data-gene.md

数据基因
  ├── 100M-test-gene.md (1 亿次测试)
  │     ├── 关联：design_003, design_004, evo_002
  │     └── 数据：assets/reports/test/goEX-100M-test.md
  │
  ├── accident-data-gene.md (事故数据)
  │     ├── 关联：acc_001-005, function-change-sop
  │     └── 数据：assets/reports/accident/
  │
  └── v0.5.0-test-gene.md (v0.5.0 测试)
        ├── 关联：design_001, design_002, evo_003, evo_004
        └── 数据：assets/data/benchmarks/test_report.json
```

---

## 🧬 goToken 基因关联图

```
┌─────────────────────────────────────────────────────────┐
│                  goToken 基因生态                        │
└─────────────────────────────────────────────────────────┘

设计基因 (design-gene.md)
  ├── design_001: 75% Token 节省原则
  │     └── 关联：75pct-hitrate-gene.md (实测验证)
  │
  ├── design_002: 精确匹配缓存策略
  │     └── 关联：75pct-hitrate-gene.md (策略效果)
  │
  ├── design_003: 2 小时缓存 TTL
  │     └── 关联：75pct-hitrate-gene.md (TTL 选择)
  │
  ├── design_004: 并发限流保护
  │
  └── design_005: 适用场景边界

监控基因 (monitoring-gene.md)
  ├── mon_001: 75% 命中率基准
  │     └── 关联：75pct-hitrate-gene.md (数据支撑)
  │
  ├── mon_002: 持续运行能力
  │     └── 关联：75pct-hitrate-gene.md (2 小时 20 分钟)
  │
  └── mon_003: 生产环境预估模型
        └── 关联：75pct-hitrate-gene.md (ROI 计算)

数据基因
  └── 75pct-hitrate-gene.md (75% 命中率)
        ├── 关联：design_001, design_002, design_003
        └── 数据：assets/data/benchmarks/metrics.json
```

---

## 🔗 跨项目关联

```
goEX  ←→  goToken
  │          │
  │          └── goToken 为 goEX 节省 Token
  │
  └── 共同遵循原则：
      ├── 用户心血 > 代码整洁
      ├── 诚实第一
      └── 持续监控
```

---

## 📊 关联统计

| 项目 | 基因文档 | 基因编码 | 关联数 |
|------|---------|---------|--------|
| goEX | 6 | 14 | 20+ |
| goToken | 3 | 8 | 10+ |
| **总计** | **9** | **22** | **30+** |

---

## 🧭 使用指南

### 场景 1: 了解 goEX 设计思想

```
起点：design-gene.md
  ↓ 阅读 5 条设计基因
  ↓ 查看关联的测试数据 (100M-test-gene.md, v0.5.0-test-gene.md)
  ↓ 验证设计是否被实践
```

### 场景 2: 学习事故教训

```
起点：accident-gene.md
  ↓ 阅读 5 条事故基因
  ↓ 查看完整数据 (accident-data-gene.md)
  ↓ 学习预防机制 (function-change-sop.md)
```

### 场景 3: 评估 goToken 效果

```
起点：75pct-hitrate-gene.md
  ↓ 查看设计原理 (design-gene.md)
  ↓ 验证监控数据 (monitoring-gene.md)
  ↓ 计算 ROI (生产环境预估模型)
```

---

## 🔍 基因编码索引

### goEX

| 编码 | 类型 | 文档 |
|------|------|------|
| `goEX_design_001-005` | 设计 | [design-gene.md](./goEX/design-gene.md) |
| `goEX_evo_001-004` | 演化 | [evolution-gene.md](./goEX/evolution-gene.md) |
| `goEX_acc_001-005` | 事故 | [accident-gene.md](./goEX/accident-gene.md) |
| `goEX_data_001-003` | 数据 | 本图谱 |

### goToken

| 编码 | 类型 | 文档 |
|------|------|------|
| `goToken_design_001-005` | 设计 | [design-gene.md](./goToken/design-gene.md) |
| `goToken_mon_001-003` | 监控 | [monitoring-gene.md](./goToken/monitoring-gene.md) |
| `goToken_data_001` | 数据 | [75pct-hitrate-gene.md](./goToken/75pct-hitrate-gene.md) |

---

**最后更新**: 2026-04-22  
**状态**: ✅ 关联图谱已建立
