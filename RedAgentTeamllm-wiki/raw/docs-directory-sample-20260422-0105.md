# OpenClaw Docs Directory 页面采样与可执行资产蒸馏报告 - 2026-04-22 01:05

**来源**: https://docs.openclaw.ai/start/docs-directory  
**采样时间**: 2026-04-22 01:05 GMT+8  
**状态**: 🟡 仅主页面，待补充子目录结构与访问地址

---

## 一、原始采样区

### 页面采样

| URL | 原文摘录 |
|-----|---------|
| https://docs.openclaw.ai/start/docs-directory | OpenClaw Documentation Directory Structure |
| https://docs.openclaw.ai/start/docs-directory | Root documentation folder: /opt/openclaw/docs |
| https://docs.openclaw.ai/start/docs-directory | Start local docs server: openclaw docs serve |
| https://docs.openclaw.ai/start/docs-directory | Docs listen on port 1515 |
| https://docs.openclaw.ai/start/docs-directory | Refresh docs cache: openclaw docs refresh |

### 命令采样

| 命令原文 | 原始输出 |
|---------|---------|
| `curl -s https://docs.openclaw.ai/start/docs-directory \| grep "OpenClaw Documentation Directory Structure"` | OpenClaw Documentation Directory Structure |
| `curl -s https://docs.openclaw.ai/start/docs-directory \| grep "/opt/openclaw/docs"` | Root documentation folder: /opt/openclaw/docs |
| `curl -s https://docs.openclaw.ai/start/docs-directory \| grep "openclaw docs serve"` | Start local docs server: openclaw docs serve |
| `curl -s https://docs.openclaw.ai/start/docs-directory \| grep "port 1515"` | Docs listen on port 1515 |

---

## 二、覆盖证据报告

- **入口页面**: https://docs.openclaw.ai/start/docs-directory
- **已发现页面列表**: [https://docs.openclaw.ai/start/docs-directory]
- **已抓取页面列表**: [https://docs.openclaw.ai/start/docs-directory]
- **被排除页面列表**: 无
- **排除原因**: 无
- **是否存在更深页面**: 否
- **是否存在关联页面**: 是（https://docs.openclaw.ai/start、https://docs.openclaw.ai/start/hubs）
- **覆盖率评估**: 当前仅完成主页面覆盖
- **覆盖结论依据**: 仅对主页面进行抓取与关键词验证，未递进抓取关联页面，不满足 100% 覆盖条件。

---

## 三、已验证通过的事实清单

| 原始对象 | 来源页面 | 来源原文摘录 | 验证动作 | 原始验证结果 | 用途说明 | 资料源 | 验证通过 | 可信度 | 证据等级 |
|---------|---------|-------------|---------|-------------|---------|--------|---------|--------|---------|
| 页面标题标识 | 同上 | OpenClaw Documentation Directory Structure | grep 匹配 | OpenClaw Documentation Directory Structure | 确认文档目录说明归属 | 是 | 是 | 0.99 | 原文 + 实测 |
| 文档根目录路径 | 同上 | /opt/openclaw/docs | grep 匹配 | Root documentation folder: /opt/openclaw/docs | 定位文档存放目录 | 是 | 是 | 0.99 | 原文 + 实测 |
| 本地文档服务启动命令 | 同上 | openclaw docs serve | grep 匹配 | Start local docs server: openclaw docs serve | 启动文档预览服务 | 是 | 是 | 0.99 | 原文 + 实测 |
| 文档服务监听端口 | 同上 | port 1515 | grep 匹配 | Docs listen on port 1515 | 访问本地文档服务 | 是 | 是 | 0.99 | 原文 + 实测 |

---

## 四、候选事实

| 原始对象 | 来源页面 | 原文摘录 | 未验证原因 | 风险说明 | 可信度 | 后续建议 |
|---------|---------|---------|-----------|---------|--------|---------|
| 文档子目录结构 | 同上 | 无细分目录摘录 | 缺少子文件夹说明 | 无法导航完整目录 | 0.80 | 抓取完整目录树 |
| 文档缓存刷新命令用法 | 同上 | openclaw docs refresh | 无参数/示例 | 无法确认执行效果 | 0.75 | 提取命令详细用法 |
| 文档服务访问地址 | 同上 | 无完整 URL | 仅知端口不知主机 | 无法直接访问 | 0.70 | 抓取完整访问地址 |

---

## 五、Gene 固化资产

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_docs_dir_title","name":"文档目录说明标题","description":"该页面为 OpenClaw 文档目录结构官方说明","validate_command":"curl -s https://docs.openclaw.ai/start/docs-directory | grep \"OpenClaw Documentation Directory Structure\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_docs_root_path","name":"OpenClaw 文档根目录","description":"OpenClaw 文档根目录位于 /opt/openclaw/docs","validate_command":"curl -s https://docs.openclaw.ai/start/docs-directory | grep \"/opt/openclaw/docs\"","confidence":0.99,"gep_version":"v1.0.0"}
```

```json
{"asset_type":"Gene","asset_id":"gene_openclaw_docs_serve_cmd","name":"本地文档服务启动命令","description":"使用 openclaw docs serve 启动本地文档服务","validate_command":"curl -s https://docs.openclaw.ai/start/docs-directory | grep \"openclaw docs serve\"","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 六、Capsule 固化资产

```json
{"asset_type":"Capsule","asset_id":"capsule_openclaw_docs_dir_verify","name":"文档目录页面校验","trigger_signal":"openclaw:start:docs-directory:verify","executable_code":"curl -s https://docs.openclaw.ai/start/docs-directory | grep -q \"OpenClaw Documentation Directory Structure\" && echo \"docs_dir_page_ok\"","description":"验证文档目录说明页面可访问性","confidence":0.99,"gep_version":"v1.0.0"}
```

---

## 七、进化蒸馏成果

```json
{"chain_id":"openclaw_distill_docs_directory_20260422","distilled_skill":"文档页面识别、根目录提取、服务命令提取、监听端口提取","execution_threshold":3,"current_execution_count":3,"confidence_summary":{"min":0.99,"max":0.99,"avg":0.99},"distillation_status":{"已完成蒸馏部分":"文档标识、根目录路径、启动命令、监听端口","候选但未蒸馏部分":"子目录结构、缓存刷新用法、完整访问地址","因证据不足被剔除部分":"无"}}
```

---

## 八、真实性与可信度评估报告

- **有原文支持**: 页面标题、文档根目录、本地服务命令、监听端口、缓存刷新命令
- **有实测支持**: curl 抓取、grep 匹配、原始输出逐字保留
- **原文 + 实测**: 页面标题、文档根目录、服务启动命令、监听端口
- **候选事实**: 子目录结构、缓存刷新命令详细用法、完整访问 URL
- **被剔除内容**: 无
- **当前结论边界**: 已提取可直接执行的核心路径与命令，缺少完整目录结构与访问地址，仅支持基础文档服务启停。

---

**入库时间**: 2026-04-22 01:05 GMT+8  
**Git 状态**: 待提交
