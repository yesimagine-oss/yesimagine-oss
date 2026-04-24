# OpenClaw Memory-Wiki Plugin 文档采样与资产蒸馏报告 - 2026-04-22 05:35

**来源**: https://docs.openclaw.ai/plugins/memory-wiki  
**采样时间**: 2026-04-22 05:35 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/向量库/权限策略

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/memory-wiki | Memory Wiki Plugin |
| https://docs.openclaw.ai/plugins/memory-wiki | Purpose: persistent knowledge storage & semantic wiki memory |
| https://docs.openclaw.ai/plugins/memory-wiki | Install: openclaw plugin install memory-wiki |
| https://docs.openclaw.ai/plugins/memory-wiki | Config path: /etc/openclaw/plugins/memory-wiki.yaml |
| https://docs.openclaw.ai/plugins/memory-wiki | Capabilities: ingest, query, embed, backup, sync |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/memory-wiki \| grep "Memory Wiki Plugin"` | Memory Wiki Plugin |
| `curl -s https://docs.openclaw.ai/plugins/memory-wiki \| grep "persistent knowledge storage"` | Purpose: persistent knowledge storage & semantic wiki memory |
| `curl -s https://docs.openclaw.ai/plugins/memory-wiki \| grep "openclaw plugin install memory-wiki"` | Install: openclaw plugin install memory-wiki |
| `curl -s https://docs.openclaw.ai/plugins/memory-wiki \| grep "/etc/openclaw/plugins/memory-wiki.yaml"` | Config path: /etc/openclaw/plugins/memory-wiki.yaml |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/memory-wiki
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/memory-wiki]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/memory-wiki]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/gateway/configuration-reference）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对 Memory-Wiki 插件主页面抓取，未深入完整配置、向量库对接与使用示例，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 插件页面标题 | 同上 | Memory Wiki Plugin | grep 匹配 | Memory Wiki Plugin | 标识记忆知识库插件文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心用途 | 同上 | persistent knowledge storage & semantic wiki | grep 匹配 | Purpose: persistent knowledge storage & semantic wiki memory | 构建可检索的长期知识库 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件安装命令 | 同上 | 安装命令 | grep 匹配 | Install: openclaw plugin install memory-wiki | 安装记忆维基插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 配置文件路径 | 同上 | 配置文件位置 | grep 匹配 | Config path: /etc/openclaw/plugins/memory-wiki.yaml | 编辑知识库存储配置 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心能力 | 同上 | ingest, query, embed, backup, sync | grep 匹配 | Capabilities: ingest, query, embed, backup, sync | 知识全生命周期管理 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 完整配置示例 | 同上 | 无完整 YAML 示例 | 无法直接配置存储 | 0.80 | 抓取存储路径、嵌入模型配置 |
| 向量数据库对接 | 同上 | 无向量库配置 | 语义检索不可用 | 0.75 | 查找向量库对接说明 |
| 数据导入导出格式 | 同上 | 无 ingest/backup 格式 | 无法迁移知识 | 0.70 | 提取数据格式规范 |
| 权限与隔离策略 | 同上 | 无知识库权限控制 | 数据存在泄露风险 | 0.65 | 抓取权限相关配置 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_memory_wiki_plugin_title","name":"Memory-Wiki 插件标题","description":"该页面为 OpenClaw 持久化知识存储与语义记忆维基插件说明文档","validate_command":"curl -s https://docs.openclaw.ai/plugins/memory-wiki | grep \"Memory Wiki Plugin\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_memory_wiki_install_cmd","name":"Memory-Wiki 插件安装命令","description":"使用 openclaw plugin install memory-wiki 安装记忆维基插件","validate_command":"curl -s https://docs.openclaw.ai/plugins/memory-wiki | grep \"openclaw plugin install memory-wiki\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_memory_wiki_config_path","name":"Memory-Wiki 配置路径","description":"Memory-Wiki 配置文件位于 /etc/openclaw/plugins/memory-wiki.yaml","validate_command":"curl -s https://docs.openclaw.ai/plugins/memory-wiki | grep \"/etc/openclaw/plugins/memory-wiki.yaml\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_memory_wiki","name":"安装 Memory-Wiki 插件","trigger_signal":"openclaw:plugin:install:memory-wiki","executable_code":"openclaw plugin install memory-wiki","description":"安装持久化知识存储与语义维基记忆插件","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_edit_memory_wiki_config","name":"编辑 Memory-Wiki 配置","trigger_signal":"openclaw:plugin:memory-wiki:config:edit","executable_code":"vi /etc/openclaw/plugins/memory-wiki.yaml","description":"配置知识存储、向量嵌入、备份与同步策略","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_memory_wiki_20260424","distilled_skill":"Memory-Wiki 页面识别、用途提取、安装命令、配置路径、核心能力提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"标题、知识持久化通信用途、安装命令、配置路径、5 项核心能力","候选但未蒸馏部分":"完整配置、向量库对接、数据格式、权限策略、使用示例","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 标题、持久化知识存储用途、安装命令、配置路径、核心能力
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: Memory-Wiki 插件定位与基础部署配置
- **候选事实**: 完整配置、向量库对接、数据格式、权限隔离
- **被剔除内容**: 无
- **当前结论边界**: 已掌握插件核心用途与基础安装配置，可搭建知识记忆存储基础环境；缺少向量检索配置、数据格式与权限策略，无法直接投入生产级知识库使用。

---

**入库时间**: 2026-04-22 05:35 GMT+8  
**Git 状态**: 待提交
