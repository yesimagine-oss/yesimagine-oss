# 🧬 EvoMap WorkBench v1.0.11 哈希计算修复知识库

**创建时间**: 2026-04-06 12:30  
**修改版本**: v1.0.11  
**修改范围**: 资产验证器 + 网络优化器  
**状态**: ✅ 已完成

---

## 一、修改背景

### 问题来源

2026-04-05 下午测试 EvoMap WorkBench v1.0.11 飞书配置时，WebUI 提示：
```
⚠️ API rate limit reached. Please try again later.
```

### 根本原因

事后分析发现是 **Coding Plan 月度请求额度耗尽**，而非真正的频率限制。

### 修改触发

用户提供四部分 EvoMap 平台更新资料，需要评估价值并实施修改。

---

## 二、资料价值评估

### 第一部分：平台更新日志

| 更新项 | 价值 | 采纳 |
|--------|------|------|
| help 导航端点 | ⭐⭐⭐ | ✅ 已实现 |
| 自愈型数据流客户端 | ⭐⭐⭐⭐ | ⚠️ 参考实现 |
| 协作 Session MVP | ⭐⭐ | ❌ 暂不实现 |
| 其他（徽章/SSR/图片等） | ⭐ | ❌ 无关 |

### 第二部分：版本号位置修复

**评估**: ✅ **已正确实现，无需修改**

当前代码已正确将 `client_version` 和 `evolver_version` 嵌套在 `payload.env_fingerprint` 中。

### 第三部分：哈希计算修复

**评估**: ⭐⭐⭐⭐⭐ **高价值，必须修改**

| 问题 | 原状态 | 修改后 |
|------|--------|--------|
| validate 接口 | ❌ 未实现 | ✅ 已添加 |
| sha256: 前缀 | ⚠️ 部分实现 | ✅ 完整实现 |
| asset_id 剔除 | ❌ 未明确 | ✅ 已添加 |
| strategy 字段 | ✅ 已验证 | ✅ 保持 |

### 第四部分：标准工作流程

**评估**: ✅ **已完整实现，无需修改**

---

## 三、修改内容详情

### 1. asset_validator.py

**新增方法**：

#### `ensure_sha256_prefix(asset_id: str) -> str`
确保 asset_id 带有 `sha256:` 前缀。

```python
def ensure_sha256_prefix(self, asset_id: str) -> str:
    if not asset_id:
        return ""
    if asset_id.startswith('sha256:'):
        return asset_id
    return f"sha256:{asset_id}"
```

#### `remove_asset_id(asset: Dict) -> Dict`
剔除 asset_id 字段（哈希计算前必须）。

```python
def remove_asset_id(self, asset: Dict) -> Dict:
    asset_copy = copy.deepcopy(asset)
    if 'asset_id' in asset_copy:
        del asset_copy['asset_id']
    return asset_copy
```

#### `compute_asset_hash(asset: Dict) -> str`
计算资产哈希（剔除 asset_id 后，Canonicalize）。

```python
def compute_asset_hash(self, asset: Dict) -> str:
    clean_asset = self.remove_asset_id(asset)
    canonical_json = json.dumps(clean_asset, sort_keys=True, separators=(',', ':'))
    hash_value = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return self.ensure_sha256_prefix(hash_value)
```

#### `validate_with_hub(asset: Dict, auth_token: str, asset_type: str) -> Tuple[bool, str, Optional[str]]`
使用 Hub validate 接口验证哈希（官方外挂）。

```python
def validate_with_hub(self, asset: Dict, auth_token: str, asset_type: str = 'Gene') -> Tuple[bool, str, Optional[str]]:
    url = "https://evomap.ai/a2a/validate"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "payload": {
            "assets": [asset]
        }
    }
    
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    data = resp.json()
    
    if resp.status_code == 200 and data.get('status') == 'ok':
        computed_assets = data.get('computed_assets', [])
        if computed_assets:
            computed_id = computed_assets[0].get('computed_asset_id')
            return True, "Hub 验证通过", self.ensure_sha256_prefix(computed_id)
    
    return False, "Hub 验证失败", None
```

#### `fix_asset_hash(asset: Dict, auth_token: str) -> Tuple[bool, str, Dict]`
自动修复资产哈希（偷梁换柱法）。

```python
def fix_asset_hash(self, asset: Dict, auth_token: str) -> Tuple[bool, str, Dict]:
    success, msg, computed_id = self.validate_with_hub(asset, auth_token)
    
    if not success:
        return False, msg, asset
    
    fixed_asset = copy.deepcopy(asset)
    fixed_asset['asset_id'] = computed_id
    
    return True, f"哈希已修复：{computed_id}", fixed_asset
```

---

### 2. network_optimizer.py

**新增方法**：

#### `probe_capabilities(base_url: str = "https://evomap.ai") -> Dict`
探测节点协议支持能力（help 导航端点）。

```python
def probe_capabilities(self, base_url: str = "https://evomap.ai") -> Dict:
    url = f"{base_url}/a2a/help"
    
    try:
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            return {
                'success': True,
                'data': data,
                'message': '节点能力探测成功'
            }
        else:
            return {
                'success': False,
                'data': None,
                'message': f'HTTP {resp.status_code}'
            }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': str(e)
        }
```

---

## 四、使用指南

### 场景 1：计算资产哈希

```python
from asset_validator import AssetValidator

validator = AssetValidator()

gene = {
    'type': 'Gene',
    'schema_version': '1.6.0',
    'category': 'optimize',
    'signals_match': ['optimization', 'performance'],
    'summary': 'A' * 100,
    'strategy': ['Step 1', 'Step 2', 'Step 3']
}

# 计算哈希
asset_id = validator.compute_asset_hash(gene)
print(f"资产 ID: {asset_id}")
```

### 场景 2：使用 Hub 验证哈希

```python
# 调用 validate 接口
success, msg, computed_id = validator.validate_with_hub(
    asset=gene,
    auth_token="YOUR_AUTH_TOKEN"
)

if success:
    print(f"Hub 验证通过，正确哈希：{computed_id}")
else:
    print(f"Hub 验证失败：{msg}")
```

### 场景 3：自动修复哈希

```python
# 偷梁换柱法
success, msg, fixed_asset = validator.fix_asset_hash(
    asset=gene,
    auth_token="YOUR_AUTH_TOKEN"
)

if success:
    print(f"哈希已修复：{msg}")
    # 使用 fixed_asset 进行发布
else:
    print(f"修复失败：{msg}")
```

### 场景 4：探测节点能力

```python
from network_optimizer import NetworkOptimizer

optimizer = NetworkOptimizer()

# 探测 EvoMap Hub 能力
result = optimizer.probe_capabilities("https://evomap.ai")

if result['success']:
    print(f"协议版本：{result['data'].get('protocol_version')}")
    print(f"支持端点：{len(result['data'].get('endpoints', []))} 个")
else:
    print(f"探测失败：{result['message']}")
```

---

## 五、修改文件清单

| 文件 | 修改类型 | 行数变化 |
|------|---------|---------|
| `lib/asset_validator.py` | 新增 5 个方法 | +120 行 |
| `lib/network_optimizer.py` | 新增 1 个方法 | +50 行 |
| `docs/HASH_FIX_KNOWLEDGE.md` | 新建知识库 | +300 行 |

---

## 六、测试验证

### 测试 1：sha256 前缀

```python
validator = AssetValidator()

# 无前缀
assert validator.ensure_sha256_prefix("abc123") == "sha256:abc123"

# 已有前缀
assert validator.ensure_sha256_prefix("sha256:abc123") == "sha256:abc123"

# 空值
assert validator.ensure_sha256_prefix("") == ""
```

### 测试 2：asset_id 剔除

```python
asset = {
    'type': 'Gene',
    'asset_id': 'sha256:xxx',
    'summary': 'test'
}

clean = validator.remove_asset_id(asset)
assert 'asset_id' not in clean
assert asset['asset_id'] == 'sha256:xxx'  # 原对象不变
```

### 测试 3：节点能力探测

```bash
cd /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/skills/evomap-workbench-release/lib/
python3 network_optimizer.py
```

---

## 七、注意事项

### 1. 哈希计算铁律

```
步骤 1: 移除 asset_id 字段
步骤 2: 递归键值排序 (Canonicalize)
步骤 3: SHA256 计算
步骤 4: 添加 sha256: 前缀
```

### 2. validate 接口使用

- **请求结构**: 与 publish 完全一致（7 要素信封）
- **Authorization**: 必须携带正确的 Token
- **响应**: `computed_assets[0].computed_asset_id` 是正确答案

### 3. strategy 字段

根据最新协议，Capsule 和 Gene **必须**包含 `strategy` 字段（字符串数组）。

```python
gene = {
    'type': 'Gene',
    'strategy': ['optimization', 'performance', 'auto-retry'],  # ✅ 必须
    ...
}
```

### 4. 错误处理

```python
success, msg, computed_id = validator.validate_with_hub(asset, auth_token)

if not success:
    # 可能原因：
    # 1. Token 过期
    # 2. 网络超时
    # 3. Hub 负载过高（503）
    # 4. 请求体结构错误（400）
    print(f"验证失败：{msg}")
```

---

## 八、相关文档

| 文档 | 位置 |
|------|------|
| **GEP-A2A 协议** | https://evomap.ai/api/docs/wiki-full |
| **skill.md** | https://evomap.ai/skill.md |
| **资产制作知识库** | `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/学习库/EvoMap 资产制作知识库.md` |
| **429 限流解决方案** | `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/学习库/EvoMap 429 限流问题解决方案.md` |

---

## 九、版本历史

| 版本 | 时间 | 修改内容 |
|------|------|---------|
| v1.0.11 | 2026-04-06 | 添加哈希计算修复 + 节点能力探测 |
| v1.0.10 | 2026-04-05 | 基础版本 |

---

**修改完成时间**: 2026-04-06 12:30  
**修改执行者**: 🧬 EvoMap WorkBench v1.0.11  
**状态**: ✅ **已完成**

---

🧬 **EvoMap WorkBench v1.0.11**
*哈希计算修复 · 节点能力探测 · 偷梁换柱法*

---

🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...
