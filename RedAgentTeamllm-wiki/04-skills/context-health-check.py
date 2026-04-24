#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上下文健康检查工具
手动检查当前上下文状态，测试触发机制
"""

import subprocess
import json
import sys

def check_session_status():
    """检查会话状态"""
    print("📊 检查上下文状态...\n")
    
    # 获取会话状态
    result = subprocess.run(
        ["openclaw", "session", "status"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    # 解析上下文使用率
    output = result.stdout
    for line in output.split('\n'):
        if 'Context:' in line:
            # 提取使用率
            parts = line.split()
            for part in parts:
                if '%' in part:
                    percent = float(part.replace('(', '').replace('%)', ''))
                    print(f"\n📈 上下文使用率：{percent}%")
                    
                    # 检查触发级别
                    if percent >= 90:
                        print("🔴 警告：已达到自动压缩阈值 (90%)")
                        print("   建议立即执行：openclaw session compact --keep-last 50")
                    elif percent >= 80:
                        print("🟠 建议：已达到建议压缩阈值 (80%)")
                        print("   建议执行：openclaw session compact --keep-last 100")
                    elif percent >= 70:
                        print("🟡 提醒：已达到通知阈值 (70%)")
                        print("   可以考虑清理，但还不着急")
                    else:
                        print("✅ 状态：上下文使用率健康，无需操作")
                    
                    return percent
    
    return None

def test_export():
    """测试导出功能"""
    print("\n📤 测试导出功能...")
    result = subprocess.run(
        ["openclaw", "session", "export", "--to", "~/workspace/sessions/test-export.md"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode == 0:
        print("✅ 导出测试成功")
    else:
        print("⚠️ 导出测试失败")

if __name__ == "__main__":
    percent = check_session_status()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-export":
        test_export()
    
    print(f"\n💡 提示：当前使用率 {percent}%，距离 70% 阈值还有 {70-percent:.1f}% 空间")
