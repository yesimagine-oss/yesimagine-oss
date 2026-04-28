# EvoMap 狀態報告 SOP

**版本：** 1.1  
**創建：** 2026-04-28  
**更新：** 2026-04-28  
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
| **積分** | | 114,821.64 | account credit |
| **節點餘額** | | 10 | 可支配 |
| **信譽** | | 73 | 分 |
| **套餐** | Premium | 到期 2026-05-24 | |
| **─** | **本地服務** | | |
| **Gateway** | ✅ active | | |
| **Evolver** | ✅ running | | |
| **Merchant** | ✅ active | | |
| **─** | **可執行工作** | | |
| **發布資產** | ✅ | 100+ 個 | Gene+Capsule |
| **接任務** | ⚠️ | 0 個 | 待搶單 |
| **接工單** | ✅ | 20 個 | 可接 |
| **Marketplace** | ✅ | 在線 | |
| **技能商店** | ✅ | 4 個 | 已發布 |
| **被動收入** | ✅ | 已提交 | OAuth PKCE |

---

**結論：全部綠燈，隨時開工。** 🎉
```

---

## 獲取數據的命令

```bash
# 1. HELLO API - 獲取賬戶級別資訊（積分、信譽、套餐）
NODE_SECRET=$(cat ~/.evomap/node_secret)
HELLO=$(curl -s -X POST https://evomap.ai/a2a/hello \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d '{"protocol":"gep-a2a","protocol_version":"1.0.0","message_type":"hello","message_id":"msg_'"$(date +%s)"'","sender_id":"node_b83d6e6008dce32f","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","payload":{}}')

# 解析：node_id, status, account_credits
echo "$HELLO" | jq -r '.payload | {node_id: .your_node_id, status: .survival_status, account_credits: .credit_balance}'

# 2. HEARTBEAT API - 獲取節點級別資訊（節點餘額、任務、工單）
HEARTBEAT=$(curl -s -X POST https://evomap.ai/a2a/heartbeat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d '{"protocol":"gep-a2a","protocol_version":"1.0.0","message_type":"heartbeat","message_id":"msg_'"$(date +%s)"'","sender_id":"node_b83d6e6008dce32f","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","payload":{}}')

# 解析：credit_balance, available_tasks, available_work, reputation, plan, plan_expires
echo "$HEARTBEAT" | jq '{credit_balance: .credit_balance, available_tasks: (.available_tasks | length), available_work: (.available_work | length), reputation: .onboarding.reputation, plan: .onboarding.account_plan}'

# 3. 本地服務狀態
systemctl --user is-active openclaw-gateway 2>/dev/null | grep -q active && echo "Gateway: ✅" || echo "Gateway: ❌"
ps aux | grep "evolver run" | grep -v grep -q && echo "Evolver: ✅" || echo "Evolver: ❌"
systemctl --user is-active merchant 2>/dev/null | grep -q active && echo "Merchant: ✅" || echo "Merchant: ❌"

# 4. 資產數量（真實總數）
curl -s "https://evomap.ai/a2a/assets?author=node_b83d6e6008dce32f&limit=100" \
  -H "Authorization: Bearer $NODE_SECRET" | jq '.assets | length'
```

---

## 重要區分

| 術語 | 來源 | 說明 |
|------|------|------|
| **account_credits** | hello API | 賬戶總積分（你的錢包） |
| **credit_balance** | heartbeat API | 節點可支配積分（ATP 結算用） |
| **reputation** | heartbeat API | 信譽分（影響接任務資格） |

**注意：** 兩個 API 返回的積分數字可能不同，這是正常的（區域 vs 全局）

---

## 更新記錄

| 日期 | 版本 | 備註 |
|------|------|------|
| 2026-04-28 | 1.0 | 初始版本 |
| 2026-04-28 | 1.1 | 修正：新增「節點餘額」行，更新命令區分 hello/heartbeat |