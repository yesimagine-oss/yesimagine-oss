---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Ollama Install.Gene
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
# Gene: Ollama 跨平台安裝

**Gene ID**: `gene_ollama_install`  
**版本**: 1.5.0  
**類別**: 部署底座  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_ollama_install
name: Ollama 跨平台安裝
category: 部署底座
signals_match:
  - Ollama
  - 安裝
  - 跨平台
  - Docker
  - 部署
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: macOS/Linux/Windows/Docker 一鍵安裝 Ollama 本地大模型引擎，支持多系統自動檢測與最優安裝策略選擇，5 分鐘內完成環境搭建。

---

## 🧬 策略

**安裝策略** (5 步驟，每步>=20 字符):

1. **系統檢測** - 自動識別操作系統類型 (macOS/Linux/Windows) 與架構 (x86/ARM)
2. **獲取安裝包** - 根據系統下載對應官方安裝包或 Docker 鏡像
3. **執行安裝** - 運行安裝腳本或 Docker 容器，配置環境變量
4. **環境校驗** - 驗證 ollama 命令可用，檢查版本號與服務狀態
5. **清理緩存** - 移除臨時下載文件，釋放磁盤空間

---

## 🛡️ 約束

```json
{
  "constraints": {
    "max_files": 5,
    "max_lines": 500,
    "forbidden_paths": [
      "node_modules/",
      ".env",
      ".git/",
      "/etc/",
      "/usr/bin/"
    ],
    "risk_level": "low"
  }
}
```

---

## ✅ 驗證

**驗證命令** (>=3 個):

```bash
# 1. 版本檢查
ollama --version

# 2. 服務狀態檢查
ollama list

# 3. 端口監聽檢查
netstat -tlnp | grep 11434 || lsof -i :11434

# 4. 健康檢查
curl http://localhost:11434/api/tags
```

---

## 📝 內容

**詳細內容** (>=100 字符):

Ollama 跨平台安裝 Gene 提供完整的本地大模型引擎安裝能力。支持 macOS (Homebrew/直接下載)、Linux (systemd/Docker)、Windows (WSL2/直接安裝) 等多種安裝方式。自動檢測系統環境並選擇最優安裝策略，確保 5 分鐘內完成環境搭建。安裝後自動驗證服務可用性，確保 11434 端口正常監聽。本 Gene 為所有 Ollama 相關操作的基礎，必須首先執行。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Capsule | capsule_ollama_oneclick_deploy_v1 | 一鍵部署膠囊 |
| Gene | gene_ollama_start | Ollama 服務啟動 |

---

## 📊 資產 ID

**asset_id**: `sha256:<待計算>` (移除 asset_id 字段後 SHA-256 哈希)

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[ollama-run.gene]]
- [[ollama-start.gene]]
- [[ollama-pull.gene]]
