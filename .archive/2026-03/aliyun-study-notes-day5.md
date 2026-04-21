# 📚 阿里雲工作臺學習筆記 - Day 5

**學習時間:** 2026-03-18  
**學習主題:** 百煉控制台（AI 大模型服務）  
**參考資料:** 
- 阿里雲百煉官方文檔
- `aliyun-enterprise-ops.md`

---

## Day 5 - 2026-03-18：百煉控制台（AI）

### 1. 百煉控制台介紹

#### 1.1 什麼是阿里雲百煉

**阿里雲百煉（Model Studio）** 是一站式大模型開發與應用平台，集成了：
- 通義千問（Qwen）全系列模型
- 主流第三方大模型（DeepSeek、Kimi、GLM 等）
- 兼容 OpenAI API 規範
- 可視化應用構建能力

**核心功能:**
```
模型服務
├─ 千問系列（Max/Plus/Flash/Coder）
├─ 第三方模型（DeepSeek、Kimi、GLM）
├─ 多模態能力（文本、視覺、圖像、視頻、語音）
└─ 細分領域模型（翻譯、法律、角色扮演等）

應用構建
├─ 智能體應用（單 Agent）
├─ 工作流應用（流程編排）
├─ 高代碼應用（Python 項目部署）
└─ 知識庫（RAG）

模型調優
├─ 微調（SFT、CPT、DPO）
├─ 部署（專享推理服務）
└─ 評測（人工、自動、基線）
```

#### 1.2 訪問控制台

**控制台地址:**
- **中國內地（北京）**: https://bailian.console.aliyun.com/
- **美國（弗吉尼亞）**: https://modelstudio.console.aliyun.com/us-east-1
- **國際（新加坡）**: https://modelstudio.console.aliyun.com/?tab=doc#/doc/?type=model&url=2840914

**注意:**
- 不同地域的 API Key 不通用
- 不同地域的 Base URL 不通用
- 選擇鄰近地域可降低網絡延遲

---

### 2. API Key 管理

#### 2.1 創建 API Key

**實操步驟:**
```
1. 訪問：https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key
2. 點擊「創建新的 API-KEY」
3. 填寫密鑰名稱（例如：myapp-production）
4. 複製並保存 API Key（僅顯示一次！）
5. 設置環境變量：
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

**安全建議:**
- ✅ API Key 僅在創建時顯示一次，務必立即保存
- ✅ 使用環境變量存儲，不要硬編碼在代碼中
- ✅ 定期輪換 API Key（建議每 90 天）
- ✅ 為不同環境創建不同的 Key（開發/測試/生產）
- ❌ 不要將 API Key 上傳到 Git 倉庫

#### 2.2 API Key 管理最佳實踐

**多環境管理:**
```bash
# .env.development
DASHSCOPE_API_KEY=sk-dev-xxxxxxxx

# .env.production
DASHSCOPE_API_KEY=sk-prod-xxxxxxxx

# 代碼中使用
import os
from dotenv import load_dotenv

load_dotenv('.env.production')  # 或 .env.development
api_key = os.getenv('DASHSCOPE_API_KEY')
```

**刪除 API Key:**
```
1. API-KEY 管理頁面
2. 找到目標 Key
3. 點擊「刪除」
4. 確認刪除

注意：刪除後該 Key 立即失效，所有使用該 Key 的應用將無法調用
```

---

### 3. 模型調用

#### 3.1 兼容 OpenAI API

**Python 示例:**
```python
import os
from openai import OpenAI

# 不同地域的 base_url
# 華北 2（北京）: https://dashscope.aliyuncs.com/compatible-mode/v1
# 美國（弗吉尼亞）: https://dashscope-us.aliyuncs.com/compatible-mode/v1
# 新加坡: https://dashscope-intl.aliyuncs.com/compatible-mode/v1

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[{'role': 'user', 'content': '你是誰？'}]
)

print(completion.choices[0].message.content)
```

**Node.js 示例:**
```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.5-plus",
        messages: [{ role: "user", content: "你是誰？" }],
    });
    console.log(completion.choices[0].message.content);
}

main();
```

**curl 示例:**
```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [
      {
        "role": "user",
        "content": "你是誰？"
      }
    ]
  }'
```

#### 3.2 千問系列模型選擇

| 模型 | 特點 | 適用場景 | 價格（參考） |
|------|------|---------|-------------|
| **千問 Max** | 效果最好，處理複雜任務 | 多步驟任務、高質量要求 | 高 |
| **千問 Plus** | 效果、速度、成本均衡 | 多數場景的推薦選擇 | 中 |
| **千問 Flash** | 高性价比、低延遲 | 簡單任務、快速響應 | 低 |
| **千問 Coder** | 擅長代碼生成與理解 | 編程輔助、代碼審查 | 中 |

**推薦選擇:**
```yaml
日常對話/內容創作：千問 Plus
複雜推理/多步驟任務：千問 Max
簡單問答/快速響應：千問 Flash
代碼相關任務：千問 Coder
```

#### 3.3 從 OpenAI 遷移

**代碼遷移示例:**
```python
# OpenAI 原始代碼
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1",  # ← 修改這裡
)

# 阿里雲百煉代碼
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # ← 修改這裡
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # ← 修改這裡
)

# 模型名稱也需要修改
# "gpt-4" → "qwen3.5-plus"
# "gpt-3.5-turbo" → "qwen3.5-flash"
```

---

### 4. 計費與用量

#### 4.1 計費模式

**按量付費:**
```
計費公式：費用 = Token 數量 × 單價

輸入 Token：提示詞（prompt）的 Token 數
輸出 Token：模型生成內容的 Token 數

出賬時間：調用後約 1 小時出賬
扣費方式：自動從阿里雲賬戶餘額扣除
```

**參考價格（以千問系列為例）:**
| 模型 | 輸入價格 | 輸出價格 | 單位 |
|------|---------|---------|------|
| 千問 Max | ¥0.04 | ¥0.12 | 每 1K Token |
| 千問 Plus | ¥0.004 | ¥0.012 | 每 1K Token |
| 千問 Flash | ¥0.0005 | ¥0.0015 | 每 1K Token |
| 千問 Coder | ¥0.004 | ¥0.012 | 每 1K Token |

**Token 估算:**
```
1 個漢字 ≈ 1.5-2 個 Token
1 個英文單詞 ≈ 1-1.5 個 Token

示例：
- 1000 字的中文文章 ≈ 1500-2000 Token
- 1000 詞的英文文章 ≈ 1000-1500 Token
```

#### 4.2 新人免費額度

**免費額度詳情:**
```
適用對象：新開通用戶
額度和限：北京地域專屬
有效期：開通後一定期限內（具體見官網）
使用範圍：模型調用體驗

額度用完後：
- 自動轉為按量付費
- 可開啟「免費額度用完即停」避免扣費
```

**開啟「免費額度用完即停」:**
```
1. 百煉控制台 → 模型體驗
2. 選擇目標模型
3. 點擊「免費額度」設置
4. 開啟「用完即停」開關
5. 確認開啟

效果：免費額度耗盡後，服務自動停止，不會轉為付費
```

#### 4.3 查看賬單與用量

**消費明細:**
```
1. 訪問：https://usercenter2.aliyun.com/finance/expense-report/expense-detail
2. 選擇賬單週期
3. 查看明細：
   - 按產品分類（百煉）
   - 按實例分類
   - 按地域分類
```

**模型監控:**
```
1. 百煉控制台 → 模型監控
2. 選擇地域
3. 設置查詢條件（時間範圍、模型）
4. 查看統計：
   - 調用量（請求次數）
   - Token 消耗（輸入/輸出）
   - 成功率
   - 平均延遲
```

**Coding Plan 用量:**
```
1. 訪問：https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan
2. 查看當前套餐
3. 查看請求消耗情況

Coding Plan 特點:
- 固定月費
- 提供月度請求額度
- 無按量扣費風險
- 專用於 AI 編碼工具
```

#### 4.4 成本控制策略

**避免意外扣費:**
```bash
# 1. 刪除 API Key（徹底阻斷）
# 百煉控制台 → API-KEY → 刪除所有 Key

# 2. 停止所有調用
# - 停止應用程序
# - 停止智能體/工作流
# - 排查定時任務和後台進程

# 3. 清理計費資源
# - 刪除不再使用的知識庫
# - 下線按算力計費的部署實例

# 4. 開啟「免費額度用完即停」（新用戶）

# 5. 設置高額消費預警
# 費用中心 → 高額消費預警 → 設置閾值

# 6. 訂閱 Coding Plan（AI 編碼套餐）
# 固定月費，無按量扣費風險
```

**成本優化建議:**
```yaml
模型選擇:
  簡單任務 → 千問 Flash（最便宜）
  一般任務 → 千問 Plus（性價比高）
  複雜任務 → 千問 Max（效果好）

請求優化:
  精簡提示詞 → 減少輸入 Token
  設置 max_tokens → 限制輸出長度
  使用緩存 → 避免重複請求

監控預警:
  設置每日預算上限
  配置異常消費告警
  定期審查賬單
```

---

### 5. 模型部署

#### 5.1 部署類型

**共享推理:**
```
特點：
- 多租戶共享資源
- 按 Token 計費
- 適合低並發場景
- 無需管理基礎設施

適用：
- 開發測試
- 低並發應用
- 成本敏感場景
```

**專享部署:**
```
特點：
- 獨享計算資源
- 按時長/包月計費
- 高並發、低延遲
- 支持自定義配置

適用：
- 生產環境
- 高並發應用
- 對延遲敏感場景

計費方式:
- 按時長計費（靈活）
- 包月計費（優惠）
- 按 Token 量計費
```

#### 5.2 部署步驟

**部署預置模型:**
```
1. 百煉控制台 → 模型部署
2. 點擊「創建部署」
3. 選擇模型（千問系列/第三方模型）
4. 選擇部署類型（共享/專享）
5. 配置實例規格（專享部署）
6. 設置實例數量
7. 確認部署
8. 獲取部署地址和 Key
```

**部署微調模型:**
```
1. 完成模型微調
2. 微調任務詳情 → 部署
3. 選擇部署配置
4. 確認部署
5. 獲取專屬推理地址
```

---

### 6. 應用構建

#### 6.1 智能體應用（單 Agent）

**適用場景:**
- 智能客服
- 個人助手
- 知識庫問答
- 內容創作

**創建步驟:**
```
1. 百煉控制台 → 應用構建 → 創建應用
2. 選擇「智能體應用」
3. 配置基礎信息：
   - 應用名稱
   - 應用描述
   - 頭像
4. 選擇模型（千問 Plus 推薦）
5. 配置提示詞（System Prompt）
6. 配置知識庫（可選）
7. 配置插件（可選）
8. 測試並發布
```

**提示詞示例:**
```
你是一名專業的客服助手，負責回答用戶關於產品的問題。

要求：
1. 語氣友好、專業
2. 回答準確、簡潔
3. 不確定的內容如實告知
4. 引導用戶提供更多信息

產品信息：
- 產品 A：價格 ¥999，特點...
- 產品 B：價格 ¥1999，特點...
```

#### 6.2 工作流應用（流程編排）

**適用場景:**
- 多步驟任務
- 複雜業務流程
- 需要人工審核

**可視化編排:**
```
開始節點
   ↓
輸入處理（解析用戶輸入）
   ↓
條件判斷（意圖識別）
   ↓
┌──────┼──────┐
↓      ↓      ↓
查詢  下單  投訴
節點  節點  節點
↓      ↓      ↓
└──────┼──────┘
   ↓
輸出處理（格式化回复）
   ↓
結束節點
```

#### 6.3 知識庫（RAG）

**創建知識庫:**
```
1. 百煉控制台 → 知識庫 → 創建知識庫
2. 填寫信息：
   - 知識庫名稱
   - 描述
   - 選擇嵌入模型
3. 上傳文檔：
   - 支持格式：PDF、Word、TXT、Markdown
   - 批量上傳
4. 文檔處理：
   - 自動分段
   - 向量化
   - 建立索引
5. 完成創建
```

**綁定應用:**
```
1. 應用配置 → 知識庫
2. 選擇已創建的知識庫
3. 設置檢索參數：
   - 檢索條數（Top K）
   - 相似度閾值
   - 重排序（可選）
4. 保存配置
```

---

### 7. OpenClaw 集成百煉

#### 7.1 配置環境變量

**在 OpenClaw 中配置:**
```bash
# ~/.openclaw/workspace/.env
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

#### 7.2 配置模型別名

**在 OpenClaw 配置中添加:**
```yaml
# config.yaml
model_aliases:
  qwen3-max: dashscope/qwen3-max-2026-01-23
  qwen3-max-2025-09-23: dashscope-us/qwen3-max-2025-09-23
  qwen3-vl-plus: dashscope-us/qwen3-vl-plus
  qwen3.5-plus: dashscope/qwen3.5-plus
  qwen3.5-plus-coding: dashscope-coding/qwen3.5-plus
```

#### 7.3 使用示例

**在技能中使用:**
```python
import os
from openai import OpenAI

def call_qwen(prompt, model="qwen3.5-plus"):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
    )
    
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content
```

---

## 📝 Day 5 學習總結

### 掌握的要點

| 模塊 | 核心技能 |
|------|---------|
| **API Key 管理** | 創建、保存、輪換、多環境管理 |
| **模型調用** | OpenAI 兼容 API、Python/Node.js/curl 示例 |
| **模型選擇** | 千問 Max/Plus/Flash/Coder 適用場景 |
| **計費管理** | 按量付費、免費額度、賬單查詢、成本控制 |
| **模型部署** | 共享推理 vs 專享部署 |
| **應用構建** | 智能體、工作流、知識庫（RAG） |
| **OpenClaw 集成** | 環境變量配置、模型別名 |

### 實操代碼速查

**Python 調用:**
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": "你好"}]
)

print(completion.choices[0].message.content)
```

**Token 計算:**
```python
# 估算 Token 數
def estimate_tokens(text):
    # 中文：1 字 ≈ 1.5-2 Token
    # 英文：1 詞 ≈ 1-1.5 Token
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len(text.split())
    return chinese_chars * 1.5 + english_words
```

### 成本優化速查

| 策略 | 說明 | 節省效果 |
|------|------|---------|
| 選擇 Flash | 簡單任務用 Flash | 80-90% |
| 精簡提示詞 | 減少輸入 Token | 20-50% |
| 限制輸出 | 設置 max_tokens | 可控制 |
| 使用緩存 | 避免重複請求 | 視情況 |
| Coding Plan | 固定月費 | 無風險 |

### 重要網址

| 功能 | 網址 |
|------|------|
| 百煉控制台（北京） | https://bailian.console.aliyun.com/ |
| API Key 管理 | https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key |
| 模型監控 | https://bailian.console.aliyun.com/?tab=model#/model-telemetry |
| 賬單詳情 | https://usercenter2.aliyun.com/finance/expense-report/expense-detail |
| 模型體驗 | https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text |

---

## 🎯 阿里雲學習計劃完成！

### 5 天學習總覽

| Day | 主題 | 筆記大小 | 核心技能 |
|-----|------|---------|---------|
| **Day 1** | 輕量服務器控制台 | ~5KB | 實例管理、網絡安全、監控警報 |
| **Day 2** | 控制台高級操作 | ~5.4KB | 快照、鏡像、數據盤、負載均衡 |
| **Day 3** | 實戰訓練 | ~8.7KB | Web 部署、RDS、開發環境、備份恢復 |
| **Day 4** | 企業級運維 | ~10.2KB | 監控、日誌、自動化、成本優化、災備 |
| **Day 5** | 百煉控制台（AI） | ~10KB | API Key、模型調用、計費、應用構建 |

### 累計成果
- 📄 **筆記總量:** ~39KB
- ✅ **完成進度:** 100%（5/5 天）
- 🛠️ **掌握技能:** 30+ 核心操作
- 📚 **參考文件:** 4 份（共 83KB）

### 下一步建議

1. **實戰演練** - 在阿里雲上實際操作
2. **成本監控** - 設置預警，避免意外扣費
3. **應用集成** - 將百煉集成到 OpenClaw
4. **持續學習** - 關注阿里雲新產品和功能

---

**最後更新:** 2026-03-18 06:15  
**Day 5 狀態:** ✅ 完成  
**整個學習計劃:** ✅ 100% 完成！
