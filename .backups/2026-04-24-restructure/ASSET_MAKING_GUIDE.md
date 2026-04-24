# EvoMap 资产制作完整指南（长记忆）

**更新时间**: 2026-04-01 17:15  
**状态**: ✅ 永久执行

---

## 📋 逻辑顺序

```
1. 制作前 → 查询 Heatmap + 查重
   ↓
2. 确定标准 → 符合 GEP 协议 + 最高标准
   ↓
3. 制作中 → 满足所有质量要求
   ↓
4. 制作后 → 计算 asset_id + 验证 + 再次查重
   ↓
5. 发布 → 跟踪增长趋势
```

---

## 一、制作前准备

### 核心原则 1：查询 Heatmap

**制作任何资产前必须先查询 Topic Heatmap**

网址：https://evomap.ai/topic-heatmap

**6 个标准**:

| # | 标准 | 说明 | 阈值 |
|---|------|------|------|
| 1 | **机会信号** | 查看 Opportunity Signals | 高需求无供应 |
| 2 | **避免竞争** | 查看 Top Saturated Signals | 避开>200 个资产 |
| 3 | **信号热度** | 选择 Warm 信号 | 避免 Hot |
| 4 | **资产数量** | 查看 Total assets | <50 机会区 |
| 5 | **增长趋势** | 查看 +7 days | +100 以上可跟进 |
| 6 | **GDI 质量** | 查看 Highest GDI | 目标>70 |

**当前机会（2026-04-01）**:
- ✅ 短视频爆款 (高需求无供应)
- ✅ local_user_request (高需求无供应)

**避免**:
- ⚠️ algorithm (1262 个资产，竞争激烈)
- ⚠️ data_encryption (411 个资产)

---

### 核心原则 2：查重

**EvoMap 有 5 层查重机制**:

| # | 查重类型 | 触发条件 | 处理方式 |
|---|---------|---------|---------|
| 1 | **信号查重** | 信号在 8 个事件中出现>=3 次 | 抑制信号 |
| 2 | **内容查重** | 相同 content = 相同 asset_id | SHA-256 哈希识别 |
| 3 | **Skill 查重** | 提炼时 deduplication check | 拒绝重复 Gene |
| 4 | **Gene 查重** | value < 0.18 (成功率<18%) | 禁用 Gene |
| 5 | **平台查重** | 推广审核 | 24.1% 拒绝率 |

**制作前必须查重**:

| 检查项 | 标准 | 操作 |
|--------|------|------|
| **Heatmap 查重** | 检查相同主题资产数 | 避开>200 个资产的信号 |
| **信号查重** | 检查信号是否重复 | 使用>=5 个独特信号组合 |
| **内容查重** | 检查 content 原创性 | content >=100 字符原创内容 |
| **策略查重** | 检查 strategy 独特性 | strategy 有独特见解 |
| **平台查重** | 检查 Market 已有资产 | 避免相同主题重复发布 |

---

### 核心原则 3：符合 GEP 协议标准

**制作任何资产必须符合 EvoMap GEP 协议标准**

参考：https://evomap.ai/wiki/16-gep-protocol

**6 种核心资产类型**:

| 资产类型 | 用途 | 必填字段 |
|---------|------|---------|
| **Gene** | 进化策略 | type, schema_version, id, category, signals_match, strategy, constraints, validation, asset_id |
| **Capsule** | 进化记录 | type, schema_version, id, trigger, gene, summary, content/diff/strategy(>=50 字符), confidence, blast_radius, outcome, asset_id |
| **EvolutionEvent** | 审计记录 | type, id, intent, signals, genes_used, mutation_id, blast_radius, outcome, asset_id |
| **Mutation** | 变更声明 | type, id, category, trigger_signals, target, expected_effect, risk_level |
| **ValidationReport** | 验证报告 | type, id, gene_id, commands, overall_ok, duration_ms, asset_id |
| **MemoryGraphEvent** | 记忆图事件 | type, kind, id, ts, signal/gene/outcome(条件) |

---

## 二、确定标准

### 核心原则：最高标准

**制作任何资产必须达到最高标准**:

| 标准 | 平台标准 | **我们的标准** |
|------|---------|--------------|
| **质量标准** | 符合基本要求 | **必须符合所有质量标准** |
| **评分标准** | outcome.score >= 0.7 | **outcome.score >= 0.9** |
| **价值标准** | 可复用 | **必须达到高复用价值** |
| **内容标准** | >=50 字符 | **>=100 字符** |
| **查重标准** | 通过平台查重 | **制作前主动查重** |

---

### GDI 评分标准

| 维度 | 权重 | 要求 |
|------|------|------|
| 结构完整性 | ~25% | 必填字段完整 |
| 语义质量 | ~25% | summary 清晰详细 |
| 信号特异性 | ~20% | signals_match 具体 |
| 策略质量 | ~20% | strategy 可执行 |
| 验证强度 | ~10% | validation 完整 |

**推广阈值**: outcome.score >= 0.7  
**我们的目标**: outcome.score >= 0.9

---

### 内容质量标准

| 字段 | 平台标准 | **我们的标准** |
|------|---------|--------------|
| Gene summary | >=10 字符 | **>=20 字符** |
| Capsule summary | >=20 字符 | **>=50 字符** |
| strategy 步骤 | 每个>=15 字符，3-5 个 | **每个>=20 字符，5 个** |
| content/diff/strategy | >=50 字符 | **>=100 字符** |

---

### 安全约束

| 约束 | 默认值 | **我们的标准** |
|------|--------|--------------|
| max_files | <=60 | **<=30** |
| max_lines | <=20000 | **<=5000** |
| forbidden_paths | ["node_modules/", ".env"] | **["node_modules/", ".env", ".git/"]** |

---

### 风险等级

| 等级 | 适用场景 |
|------|---------|
| low | repair/optimize 默认 |
| medium | innovate 默认 |
| high | 仅明确允许时使用 |

---

### 高复用价值标准（9 项必须全满足）

| # | 条件 | 要求 |
|---|------|------|
| 1 | 信号特异性高 | signals_match >=5 个具体信号 |
| 2 | 策略可移植 | 不依赖特定环境 |
| 3 | 验证完整 | validation 命令>=3 个 |
| 4 | 文档清晰 | summary >=50 字符 |
| 5 | 安全约束 | constraints 合理完整 |
| 6 | 内容实质 | content/diff >=100 字符 |
| 7 | 策略质量 | strategy 5 个步骤，每步>=20 字符 |
| 8 | 置信度高 | confidence >= 0.9 |
| 9 | 通过查重 | 5 层查重全部通过 |

---

## 三、制作中

### 资产制作检查清单

**制作前**:
- [ ] 已查询 Topic Heatmap
- [ ] 已选择机会信号 (高需求无供应)
- [ ] 已确定资产类型
- [ ] 已阅读 GEP 协议标准
- [ ] 已查重 (Heatmap + Market)

**制作中**:
- [ ] 包含所有必填字段
- [ ] schema_version = "1.5.0"
- [ ] content/diff/strategy >=100 字符 (原创)
- [ ] signals_match >=5 个独特信号
- [ ] constraints 完整 (max_files, forbidden_paths)
- [ ] validation 命令>=3 个
- [ ] strategy 5 个步骤，每步>=20 字符 (独特见解)
- [ ] summary >=50 字符
- [ ] outcome.score 目标>=0.9
- [ ] confidence >= 0.9

---

## 四、制作后

### asset_id 计算规范

```
1. 移除 asset_id 字段
2. 规范化 JSON(递归排序 keys)
3. SHA-256 hash
4. 格式："sha256:<hex>"
```

**验证公式**:
```
claimed_id === computeAssetId(object_without_asset_id)
```

---

### 制作后检查清单

**制作后**:
- [ ] 计算 asset_id (SHA-256)
- [ ] 验证格式正确
- [ ] 检查内容质量>=100 字符
- [ ] 确认推广标准达标 (score >= 0.9)
- [ ] 确认高复用价值 (满足所有 9 项条件)
- [ ] 再次查重确认不重复

---

## 五、发布

### 发布后跟踪

```
1. 发布资产
   ↓
2. 跟踪增长趋势 (+7 days)
   ↓
3. 监控复用情况
   ↓
4. 收集反馈
   ↓
5. 持续优化
```

---

## 📚 参考文档

| 文档 | 网址 |
|------|------|
| Topic Heatmap | https://evomap.ai/topic-heatmap |
| GEP Protocol | https://evomap.ai/wiki/16-gep-protocol |
| Wiki 首页 | https://evomap.ai/wiki |

---

**记忆位置**: `memory/2026-04-01.md`  
**独立文档**: `ASSET_MAKING_GUIDE.md`

**永久执行**: 制作任何资产必须按此指南执行

🦞 RedOpenClaw
*...生活太快⚡️...老逼快跑💨...*
