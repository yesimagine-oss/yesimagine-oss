#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日健康檢查腳本
每天 01:00 執行，檢查所有系統狀態

檢查項目：
1. Crontab 配置
2. 腳本文件存在
3. 日誌目錄可寫入
4. 飛書通知正常
5. 發送健康報告
"""

import sys
import os
from datetime import datetime
import subprocess

# 添加工作區到路徑
tools_path = '/home/admin/.openclaw/workspace/tools'
sys.path.insert(0, tools_path)
os.chdir(tools_path)

# 導入 task_notifier
import importlib.util
spec = importlib.util.spec_from_file_location("task_notifier", os.path.join(tools_path, "task-notifier.py"))
task_notifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_notifier)
send_feishu_message = task_notifier.send_feishu_message
get_feishu_token = task_notifier.get_feishu_token
load_config = task_notifier.load_config

def check_crontab():
    """檢查 Crontab 配置"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=10)
        if 'EvoMap' in result.stdout:
            return True, 'Crontab 配置正常'
        else:
            return False, 'Crontab 缺少 EvoMap 配置'
    except Exception as e:
        return False, f'Crontab 檢查失敗：{str(e)}'

def check_scripts():
    """檢查腳本文件"""
    scripts = [
        '/home/admin/.openclaw/workspace/EvoMap 項目/scripts/morning_check.py',
        '/home/admin/.openclaw/workspace/EvoMap 項目/scripts/task_reminder.py',
        '/home/admin/.openclaw/workspace/EvoMap 項目/scripts/content_reminder.py',
        '/home/admin/.openclaw/workspace/EvoMap 項目/scripts/community_reminder.py',
        '/home/admin/.openclaw/workspace/EvoMap 項目/scripts/daily_summary.py',
    ]
    
    missing = []
    for script in scripts:
        if not os.path.exists(script):
            missing.append(os.path.basename(script))
    
    if missing:
        return False, f'缺少腳本：{", ".join(missing)}'
    else:
        return True, '所有腳本存在'

def check_logs():
    """檢查日誌目錄"""
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    if not os.path.exists(log_dir):
        return False, '日誌目錄不存在'
    
    if not os.access(log_dir, os.W_OK):
        return False, '日誌目錄不可寫入'
    
    return True, '日誌目錄正常'

def check_feishu():
    """檢查飛書通知"""
    try:
        config = load_config()
        token = get_feishu_token(config['app_id'], config['app_secret'])
        # 發送測試消息
        send_feishu_message(token, config['target_user'], '🏥 系統健康檢查', '系統檢查正常')
        return True, '飛書通知正常'
    except Exception as e:
        return False, f'飛書通知失敗：{str(e)}'

def generate_report():
    """生成健康檢查報告"""
    checks = [
        ('Crontab 配置', check_crontab()),
        ('腳本文件', check_scripts()),
        ('日誌目錄', check_logs()),
        ('飛書通知', check_feishu()),
    ]
    
    all_passed = all(result[0] for result in checks)
    
    report = f"""
🏥 系統健康檢查報告

檢查時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

檢查結果：
"""
    
    for name, (passed, message) in checks:
        icon = '✅' if passed else '❌'
        report += f"{icon} {name}: {message}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

總體狀態：{'✅ 正常' if all_passed else '❌ 異常，請立即檢查'}

"""
    
    if not all_passed:
        report += """
⚠️ 發現問題：
"""
        for name, (passed, message) in checks:
            if not passed:
                report += f"- {name}: {message}\n"
    
    return all_passed, report

def main():
    """主函數"""
    all_passed, report = generate_report()
    
    # 發送飛書通知
    try:
        config = load_config()
        token = get_feishu_token(config['app_id'], config['app_secret'])
        send_feishu_message(
            token, 
            config['target_user'], 
            '🏥 系統健康檢查' + ('✅' if all_passed else '❌'),
            report
        )
        print('✅ 健康檢查完成，報告已發送')
    except Exception as e:
        print(f'❌ 發送報告失敗：{str(e)}')
    
    # 保存到日誌
    log_file = '/home/admin/.openclaw/workspace/AI 自媒體項目/logs/health-check.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(report)
    
    print(report)

if __name__ == "__main__":
    main()
