# OpenClaw Hubs 启动页面采样与可执行资产蒸馏报告 - 2026-04-22 01:15

**来源**: https://docs.openclaw.ai/start/hubs  
**采样时间**: 2026-04-22 01:15 GMT+8  
**状态**: 🟡 仅主页面，待补充创建流程与配置格式

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/start/hubs | OpenClaw Hubs Getting Started |
| https://docs.openclaw.ai/start/hubs | Create your first hub |
| https://docs.openclaw.ai/start/hubs | Hub configuration directory: /var/lib/openclaw/hubs |
| https://docs.openclaw.ai/start/hubs | Start hub with: openclaw hub start |
| https://docs.openclaw.ai/start/hubs | List running hubs: openclaw hub list |
| https://docs.openclaw.ai/start/hubs | Stop hub with: openclaw hub stop |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/start/hubs \| grep "OpenClaw Hubs Getting Started"` | OpenClaw Hubs Getting Started |
| `curl -s https://docs.openclaw.ai/start/hubs \| grep "/var/lib/openclaw/hubs"` | Hub configuration directory: /var/lib/openclaw/hubs |
| `curl -s https://docs.openclaw.ai/start/hubs \| grep "openclaw hub start"` | Start hub with: openclaw hub start |
| `curl -s https://docs.openclaw.ai/start/hubs \| grep "openclaw hub list"` | List running hubs: openclaw hub list |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/start/hubs
- **已发现页面列表**: [https://docs.openclaw.ai/start/hubs]
- **已抓取页面列表**: [https://docs.openclaw.ai/start/hubs]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/start、https://docs.openclaw.ai/channels）
- **是否仍有未抓取区域**: 是（关联页面未抓取，配置格式/创建步骤未抓取）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对主页面进行抓取与关键词验证，未对关联上级/子页面做递进抓取，不满足 100% 覆盖条件

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 页面标题标识 | 同上 | OpenClaw Hubs Getting Started | grep 匹配 | OpenClaw Hubs Getting Started | 确认入门文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| Hub 配置目录 | 同上 | /var/lib/openclaw/hubs | grep 匹配 | Hub configuration directory: /var/lib/openclaw/hubs | 定位配置文件目录 | 是 | 是 | 0.99 | 原文 + 实测 |
| Hub 启动命令 | 同上 | openclaw hub start | grep 匹配 | Start hub with: openclaw hub start | 执行 Hub 启动操作 | 是 | 是 | 0.99 | 原文 + 实测 |
| Hub 列表查看命令 | 同上 | openclaw hub list | grep 匹配 | List running hubs: openclaw hub list | 查看运行中 Hub 实例 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 来源原文摘录 | 未验证原因 | 风险说明 | 暂定可信度 | 后续验证建议 |
|---------|---------|-------------|-----------|---------|-----------|-------------|
| 创建首个 Hub 详细步骤 | 同上 | Create your first hub | 无分步命令/流程 | 无法完成创建操作 | 0.80 | 抓取完整创建步骤 |
| Hub 停止命令完整用法 | 同上 | openclaw hub stop | 无参数/示例 | 无法精准停止指定 Hub | 0.75 | 提取停止命令用法 |
| Hub 配置文件格式 | 同上 | 无配置字段摘录 | 缺少配置结构 | 无法编写合法 Hub 配置 | 0.70 | 抓取配置文件示例 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_hubs_start_title","name":"Hub 入门文档标题","description":"该页面为 OpenClaw Hubs 官方入门文档","validate_command":"curl -s https://docs.openclaw.ai/start/hubs | grep \"OpenClaw Hubs Getting Started\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_hub_config_dir","name":"Hub 配置文件目录","description":"OpenClaw Hub 配置文件默认存放于 /var/lib/openclaw/hubs","validate_command":"curl -s https://docs.openclaw.ai/start/hubs | grep \"/var/lib/openclaw/hubs\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_hub_start_cmd","name":"Hub 启动命令","description":"使用 openclaw hub start 命令启动 Hub 实例","validate_command":"curl -s https://docs.openclaw.ai/start/hubs | grep \"openclaw hub start\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_hubs_start_verify","name":"Hub 入门页面校验","trigger_signal":"openclaw:start:hubs:verify","executable_code":"curl -s https://docs.openclaw.ai/start/hubs | grep -q \"OpenClaw Hubs Getting Started\" && echo \"hubs_start_page_ok\"","description":"验证 Hub 入门文档可访问性","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_start_hubs_20260422","distilled_skill":"Hub 页面识别、配置目录提取、启动命令提取、列表命令提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"文档标识、配置目录、启动命令、列表查看命令","候选但未蒸馏部分":"Hub 创建步骤、停止命令用法、配置文件格式","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 页面标题、创建 Hub、配置目录、启动命令、列表命令、停止命令
- **有实测支持**: curl 页面抓取、grep 关键词匹配、原始结果逐字输出
- **原文 + 实测**: 文档标题、配置目录、启动命令、列表查看命令
- **候选事实**: Hub 创建详细步骤、停止命令完整用法、Hub 配置文件格式
- **被剔除内容**: 无
- **当前结论边界**: 已提取可直接执行的基础命令与路径，缺少创建流程与配置格式，仅支持 Hub 启停与状态查看

---

**入库时间**: 2026-04-22 01:15 GMT+8  
**Git 状态**: 待提交
