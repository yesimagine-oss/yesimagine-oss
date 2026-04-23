import os
import sys
import datetime
import json
import hashlib
import time
import random
import shutil

def calculate_sha256(file_path):
    """
    计算文件的SHA256哈希值
    """
    with open(file_path, 'rb') as f:
        data = f.read()
        sha256_hash = hashlib.sha256(data).hexdigest()
        return sha256_hash

def verify_signature(file_path, expected_signature):
    """
    验证文件签名
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 检查签名是否存在
        if content.endswith(expected_signature):
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ 验证签名失败: {e}")
        return False

def add_signature_to_file(file_path, signature):
    """
    在文件末尾添加数字签名
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 添加签名到文件末尾
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content + '\n\n' + signature)
        print(f"✅ 签名已添加到 {file_path}")
    except Exception as e:
        print(f"❌ 添加签名失败: {e}")

def main():
    """
    主函数：为所有Python文件添加数字签名
    """
    # 获取当前目录下的所有Python文件
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    # 生成签名
    signature = "EVO_MAP_WORKBENCH_MIN_SIGNATURE_1.0.11"
    
    # 为每个Python文件添加签名
    for file in python_files:
        file_path = os.path.join(os.getcwd(), file)
        add_signature_to_file(file_path, signature)

if __name__ == "__main__":
    main()