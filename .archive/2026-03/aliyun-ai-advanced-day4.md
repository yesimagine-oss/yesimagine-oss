# 📚 阿里雲 AI 應用進階 - Day 4：模型微調實戰完整指南

**學習時間:** 2026-03-18  
**主題:** SFT 微調、DPO 優化、模型評估、行業模型實戰

---

## 一、SFT 微調（監督微調）

### 1.1 什麼是 SFT

```
SFT (Supervised Fine-Tuning) = 監督微調

原理:
基礎模型 + 標註數據 → 微調 → 行業專屬模型

適用場景:
- 客服問答（學習企業話術）
- 醫療諮詢（學習醫學知識）
- 法律顧問（學習法律條文）
- 技術支持（學習產品知識）
```

### 1.2 數據準備

**訓練數據格式 (JSONL):**

```jsonl
{"instruction": "回答用戶關於退貨的問題", "input": "我買的衣服不合適，可以退貨嗎？", "output": "可以的，我們支持 7 天無理由退貨。請保持商品吊牌完整，聯繫客服辦理退貨手續。"}
{"instruction": "查詢訂單狀態", "input": "我的訂單號是 12345，現在到哪了？", "output": "您的訂單 12345 已從上海倉庫發出，預計明天送達。"}
{"instruction": "推薦產品", "input": "我想買一台筆記本電腦，預算 5000 元左右", "output": "推薦您聯想小新 Pro14，配置 i5-12 代處理器，16GB 內存，512GB SSD，售價 4999 元，性價比很高。"}
```

**數據量建議:**

| 場景 | 最小數據量 | 推薦數據量 | 效果 |
|------|----------|----------|------|
| 簡單問答 | 100 條 | 500-1000 條 | ⭐⭐⭐ |
| 專業領域 | 500 條 | 2000-5000 條 | ⭐⭐⭐⭐ |
| 複雜任務 | 1000 條 | 5000-10000 條 | ⭐⭐⭐⭐⭐ |

### 1.3 百煉控制台微調步驟

```
步驟 1：準備數據
1. 按上述格式準備 JSONL 文件
2. 訓練集：80% 數據
3. 驗證集：20% 數據

步驟 2：上傳數據
1. 百煉控制台 → 數據管理
2. 上傳 train.jsonl 和 val.jsonl
3. 選擇數據類型：對話/問答

步驟 3：創建微調任務
1. 模型訓練 → 創建微調任務
2. 選擇基礎模型：qwen3.5-plus
3. 選擇訓練數據
4. 配置參數：
   - Epochs: 3
   - Batch Size: 4
   - Learning Rate: 1e-5
   - Max Length: 1024
5. 開始訓練

步驟 4：等待完成
- 小數據集（<1000 條）：約 30 分鐘
- 中等數據集（1000-5000 條）：約 1-2 小時
- 大數據集（>5000 條）：約 3-5 小時

步驟 5：測試模型
1. 訓練完成後自動部署
2. 獲取模型 ID
3. 使用 API 測試
```

### 1.4 微調參數調優

```yaml
關鍵參數:

Epochs (訓練輪數):
  範圍：1-10
  推薦：3-5
  說明:
    - 太少：欠拟合，學不到知識
    - 太多：過拟合，泛化能力差
  建議：從小數據開始，逐步增加

Batch Size (批次大小):
  範圍：1-32
  推薦：4-8
  說明:
    - 太小：訓練不穩定
    - 太大：內存不足
  建議：根據顯存調整

Learning Rate (學習率):
  範圍：1e-6 到 1e-4
  推薦：1e-5
  說明:
    - 太小：收斂慢
    - 太大：不收斂
  建議：使用學習率調度

Max Length (最大長度):
  範圍：512-4096
  推薦：1024-2048
  說明:
    - 太短：信息不完整
    - 太長：計算資源浪費
  建議：根據數據分佈調整

LoRA 參數:
  r: 8-16 (低秩矩陣維度)
  alpha: 16-32 (縮放係數)
  說明：參數高效微調，節省資源
```

---

## 二、DPO 優化（直接偏好優化）

### 2.1 什麼是 DPO

```
DPO (Direct Preference Optimization) = 直接偏好優化

原理:
微調模型 + 偏好數據 → 優化 → 更符合人類偏好

與 RLHF 對比:
RLHF: 複雜，需要獎勵模型，訓練不穩定
DPO: 簡單，直接優化，訓練穩定

適用場景:
- 提高回答質量
- 減少有害輸出
- 調整語氣風格
- 對齊企業價值觀
```

### 2.2 偏好數據格式

```jsonl
{
  "prompt": "用戶問題",
  "chosen": "優質回答（人類偏好）",
  "rejected": "劣質回答（人類不偏好）"
}

示例:
{
  "prompt": "怎麼評價競爭對手的產品？",
  "chosen": "每家產品都有各自優勢，建議您根據實際需求選擇。我們產品的優勢是...",
  "rejected": "對手產品很差，不如我們的產品。"
}
```

### 2.3 DPO 配置

```yaml
DPO 參數:

Beta (溫度參數):
  範圍：0.1-0.5
  推薦：0.1-0.2
  說明:
    - 太小：優化力度弱
    - 太大：影響模型能力
  建議：從 0.1 開始

Epochs:
  範圍：1-3
  推薦：1-2
  說明：DPO 通常 1-2 輪即可

Batch Size:
  範圍：2-8
  推薦：4
  說明：需要成對數據（chosen+rejected）
```

---

## 三、模型評估

### 3.1 評估指標

| 指標 | 說明 | 適用場景 | 計算方式 |
|------|------|---------|---------|
| **Accuracy** | 準確率 | 分類任務 | 正確數/總數 |
| **F1 Score** | 綜合指標 | 不平衡數據 | 精確率和召回率調和 |
| **ROUGE** | 文本相似度 | 摘要生成 | N-gram 重疊率 |
| **BLEU** | 翻譯質量 | 翻譯任務 | 精確度為主的相似度 |
| **人工評分** | 主觀質量 | 所有場景 | 1-5 分評分 |

### 3.2 自動化評估腳本

```python
"""
模型評估腳本
"""
import json
from typing import List, Dict
from openai import OpenAI

class ModelEvaluator:
    """模型評估器"""
    
    def __init__(self, config, model_id: str):
        self.config = config
        self.model_id = model_id
        self.client = OpenAI(
            api_key=config.DASHSCOPE_API_KEY,
            base_url=config.DASHSCOPE_BASE_URL
        )
    
    def evaluate(self, test_data: List[Dict]) -> Dict:
        """
        評估模型
        
        Args:
            test_data: 測試數據列表
            
        Returns:
            評估結果
        """
        results = []
        
        for sample in test_data:
            # 生成回答
            prediction = self._generate(sample['prompt'])
            
            # 計算指標
            score = self._calculate_score(prediction, sample['golden'])
            
            results.append({
                'prompt': sample['prompt'],
                'prediction': prediction,
                'golden': sample['golden'],
                'score': score
            })
        
        # 彙總統計
        metrics = self._aggregate_metrics(results)
        
        return {
            'total_samples': len(test_data),
            'metrics': metrics,
            'details': results
        }
    
    def _generate(self, prompt: str) -> str:
        """生成回答"""
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=512
        )
        return response.choices[0].message.content
    
    def _calculate_score(self, prediction: str, golden: str) -> Dict:
        """計算單樣本得分"""
        # 簡化版：使用 ROUGE-L
        from rouge import Rouge
        rouge = Rouge()
        scores = rouge.get_scores(prediction, golden)[0]
        
        return {
            'rouge-l': scores['rouge-l']['f'],
            'exact_match': 1.0 if prediction.strip() == golden.strip() else 0.0
        }
    
    def _aggregate_metrics(self, results: List[Dict]) -> Dict:
        """彙總統計指標"""
        import numpy as np
        
        rouge_scores = [r['score']['rouge-l'] for r in results]
        em_scores = [r['score']['exact_match'] for r in results]
        
        return {
            'rouge-l': {
                'mean': np.mean(rouge_scores),
                'std': np.std(rouge_scores),
                'min': np.min(rouge_scores),
                'max': np.max(rouge_scores)
            },
            'exact_match': {
                'mean': np.mean(em_scores),
                'count': sum(em_scores)
            }
        }

# 使用示例
evaluator = ModelEvaluator(config, "qwen3.5-ft")
test_data = [
    {"prompt": "問題 1", "golden": "參考回答 1"},
    {"prompt": "問題 2", "golden": "參考回答 2"}
]
results = evaluator.evaluate(test_data)
print(f"ROUGE-L: {results['metrics']['rouge-l']['mean']:.4f}")
```

### 3.3 人工評估模板

```markdown
# 模型評估表

評估員：___________  日期：___________

| 樣本 | 問題 | 模型回答 | 參考回答 | 評分 (1-5) | 備註 |
|------|------|---------|---------|-----------|------|
| 1 | ... | ... | ... | ⭐⭐⭐⭐ | 回答準確，但略長 |
| 2 | ... | ... | ... | ⭐⭐⭐⭐⭐ | 完美 |
| 3 | ... | ... | ... | ⭐⭐⭐ | 遺漏關鍵信息 |

評分標準:
⭐⭐⭐⭐⭐ (5 分): 完美，超出預期
⭐⭐⭐⭐ (4 分): 良好，小瑕疵
⭐⭐⭐ (3 分): 合格，有改進空間
⭐⭐ (2 分): 不合格，重大問題
⭐ (1 分): 完全錯誤

總體評價:
- 平均分：___ / 5
- 優點：___________
- 改進建議：___________
```

---

## 四、成本優化

### 4.1 微調成本估算

```
百煉微調計費:

訓練費用:
- qwen3.5-plus: ¥0.5/小時
- 訓練時長：數據量 × Epochs / 吞吐

示例計算:
數據量：1000 條
Epochs: 3
吞吐量：100 條/分鐘
訓練時長：1000 × 3 / 100 = 30 分鐘
訓練費用：0.5 × 0.5 = ¥0.25

存儲費用:
- 模型存儲：¥0.1/GB/天
- 模型大小：約 1-5GB
- 月費用：¥3-15

推理費用:
- 微調後模型：與基礎模型相同
- qwen3.5-plus: ¥0.004/1K tokens (輸入) + ¥0.012/1K tokens (輸出)

總成本（首月）:
- 訓練：¥0.25
- 存儲：¥10
- 推理（10 萬 tokens/天）: ¥50/天 × 30 = ¥1500
- 合計：約 ¥1510
```

### 4.2 成本優化技巧

```yaml
訓練階段優化:

1. 數據質量優先:
   - 100 條高質量數據 > 1000 條低質量
   - 人工審核訓練數據
   - 去除重複和錯誤樣本

2. 從小規模開始:
   - 先用 100-200 條測試
   - 驗證效果後再擴大
   - 避免浪費訓練資源

3. 選擇合適的 Epochs:
   - 小數據集：3-5 epochs
   - 大數據集：1-2 epochs
   - 監控驗證集損失，早停

推理階段優化:

1. 模型選擇:
   - 簡單任務：qwen3.5-flash (便宜 10 倍)
   - 一般任務：qwen3.5-plus
   - 複雜任務：qwen3.5-max

2. Token 優化:
   - 精簡提示詞
   - 限制 max_tokens
   - 使用緩存

3. 批量處理:
   - 合併多個請求
   - 減少 API 調用次數
```

### 4.3 成本監控腳本

```python
"""
成本監控腳本
"""
import requests
from datetime import datetime, timedelta

class CostMonitor:
    """成本監控器"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.DASHSCOPE_API_KEY
    
    def get_daily_cost(self, date: str = None) -> Dict:
        """獲取每日成本"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 調用阿里雲賬單 API
        # 這裡是示例，實際需要使用阿里雲 SDK
        response = requests.get(
            "https://billing.aliyuncs.com/api/daily-cost",
            headers={"Authorization": f"Bearer {self.api_key}"},
            params={"date": date}
        )
        
        data = response.json()
        
        return {
            'date': date,
            'total_cost': data.get('total', 0),
            'training_cost': data.get('training', 0),
            'inference_cost': data.get('inference', 0),
            'storage_cost': data.get('storage', 0)
        }
    
    def get_monthly_cost(self, year: int, month: int) -> Dict:
        """獲取月度成本"""
        # 彙總每日成本
        daily_costs = []
        days_in_month = 30  # 簡化
        
        for day in range(1, days_in_month + 1):
            date = f"{year}-{month:02d}-{day:02d}"
            cost = self.get_daily_cost(date)
            daily_costs.append(cost)
        
        total = sum(c['total_cost'] for c in daily_costs)
        avg = total / len(daily_costs)
        
        return {
            'year': year,
            'month': month,
            'total': total,
            'daily_avg': avg,
            'daily_costs': daily_costs
        }
    
    def set_budget_alert(self, budget: float):
        """設置預算告警"""
        # 當成本超過預算時發送通知
        # 可以集成釘釘、郵件等
        print(f"設置預算告警：¥{budget}")

# 使用示例
monitor = CostMonitor(config)
today_cost = monitor.get_daily_cost()
print(f"今日成本：¥{today_cost['total_cost']:.2f}")

monthly = monitor.get_monthly_cost(2026, 3)
print(f"本月總成本：¥{monthly['total']:.2f}")
```

---

## 五、實戰：行業專屬模型

### 5.1 電商客服模型

**場景:** 電商平台智能客服

**數據準備:**
```jsonl
{"instruction": "退貨政策", "input": "可以退貨嗎？", "output": "我們支持 7 天無理由退貨，請保持商品完好。"}
{"instruction": "物流查詢", "input": "訂單到哪了？", "output": "請提供訂單號，我幫您查詢。"}
{"instruction": "產品推薦", "input": "推薦一款手機", "output": "請問您的預算是多少？主要用途是什麼？"}
```

**微調配置:**
```yaml
基礎模型：qwen3.5-plus
訓練數據：2000 條客服對話
Epochs: 3
Batch Size: 4
Learning Rate: 1e-5
Max Length: 1024
```

**預期效果:**
- 回答準確率：> 90%
- 用戶滿意度：> 4.5/5
- 人工客服工作量：減少 70%

### 5.2 醫療諮詢模型

**場景:** 在線醫療諮詢

**數據準備:**
```jsonl
{"instruction": "症狀分析", "input": "頭痛發燒怎麼辦？", "output": "建議測量體溫，多喝水，如持續高燒請就醫。"}
{"instruction": "用藥指導", "input": "感冒吃什麼藥？", "output": "普通感冒可服用感冒清熱顆粒，如有其他症狀請諮詢醫生。"}
```

**注意事項:**
```
⚠️ 醫療模型特殊要求:
1. 數據需要專業醫生審核
2. 回答必須謹慎，避免誤導
3. 建議就醫的情況必須明確說明
4. 符合醫療法規要求
```

### 5.3 法律顧問模型

**場景:** 法律諮詢助手

**數據準備:**
```jsonl
{"instruction": "勞動法諮詢", "input": "公司辭退我有賠償嗎？", "output": "根據勞動合同法，違法解除應支付賠償金，標準為..."}
{"instruction": "合同法諮詢", "input": "合同違約怎麼辦？", "output": "可以要求違約方承擔違約責任，包括..."}
```

**預期效果:**
- 法律條款引用準確率：> 95%
- 案例匹配準確率：> 85%
- 用戶满意度：> 4/5

---

## 六、快速開始指南

### 6.1 最簡單的微調流程

```bash
# 1. 準備數據（最少 100 條）
cat > train_data.jsonl << 'EOF'
{"instruction": "問題 1", "input": "", "output": "回答 1"}
{"instruction": "問題 2", "input": "", "output": "回答 2"}
EOF

# 2. 百煉控制台上傳
# https://bailian.console.aliyun.com/
# → 數據管理 → 上傳

# 3. 創建微調任務
# → 模型訓練 → 創建任務
# → 選擇 qwen3.5-plus
# → 選擇訓練數據
# → 開始訓練

# 4. 等待完成（約 30 分鐘）

# 5. 測試模型
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "你的微調模型 ID",
    "messages": [{"role": "user", "content": "測試問題"}]
  }'
```

### 6.2 預算建議

```yaml
初學者（測試）:
  數據量：100-200 條
  訓練成本：< ¥1
  推理成本：¥50-100/月
  適合：個人項目、概念驗證

小企業（生產）:
  數據量：1000-2000 條
  訓練成本：¥5-10
  推理成本：¥500-1000/月
  適合：客服系統、內部工具

大企業（規模化）:
  數據量：5000-10000 條
  訓練成本：¥50-100
  推理成本：¥5000+/月
  適合：多場景應用、高併發
```

---

## 七、常見問題

### Q1: 需要多少數據？
```
A: 
- 簡單任務：100-500 條
- 中等任務：500-2000 條
- 複雜任務：2000-10000 條

質量 > 數量，100 條高質量數據勝過 1000 條低質量
```

### Q2: 微調需要多久？
```
A:
- 100 條數據：約 10-20 分鐘
- 1000 條數據：約 30-60 分鐘
- 10000 條數據：約 3-5 小時
```

### Q3: 微調後效果不好怎麼辦？
```
A:
1. 檢查數據質量（是否有錯誤、不一致）
2. 增加數據量
3. 調整超參數（Epochs、Learning Rate）
4. 嘗試不同的基礎模型
5. 考慮使用 DPO 優化
```

### Q4: 微調和 RAG 怎麼選？
```
A:
微調適合:
- 學習特定風格/話術
- 提高專業領域準確率
- 固化知識到模型

RAG 適合:
- 知識頻繁更新
- 需要引用具體文檔
- 數據量大且動態

最佳實踐：微調 + RAG 結合使用
```

---

**完成時間:** 2026-03-18  
**狀態:** ✅ Day 4 完成  
**核心收穫:** SFT 微調流程、DPO 優化、模型評估、成本估算
