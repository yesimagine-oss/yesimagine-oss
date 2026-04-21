# Claim 任务 0 任务问题分析与修复

**分析时间**: 2026-03-27 01:40 GMT+8

---

## 🔍 问题发现

### 现象对比

| 测试方式 | 结果 | 任务数 |
|---------|------|--------|
| **直接 API 测试** | ✅ 成功 | 10 个 |
| **v6 脚本运行** | ⚠️ 0 任务 | 0 个 |

### 可用任务列表

```
1. Performance bottleneck detected - 0 credits (声誉 0)
2. How to bind Discord guild... - 100 credits (声誉 0)
3. Create a case study analysis... - 243 credits (声誉 50)
4. How to integrate AI tools... - 114 credits (声誉 30)
5. What are the latest trends... - 237 credits (声誉 30)
...
```

---

## 🐛 问题原因分析

### 可能原因 1: Bounty 筛选过严

**v6 脚本筛选条件**:
```python
MIN_BOUNTY = 100  # 最低 100 credits
```

**实际任务**:
- 任务 1: 0 credits ❌
- 任务 2: 100 credits ✅
- 任务 3: 243 credits ✅
- 任务 4: 114 credits ✅
- 任务 5: 237 credits ✅

**分析**: 应该有 4 个任务符合，不是 0 个

### 可能原因 2: 声誉筛选

**v6 脚本**:
```python
if task.get('min_reputation', 0) > OUR_REPUTATION:
    return False, f"声誉要求过高 ({min_rep} > {OUR_REPUTATION})"
```

**当前声誉**: 62.86

**分析**: 所有任务声誉要求都低于 62.86，应该都符合

### 可能原因 3: 任务已 Claim 检查

**v6 脚本**:
```python
if is_already_claimed(task):
    return False, "已 Claim 过此任务"
```

**分析**: 可能所有任务都被标记为已 Claim

### 可能原因 4: Heatmap 匹配

**v6 脚本**:
```python
# Heatmap 驱动筛选
if not matches_heatmap(task):
    return False, "不匹配 Heatmap 机会"
```

**分析**: Heatmap 可能没有匹配的任务

### 可能原因 5: API 响应解析错误

**v6 脚本**:
```python
tasks = result.get('tasks', [])
```

**分析**: 可能解析失败，tasks 为空列表

---

## 🔧 修复方案

### 修复 1: 降低筛选门槛

```python
# 修改前
MIN_BOUNTY = 100

# 修改后
MIN_BOUNTY = 50  # 降低到 50 credits
```

### 修复 2: 添加调试日志

```python
# 在获取任务后添加
logger.info(f"获取到 {len(tasks)} 个任务")
for task in tasks:
    logger.info(f"  - {task.get('title', 'N/A')[:50]}...")
    logger.info(f"    Bounty: {task.get('bounty_amount', 0)}")
    logger.info(f"    声誉：{task.get('min_reputation', 0)}")
```

### 修复 3: 检查 Heatmap 匹配逻辑

```python
def matches_heatmap(task):
    """检查任务是否匹配 Heatmap 机会"""
    
    # 获取 Heatmap 数据
    heatmap_data = load_heatmap()
    
    # 检查任务信号是否匹配
    task_signals = task.get('signals', '').split(',')
    
    for signal in task_signals:
        if signal in heatmap_data['opportunities']:
            return True
    
    return False  # ← 可能这里返回 False
```

### 修复 4: 简化筛选逻辑（临时方案）

```python
# 临时简化，先确保能 Claim 到任务
def should_claim_task_simple(task):
    """简化版筛选"""
    
    # 只检查基本条件
    if task.get('bounty_amount', 0) < 50:
        return False, "Bounty 过低"
    
    if task.get('min_reputation', 0) > 70:
        return False, "声誉要求过高"
    
    # 不检查 Heatmap 匹配
    return True, "符合条件"
```

---

## 📝 立即修复

让我创建一个修复版本：

```python
# auto-claim-task-v7.py

# 修复 1: 降低门槛
MIN_BOUNTY = 50  # 从 100 降到 50

# 修复 2: 添加详细日志
logger.info(f"获取到 {len(tasks)} 个原始任务")
for i, task in enumerate(tasks):
    logger.info(f"  [{i+1}] {task.get('title', 'N/A')[:50]}...")
    logger.info(f"      Bounty: {task.get('bounty_amount', 0)}")
    logger.info(f"      声誉：{task.get('min_reputation', 0)}")

# 修复 3: 简化 Heatmap 匹配
def matches_heatmap(task):
    """简化匹配逻辑"""
    # 暂时返回 True，确保不过滤掉任务
    return True

# 修复 4: 添加失败原因统计
filter_stats = {
    'bounty_too_low': 0,
    'reputation_too_high': 0,
    'already_claimed': 0,
    'heatmap_mismatch': 0,
    'quality_too_low': 0
}
```

---

## 🎯 测试计划

### 测试 1: 直接运行修复版

```bash
cd /home/admin/.openclaw/workspace/ai知识变现/evomap项目
python3 scripts/auto-claim-task-v7.py
```

**预期**:
- 获取到 10 个任务
- 筛选出 4-6 个可 Claim 任务
- Claim 1-2 个任务

### 测试 2: 手动 Claim 测试

```python
# 手动 Claim 一个任务
import requests

task_id = 'cmded50754937e4efe7015c34'  # 任务 3

response = requests.post(
    'https://evomap.ai/a2a/task/claim',
    json={'task_id': task_id, 'node_id': 'node_67c3b8b37becd262'},
    headers={'Authorization': 'Bearer bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'}
)

print(response.json())
```

### 测试 3: 完整流程测试

1. Claim 任务
2. 完成任务（真实执行）
3. 提交任务
4. 验证结果

---

## 📊 预期结果

**修复后**:
- ✅ 获取到 10 个任务
- ✅ 筛选出 4-6 个可 Claim 任务
- ✅ Claim 1-2 个任务
- ✅ 完成任务并提交
- ✅ 获得 credits 和声誉

**时间表**:
- 01:45 - 创建 v7 版本
- 01:50 - 测试 v7 版本
- 02:00 - 手动 Claim 测试
- 02:30 - 完整流程测试

---

**分析者**: RedOpenClaw  
**分析时间**: 2026-03-27 01:40 GMT+8  
**状态**: 🔧 准备修复
