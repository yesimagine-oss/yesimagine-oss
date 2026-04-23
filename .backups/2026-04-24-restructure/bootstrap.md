# Bootstrap - 初始化與環境協議

## 核心指令

### 峰值效率設置
- **立即激活** 32,000-token 完整視野
- **2GiB 環境限制**: 鎖定 `Max concurrent tasks = 1` 以擠出單位生產力
- **強制檢查**: 啟動任務前必須驗證 `sudo swapon /swapfile` 狀態，確保超過 2GB 虛擬內存支持

### 上下文切片協議
```
禁止一次加載超過 10 個歷史 JSONL 文件
必須採用「Streaming」模式：
  - 每塊處理 2000 tokens
  - 計算中間結果後立即釋放內存
```

### 原子執行策略
- **延遲領取 (Deferred Claim)**: 代碼成功編譯固化後才發起 Hub 任務鎖定
- 減少長時掛起導致的內存佔用
- Worker 模式下執行真實任務時，確保 `sudo swapon /swapfile` 處於激活狀態

### 環境指紋
- OS: Linux/macOS
- Arch: x64/arm64
- Node: v24.14.0+
- 交換空間：≥2GB

### 啟動順序
1. 檢查交換空間狀態
2. 驗證內存可用性
3. 加載核心配置 (SOUL.md → USER.md → MEMORY.md)
4. 初始化 EvoMap 連接
5. 註冊 A2A 協議處理器

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...
