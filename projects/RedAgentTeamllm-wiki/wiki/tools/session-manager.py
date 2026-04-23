#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
會話管理工具 - Session Manager
功能：自動清理、監控、報告、告警

使用方式:
    python3 session-manager.py status      # 查看狀態
    python3 session-manager.py cleanup     # 執行清理
    python3 session-manager.py report      # 生成報告
    python3 session-manager.py monitor     # 監控並告警
    python3 session-manager.py init        # 初始化配置
"""

import os
import sys
import json
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# 配置
SESSION_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
CONFIG_FILE = Path.home() / ".openclaw" / "config.yaml"
LOG_FILE = Path("/tmp/session-manager.log")

# 默認配置
DEFAULT_CONFIG = {
    "retention_days": 7,          # 保留天數
    "max_count": 50,              # 最大會話數
    "max_bytes_mb": 100,          # 最大體積 (MB)
    "auto_cleanup": True,         # 是否自動清理
    "notify_on_cleanup": True,    # 清理後通知
    "alert_threshold_mb": 80,     # 告警閾值 (MB)
}

# 顏色
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def log(message, level="INFO"):
    """記錄日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    
    # 寫入日誌文件
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except Exception as e:
        pass

def get_size_mb(path):
    """獲取目錄大小 (MB)"""
    if not path.exists():
        return 0
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return round(total / 1024 / 1024, 2)

def get_session_count():
    """獲取會話數量"""
    if not SESSION_DIR.exists():
        return 0
    return len(list(SESSION_DIR.glob("*.jsonl")))

def run_command(cmd):
    """執行 shell 命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def load_config():
    """加載配置"""
    config = DEFAULT_CONFIG.copy()
    
    # 嘗試從配置文件讀取
    config_path = Path(__file__).parent / "session-manager-config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            log(f"讀取配置失敗：{e}", "WARNING")
    
    return config

def save_config(config):
    """保存配置"""
    config_path = Path(__file__).parent / "session-manager-config.json"
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        log(f"配置已保存：{config_path}")
        return True
    except Exception as e:
        log(f"保存配置失敗：{e}", "ERROR")
        return False

def status():
    """查看狀態"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}📊 會話管理狀態{Colors.RESET}\n")
    
    # 基本信息
    print(f"{Colors.BLUE}會話目錄:{Colors.RESET} {SESSION_DIR}")
    print(f"{Colors.BLUE}存在狀態:{Colors.RESET} {'✅ 存在' if SESSION_DIR.exists() else '❌ 不存在'}")
    
    if SESSION_DIR.exists():
        size_mb = get_size_mb(SESSION_DIR)
        count = get_session_count()
        
        print(f"\n{Colors.BOLD}當前狀態:{Colors.RESET}")
        print(f"  會話數量：{Colors.GREEN}{count}{Colors.RESET} 個")
        print(f"  總體積：{Colors.GREEN}{size_mb}{Colors.RESET} MB")
        
        # 評估狀態
        if size_mb > config["max_bytes_mb"]:
            status_color = Colors.RED
            status_text = "⚠️ 超過限制"
        elif size_mb > config["alert_threshold_mb"]:
            status_color = Colors.YELLOW
            status_text = "⚠️ 接近限制"
        else:
            status_color = Colors.GREEN
            status_text = "✅ 健康"
        
        print(f"  健康狀態：{status_color}{status_text}{Colors.RESET}")
        
        # 限制配置
        print(f"\n{Colors.BOLD}配置限制:{Colors.RESET}")
        print(f"  保留天數：{config['retention_days']} 天")
        print(f"  最大數量：{config['max_count']} 個")
        print(f"  最大體積：{config['max_bytes_mb']} MB")
        print(f"  告警閾值：{config['alert_threshold_mb']} MB")
        
        # 列出最大的 5 個會話
        print(f"\n{Colors.BOLD}最大的 5 個會話:{Colors.RESET}")
        sessions = sorted(
            [(f, f.stat().st_size / 1024 / 1024) for f in SESSION_DIR.glob("*.jsonl")],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for i, (session_file, size) in enumerate(sessions, 1):
            age_days = (datetime.now().timestamp() - session_file.stat().st_mtime) / 86400
            age_str = f"{age_days:.1f}天" if age_days > 1 else f"{age_days*24:.0f}小時"
            print(f"  {i}. {session_file.name[:40]}... - {size:.2f}MB ({age_str}前)")
    
    # 配置文件狀態
    config_path = Path(__file__).parent / "session-manager-config.json"
    print(f"\n{Colors.BOLD}配置文件:{Colors.RESET}")
    print(f"  位置：{config_path}")
    print(f"  狀態：{'✅ 存在' if config_path.exists() else '❌ 不存在'}")

def cleanup(dry_run=False):
    """執行清理"""
    config = load_config()
    
    log(f"開始清理 (dry_run={dry_run})")
    
    actions = []
    
    # 1. 刪除 .deleted 文件
    deleted_files = list(SESSION_DIR.glob("*.deleted*"))
    if deleted_files:
        actions.append(f"刪除 {len(deleted_files)} 個 .deleted 文件")
        if not dry_run:
            for f in deleted_files:
                f.unlink()
                log(f"已刪除：{f.name}")
    
    # 2. 刪除超過保留期的文件
    cutoff = datetime.now() - timedelta(days=config["retention_days"])
    old_files = [
        f for f in SESSION_DIR.glob("*.jsonl")
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff
    ]
    
    if old_files:
        actions.append(f"刪除 {len(old_files)} 個超過 {config['retention_days']} 天的會話")
        if not dry_run:
            for f in old_files:
                f.unlink()
                log(f"已刪除舊會話：{f.name}")
    
    # 3. 如果數量超過限制，刪除最舊的
    current_count = get_session_count()
    if current_count > config["max_count"]:
        excess = current_count - config["max_count"]
        actions.append(f"刪除 {excess} 個最舊會話 (超過數量限制)")
        
        if not dry_run:
            sessions = sorted(
                SESSION_DIR.glob("*.jsonl"),
                key=lambda f: f.stat().st_mtime
            )[:excess]
            for f in sessions:
                f.unlink()
                log(f"已刪除超額會話：{f.name}")
    
    # 4. 運行 OpenClaw 官方 cleanup
    log("運行 OpenClaw 官方 cleanup...")
    cmd = "openclaw sessions cleanup --enforce --all-agents"
    if dry_run:
        cmd += " --dry-run"
    
    success, stdout, stderr = run_command(cmd)
    if success:
        actions.append("✅ OpenClaw cleanup 執行成功")
    else:
        actions.append(f"⚠️ OpenClaw cleanup 執行失敗：{stderr}")
    
    # 5. 統計結果
    final_size = get_size_mb(SESSION_DIR)
    final_count = get_session_count()
    
    # 輸出報告
    print(f"\n{Colors.BOLD}🧹 清理報告{'(預覽)' if dry_run else ''}{Colors.RESET}\n")
    
    for action in actions:
        print(f"  ✅ {action}")
    
    print(f"\n{Colors.BOLD}清理後狀態:{Colors.RESET}")
    print(f"  會話數量：{Colors.GREEN}{final_count}{Colors.RESET} 個")
    print(f"  總體積：{Colors.GREEN}{final_size}{Colors.RESET} MB")
    
    if not dry_run and config["notify_on_cleanup"]:
        log(f"清理完成：{final_count}個會話，{final_size}MB")
    
    return True

def report():
    """生成詳細報告"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}📋 會話管理詳細報告{Colors.RESET}")
    print(f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 基本信息
    size_mb = get_size_mb(SESSION_DIR)
    count = get_session_count()
    
    print(f"{Colors.BOLD}基本統計:{Colors.RESET}")
    print(f"  總會話數：{count}")
    print(f"  總體積：{size_mb} MB")
    print(f"  平均大小：{size_mb/count:.2f} MB" if count > 0 else "  平均大小：N/A")
    
    # 按年齡分佈
    print(f"\n{Colors.BOLD}年齡分佈:{Colors.RESET}")
    now = datetime.now()
    age_buckets = {"<1 天": 0, "1-3 天": 0, "3-7 天": 0, "7-30 天": 0, ">30 天": 0}
    
    for f in SESSION_DIR.glob("*.jsonl"):
        age_days = (now.timestamp() - f.stat().st_mtime) / 86400
        if age_days < 1:
            age_buckets["<1 天"] += 1
        elif age_days < 3:
            age_buckets["1-3 天"] += 1
        elif age_days < 7:
            age_buckets["3-7 天"] += 1
        elif age_days < 30:
            age_buckets["7-30 天"] += 1
        else:
            age_buckets[">30 天"] += 1
    
    for age, count in age_buckets.items():
        if count > 0:
            print(f"  {age}: {count} 個")
    
    # 體積分佈
    print(f"\n{Colors.BOLD}體積分佈:{Colors.RESET}")
    size_buckets = {"<100KB": 0, "100KB-1MB": 0, "1MB-5MB": 0, ">5MB": 0}
    
    for f in SESSION_DIR.glob("*.jsonl"):
        size_kb = f.stat().st_size / 1024
        if size_kb < 100:
            size_buckets["<100KB"] += 1
        elif size_kb < 1024:
            size_buckets["100KB-1MB"] += 1
        elif size_kb < 5120:
            size_buckets["1MB-5MB"] += 1
        else:
            size_buckets[">5MB"] += 1
    
    for size, count in size_buckets.items():
        if count > 0:
            print(f"  {size}: {count} 個")
    
    # 增長預測
    print(f"\n{Colors.BOLD}增長預測:{Colors.RESET}")
    print(f"  當前：{size_mb} MB")
    print(f"  預估每月：{size_mb * 30:.0f} MB (按當前增速)")
    print(f"  達到限制 ({config['max_bytes_mb']}MB) 還需：{(config['max_bytes_mb'] - size_mb) / (size_mb + 0.1) * 30:.0f} 天")
    
    # 建議
    print(f"\n{Colors.BOLD}優化建議:{Colors.RESET}")
    if size_mb > config["alert_threshold_mb"]:
        print(f"  {Colors.YELLOW}⚠️ 體積接近限制，建議執行清理{Colors.RESET}")
    if count > config["max_count"] * 0.8:
        print(f"  {Colors.YELLOW}⚠️ 會話數量接近限制 ({count}/{config['max_count']}){Colors.RESET}")
    if age_buckets.get(">30 天", 0) > 0:
        print(f"  {Colors.YELLOW}⚠️ 發現 {age_buckets['>30 天']} 個超過 30 天的舊會話{Colors.RESET}")
    
    print(f"  {Colors.GREEN}✅ 建議保留當前配置{Colors.RESET}")

def monitor():
    """監控並告警"""
    config = load_config()
    size_mb = get_size_mb(SESSION_DIR)
    count = get_session_count()
    
    alerts = []
    
    # 檢查體積
    if size_mb > config["max_bytes_mb"]:
        alerts.append(f"🔴 體積超過限制：{size_mb}MB > {config['max_bytes_mb']}MB")
    elif size_mb > config["alert_threshold_mb"]:
        alerts.append(f"🟡 體積接近限制：{size_mb}MB > {config['alert_threshold_mb']}MB")
    
    # 檢查數量
    if count > config["max_count"]:
        alerts.append(f"🔴 會話數量超過限制：{count} > {config['max_count']}")
    
    # 檢查舊會話
    cutoff = datetime.now() - timedelta(days=config["retention_days"] * 2)
    old_sessions = [
        f for f in SESSION_DIR.glob("*.jsonl")
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff
    ]
    if old_sessions:
        alerts.append(f"🟡 發現 {len(old_sessions)} 個超期會話")
    
    # 輸出
    if alerts:
        print(f"\n{Colors.RED}⚠️ 監控告警{Colors.RESET}\n")
        for alert in alerts:
            print(f"  {alert}")
        log(f"告警：{', '.join(alerts)}", "ALERT")
        return False
    else:
        print(f"\n{Colors.GREEN}✅ 監控正常{Colors.RESET}")
        print(f"  體積：{size_mb}MB / {config['max_bytes_mb']}MB")
        print(f"  數量：{count} / {config['max_count']}")
        return True

def init():
    """初始化配置"""
    print(f"\n{Colors.BOLD}🔧 初始化會話管理配置{Colors.RESET}\n")
    
    # 創建配置文件
    config = DEFAULT_CONFIG.copy()
    
    print("默認配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print(f"\n是否修改配置？(y/N): ", end="")
    
    # 簡單交互（實際使用時可以改進）
    try:
        response = input().strip().lower()
        if response == "y":
            print("\n輸入新配置 (直接回車使用默認值):")
            for key in config:
                value = input(f"  {key} [{config[key]}]: ").strip()
                if value:
                    try:
                        config[key] = int(value) if key != "auto_cleanup" else value.lower() == "true"
                    except:
                        config[key] = value
        
        if save_config(config):
            print(f"\n{Colors.GREEN}✅ 配置已保存{Colors.RESET}")
            print(f"配置文件：{Path(__file__).parent / 'session-manager-config.json'}")
            
            # 建議設置 crontab
            print(f"\n{Colors.BOLD}建議設置定時任務:{Colors.RESET}")
            print(f"  crontab -e")
            print(f"  添加：0 3 * * * python3 {Path(__file__).absolute()} cleanup")
            
            return True
    except Exception as e:
        log(f"初始化失敗：{e}", "ERROR")
        return False
    
    return False

def show_help():
    """顯示幫助"""
    print(f"""
{Colors.BOLD}會話管理工具 - Session Manager{Colors.RESET}

用法：python3 session-manager.py <命令> [選項]

命令:
  status    查看狀態
  cleanup   執行清理
  report    生成詳細報告
  monitor   監控並告警
  init      初始化配置
  help      顯示幫助

選項:
  --dry-run 預覽清理效果（不實際刪除）

示例:
  python3 session-manager.py status
  python3 session-manager.py cleanup --dry-run
  python3 session-manager.py report
  python3 session-manager.py monitor
  python3 session-manager.py init

配置文件:
  {Path(__file__).parent / 'session-manager-config.json'}

日誌文件:
  {LOG_FILE}
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if command == "status":
        status()
    elif command == "cleanup":
        cleanup(dry_run)
    elif command == "report":
        report()
    elif command == "monitor":
        monitor()
    elif command == "init":
        init()
    elif command == "help":
        show_help()
    else:
        print(f"未知命令：{command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
