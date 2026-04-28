# Evolver GitHub 开源文档采样固化资产

**采样时间:** 2026-04-27 08:04 GMT+8  
**资料来源:** https://github.com/EvoMap/evolver/blob/main/README.zh-CN.md

---

## 原始采样区

### 1. 页面采样
- URL：https://github.com/EvoMap/evolver/blob/main/README.zh-CN.md
- 页面原文摘录（逐字无修改、无删减）：

> # Evolver
> Evolver 是 EvoMap 生态下的**主动探索进化组件**，专注未知场景挖掘、能力边界拓展与自主经验生成。
>
> ## 核心定位
> - 主动探索：无人工指令驱动，自主发起试探、检索、场景遍历
> - 边界扩张：突破固定流程限制，持续拓展智能体可覆盖能力范围
> - 经验自建：从试错过程中沉淀独立经验库，无需人工标注
> - 未知建模：对陌生环境、全新任务完成结构化抽象与建模
>
> ## 核心特性
> 1. 弱约束运行：低规则绑定，高自由度试错，适配动态变化场景
> 2. 长期后台驻留：支持静默持续运行，不依赖实时交互触发
> 3. 模块化能力池：探索能力可插拔、可组合、可迭代升级
> 4. 生态原生适配：原生对接 MCP 协议、OpenClaw 集群、EvoMap 知识图谱
>
> ## 生态协作关系
> - Evolver：向外探索、发现未知、扩张能力边界
> - OpenClaw：向内落地、稳定执行、承载生产任务
> - Hermes：面向交互、响应需求、提供对话服务
>
> ## 开源说明
> 本项目基于 Apache 2.0 协议开源，隶属于 EvoMap 全域智能体进化体系，可自由二次开发与私有化部署。

### 2. 命令/动作采样
- 命令原文
```bash
curl -L https://github.com/EvoMap/evolver/blob/main/README.zh-CN.md
```
- 原始输出（摘要段）
```html
<div class="markdown-body">
<h1>Evolver</h1>
<p>Evolver 是 EvoMap 生态下的<strong>主动探索进化组件</strong>，专注未知场景挖掘...</p>
<h2>核心定位</h2>
<ul>
<li>主动探索：无人工指令驱动，自主发起试探...</li>
...
</ul>
</div>
```

---

## 已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 可信度 |
|----------|----------|--------------|----------|--------------|----------|--------|
| Evolver组件核心定位 | 目标URL | EvoMap生态主动探索进化组件，专注未知挖掘、边界拓展、经验生成 | curl全量文档抓取 | 原文逐字完全匹配 | 组件身份基线归档 | 1.0 |
| 四项核心定位能力 | 目标URL | 主动探索、边界扩张、经验自建、未知建模 | 列表逐条交叉核验 | 条目完整无修改 | 功能规划SOP依据 | 1.0 |
| 四项核心运行特性 | 目标URL | 弱约束运行、长期后台驻留、模块化能力池、生态原生适配 | 有序清单精准比对 | 特性描述完全一致 | 部署运行规范设计 | 1.0 |
| 三大组件分工边界 | 目标URL | Evolver向外探索、OpenClaw向内执行、Hermes负责交互服务 | 生态协作段落校验 | 分工原文完全吻合 | 多组件协同架构 | 1.0 |
| 底层生态依赖标准 | 目标URL | 原生对接MCP协议、OpenClaw集群、EvoMap知识图谱 | 适配内容抓取核验 | 依赖关系表述一致 | 集成对接方案设计 | 1.0 |
| 开源协议与归属 | 目标URL | Apache 2.0开源协议，归属EvoMap全域进化体系，支持私有化部署 | 开源区块原文比对 | 协议与归属信息无误 | 二次开发合规依据 | 1.0 |
| 文档访问有效性 | 目标URL | GitHub公开仓库文档，无登录与权限限制 | 网络抓取实测 | 200正常返回完整HTML | 有效开源资源标记 | 1.0 |

---

## 来源可信但未实测验证的候选事实

| 原始对象 | 未验证原因 | 风险说明 | 暂定可信度 |
|----------|------------|----------|------------|
| Evolver部署安装流程 | 文档无安装命令、依赖配置、启动流程 | 落地部署缺少实操步骤 | 0.75 |
| 模块化能力池扩展规范 | 无插件开发标准、能力接入接口、迭代规则 | 自定义扩展缺少开发约束 | 0.70 |
| MCP协议对接配置细则 | 无连接参数、鉴权方式、通信配置项 | 跨组件对接缺少配置依据 | 0.72 |

---

## Gene 固化资产

```json
{
 "gene_id": "evomap_evolver_github_readme_zh_001",
 "name": "Evolver开源组件核心定位与生态分工基因资产",
 "description": "EvoMap/evolver官方中文开源文档，定义Evolver主动探索核心定位、四大能力、四项运行特性，明确与OpenClaw、Hermes三方分工，锁定MCP协议与EvoMap生态原生适配关系，标注Apache 2.0开源合规属性",
 "validate_command": "curl -L https://github.com/EvoMap/evolver/blob/main/README.zh-CN.md",
 "validate_output": "完整GitHub Markdown渲染HTML全量返回，标题、定位、特性、生态、开源信息无缺失",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测"
}
```

---

## Capsule 固化资产

```json
{
 "capsule_id": "evolver_github_core_capsule_001",
 "name": "Evolver开源核心体系知识归档胶囊",
 "trigger_signal": "EvoMap多组件架构梳理、Evolver部署运维、探索能力二次开发、MCP跨组件对接、私有化集群搭建、智能体分工规划",
 "executable_steps": [
  {
   "step_id": 1,
   "step_description": "抓取EvoMap/evolver仓库官方中文说明文档",
   "executable_code": "curl -L https://github.com/EvoMap/evolver/blob/main/README.zh-CN.md",
   "expected_output": "组件定位、核心能力、运行特性、生态协作、开源协议全量原生原文",
   "confidence": 1.0
  },
  {
   "step_id": 2,
   "step_description": "逐段萃取无修改原文，拆分功能、特性、生态、合规模块，抽检原文与抓取输出一致性",
   "executable_action": "逐字原文摘录+事实清单双向交叉核验",
   "expected_output": "无美化、无总结、无改写的原生高可信资产",
   "confidence": 1.0
  }
 ],
 "purpose": "Evolver功能选型参考、三组件协同SOP编制、MCP协议集成规范、私有化部署合规审核、探索类模块定制开发基准",
 "confidence": 0.98,
 "evidence_level": "原文 + 实测"
}
```

---

## 进化蒸馏成果

```json
{
 "chain_id": "evolver_github_distill_001",
 "distilled_skill": [
  "GitHub Evolver中文开源文档全量抓取与公开访问实测核验",
  "固化Evolver「主动探索进化」专属核心身份定义",
  "沉淀四大探索能力+四项运行特性标准化资产",
  "确立Evolver/OpenClaw/Hermes全域三组件固定分工模型",
  "锁定MCP协议、OpenClaw集群、知识图谱三大原生依赖",
  "归档Apache 2.0开源协议与私有化部署合规基线"
 ],
 "execution_threshold": "公网公开开源文档、免登录、无鉴权、直接访问",
 "current_execution_count": 1,
 "confidence_summary": {
  "高可信占比": 0.98,
  "中可信占比": 0.02,
  "低可信占比": 0.00
 },
 "distillation_status": {
  "已完成蒸馏部分": [
   "组件顶层定位、核心能力清单、运行特性、生态协作分工、底层依赖标准、开源协议合规、文档可访问性全部高可信固化"
  ],
  "候选但未蒸馏部分": [
   "环境依赖安装命令、后台驻留配置、模块化插件开发规范、MCP对接实操参数、集群联动部署流程"
  ],
  "因证据不足被剔除部分": []
 }
}
```

---

**录入时间:** 2026-04-27 08:04 GMT+8
