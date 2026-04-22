# 飛書機器人配置指南

## 場景

您在外面（手機）→ 看到網頁 → 發給飛書機器人 → 家裡 goEX 抓取 → 保存到知識庫

---

## 配置步驟

### 1. 飛書開放平台創建機器人

1. 訪問 https://open.feishu.cn/app
2. 創建自建應用
3. 添加「機器人」能力
4. 獲取 App ID 和 App Secret

### 2. 配置飛書機器人 web hook

**當前 goEX HTTP 服務**:
```
URL: http://家裡 IP:8081/wiki
方法：POST
請求格式：{"url": "https://..."}
```

**內網穿透**（如果家裡沒有公網 IP）:
```bash
# 使用 frp/ngrok/cloudflared
# 示例：cloudflared
cloudflared tunnel --url http://localhost:8081
# 獲得：https://xxx.ngrok.io
```

### 3. 飛書機器人配置

**事件訂閱**:
- 訂閱 `im.message.receive_v1`
- 驗證 URL: `https://xxx.ngrok.io/feishu/verify`

**機器人配置**:
```yaml
命令：/wiki
觸發：收到 URL 或 /wiki 開頭的消息
動作：轉發到 goEX HTTP API
```

### 4. 飛書機器人代碼（可選）

如果您有自己的飛書機器人服務：

```python
# feishu_bot.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
GOEX_URL = "http://localhost:8081/wiki"

@app.route('/feishu/message', methods=['POST'])
def handle_message():
    data = request.json
    # 提取消息中的 URL
    content = data.get('content', '')
    url = extract_url(content)
    
    if url:
        # 調用 goEX
        response = requests.post(GOEX_URL, json={'url': url})
        result = response.json()
        
        if result['success']:
            return jsonify({
                'text': f"✅ 已抓取到知識庫\n文件：{result['file']}"
            })
        else:
            return jsonify({
                'text': f"❌ 抓取失敗：{result['error']}"
            })
    
    return jsonify({'text': '請發送 URL 或使用 /wiki https://url'})

def extract_url(text):
    import re
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else None

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 使用示例

### 飛書聊天中

```
用戶：https://evomap.ai/zh/atp

機器人：✅ 已抓取到知識庫
       文件：RedAgentTeamllm-wiki/raw/general/evomap_ai_zh_atp.md
       auto-ingest.py 會自動編譯入庫（每日 05:00）
```

### 或使用命令

```
用戶：/wiki https://evomap.ai/zh/atp

機器人：✅ 已抓取到知識庫
       文件：RedAgentTeamllm-wiki/raw/general/evomap_ai_zh_atp.md
```

---

## 快速測試

### 本地測試

```bash
# 1. 啟動 goEX HTTP 服務
cd ~/.goex && ./goEX --http-server :8081

# 2. 測試 API
curl -X POST http://localhost:8081/wiki \
  -H "Content-Type: application/json" \
  -d '{"url":"https://evomap.ai/zh/atp"}'

# 3. 查看結果
ls -lh RedAgentTeamllm-wiki/raw/general/
```

### 遠程測試（需要內網穿透）

```bash
# 1. 啟動內網穿透
cloudflared tunnel --url http://localhost:8081
# 獲得：https://xxx.ngrok.io

# 2. 測試遠程 API
curl -X POST https://xxx.ngrok.io/wiki \
  -H "Content-Type: application/json" \
  -d '{"url":"https://evomap.ai/zh/atp"}'
```

---

## 當前狀態

✅ goEX HTTP 服務已實現
✅ API 測試成功
⏳ 飛書機器人配置（需用戶確認）
⏳ 內網穿透配置（如需遠程訪問）

---

## 下一步

1. 確認是否需要內網穿透
2. 配置飛書機器人
3. 測試遠程抓取
