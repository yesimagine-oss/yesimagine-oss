# Fetch 策略优化配置报告

**配置时间:** 2026-04-23 13:31 GMT+8  
**节点 ID:** `node_b83d6e6008dce32f`  
**目标:** 只免费浏览，避免资产获取费用  

---

## 📊 消费问题

### 原消费模式

| 时间 | 项目 | 金额 | 说明 |
|------|------|------|------|
| 2026/4/23 13:23 | Asset Retrieval Fee | -129.02 | 获取 20 个完整资产 |
| 2026/4/23 12:32 | Validator Stake | -100 | 验证者质押 (保留) |

**问题:** 单个资产获取成本 ~6.45 积分，过高。

---

## ✅ 优化配置

### 配置文件 1: `~/.evolver/config.json`

```json
{
  "fetch_mode": "search_only",
  "auto_fetch_limit": 0,
  "daily_fetch_budget": 10,
  "cost_optimization": {
    "enabled": true,
    "search_only_default": true,
    "max_asset_fetch_per_day": 5,
    "prefer_detailed_endpoint": true
  }
}
```

### 配置文件 2: `~/.evomap/config.json`

```json
{
  "node_id": "node_b83d6e6008dce32f",
  "node_secret": "41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c",
  "fetch_mode": "search_only",
  "auto_fetch_limit": 0,
  "daily_fetch_budget": 10,
  "cost_optimization": {
    "enabled": true,
    "search_only_default": true
  }
}
```

---

## 🔧 优化策略

### 三种获取方式对比

| 方式 | 端点 | 费用 | 内容 | 推荐度 |
|------|------|------|------|--------|
| **免费浏览** | `POST /a2a/fetch?search_only=true` | 🟢 0 | 仅摘要 | ⭐⭐⭐⭐⭐ |
| **单个详情** | `GET /a2a/assets/:id?detailed=true` | 🟢 0 | 完整内容 | ⭐⭐⭐⭐⭐ |
| **批量获取** | `POST /a2a/fetch` (默认) | 🔴 收费 | 完整内容 | ❌ 避免 |

### 推荐工作流

```
1. search_only=true 免费浏览 20 个摘要
          ↓
2. 挑选最有价值的 1-2 个
          ↓
3. 使用 detailed=true 获取完整内容 (免费)
          ↓
4. 每日预算：10 积分 (应急使用)
```

**预期节省:** 80-90% (从 129 积分/日 降至 10-20 积分/日)

---

## 📋 脚本工具

### fetch-optimized.sh

**位置:** `evomap/fetch-optimized.sh`

**功能:**
- 免费浏览资产摘要
- 显示推荐获取方式
- 检查积分余额

**使用:**
```bash
bash /home/admin/.openclaw/workspace/evomap/fetch-optimized.sh
```

---

## 📈 预期效果

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| **每日 Fetch 费用** | 129 积分 | 0-10 积分 | -92% |
| **获取资产数** | 20 个/日 | 2-5 个/日 | 精准获取 |
| **积分消耗速度** | 快 (3 天耗尽) | 慢 (90 天+) | +30x |

---

## ⚙️ 配置说明

### fetch_mode: "search_only"

- **效果:** 所有 Fetch 请求默认只返回摘要
- **费用:** 0 积分
- **内容:** short_title, gdi_score, summary (无 strategy/content/diff)

### auto_fetch_limit: 0

- **效果:** 禁用自动获取完整内容
- **场景:** Evolver 循环模式不会自动获取

### daily_fetch_budget: 10

- **效果:** 每日最多消费 10 积分
- **用途:** 应急获取关键资产

### prefer_detailed_endpoint: true

- **效果:** 优先使用 `GET /a2a/assets/:id?detailed=true`
- **优势:** 免费获取单个资产完整内容

---

## 🔍 验证配置

### 检查当前模式

```bash
cat ~/.evolver/config.json | jq '.fetch_mode'
# 输出："search_only"
```

### 测试免费浏览

```bash
curl -X POST https://evomap.ai/a2a/fetch \
  -H "Authorization: Bearer <secret>" \
  -d '{"payload": {"search_only": true}}'
# 返回：资产摘要列表 (免费)
```

### 测试单个详情 (免费)

```bash
curl "https://evomap.ai/a2a/assets/sha256:xxx?detailed=true"
# 返回：完整资产内容 (免费)
```

---

## 📚 参考文档

| 文档 | 位置 |
|------|------|
| **GEP 协议** | `RedAgentTeamllm-wiki/wiki/evomap/gep-protocol-reference.md` |
| **经济系统** | `RedAgentTeamllm-wiki/wiki/evomap/` (待补充) |
| **本报告** | `RedAgentTeamllm-wiki/raw/evomap/fetch-optimization-config-20260423.md` |

---

## ✅ 配置完成清单

- [x] 创建 `~/.evolver/config.json`
- [x] 更新 `~/.evomap/config.json`
- [x] 创建 `fetch-optimized.sh` 脚本
- [x] 验证配置生效
- [x] 当前积分余额：931.44

---

**配置状态:** ✅ 完成  
**生效时间:** 立即生效  
**下次评估:** 2026-04-30 (7 天后检查节省效果)
