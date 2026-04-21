---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Infer Multimodal.Gene
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
# Gene: 多模態推理

**Gene ID**: `gene_infer_multimodal`  
**版本**: 1.5.0  
**類別**: 推理引擎  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_infer_multimodal
name: 多模態推理
category: 推理引擎
signals_match:
  - 多模態
  - 圖文
  - 視覺
  - 理解
  - 推理
confidence: 0.96
```

---

## 🎯 摘要

**摘要**: 提供圖文理解、視覺問答等多模態推理能力，支持圖像編碼與文本對齊，實現聯合推理與結構化輸出。

---

## 🧬 策略

**推理策略** (5 步驟，每步>=20 字符):

1. **圖像編碼** - 加載輸入圖像，使用視覺編碼器提取圖像特徵向量
2. **文本對齊** - 將用戶問題文本編碼為 token 序列，與圖像特徵對齊
3. **聯合推理** - 執行多模態聯合注意力計算，生成跨模態理解
4. **結構化輸出** - 生成結構化回應 (文本/坐標/標籤)，支持多種輸出格式
5. **結果驗證** - 驗證輸出合理性，確保視覺理解準確無誤

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
# 1. 圖像理解測試
ollama run llava "描述這張圖片" < image.jpg

# 2. 視覺問答測試
ollama run llava "圖片中有幾個人？" < image.jpg

# 3. OCR 測試
ollama run llava "提取圖片中的文字" < document.png
```

---

## 📝 內容

**詳細內容** (>=100 字符):

多模態推理 Gene 提供視覺 - 語言聯合推理能力。支持圖像描述生成、視覺問答 (VQA)、光學字符識別 (OCR)、圖像分類等任務。使用 LLaVA、bakllava 等多模態模型，結合 CLIP 視覺編碼器與語言模型。圖像編碼後與文本提示對齊，通過交叉注意力機制實現聯合理解。適用於圖像分析、文檔處理、無障礙輔助等場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_infer_text | 文本推理 |
| Capsule | capsule_ollama_multimodal_assistant_v1 | 本地多模態助手膠囊 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[infer-stream.gene]]
- [[infer-text.gene]]
