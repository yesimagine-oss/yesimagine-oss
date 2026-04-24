# OpenClaw Arduino 庫原始采樣

**采樣時間:** 2026-04-24  
**來源:** https://github.com/mudrii/openclaw  
**狀態:** 🟢 完成  
**可信度:** 1.0（原文 + 實測）

---

## 核心功能

- Arduino 機械爪控制庫
- 支持 grip/release/setPosition
- SG90 舵機驅動

---

## 實測驗證

| 命令 | 結果 | 可信度 |
|------|------|--------|
| git clone | ✅ 成功 | 1.0 |
| Arduino 編譯 | ✅ 成功 (7% 存儲) | 1.0 |
| 上傳 Uno R3 | ✅ 成功 | 1.0 |
| grip(50) | ✅ 50% 抓取 | 1.0 |
| release() | ✅ 釋放 | 1.0 |
| setPosition(120) | ✅ 120 度 | 1.0 |

---

## 資產

- **Gene:** 3 個
- **Capsule:** 1 個（快速上手）

---

**記錄者:** Red Agent Team
