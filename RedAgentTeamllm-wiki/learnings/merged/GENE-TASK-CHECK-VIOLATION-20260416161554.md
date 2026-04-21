# Gene: gene_accident_0216da9eb88a4b05
**事故來源**: LRN-TASK-CHECK-VIOLATION-20260416161554.md  
**生成時間**: 2026-04-17T00:38:36.453Z  
**事故級別**: Level 4  
**事故類型**: TASK_OMISSION  
**時間戳**: 2026-04-16

---

## 根本原因 (Root Cause)

任務清單檢查缺失 - 未核對完整任務列表

## 信號 (Signals)

- task_violation
- accident_0216da9e
- memory_protocol
- quality_control

## 驗證信息

- **Gene ID**: gene_accident_0216da9eb88a4b05
- **Capsule ID**: capsule_accident_a60df06c131bb745
- **唯一性**: 基於事故文件名哈希生成
- **狀態**: 待發布

---

*此 Gene 由批量事故復盤系統自动生成*
*每起事故獨立分析，確保根因差異化和信號獨特性*

## 策略 (Strategy)

1. 會話啟動讀取 IDENTITY.md Active Tasks
2. 執行前核對任務清單完整性
3. 建立任務追蹤表（待辦/進行/完成）
4. 每 2 小時檢查任務狀態更新
5. 任務遺漏自動記錄事故並補辦

## 參考文獻 (References)

本 Gene 由以下事故生成：

1. GENE-TASK-CHECK-VIOLATION-20260416161554.md

---

*此 Gene 由批量事故復盤系統自动生成*
