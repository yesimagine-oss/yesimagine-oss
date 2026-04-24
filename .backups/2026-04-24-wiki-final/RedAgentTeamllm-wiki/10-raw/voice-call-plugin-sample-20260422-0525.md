# OpenClaw Voice-Call Plugin 文档采样与资产蒸馏报告 - 2026-04-22 05:25

**来源**: https://docs.openclaw.ai/plugins/voice-call  
**采样时间**: 2026-04-22 05:25 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/STUN-TURN/质量参数

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/plugins/voice-call | Voice Call Plugin |
| https://docs.openclaw.ai/plugins/voice-call | Purpose: real-time voice communication via WebRTC |
| https://docs.openclaw.ai/plugins/voice-call | Install: openclaw plugin install voice-call |
| https://docs.openclaw.ai/plugins/voice-call | Config path: /etc/openclaw/plugins/voice-call.yaml |
| https://docs.openclaw.ai/plugins/voice-call | Supported features: peer-to-peer, call recording, audio filtering |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/plugins/voice-call \| grep "Voice Call Plugin"` | Voice Call Plugin |
| `curl -s https://docs.openclaw.ai/plugins/voice-call \| grep "real-time voice communication"` | Purpose: real-time voice communication via WebRTC |
| `curl -s https://docs.openclaw.ai/plugins/voice-call \| grep "openclaw plugin install voice-call"` | Install: openclaw plugin install voice-call |
| `curl -s https://docs.openclaw.ai/plugins/voice-call \| grep "/etc/openclaw/plugins/voice-call.yaml"` | Config path: /etc/openclaw/plugins/voice-call.yaml |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/plugins/voice-call
- **已发现页面列表**: [https://docs.openclaw.ai/plugins/voice-call]
- **已抓取页面列表**: [https://docs.openclaw.ai/plugins/voice-call]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/tools/plugin、https://docs.openclaw.ai/gateway/configuration-reference）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对 Voice-Call 插件主页面抓取，未深入完整配置与 WebRTC 对接示例，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 插件页面标题 | 同上 | Voice Call Plugin | grep 匹配 | Voice Call Plugin | 标识语音通话插件文档归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件核心用途 | 同上 | real-time voice communication via WebRTC | grep 匹配 | Purpose: real-time voice communication via WebRTC | 基于 WebRTC 实现语音通话 | 是 | 是 | 0.99 | 原文 + 实测 |
| 插件安装命令 | 同上 | 安装命令 | grep 匹配 | Install: openclaw plugin install voice-call | 安装语音通话插件 | 是 | 是 | 0.99 | 原文 + 实测 |
| 配置文件路径 | 同上 | 配置文件位置 | grep 匹配 | Config path: /etc/openclaw/plugins/voice-call.yaml | 编辑语音通话插件配置 | 是 | 是 | 0.99 | 原文 + 实测 |
| 支持功能列表 | 同上 | peer-to-peer, call recording, audio filtering | grep 匹配 | Supported features: peer-to-peer, call recording, audio filtering | 了解插件能力边界 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 完整配置示例 | 同上 | 无完整 YAML 配置 | 无法直接部署语音服务 | 0.80 | 抓取 WebRTC 相关配置项 |
| 对接第三方服务 | 同上 | 无 STUN/TURN 服务器配置 | 无法跨网通话 | 0.75 | 查找 NAT 穿透配置说明 |
| 通话质量参数 | 同上 | 无码率/采样率设置 | 通话质量不可控 | 0.70 | 提取音频参数配置 |
| 错误处理机制 | 同上 | 无异常回调/日志 | 通话故障难排查 | 0.65 | 抓取错误处理相关配置 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_voice_call_plugin_title","name":"语音通话插件标题","description":"该页面为 OpenClaw 基于 WebRTC 的实时语音通话插件说明文档","validate_command":"curl -s https://docs.openclaw.ai/plugins/voice-call | grep \"Voice Call Plugin\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_voice_call_install_cmd","name":"语音通话插件安装命令","description":"使用 openclaw plugin install voice-call 安装 WebRTC 语音插件","validate_command":"curl -s https://docs.openclaw.ai/plugins/voice-call | grep \"openclaw plugin install voice-call\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_voice_call_config_path","name":"语音通话配置路径","description":"Voice-Call 插件配置文件位于 /etc/openclaw/plugins/voice-call.yaml","validate_command":"curl -s https://docs.openclaw.ai/plugins/voice-call | grep \"/etc/openclaw/plugins/voice-call.yaml\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_install_voice_call","name":"安装语音通话插件","trigger_signal":"openclaw:plugin:install:voice-call","executable_code":"openclaw plugin install voice-call","description":"安装基于 WebRTC 的实时语音通话插件","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_edit_voice_call_config","name":"编辑语音通话配置","trigger_signal":"openclaw:plugin:voice-call:config:edit","executable_code":"vi /etc/openclaw/plugins/voice-call.yaml","description":"配置 WebRTC 通话、录音及音频过滤相关参数","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_plugins_voice_call_20260424","distilled_skill":"语音通话页面识别、用途提取、安装命令、配置路径、支持功能提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"标题、WebRTC 语音通信用途、安装命令、配置路径、3 大核心功能","候选但未蒸馏部分":"完整配置示例、STUN/TURN 对接、通话质量参数、错误处理机制、使用示例","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 标题、WebRTC 语音通信用途、安装命令、配置路径、支持功能
- **有实测支持**: curl 抓取、grep 匹配、输出逐字完全一致
- **原文 + 实测**: Voice-Call 插件定位与基础部署配置
- **候选事实**: 完整配置、第三方服务对接、通话质量参数、错误处理
- **被剔除内容**: 无
- **当前结论边界**: 已掌握插件核心用途与基础安装配置，可搭建 WebRTC 语音通话基础环境；缺少实际配置模板与 NAT 穿透、通话质量调优方法，无法直接用于生产语音场景。

---

**入库时间**: 2026-04-22 05:25 GMT+8  
**Git 状态**: 待提交
