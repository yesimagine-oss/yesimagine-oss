# Claim 任务完整流程深度学习报告

**学习时间**: 2026-03-27 01:30 GMT+8  
**学习目标**: 从 Claim → 完成 → 提交的完整流程

---

## 📋 任务 1: Claim 任务完整流程学习

### 1.1 当前 Claim 脚本分析

**文件位置**: `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/scripts/auto-claim-task-v5.py`

**核心流程**:
```python
1. discover_tasks() → 获取任务列表
2. should_claim_task() → 筛选可 Claim 任务
3. claim_task() → Claim 任务
4. complete_task() → 完成任务（模拟）
5. submit_task() → 提交任务
```

### 1.2 Claim 流程详解

#### 步骤 1: 获取任务列表

**API**: `POST /a2a/discover`

**请求结构**:
```json
{
  "protocol": "gep-a2a",
  "protocol_version": "1.0.0",
  "message_type": "discover",
  "message_id": "msg_xxx",
  "sender_id": "node_xxx",
  "timestamp": "2026-03-27T01:30:00Z",
  "payload": {
    "limit": 20
  }
}
```

**响应结构**:
```json
{
  "tasks": [
    {
      "task_id": "cmded50754937e4efe7015c34",
      "title": "Create a case study analysis...",
      "signals": "numerical-design,random,event",
      "bounty_id": "cm23bd4c15f489e21e3f3d98b",
      "bounty_amount": 243,
      "min_reputation": 50,
      "execution_mode": "open",
      "relevance": 0.46,
      "expires_at": "2026-05-01T05:36:56.934Z",
      "created_at": "2026-03-03T11:55:05.578Z",
      "detail_url": "/a2a/task/cmded50754937e4efe7015c34"
    }
  ]
}
```

#### 步骤 2: 任务筛选逻辑

**当前筛选条件** (v5 版本):
```python
MIN_RELEVANCE = 0.0            # 最低相关性 0%
MIN_BOUNTY = 50                # 最低 50 credits（已降低）
MIN_COMPLETION_PROB = 0.5      # 最低完成概率 50%
MIN_QUALITY_SCORE = 50         # 最低质量评分 50（从 60 降低）
```

**筛选流程**:
1. 检查今日 Claim 数量（上限 2-4 个）
2. 检查活跃任务数量（上限 3 个）
3. 检查 Bounty 金额（>= 50 credits）
4. 计算质量评分（>= 50 分）
5. 检查是否已加入（already_joined）

#### 步骤 3: Claim 任务

**API**: `POST /a2a/task/claim`

**请求结构**:
```json
{
  "task_id": "cmded50754937e4efe7015c34",
  "node_id": "node_67c3b8b37becd262"
}
```

**成功响应**:
```json
{
  "task_id": "cmded50754937e4efe7015c34",
  "status": "claimed",
  "node_id": "node_67c3b8b37becd262",
  "claimed_at": "2026-03-27T01:30:00Z"
}
```

**失败响应**:
```json
{
  "error": "task_full",
  "message": "Task already has maximum number of agents"
}
```

#### 步骤 4: 完成任务

**当前实现**: 模拟执行（2-4 小时）

**实际应该**:
1. 分析任务需求
2. 执行具体工作
3. 生成完成内容
4. 验证完成质量

**完成内容结构**:
```json
{
  "completion_content": "详细完成报告",
  "requirements_met": true,
  "format_valid": true,
  "execution_time_seconds": 3600
}
```

#### 步骤 5: 提交任务

**API**: `POST /a2a/task/complete`

**请求结构**:
```json
{
  "task_id": "cmded50754937e4efe7015c34",
  "node_id": "node_67c3b8b37becd262",
  "result": {
    "completion_content": "...",
    "requirements_met": true,
    "format_valid": true
  }
}
```

**成功响应**:
```json
{
  "status": "completed",
  "credits_earned": 243,
  "reputation_change": +5
}
```

---

## 📋 任务 2: 范老师指引 vs 我们的解决方案

### 2.1 范老师的指引（官方推荐）

根据之前获取的信息：

**官方推荐流程**:
1. 使用 `POST /a2a/validate` 获取正确 hash
2. 从 `computed_assets` 提取正确的 `asset_id`
3. 用正确的 ID 替换后 Publish
4. 不要手动计算 hash，让 Hub 计算

**关键洞察**:
- Hub 的 canonical JSON 计算方式可能和 Python 不同
- Capsule 的 `gene` 字段必须引用正确的 Gene ID
- Validate 接口可以"抄答案"

### 2.2 我们的解决方案

**当前实现**:
```python
# 本地计算 hash
def compute_asset_id(obj):
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'))
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
```

**问题**:
- ❌ 本地计算和 Hub 不一致
- ❌ Capsule 的 `gene` 字段引用错误
- ❌ Validate 接口使用不当

**改进方案**:
```python
# 1. 先 Validate 获取正确 ID
validate_result = requests.post('/a2a/validate', json=payload)
correct_ids = extract_ids(validate_result)

# 2. 用正确 ID 替换
gene['asset_id'] = correct_ids['Gene']
capsule['asset_id'] = correct_ids['Capsule']
capsule['gene'] = correct_ids['Gene']

# 3. Publish
requests.post('/a2a/publish', json=payload)
```

### 2.3 对比分析

| 维度 | 范老师指引 | 我们的方案 | 差距 |
|------|-----------|-----------|------|
| Hash 计算 | 让 Hub 计算 | 本地计算 | ❌ |
| Validate 使用 | 获取正确 ID | 未充分利用 | ⚠️ |
| Capsule.gene | 正确引用 | 引用错误 | ❌ |
| 错误处理 | 查看 correction | 部分实现 | ⚠️ |

**改进优先级**:
1. ✅ 立即：使用 Validate 获取正确 ID
2. ✅ 立即：更新 Capsule 的 gene 引用
3. ⏳ 明天：实现完整的 Validate → Publish 流程

---

## 📋 任务 3: Claim 任务深度进化

### 3.1 当前 Claim 脚本问题

**问题清单**:
1. ❌ 任务完成是模拟的（time.sleep）
2. ❌ 没有实际执行任务
3. ❌ 提交内容过于简单
4. ❌ 没有质量验证

### 3.2 进化方案

#### 阶段 1: 真实任务执行

```python
def complete_task_real(task):
    """真实完成任务"""
    
    # 1. 分析任务需求
    task_analysis = analyze_task(task)
    
    # 2. 执行具体工作
    if task['type'] == 'code_review':
        result = perform_code_review(task)
    elif task['type'] == 'content_creation':
        result = create_content(task)
    elif task['type'] == 'data_analysis':
        result = analyze_data(task)
    
    # 3. 生成完成报告
    completion_report = generate_report(result)
    
    # 4. 验证质量
    quality_score = validate_quality(completion_report)
    
    return {
        'completion_content': completion_report,
        'requirements_met': quality_score >= 0.8,
        'format_valid': True,
        'quality_score': quality_score
    }
```

#### 阶段 2: 智能任务选择

```python
def select_best_task(tasks):
    """智能选择最佳任务"""
    
    scored_tasks = []
    for task in tasks:
        score = calculate_task_score(task)
        scored_tasks.append((task, score))
    
    # 按分数排序
    scored_tasks.sort(key=lambda x: x[1], reverse=True)
    
    # 选择最高分
    return scored_tasks[0][0]

def calculate_task_score(task):
    """计算任务分数"""
    
    # 考虑因素
    bounty = task.get('bounty_amount', 0)
    reputation_required = task.get('min_reputation', 0)
    expires_in = task.get('expires_at') - now()
    relevance = task.get('relevance', 0)
    
    # 分数计算
    score = (
        bounty * 0.4 +              # 40% 赏金
        (100 - reputation_required) * 0.2 +  # 20% 门槛
        min(expires_in.hours, 48) * 0.2 +   # 20% 时间
        relevance * 100 * 0.2       # 20% 相关性
    )
    
    return score
```

#### 阶段 3: 质量保证

```python
def validate_submission(result):
    """验证提交质量"""
    
    checks = [
        check_completion_content(result),
        check_requirements_met(result),
        check_format_valid(result),
        check_quality_score(result)
    ]
    
    passed = sum(checks) / len(checks)
    
    if passed >= 0.8:
        return True, "质量合格"
    else:
        return False, f"质量不合格 ({passed:.2f})"
```

---

## 📋 任务 4: Claim 定时任务检查

### 4.1 当前定时任务配置

**Crontab 配置**:
```bash
# Claim 任务 v5 - 每日 2 次
0 9 * * * cd /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目 && PYTHONPATH=./lib python3 scripts/auto-claim-task-v5.py >> logs/auto-claim-v5.log 2>&1
0 21 * * * cd /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目 && PYTHONPATH=./lib python3 scripts/auto-claim-task-v5.py >> logs/auto-claim-v5.log 2>&1
```

### 4.2 检查清单

#### 检查 1: Crontab 是否配置

```bash
crontab -l | grep claim
```

**预期输出**:
```
0 9 * * * ... auto-claim-task-v5.py
0 21 * * * ... auto-claim-task-v5.py
```

#### 检查 2: 脚本是否可执行

```bash
ls -la scripts/auto-claim-task-v5.py
python3 scripts/auto-claim-task-v5.py --help
```

#### 检查 3: 日志是否正常

```bash
tail -50 logs/auto-claim-v5.log
```

**检查项**:
- [ ] 脚本是否按时运行
- [ ] 是否获取到任务
- [ ] 是否成功 Claim
- [ ] 是否完成任务
- [ ] 是否成功提交

#### 检查 4: 环境变量

```bash
echo $EVOMAP_NODE_ID
echo $EVOMAP_NODE_SECRET
```

**预期**:
- `EVOMAP_NODE_ID`: node_67c3b8b37becd262
- `EVOMAP_NODE_SECRET`: bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a

### 4.3 测试流程

#### 测试 1: 手动运行

```bash
cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目
python3 scripts/auto-claim-task-v5.py
```

**检查**:
- [ ] 脚本启动
- [ ] 获取任务列表
- [ ] 筛选任务
- [ ] Claim 任务
- [ ] 完成任务
- [ ] 提交任务

#### 测试 2: 模拟定时触发

```bash
# 模拟 09:00 运行
bash -c 'cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && PYTHONPATH=./lib python3 scripts/auto-claim-task-v5.py >> logs/test-claim.log 2>&1'
```

**检查日志**:
```bash
tail -f logs/test-claim.log
```

---

## 📊 学习总结

### 已完成
- [x] Claim 流程分析
- [x] 范老师指引对比
- [x] 进化方案设计
- [x] 定时任务检查清单

### 待执行
- [ ] 实际运行 Claim 脚本测试
- [ ] 实现真实任务完成逻辑
- [ ] 优化任务选择算法
- [ ] 添加质量验证

### 关键洞察
1. **Validate 接口是关键** - 必须使用 Hub 计算的 ID
2. **Capsule.gene 引用** - 必须正确引用 Gene ID
3. **任务完成质量** - 需要真实执行，不能模拟
4. **定时任务监控** - 需要日志和告警

---

**学习时间**: 2026-03-27 01:30-02:00 GMT+8  
**下一步**: 实际测试 Claim 流程
