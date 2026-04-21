# 2026-03-21 Control UI Token 配置事故

**創建時間:** 2026-03-21 09:40  
**狀態:** ⚠️ 已恢復但未解決（臨時方案）  
**嚴重程度:** 🔴 高（導致 Control UI 無法連接約 20 分鐘）

---

## 事故經過

### 起因

用戶提供 Serper.dev API Key (`01529847d4aa3cf47b86ca87d28519110db06390`)，目的是配置 Serper 搜索技能。

### 錯誤操作

| 時間 | 操作 | 問題 |
|------|------|------|
| 09:05 | AI 將 Serper Key 配置到 `gateway.auth.token` | ❌ **錯配配置項** |
| 09:08 | Gateway 重啟，使用新 Token | ❌ Control UI 仍用舊 Token |
| 09:14 | 用戶發現 Control UI 無法連接 | 🔴 事故暴露 |
| 09:17 | AI 恢復舊 Token (`fdf1ad31d55d3141e9b62cfaadf8420d`) | ❌ 未配置 `gateway.remote.token` |
| 09:19-09:40 | 多次重啟失敗，Token 驗證持續失敗 | 🔴 CLI 與 Gateway Token 不匹配 |

### 根本原因

1. **AI 誤解用戶意圖** - 將 Serper API Key 誤認為 Control UI Token
2. **配置不完整** - 只修改 `gateway.auth.token`，未同步 `gateway.remote.token`
3. **未驗證即交付** - 配置後未確認 Control UI 可正常連接

---

## 最終解決方案

**完成時間:** 2026-03-21 12:21

```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "fftVY5aYnA4Aymsd+SZjFZNeqRFJzyV/B/Y3g10dMSpCTdx/1i6/84rQcOvJ31PTp9DCIodbhO2HuT0fd8SLJA=="
    },
    "remote": {
      "token": "fftVY5aYnA4Aymsd+SZjFZNeqRFJzyV/B/Y3g10dMSpCTdx/1i6/84rQcOvJ31PTp9DCIodbhO2HuT0fd8SLJA=="
    }
  }
}
```

**狀態:** ✅ 完全恢復，用戶已生成並使用新的安全 Token

---

## 待解決事項

### 1. 分離配置（優先級：高）

- [x] 恢復 Control UI Token 為原值 (`fdf1ad31d55d3141e9b62cfaadf8420d`) → ✅ 用戶已生成新 Token
- [x] 正確配置 Serper API Key 到 Serper skill → ✅ 已完成（2026-03-21 12:25）
- [x] 通知用戶在 Control UI 界面更新 Token → ✅ 已完成

### 2. 訪問地址錯誤（新增）

- [x] 確保用戶知道使用公網 IP `47.104.30.181` 而非內網 IP `172.19.12.252` → ✅ 已解決

### 2. Serper 技能配置

- [ ] 將 `01529847d4aa3cf47b86ca87d28519110db06390` 配置到 Serper skill
- [ ] 記錄到 `TOOLS.md`
- [ ] 測試 Serper 搜索功能

### 3. 流程改進

- [ ] 配置敏感信息前必須確認用途
- [ ] 配置後必須驗證功能可用性
- [ ] 建立配置檢查清單

---

## 教訓

| 教訓 | 改進措施 |
|------|---------|
| **不確認用途就配置** | 配置前必須問：這個 Key 用於什麼？ |
| **配置不完整** | 修改 `auth.token` 必須同步 `remote.token` |
| **未驗證即交付** | 配置後必須測試：Control UI 能連接嗎？ |
| **混淆不同系統的密鑰** | 建立密鑰分類：API Key ≠ UI Token |
| **給出內網 IP 而非公網 IP** | 提供訪問地址時必須說明：內網 vs 公網 |

---

## 相關文件

- 配置文件：`/home/admin/.openclaw/openclaw.json`
- 原 Control UI Token: `fdf1ad31d55d3141e9b62cfaadf8420d`
- Serper API Key: `01529847d4aa3cf47b86ca87d28519110db06390`

---

**備註:** 此事故目前使用臨時方案（Serper Key 作為 Control UI Token），需盡快分離配置。
