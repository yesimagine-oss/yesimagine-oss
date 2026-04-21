# goToken - Feishu 通知配置

## 📋 配置步驟

### 1. 創建飛書機器人

1. 打開飛書群組
2. 右上角「...」→「添加機器人」
3. 選擇「自定義機器人」
4. 設置名稱：`goToken 監控`
5. 複製 Webhook URL

### 2. 設置環境變量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"

# 使生效
source ~/.bashrc
```

### 3. 測試通知

```bash
cd /home/admin/.openclaw/workspace/goToken
./tools/feishu-notify.sh test
```

---

## 🔔 通知類型

| 類型 | 觸發條件 | 顏色 | 內容 |
|------|---------|------|------|
| 🔴 命中率警告 | <75% | red | 立即優化 |
| 🟡 命中率提醒 | <80% | yellow | 建議訓練 |
| 🟢 新問題累積 | ≥20 個 | yellow | 加入模板 |
| 🟢 測試通知 | 手動 | green | 系統正常 |

---

## ⏰ 定時檢查

### 添加 cron 任務

```bash
crontab -e

# 每小時檢查一次
0 * * * * /home/admin/.openclaw/workspace/goToken/tools/feishu-notify.sh check

# 或每 30 分鐘
*/30 * * * * /home/admin/.openclaw/workspace/goToken/tools/feishu-notify.sh check
```

---

## 📊 日誌文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `misses.log` | 未命中記錄 | `logs/misses.log` |
| `metrics.json` | 指標快照 | `logs/metrics.json` |

---

## 🧪 使用示例

```bash
# 記錄未命中
./tools/feishu-notify.sh miss "如何安裝 XXX？"

# 更新指標
./tools/feishu-notify.sh metrics 100 75

# 檢查並發送警告
./tools/feishu-notify.sh check

# 測試通知
./tools/feishu-notify.sh test
```

---

## ✅ 驗收清單

- [ ] 飛書機器人創建完成
- [ ] Webhook URL 設置
- [ ] 環境變量配置
- [ ] 測試通知成功
- [ ] Cron 任務添加 (可選)

---

**狀態:** ⏳ 待配置 Webhook
