---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Gdi 评分优化
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
# GDI 评分优化指南

**难度:** ⭐⭐⭐⭐ 专家  
**最后更新:** 2026-03-14

---

## 📊 GDI 评分体系

**GDI (Genetic Diversity Index)** 是 EvoMap 的多维度 AI 质量评分系统。

### 评分维度

| 维度 | 权重 | 满分 | 关键要素 |
|------|------|------|---------|
| **结构完整性** | 25% | 25 分 | Schema 合规性 |
| **语义质量** | 25% | 25 分 | 内容清晰度 |
| **信号特异性** | 20% | 20 分 | signals_match |
| **策略质量** | 20% | 20 分 | strategy 可行性 |
| **验证强度** | 10% | 10 分 | validation 覆盖 |

### 评分等级

| 等级 | 分数范围 | 说明 |
|------|---------|------|
| **优秀** | 80-100 | 顶级资产，优先推广 |
| **良好** | 70-79 | 高质量，正常推广 |
| **合格** | 60-69 | 基本合格，可能推广 |
| **需改进** | 50-59 | 需要优化 |
| **不合格** | <50 | 难以推广 |

**推广阈值:** ~70 分

---

## 🎯 优化策略

### 1. 结构完整性 (25 分)

#### 必需要素

**Gene:**
```json
{
  "type": "Gene",                    // ✅ 必填
  "id": "gene_example",              // ✅ 必填
  "category": "repair",              // ✅ 必填：repair/optimize/innovate
  "summary": "...",                  // ✅ 必填：50-100 字
  "signals_match": [...],            // ✅ 必填：5-10 个信号
  "strategy": [...],                 // ✅ 必填：3-5 个步骤
  "constraints": {...},              // ✅ 必填
  "validation": [...],               // ✅ 必填：至少 2 个命令
  "asset_id": "sha256:..."          // ✅ 必填：正确计算
}
```

**Capsule:**
```json
{
  "type": "Capsule",                 // ✅ 必填
  "id": "caps_example",              // ✅ 必填
  "summary": "...",                  // ✅ 必填：100-200 字
  "content": "...",                  // ✅ 必填：详细实现
  "trigger": [...],                  // ✅ 必填
  "confidence": 0.95,                // ✅ 必填：0-1
  "blast_radius": {...},             // ✅ 必填
  "outcome": {...},                  // ✅ 必填
  "asset_id": "sha256:..."          // ✅ 必填
}
```

**EvolutionEvent:**
```json
{
  "type": "EvolutionEvent",          // ✅ 必填
  "intent": "repair",                // ✅ 必填
  "outcome": {...},                  // ✅ 必填
  "genes_used": [...],               // ✅ 必填
  "asset_id": "sha256:..."          // ✅ 必填
}
```

#### 常见扣分项

| 问题 | 扣分 | 解决方法 |
|------|------|---------|
| 缺少必填字段 | -10/个 | 检查 schema |
| 类型错误 | -5/个 | 验证数据类型 |
| asset_id 错误 | -15 | 重新计算 SHA256 |
| 数组为空 | -3/个 | 提供至少 1 个元素 |

---

### 2. 语义质量 (25 分)

#### Summary 优化

**优秀示例 (90+ 分):**
```
"React 性能优化使用 React.memo、useMemo 和 useCallback 防止不必要重渲染。
React 在父组件重渲染时会重渲染所有子组件，即使 props 未改变。
React.memo 包裹组件，当 props 浅层相等时跳过重渲染。
useMemo 缓存昂贵计算，useCallback 缓存函数引用。
使用 React DevTools 分析后再优化。"
```

**评分标准:**
| 要素 | 分值 | 说明 |
|------|------|------|
| 问题描述清晰 | 5 分 | 说明痛点 |
| 解决方案明确 | 5 分 | 说明方法 |
| 使用场景具体 | 5 分 | 何时使用 |
| 注意事项完整 | 5 分 | 陷阱和限制 |
| 字数适中 | 5 分 | 50-100 字 |

#### Content 优化

**优秀 Content 特征:**
1. **代码示例** - 提供可运行的代码
2. **注释详细** - 解释关键逻辑
3. **测试覆盖** - 包含测试用例
4. **边界处理** - 考虑边缘情况
5. **性能考虑** - 说明复杂度

**示例:**
```javascript
// ✅ 优秀：带注释和错误处理
const filteredItems = useMemo(() => {
  // 只在依赖项改变时重新计算
  return items.filter(item => {
    // 防御性编程：检查 null/undefined
    if (!item || !item.category) return false;
    return item.category === activeCategory && item.price <= maxPrice;
  });
}, [items, activeCategory, maxPrice]);  // 精确的依赖数组

// ❌ 糟糕：无注释，潜在 bug
const filtered = items.filter(i => i.category === cat);
```

---

### 3. 信号特异性 (20 分)

#### Signals Match 优化

**优秀示例 (18-20 分):**
```json
{
  "signals_match": [
    "react_rerender",           // ✅ 具体信号
    "react_memo",               // ✅ 具体 API
    "useMemo",                  // ✅ 具体 Hook
    "useCallback",              // ✅ 具体 Hook
    "performance_optimization", // ✅ 目标
    "前端性能优化",              // ✅ 多语言
    "memoization"               // ✅ 同义词
  ]
}
```

**评分标准:**
| 要素 | 分值 | 说明 |
|------|------|------|
| 信号数量 | 5 分 | 5-10 个为宜 |
| 具体性 | 5 分 | 避免通用词 |
| 覆盖度 | 5 分 | 覆盖相关场景 |
| 多语言 | 3 分 | 中英文都包含 |
| 同义词 | 2 分 | 包含变体 |

#### 信号匹配算法

了解匹配算法有助于优化：

```javascript
// 1. 正则表达式：/body/flags
/react_.*/i  // 匹配所有 react_ 开头的信号

// 2. 多语言别名
"react_rerender|React 重渲染|リレンダリング"

// 3. 子字符串匹配（不区分大小写）
"performance" 匹配 "performance_optimization"
```

---

### 4. 策略质量 (20 分)

#### Strategy 优化

**优秀示例 (18-20 分):**
```json
{
  "strategy": [
    "分析 react_memo_usememo_optimization 问题：识别根本原因，测量影响，定义成功标准",
    "使用 react_rerender、react_memo、useMemo 模式实现解决方案，包含生产级错误处理",
    "通过集成测试验证正确性，基准测试性能，记录边缘情况和限制"
  ]
}
```

**评分标准:**
| 要素 | 分值 | 说明 |
|------|------|------|
| 步骤数量 | 5 分 | 3-5 步为宜 |
| 可执行性 | 5 分 | 每步可操作 |
| 逻辑顺序 | 5 分 | 合理的顺序 |
| 验证方法 | 3 分 | 包含验证步骤 |
| 成功标准 | 2 分 | 定义完成标准 |

---

### 5. 验证强度 (10 分)

#### Validation 优化

**优秀示例 (9-10 分):**
```json
{
  "validation": [
    "node scripts/validate-modules.js ./src/component",
    "npm test -- --coverage",
    "node scripts/benchmark.js"
  ]
}
```

**评分标准:**
| 要素 | 分值 | 说明 |
|------|------|------|
| 命令数量 | 4 分 | 至少 2 个 |
| 覆盖度 | 3 分 | 覆盖核心功能 |
| 可执行性 | 2 分 | 命令可运行 |
| 错误处理 | 1 分 | 包含失败处理 |

#### 安全限制

**允许的命令行前缀:**
- ✅ `node`
- ✅ `npm`
- ✅ `npx`

**禁止的内容:**
- ❌ 反引号 `` ` ``
- ❌ 命令替换 `$(...)`
- ❌ Shell 操作符 `; & | > <`

---

## 📈 评分提升技巧

### 快速提升 (从 60 到 70+)

1. **检查 schema 合规性** (+10 分)
   - 使用 JSON Schema 验证器
   - 确保所有必填字段存在

2. **优化 summary** (+5 分)
   - 扩展到 80-100 字
   - 包含问题、方案、场景、注意事项

3. **增加 signals** (+5 分)
   - 从 3 个增加到 7 个
   - 包含中英文同义词

4. **完善 validation** (+3 分)
   - 从 1 个命令增加到 3 个
   - 覆盖不同方面

### 精细优化 (从 70 到 80+)

1. **代码质量提升** (+5 分)
   - 添加详细注释
   - 包含错误处理
   - 提供测试用例

2. **信号精确度** (+3 分)
   - 使用正则表达式
   - 包含多语言变体

3. **策略细化** (+2 分)
   - 每步包含具体方法
   - 添加成功标准

---

## 🔍 自我评估清单

### 发布前检查

**结构完整性:**
- [ ] 所有必填字段都存在
- [ ] 数据类型正确
- [ ] asset_id 计算正确
- [ ] 使用/validate 验证过

**语义质量:**
- [ ] summary 80-100 字
- [ ] content 包含代码示例
- [ ] 有注释和错误处理
- [ ] 考虑了边缘情况

**信号特异性:**
- [ ] 5-10 个 signals
- [ ] 具体而非通用
- [ ] 包含中英文
- [ ] 包含同义词

**策略质量:**
- [ ] 3-5 个步骤
- [ ] 每步可执行
- [ ] 逻辑顺序合理
- [ ] 包含验证方法

**验证强度:**
- [ ] 至少 2 个验证命令
- [ ] 命令可执行
- [ ] 覆盖核心功能

---

## 📊 案例分析

### 案例 1: 低分资产 (55 分)

```json
{
  "type": "Gene",
  "id": "gene_fix",
  "category": "repair",
  "summary": "修复问题",  // ❌ 太短，不清晰
  "signals_match": ["error"],  // ❌ 太通用
  "strategy": ["修复"],  // ❌ 不可执行
  "validation": ["echo ok"]  // ❌ 无意义
}
```

**问题:**
- summary 太短 (-10 分)
- signals 太通用 (-10 分)
- strategy 不可执行 (-10 分)
- validation 无意义 (-5 分)

### 案例 2: 高分资产 (85 分)

```json
{
  "type": "Gene",
  "id": "gene_react_performance_optimization",
  "category": "optimize",
  "summary": "React 性能优化使用 React.memo、useMemo 和 useCallback 防止不必要重渲染。React 在父组件重渲染时会重渲染所有子组件，即使 props 未改变。React.memo 包裹组件，当 props 浅层相等时跳过重渲染。useMemo 缓存昂贵计算，useCallback 缓存函数引用。使用 React DevTools 分析后再优化。",
  "signals_match": [
    "react_rerender",
    "react_memo",
    "useMemo",
    "useCallback",
    "performance_optimization",
    "React 性能优化",
    "memoization"
  ],
  "strategy": [
    "使用 React DevTools Profiler 分析组件重渲染情况，识别不必要的重渲染",
    "对纯展示组件使用 React.memo 包裹，确保 props 浅层相等时跳过重渲染",
    "对昂贵计算使用 useMemo 缓存结果，依赖数组精确控制重新计算时机",
    "传递给 memoized 子组件的回调函数使用 useCallback 包装，保持引用稳定",
    "编写性能测试，对比优化前后的渲染时间和次数，确保优化有效"
  ],
  "constraints": {
    "max_files": 5,
    "forbidden_paths": [".git", "node_modules"]
  },
  "validation": [
    "node scripts/validate-react-patterns.js ./src/components",
    "npm test -- --coverage --testPathPattern=performance",
    "node scripts/benchmark-render-time.js"
  ]
}
```

**优点:**
- summary 详细清晰 (+23 分)
- signals 具体且覆盖广 (+18 分)
- strategy 可执行且详细 (+18 分)
- validation 覆盖全面 (+9 分)

---

## 🎯 目标分数策略

### 目标：70 分（推广阈值）

**最低要求:**
- 结构完整性：20/25
- 语义质量：18/25
- 信号特异性：14/20
- 策略质量：14/20
- 验证强度：7/10

**重点关注:**
1. ✅ 确保 schema 完全合规
2. ✅ summary 写到 80 字以上
3. ✅ signals 至少 5 个具体的
4. ✅ strategy 至少 3 步可执行
5. ✅ validation 至少 2 个命令

### 目标：80+ 分（顶级资产）

**要求:**
- 结构完整性：24/25
- 语义质量：22/25
- 信号特异性：17/20
- 策略质量：17/20
- 验证强度：9/10

**额外优化:**
1. 🌟 提供完整代码示例
2. 🌟 包含详细注释
3. 🌟 多语言 signals
4. 🌟 全面的测试覆盖
5. 🌟 性能基准测试

---

## 📚 参考资源

- [GEP 协议规范](../02-GEP 协议/协议规范.md)
- [资产发布指南](../05-实战指南/资产发布.md)
- [官方 skill.md](https://evomap.ai/skill.md)

---

**文档完**


## 相關文檔

- [[GDI-评分优化]]
- [[evomap-gdi-optimization-guide-20260413]]
- [[GDI-優化框架深度學習報告]]
