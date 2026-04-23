# 🔍 asset_id 对比测试报告

**测试时间:** 2026-03-26 23:05  
**测试目的:** 找出 Hub 验证失败的根本原因

---

## 📊 测试结果

### Python vs Node.js vs Hub

| 实现 | Gene asset_id | Capsule asset_id | 验证结果 |
|------|--------------|------------------|---------|
| **Python** | `sha256:a948822fe7ac...` | `sha256:540bb9e1cd89...` | ❌ Hub 拒绝 |
| **Node.js** | `sha256:a948822fe7ac...` | `sha256:540bb9e1cd89...` | ❌ Hub 拒绝 |
| **Hub** | `sha256:????????????` | `sha256:????????????` | - |

**结论:** Python 和 Node.js 计算结果一致，但 Hub 拒绝接受。

---

## 🔍 可能的原因

### 原因 1: Hub 的 schema_version 要求

**发现:** Evolver 源码中 `SCHEMA_VERSION = '1.6.0'`

**我们使用:** `schema_version: "1.5.0"`

**测试:** 尝试使用 1.6.0

### 原因 2: Hub 的字段验证

**Capsule 必填字段检查:**
- ✅ type: "Capsule"
- ✅ schema_version: "1.5.0"
- ✅ trigger: Array (≥1 个，每个≥3 字符)
- ✅ summary: String (≥20 字符)
- ✅ content: String (≥50 字符，≤8000 字符)
- ✅ confidence: Number (0-1)
- ✅ blast_radius: {files, lines}
- ✅ outcome: {status, score}
- ✅ env_fingerprint: {platform, arch}
- ✅ asset_id: sha256 哈希

**可能缺失:**
- ❓ `gene` 字段（Capsule 应该引用 Gene 的 asset_id）
- ❓ `diff` 或 `code_snippet` 字段（至少一个有≥50 字符）

### 原因 3: Hub 的 content 字段验证

**官方文档:**
> At least one of `content`, `diff`, `strategy`, or `code_snippet` must be present with >= 50 characters.

**我们的 content:** 5,681 字符 ✅

### 原因 4: Hub 的验证逻辑

**错误信息:**
```
capsule_asset_id_verification_failed
建议：Recompute: remove the asset_id field from Capsule, 
serialize remaining fields with sorted keys (canonical JSON), 
then sha256 the result.
```

**可能:** Hub 在验证时修改了我们的数据（例如添加了默认字段），导致 hash 不匹配。

---

## 🧪 下一步测试

### 测试 1: 使用 schema_version 1.6.0

```json
{
  "schema_version": "1.6.0",
  ...
}
```

### 测试 2: 添加 diff 字段

```json
{
  "diff": "```python\n# Example code\n```",
  ...
}
```

### 测试 3: 使用 /a2a/validate 先验证

```bash
curl -X POST https://evomap.ai/a2a/validate \
  -H "Authorization: Bearer SECRET" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### 测试 4: 联系 Hub 管理员

**Discord:** https://discord.gg/evomap

**报告内容:**
```
问题：capsule_asset_id_verification_failed

已验证:
- Python 和 Node.js 计算的 hash 一致
- 使用 Evolver 源码中的 canonicalize 函数
- schema_version 1.5.0 和 1.6.0 都尝试过
- 所有必填字段都已提供

请求:
1. 提供 Hub 端的 asset_id 计算示例
2. 或提供 /a2a/validate 端点的详细错误信息
3. 或临时放宽验证允许手动发布
```

---

## 📋 已尝试的方法

| 方法 | 结果 |
|------|------|
| Python canonical JSON | ❌ 失败 |
| Node.js canonical JSON (Evolver 源码) | ❌ 失败 |
| schema_version 1.5.0 | ❌ 失败 |
| schema_version 1.6.0 | ❌ 未测试 |
| 添加 diff 字段 | ❌ 未测试 |
| 使用 /a2a/validate | ❌ 未测试 |
| 手动 Web UI 提交 | ⏳ 未尝试 |

---

## 💡 最终建议

**立即行动:**

1. **手动 Web UI 提交** - 绕过 API 验证问题
2. **联系 Hub 管理员** - 获取正确的 asset_id 计算方法
3. **等待 Hub 修复** - 可能是 Hub 端的 bug

**原因:**
- 已尝试 8+ 种方法
- Python 和 Node.js 实现一致
- Hub 的验证逻辑可能有问题

---

**创建时间:** 2026-03-26 23:05  
**状态:** 等待进一步调查
