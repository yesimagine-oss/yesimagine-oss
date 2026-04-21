# 📚 阿里雲 AI 應用進階 - Day 1 學習筆記

**學習時間:** 2026-03-18  
**學習主題:** Agent 編排與插件系統  
**參考資料:** 阿里雲百煉官方文檔

---

## Day 1 - Agent 編排與插件系統

### 1. 單 Agent 高級配置

#### 1.1 Agent 架構解析

**核心組件:**
```
智能體（Agent）
├─ 模型層（Model）
│   ├─ 千問 Max/Plus/Flash
│   └─ 第三方模型
│
├─ 知識層（Knowledge）
│   ├─ 知識庫 RAG
│   └─ 長期記憶
│
├─ 工具層（Tools）
│   ├─ 插件系統
│   └─ API 調用
│
└─ 流程層（Flow）
    ├─ 對話管理
    └─ 任務規劃
```

#### 1.2 高級提示詞工程

**System Prompt 結構:**
```markdown
# 角色定義
你是一名專業的{角色名稱}，負責{職責描述}。

# 能力範圍
- 能力 1：{具體描述}
- 能力 2：{具體描述}
- 能力 3：{具體描述}

# 工作流程
1. 第一步：{動作}
2. 第二步：{動作}
3. 第三步：{動作}

# 約束條件
- 限制 1：{具體限制}
- 限制 2：{具體限制}
- 禁止：{禁止事項}

# 回復規範
- 語氣：{友好/專業/簡潔}
- 格式：{結構化/段落/列表}
- 長度：{簡短/詳細}

# 示例對話
用戶：{示例問題}
助手：{示例回答}
```

**實戰示例 - 智能客服:**
```markdown
# 角色定義
你是一名專業的電商客服助手，負責回答用戶關於產品、訂單、售後的問題。

# 能力範圍
- 產品諮詢：價格、規格、庫存、促銷
- 訂單查詢：訂單狀態、物流信息
- 售後服務：退換貨、維修、投訴

# 工作流程
1. 理解用戶問題類型（產品/訂單/售後）
2. 檢索相關知識庫
3. 給出準確回答
4. 如無法解決，引導轉人工客服

# 約束條件
- 只能回答與本店相關的問題
- 不確定的信息如實告知
- 禁止承諾無法實現的服務
- 敏感問題（政治、宗教）禮貌回避

# 回復規範
- 語氣：友好、耐心、專業
- 格式：結構化，使用列表
- 長度：簡潔，不超過 200 字

# 示例對話
用戶：這個產品多少錢？
助手：您好！這款產品原價¥999，現活動價¥799，包郵到家~
```

#### 1.3 參數調優

**關鍵參數:**
```yaml
溫度（Temperature）:
  範圍：0-2
  推薦：0.7（平衡創造性和準確性）
  場景:
    0.1-0.3: 事實性問答、代碼生成
    0.5-0.7: 一般對話、客服
    0.8-1.0: 創意寫作、頭腦風暴
    1.0-2.0: 高度創造性任務

最大 Token（max_tokens）:
  推薦：512-2048
  場景:
    256-512: 簡短回答、分類
    512-1024: 一般對話
    1024-2048: 詳細解答
    2048+: 長文本生成

Top P:
  範圍：0-1
  推薦：0.8-0.95
  說明：控制詞彙多樣性

頻率懲罰（frequency_penalty）:
  範圍：0-2
  推薦：0.1-0.3
  說明：減少重複內容

存在懲罰（presence_penalty）:
  範圍：0-2
  推薦：0.1-0.3
  說明：鼓勵新話題
```

---

### 2. 多 Agent 協作

#### 2.1 多 Agent 架構

**架構模式:**
```
模式一：主從式
    主 Agent（協調者）
    ├── 從 Agent 1（專家 A）
    ├── 從 Agent 2（專家 B）
    └── 從 Agent 3（專家 C）

模式二：流水線式
    用戶輸入 → Agent1 → Agent2 → Agent3 → 輸出

模式三：投票式
    用戶輸入 → [Agent1, Agent2, Agent3] → 投票 → 輸出
```

#### 2.2 協作場景

**場景一：複雜問題分解**
```
用戶問題：我想開一家網店，需要怎麼準備？

主 Agent 分析 → 分解為：
├─ 市場調研 Agent：分析目標市場
├─ 選品 Agent：推薦產品類別
├─ 運營 Agent：制定運營計劃
└─ 財務 Agent：預算規劃

最後匯總 → 完整方案
```

**場景二：專業領域協作**
```
醫療諮詢場景：
├─ 分診 Agent：初步判斷科室
├─ 專科 Agent：專業建議
├─ 用藥 Agent：用藥指導
└─ 掛號 Agent：預約服務
```

#### 2.3 實現方式

**工作流編排:**
```yaml
# workflow.yml
nodes:
  - id: analyzer
    type: agent
    model: qwen3.5-plus
    prompt: 分析用戶意圖，分類為：技術/產品/訂單/售後
  
  - id: tech_support
    type: agent
    model: qwen3.5-plus
    condition: intent == '技術'
    prompt: 技術支持專家...
  
  - id: product_support
    type: agent
    model: qwen3.5-plus
    condition: intent == '產品'
    prompt: 產品諮詢專家...
  
  - id: summarizer
    type: agent
    model: qwen3.5-plus
    prompt: 總結以上回答，確保一致性

edges:
  - from: analyzer
    to: tech_support
    condition: intent == '技術'
  - from: analyzer
    to: product_support
    condition: intent == '產品'
  - from: tech_support
    to: summarizer
  - from: product_support
    to: summarizer
```

---

### 3. 插件系統详解

#### 3.1 插件類型

**內置插件:**
```
- 搜索插件：聯網搜索、新聞查詢
- 計算插件：數學計算、單位轉換
- 日曆插件：日期計算、日程管理
- 翻譯插件：多語言翻譯
- 編程插件：代碼執行、調試
```

**自定義插件:**
```
- API 調用插件：調用第三方服務
- 數據庫插件：查詢內部數據
- 業務系統插件：ERP、CRM 集成
- 自定義腳本：Python/JS 執行
```

#### 3.2 創建自定義插件

**插件配置（OpenAPI 規範）:**
```yaml
# plugin.yaml
openapi: 3.0.0
info:
  title: 天氣查詢插件
  version: 1.0.0
  description: 查詢實時天氣信息

servers:
  - url: https://api.weather.com

paths:
  /weather:
    get:
      operationId: getWeather
      summary: 查詢天氣
      parameters:
        - name: city
          in: query
          required: true
          schema:
            type: string
          description: 城市名稱
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  temperature:
                    type: number
                  condition:
                    type: string
                  humidity:
                    type: number
```

**插件註冊:**
```
1. 百煉控制台 → 插件中心
2. 點擊「創建插件」
3. 填寫信息：
   - 插件名稱：天氣查詢
   - 描述：查詢實時天氣
   - API 配置：上傳 OpenAPI YAML
   - 認證方式：API Key / OAuth
4. 測試插件
5. 發布插件
```

**在 Agent 中使用:**
```markdown
# System Prompt 中添加
你可以使用以下工具：

## 天氣查詢
- 用途：查詢實時天氣
- 參數：city（城市名稱）
- 示例：天氣查詢（北京）

當用戶詢問天氣時，請調用此插件。
```

#### 3.3 插件調用流程

```
用戶問題 → Agent 分析
              ↓
      識別需要插件
              ↓
      構造插件請求
              ↓
      執行插件調用
              ↓
      解析插件返回
              ↓
      整合回答 → 用戶
```

**示例對話:**
```
用戶：北京今天天氣怎麼樣？

Agent 思考：用戶詢問天氣，需要調用天氣插件
          ↓
調用：getWeather(city="北京")
          ↓
返回：{"temperature": 25, "condition": "晴", "humidity": 60}
          ↓
整合：北京今天天氣晴朗，氣溫 25°C，濕度 60%，適宜外出~
```

---

### 4. MCP 協議（Model Context Protocol）

#### 4.1 什麼是 MCP

**Model Context Protocol** 是一種標準化協議，用於：
- 統一模型與外部工具的通信
- 支持多種工具類型
- 簡化插件開發

**核心概念:**
```
MCP 架構:
├─ Client（模型側）
│   └─ 發送請求、接收響應
│
├─ Server（工具側）
│   └─ 實現工具邏輯
│
└─ Protocol（協議層）
    └─ 標準化通信格式
```

#### 4.2 MCP 資源類型

**Resources（資源）:**
```json
{
  "uri": "file:///documents/manual.pdf",
  "name": "產品手冊",
  "mimeType": "application/pdf",
  "description": "產品使用手冊"
}
```

**Prompts（提示詞模板）:**
```json
{
  "name": "客服回復模板",
  "description": "生成客服回復",
  "arguments": [
    {"name": "問題類型", "required": true},
    {"name": "用戶等級", "required": false}
  ]
}
```

**Tools（工具）:**
```json
{
  "name": "查詢訂單",
  "description": "查詢訂單狀態",
  "inputSchema": {
    "type": "object",
    "properties": {
      "orderId": {"type": "string"}
    },
    "required": ["orderId"]
  }
}
```

#### 4.3 MCP 服務器示例

**Python MCP Server:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("my-app")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_order",
            description="查詢訂單狀態",
            inputSchema={
                "type": "object",
                "properties": {
                    "orderId": {"type": "string"}
                },
                "required": ["orderId"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query_order":
        # 查詢訂單邏輯
        order_info = await get_order(arguments["orderId"])
        return [TextContent(text=f"訂單狀態：{order_info.status}")]
```

**配置 MCP 到百煉:**
```
1. 部署 MCP Server
2. 百煉控制台 → 插件中心 → MCP 插件
3. 添加 MCP Server 地址
4. 配置認證信息
5. 測試連接
6. 在 Agent 中啟用
```

---

### 5. 實戰：智能客服 Agent

#### 5.1 需求分析

**功能需求:**
```
- 自動回答產品問題
- 查詢訂單狀態
- 處理退換貨申請
- 轉接人工客服
- 記錄對話歷史
```

**技術方案:**
```yaml
模型：千問 Plus（性價比高）
知識庫：產品手冊 + FAQ + 價格表
插件:
  - 訂單查詢插件
  - 退換貨插件
  - 人工客服插件
渠道：钉钉 + Web
```

#### 5.2 配置步驟

**步驟 1：創建知識庫**
```
1. 百煉控制台 → 知識庫 → 創建
2. 上傳文檔：
   - 產品手冊.pdf
   - FAQ 大全.docx
   - 價格表.xlsx
3. 配置分段：
   - 分段大小：500 tokens
   - 重疊：50 tokens
4. 向量化處理
5. 完成創建
```

**步驟 2：創建插件**
```yaml
# 訂單查詢插件
名稱：query_order
描述：查詢訂單狀態
API: POST https://api.example.com/orders/{id}
認證：API Key

# 退換貨插件
名稱：apply_return
描述：申請退換貨
API: POST https://api.example.com/returns
參數：orderId, reason, images
```

**步驟 3：創建 Agent**
```
1. 百煉控制台 → 應用構建 → 創建應用
2. 選擇「智能體應用」
3. 配置：
   - 名稱：智能客服助手
   - 模型：千問 Plus
   - 溫度：0.7
   - 最大 Token: 1024
4. 綁定知識庫
5. 啟用插件
6. 配置 System Prompt
```

**步驟 4：System Prompt**
```markdown
# 角色定義
你是一名專業的電商客服助手，名為「小智」，負責回答用戶關於產品、訂單、售後的問題。

# 能力範圍
- 產品諮詢：價格、規格、庫存、促銷活動
- 訂單查詢：訂單狀態、物流信息、預計送達
- 售後服務：退換貨政策、維修服務、投訴處理

# 工作流程
1. 理解用戶問題類型（產品/訂單/售後/其他）
2. 如需要，調用相應插件獲取信息
3. 結合知識庫內容，給出準確回答
4. 如無法解決，引導用戶轉人工客服

# 約束條件
- 只能回答與本店相關的問題
- 不確定的信息如實告知，不要編造
- 禁止承諾無法實現的服務
- 價格信息以知識庫為準
- 敏感問題（政治、宗教）禮貌回避

# 回復規範
- 語氣：友好、耐心、專業
- 格式：結構化，適當使用列表
- 長度：簡潔，一般不超過 200 字
- 稱呼：使用「您」表示尊重

# 轉人工規則
遇到以下情況轉人工客服：
1. 用戶明確要求人工
2. 問題超出你的能力範圍
3. 用戶情緒激動需要安撫
4. 涉及退款、賠償等敏感問題
```

#### 5.3 測試與優化

**測試用例:**
```markdown
用例 1：產品諮詢
用戶：這款手機多少錢？
預期：回答價格，並介紹促銷活動

用例 2：訂單查詢
用戶：我的訂單到哪了？訂單號 12345
預期：調用插件，返回物流信息

用例 3：退換貨
用戶：我想退貨，怎麼操作？
預期：說明退換貨政策，引導申請

用例 4：投訴
用戶：你們的產品質量太差了！
預期：安撫情緒，轉人工客服
```

**優化方向:**
```
- 根據對話日誌調整提示詞
- 添加常見問題到知識庫
- 優化插件響應速度
- 設置敏感詞過濾
- 定期更新產品信息
```

---

## 📝 Day 1 學習總結

### 掌握的要點

| 模塊 | 核心技能 |
|------|---------|
| **單 Agent 配置** | System Prompt 工程、參數調優 |
| **多 Agent 協作** | 架構設計、任務分解、結果匯總 |
| **插件系統** | OpenAPI 規範、自定義插件、插件調用 |
| **MCP 協議** | 資源/提示詞/工具、MCP Server 開發 |
| **實戰應用** | 智能客服 Agent 完整配置 |

### 實操代碼速查

**OpenAPI 插件配置:**
```yaml
openapi: 3.0.0
info:
  title: 我的插件
  version: 1.0.0
paths:
  /api:
    get:
      operationId: myFunction
      parameters: [...]
```

**MCP Tool 定義:**
```python
@app.list_tools()
async def list_tools():
    return [Tool(name="tool_name", ...)]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    # 實現邏輯
```

### 下一步

- [ ] 實踐：創建自己的第一個 Agent
- [ ] 實踐：開發一個自定義插件
- [ ] 預習：Day 2 知識庫 RAG

---

**最後更新:** 2026-03-18 06:30  
**Day 1 狀態:** ✅ 學習中
