# 🔐 OAuth 2.0 授权完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L2-L3

---

## 📋 OAuth 2.0 概述

### 什么是 OAuth 2.0

```
OAuth 2.0 是一种授权协议，允许用户授权第三方应用访问其资源，
而无需将用户名和密码提供给第三方应用。

飞书开放平台使用 OAuth 2.0 进行用户授权。
```

### 授权流程

```
┌─────────┐      ┌─────────┐      ┌─────────┐
│  用户   │      │  应用   │      │  飞书   │
└────┬────┘      └────┬────┘      └────┬────┘
     │                │                │
     │  1. 点击授权   │                │
     │───────────────>│                │
     │                │                │
     │                │  2. 重定向授权 │
     │───────────────────────────────>│
     │                │                │
     │  3. 用户登录   │                │
     │<───────────────────────────────│
     │   并同意授权   │                │
     │                │                │
     │  4. 返回 Code  │                │
     │<───────────────────────────────│
     │                │                │
     │  5. 发送 Code  │                │
     │───────────────>│                │
     │                │                │
     │                │  6. 换取 Token │
     │                │───────────────>│
     │                │                │
     │                │  7. 返回 Token │
     │                │<───────────────│
     │                │                │
     │                │  8. 使用 Token │
     │                │───────────────>│
     │                │                │
     │                │  9. 返回数据   │
     │                │<───────────────│
     │                │                │

═══════════════════════════════════════
步骤说明:
1. 用户点击应用的授权按钮
2. 应用重定向用户到飞书授权页面
3. 用户登录飞书并同意授权
4. 飞书重定向回应用，附带授权码 (Code)
5. 应用获取授权码
6. 应用用授权码换取 Access Token
7. 飞书返回 Access Token 和 Refresh Token
8. 应用使用 Access Token 访问 API
9. 飞书返回请求的数据
═══════════════════════════════════════
```

---

## 🔑 授权模式

### 授权码模式（推荐）

```
适用场景：Web 应用、服务端应用

流程:
1. 构建授权 URL
2. 用户授权
3. 获取授权码
4. 换取 Access Token

优点:
✅ 安全性高（Code 一次性使用）
✅ Token 不经过浏览器
✅ 支持 Refresh Token

缺点:
❌ 需要服务端
❌ 流程较复杂
```

### 隐式授权模式

```
适用场景：单页应用 (SPA)、移动端

流程:
1. 构建授权 URL
2. 用户授权
3. 直接返回 Access Token

优点:
✅ 流程简单
✅ 无需服务端

缺点:
❌ 安全性较低
❌ Token 暴露在 URL 中
❌ 不支持 Refresh Token
```

---

## 🛠️ 实战实现

### 1. 创建飞书应用

```
步骤:
1. 访问 https://open.feishu.cn/
2. 登录开发者后台
3. 创建应用
4. 配置重定向 URI
5. 获取 App ID 和 App Secret
6. 开启 OAuth 权限
```

### 2. 配置重定向 URI

```
示例:
https://yourdomain.com/oauth/callback
http://localhost:8080/oauth/callback

注意:
- 必须与授权 URL 中的一致
- 支持多个重定向 URI
- 生产环境使用 HTTPS
```

### 3. 构建授权 URL

```python
import urllib.parse

def build_auth_url(app_id, redirect_uri, state=None):
    """
    构建授权 URL
    
    Args:
        app_id: 应用 ID
        redirect_uri: 重定向 URI
        state: 状态参数（防 CSRF）
    
    Returns:
        str: 授权 URL
    """
    base_url = "https://open.feishu.cn/open-apis/authen/v1/authorize"
    
    params = {
        "app_id": app_id,
        "redirect_uri": redirect_uri,
        "state": state or "random_state_string",
        "response_type": "code"
    }
    
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"

# 使用示例
auth_url = build_auth_url(
    app_id="cli_xxxxx",
    redirect_uri="https://yourdomain.com/oauth/callback",
    state="random_state_123"
)

print(f"授权 URL: {auth_url}")
```

### 4. 处理授权回调

```python
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/oauth/callback')
def oauth_callback():
    """处理 OAuth 回调"""
    # 获取授权码
    code = request.args.get('code')
    state = request.args.get('state')
    
    # 验证 state（防 CSRF）
    if state != session.get('oauth_state'):
        return "Invalid state", 400
    
    # 用授权码换取 Token
    token_info = get_access_token(code)
    
    # 保存 Token
    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    
    return redirect('/dashboard')
```

### 5. 换取 Access Token

```python
import requests

def get_access_token(code, app_id, app_secret, redirect_uri):
    """
    用授权码换取 Access Token
    
    Args:
        code: 授权码
        app_id: 应用 ID
        app_secret: 应用 Secret
        redirect_uri: 重定向 URI
    
    Returns:
        dict: Token 信息
    """
    url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
    
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": redirect_uri
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return {
            "access_token": result["data"]["access_token"],
            "refresh_token": result["data"]["refresh_token"],
            "expires_in": result["data"]["expires_in"],
            "token_type": result["data"]["token_type"]
        }
    else:
        raise Exception(f"获取 Token 失败：{result.get('msg')}")
```

### 6. 刷新 Access Token

```python
def refresh_access_token(refresh_token, app_id, app_secret):
    """
    刷新 Access Token
    
    Args:
        refresh_token: Refresh Token
        app_id: 应用 ID
        app_secret: 应用 Secret
    
    Returns:
        dict: 新 Token 信息
    """
    url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
    
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": app_id,
        "client_secret": app_secret
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return {
            "access_token": result["data"]["access_token"],
            "refresh_token": result["data"]["refresh_token"],
            "expires_in": result["data"]["expires_in"]
        }
    else:
        raise Exception(f"刷新 Token 失败：{result.get('msg')}")
```

### 7. 获取用户信息

```python
def get_user_info(access_token):
    """
    获取用户信息
    
    Args:
        access_token: Access Token
    
    Returns:
        dict: 用户信息
    """
    url = "https://open.feishu.cn/open-apis/authen/v1/user_info"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"获取用户信息失败：{result.get('msg')}")
```

---

## 🔐 安全最佳实践

### 1. State 参数防 CSRF

```python
import secrets

# 生成随机 state
state = secrets.token_urlsafe(32)
session['oauth_state'] = state

# 构建授权 URL 时包含 state
auth_url = build_auth_url(app_id, redirect_uri, state)

# 回调时验证 state
if request.args.get('state') != session['oauth_state']:
    return "Invalid state", 400
```

### 2. Token 安全存储

```python
# ❌ 错误：明文存储
session['access_token'] = token

# ✅ 正确：加密存储
from cryptography.fernet import Fernet

cipher = Fernet(secret_key)
encrypted_token = cipher.encrypt(token.encode())
session['access_token'] = encrypted_token

# 使用时解密
token = cipher.decrypt(encrypted_token).decode()
```

### 3. Token 自动刷新

```python
import time

class TokenManager:
    def __init__(self, access_token, refresh_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = time.time() + expires_in - 300  # 提前 5 分钟刷新
    
    def get_access_token(self):
        """获取有效的 Access Token"""
        if time.time() >= self.expires_at:
            # Token 过期，刷新
            self.refresh()
        return self.access_token
    
    def refresh(self):
        """刷新 Token"""
        token_info = refresh_access_token(
            self.refresh_token,
            app_id,
            app_secret
        )
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.expires_at = time.time() + token_info['expires_in'] - 300
```

### 4. 权限最小化

```
申请权限原则:
✅ 只申请需要的权限
✅ 明确告知用户用途
✅ 定期审查权限
✅ 及时撤销不用的权限

示例:
如果只需要读取用户信息:
- 申请：user_info
- 不要申请：message.send, calendar.write
```

---

## 📊 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | - |
| 99991663 | Token 无效 | 重新授权 |
| 99991665 | 没有权限 | 检查权限配置 |
| 99991666 | 参数错误 | 检查请求参数 |
| 99991667 | 频率超限 | 降低请求频率 |
| 1001 | Code 已使用 | 重新授权 |
| 1002 | Code 过期 | 重新授权 |
| 1003 | Redirect URI 不匹配 | 检查配置 |

### 错误处理示例

```python
class OAuthError(Exception):
    """OAuth 错误基类"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)

def handle_oauth_error(result):
    """处理 OAuth 错误"""
    code = result.get("code")
    msg = result.get("msg")
    
    if code == 0:
        return
    
    error_map = {
        1001: "授权码已使用，请重新授权",
        1002: "授权码已过期，请重新授权",
        1003: "重定向 URI 不匹配",
        99991663: "Token 无效，请重新登录",
        99991665: "没有权限，请联系管理员",
    }
    
    error_msg = error_map.get(code, msg)
    raise OAuthError(code, error_msg)
```

---

## 📝 完整示例

### Flask OAuth 完整示例

```python
from flask import Flask, redirect, request, session, url_for
import requests
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

# 配置
APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")
REDIRECT_URI = "http://localhost:5000/oauth/callback"

class FeishuOAuth:
    """飞书 OAuth 客户端"""
    
    def __init__(self, app_id, app_secret, redirect_uri):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.base_url = "https://open.feishu.cn/open-apis/authen/v1"
    
    def get_authorization_url(self, state=None):
        """获取授权 URL"""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "app_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "response_type": "code"
        }
        
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.base_url}/authorize?{query}", state
    
    def get_access_token(self, code):
        """获取 Access Token"""
        url = f"{self.base_url}/access_token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取 Token 失败：{result.get('msg')}")
        
        return result["data"]
    
    def refresh_access_token(self, refresh_token):
        """刷新 Access Token"""
        url = f"{self.base_url}/refresh_access_token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.app_id,
            "client_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"刷新 Token 失败：{result.get('msg')}")
        
        return result["data"]
    
    def get_user_info(self, access_token):
        """获取用户信息"""
        url = f"{self.base_url}/user_info"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取用户信息失败：{result.get('msg')}")
        
        return result["data"]

# 初始化 OAuth 客户端
oauth = FeishuOAuth(APP_ID, APP_SECRET, REDIRECT_URI)

@app.route('/')
def index():
    """首页"""
    if 'access_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """登录"""
    auth_url, state = oauth.get_authorization_url()
    session['oauth_state'] = state
    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    """OAuth 回调"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    # 验证 state
    if state != session.get('oauth_state'):
        return "Invalid state", 400
    
    # 获取 Token
    token_info = oauth.get_access_token(code)
    
    # 保存 Token
    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """用户仪表盘"""
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    try:
        user_info = oauth.get_user_info(session['access_token'])
        return f"""
        <h1>欢迎，{user_info.get('name')}</h1>
        <p>用户 ID: {user_info.get('user_id')}</p>
        <p>邮箱：{user_info.get('email')}</p>
        <a href="{url_for('logout')}">退出登录</a>
        """
    except Exception as e:
        return f"错误：{e}", 500

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 📚 学习资源

### 官方文档

- 飞书 OAuth 文档：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- OAuth 2.0 规范：https://oauth.net/2/
- 飞书应用权限：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

### 示例代码

- GitHub 示例：https://github.com/openclaw/feishu-oauth-examples
- Flask OAuth: https://github.com/openclaw/feishu-flask-oauth

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L2-L3

🔐 **OAuth 2.0 完整指南已创建！包含完整实现代码和安全最佳实践！**
