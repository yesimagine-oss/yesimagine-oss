# 自研 · Red AgentTeam Health Check 自动化健康检查系统

**创建时间:** 2026-04-27  
**状态:** 🔴 发现 Evolver 未在运行（待重启）  
**位置:** `05-auto/health-check.sh` + `05-auto/check_hub_credits.py`

---

## 一、背景故事

**问题发现：**

2026-04-27 早上，我们想重启 Evolver，却发现：
- Evolver 进程从 4 月 23 日起就已经停了
- 整整 4 天没有任何通知
- 全靠偶然检查日志才发现

**根源：**
- Evolver 有 systemd 服务，但服务挂了不会自动通知
- 飞书 Webhook 配置了但从来没填（是空的）
- 全靠人工巡查，不可靠

**解决思路：**

复用 goToken 已配置好的飞书 Webhook，写一个健康检查脚本，自动化监控：
1. Evolver 进程是否在跑
2. Hub 心跳是否超时（超过 10 分钟）
3. 积分是否低于阈值

---

## 二、设计决策

### 为什么自己先用，不是直接发布？

| 阶段 | 原因 |
|------|------|
| 自己先用 | 有真实运行环境验证，打磨到稳定再发布 |
| 打磨期 | 确认告警准确、不误报、不漏报 |
| 成熟后 | 再发布成 Hub 资产，有真实案例背书 |

### 为什么不单独建 Webhook？

goToken 已经配好了飞书 Webhook，**复用同一个**，不用多管理一个机器人。

### 为什么不用 systemd 定时器？

systemd 的 `OnUnitActiveSec=5min` 有精度问题，而且重启后不一定立刻执行。用 crontab 更直接可控。

---

## 三、检测逻辑

```
健康检查流程：

1. 检查 Evolver 进程
   └─ pgrep -f "node.*evolver" → 进程是否存在

2. 检查 Hub 心跳年龄
   └─ 读取 .evolver/memory/evolution/evolution_state.json
   └─ 计算 (now_ms - lastRun) / 1000
   └─ > 600 秒 → 告警

3. 检查积分余额
   └─ 发 hello 到 Hub，获取 credit_balance
   └─ < 1000 → 告警

4. 有任何告警 → 发飞书通知
   └─ curl -X POST FEISHU_WEBHOOK
```

---

## 四、部署方式

```bash
# 添加 crontab（每5分钟跑一次）
*/5 * * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/05-auto/health-check.sh

# 查看日志
tail -f /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/health-check.log
```

---

## 五、文件清单

| 文件 | 用途 |
|------|------|
| `05-auto/health-check.sh` | 主脚本，Bash 实现 |
| `05-auto/check_hub_credits.py` | Hub 积分查询 Python 辅助脚本 |
| `07-learnings/sovereign-evolution-Evolver-20260427.md` | Evolver 学习报告 |
| `log/health-check.log` | 运行日志 |

---

## 六、已知问题

| 问题 | 原因 | 状态 |
|------|------|------|
| Evolver 进程未运行 | 旧 PID 492345 已消失，需重新启动 | 🔴 待处理 |
| health-check.sh 进程检测逻辑待验证 | pgrep 在无进程时行为需确认 | ⚠️ 待确认 |
| 心跳 age 计算依赖 state 文件 | 如果文件不存在会返回 9999 | ✅ 已处理 |

---

## 七、下一步计划

- [ ] 重启 Evolver（`evolver run --loop`）
- [ ] 确认 health-check.sh 能正确检测到进程
- [ ] 配置 crontab 自动化
- [ ] 稳定运行 1 周后发布到 Hub

---

**制作人:** RedOpenClaw  
**最后更新:** 2026-04-27 09:49 GMT+8
