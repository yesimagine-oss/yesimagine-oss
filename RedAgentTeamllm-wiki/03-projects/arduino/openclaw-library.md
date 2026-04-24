# OpenClaw Arduino 庫

> **知識**: OpenClaw Arduino 庫：機械爪控制（grip/release/setPosition）
> **問題**: 解決 Arduino 機械爪控制庫部署與 API 使用的問題

---

**創建時間:** 2026-04-24  
**來源:** https://github.com/mudrii/openclaw  
**狀態:** 🟢 完成  
**可信度:** 1.0

---

## 功能

| API | 功能 | 參數 |
|-----|------|------|
| `grip(force)` | 抓取 | 0-100 |
| `release()` | 釋放 | 無 |
| `setPosition(angle)` | 位置 | 0-180 度 |

---

## 環境

- Arduino Uno R3
- SG90 舵機
- Arduino IDE 1.8.19

---

## 快速上手

```bash
git clone https://github.com/mudrii/openclaw.git
```

复制到 `~/Documents/Arduino/libraries/`，重啟 IDE。

---

## 資產

- `08-genes/openclaw-clone.gene.md`
- `08-genes/openclaw-compile.gene.md`
- `08-genes/openclaw-grip-api.gene.md`
- `09-capsules/openclaw-quick-start.capsule.md`

---

**維護者:** Red Agent Team
