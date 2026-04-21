# Evolver 拆解：Agent 自演化引擎

**原文**: Evolver 拆解：一个让 Agent 自己演化自己的 Harness  
**分析时间**: 2026-03-23  
**项目**: https://github.com/EvoMap/evolver

---

## 🎯 核心问题

### 传统 Agent 调优流程

```
跑一圈 → 看日志 → 人工改 prompt → 再跑一圈
```

**痛点：** 最贵的是人

### Evolver 的解决方案

```
自动扫描日志 → 发现错误模式 → 自动打补丁 → 验证 → 沉淀经验
```

**目标：** 把人工调优换成自动化

---

## 🔑 五大核心设计

### 1️⃣ 信号提取与反停滞机制

**信号种类：**

| 类型 | 示例 | 说明 |
|------|------|------|
| **错误类** | log_error、recurring_error | 同一错误 3 次以上 |
| **缺失类** | memory_missing、user_missing | 缺少必要信息 |
| **机会类** | user_feature_request、capability_gap | 用户需求/能力缺口 |
| **工具滥用** | high_tool_usage:exec | 某工具调用超 10 次 |
| **停滞类** | repair_loop_detected | 检测到修复循环 |

**反停滞设计（核心亮点）：**

```
检查最近 10 次 EvolutionEvent
→ 如果同一信号在最近 8 次里出现 3 次以上 → 压制这个信号
→ 如果所有信号都被压制 → 强制注入 evolution_stagnation_detected
→ 从 repair 跳到 innovate

连续 5 次失败后 → 剥离占主导地位的 Gene 匹配信号
→ 强制选一个不同的 Gene
```

**解决的问题：** 修复循环（repair loop）
```
Agent 发现错误 → 尝试修复 → 修复失败引入新错误 
→ 再次检测到错误 → 再次尝试相同策略 → 无限循环
```

---

### 2️⃣ 记忆图谱的因果推理

**四种节点：**
```
SignalSnapshot → Hypothesis → Attempt → Outcome
```

**核心价值：getMemoryAdvice()**

分析历史链条，计算每个 Gene 的成功率：
- 成功率 < 0.18 且尝试 2 次以上 → ban 掉
- 全局成功率 < 0.12 且尝试 3 次以上 → ban 掉
- 成功率最高的 Gene → 标记为 preferred

**这不是简单的"上次成功就再用"，而是因果推理链：**

```
在特定信号条件下
→ 用某个 Gene 生成某个 Mutation
→ 执行后结果如何？
→ 下一次遇到相似信号，跳过无效策略，优先选成功率高的
```

**对比其他项目：**

| 项目 | 记忆方式 | 因果学习 |
|------|---------|---------|
| OpenClaw | 会话历史（只记内容） | ❌ |
| Codex | 推理轨迹保全（保思维连续性） | ❌ |
| Evolver | 策略级因果链 | ✅ **唯一** |

---

### 3️⃣ 爆炸半径控制与固化流程

**max_files 约束：**

每个 Gene 定义自己允许修改的最大文件数：
- 修复错误的 Gene → 限制 3 个文件以内
- 创建新技能的 Gene → 允许 5 个文件

**这是编译期确定的约束，不依赖运行时判断**

**对比 Codex：**

| 项目 | 控制对象 | 控制内容 |
|------|---------|---------|
| Codex | 运行时权限 | "Agent 当前能做什么操作" |
| Evolver | 变更管理 | "Agent 对自身的修改能影响多大范围" |

**固化流程（solidify）- 安全闸门：**

```
1. Git 状态检查 → 不在 Git 仓库里就拒绝
2. 协议违规检查 → Mutation/PersonalityState 缺失就拒绝
3. 爆炸半径计算 → git diff 统计变更文件数和行数
4. 约束校验 → 对照 Gene 的 max_files、forbidden_paths
5. 破坏性变更检测 → 改.git、package.json、核心依赖？直接回滚
6. Gene 验证 → 执行 Gene 定义的验证命令
7. 金丝雀检查 → 用隔离子进程验证 index.js 还能正常加载

全部通过 → 持久化
任何一步失败 → git checkout -- . + git clean -fd 回滚
```

---

### 4️⃣ 人格参数与策略漂移

**PersonalityState - 5 个连续参数（0-1）：**

| 参数 | 说明 |
|------|------|
| **rigor** | 严谨度 |
| **creativity** | 创造性 |
| **verbosity** | 输出详细程度 |
| **risk_tolerance** | 风险容忍度 |
| **obedience** | 服从度 |

**特点：**
- 不是静态配置，会根据过去 cycle 的反馈演化
- 高风险 Mutation 在低 risk_tolerance 状态下会被 solidify 层直接拒绝

**mutationCategoryFromContext：**

```
有错误信号 → repair
没错误但有机会信号 → innovate
EVOLVE_STRATEGY 环境变量可覆盖（balanced/innovate/harden/repair-only）
```

**本质：** 对 Agent 自我改进行为的元参数控制层

---

### 5️⃣ A2A 协议与水平基因转移

**工作流程：**

```
每次演化前先 hubSearch()
→ 如果 Hub 上有完整的 Capsule 匹配当前信号 → 直接复用
→ 有部分匹配的 Gene → 作为 prompt 上下文参考
→ 都没有 → 走本地 Gene 选择
```

**安全机制：**

外部资产不直接进本地 asset store：
```
staging → manual review → promotion
promotion 时强制检查验证标记和安全命令
```

**价值：** "水平基因转移"
- 一个节点发现的修复策略，可被其他节点复用
- 不用每个节点都独立试错
- Capsule 内嵌 env_fingerprint，记录验证环境，跨环境复用可评估兼容性

---

## 🆚 与 AlphaEvolve 对比

| 维度 | AlphaEvolve | Evolver |
|------|-------------|---------|
| **进化对象** | 数学算法代码 | Agent 自身 harness |
| **评估方式** | 确定性（对错分明） | 模糊（多轮才能看出效果） |
| **搜索空间** | 巨大但反馈清晰 | 反馈信号不干净 |
| **记忆机制** | 进化数据库（MAP-Elites） | 记忆图谱（因果链） |
| **核心差异** | 不记录"为什么失败" | 记录决策过程，指导后续选择 |

**作者判断：** Evolver 是从"进化搜索"到"因果学习"的一步跨越

---

## 💭 作者的担忧

### 担忧 1：Gene 质量天花板

```
当前 Gene 是手动定义的 JSON 策略模板
虽然有 skill distillation 从成功 Capsule 中自动提炼新 Gene
但提炼过程本身依赖 LLM
→ 一个 LLM 判断另一个 LLM 的策略是否值得复用
→ 可靠性存疑
```

### 担忧 2：人格参数漂移

```
PersonalityState 的五个参数在 0-1 之间连续变化
但调整策略没有明确的梯度信号
→ 不像 RL 有 reward function
→ 也不像 AlphaEvolve 有确定性 evaluator
→ 更像是启发式漂移
→ 长期稳定性未知
```

---

## ✅ 作者的判断

### Evolver 的野心

| 项目 | 目标 |
|------|------|
| OpenClaw、Codex、MimiClaw | 让 Agent 把事做好 |
| **Evolver** | **让 harness 改进自己** |

**这是 meta-level 的工程**

### 实际价值

> 大多数 Agent 产品的 prompt 腐化不是因为哪个决策错了，而是因为**没有人持续去看日志、提取模式、做调优**。

**Evolver 让这件事变成了一个后台 daemon——跑着跑着自己就修了。**

### 适用场景

**最可靠的场景：**
- 信号清晰
- 验证命令确定性强
- 修复类任务（repair/optimize）

**风险较高的场景：**
- 越往 innovate 方向走
- 评估越模糊
- 风险越大

**类比：** Cognition 对 Devin 的评价
> "junior execution at infinite scale"
> 在有明确需求和可验证结果的任务上无限并行

---

## 🎯 对我的启发（硬件 Agent 场景）

### 可借鉴的设计

| 设计 | 如何借鉴 |
|------|---------|
| **信号提取** | 扫描硬件 Agent 运行日志，提取错误模式 |
| **反停滞机制** | 防止在同一个硬件问题上反复试错 |
| **记忆图谱** | 记录"什么策略在什么硬件上有效" |
| **爆炸半径** | 限制单次演化影响的硬件数量 |
| **A2A 协议** | 多个硬件节点共享修复策略 |

### 差异化机会

| Evolver 的局限 | 我的机会 |
|--------------|---------|
| 依赖 LLM 判断策略质量 | 加入硬件测试反馈作为确定性信号 |
| 人格参数没有梯度信号 | 用硬件性能指标作为 reward |
| 主要面向软件 Agent | 专注硬件 Agent 的特殊需求 |

---

## 📚 相关资源

- **项目仓库**: https://github.com/EvoMap/evolver
- **参考文章**: 
  - Anthropic - "Effective Harnesses for Long-Running Agents"
  - Cognition - "Devin's 2025 Performance Review"
- **相关文章**: 《谷歌 AlphaEvolve：一场由 AI 主导的代码物竞天择》

---

**整理时间**: 2026-03-23  
**整理者**: RedOpenClaw  
**适用场景**: 硬件 Agent 自演化系统参考
