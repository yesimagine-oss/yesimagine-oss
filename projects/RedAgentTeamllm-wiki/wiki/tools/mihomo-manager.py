#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
Mihomo 按需啟動管理器

功能:
- 檢查 Mihomo 狀態
- 按需自動啟動
- 等待就緒
- 可選自動關閉

使用:
    python3 mihomo-manager.py check      # 檢查狀態
    python3 mihomo-manager.py start      # 啟動
    python3 mihomo-manager.py stop       # 停止
    python3 mihomo-manager.py status     # 詳細狀態
    python3 mihomo-manager.py on-demand  # 按需啟動（用於微信抓取）
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

MIHOMO_API_URL = "http://127.0.0.1:9090"
MIHOMO_HEALTH_ENDPOINT = f"{MIHOMO_API_URL}/health"

def check_mihomo_process() -> bool:
    """檢查 Mihomo 進程是否運行"""
    try:
        result = subprocess.run(
            ['pgrep', '-la', 'mihomo'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 檢查進程失敗：{e}")
        return False

def check_mihomo_health() -> bool:
    """檢查 Mihomo API 健康狀態"""
    try:
        response = requests.get(MIHOMO_HEALTH_ENDPOINT, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def get_mihomo_status() -> dict:
    """獲取 Mihomo 詳細狀態"""
    status = {
        'process_running': False,
        'api_healthy': False,
        'ready': False,
        'timestamp': datetime.now().isoformat()
    }
    
    # 檢查進程
    status['process_running'] = check_mihomo_process()
    
    # 檢查 API 健康
    if status['process_running']:
        status['api_healthy'] = check_mihomo_health()
        status['ready'] = status['api_healthy']
    
    return status

def start_mihomo() -> bool:
    """啟動 Mihomo"""
    print("📡 啟動 Mihomo...")
    
    try:
        # 嘗試 systemctl
        result = subprocess.run(
            ['systemctl', '--user', 'start', 'mihomo'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ 通過 systemctl 啟動成功")
            return True
        
        # 嘗試直接啟動
        print("⚠️ systemctl 失敗，嘗試直接啟動...")
        result = subprocess.run(
            ['which', 'mihomo'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        
        if result.returncode == 0:
            mihomo_path = result.stdout.strip()
            subprocess.Popen(
                [mihomo_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ 直接啟動成功")
            return True
        
        print("❌ 未找到 Mihomo 可執行文件")
        return False
        
    except Exception as e:
        print(f"❌ 啟動失敗：{e}")
        return False

def wait_for_ready(timeout: int = 10) -> bool:
    """等待 Mihomo 就緒"""
    print(f"⏳ 等待 Mihomo 就緒 (最多 {timeout} 秒)...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_mihomo_health():
            print(f"✅ Mihomo 已就緒 (用時 {time.time() - start_time:.1f}秒)")
            return True
        time.sleep(0.5)
    
    print(f"❌ Mihomo 未在 {timeout} 秒內就緒")
    return False

def stop_mihomo() -> bool:
    """停止 Mihomo"""
    print("🛑 停止 Mihomo...")
    
    try:
        result = subprocess.run(
            ['systemctl', '--user', 'stop', 'mihomo'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ 停止成功")
            return True
        
        # 嘗試 kill
        subprocess.run(['pkill', 'mihomo'], capture_output=True)
        print("✅ 已強制停止")
        return True
        
    except Exception as e:
        print(f"❌ 停止失敗：{e}")
        return False

def on_demand_start() -> bool:
    """按需啟動 Mihomo（用於微信抓取）"""
    print("=" * 60)
    print("📡 Mihomo 按需啟動檢查")
    print("=" * 60)
    
    # 獲取當前狀態
    status = get_mihomo_status()
    
    print(f"進程狀態：{'✅ 運行中' if status['process_running'] else '❌ 未運行'}")
    print(f"API 健康：{'✅ 正常' if status['api_healthy'] else '❌ 異常'}")
    print(f"整體狀態：{'✅ 就緒' if status['ready'] else '⚠️ 未就緒'}")
    print("-" * 60)
    
    # 如果已經就緒，直接返回
    if status['ready']:
        print("✅ Mihomo 已就緒，無需啟動")
        return True
    
    # 需要啟動
    if not start_mihomo():
        print("❌ Mihomo 啟動失敗")
        return False
    
    # 等待就緒
    if not wait_for_ready(timeout=15):
        print("❌ Mihomo 未在指定時間內就緒")
        return False
    
    print("=" * 60)
    print("✅ Mihomo 按需啟動完成")
    print("=" * 60)
    return True

def show_status():
    """顯示詳細狀態"""
    print("=" * 60)
    print("📊 Mihomo 狀態報告")
    print("=" * 60)
    
    status = get_mihomo_status()
    
    print(f"檢查時間：{status['timestamp']}")
    print(f"進程運行：{'✅ 是' if status['process_running'] else '❌ 否'}")
    print(f"API 健康：{'✅ 是' if status['api_healthy'] else '❌ 否'}")
    print(f"整體就緒：{'✅ 是' if status['ready'] else '❌ 否'}")
    
    if status['ready']:
        print("\n✅ Mihomo 可以正常使用")
    else:
        print("\n⚠️ Mihomo 未就緒，需要啟動")
        print("   運行：python3 mihomo-manager.py on-demand")
    
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'check':
        # 簡單檢查
        if check_mihomo_process():
            print("✅ Mihomo 進程運行中")
            sys.exit(0)
        else:
            print("❌ Mihomo 進程未運行")
            sys.exit(1)
    
    elif command == 'start':
        # 啟動
        if start_mihomo():
            wait_for_ready()
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif command == 'stop':
        # 停止
        stop_mihomo()
        sys.exit(0)
    
    elif command == 'status':
        # 詳細狀態
        show_status()
        sys.exit(0)
    
    elif command == 'on-demand':
        # 按需啟動
        if on_demand_start():
            sys.exit(0)
        else:
            sys.exit(1)
    
    else:
        print(f"❌ 未知命令：{command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
