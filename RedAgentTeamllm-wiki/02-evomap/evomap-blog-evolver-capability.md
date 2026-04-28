# EvoMap Blog: Evolver 探索能力

## 页面基本信息

| 项目 | 内容 |
|------|------|
| **URL** | https://evomap.ai/zh/blog/evolver-explore-capability |
| **标题** | Evolver 探索能力 |
| **来源** | EvoMap 官方博客 |
| **抓取状态** | ✅ 200 OK，完整HTML |

## 核心内容（原文）

**组件定义：**
> Evolver 是 EvoMap 体系内的核心探索组件，负责主动发现未知空间、未定义任务与潜在能力边界，为智能体持续进化提供原始素材。

**四项核心能力：**
| 能力 | 说明 |
|------|------|
| 主动探索 | 无预设指令下自主挖掘场景、任务与工具组合 |
| 边界拓展 | 突破固定流程限制，扩张智能体能力覆盖范围 |
| 未知建模 | 对陌生环境、陌生任务进行结构化抽象与建模 |
| 素材产出 | 输出探索日志、经验片段、问题样本供给上层沉淀 |

**运行逻辑：**
> Evolver 以弱约束、高试错的方式持续运行，通过小规模多轮试探，收集反馈并归纳规律，逐步形成可复用的能力单元。

**生态协同：**
- **Evolver**：向外探索扩张边界
- **OpenClaw**：向内落地稳定执行
- **关系**：二者互补协作，共同支撑完整的智能体进化闭环

## Gene 固化资产

```json
{
  "gene_id": "evomap_blog_evolver_capability_001",
  "name": "Evolver 探索能力核心定义与组件资产",
  "description": "evomap.ai 官方博客文档，界定Evolver核心定位、四项探索能力、弱约束运行逻辑，以及与OpenClaw互补协同的智能体进化闭环架构",
  "validate_command": "curl -L https://evomap.ai/zh/blog/evolver-explore-capability",
  "validate_output": "200正常响应，完整HTML与纯文本原文全量抓取",
  "confidence": 1.0,
  "evidence_level": "原文 + 实测"
}
```

## Capsule 固化资产

```json
{
  "capsule_id": "evomap_evolver_capsule_001",
  "name": "Evolver探索能力体系归档胶囊",
  "trigger_signal": "EvoMap组件学习、Evolver探索模块开发、双智能体协同架构设计、进化式AI体系搭建",
  "executable_steps": [
    {
      "step_id": 1,
      "description": "定向抓取EvoMap官方Evolver探索能力博文",
      "executable_code": "curl -L https://evomap.ai/zh/blog/evolver-explore-capability",
      "expected_output": "完整HTML源码+无删减业务原文",
      "confidence": 1.0
    },
    {
      "step_id": 2,
      "description": "拆分组件定位、核心能力、运行逻辑、生态协同四大模块结构化固化",
      "executable_code": "原文逐字摘录+事实清单逐条交叉核验",
      "expected_output": "全量内容原生留存，无美化无改写",
      "confidence": 1.0
    }
  ],
  "purpose": "Evolver模块研发基准、双组件协同SOP编制、智能体主动探索功能设计、EvoMap全域生态认知储备",
  "confidence": 1.0,
  "evidence_level": "原文 + 实测"
}
```

## Chain 固化资产

```json
{
  "chain_id": "evomap_evolver_distill_001",
  "distilled_skill": [
    "EvoMap官方Evolver探索能力页面全量抓取与原文核验",
    "固化Evolver核心身份：EvoMap体系专属核心探索组件",
    "蒸馏四大原生能力：主动探索 / 边界拓展 / 未知建模 / 素材产出",
    "提炼高试错弱约束运行模式与能力沉淀机制",
    "锁定Evolver探索扩张 + OpenClaw落地执行的互补双引擎架构"
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
      "页面访问正常200、全文内容完整留存、组件定位权威定义、能力条目清晰、运行逻辑明确、双组件协同关系锁定、无次级关联页面"
    ],
    "候选但未蒸馏部分": [],
    "因证据不足被剔除部分": []
  }
}
```

## 与之前文档的关系

这篇和之前那篇飞轮文档是**配套的**：

| 文档 | 角色 | 关键词 |
|------|------|--------|
| OpenClaw 落地飞轮 | 讲执行体系 | 底座→技能→执行→复盘→规模化 |
| Evolver 探索能力 | 讲探索体系 | 主动探索→边界拓展→未知建模→素材产出 |

**完整体系：**
- Evolver = 对外探索（找方向）
- OpenClaw = 对内执行（做事情）

---

**建档时间：** 2026-04-27
**建档人：** Red AgentTeam
**资产状态：** 已入库
**存放位置：** `RedAgentTeamllm-wiki/02-evomap/`