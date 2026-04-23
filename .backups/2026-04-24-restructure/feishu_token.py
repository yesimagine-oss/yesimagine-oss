import requests
import json

def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 使用用户提供的凭证
app_id = "cli_a929676f8bf81cc7"
app_secret = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"

# 获取租户访问令牌
token_response = get_tenant_access_token(app_id, app_secret)
print(json.dumps(token_response, indent=4))