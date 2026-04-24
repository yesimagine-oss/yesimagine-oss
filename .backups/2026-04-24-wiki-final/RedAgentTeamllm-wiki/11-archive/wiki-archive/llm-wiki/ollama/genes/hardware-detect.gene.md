---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Hardware Detect.Gene
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# Gene: 硬件檢測

**Gene ID**: `gene_hardware_detect`  
**版本**: 1.5.0  
**類別**: 硬件適配  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_hardware_detect
name: 硬件檢測
category: 硬件適配
signals_match:
  - 硬件
  - 檢測
  - GPU
  - AppleSilicon
  - CUDA
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: 自動檢測 CPU/GPU/內存/芯片架構等硬件信息，評估性能並選擇最優推理策略，確保資源最大化利用。

---

## 🧬 策略

**檢測策略** (5 步驟，每步>=20 字符):

1. **系統調用** - 調用系統 API 獲取硬件信息 (CPU 型號、核心數、內存大小)
2. **設備枚舉** - 枚舉 GPU 設備 (NVIDIA/AMD/Apple GPU)，獲取顯存與架構信息
3. **性能評估** - 基於硬件規格評估推理性能，預測 token/s 生成速度
4. **最優策略** - 根據評估結果選擇最優推理策略 (GPU 加速/CPU/量化)
5. **配置生成** - 生成優化配置文件，設置層數、批大小、內存限制等參數

---

## 🛡️ 約束

```json
{
  "constraints": {
    "max_files": 3,
    "max_lines": 400,
    "forbidden_paths": [
      "node_modules/",
      ".env",
      ".git/"
    ],
    "risk_level": "low"
  }
}
```

---

## ✅ 驗證

**驗證命令** (>=3 個):

```bash
# 1. CPU/內存檢測
lscpu | grep -E "Model name|CPU\(s\)" && free -h

# 2. GPU 檢測 (NVIDIA)
nvidia-smi --query-gpu=name,memory.total --format=csv

# 3. Apple Silicon 檢測
system_profiler SPDisplaysDataType | grep -E "Chipset Type|Total Number of Cores"
```

---

## 📝 內容

**詳細內容** (>=100 字符):

硬件檢測 Gene 提供全面的硬件信息採集與分析能力。支持 x86/ARM 架構檢測、NVIDIA/AMD/Apple GPU 識別、內存容量與速度評估。基於檢測結果自動選擇最優推理後端 (CUDA/Metal/CPU)、量化精度 (4bit/8bit/16bit)、批處理大小等參數。性能評估模型預測不同配置下的 token/s 生成速度，輔助用戶選擇最佳配置。適用於自動優化、性能調試、資源監控等場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_apple_silicon_optimize | Apple Silicon 優化 |
| Gene | gene_cuda_optimize | NVIDIA CUDA 優化 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成
