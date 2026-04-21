# 📚 阿里雲 AI 應用進階 - Day 5：應用發布與運營

**學習時間:** 2026-03-18  
**學習主題:** 多渠道發布、數據監控、A/B 測試、完整上線  
**目標:** 可生產部署的完整應用系統

---

## 一、多渠道發布

### 1.1 渠道總覽

```
應用發布渠道:

┌─────────────────────────────────────────┐
│           你的 AI 應用                    │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┐
    ↓           ↓           ↓
┌───────┐  ┌───────┐  ┌───────┐
│ 釘釘  │  │ 微信  │  │  Web  │
│機器人 │  │公眾號 │  │ 應用  │
└───────┘  └───────┘  └───────┘
    │           │           │
    ↓           ↓           ↓
企業用戶    個人用戶     所有用戶
```

### 1.2 釘釘機器人集成

#### 步驟 1：創建釘釘機器人

```
1. 打開釘釘群
2. 群設置 → 智能助手 → 添加機器人
3. 選擇「自定義」
4. 填寫信息：
   - 機器人名稱：AI 助手
   - 頭像：上傳 logo
5. 獲取 Webhook URL
   https://oapi.dingtalk.com/robot/send?access_token=xxx
6. 安全設置：
   - 選擇「自定義關鍵詞」
   - 添加關鍵詞：AI、助手、問題
7. 完成創建
```

#### 步驟 2：釘釘機器人代碼

```python
"""
釘釘機器人集成
"""
from flask import Flask, request, jsonify
import requests
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 配置
DINGTALK_ACCESS_TOKEN = "xxx"
AI_API_URL = "http://localhost:5000/api/query"

class DingTalkBot:
    """釘釘機器人"""
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.webhook = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"
    
    def send_text(self, content: str, mentioned_users: list = None):
        """發送文本消息"""
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "userIds": mentioned_users or [],
                "isAtAll": mentioned_users is None
            }
        }
        
        response = requests.post(self.webhook, json=payload)
        return response.json()
    
    def send_markdown(self, title: str, text: str):
        """發送 Markdown 消息"""
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        
        response = requests.post(self.webhook, json=payload)
        return response.json()
    
    def send_link(self, title: str, text: str, pic_url: str, message_url: str):
        """發送鏈接消息"""
        payload = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "picUrl": pic_url,
                "messageUrl": message_url
            }
        }
        
        response = requests.post(self.webhook, json=payload)
        return response.json()

# 初始化機器人
bot = DingTalkBot(DINGTALK_ACCESS_TOKEN)

@app.route('/dingtalk/callback', methods=['POST'])
def dingtalk_callback():
    """
    釘釘回調接口
    
    用戶在釘釘中 @機器人 提問
    → 釘釘服務器轉發到此接口
    → 調用 AI API 獲取回答
    → 返回回答給釘釘
    """
    data = request.json
    
    # 解析用戶消息
    msg_type = data.get('msgtype')
    if msg_type != 'text':
        return jsonify({'result': 'ok'})
    
    content = data.get('text', {}).get('content', '')
    sender = data.get('senderId', 'unknown')
    conversation_id = data.get('conversationId', 'unknown')
    
    logging.info(f"收到釘釘消息：{content[:50]}... from {sender}")
    
    # 調用 AI API
    ai_response = requests.post(AI_API_URL, json={
        'question': content,
        'user_id': sender,
        'channel': 'dingtalk'
    })
    
    answer = ai_response.json().get('answer', '抱歉，我暫時無法回答這個問題。')
    
    # 發送回答
    bot.send_text(answer, mentioned_users=[sender])
    
    logging.info(f"已回復釘釘用戶 {sender}")
    
    return jsonify({'result': 'ok'})

# 使用示例
if __name__ == '__main__':
    # 發送歡迎消息
    bot.send_markdown(
        title="AI 助手已上線",
        text="## 🤖 AI 助手已上線\n\n"
             "我可以幫您：\n"
             "- 回答產品問題\n"
             "- 查詢訂單狀態\n"
             "- 處理售後問題\n\n"
             "隨時 @我 提問吧！"
    )
    
    # 啟動回調服務
    app.run(port=5002)
```

### 1.3 微信公眾號集成

#### 步驟 1：微信公眾號配置

```
1. 登錄微信公眾號平台
   https://mp.weixin.qq.com/

2. 開發 → 基本配置
   - 獲取 AppID 和 AppSecret

3. 服務器配置
   - URL: https://your-domain.com/wechat/callback
   - Token: 自定義（如：mytoken123）
   - EncodingAESKey: 隨機生成

4. 驗證服務器
   - 點擊「提交」
   - 微信會發送驗證請求
   - 代碼需要正確響應

5. 啟用服務器
   - 驗證通過後啟用
```

#### 步驟 2：微信後端代碼

```python
"""
微信公眾號集成
"""
from flask import Flask, request, Response
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

app = Flask(__name__)

# 微信配置
WECHAT_APPID = "your_appid"
WECHAT_SECRET = "your_secret"
WECHAT_TOKEN = "your_token"
WECHAT_ENCODING_AES_KEY = "your_aes_key"

AI_API_URL = "http://localhost:5000/api/query"

def verify_signature(token, timestamp, nonce, signature):
    """驗證微信簽名"""
    check_str = ''.join(sorted([token, timestamp, nonce]))
    hash_str = hashlib.sha1(check_str.encode()).hexdigest()
    return hash_str == signature

def get_access_token():
    """獲取微信 access token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": WECHAT_APPID,
        "secret": WECHAT_SECRET
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data.get('access_token')

def send_customer_message(openid: str, content: str):
    """發送客服消息"""
    access_token = get_access_token()
    
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
    
    payload = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    """微信回調接口"""
    
    # GET: 驗證服務器
    if request.method == 'GET':
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        
        if verify_signature(WECHAT_TOKEN, timestamp, nonce, signature):
            return Response(echostr, mimetype='text/plain')
        else:
            return Response('failed', mimetype='text/plain', status=403)
    
    # POST: 處理用戶消息
    elif request.method == 'POST':
        # 解析 XML
        xml_data = request.data
        root = ET.fromstring(xml_data)
        
        # 提取消息內容
        msg_type = root.find('MsgType').text
        from_user = root.find('FromUserName').text
        to_user = root.find('ToUserName').text
        create_time = int(root.find('CreateTime').text)
        
        # 只處理文本消息
        if msg_type != 'text':
            return Response('success', mimetype='text/plain')
        
        content = root.find('Content').text
        
        # 調用 AI API
        ai_response = requests.post(AI_API_URL, json={
            'question': content,
            'user_id': from_user,
            'channel': 'wechat'
        })
        
        answer = ai_response.json().get('answer', '抱歉，我暫時無法回答這個問題。')
        
        # 構建回復 XML
        reply_xml = f"""
        <xml>
            <ToUserName><![CDATA[{from_user}]]></ToUserName>
            <FromUserName><![CDATA[{to_user}]]></FromUserName>
            <CreateTime>{int(datetime.now().timestamp())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{answer}]]></Content>
        </xml>
        """
        
        return Response(reply_xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(port=5003)
```

### 1.4 Web 應用部署

#### 完整 Web 應用（整合版）

```python
"""
Web 應用（完整生產版）
"""
from flask import Flask, render_template, request, jsonify, session
import uuid
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 存儲對話歷史
conversations = {}

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """聊天接口"""
    data = request.json
    question = data.get('question', '')
    session_id = data.get('session_id')
    
    # 創建或獲取會話
    if not session_id:
        session_id = str(uuid.uuid4())
        conversations[session_id] = {
            'created': datetime.now(),
            'messages': [],
            'user_id': request.remote_addr
        }
    
    conv = conversations[session_id]
    
    # 保存用戶消息
    conv['messages'].append({
        'role': 'user',
        'content': question,
        'time': datetime.now()
    })
    
    # 調用 AI（這裡調用你的 RAG 引擎）
    # from rag_engine import RAGEngine
    # engine = RAGEngine(config, kb)
    # result = engine.query(question)
    
    # 模擬回答
    result = {
        'answer': f"這是對「{question[:20]}...」的回答",
        'sources': [],
        'latency': 0.5
    }
    
    # 保存 AI 回答
    conv['messages'].append({
        'role': 'assistant',
        'content': result['answer'],
        'time': datetime.now()
    })
    
    return jsonify({
        'session_id': session_id,
        'answer': result['answer'],
        'sources': result.get('sources', []),
        'latency': result.get('latency', 0)
    })

@app.route('/history/<session_id>')
def get_history(session_id):
    """獲取對話歷史"""
    conv = conversations.get(session_id)
    if not conv:
        return jsonify({'error': '會話不存在'}), 404
    
    return jsonify({
        'created': conv['created'].isoformat(),
        'messages': conv['messages'],
        'total_messages': len(conv['messages'])
    })

@app.route('/stats')
def stats():
    """統計信息"""
    total_conversations = len(conversations)
    total_messages = sum(len(c['messages']) for c in conversations.values())
    
    return jsonify({
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'active_sessions': len([c for c in conversations.values() 
                               if (datetime.now() - c['created']).total_seconds() < 3600])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### HTML 前端模板

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 智能助手</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .container { max-width: 800px; margin: 0 auto; height: 100vh; display: flex; flex-direction: column; }
        .header { background: #1890ff; color: white; padding: 20px; text-align: center; }
        .chat-box { flex: 1; overflow-y: auto; padding: 20px; background: #f5f5f5; }
        .message { margin: 10px 0; padding: 15px; border-radius: 8px; max-width: 80%; }
        .message.user { background: #1890ff; color: white; margin-left: auto; }
        .message.assistant { background: white; margin-right: auto; }
        .input-box { padding: 20px; background: white; border-top: 1px solid #ddd; }
        .input-box input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        .input-box button { margin-top: 10px; padding: 12px 24px; background: #1890ff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .sources { font-size: 12px; color: #999; margin-top: 10px; }
        .loading { display: none; text-align: center; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 智能助手</h1>
            <p>隨時隨地為您解答問題</p>
        </div>
        
        <div class="chat-box" id="chatBox">
            <div class="message assistant">
                您好！我是 AI 助手，有什麼可以幫您？
            </div>
        </div>
        
        <div class="loading" id="loading">思考中...</div>
        
        <div class="input-box">
            <input type="text" id="questionInput" placeholder="輸入您的問題..." onkeypress="if(event.keyCode==13) sendMessage()">
            <button onclick="sendMessage()">發送</button>
        </div>
    </div>
    
    <script>
        let sessionId = null;
        
        async function sendMessage() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            if (!question) return;
            
            // 添加用戶消息
            addMessage(question, 'user');
            input.value = '';
            
            // 顯示加載
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        question: question,
                        session_id: sessionId
                    })
                });
                
                const data = await response.json();
                sessionId = data.session_id;
                
                // 添加 AI 回答
                addMessage(data.answer, 'assistant', data.sources);
            } catch (error) {
                addMessage('抱歉，發生錯誤，請稍後再試。', 'assistant');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function addMessage(content, role, sources = null) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${role}`;
            
            let html = `<p>${content}</p>`;
            if (sources && sources.length > 0) {
                html += `<div class="sources">📚 參考來源：${sources.length} 個文檔</div>`;
            }
            
            msgDiv.innerHTML = html;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
```

---

## 二、數據監控與分析

### 2.1 監控儀表板

```python
"""
監控儀表板
"""
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# 模擬數據（實際應從數據庫存儲）
metrics_data = {
    'total_queries': 0,
    'today_queries': 0,
    'avg_latency': 0,
    'error_rate': 0,
    'user_satisfaction': 0,
    'hourly_stats': [],
    'daily_stats': []
}

@app.route('/dashboard')
def dashboard():
    """監控儀表板頁面"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """獲取實時指標"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics_data
    })

@app.route('/api/metrics/hourly')
def get_hourly_metrics():
    """獲取每小時統計"""
    # 返回過去 24 小時數據
    hours = []
    for i in range(24):
        hour = (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:00')
        hours.append({
            'hour': hour,
            'queries': 0,  # 實際從數據庫查詢
            'avg_latency': 0,
            'errors': 0
        })
    return jsonify(hours)

@app.route('/api/metrics/daily')
def get_daily_metrics():
    """獲取每日統計"""
    # 返回過去 30 天數據
    days = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        days.append({
            'date': date,
            'queries': 0,
            'users': 0,
            'satisfaction': 0
        })
    return jsonify(days)

if __name__ == '__main__':
    app.run(port=5004)
```

### 2.2 監控儀表板 HTML

```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>AI 應用監控儀表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f2f5; }
        .header { background: #1890ff; color: white; padding: 20px; margin-bottom: 20px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .metric-value { font-size: 32px; font-weight: bold; color: #1890ff; }
        .metric-label { color: #666; margin-top: 5px; }
        .chart-container { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 AI 應用監控儀表板</h1>
        <p>實時監控應用運行狀態</p>
    </div>
    
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-value" id="totalQueries">0</div>
            <div class="metric-label">總查詢次數</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="todayQueries">0</div>
            <div class="metric-label">今日查詢</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="avgLatency">0ms</div>
            <div class="metric-label">平均響應時間</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="errorRate">0%</div>
            <div class="metric-label">錯誤率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="satisfaction">0</div>
            <div class="metric-label">用戶滿意度</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>24 小時查詢趨勢</h3>
        <canvas id="hourlyChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h3>30 天用戶趨勢</h3>
        <canvas id="dailyChart"></canvas>
    </div>
    
    <script>
        // 實時更新指標
        async function updateMetrics() {
            const response = await fetch('/api/metrics');
            const data = await response.json();
            
            document.getElementById('totalQueries').textContent = data.metrics.total_queries.toLocaleString();
            document.getElementById('todayQueries').textContent = data.metrics.today_queries.toLocaleString();
            document.getElementById('avgLatency').textContent = data.metrics.avg_latency.toFixed(0) + 'ms';
            document.getElementById('errorRate').textContent = data.metrics.error_rate.toFixed(1) + '%';
            document.getElementById('satisfaction').textContent = data.metrics.user_satisfaction.toFixed(1);
        }
        
        // 加載圖表
        async function loadCharts() {
            // 24 小時趨勢
            const hourlyResponse = await fetch('/api/metrics/hourly');
            const hourlyData = await hourlyResponse.json();
            
            new Chart(document.getElementById('hourlyChart'), {
                type: 'line',
                data: {
                    labels: hourlyData.map(d => d.hour),
                    datasets: [{
                        label: '查詢次數',
                        data: hourlyData.map(d => d.queries),
                        borderColor: '#1890ff',
                        tension: 0.1
                    }]
                }
            });
            
            // 30 天趨勢
            const dailyResponse = await fetch('/api/metrics/daily');
            const dailyData = await dailyResponse.json();
            
            new Chart(document.getElementById('dailyChart'), {
                type: 'bar',
                data: {
                    labels: dailyData.map(d => d.date),
                    datasets: [{
                        label: '活躍用戶',
                        data: dailyData.map(d => d.users),
                        backgroundColor: '#1890ff'
                    }]
                }
            });
        }
        
        // 初始化
        updateMetrics();
        loadCharts();
        
        // 每 30 秒更新
        setInterval(updateMetrics, 30000);
    </script>
</body>
</html>
```

---

## 三、A/B 測試

### 3.1 A/B 測試框架

```python
"""
A/B 測試框架
"""
import random
from typing import Dict, List
from datetime import datetime

class ABTest:
    """A/B 測試管理器"""
    
    def __init__(self):
        self.experiments = {}
        self.user_assignments = {}
    
    def create_experiment(self, experiment_id: str, variants: List[str], 
                         traffic_split: List[float]):
        """
        創建 A/B 測試
        
        Args:
            experiment_id: 實驗 ID
            variants: 變體列表 ['A', 'B', 'C']
            traffic_split: 流量分配 [0.5, 0.3, 0.2]
        """
        self.experiments[experiment_id] = {
            'variants': variants,
            'traffic_split': traffic_split,
            'created': datetime.now(),
            'results': {v: {'impressions': 0, 'conversions': 0} for v in variants}
        }
    
    def get_variant(self, experiment_id: str, user_id: str) -> str:
        """
        為用戶分配變體
        
        Args:
            experiment_id: 實驗 ID
            user_id: 用戶 ID
            
        Returns:
            分配的變體（A/B/C）
        """
        # 如果用戶已有分配，返回原分配
        cache_key = f"{experiment_id}:{user_id}"
        if cache_key in self.user_assignments:
            return self.user_assignments[cache_key]
        
        # 新用戶，按流量分配
        experiment = self.experiments[experiment_id]
        rand = random.random()
        
        cumulative = 0
        for i, split in enumerate(experiment['traffic_split']):
            cumulative += split
            if rand < cumulative:
                variant = experiment['variants'][i]
                self.user_assignments[cache_key] = variant
                
                # 記錄曝光
                experiment['results'][variant]['impressions'] += 1
                
                return variant
        
        # 默認最後一個變體
        variant = experiment['variants'][-1]
        self.user_assignments[cache_key] = variant
        experiment['results'][variant]['impressions'] += 1
        return variant
    
    def record_conversion(self, experiment_id: str, user_id: str, variant: str):
        """記錄轉化"""
        if experiment_id in self.experiments:
            self.experiments[experiment_id]['results'][variant]['conversions'] += 1
    
    def get_results(self, experiment_id: str) -> Dict:
        """獲取實驗結果"""
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return {'error': '實驗不存在'}
        
        results = experiment['results']
        
        # 計算轉化率
        for variant in results:
            impressions = results[variant]['impressions']
            conversions = results[variant]['conversions']
            results[variant]['conversion_rate'] = (
                conversions / impressions if impressions > 0 else 0
            )
        
        return {
            'experiment_id': experiment_id,
            'variants': results,
            'winner': max(results.keys(), 
                         key=lambda v: results[v]['conversion_rate'])
        }

# 使用示例
ab_test = ABTest()

# 創建實驗：測試不同模型
ab_test.create_experiment(
    experiment_id='model_comparison',
    variants=['qwen3.5-flash', 'qwen3.5-plus', 'qwen3.5-max'],
    traffic_split=[0.5, 0.3, 0.2]  # 50% 用 Flash，30% 用 Plus，20% 用 Max
)

# 為用戶分配變體
user_id = 'user_123'
variant = ab_test.get_variant('model_comparison', user_id)
print(f"用戶 {user_id} 分配到模型：{variant}")

# 記錄轉化（用戶點贊/滿意）
ab_test.record_conversion('model_comparison', user_id, variant)

# 查看結果
results = ab_test.get_results('model_comparison')
print(f"最佳模型：{results['winner']}")
```

### 3.2 A/B 測試場景

```yaml
場景 1: 模型對比
  變體 A: qwen3.5-flash (低成本)
  變體 B: qwen3.5-plus (平衡)
  變體 C: qwen3.5-max (高質量)
  指標：用戶滿意度、響應時間、成本

場景 2: 提示詞優化
  變體 A: 簡潔版提示詞
  變體 B: 詳細版提示詞
  指標：回答準確率、Token 使用量

場景 3: RAG 配置
  變體 A: Top K = 3
  變體 B: Top K = 5
  變體 C: Top K = 10 + Rerank
  指標：回答準確率、響應時間

場景 4: UI 設計
  變體 A: 簡潔風格
  變體 B: 豐富風格
  指標：用戶停留時間、轉化率
```

---

## 四、用戶反饋收集

### 4.1 反饋系統

```python
"""
用戶反饋收集系統
"""
from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# 存儲反饋
feedbacks = []

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """提交反饋"""
    data = request.json
    
    feedback = {
        'id': len(feedbacks) + 1,
        'timestamp': datetime.now().isoformat(),
        'session_id': data.get('session_id'),
        'question': data.get('question'),
        'answer': data.get('answer'),
        'rating': data.get('rating'),  # 1-5 分
        'comment': data.get('comment', ''),
        'user_id': data.get('user_id'),
        'channel': data.get('channel', 'web')
    }
    
    feedbacks.append(feedback)
    
    # 分析反饋
    if feedback['rating'] <= 2:
        # 低分反饋，發送告警
        send_alert(feedback)
    
    return jsonify({'status': 'ok', 'feedback_id': feedback['id']})

@app.route('/feedback/stats')
def feedback_stats():
    """反饋統計"""
    total = len(feedbacks)
    if total == 0:
        return jsonify({'error': '無反饋數據'})
    
    ratings = [f['rating'] for f in feedbacks if 'rating' in f]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return jsonify({
        'total_feedbacks': total,
        'average_rating': avg_rating,
        'rating_distribution': {
            '5_star': len([r for r in ratings if r == 5]),
            '4_star': len([r for r in ratings if r == 4]),
            '3_star': len([r for r in ratings if r == 3]),
            '2_star': len([r for r in ratings if r == 2]),
            '1_star': len([r for r in ratings if r == 1])
        }
    })

def send_alert(feedback):
    """發送低分反饋告警"""
    # 可以集成釘釘、郵件等
    print(f"⚠️ 低分反饋警報：{feedback['rating']}分 - {feedback['comment']}")

if __name__ == '__main__':
    app.run(port=5005)
```

### 4.2 反饋收集 UI

```html
<!-- 反饋組件 -->
<div class="feedback-section">
    <p>對本次回答滿意嗎？</p>
    <div class="rating">
        <span onclick="rate(5)">⭐</span>
        <span onclick="rate(4)">⭐</span>
        <span onclick="rate(3)">⭐</span>
        <span onclick="rate(2)">⭐</span>
        <span onclick="rate(1)">⭐</span>
    </div>
    <textarea id="feedbackComment" placeholder="請告訴我們哪裡可以改進..."></textarea>
    <button onclick="submitFeedback()">提交反饋</button>
</div>

<script>
let currentRating = 0;

function rate(stars) {
    currentRating = stars;
    // 更新 UI 顯示
    const ratingDiv = document.querySelector('.rating');
    const spans = ratingDiv.querySelectorAll('span');
    spans.forEach((span, i) => {
        span.style.color = i < stars ? '#ffc107' : '#ddd';
    });
}

async function submitFeedback() {
    if (currentRating === 0) {
        alert('請先評分');
        return;
    }
    
    const comment = document.getElementById('feedbackComment').value;
    
    await fetch('/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            session_id: sessionId,
            question: lastQuestion,
            answer: lastAnswer,
            rating: currentRating,
            comment: comment
        })
    });
    
    alert('感謝您的反饋！');
    currentRating = 0;
    document.getElementById('feedbackComment').value = '';
}
</script>
```

---

## 五、完整應用上線清單

### 5.1 上線前檢查

```markdown
## 技術檢查
- [ ] 代碼已測試（單元測試、集成測試）
- [ ] 性能測試通過（响应時間 < 2 秒）
- [ ] 壓力測試通過（支持 100+ 併發）
- [ ] 錯誤處理完善
- [ ] 日誌記錄完整
- [ ] 監控告警配置

## 安全檢查
- [ ] API Key 未硬編碼
- [ ] 輸入驗證啟用
- [ ] SQL 注入防護
- [ ] XSS 防護
- [ ] HTTPS 配置
- [ ] 權限控制

## 數據檢查
- [ ] 知識庫已更新
- [ ] 測試數據已清理
- [ ] 備份策略配置
- [ ] 數據合規檢查

## 運維檢查
- [ ] 服務器資源充足
- [ ] 自動伸縮配置
- [ ] 災難恢復預案
- [ ] 監控儀表板就緒

## 文檔檢查
- [ ] 用戶手冊完成
- [ ] API 文檔完成
- [ ] 故障排查指南
- [ ] 聯繫方式明確
```

### 5.2 上線流程

```bash
# 1. 最後測試
python test_all.py

# 2. 備份當前版本
git tag v1.0.0
git push origin v1.0.0

# 3. 部署到生產
scp -r app.py templates/ user@server:/opt/ai-app/

# 4. 重啟服務
ssh user@server "sudo systemctl restart ai-app"

# 5. 健康檢查
curl https://your-domain.com/health

# 6. 監控確認
# 查看儀表板，確認指標正常

# 7. 通知團隊
# 發送上線通知到釘釘/微信群
```

### 5.3 上線後監控

```python
"""
上線後監控腳本
"""
import requests
import time
from datetime import datetime

def health_check():
    """健康檢查"""
    try:
        response = requests.get('https://your-domain.com/health', timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✅ 健康檢查通過")
            return True
        else:
            print(f"[{datetime.now()}] ❌ 健康檢查失敗：{response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ 健康檢查異常：{e}")
        return False

def performance_check():
    """性能檢查"""
    start = time.time()
    response = requests.post('https://your-domain.com/api/query', 
                           json={'question': '測試'})
    latency = (time.time() - start) * 1000
    
    if latency < 2000:
        print(f"[{datetime.now()}] ✅ 性能正常：{latency:.0f}ms")
        return True
    else:
        print(f"[{datetime.now()}] ⚠️ 性能警告：{latency:.0f}ms")
        return False

# 每 5 分鐘檢查一次
while True:
    health_check()
    performance_check()
    time.sleep(300)
```

---

## 六、5 天進階課程總結

### 6.1 技能總覽

| Day | 主題 | 核心技能 | 實戰項目 |
|-----|------|---------|---------|
| **Day 1** | Agent 編排 | System Prompt、插件系統、MCP 協議 | 智能客服 Agent |
| **Day 2** | RAG 知識庫 | 向量檢索、文檔分段、Rerank | RAG 引擎系統 |
| **Day 3** | 工作流編排 | 節點系統、條件分支、API 集成 | 自動化審批流 |
| **Day 4** | 模型微調 | SFT、DPO、模型評估、成本優化 | 行業專屬模型 |
| **Day 5** | 應用發布 | 多渠道、監控、A/B 測試、反饋 | 完整生產系統 |

### 6.2 代碼總量

```
Day 1: 8.5KB 筆記
Day 2: 8.9KB 筆記 + 800 行代碼
Day 3: 700 行代碼
Day 4: 11KB 指南
Day 5: 12KB 指南 + 500 行代碼

總計:
- 筆記/指南：~40KB
- 代碼：2000+ 行
- 實戰項目：5 個完整系統
```

### 6.3 能力模型

```
初級 → 中級 → 高級

初級（完成 Day 1-2）:
✅ 創建簡單 Agent
✅ 配置基礎知識庫
⚠️ 需要指導完成項目

中級（完成 Day 3-4）:
✅ 獨立開發完整應用
✅ 性能優化與安全配置
✅ 模型微調能力
⚠️ 需要經驗積累

高級（完成 Day 5）:
✅ 設計高可用架構
✅ 多渠道發布與運營
✅ 數據驅動優化
✅ 指導團隊成員
```

---

## 七、下一步建議

### 7.1 實戰項目

```
推薦項目（三選一）:

1. 企業智能客服系統
   - 釘釘/微信集成
   - 知識庫 RAG
   - 人工客服轉接
   - 數據分析儀表板

2. 行業知識助手
   - 專業領域微調
   - 多知識庫融合
   - 權限管理
   - 審計日誌

3. 自動化審批平台
   - 工作流編排
   - 多級審批
   - API 集成
   - 移動端適配
```

### 7.2 持續學習

```
技術深度:
- 學習 Kubernetes 部署
- 深入研究向量數據庫
- 掌握更多微調技巧

業務廣度:
- 了解行業最佳實踐
- 學習產品運營知識
- 關注 AI 最新發展

認證路線:
- ACA 人工智能工程師
- ACP 人工智能專家
- ACE 人工智能架構師
```

### 7.3 變現路徑

```
1. 技術服務
   - 企業 AI 諮詢
   - 系統開發外包
   - 技術培訓

2. 產品化
   - SaaS 服務
   - 行業解決方案
   - API 服務

3. 內容變現
   - 技術博客
   - 在線課程
   - 技術書籍
```

---

**完成時間:** 2026-03-18  
**狀態:** ✅ Day 5 完成  
**5 天進階課程:** ✅ 100% 完成！

**老胡，恭喜你完成整個阿里雲 AI 應用進階課程！** 🎉
