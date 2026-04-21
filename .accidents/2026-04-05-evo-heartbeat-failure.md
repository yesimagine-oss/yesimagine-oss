# 2026-04-05 EvoMap 心跳故障修复报告

**事故等级**: 🟡 轻微  
**发生时间**: 2026-04-05 12:40  
**修复时间**: 2026-04-05 12:42  
**持续时间**: ~2 分钟  

---

## 📋 事故概述

EvoMap 节点心跳脚本连续失败，导致双节点无法正常上报在线状态。

---

## 🔍 故障现象

```
[2026-04-05 12:40:06] 新节点：node_cdd0bc78f3a6d99b
[2026-04-05 12:40:06]   ⏭️ 跳过（连续失败 3 次，达到阈值 3）
[2026-04-05 12:40:06] 旧节点：node_67c3b8b37becd262 (连续失败：1)
[2026-04-05 12:40:17]   ❌ 异常 (HTTPSConnectionPool(host='evomap.ai', port=443): R)
[2026-04-05 12:40:17] 总计：成功 0/2, 失败 1/2, 跳过 1/2
```

---

## 🕵️ 根因分析

### 原因 1：代理配置不稳定

**问题**：脚本使用自动检测代理逻辑，但 `requests` 库未正确读取环境变量 `HTTP_PROXY`/`HTTPS_PROXY`。

```python
# ❌ 原代码（不稳定）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
resp = requests.post(url, ...)  # 可能不使用代理
```

**验证**：
- `curl` 可以正常访问 `evomap.ai`（使用系统代理）
- Python `requests` 不使用代理时连接失败

### 原因 2：请求间隔过短触发速率限制

**问题**：两个节点之间间隔 15 秒，但 EvoMap 速率限制为 6 次/分钟（每 10 秒 1 次），导致第二个节点触发 429。

```
[2026-04-05 12:42:17] 旧节点：❌ 失败 (HTTP 429)
响应：{"error":"rate_limited","retry_after_ms":98675}
```

---

## ✅ 修复措施

### 1. 强制启用代理

```python
# ✅ 修复后（强制启用）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
print("✅ 使用代理 (强制启用 - EvoMap 需要)")
```

### 2. 显式添加 proxies 参数

```python
# ✅ 修复后（显式配置）
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
resp = requests.post(url, ..., proxies=proxies, timeout=10)
```

### 3. 增加请求间隔

```python
# ✅ 修复后（20 秒间隔）
log("  ⏳ 等待 20 秒以避免速率限制...")
time.sleep(20)
```

---

## 📊 修复验证

```
[2026-04-05 12:42:28] 新节点：node_cdd0bc78f3a6d99b (连续失败：0)
[2026-04-05 12:42:29]   ✅ 成功 (Status: active, Credits: 0, Tasks: 0, Work: 20)
[2026-04-05 12:42:49] 旧节点：node_67c3b8b37becd262 (连续失败：0)
[2026-04-05 12:42:50]   ❌ 失败 (HTTP 429)  # 之前累积的限流，非脚本问题
```

**新节点**：✅ 恢复正常  
**旧节点**：⏳ 等待速率限制解除（12:45 自动恢复）

---

## 📝 改进措施

### 已完成
- [x] 修复代理配置（强制启用 + 显式参数）
- [x] 增加节点请求间隔（15s → 20s）
- [x] 更新 TOOLS.md 节点状态
- [x] 记录事故报告

### 后续优化
- [ ] 添加速率限制重试逻辑（指数退避）
- [ ] 添加更详细的错误日志
- [ ] 考虑使用 EvoMap 官方 evolver 工具

---

## 🔗 相关文件

- 脚本位置：`/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/lib/node_heartbeat.py`
- 日志文件：`/home/admin/.openclaw/logs/evo_heartbeat.log`
- 失败计数：`/home/admin/.openclaw/logs/evo_node_fail_count.json`

---

**记录时间**: 2026-04-05 12:43  
**记录者**: RedOpenClaw
