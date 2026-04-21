# Evolver 配置文檔

## 安裝狀態

- **版本:** 1.53.0 ✅
- **安裝位置:** `/usr/lib/node_modules/@evomap/evolver`
- **二進制:** `/usr/bin/evolver`
- **安裝日期:** 2026-04-13

## 配置

### 環境變量

```bash
export MEMORY_DIR=/home/admin/.openclaw/workspace/.evolver/memory
```

### 目錄結構

```
/home/admin/.openclaw/workspace/.evolver/
├── memory/          # Evolver 運行時內存目錄
└── evolution.log    # 進化日誌
```

## 權限修復

已修復權限問題：
- `/usr/lib/node_modules/@evomap/evolver/memory` - 777 (全局可寫)
- 用戶級 MEMORY_DIR 已配置到工作區

## 驗證命令

```bash
# 檢查版本
evolver --version

# 測試 fetch 命令
evolver fetch --help

# 測試運行 (自帶記憶體目錄)
MEMORY_DIR=/home/admin/.openclaw/workspace/.evolver/memory evolver --version
```

## 使用示例

### 獲取 Skill

```bash
evolver fetch --skill=capsule_eva_task_quality_metrics_1772250032074_6299
```

### 運行 Evolver

```bash
cd /home/admin/.openclaw/workspace
MEMORY_DIR=/home/admin/.openclaw/workspace/.evolver/memory evolver run
```

### 查看資產日誌

```bash
evolver asset-log --last=10 --json
```

## 安全檢查

- [x] 版本驗證 (1.53.0)
- [x] 權限修復 (memory 目錄可寫)
- [x] 環境變量配置 (MEMORY_DIR)
- [x] 命令測試 (fetch, --version)
- [x] 工作區集成 (.evolver 目錄)

## 更新記錄

| 日期 | 操作 | 說明 |
|------|------|------|
| 2026-04-13 | 安裝 | 全局安裝 @evomap/evolver@1.53.0 |
| 2026-04-13 | 修復 | 創建 memory 目錄並設置權限 |
| 2026-04-13 | 配置 | 設置 MEMORY_DIR 環境變量 |

---

**最後更新:** 2026-04-13 13:15 GMT+8
**狀態:** ✅ 安全可用
