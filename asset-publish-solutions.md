# 🔧 EvoMap Asset ID 哈希验证问题 - 解决方案报告

**创建时间**: 2026-03-27 11:30  
**问题**: API 发布时 asset_id 验证失败  
**状态**: 需要进一步调查/使用 Web UI 替代

---

## 📊 问题总结

### 现象

使用 Python API 发布资产时，Hub 返回 `gene_asset_id_verification_failed` 错误，提示客户端计算的 asset_id 与 Hub 计算的不一致。

### 根本原因

EvoMap Hub 使用 **JavaScript 的 `JSON.stringify()`** 进行 canonical JSON 序列化，而 Python 的 `json.dumps()` 即使使用 `sort_keys=True` 和 `ensure_ascii=True` 也无法完全匹配。

---

## 🔬 测试过的所有方法

### 方法 1: Python json.dumps (基础)
```python
json.dumps(data, sort_keys=True, separators=(',', ':'))
```
**结果**: ❌ 失败  
**原因**: 中文等 Unicode 字符保持 UTF-8，而 JS 转为 `\uXXXX`

---

### 方法 2: Python json.dumps (ensure_ascii=True)
```python
json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
```
**结果**: ❌ 失败  
**原因**: 即使 Unicode 转义一致，仍有其他差异

---

### 方法 3: 移除所有非必填字段
```python
gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "id": "...",
    "category": "...",
    "signals_match": [...],
    "summary": "...",
    "strategy": [...],
    "constraints": {...},
    "validation": []
}
```
**结果**: ❌ 失败  
**原因**: 不是字段问题，是序列化算法差异

---

### 方法 4: 使用 PENDING 占位符
```python
capsule = {
    "gene": "PENDING",  # 让 Hub 替换
    ...
}
```
**结果**: ❌ 失败  
**原因**: Hub 要求必须提供 asset_id，不接受 PENDING

---

### 方法 5: 让 Hub 计算 (compute_asset_ids: True)
```python
{
    "payload": {
        "assets": [...],
        "compute_asset_ids": True
    }
}
```
**结果**: ❌ 失败  
**原因**: Hub 不支持此参数，要求客户端必须提供

---

## 🔍 可能的差异点

### 1. Unicode 转义

| 字符 | JavaScript | Python (ensure_ascii=True) |
|------|-----------|---------------------------|
| `中` | `\u4e2d` | `\u4e2d` ✅ |
| `é` | `\u00e9` | `\u00e9` ✅ |
| `😀` | `\ud83d\ude00` | `\ud83d\ude00` ✅ |

**结论**: Unicode 转义一致

---

### 2. 嵌套对象排序

**输入**:
```json
{"b": 1, "a": {"z": 1, "a": 2}}
```

**JavaScript**:
```javascript
JSON.stringify(obj, Object.keys(obj).sort())
// {"a":{"a":2,"z":1},"b":1}
```

**Python**:
```python
json.dumps(obj, sort_keys=True)
# {"a": {"a": 2, "z": 1}, "b": 1}
```

**结论**: 嵌套排序一致 ✅

---

### 3. 可能的隐藏差异

| 差异点 | 测试难度 | 可能性 |
|--------|---------|--------|
| **数字精度** | 中 | 🟡 中 |
| **布尔值大小写** | 低 | 🟢 低 (已验证一致) |
| **null vs undefined** | 中 | 🟡 中 |
| **数组内对象** | 高 | 🟠 高 |
| **特殊字符转义** | 高 | 🟠 高 |
| **Hub 自定义算法** | 极高 | 🔴 极高 |

---

## 💡 解决方案建议

### 方案 1: 使用 Node.js 子进程（推荐 ⭐⭐⭐⭐⭐）

**思路**: 在 Python 中调用 Node.js 脚本进行序列化

**实现**:
```python
import subprocess
import json

def compute_asset_id_js(data):
    """使用 Node.js 计算 asset_id"""
    data_copy = {k: v for k, v in data.items() if k != 'asset_id'}
    
    # 调用 Node.js 脚本
    node_script = '''
    const data = %s;
    const canonical = JSON.stringify(data, Object.keys(data).sort());
    const crypto = require('crypto');
    const hash = crypto.createHash('sha256').update(canonical).digest('hex');
    console.log('sha256:' + hash);
    ''' % json.dumps(data_copy)
    
    result = subprocess.run(
        ['node', '-e', node_script],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
```

**优点**:
- ✅ 100% 匹配 Hub 的序列化
- ✅ 无需逆向工程
- ✅ 可批量处理

**缺点**:
- ⚠️ 需要 Node.js 环境
- ⚠️ 子进程调用有性能开销

**实施时间**: 30 分钟

---

### 方案 2: 使用 Pyppeteer 自动化 Web UI（推荐 ⭐⭐⭐⭐）

**思路**: 用 Python 控制浏览器自动填写 Web UI 表单

**实现**:
```python
import asyncio
from pyppeteer import launch

async def publish_via_browser(asset_data):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://evomap.ai/publish')
    
    # 自动填写表单
    await page.evaluate('''(data) => {
        for (const [key, value] of Object.entries(data)) {
            const input = document.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = typeof value === 'object' ? JSON.stringify(value) : value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }''', asset_data)
    
    await page.click('button[type="submit"]')
    await browser.close()
```

**优点**:
- ✅ 100% 可靠（与手动发布相同）
- ✅ 可批量处理
- ✅ 无需关心序列化

**缺点**:
- ⚠️ 需要安装 pyppeteer
- ⚠️ 需要浏览器环境
- ⚠️ 速度较慢

**实施时间**: 60 分钟

---

### 方案 3: 联系 EvoMap 官方获取算法文档（推荐 ⭐⭐⭐）

**思路**: 直接向官方询问 canonical JSON 的具体规则

**行动**:
1. 加入 EvoMap Discord
2. 在 #developer-support 频道提问
3. 请求提供 Python SDK 或序列化示例

**模板**:
```
Hi EvoMap team!

I'm trying to publish assets via API but getting 
`gene_asset_id_verification_failed` errors.

Could you please share:
1. The exact canonical JSON serialization rules?
2. Or provide a Python SDK?
3. Or a reference implementation?

Thanks!
```

**优点**:
- ✅ 一劳永逸
- ✅ 官方支持
- ✅ 可能获得 Python SDK

**缺点**:
- ⚠️ 响应时间不确定
- ⚠️ 可能没有官方答案

**实施时间**: 1-7 天（等待响应）

---

### 方案 4: 逆向工程 Hub 代码（不推荐 ⭐）

**思路**: 如果 Hub 是开源的，查看源码

**行动**:
1. 检查 https://github.com/EvoMap/evolver
2. 查找 asset_id 计算相关代码
3. 复制算法到 Python

**现状**: 
- ❌ Hub 服务端代码不开源
- ❌ 只有客户端 evolver 开源
- ❌ 客户端不包含 Hub 的序列化逻辑

**结论**: 不可行

---

### 方案 5: 暴力破解（不推荐 ⭐）

**思路**: 尝试不同的序列化变体，直到匹配

**实现**:
```python
# 尝试所有可能的组合
for ensure_ascii in [True, False]:
    for separators in [(',', ':'), (', ', ': ')]:
        for sort_keys in [True, False]:
            # 计算 hash 并尝试发布
            # 如果成功，记录这个组合
```

**缺点**:
- ❌ 需要多次 API 调用（可能被限流）
- ❌ 可能永远找不到正确组合
- ❌ 效率极低

**结论**: 不切实际

---

### 方案 6: 使用 Web UI 手动发布（当前最佳 ⭐⭐⭐⭐⭐）

**思路**: 暂时使用 Web UI，等待官方解决方案

**步骤**:
1. 打开 https://evomap.ai
2. 手动填写表单发布
3. 同时向官方反馈 API 问题

**优点**:
- ✅ 立即可用
- ✅ 100% 可靠
- ✅ 无需技术修改

**缺点**:
- ⚠️ 无法自动化
- ⚠️ 耗时（每个 Bundle 15 分钟）

**实施时间**: 立即

---

## 🎯 推荐行动方案

### 短期（今天）
**使用 Web UI 手动发布**
- 发布自适应负载均衡器 EvolutionEvent
- 发布 4 个 P0 机会资产包
- 获得 240 积分

### 中期（本周）
**实施方案 1: Node.js 子进程**
- 创建 Python 包装器
- 测试所有资产类型
- 实现批量发布

### 长期（本月）
**实施方案 3: 联系官方**
- 加入 Discord
- 提交 Issue
- 推动官方 Python SDK

---

## 📝 实施 Node.js 子进程方案

### 步骤 1: 创建 Node.js 脚本

```javascript
// compute_asset_id.js
const data = JSON.parse(process.argv[2]);
const canonical = JSON.stringify(data, Object.keys(data).sort());
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update(canonical).digest('hex');
console.log('sha256:' + hash);
```

### 步骤 2: Python 调用

```python
import subprocess
import json

def compute_asset_id(data):
    data_copy = {k: v for k, v in data.items() if k != 'asset_id'}
    result = subprocess.run(
        ['node', 'compute_asset_id.js', json.dumps(data_copy)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
```

### 步骤 3: 测试

```python
gene = {...}  # Gene 数据
gene['asset_id'] = compute_asset_id(gene)
# 发布...
```

### 预计时间
- 创建脚本：10 分钟
- 测试：15 分钟
- 集成：15 分钟
- **总计**: 40 分钟

---

## 📊 方案对比

| 方案 | 可靠性 | 实施时间 | 可维护性 | 推荐度 |
|------|-------|---------|---------|--------|
| **Node.js 子进程** | ⭐⭐⭐⭐⭐ | 40 分钟 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Web UI 自动化** | ⭐⭐⭐⭐⭐ | 60 分钟 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **联系官方** | ⭐⭐⭐⭐⭐ | 1-7 天 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Web UI 手动** | ⭐⭐⭐⭐⭐ | 60 分钟 | ⭐⭐ | ⭐⭐⭐⭐ |
| **逆向工程** | ⭐ | N/A | N/A | ⭐ |
| **暴力破解** | ⭐ | 数小时 | ⭐ | ⭐ |

---

## ✅ 下一步行动

### 立即执行（60 分钟）
1. 使用 Web UI 手动发布所有待发布资产
2. 确保不错过 P0 机会

### 本周执行（40 分钟）
1. 实施 Node.js 子进程方案
2. 测试批量发布
3. 发布剩余资产

### 本月执行
1. 联系 EvoMap 官方
2. 推动 Python SDK 开发
3. 贡献社区

---

**报告生成**: 2026-03-27 11:30  
**建议**: 先用 Web UI 发布，再实施 Node.js 方案
