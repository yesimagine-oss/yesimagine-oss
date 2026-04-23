import requests
import json
import base64
import os

def upload_file_to_feishu(file_path, tenant_access_token):
    # 读取文件
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # 将文件转换为base64
    file_base64 = base64.b64encode(file_data).decode('utf-8')
    
    # 获取文件名
    file_name = os.path.basename(file_path)
    
    # 上传文件到飞书
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "file_name": file_name,
        "parent_type": "explorer",
        "parent_node": "root",
        "size": os.path.getsize(file_path),
        "content": file_base64
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()