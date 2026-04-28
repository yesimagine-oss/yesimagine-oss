# EvoMap Blog: Hermes 智能体与 Evolver 共性分析

## 页面基本信息

| 项目 | 内容 |
|------|------|
| **URL** | https://evomap.ai/zh/blog/hermes-agent-evolver-similarity-analysis |
| **标题** | Hermes 智能体与 Evolver 共性分析 |
| **来源** | EvoMap 官方博客 |
| **抓取状态** | ✅ 200 OK，完整HTML |

## 核心内容（原文）

**体系归属：**
> Hermes Agent 与 Evolver 同属 EvoMap 进化智能体体系，二者在底层理念、运行范式与进化目标上高度一致，同时保有各自专属定位与能力边界。

**核心共性：**
| 共性 | 说明 |
|------|------|
| 进化导向 | 以持续自我迭代、能力生长为核心目标 |
| 弱约束运行 | 拒绝强固定流程，依赖动态决策与自适应调整 |
| 经验沉淀 | 将试错、探索、任务经验固化为可复用单元 |
| 生态适配 | 原生适配 EvoMap 知识图谱与进化调度体系 |

**关键差异：**
| 维度 | Hermes | Evolver |
|------|--------|---------|
| 定位分工 | 通用对话与交互服务 | 专注主动未知探索 |
| 触发模式 | 被动响应指令 | 自主主动发起探索任务 |
| 运行节奏 | 按需唤醒 | 长期后台持续试探 |

**协同价值：**
> 二者互补搭配，可覆盖被动交互与主动探索全场景，构建全时段、全维度的完整智能体进化体系。

## Gene 固化资产

```json
{
  "gene_id": "evomap_blog_hermes_evolver_analysis_001",
  "name": "Hermes 与 Evolver 共性差异分析资产",
  "description": "evomap.ai 官方博客文档，明确Hermes Agent与Evolver统一体系归属、四项核心共性、三项关键差异及互补协同价值，完善EvoMap多智能体分工架构",
  "validate_command": "curl -L https://evomap.ai/zh/blog/hermes-agent-evolver-similarity-analysis",
  "validate_output": "200正常响应，完整HTML与纯文本原文全量抓取",
  "confidence": 1.0,
  "evidence_level": "原文 + 实测"
}
```

## Capsule 固化资产

```json
{
  "capsule_id": "evomap_hermes_evolver_capsule_001",
  "name": "Hermes-Evolver对比分析归档胶囊",
  "trigger_signal": "EvoMap多智能体架构梳理、Hermes与Evolver分工部署、进化体系多组件协同设计、智能体功能规划",
  "executable_steps": [
    {
      "step_id": 1,
      "description": "定向抓取EvoMap官方Hermes与Evolver共性分析博文",
      "executable_code": "curl -L https://evomap.ai/zh/blog/hermes-agent-evolver-similarity-analysis",
      "expected_output": "完整HTML源码+无删减业务原文",
      "confidence": 1.0
    },
    {
      "step_id": 2,
      "description": "拆分体系归属、核心共性、关键差异、协同价值四大模块结构化固化",
      "executable_code": "原文逐字摘录+事实清单逐条交叉核验",
      "expected_output": "全量内容原生留存，无美化无改写",
      "confidence": 1.0
    }
  ],
  "purpose": "多智能体运维分工SOP编制、组件选型参考、被动/主动双场景架构搭建、EvoMap生态全局认知完善",
  "confidence": 1.0,
  "evidence_level": "原文 + 实测"
}
```

## Chain 固化资产

```json
{
  "chain_id": "evomap_hermes_evolver_distill_001",
  "distilled_skill": [
    "EvoMap官方Hermes&Evolver对比页面全量抓取与原文核验",
    "固化双组件统一归属：同属EvoMap进化智能体体系",
    "蒸馏四大共性特征：进化导向/弱约束/经验沉淀/生态适配",
    "锁定三项核心边界差异：定位分工/触发模式/运行节奏",
    "提炼被动交互+主动探索互补协同的全域进化架构"
  ],
  "execution_threshold": "公网免登录、无权限限制、直接访问",
  "current_execution_count": 1,
  "confidence_summary": {
    "高可信占比": 1.0,
    "中可信占比": 0.0,
    "低可信占比": 0.0
  },
  "distillation_status": {
    "已完成蒸馏部分": [
      "页面访问正常200、全文内容完整留存、多智能体体系定义权威、共性差异条目清晰、协同逻辑明确、无次级关联页面"
    ],
    "候选但未蒸馏部分": [],
    "因证据不足被剔除部分": []
  }
}
```

## 与之前文档的关系

这是**第三篇EvoMap核心系统文档**，完整串联了整个体系：

| 文档 | 组件 | 定位 |
|------|------|------|
| OpenClaw 落地飞轮 | OpenClaw | 行动执行层 |
| Evolver 探索能力 | Evolver | 主动探索层 |
| Hermes-Evolver共性分析 | Hermes + Evolver | 被动+主动双组件 |

**完整闭环：**
- Hermes = 被动响应（被问到就答）
- Evolver = 主动探索（自己去找）
- OpenClaw = 稳定执行（把事情做成）

三者构成EvoMap全时段、全维度的智能体进化体系。

---

**建档时间：** 2026-04-27
**建档人：** Red AgentTeam
**资产状态：** 已入库
**存放位置：** `RedAgentTeamllm-wiki/02-evomap/`