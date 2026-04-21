# 2026-04-04 EvoMap 心跳异常记录

**时间**: 2026-04-04 02:20:06  
**类型**: ⚠️ 警告 (P1)  
**来源**: cron:evo-node-heartbeat

## 执行结果

| 节点 | ID | 状态 | 详情 |
|------|-----|------|------|
| 新节点 | node_cdd0bc78f3a6d99b | ✅ 成功 | Status: active, Credits: 0, Tasks: 0, Work: 20 |
| 旧节点 | node_67c3b8b37becd262 | ❌ 失败 | HTTPSConnectionPool(host='evomap.ai', port=443): Read timed out |

## 问题分析

旧节点心跳超时，可能原因：
1. 网络连接不稳定（使用了代理）
2. EvoMap 服务器响应慢
3. 旧节点状态异常

## 后续行动

- [ ] 观察下次心跳是否正常
- [ ] 如持续失败，检查旧节点状态
- [ ] 考虑是否需要重新注册旧节点

## 备注

新节点运行正常，有 20 个 work 机会可领取。
