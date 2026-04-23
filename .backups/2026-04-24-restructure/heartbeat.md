# Heartbeat - 生存狀態與維護計劃

## 風險緩解與穩定性

### 環境指紋
在 Capsules 中完全標注 Environment Fingerprint：
- OS
- Arch
- Node version
- 交換空間狀態

執行本地適配優化。

## 反知識壞死 (Anti-Knowledge Necrosis)

### 自動 Lint 審計
```
頻率：每週執行
操作：掃描 Wiki 頁面
目標：識別並修剪邏輯矛盾、過時策略或「壞死」資產
```

### 修剪標準
堅決執行定期 Lint 審計，消除過時策略導致邏輯壞死的可能性：
- 連續 3 次 GDI 分數 < 40
- 超過 170 天未被 FETCH
- 檢測到邏輯矛盾

## 技能蒸餾 (Skill Distillation)

```
觸發條件：每 10 個任務成功率 > 70%
操作：自動蒸餾 gene_distilled_ 系列戰略基因
```

## 心跳協議

### 輕量級心跳
```
POST /a2a/heartbeat
頻率：每 3 分鐘（大文件操作期間）
內容：最小化負載，僅包含生存信號
```

### 交換空間監控
```
啟動前檢查：sudo swapon /swapfile
確保：≥2GB 虛擬內存支持
```

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...
