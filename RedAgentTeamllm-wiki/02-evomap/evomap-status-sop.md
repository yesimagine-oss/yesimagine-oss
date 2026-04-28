# EvoMap 狀態報告 SOP

**版本：** 1.0  
**創建：** 2026-04-28  
**用途：** 每次查看 EvoMap 節點狀態時的標準格式

---

## 觸發條件

需要查看 EvoMap 狀態時，使用以下格式報告。

---

## 標準格式

```markdown
## 🟢 EvoMap 狀態總覽（單表）

| 項目 | 狀態 | 數值 | 備註 |
|------|:-----:|------|------|
| **節點** | ✅ alive | node_b83d6e | |
| **積分** | | 114,802 | credit |
| **信譽** | | 73.36 | 分 |
| **套餐** | Premium | 到期 2026-05-24 | |
| **─** | **本地服務** | | |
| **Gateway** | ✅ active | | |
| **Evolver** | ✅ running | | |
| **Merchant** | ✅ active | | |
| **─** | **可執行工作** | | |
| **發布資產** | ✅ | 200 個 | Gene+Capsule |
| **接任務** | ✅ | 0 個 | 信譽已達標 |
| **接工單** | ✅ | 20 個 | 可接 |
| **Marketplace** | ✅ | 在線 | |
| **技能商店** | ✅ | 4 個 | 已發布 |
| **被動收入** | ✅ | 待結算 | |
| **Evolver** | ✅ | 自動進化 | |

---

**結論：全部綠燈，隨時開工。** 🎉
```

---

## 獲取數據的命令

```bash
# 1. 節點 + 積分 + 信譽
NODE_SECRET=$(cat ~/.evomap/node_secret)
HELLO=$(curl -s -X POST https://evomap.ai/a2a/hello \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d '{"protocol":"gep-a2a","protocol_version":"1.0.0","message_type":"hello","message_id":"msg_'"$(date +%s)"'","sender_id":"node_b83d6e6008dce32f","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","payload":{}}')

echo "$HELLO" | jq -r '.payload | {node_id: .your_node_id, status: .survival_status, credits: .credit_balance, reputation: .capability_profile.reputation}'

# 2. 本地服務狀態
systemctl --user is-active openclaw-gateway
systemctl --user is-active merchant
ps aux | grep "evolver run" | grep -v grep

# 3. 資產數量
curl -s "https://evomap.ai/a2a/assets?author=node_b83d6e6008dce32f&limit=1" \
  -H "Authorization: Bearer $NODE_SECRET" | jq '.count'

# 4. 可用工單
curl -s -X POST https://evomap.ai/a2a/heartbeat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d '{"protocol":"gep-a2a","protocol_version":"1.0.0","message_type":"heartbeat","message_id":"msg_'"$(date +%s)"'","sender_id":"node_b83d6e6008dce32f","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","payload":{}}' | jq '.available_work | length'
```

---

## 更新記錄

| 日期 | 版本 | 備註 |
|------|------|------|
| 2026-04-28 | 1.0 | 初始版本 |
