---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Redagentteamllm Wiki 規範整理報告  20260414
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
# RedAgentTeamllm-wiki 規範整理報告

**整理日期:** 2026-04-14 10:02 GMT+8  
**整理範圍:** RedAgentTeamllm-wiki 知識庫  
**狀態:** ✅ 完成

---

## 📊 知識庫現狀

| 指標 | 數值 |
|------|------|
| **總文件數** | 785 個 .md |
| **總大小** | ~170MB |
| **目錄數** | ~40 個 |
| **最大目錄** | gmail/ (118MB) |

---

## 📂 目錄結構

```
RedAgentTeamllm-wiki/
├── accidents/           # 事故記錄
├── AGENTS.md            # Agent 配置
├── backup/              # 備份
├── CLAUDE.md            # Claude 配置
├── .evolution/          # Evolver 進化
├── index.md             # 索引
├── .ingest_state.json   # 知識攝取狀態
├── learnings/           # 學習記錄
├── log.md               # 日誌
├── logs/                # 日誌目錄
├── .migration/          # 遷移相關
├── protocols/           # 協議
├── raw/                 # 原始資料
├── reports/             # 報告
├── schema/              # 架構
├── scripts/             # 腳本
└── wiki/                # 知識庫主體
```

---

## 📚 wiki/ 結構

```
wiki/
├── accidents/           # 事故記錄
├── agent-browser-study/ # agent-browser 研究
├── ai-media-project/    # AI 自媒體項目
├── analysis/            # 分析報告
├── archive/             # 歸檔
├── assets/              # 資產
├── collections/         # 收藏
├── concepts/            # 概念
├── design/              # 設計
├── docker/              # Docker 知識
├── docs/                # 文檔
├── douyin-knowledge/    # 抖音知識
├── email-monitor/       # 郵件監控
├── entities/            # 實體頁面
├── evolver/             # Evolver
├── evomap/              # EvoMap (1.2MB)
│   ├── 01-平台概览
│   ├── 02-GEP-协议
│   ├── 03-经济系统
│   ├── 04-技术实现
│   ├── 05-实战指南
│   ├── 06-高级主题
│   ├── 07-风险与安全
│   ├── 08-资源与工具
│   ├── 09-实战案例
│   ├── 10-补充文档
│   ├── 11-进阶内容
│   ├── 12-终极扩展
│   ├── 13-补充完善
│   ├── 14-深度扩展
│   ├── 15-高级扩展
│   ├── 16-终极完善
│   ├── 17-最终完善
│   ├── 18-终极扩展
│   ├── 19-集成指南 ✅ 新增
│   ├── 20-变现方案 ✅ 新增
│   └── 21-Blog 学习 ✅ 新增
├── evomap-project/      # EvoMap 項目
├── evomap-workbench/    # EvoMap WorkBench
├── gmail/               # Gmail (118MB)
├── instreet/            # InStreet
├── instreet-serial/     # InStreet 系列
├── knowledge-base/      # 知識庫
├── learning/            # 學習
├── learnings/           # 學習記錄
├── llm-wiki/            # LLM Wiki
├── memory/              # 記憶
├── nodejs/              # Node.js
├── projects/            # 項目
├── python/              # Python
├── reports/             # 報告
├── serper/              # Serper
├── skills/              # Skills (32MB)
├── sources/             # 來源
├── systems/             # 系統
├── tools/               # 工具
└── index.md             # 主索引
```

---

## 📋 核心規範文件

### 1. AGENTS.md (Agent 運行準則)

```markdown
# Agent 运行准则
所属团队：RedAgent Team
知识库路径：./llm-wiki
协同签名：DouB for Red

1. 最高优先级：保护 llm-wiki 资产完整性。
2. 只新增，不覆盖、不删除原有内容。
3. 所有操作写入 log.md。
4. 与 DouB 协同工作，保持统一行为。
5. 禁止擅自修改关联信息。
```

### 2. CLAUDE.md (CLAUDE 行為規範)

```markdown
# CLAUDE 行为规范
归属：RedAgent Team 私有资产
关联节点：node_cdd0bc78f3a6d99b
关联存储：llm-wiki 永久知识库

1. 严禁外泄、篡改、删除任何资产内容。
2. 仅从 llm-wiki 读取知识，禁止幻觉与编造。
3. 不修改、不移动、不破坏目录结构。
4. 回答必须溯源至 raw/ 或 wiki/。
5. 严格服从 RedAgent Team 指令。
```

### 3. index.md (知識庫索引)

- 知識條目總數：162
- Wiki 頁面：44
- Schema 模板：17
- Reports：46
- Protocols：7
- Learnings：5
- Accidents：11

---

## 🔧 專項規範

### EvoMap 相關規範

| 文件 | 說明 |
|------|------|
| `evomap/02-GEP-协议/协议规范.md` | GEP 協議設計規範 |
| `evomap/05-实战指南/资产发布.md` | 資產發布指南 |
| `evomap/17-最终完善/贡献者完整指南.md` | 貢獻者指南 |
| `evomap/20-集成指南/` | AI 集成指南 (9 個) |
| `evomap/20-变现方案/` | 變現方案 (3 個) |
| `evomap/21-Blog 学习/` | 學習報告 (4 個) |

### 工具規範

| 文件 | 說明 |
|------|------|
| `tools/飞书文档创建规范.md` | 飛書文檔創建規範 |
| `tools/README-proxy-manager.md` | 代理管理器說明 |
| `tools/README-daily-brief-v7.md` | 每日簡報規範 |

---

## ✅ 規範執行狀態

| 規範 | 狀態 | 說明 |
|------|------|------|
| **AGENTS.md** | ✅ 遵循 | 保護知識庫完整性 |
| **CLAUDE.md** | ✅ 遵循 | 禁止幻覺與編造 |
| **只新增不覆蓋** | ✅ 遵循 | 所有操作可追溯 |
| **操作寫入 log.md** | ✅ 遵循 | 日誌完整記錄 |
| **溯源至 raw/ 或 wiki/** | ✅ 遵循 | 回答有依據 |

---

## 🎯 待優化項目

| 項目 | 優先級 | 說明 |
|------|--------|------|
| **統一命名規範** | 中 | 部分目錄使用簡體/繁體混用 |
| **清理空目錄** | 低 | 部分目錄為空或已遷移 |
| **合併重複內容** | 中 | 部分主題存在多個版本 |
| **更新過期文檔** | 高 | 部分文檔需要更新 |

---

## 📝 整理建議

### 1. 結構優化

```
建議：
- 統一使用繁體中文目錄名
- 合併 evomap/ 和 evomap-project/
- 清理 gmail/ 中的冗餘文件
```

### 2. 規範文檔集中管理

```
建議創建：
wiki/00-規範與指南/
├── 01-命名規範.md
├── 02-目錄結構規範.md
├── 03-文檔撰寫規範.md
├── 04-版本管理規範.md
└── 05-合併與遷移規範.md
```

### 3. 索引更新

```
建議：
- 更新 index.md 統計數據
- 添加目錄大小統計
- 標記最後更新時間
```

---

## 📊 總結

**RedAgentTeamllm-wiki 規範整理完成。**

**核心規範：**
- ✅ AGENTS.md - Agent 運行準則
- ✅ CLAUDE.md - CLAUDE 行為規範
- ✅ index.md - 知識庫索引

**專項規範：**
- ✅ EvoMap 協議規範
- ✅ 工具使用規範
- ✅ 資產發布規範

**待優化：**
- ⚠️ 統一命名規範
- ⚠️ 清理冗餘內容
- ⚠️ 更新過期文檔

---

**整理人:** Red Agent Team  
**整理日期:** 2026-04-14 10:02 GMT+8  
**狀態:** ✅ 完成

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**


## 相關文檔

- [[WIKI_EVOLUTION_SUMMARY]]
- [[EvoMap Wiki 完整學習與知識庫更新計劃]]
- [[06-go_3layer_wiki_ingest]]
