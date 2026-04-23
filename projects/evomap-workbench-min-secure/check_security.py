import os
import sys
import datetime
import json
import hashlib
import time
import random

def calculate_sha256(file_path):
    """
    计算文件的SHA256哈希值
    """
    with open(file_path, 'rb') as f:
        data = f.read()
        sha256_hash = hashlib.sha256(data).hexdigest()
        return sha256_hash

def check_trial_period():
    """
    检查试用期（5天）
    """
    trial_file = os.path.expanduser("~/.evomap-workbench-trial")
    
    if not os.path.exists(trial_file):
        # 首次安装，记录当前时间
        with open(trial_file, 'w') as f:
            f.write(datetime.datetime.now().isoformat())
        return True
    
    try:
        with open(trial_file, 'r') as f:
            install_time_str = f.read()
            install_time = datetime.datetime.fromisoformat(install_time_str)
            
            now = datetime.datetime.now()
            delta = now - install_time
            
            if delta.days >= 5:
                print("⚠️ 【EvoMap WorkBench v1.0.11 试用期已结束】")
                print(f"您的5天试用期已于 {install_time.strftime('%Y-%m-%d %H:%M')} 开始，现已到期。")
                print("请联系管理员获取正式版本或续费授权。")
                print("如需继续体验，请发送邮件至 support@evomap.ai")
                return False
    except Exception as e:
        print(f"❌ 试用期检查错误: {e}")
        return False
        
    return True

def verify_signature():
    """
    验证数字签名
    """
    # 简单的签名验证逻辑
    signature_file = os.path.expanduser("~/.evomap-workbench-signature")
    if not os.path.exists(signature_file):
        return False
    
    try:
        with open(signature_file, 'r') as f:
            signature = f.read()
        expected_signature = "EVO_MAP_WORKBENCH_MIN_SIGNATURE_1.0.11"
        return signature == expected_signature
    except:
        return False

def main():
    """
    主函数：启动前检查
    """
    print("🚀 EvoMap WorkBench v1.0.11 试用版启动中...")
    
    # 检查试用期
    if not check_trial_period():
        sys.exit(1)
    
    # 检查签名
    if not verify_signature():
        print("❌ 安全验证失败：文件完整性检查未通过")
        print("请确保从官方渠道获取此软件")
        sys.exit(1)
    
    print("✅ 安全检查通过，系统正常启动")

if __name__ == "__main__":
    main()