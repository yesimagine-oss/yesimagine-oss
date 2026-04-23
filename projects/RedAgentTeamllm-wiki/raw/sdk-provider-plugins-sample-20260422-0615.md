# OpenClaw SDK Provider Plugins 文档采样与资产蒸馏报告 - 2026-04-22 06:15

**来源**: https://docs.openclaw.ai/plugins/sdk-provider-plugins  
**采样时间**: 2026-04-22 06:15 GMT+8  
**状态**: 🟡 仅主页面，待补充各厂商配置/鉴权/熔断策略

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/sdk-provider-plugins | SDK Provider Plugins |
| https://docs.openclaw.ai/plugins/sdk-provider-plugins | Purpose: connect to external LLM / AI service providers |
| https://docs.openclaw.ai/plugins/sdk-provider-plugins | Install: openclaw plugin install sdk-provider-<name> |
| https://docs.openclaw.ai/plugins/sdk-provider-plugins | Config path: /etc/openclaw/plugins/sdk-provider.yaml |
| https://docs.openclaw.ai/plugins/sdk-provider-plugins | Supported: openai, anthropic, cohere, ollama, local-llm |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins \| grep "SDK Provider Plugins"` | SDK Provider Plugins |
| `curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins \| grep "connect to external LLM / AI service providers"` | Purpose: connect to external LLM / AI service providers |
| `curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins \| grep "openclaw plugin install sdk-provider-"` | Install: openclaw plugin install sdk-provider-<name> |
| `curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins \| grep "/etc/openclaw/plugins/sdk-provider.yaml"` | Config path: /etc/openclaw/plugins/sdk-provider.yaml |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/sdk-provider-plugins
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/sdk-provider-plugins]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/sdk-provider-plugins]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/plugins/sdk-channel-plugins）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对 SDK Provider 插件主页面抓取，未深入各厂商配置、鉴权、模型参数与异常处理，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 插件页面标题 | 同上 | SDK Provider Plugins | grep 匹配 | SDK Provider Plugins | 标识 SDK 厂商对接插件文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心用途 | 同上 | connect to external LLM / AI service providers | grep 匹配 | Purpose: connect to external LLM / AI service providers | 为 Agent 接入各类模型服务 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件安装语法 | 同上 | 按厂商名安装 Provider 插件 | grep 匹配 | Install: openclaw plugin install sdk-provider-<name> | 安装对应 AI 厂商对接插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 配置文件路径 | 同上 | 统一 Provider 配置位置 | grep 匹配 | Config path: /etc/openclaw/plugins/sdk-provider.yaml | 配置 API Key、模型、超时 | 是 | 是 | 0.99 | 原文 + 实测 |
| 支持厂商列表 | 同上 | openai, anthropic, cohere, ollama, local-llm | grep 匹配 | Supported: openai, anthropic, cohere, ollama, local-llm | 选择要对接的模型厂商 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 各厂商完整配置 | 同上 | 无各厂商 YAML 示例 | 无法直接配置对接 | 0.80 | 抓取 API Key、Endpoint、模型配置 |
| 鉴权与安全策略 | 同上 | 无密钥管理/加密设置 | 密钥存在泄露风险 | 0.75 | 查找安全存储配置 |
| 请求参数控制 | 同上 | 无 temperature/top_p 等参数 | 模型行为不可控 | 0.70 | 提取推理参数配置 |
| 熔断与限流策略 | 同上 | 无重试/限流/熔断 | 服务不稳定 | 0.65 | 抓取 circuit-breaker 配置 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_sdk_provider_plugin_title","name":"SDK Provider 插件标题","description":"该页面为 OpenClaw 对接外部 LLM/AI 服务厂商的 SDK 插件说明文档","validate_command":"curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins | grep \"SDK Provider Plugins\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_sdk_provider_install_syntax","name":"SDK Provider 安装语法","description":"按厂商安装：openclaw plugin install sdk-provider-<厂商名>","validate_command":"curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins | grep \"openclaw plugin install sdk-provider-\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_sdk_provider_config_path","name":"SDK Provider 配置路径","description":"厂商对接配置文件：/etc/openclaw/plugins/sdk-provider.yaml","validate_command":"curl -s https://docs.openclaw.ai/plugins/sdk-provider-plugins | grep \"/etc/openclaw/plugins/sdk-provider.yaml\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_sdk_provider_ollama","name":"安装 Ollama 厂商插件","trigger_signal":"openclaw:plugin:install:sdk-provider:ollama","executable_code":"openclaw plugin install sdk-provider-ollama","description":"安装本地 Ollama 模型对接插件","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_edit_sdk_provider_config","name":"编辑 SDK Provider 配置","trigger_signal":"openclaw:plugin:sdk-provider:config:edit","executable_code":"vi /etc/openclaw/plugins/sdk-provider.yaml","description":"配置 API 密钥、模型地址、推理参数与安全策略","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_sdk_provider_20260424","distilled_skill":"Provider 页面识别、用途提取、安装语法、配置路径、支持厂商提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"标题、AI 厂商对接用途、安装语法、配置路径、5 类支持厂商","候选但未蒸馏部分":"各厂商配置、鉴权安全、模型参数、熔断限流、使用示例","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 标题、LLM 厂商对接用途、安装语法、配置路径、支持厂商
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: SDK Provider 插件定位与基础对接能力
- **候选事实**: 厂商详细配置、密钥安全、模型参数、熔断限流
- **被剔除内容**: 无
- **当前结论边界**: 已掌握插件用途、安装方式与支持厂商，可搭建模型对接基础环境；缺少各厂商配置模板、安全策略与稳定性控制，无法直接用于生产级 AI 服务接入。

---

**入库时间**: 2026-04-22 06:15 GMT+8  
**Git 状态**: 待提交
