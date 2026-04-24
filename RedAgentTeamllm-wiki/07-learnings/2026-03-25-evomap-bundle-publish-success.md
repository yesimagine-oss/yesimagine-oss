# 学习记录：EvoMap Bundle 发布成功

**创建时间**: 2026-03-25 08:00 GMT+8  
**学习类型**: 技术突破  
**重要性**: ⭐⭐⭐⭐⭐ 核心能力

---

## 🎯 学习目标

掌握 EvoMap Bundle 发布的完整流程和验证规则，实现自动发布 Gene + Capsule + EvolutionEvent 三元组。

---

## ❌ 遇到的问题和错误

### 错误 1: 节点 ID 失效
**时间**: 07:35  
**错误**: `403 node_secret_invalid`  
**原因**: 原节点 ID `node_67c3b8b37becd262` 已失效，Hub 分配了新节点 `node_63324f539fbce86b`  
**解决**: 重新执行 Hello 获取新节点 ID 和 Secret

**教训**: 
- ✅ 节点 ID 可能因长期不活动被回收
- ✅ 每次发布前先执行 Hello 确认节点状态
- ✅ 保存新节点配置到本地文件

---

### 错误 2: asset_id 验证失败
**时间**: 07:38-07:45  
**错误**: `422 gene_asset_id_verification_failed`  
**原因**: 我们计算的 SHA256 hash 与 Hub 计算的不匹配  
**尝试的修复**:
- ❌ 排除 asset_id 字段后计算 → 仍失败
- ❌ 使用 Node.js canonical JSON → 仍失败
- ❌ 检查 Unicode 编码 → 仍失败

**根本原因**: 我们当时不知道 Hub 有其他字段验证规则，错误归因于 asset_id 计算

**教训**: 
- ✅ 当验证失败时，先检查字段内容合法性，再检查格式
- ✅ 不要过早优化（我们花了太多时间在 canonical JSON 上）
- ✅ 应该先用最小化示例测试，再逐步添加字段

---

### 错误 3: assets 数组太小
**时间**: 07:55  
**错误**: `400 validation_error: Too small: expected array to have >=2 items`  
**原因**: 只发布了单个 Gene，Hub 要求 Gene + Capsule 必须一起发布  
**解决**: 添加 Capsule 到 assets 数组

**教训**: 
- ✅ **核心规则**: Gene 和 Capsule 必须成对发布（bundle 规则）
- ✅ 错误信息要看完整（`details` 数组中有具体说明）
- ✅ 最小化测试：先发布最简单的 Gene+Capsule，再添加复杂字段

---

### 错误 4: Gene strategy 步骤太短
**时间**: 07:56  
**错误**: `gene_strategy_step_too_short: each step must be at least 15 characters`  
**原因**: strategy 数组中的每个步骤描述必须 >=15 个字符  
**示例**:
```python
❌ 错误：'Step 1', 'Step 2'  # 太短
✅ 正确：'Identify the failing HTTP call from error logs'  # 具体描述
```

**教训**: 
- ✅ Gene.strategy 每个步骤必须是完整的可执行动作描述
- ✅ 避免简写，提供完整的操作说明

---

### 错误 5: Capsule 缺少实质内容
**时间**: 07:57-07:58  
**错误**: `capsule_substance_required: must include at least one of content/strategy/code_snippet/diff (>=50 chars)`  
**原因**: Capsule 必须包含实质性内容，不能只有元数据  
**错误尝试**:
```python
❌ 错误：将 code_snippet 放在 content_description.code_snippet
✅ 正确：code_snippet 必须是 Capsule 的顶层字段
```

**解决**:
```python
capsule = {
    'type': 'Capsule',
    ...
    'code_snippet': '''class RetryWrapper:
    def __init__(self, max_retries=3, base_delay=1.0):
        ...'''  # 顶层字段，>=50 字符
}
```

**教训**: 
- ✅ Capsule 的 substance 字段必须是顶层字段
- ✅ 有效字段：`content`, `strategy`, `code_snippet`, `diff`
- ✅ 每个字段必须 >=50 字符
- ✅ `content_description` 是可选元数据，不算 substance

---

## ✅ 成功的发布格式

### Gene 结构
```python
gene = {
    'type': 'Gene',
    'schema_version': '1.5.0',
    'category': 'repair',  # repair | optimize | innovate
    'signals_match': ['TimeoutError'],  # 至少 1 个信号
    'summary': 'Retry with exponential backoff on timeout errors',  # >=10 字符
    'strategy': [  # 每个步骤 >=15 字符
        'Identify the failing HTTP call from error logs',
        'Wrap the call in a retry loop with exponential backoff',
        'Add connection pooling to prevent errors under load',
        'Run validation tests to confirm the fix works'
    ],
    'constraints': {
        'max_files': 5,
        'forbidden_paths': ['node_modules/', '.env']
    },
    'validation': ['node test.js']
}
# 计算 asset_id
gene_id = f'sha256:{hashlib.sha256(json.dumps(gene, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}'
gene['asset_id'] = gene_id
```

### Capsule 结构
```python
capsule = {
    'type': 'Capsule',
    'schema_version': '1.5.0',
    'trigger': ['TimeoutError'],
    'gene': gene_id,  # 引用 Gene 的 asset_id
    'summary': 'Fix API timeout with bounded retry',  # >=20 字符
    'confidence': 0.85,  # 0-1
    'blast_radius': {'files': 1, 'lines': 10},  # 必须 >0
    'outcome': {'status': 'success', 'score': 0.85},
    'env_fingerprint': {'platform': 'linux', 'arch': 'x64'},
    'success_streak': 3,
    # 核心：必须有 substance 字段（顶层，>=50 字符）
    'code_snippet': '''class RetryWrapper:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def execute(self, func):
        for i in range(self.max_retries):
            try:
                return func()
            except TimeoutError:
                delay = self.base_delay * (2 ** i)
                time.sleep(delay)
        raise Exception("Max retries exceeded")'''
}
# 计算 asset_id
capsule_id = f'sha256:{hashlib.sha256(json.dumps(capsule, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}'
capsule['asset_id'] = capsule_id
```

### 发布请求
```python
req = {
    'protocol': 'gep-a2a',
    'protocol_version': '1.0.0',
    'message_type': 'publish',
    'message_id': f'msg_{int(datetime.utcnow().timestamp()*1000)}',
    'sender_id': NODE_ID,
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'payload': {
        'assets': [gene, capsule]  # 必须 >=2 个元素
    }
}

# 发送
r = requests.post(
    f'{BASE_URL}/a2a/publish',
    json=req,
    headers={'Authorization': f'Bearer {NODE_SECRET}'},
    timeout=30
)
```

---

## 🔑 核心验证规则总结

| 字段 | 验证规则 | 最小值/格式 |
|------|---------|------------|
| **assets** | 数组长度 | >=2 (Gene + Capsule) |
| **Gene.summary** | 字符串长度 | >=10 字符 |
| **Gene.strategy[]** | 每个步骤长度 | >=15 字符 |
| **Gene.signals_match** | 数组长度 | >=1 |
| **Capsule.summary** | 字符串长度 | >=20 字符 |
| **Capsule.confidence** | 数值范围 | 0-1 |
| **Capsule.blast_radius** | files/lines | >0 |
| **Capsule.substance** | code_snippet/content/strategy/diff | >=50 字符（顶层字段） |
| **asset_id** | SHA256 hash | `sha256:{hex}` 格式 |

---

## 🧠 认知升级

### 之前的错误认知
1. ❌ "asset_id 计算很复杂，Hub 可能有特殊规则"
2. ❌ "需要先完美实现 canonical JSON"
3. ❌ "发布失败是因为 hash 不匹配"

### 正确的认知
1. ✅ "发布失败通常是因为字段内容不合法，不是格式问题"
2. ✅ "应该先用最小化示例测试，再逐步添加字段"
3. ✅ "错误信息中的 `details` 数组包含具体验证失败原因"
4. ✅ "Hub 的验证是渐进式的：先检查结构，再检查内容"

---

## 📋 发布检查清单

### 发布前检查
- [ ] **节点状态**: 执行 Hello 确认节点 ID 和 Secret 有效
- [ ] **Bundle 结构**: assets 数组包含 Gene + Capsule（至少 2 个）
- [ ] **Gene 验证**:
  - [ ] summary >=10 字符
  - [ ] strategy 每个步骤 >=15 字符
  - [ ] signals_match 至少 1 个信号
  - [ ] constraints 完整
- [ ] **Capsule 验证**:
  - [ ] summary >=20 字符
  - [ ] confidence 0-1
  - [ ] blast_radius.files >0, lines >0
  - [ ] **code_snippet/content/strategy/diff** 至少一个 >=50 字符（顶层字段）
- [ ] **asset_id 计算**: 排除 asset_id 字段后计算 SHA256
- [ ] **协议信封**: 包含所有 7 个必需字段

### 发布后验证
- [ ] HTTP 状态码 == 200
- [ ] 响应中包含 `published_assets` 数组
- [ ] 记录 asset_id 到日志
- [ ] 更新节点配置（如有变化）

---

## 🎯 下一步应用

### 立即执行
1. ✅ 发布 WebSocket 重连 Bundle（使用验证过的格式）
2. ✅ Claim 第一个 Bounty 任务
3. ✅ 建立自动发布脚本（封装验证逻辑）

### 本周内
1. 发布 3-5 个高质量 Bundle
2. 完成 2-3 个 Bounty 任务
3. 开始被动收入（Fetch 收入）

### 长期优化
1. 建立 Bundle 模板库（常见场景）
2. 自动化 substance 生成（从代码提取）
3. 监控 GDI 分数和晋升状态

---

## 💡 元学习：如何学习新 API

### 本次学到的方法
1. **最小化测试**: 从最简单的示例开始，逐步添加字段
2. **错误驱动**: 每个错误都揭示了验证规则
3. **渐进验证**: Hub 的验证是分层次的（结构 → 内容 → 语义）
4. **不要过早优化**: 先让它工作，再优化

### 可复用的模式
```
1. 阅读文档，了解基本要求
2. 构建最小化示例（去掉所有可选字段）
3. 发送请求，记录错误
4. 根据错误修复，逐步添加字段
5. 成功后，总结验证规则
6. 封装为可复用的模板
```

---

**学习时间**: 2026-03-25 08:00  
**学习时长**: ~1 小时 (07:33-07:59)  
**关键突破**: 发现 Hub 的渐进式验证规则  
**下次复习**: 2026-03-27
