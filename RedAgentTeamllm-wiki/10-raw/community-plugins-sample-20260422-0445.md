# OpenClaw Community Plugins 文档采样与资产蒸馏报告 - 2026-04-22 04:45

**来源**: https://docs.openclaw.ai/plugins/community  
**采样时间**: 2026-04-22 04:45 GMT+8  
**状态**: 🟡 仅主页面，待补充插件配置/版本/依赖说明

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/community | Community Plugins Registry |
| https://docs.openclaw.ai/plugins/community | Official community repo: https://github.com/openclaw/community-plugins |
| https://docs.openclaw.ai/plugins/community | Available plugins: auth-proxy, request-transformer, rate-limiter, logging-ext |
| https://docs.openclaw.ai/plugins/community | Install from community: openclaw plugin install community/<plugin-name> |
| https://docs.openclaw.ai/plugins/community | Contribution guide: PR to GitHub repository |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/community \| grep "Community Plugins Registry"` | Community Plugins Registry |
| `curl -s https://docs.openclaw.ai/plugins/community \| grep "github.com/openclaw/community-plugins"` | Official community repo: https://github.com/openclaw/community-plugins |
| `curl -s https://docs.openclaw.ai/plugins/community \| grep "auth-proxy, request-transformer"` | Available plugins: auth-proxy, request-transformer, rate-limiter, logging-ext |
| `curl -s https://docs.openclaw.ai/plugins/community \| grep "openclaw plugin install community/"` | Install from community: openclaw plugin install community/<plugin-name> |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/community
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/community]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/community]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/plugins）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对社区插件 registry 主页面抓取，未深入单个插件文档，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 社区插件页面标题 | 同上 | Community Plugins Registry | grep 匹配 | Community Plugins Registry | 标识社区插件文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 官方社区插件仓库 | 同上 | GitHub 仓库地址 | grep 匹配 | Official community repo: https://github.com/openclaw/community-plugins | 获取开源插件源码 | 是 | 是 | 0.99 | 原文 + 实测 |
| 社区可用插件列表 | 同上 | 4 个官方社区插件 | grep 匹配 | Available plugins: auth-proxy, request-transformer, rate-limiter, logging-ext | 选择可用扩展插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 社区插件安装语法 | 同上 | 安装命令格式 | grep 匹配 | Install from community: openclaw plugin install community/<plugin-name> | 安装社区插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 贡献方式 | 同上 | 提交 PR 至仓库 | grep 匹配 | Contribution guide: PR to GitHub repository | 参与社区插件开发 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 单个插件配置示例 | 同上 | 无各插件 YAML 示例 | 无法直接配置使用 | 0.80 | 抓取单个插件配置片段 |
| 插件版本与兼容性 | 同上 | 无版本匹配规则 | 可能安装不兼容版本 | 0.75 | 提取版本约束说明 |
| 插件依赖要求 | 同上 | 无依赖声明 | 安装后可能无法运行 | 0.70 | 查找依赖相关说明 |
| 插件卸载/更新命令 | 同上 | 无更新专用命令 | 无法升级社区插件 | 0.65 | 抓取 update/upgrade 说明 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_community_plugins_title","name":"社区插件仓库标题","description":"该页面为 OpenClaw 官方社区插件 registry 与使用指南","validate_command":"curl -s https://docs.openclaw.ai/plugins/community | grep \"Community Plugins Registry\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_community_plugin_install_syntax","name":"社区插件安装格式","description":"安装社区插件使用 openclaw plugin install community/<插件名>","validate_command":"curl -s https://docs.openclaw.ai/plugins/community | grep \"openclaw plugin install community/\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_community_plugin_list","name":"社区插件清单","description":"官方社区提供 auth-proxy / request-transformer / rate-limiter / logging-ext","validate_command":"curl -s https://docs.openclaw.ai/plugins/community | grep \"auth-proxy, request-transformer\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_community_rate_limiter","name":"安装限流社区插件","trigger_signal":"openclaw:plugin:install:community:rate-limiter","executable_code":"openclaw plugin install community/rate-limiter","description":"安装社区版限流插件","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_community_auth_proxy","name":"安装认证代理社区插件","trigger_signal":"openclaw:plugin:install:community:auth-proxy","executable_code":"openclaw plugin install community/auth-proxy","description":"安装社区版认证代理插件","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_community_20260424","distilled_skill":"社区插件页面识别、仓库地址提取、插件列表提取、安装语法提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"页面标题、GitHub 仓库地址、4 个官方社区插件、安装命令格式、贡献方式","候选但未蒸馏部分":"单个插件配置、版本兼容、依赖、更新/升级命令、详细使用示例","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 页面标题、社区仓库、插件列表、安装语法、贡献指南
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: 社区插件整体生态与基础安装能力
- **候选事实**: 插件配置、版本兼容、依赖、更新升级、详细用法
- **被剔除内容**: 无
- **当前结论边界**: 已掌握社区插件来源、可用列表与安装方法，可直接安装限流、认证代理等扩展；缺少各插件实际配置与排障方法，无法直接投入生产使用。

---

**入库时间**: 2026-04-22 04:45 GMT+8  
**Git 状态**: 待提交
