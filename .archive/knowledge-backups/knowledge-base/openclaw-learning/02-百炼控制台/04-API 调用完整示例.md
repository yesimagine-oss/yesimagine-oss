# 百炼 API 调用完整示例

**学习时间**: 2026-03-12 11:20
**难度**: ⭐⭐⭐ 进阶
**预计时间**: 45 分钟

---

## 🔑 前置准备

### 获取 API Key

1. 登录百炼控制台
2. 进入「API-KEY 管理」
3. 创建新 Key
4. 安全保存 Key

---

## 📝 基础调用示例

### cURL 调用

```bash
curl -X POST "https://coding.dashscope.aliyuncs.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-YOUR_API_KEY" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "max_tokens": 1000
  }'
```

### 响应示例

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "qwen3.5-plus",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "你好！有什么可以帮你的吗？"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

---

## 🐍 Python 示例

### 基础调用

```python
import requests
import json

API_KEY = "sk-YOUR_API_KEY"
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

def chat(prompt, model="qwen3.5-plus"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error: {response.text}")

# 使用示例
response = chat("你好，请介绍一下自己")
print(response)
```

### 流式调用

```python
import requests
import json

def chat_stream(prompt, model="qwen3.5-plus"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data["choices"][0]["delta"].get("content"):
                    print(data["choices"][0]["delta"]["content"], end="", flush=True)

# 使用示例
chat_stream("写一首关于春天的诗")
```

### 带错误处理

```python
import requests
import time
from typing import Optional

class APIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

def chat_with_retry(
    prompt: str,
    model: str = "qwen3.5-plus",
    max_retries: int = 3,
    timeout: int = 30
) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            
            elif response.status_code == 429:
                # 速率限制，等待后重试
                wait_time = 2 ** attempt
                print(f"速率限制，等待 {wait_time}秒后重试...")
                time.sleep(wait_time)
                
            elif response.status_code >= 500:
                # 服务器错误，重试
                print(f"服务器错误，重试...")
                time.sleep(1)
                
            else:
                # 其他错误，抛出异常
                raise APIError(
                    response.status_code,
                    response.json().get("error", {}).get("message", "Unknown error")
                )
                
        except requests.exceptions.Timeout:
            print(f"请求超时，重试...")
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"网络错误：{e}")
            raise
    
    raise APIError(0, "达到最大重试次数")

# 使用示例
try:
    response = chat_with_retry("你好")
    print(response)
except APIError as e:
    print(f"API 调用失败：{e}")
```

---

## 📜 Node.js 示例

### 基础调用

```javascript
const axios = require('axios');

const API_KEY = 'sk-YOUR_API_KEY';
const BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1';

async function chat(prompt, model = 'qwen3.5-plus') {
  try {
    const response = await axios.post(
      `${BASE_URL}/chat/completions`,
      {
        model: model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 1000
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        }
      }
    );
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
}

// 使用示例
chat('你好').then(console.log);
```

### 流式调用

```javascript
const axios = require('axios');

async function chatStream(prompt, model = 'qwen3.5-plus') {
  const response = await axios.post(
    `${BASE_URL}/chat/completions`,
    {
      model: model,
      messages: [{ role: 'user', content: prompt }],
      stream: true
    },
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      responseType: 'stream'
    }
  );
  
  response.data.on('data', (chunk) => {
    const lines = chunk.toString().split('\n');
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        const content = data.choices[0]?.delta?.content;
        if (content) {
          process.stdout.write(content);
        }
      }
    }
  });
}

// 使用示例
chatStream('写一首诗');
```

---

## 🛠️ 高级用法

### 多轮对话

```python
def multi_turn_chat():
    messages = []
    
    while True:
        user_input = input("你：")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        messages.append({"role": "user", "content": user_input})
        
        response = chat_with_history(messages)
        print(f"AI: {response}")
        
        messages.append({"role": "assistant", "content": response})

def chat_with_history(messages, model="qwen3.5-plus"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data
    )
    
    return response.json()["choices"][0]["message"]["content"]

# 使用示例
multi_turn_chat()
```

### 图像理解

```python
import base64

def chat_with_image(image_path, prompt, model="qwen3.5-plus"):
    # 读取并编码图片
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data
    )
    
    return response.json()["choices"][0]["message"]["content"]

# 使用示例
response = chat_with_image("image.jpg", "这张图片里有什么？")
print(response)
```

### 函数调用

```python
def chat_with_functions(prompt, functions, model="qwen3.5-plus"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "functions": functions,
        "function_call": "auto"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data
    )
    
    result = response.json()
    message = result["choices"][0]["message"]
    
    if message.get("function_call"):
        # 需要调用函数
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])
        return call_function(function_name, function_args)
    
    return message["content"]

def call_function(name, args):
    # 实现函数调用逻辑
    pass

# 使用示例
functions = [
    {
        "name": "get_weather",
        "description": "获取天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    }
]

response = chat_with_functions("北京今天天气怎么样？", functions)
print(response)
```

---

## ⚠️ 错误处理

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求格式 |
| 401 | 认证失败 | 检查 API Key |
| 403 | 权限不足 | 检查 Key 权限 |
| 429 | 请求过多 | 降低频率或等待 |
| 500 | 服务器错误 | 稍后重试 |
| 503 | 服务不可用 | 检查服务状态 |

### 错误处理示例

```python
def handle_api_error(error):
    if error.status_code == 401:
        return "API Key 无效，请检查配置"
    elif error.status_code == 429:
        return "请求过于频繁，请稍后再试"
    elif error.status_code >= 500:
        return "服务器错误，请稍后重试"
    else:
        return f"未知错误：{error.message}"
```

---

## ✅ 验收清单

- [ ] 已获取 API Key
- [ ] 基础调用测试通过
- [ ] 流式调用测试通过
- [ ] 错误处理已实现
- [ ] 多轮对话已测试

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容
