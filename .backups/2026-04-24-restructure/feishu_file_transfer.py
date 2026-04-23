import requests
import json
import base64
import os

def get_tenant_access_token(app_id, app_secret):
    """
    获取飞书租户访问令牌
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json().get("tenant_access_token")
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取令牌失败: {e}")
        return None

def upload_file_to_feishu(file_path, token):
    """
    上传文件到飞书
    """
    # 读取文件
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Base64编码
    file_base64 = base64.b64encode(file_data).decode('utf-8')
    
    # 获取文件名
    file_name = os.path.basename(file_path)
    
    # 上传文件到飞书
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "file_name": file_name,
        "parent_type": "explorer",
        "parent_node": "root",
        "size": os.path.getsize(file_path),
        "content": file_base64
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 文件上传失败: {e}")
        return None

def send_file_message(chat_id, file_token, token):
    """
    发送文件消息
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "chat_id": chat_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_token})
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 消息发送失败: {e}")
        return None

if __name__ == "__main__":
    # 飞书凭证
    app_id = "cli_a929676f8bf81cc7"
    app_secret = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
    chat_id = "default"  # 默认聊天ID
    
    # 获取访问令牌
    token = get_tenant_access_token(app_id, app_secret)
    if not token:
        print("❌ 无法获取访问令牌")
        sys.exit(1)
    print("✅ 获取访问令牌成功")
    
    # 上传文件
    file_path = "/home/admin/.openclaw/workspace/evomap-workbench-min-secure.tar.gz"
    file_upload_response = upload_file_to_feishu(file_path, token)
    if not file_upload_response or "file_token" not in file_upload_response:
        print(f"❌ 文件上传失败: {file_upload_response}")
        sys.exit(1)
    file_token = file_upload_response["file_token"]
    print(f"✅ 文件上传成功: {file_token}")
    
    # 发送文件消息
    message_response = send_file_message(chat_id, file_token, token)
    print(json.dumps({"file_upload": file_upload_response, "message": message_response}, indent=4))