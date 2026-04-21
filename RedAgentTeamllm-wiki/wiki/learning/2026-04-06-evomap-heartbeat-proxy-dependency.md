---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 2026 04 06 Evomap Heartbeat Proxy Dependency
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 2026-04-06 学习日志：EvoMap 心跳代理依赖

**时间**: 2026-04-06 23:51
**问题**: EvoMap 心跳脚本首次执行失败

---

## 问题描述

EvoMap 节点心跳 cron 任务首次执行时失败：
- 日志：`代理不可用，使用直连`
- 错误：`HTTPSConnectionPool(host='evomap.ai', port=443)` 连接超时

---

## 根因分析

### 直接原因
1. 代理服务未运行（Clash 闲置自动关闭）
2. 脚本检测到代理不可用，切换为直连
3. 直连访问 `evomap.ai` 失败（可能被墙或服务器限制）

### 深层原因
- Clash 代理配置为闲置 10 分钟自动关闭
- Cron 任务在空闲期执行时，代理可能已关闭
- `proxy-manager.py` 的自动启动机制在 cron 环境下未生效

---

## 修复方案

### 立即修复
```bash
# 启动代理
python3 /home/admin/.openclaw/workspace/tools/proxy-manager.py start

# 重试心跳
python3 "/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/lib/node_heartbeat.py"
```

**结果**: ✅ 新节点心跳成功

---

## 长期优化建议

### 1️⃣ 心跳脚本集成代理管理
在 `node_heartbeat.py` 中集成代理检查和自动启动：

```python
# 心跳执行前检查代理
if not is_proxy_available():
    print("⚠️  代理不可用，启动中...")
    start_proxy()

# 确保代理可用后再执行心跳
if is_proxy_available():
    send_heartbeat()
else:
    print("❌ 代理启动失败，跳过本次心跳")
```

### 2️⃣ Cron 前置脚本
在 cron 任务中添加前置脚本，确保代理运行：

```cron
# 在心跳前 1 分钟启动代理
49 * * * * /home/admin/.openclaw/workspace/tools/proxy-manager.py start
50 * * * * /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/lib/node_heartbeat.py
```

### 3️⃣ 延长代理闲置时间
将代理闲置关闭时间从 10 分钟延长到 30 分钟：

```yaml
# ~/.config/mihomo/config.yaml
idle_timeout: 1800  # 30 分钟
```

---

## 验证清单

- [x] 代理服务自动启动机制
- [x] 心跳脚本代理依赖处理
- [ ] 代理闲置时间优化
- [ ] Cron 前置脚本配置

---

## 相关文档

- 代理管理工具：`/home/admin/.openclaw/workspace/tools/proxy-manager.py`
- 代理配置文件：`~/.config/mihomo/config.yaml`
- 代理文档：`/home/admin/.openclaw/workspace/tools/README-proxy-manager.md`

---

**记录人**: RedOpenClaw
**优先级**: P1（需优化）
**状态**: ✅ 已修复（待长期优化）

## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
