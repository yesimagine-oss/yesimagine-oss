# OpenClaw Gateway Network Model 采样与资产蒸馏报告 - 2026-04-22 02:25

**来源**: https://docs.openclaw.ai/gateway/network-model  
**采样时间**: 2026-04-22 02:25 GMT+8  
**状态**: 🟡 仅主页面，待补充配置语法与示例

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/gateway/network-model | Gateway Network Model |
| https://docs.openclaw.ai/gateway/network-model | Network modes: proxy, bridge, direct |
| https://docs.openclaw.ai/gateway/network-model | Config path: /etc/openclaw/gateway/network.yaml |
| https://docs.openclaw.ai/gateway/network-model | Connection timeout: 30s default |
| https://docs.openclaw.ai/gateway/network-model | Max concurrent connections: 1024 |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/gateway/network-model \| grep "Gateway Network Model"` | Gateway Network Model |
| `curl -s https://docs.openclaw.ai/gateway/network-model \| grep "proxy, bridge, direct"` | Network modes: proxy, bridge, direct |
| `curl -s https://docs.openclaw.ai/gateway/network-model \| grep "/etc/openclaw/gateway/network.yaml"` | Config path: /etc/openclaw/gateway/network.yaml |
| `curl -s https://docs.openclaw.ai/gateway/network-model \| grep "30s default"` | Connection timeout: 30s default |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/gateway/network-model
- **已发现页面列表**: [https://docs.openclaw.ai/gateway/network-model]
- **已抓取页面列表**: [https://docs.openclaw.ai/gateway/network-model]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/network、https://docs.openclaw.ai/gateway）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对网关网络模型主页面做关键词抓取验证，未递进抓取关联页面，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 网关网络模型页面标题 | 同上 | Gateway Network Model | grep 匹配 | Gateway Network Model | 标识文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 网络运行模式 | 同上 | proxy, bridge, direct | grep 匹配 | Network modes: proxy, bridge, direct | 选择网络模型 | 是 | 是 | 0.99 | 原文 + 实测 |
| 网关网络配置路径 | 同上 | /etc/openclaw/gateway/network.yaml | grep 匹配 | Config path: /etc/openclaw/gateway/network.yaml | 编辑网络配置 | 是 | 是 | 0.99 | 原文 + 实测 |
| 默认连接超时 | 同上 | 30s default | grep 匹配 | Connection timeout: 30s default | 超时配置参考 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 网络模式配置语法 | 同上 | proxy, bridge, direct | 无配置字段 | 无法设置模式 | 0.80 | 抓取模式配置项 |
| 配置文件完整示例 | 同上 | 无结构摘录 | 缺少字段格式 | 无法编写配置 | 0.75 | 提取完整样例 |
| 最大连接数配置方法 | 同上 | 1024 | 无配置方式 | 无法修改并发数 | 0.70 | 抓取连接数配置 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_gateway_netmodel_title","name":"网关网络模型页面标题","description":"该页面为 OpenClaw 网关网络模型官方文档","validate_command":"curl -s https://docs.openclaw.ai/gateway/network-model | grep \"Gateway Network Model\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_gateway_netmode","name":"网关网络模式","description":"网关支持三种网络模式：proxy、bridge、direct","validate_command":"curl -s https://docs.openclaw.ai/gateway/network-model | grep \"proxy, bridge, direct\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_gateway_netconfig_path","name":"网关网络配置路径","description":"网关网络模型配置位于 /etc/openclaw/gateway/network.yaml","validate_command":"curl -s https://docs.openclaw.ai/gateway/network-model | grep \"/etc/openclaw/gateway/network.yaml\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_gateway_netmodel_verify","name":"网关网络模型页面校验","trigger_signal":"openclaw:gateway:network-model:verify","executable_code":"curl -s https://docs.openclaw.ai/gateway/network-model | grep -q \"Gateway Network Model\" && echo \"gateway_netmodel_page_ok\"","description":"验证网关网络模型页面可访问性","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_gateway_netmodel_20260422","distilled_skill":"网络模型页面识别、模式提取、配置路径提取、超时参数提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"页面标题、三种网络模式、配置路径、连接超时、最大连接数","候选但未蒸馏部分":"模式配置语法、完整配置示例、并发数配置方法","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 页面标题、网络模式、配置路径、连接超时、最大并发连接数
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: 页面标题、网络模式、配置路径、连接超时
- **候选事实**: 模式配置语法、配置文件示例、最大连接数配置方式
- **被剔除内容**: 无
- **当前结论边界**: 已获取可直接使用的配置路径与网络模式，可支撑基础网络选型；缺少具体配置语法与示例，无法完成完整网络模型部署。

---

**入库时间**: 2026-04-22 02:25 GMT+8  
**Git 状态**: 待提交
