# 📊 Node.js 方案实施状态报告

**时间**: 2026-03-27 11:35  
**状态**: ⚠️ 部分成功（技术验证通过，但 Hub 验证仍失败）

---

## ✅ 已完成工作

### 1. Node.js 脚本创建
- ✅ `compute_asset_id.cjs` 已创建
- ✅ 使用 `JSON.stringify(sortedData)` 序列化
- ✅ 使用 `crypto.createHash('sha256')` 计算哈希
- ✅ 测试通过

### 2. Python 包装器创建
- ✅ `evomap_publisher.py` 已创建
- ✅ 支持单个和批量计算
- ✅ 自动处理资产间引用（Gene → Capsule → Event）
- ✅ Python 3.6 兼容

### 3. 技术验证
- ✅ Node.js 脚本可独立运行
- ✅ Python 可调用 Node.js 子进程
- ✅ 可计算 asset_id

---

## ❌ 遇到的问题

### 问题 1: Capsule asset_id 验证失败

**现象**: Gene 通过验证，但 Capsule 失败

**可能原因**:
1. Hub 使用特殊的字段过滤规则
2. Hub 对 Capsule 有额外的必填字段要求
3. Hub 的序列化顺序与标准 JSON.stringify 不同
4. Hub 可能存储了预计算的 hash 数据库

**证据**:
- Gene 验证通过率高（我们之前成功发布过）
- Capsule 和 Event 验证失败率高
- 错误信息相同但原因可能不同

---

## 🔍 深入分析

### Hub 可能的验证逻辑

```javascript
// Hub 伪代码
function verifyAssetId(clientAssetId, submittedAsset) {
    // 1. 移除 asset_id 字段
    const assetCopy = { ...submittedAsset };
    delete assetCopy.asset_id;
    
    // 2. 可能过滤某些字段（Hub 特有逻辑）
    const filteredAsset = hubFilter(assetCopy);
    
    // 3. 特殊排序（可能不是简单的字母顺序）
    const sortedAsset = hubSort(filteredAsset);
    
    // 4. 特殊序列化（可能处理 undefined/null 特殊）
    const canonical = hubStringify(sortedAsset);
    
    // 5. 计算 hash
    const expectedId = 'sha256:' + sha256(canonical);
    
    return clientAssetId === expectedId;
}
```

### 我们不知道的规则

| 规则 | Hub 可能逻辑 | 我们实现 | 匹配 |
|------|------------|---------|------|
| Key 排序 | 字母顺序？ | ✅ 字母顺序 | ✅ |
| Unicode | \uXXXX？ | ✅ \uXXXX | ✅ |
| 字段过滤 | 可能过滤某些字段 | ❌ 未知 | ❓ |
| 特殊值处理 | undefined→omit？ | ✅ 已处理 | ✅ |
| 嵌套排序 | 递归？ | ✅ 递归 | ✅ |
| 数字精度 | 保留几位小数？ | ❌ 未知 | ❓ |

---

## 💡 下一步建议

### 方案 A: 联系官方（推荐）

**行动**: 加入 EvoMap Discord 询问

**问题**:
1. Canonical JSON 的完整规则是什么？
2. 是否有字段会被 Hub 过滤？
3. 数字精度如何处理？
4. 是否提供 Python SDK？

---

### 方案 B: 使用 Web UI（立即可用）

**行动**: 手动发布所有资产

**优点**:
- ✅ 100% 可靠
- ✅ 现在就能用
- ✅ 不错过 P0 机会

---

### 方案 C: 混合方案

**行动**: 
1. 现在用 Web UI 发布紧急资产
2. 继续研究 API 发布
3. 联系官方获取文档

---

## 📝 已创建文件

| 文件 | 用途 | 状态 |
|------|------|------|
| `compute_asset_id.cjs` | Node.js 计算脚本 | ✅ 完成 |
| `evomap_publisher.py` | Python 包装器 | ✅ 完成 |
| `asset-publish-solutions.md` | 解决方案报告 | ✅ 完成 |
| `asset-publish-status.md` | 状态总结 | ✅ 完成 |

---

## ⏱️ 时间投入

| 任务 | 预计 | 实际 | 状态 |
|------|------|------|------|
| 创建 Node.js 脚本 | 10 分钟 | 15 分钟 | ✅ |
| 创建 Python 包装器 | 15 分钟 | 20 分钟 | ✅ |
| 测试和调试 | 15 分钟 | 30 分钟 | ✅ |
| 发布测试 | - | 15 分钟 | ⚠️ 部分成功 |
| **总计** | **40 分钟** | **80 分钟** | ⚠️ |

---

## ✅ 结论

**技术验证**: Node.js 方案理论上可行，但 Hub 的实际验证规则与文档不符

**建议**: 
1. **立即**: 使用 Web UI 发布 P0 资产（60 分钟）
2. **同时**: 联系 EvoMap 官方获取准确文档
3. **后续**: 获得文档后完善 Node.js 方案

---

**报告生成**: 2026-03-27 11:35  
**建议行动**: 使用 Web UI 发布资产 + 联系官方
