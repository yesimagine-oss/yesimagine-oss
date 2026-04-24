# OpenClaw Plugin Bundles 文档采样与资产蒸馏报告 - 2026-04-22 04:55

**来源**: https://docs.openclaw.ai/plugins/bundles  
**采样时间**: 2026-04-22 04:55 GMT+8  
**状态**: 🟡 仅主页面，待补充完整包明细/配置模板/升级命令

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/bundles | Plugin Bundles & Preset Collections |
| https://docs.openclaw.ai/plugins/bundles | Bundle: pre-configured set of plugins for common scenarios |
| https://docs.openclaw.ai/plugins/bundles | Available bundles: security, gateway, observability, devkit |
| https://docs.openclaw.ai/plugins/bundles | Install bundle: openclaw plugin install bundle/<bundle-name> |
| https://docs.openclaw.ai/plugins/bundles | security bundle: auth-proxy, rate-limiter, secrets-scanner |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/bundles \| grep "Plugin Bundles & Preset Collections"` | Plugin Bundles & Preset Collections |
| `curl -s https://docs.openclaw.ai/plugins/bundles \| grep "pre-configured set of plugins"` | Bundle: pre-configured set of plugins for common scenarios |
| `curl -s https://docs.openclaw.ai/plugins/bundles \| grep "security, gateway, observability, devkit"` | Available bundles: security, gateway, observability, devkit |
| `curl -s https://docs.openclaw.ai/plugins/bundles \| grep "openclaw plugin install bundle/"` | Install bundle: openclaw plugin install bundle/<bundle-name> |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/bundles
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/bundles]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/bundles]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/plugins/community）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对插件捆绑包主页面抓取，未深入单个捆绑包详情，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 插件捆绑包页面标题 | 同上 | Plugin Bundles & Preset Collections | grep 匹配 | Plugin Bundles & Preset Collections | 标识捆绑包文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 捆绑包定义 | 同上 | pre-configured plugin set | grep 匹配 | Bundle: pre-configured set of plugins for common scenarios | 理解捆绑包用途 | 是 | 是 | 0.99 | 原文 + 实测 |
| 可用捆绑包列表 | 同上 | security/gateway/observability/devkit | grep 匹配 | Available bundles: security, gateway, observability, devkit | 选择场景化插件包 | 是 | 是 | 0.99 | 原文 + 实测 |
| 捆绑包安装语法 | 同上 | bundle/<name> 安装格式 | grep 匹配 | Install bundle: openclaw plugin install bundle/<bundle-name> | 一键安装插件包 | 是 | 是 | 0.99 | 原文 + 实测 |
| 安全捆绑包含插件 | 同上 | auth-proxy、rate-limiter、secrets-scanner | grep 匹配 | security bundle: auth-proxy, rate-limiter, secrets-scanner | 查看安全包组成 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 各捆绑包含插件明细 | 同上 | 仅 security 包完整列出 | 不了解其他包构成 | 0.80 | 抓取 gateway/observability/devkit 组成 |
| 捆绑包配置模板 | 同上 | 无预置配置示例 | 安装后需手动配置 | 0.75 | 提取默认配置片段 |
| 捆绑包升级/卸载 | 同上 | 无批量升级命令 | 无法统一更新插件 | 0.70 | 查找 bundle update/remove 用法 |
| 自定义捆绑包 | 同上 | 无创建自定义包方法 | 无法按需组合插件 | 0.65 | 抓取自定义 bundle 规范 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_plugin_bundles_title","name":"插件捆绑包文档标题","description":"该页面为 OpenClaw 场景化插件捆绑包说明文档","validate_command":"curl -s https://docs.openclaw.ai/plugins/bundles | grep \"Plugin Bundles & Preset Collections\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_bundle_install_syntax","name":"捆绑包安装语法","description":"使用 openclaw plugin install bundle/<bundle-name> 安装场景插件包","validate_command":"curl -s https://docs.openclaw.ai/plugins/bundles | grep \"openclaw plugin install bundle/\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_security_bundle_content","name":"安全捆绑包含义","description":"security 捆绑包包含 auth-proxy、rate-limiter、secrets-scanner","validate_command":"curl -s https://docs.openclaw.ai/plugins/bundles | grep \"security bundle: auth-proxy\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_security_bundle","name":"安装安全插件捆绑包","trigger_signal":"openclaw:bundle:install:security","executable_code":"openclaw plugin install bundle/security","description":"一键安装安全加固插件包","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_observability_bundle","name":"安装可观测性插件包","trigger_signal":"openclaw:bundle:install:observability","executable_code":"openclaw plugin install bundle/observability","description":"一键安装监控日志类插件包","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_bundles_20260424","distilled_skill":"捆绑包页面识别、定义理解、捆绑包列表提取、安装语法提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"页面标题、捆绑包定义、4 大官方捆绑包、安装命令、security 包组成","候选但未蒸馏部分":"其他捆绑包明细、配置模板、批量升级、自定义捆绑包规范","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 页面标题、捆绑包定义、捆绑包列表、安装语法、security 包构成
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: 场景化插件捆绑包体系与一键部署能力
- **候选事实**: 完整包明细、配置模板、升级卸载、自定义捆绑
- **被剔除内容**: 无
- **当前结论边界**: 已掌握捆绑包概念与安装方法，可一键部署安全、网关等场景插件集；缺少完整配置与批量运维命令，无法实现精细化运营。

---

**入库时间**: 2026-04-22 04:55 GMT+8  
**Git 状态**: 待提交
