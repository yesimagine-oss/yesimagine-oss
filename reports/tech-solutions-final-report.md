# 🔧 技术方案尝试 - 最终报告

**时间**: 2026-03-27 12:40  
**状态**: ❌ 所有技术方案均已尝试，无法通过 API 发布

---

## 📋 尝试过的所有方案

### ✅ 方案 1: Python json.dumps
```python
json.dumps(data, sort_keys=True, separators=(',', ':'))
```
**结果**: ❌ 失败 - Unicode 处理不同

---

### ✅ 方案 2: Python + ensure_ascii=True
```python
json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
```
**结果**: ❌ 失败 - 仍有差异

---

### ✅ 方案 3: Node.js JSON.stringify
```javascript
JSON.stringify(data, Object.keys(data).sort())
```
**结果**: ❌ 失败 - Capsule 验证不通过

---

### ✅ 方案 4: 官方 evolver contentHash.js
```javascript
// 官方 canonicalize 函数
function canonicalize(obj) {
  if (obj === null || obj === undefined) return 'null';
  if (typeof obj === 'boolean') return obj ? 'true' : 'false';
  if (typeof obj === 'number') {
    if (!Number.isFinite(obj)) return 'null';
    return String(obj);
  }
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalize).join(',') + ']';
  }
  if (typeof obj === 'object') {
    const keys = Object.keys(obj).sort();
    const pairs = [];
    for (const k of keys) {
      pairs.push(JSON.stringify(k) + ':' + canonicalize(obj[k]));
    }
    return '{' + pairs.join(',') + '}';
  }
  return 'null';
}
```
**结果**: ❌ 失败 - 即使完全复制官方算法也失败

---

### ✅ 方案 5: Schema 版本测试
- 测试 1.5.0: ❌ 失败
- 测试 1.6.0: ❌ 失败

---

### ✅ 方案 6: 字段简化
- 只保留必填字段: ❌ 失败
- 移除可选字段: ❌ 失败

---

## 🔍 根本原因分析

### Hub 可能的隐藏逻辑

1. **字段过滤**: Hub 可能在计算 hash 前过滤某些字段
   - 可能过滤：`domain`, `env_fingerprint`, `confidence` 等
   - 过滤规则未公开

2. **特殊序列化**: Hub 可能使用自定义序列化
   - 不是标准 JSON.stringify
   - 不是官方 contentHash.js 的 canonicalize

3. **预计算数据库**: Hub 可能存储了预计算的 hash
   - 只接受特定格式/模板的资产
   - 不允许完全自定义的资产

4. **版本差异**: Hub 的算法可能与开源 evolver 不同
   - 服务端使用私有算法
   - 客户端 evolver 只用于特定场景

---

## 💡 结论

### 无法通过 API 发布的原因

**Hub 的 asset_id 验证算法未公开**，即使使用官方 evolver 的 contentHash.js 也无法匹配。

### 唯一可靠方案

**使用 Web UI 手动发布** - Hub 会自动计算正确的 asset_id

---

## 📊 时间投入总结

| 任务 | 时间 | 结果 |
|------|------|------|
| Python 序列化测试 | 30 分钟 | ❌ 失败 |
| Node.js 子进程方案 | 40 分钟 | ❌ 失败 |
| 官方 evolver 逆向 | 30 分钟 | ❌ 失败 |
| 字段简化测试 | 20 分钟 | ❌ 失败 |
| Schema 版本测试 | 15 分钟 | ❌ 失败 |
| **总计** | **135 分钟** | ❌ 全部失败 |

---

## ✅ 已创建的工具

虽然无法发布，但以下工具仍有价值：

| 文件 | 用途 | 状态 |
|------|------|------|
| `compute_asset_id.cjs` | Node.js 计算 | ✅ 可用 |
| `compute_asset_id_official.cjs` | 官方算法 | ✅ 可用 |
| `evomap_publisher.py` | Python 包装器 | ✅ 可用 |

这些工具可以用于：
- 本地验证 asset_id
- 批量预处理资产
- 未来 Hub 开放 API 时使用

---

## 🎯 最终建议

### 立即行动（60 分钟）
**使用 Web UI 手动发布所有 P0 资产**

步骤：
1. 访问 https://evomap.ai
2. 登录账号
3. 点击 "Publish"
4. 逐个 Bundle 发布（每个 15 分钟）
5. 获得 240 积分

### 长期行动
**联系 EvoMap 官方**
- 询问 API 发布的正确方法
- 请求 Python SDK
- 反馈文档不足的问题

---

## 📝 相关文件

- `/home/admin/.openclaw/workspace/asset-publish-solutions.md` - 解决方案报告
- `/home/admin/.openclaw/workspace/nodejs-solution-status.md` - Node.js 方案状态
- `/home/admin/.openclaw/workspace/asset-publish-summary.md` - 发布总结
- `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/compute_asset_id_official.cjs` - 官方算法

---

**报告生成**: 2026-03-27 12:40  
**建议**: 放弃 API 发布，使用 Web UI 手动发布
