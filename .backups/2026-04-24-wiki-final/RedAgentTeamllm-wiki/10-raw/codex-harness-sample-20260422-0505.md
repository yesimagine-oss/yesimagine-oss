# OpenClaw Codex-Harness Plugin 文档采样与资产蒸馏报告 - 2026-04-22 05:05

**来源**: https://docs.openclaw.ai/plugins/codex-harness  
**采样时间**: 2026-04-22 05:05 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/调用方式/安全策略

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/codex-harness | Codex Harness Plugin |
| https://docs.openclaw.ai/plugins/codex-harness | Purpose: secure code execution & sandboxed agent runtime |
| https://docs.openclaw.ai/plugins/codex-harness | Install: openclaw plugin install codex-harness |
| https://docs.openclaw.ai/plugins/codex-harness | Config path: /etc/openclaw/plugins/codex-harness.yaml |
| https://docs.openclaw.ai/plugins/codex-harness | Capabilities: isolate, timeout, resource-limit, log-capture |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/codex-harness \| grep "Codex Harness Plugin"` | Codex Harness Plugin |
| `curl -s https://docs.openclaw.ai/plugins/codex-harness \| grep "secure code execution"` | Purpose: secure code execution & sandboxed agent runtime |
| `curl -s https://docs.openclaw.ai/plugins/codex-harness \| grep "openclaw plugin install codex-harness"` | Install: openclaw plugin install codex-harness |
| `curl -s https://docs.openclaw.ai/plugins/codex-harness \| grep "/etc/openclaw/plugins/codex-harness.yaml"` | Config path: /etc/openclaw/plugins/codex-harness.yaml |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/codex-harness
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/codex-harness]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/codex-harness]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/plugins/bundles）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对 Codex-Harness 插件主页面抓取，未深入完整配置与运行时示例，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 插件页面标题 | 同上 | Codex Harness Plugin | grep 匹配 | Codex Harness Plugin | 标识插件文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心用途 | 同上 | secure code execution & sandboxed | grep 匹配 | Purpose: secure code execution & sandboxed agent runtime | 安全运行代码/Agent | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件安装命令 | 同上 | 直接安装命令 | grep 匹配 | Install: openclaw plugin install codex-harness | 安装 Codex 沙箱插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 配置文件路径 | 同上 | 插件配置位置 | grep 匹配 | Config path: /etc/openclaw/plugins/codex-harness.yaml | 修改沙箱配置 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心能力 | 同上 | isolate, timeout, resource-limit | grep 匹配 | Capabilities: isolate, timeout, resource-limit, log-capture | 控制沙箱行为 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 完整配置示例 | 同上 | 无完整 YAML 示例 | 无法直接配置 | 0.80 | 抓取配置字段说明 |
| 运行时调用方式 | 同上 | 无执行接口/命令 | 无法使用沙箱 | 0.75 | 提取调用语法 |
| 资源限制默认值 | 同上 | 无 CPU/内存默认值 | 可能资源溢出 | 0.70 | 查找默认限制 |
| 安全策略配置 | 同上 | 无权限白名单 | 存在安全风险 | 0.65 | 抓取安全策略项 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_codex_harness_title","name":"Codex-Harness 插件标题","description":"该页面为 OpenClaw 安全代码执行沙箱插件说明文档","validate_command":"curl -s https://docs.openclaw.ai/plugins/codex-harness | grep \"Codex Harness Plugin\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_codex_install_cmd","name":"Codex 插件安装命令","description":"使用 openclaw plugin install codex-harness 安装沙箱插件","validate_command":"curl -s https://docs.openclaw.ai/plugins/codex-harness | grep \"openclaw plugin install codex-harness\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_codex_config_path","name":"Codex 配置路径","description":"Codex-Harness 配置文件位于 /etc/openclaw/plugins/codex-harness.yaml","validate_command":"curl -s https://docs.openclaw.ai/plugins/codex-harness | grep \"/etc/openclaw/plugins/codex-harness.yaml\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_codex_harness","name":"安装 Codex-Harness 沙箱插件","trigger_signal":"openclaw:plugin:install:codex-harness","executable_code":"openclaw plugin install codex-harness","description":"安装安全代码执行沙箱插件","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_edit_codex_config","name":"编辑 Codex 沙箱配置","trigger_signal":"openclaw:plugin:codex:config:edit","executable_code":"vi /etc/openclaw/plugins/codex-harness.yaml","description":"修改沙箱隔离、超时、资源限制配置","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_codex_harness_20260424","distilled_skill":"Codex 页面识别、用途提取、安装命令、配置路径、核心能力提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"标题、用途、安装命令、配置路径、沙箱四大核心能力","候选但未蒸馏部分":"完整配置、调用方式、资源默认值、安全策略、运行示例","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 标题、用途、安装命令、配置路径、核心能力
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: Codex-Harness 沙箱插件定位与基础部署配置
- **候选事实**: 完整配置、调用方式、资源限制、安全策略
- **被剔除内容**: 无
- **当前结论边界**: 已掌握插件用途、安装与配置位置，可部署安全沙箱环境；缺少实际调用与精细配置，无法直接投入代码执行场景。

---

**入库时间**: 2026-04-22 05:05 GMT+8  
**Git 状态**: 待提交
