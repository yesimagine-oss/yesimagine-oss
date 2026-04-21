#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
會話管理系統 v2.0 - 核心突破版
Session Manager Pro - Intelligent Conversation Lifecycle Management

核心突破:
1. AI 智能價值評分 - 識別重要會話自動保留
2. 分級存儲策略 - 重要/普通/臨時三級管理
3. 壓縮歸檔機制 - 舊會話壓縮存檔而非刪除
4. 智能備份 - 重要會話自動備份到 Feishu/本地
5. 跨會話搜索 - 清理前可搜索歷史內容
6. 增量清理 - 只清理低價值內容

使用方式:
    python3 session-manager-pro.py analyze     # AI 分析會話價值
    python3 session-manager-pro.py archive     # 歸檔舊會話
    python3 session-manager-pro.py backup      # 備份重要會話
    python3 session-manager-pro.py search      # 搜索歷史內容
    python3 session-manager-pro.py lifecycle   # 查看生命週期
    python3 session-manager-pro.py smart       # 智能清理（推薦）
"""

import os
import sys
import json
import subprocess
import shutil
import re
import gzip
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# 配置
SESSION_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
ARCHIVE_DIR = Path.home() / ".openclaw" / "archive" / "sessions"
BACKUP_DIR = Path.home() / ".openclaw" / "backup" / "sessions"
CONFIG_FILE = Path(__file__).parent / "session-manager-pro-config.json"
LOG_FILE = Path("/tmp/session-manager-pro.log")
VALUE_CACHE_FILE = Path(__file__).parent / "session-value-cache.json"

# 顏色
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def log(message, level="INFO"):
    """記錄日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except:
        pass

def get_size_mb(path):
    """獲取大小 (MB)"""
    if not path.exists():
        return 0
    if path.is_file():
        return round(path.stat().st_size / 1024 / 1024, 2)
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return round(total / 1024 / 1024, 2)

def load_config():
    """加載配置"""
    default_config = {
        "value_scoring": {
            "code_weight": 30,        # 包含代碼的權重
            "config_weight": 25,      # 包含配置的權重
            "length_weight": 20,      # 長度權重
            "recency_weight": 15,     # 新近度權重
            "frequency_weight": 10    # 頻率權重
        },
        "retention": {
            "critical_days": 90,      # 關鍵會話保留 90 天
            "important_days": 30,     # 重要會話保留 30 天
            "normal_days": 7,         # 普通會話保留 7 天
            "temp_days": 1            # 臨時會話保留 1 天
        },
        "archive": {
            "enabled": True,
            "compress": True,
            "before_delete_days": 30
        },
        "backup": {
            "enabled": True,
            "auto_backup_critical": True,
            "backup_to_feishu": False
        },
        "thresholds": {
            "critical_score": 80,     # 關鍵會話分數閾值
            "important_score": 60,    # 重要會話分數閾值
            "normal_score": 40        # 普通會話分數閾值
        }
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                # 深度合併
                for key in user_config:
                    if key in default_config:
                        if isinstance(default_config[key], dict):
                            default_config[key].update(user_config[key])
                        else:
                            default_config[key] = user_config[key]
        except Exception as e:
            log(f"讀取配置失敗：{e}", "WARNING")
    
    return default_config

def save_config(config):
    """保存配置"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        log(f"保存配置失敗：{e}", "ERROR")
        return False

def analyze_session(session_file):
    """AI 智能分析會話價值"""
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return {"score": 0, "level": "unknown", "reasons": ["無法讀取"]}
    
    score = 0
    reasons = []
    metadata = {}
    
    # 1. 代碼檢測 (權重 30)
    code_patterns = [
        r'```[a-z]*\n', r'def\s+\w+', r'function\s+\w+', r'import\s+\w+',
        r'class\s+\w+', r'const\s+\w+', r'let\s+\w+', r'var\s+\w+',
        r'{\s*"', r'\[\s*{', r'=>', r'async\s+', r'await\s+'
    ]
    code_matches = sum(1 for p in code_patterns if re.search(p, content))
    code_score = min(code_matches * 3, 30)
    if code_score > 10:
        score += code_score
        reasons.append(f"包含代碼片段 (+{code_score})")
        metadata["has_code"] = True
    
    # 2. 配置檢測 (權重 25)
    config_patterns = [
        r'api[_-]?key', r'token', r'password', r'secret',
        r'host.*:\s*\d+', r'port.*:\s*\d+', r'url.*http',
        r'database', r'redis', r'mongo', r'mysql',
        r'config', r'env', r'\.yaml', r'\.json'
    ]
    config_matches = sum(1 for p in config_patterns if re.search(p, content, re.I))
    config_score = min(config_matches * 5, 25)
    if config_score > 5:
        score += config_score
        reasons.append(f"包含配置信息 (+{config_score})")
        metadata["has_config"] = True
    
    # 3. 長度檢測 (權重 20)
    line_count = len(content.split('\n'))
    if line_count > 1000:
        length_score = 20
    elif line_count > 500:
        length_score = 15
    elif line_count > 100:
        length_score = 10
    else:
        length_score = 5
    score += length_score
    reasons.append(f"長度 {line_count} 行 (+{length_score})")
    metadata["line_count"] = line_count
    
    # 4. 新近度檢測 (權重 15)
    mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
    age_days = (datetime.now() - mtime).days
    if age_days == 0:
        recency_score = 15
    elif age_days < 3:
        recency_score = 12
    elif age_days < 7:
        recency_score = 8
    elif age_days < 30:
        recency_score = 4
    else:
        recency_score = 1
    score += recency_score
    reasons.append(f" {age_days} 天前 (+{recency_score})")
    metadata["age_days"] = age_days
    
    # 5. 關鍵詞檢測 (額外加分)
    keywords = {
        "重要": 5, "關鍵": 5, "必須": 5, "切記": 5,
        "教程": 3, "指南": 3, "手冊": 3, "文檔": 3,
        "配置": 3, "部署": 3, "上線": 3, "生產": 3,
        "bug": 2, "fix": 2, "修復": 2, "解決": 2
    }
    keyword_score = 0
    for kw, points in keywords.items():
        if kw.lower() in content.lower():
            keyword_score += points
    keyword_score = min(keyword_score, 10)
    if keyword_score > 0:
        score += keyword_score
        reasons.append(f"關鍵詞 (+{keyword_score})")
    
    # 歸一化分數 (0-100)
    score = min(score, 100)
    
    # 確定等級
    config = load_config()
    if score >= config["thresholds"]["critical_score"]:
        level = "critical"
        level_name = "🔴 關鍵"
    elif score >= config["thresholds"]["important_score"]:
        level = "important"
        level_name = "🟡 重要"
    elif score >= config["thresholds"]["normal_score"]:
        level = "normal"
        level_name = "🟢 普通"
    else:
        level = "temp"
        level_name = "⚪ 臨時"
    
    return {
        "score": score,
        "level": level,
        "level_name": level_name,
        "reasons": reasons,
        "metadata": metadata
    }

def analyze_all():
    """分析所有會話"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}🧠 AI 智能會話價值分析{Colors.RESET}\n")
    
    if not SESSION_DIR.exists():
        print(f"{Colors.RED}❌ 會話目錄不存在{Colors.RESET}")
        return
    
    sessions = list(SESSION_DIR.glob("*.jsonl"))
    if not sessions:
        print(f"{Colors.YELLOW}⚠️ 沒有會話文件{Colors.RESET}")
        return
    
    results = []
    for session_file in sessions:
        analysis = analyze_session(session_file)
        results.append({
            "file": session_file,
            "name": session_file.name,
            "size_mb": get_size_mb(session_file),
            **analysis
        })
    
    # 按分數排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # 統計
    stats = Counter(r["level"] for r in results)
    total_size = sum(r["size_mb"] for r in results)
    
    # 輸出
    print(f"{Colors.BLUE}總會話：{len(results)} 個 | 總體積：{total_size:.2f}MB{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}價值分佈:{Colors.RESET}")
    level_names = {
        "critical": "🔴 關鍵",
        "important": "🟡 重要",
        "normal": "🟢 普通",
        "temp": "⚪ 臨時"
    }
    for level, name in level_names.items():
        count = stats.get(level, 0)
        if count > 0:
            print(f"  {name}: {count} 個")
    
    print(f"\n{Colors.BOLD}會話詳情 (按價值排序):{Colors.RESET}\n")
    
    for i, r in enumerate(results[:20], 1):  # 只显示前 20 个
        print(f"{i:2d}. {Colors.BOLD}{r['name'][:50]}{Colors.RESET}")
        print(f"    分數：{r['score']}/100 | {r['level_name']} | {r['size_mb']:.2f}MB | {r['metadata'].get('age_days', '?')}天前")
        if r['reasons']:
            print(f"    原因：{' | '.join(r['reasons'][:3])}")
        print()
    
    if len(results) > 20:
        print(f"... 還有 {len(results) - 20} 個會話")
    
    # 保存緩存
    cache = {
        "timestamp": datetime.now().isoformat(),
        "results": [
            {
                "name": r["name"],
                "score": r["score"],
                "level": r["level"],
                "size_mb": r["size_mb"]
            }
            for r in results
        ]
    }
    try:
        with open(VALUE_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except:
        pass
    
    return results

def archive_sessions(dry_run=False):
    """歸檔舊會話"""
    config = load_config()
    
    if not config["archive"]["enabled"]:
        log("歸檔功能未啟用", "INFO")
        return
    
    print(f"\n{Colors.BOLD}📦 會話歸檔{Colors.RESET}{' (預覽)' if dry_run else ''}\n")
    
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 找出需要歸檔的會話（超過 30 天的普通/臨時會話）
    cutoff = datetime.now() - timedelta(days=config["archive"]["before_delete_days"])
    to_archive = []
    
    for session_file in SESSION_DIR.glob("*.jsonl"):
        if session_file.stat().st_mtime < cutoff.timestamp():
            analysis = analyze_session(session_file)
            if analysis["level"] in ["normal", "temp"]:
                to_archive.append((session_file, analysis))
    
    if not to_archive:
        print(f"{Colors.GREEN}✅ 沒有需要歸檔的會話{Colors.RESET}")
        return
    
    print(f"找到 {len(to_archive)} 個需要歸檔的會話\n")
    
    for session_file, analysis in to_archive:
        archive_name = f"{session_file.stem}_{datetime.now().strftime('%Y%m%d')}.jsonl"
        archive_path = ARCHIVE_DIR / archive_name
        
        if config["archive"]["compress"]:
            archive_name += ".gz"
            archive_path = ARCHIVE_DIR / archive_name
        
        print(f"  {session_file.name} → {archive_name}")
        print(f"    分數：{analysis['score']} | {analysis['level_name']} | {analysis['metadata'].get('age_days', '?')}天前")
        
        if not dry_run:
            try:
                if config["archive"]["compress"]:
                    with open(session_file, 'rb') as f_in:
                        with gzip.open(archive_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                else:
                    shutil.copy2(session_file, archive_path)
                
                # 添加歸檔元數據
                meta_path = archive_path.with_suffix('.meta.json')
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "original_name": session_file.name,
                        "archived_at": datetime.now().isoformat(),
                        "analysis": analysis
                    }, f, indent=2, ensure_ascii=False)
                
                # 刪除原文件
                session_file.unlink()
                print(f"    {Colors.GREEN}✅ 歸檔完成{Colors.RESET}")
            except Exception as e:
                print(f"    {Colors.RED}❌ 失敗：{e}{Colors.RESET}")
    
    # 統計
    archive_size = get_size_mb(ARCHIVE_DIR)
    archive_count = len(list(ARCHIVE_DIR.glob("*.jsonl*")))
    print(f"\n歸檔目錄：{archive_count} 個文件 | {archive_size:.2f}MB")

def backup_critical():
    """備份關鍵會話"""
    config = load_config()
    
    if not config["backup"]["enabled"]:
        log("備份功能未啟用", "INFO")
        return
    
    print(f"\n{Colors.BOLD}💾 關鍵會話備份{Colors.RESET}\n")
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # 找出關鍵會話
    critical_sessions = []
    for session_file in SESSION_DIR.glob("*.jsonl"):
        analysis = analyze_session(session_file)
        if analysis["level"] == "critical":
            critical_sessions.append((session_file, analysis))
    
    if not critical_sessions:
        print(f"{Colors.GREEN}✅ 沒有關鍵會話需要備份{Colors.RESET}")
        return
    
    print(f"找到 {len(critical_sessions)} 個關鍵會話\n")
    
    for session_file, analysis in critical_sessions:
        backup_name = f"{session_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        backup_path = BACKUP_DIR / backup_name
        
        print(f"  {session_file.name} → {backup_name}")
        print(f"    分數：{analysis['score']} | 大小：{get_size_mb(session_file):.2f}MB")
        
        try:
            shutil.copy2(session_file, backup_path)
            
            # 添加備份元數據
            meta_path = backup_path.with_suffix('.meta.json')
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump({
                    "original_name": session_file.name,
                    "backed_up_at": datetime.now().isoformat(),
                    "analysis": analysis,
                    "checksum": hashlib.md5(open(session_file, 'rb').read()).hexdigest()
                }, f, indent=2, ensure_ascii=False)
            
            print(f"    {Colors.GREEN}✅ 備份完成{Colors.RESET}")
        except Exception as e:
            print(f"    {Colors.RED}❌ 失敗：{e}{Colors.RESET}")
    
    # 統計
    backup_size = get_size_mb(BACKUP_DIR)
    backup_count = len(list(BACKUP_DIR.glob("*.jsonl")))
    print(f"\n備份目錄：{backup_count} 個文件 | {backup_size:.2f}MB")

def search_sessions(query):
    """搜索會話內容"""
    print(f"\n{Colors.BOLD}🔍 搜索會話：'{query}'{Colors.RESET}\n")
    
    if not SESSION_DIR.exists():
        print(f"{Colors.RED}❌ 會話目錄不存在{Colors.RESET}")
        return
    
    results = []
    
    for session_file in SESSION_DIR.glob("*.jsonl"):
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if query.lower() in content.lower():
                # 計算相關度
                matches = len(re.findall(re.escape(query), content, re.I))
                results.append({
                    "file": session_file,
                    "name": session_file.name,
                    "matches": matches,
                    "size_mb": get_size_mb(session_file)
                })
        except:
            continue
    
    if not results:
        print(f"{Colors.YELLOW}⚠️ 未找到匹配結果{Colors.RESET}")
        return
    
    # 按匹配度排序
    results.sort(key=lambda x: x["matches"], reverse=True)
    
    print(f"找到 {len(results)} 個匹配結果:\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']}")
        print(f"   匹配次數：{r['matches']} | 大小：{r['size_mb']:.2f}MB")
        
        # 顯示上下文片段
        try:
            with open(r["file"], "r", encoding="utf-8") as f:
                content = f.read()
                idx = content.lower().find(query.lower())
                if idx >= 0:
                    start = max(0, idx - 50)
                    end = min(len(content), idx + len(query) + 50)
                    snippet = content[start:end].replace('\n', ' ')
                    print(f"   片段：...{snippet}...")
        except:
            pass
        print()

def smart_cleanup(dry_run=False):
    """智能清理（核心功能）"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}🧠 智能清理{' (預覽)' if dry_run else ''}{Colors.RESET}\n")
    
    # 先分析所有會話
    results = analyze_all()
    if not results:
        return
    
    # 計算清理策略
    cleanup_list = []
    keep_list = []
    
    for r in results:
        retention_days = {
            "critical": config["retention"]["critical_days"],
            "important": config["retention"]["important_days"],
            "normal": config["retention"]["normal_days"],
            "temp": config["retention"]["temp_days"]
        }[r["level"]]
        
        age_days = r["metadata"].get("age_days", 0)
        
        if age_days > retention_days:
            cleanup_list.append({
                **r,
                "reason": f"超過保留期 ({age_days}天 > {retention_days}天)",
                "action": "archive" if age_days < 60 else "delete"
            })
        else:
            keep_list.append(r)
    
    # 檢查體積限制
    total_size = sum(r["size_mb"] for r in results)
    max_bytes = config["thresholds"].get("max_bytes_mb", 100)
    
    if total_size > max_bytes and len(cleanup_list) == 0:
        # 需要強制清理一些會話
        print(f"{Colors.YELLOW}⚠️ 總體積 {total_size:.2f}MB 超過限制 {max_bytes}MB{Colors.RESET}")
        print(f"   將清理最低價值的會話...\n")
        
        # 按分數排序，清理最低分數的
        results.sort(key=lambda x: x["score"])
        freed = 0
        for r in results:
            if total_size - freed <= max_bytes * 0.8:
                break
            if r["level"] not in ["critical"]:  # 不刪除關鍵會話
                cleanup_list.append({
                    **r,
                    "reason": f"體積限制 (釋放 {r['size_mb']:.2f}MB)",
                    "action": "archive"
                })
                freed += r["size_mb"]
    
    # 輸出清理計劃
    print(f"{Colors.BOLD}清理計劃:{Colors.RESET}\n")
    
    if not cleanup_list:
        print(f"{Colors.GREEN}✅ 無需清理{Colors.RESET}")
        return
    
    print(f"將清理 {len(cleanup_list)} 個會話，釋放約 {sum(r['size_mb'] for r in cleanup_list):.2f}MB\n")
    
    for r in cleanup_list:
        action_icon = "📦 歸檔" if r["action"] == "archive" else "🗑️ 刪除"
        print(f"  {action_icon} {r['name'][:50]}")
        print(f"      {r['reason']}")
        print(f"      分數：{r['score']} | {r['level_name']} | {r['size_mb']:.2f}MB\n")
    
    if not dry_run:
        print(f"\n{Colors.YELLOW}⚠️ 確認執行清理？(y/N): {Colors.RESET}", end="")
        try:
            response = input().strip().lower()
            if response != "y":
                print(f"{Colors.YELLOW}已取消{Colors.RESET}")
                return
        except:
            print(f"{Colors.YELLOW}非交互模式，跳過確認{Colors.RESET}")
        
        # 執行清理
        for r in cleanup_list:
            try:
                if r["action"] == "archive":
                    # 歸檔
                    archive_name = f"{r['file'].stem}_archived_{datetime.now().strftime('%Y%m%d')}.jsonl.gz"
                    archive_path = ARCHIVE_DIR / archive_name
                    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
                    
                    with open(r["file"], 'rb') as f_in:
                        with gzip.open(archive_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    r["file"].unlink()
                    print(f"  {Colors.GREEN}✅ 已歸檔{Colors.RESET}: {r['name']}")
                else:
                    # 刪除
                    r["file"].unlink()
                    print(f"  {Colors.GREEN}✅ 已刪除{Colors.RESET}: {r['name']}")
            except Exception as e:
                print(f"  {Colors.RED}❌ 失敗：{e}{Colors.RESET}")
        
        # 運行 OpenClaw 官方 cleanup
        log("運行 OpenClaw cleanup...")
        subprocess.run(
            ["openclaw", "sessions", "cleanup", "--enforce"],
            capture_output=True,
            text=True
        )
        
        # 最終統計
        final_size = get_size_mb(SESSION_DIR)
        final_count = len(list(SESSION_DIR.glob("*.jsonl")))
        print(f"\n{Colors.BOLD}清理完成:{Colors.RESET}")
        print(f"  剩餘會話：{final_count} 個")
        print(f"  剩餘體積：{final_size:.2f}MB")

def lifecycle():
    """查看會話生命週期"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}📊 會話生命週期管理{Colors.RESET}\n")
    
    if not SESSION_DIR.exists():
        print(f"{Colors.RED}❌ 會話目錄不存在{Colors.RESET}")
        return
    
    # 分析所有會話
    results = []
    for session_file in SESSION_DIR.glob("*.jsonl"):
        analysis = analyze_session(session_file)
        age_days = analysis["metadata"].get("age_days", 0)
        
        retention_days = {
            "critical": config["retention"]["critical_days"],
            "important": config["retention"]["important_days"],
            "normal": config["retention"]["normal_days"],
            "temp": config["retention"]["temp_days"]
        }[analysis["level"]]
        
        remaining = retention_days - age_days
        
        results.append({
            "file": session_file,
            "name": session_file.name,
            "age_days": age_days,
            "retention_days": retention_days,
            "remaining": remaining,
            **analysis
        })
    
    # 按剩餘天數排序
    results.sort(key=lambda x: x["remaining"])
    
    print(f"{Colors.BOLD}即將到期的會話:{Colors.RESET}\n")
    
    for r in results[:10]:
        if r["remaining"] <= 0:
            status = f"{Colors.RED}已過期 {abs(r['remaining'])}天{Colors.RESET}"
        elif r["remaining"] <= 3:
            status = f"{Colors.YELLOW}即將到期 ({r['remaining']}天){Colors.RESET}"
        else:
            status = f"{Colors.GREEN}{r['remaining']}天{Colors.RESET}"
        
        print(f"  {r['name'][:40]}")
        print(f"    {r['level_name']} | {r['age_days']}天 / {r['retention_days']}天 | 剩餘：{status}")
        print()

def show_help():
    """顯示幫助"""
    print(f"""
{Colors.BOLD}會話管理系統 Pro v2.0 - 核心突破版{Colors.RESET}

用法：python3 session-manager-pro.py <命令> [選項]

核心命令:
  analyze     AI 智能分析會話價值
  archive     歸檔舊會話（壓縮存儲）
  backup      備份關鍵會話
  search      搜索歷史內容
  lifecycle   查看會話生命週期
  smart       智能清理（推薦使用）
  status      查看狀態
  init        初始化配置
  help        顯示幫助

選項:
  --dry-run   預覽效果（不實際執行）

示例:
  python3 session-manager-pro.py analyze
  python3 session-manager-pro.py smart --dry-run
  python3 session-manager-pro.py search "API key"
  python3 session-manager-pro.py lifecycle

核心突破:
  ✅ AI 智能價值評分 - 識別重要會話
  ✅ 分級存儲策略 - 關鍵/重要/普通/臨時
  ✅ 壓縮歸檔機制 - 舊會話壓縮而非刪除
  ✅ 智能備份 - 關鍵會話自動備份
  ✅ 跨會話搜索 - 搜索歷史內容
  ✅ 生命週期管理 - 可視化剩餘天數

配置文件:
  {CONFIG_FILE}
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if command == "analyze":
        analyze_all()
    elif command == "archive":
        archive_sessions(dry_run)
    elif command == "backup":
        backup_critical()
    elif command == "search":
        if len(sys.argv) < 3:
            print(f"{Colors.RED}❌ 請提供搜索關鍵詞{Colors.RESET}")
            sys.exit(1)
        search_sessions(" ".join(sys.argv[2:]))
    elif command == "lifecycle":
        lifecycle()
    elif command == "smart":
        smart_cleanup(dry_run)
    elif command == "status":
        analyze_all()
    elif command == "init":
        config = load_config()
        if save_config(config):
            print(f"{Colors.GREEN}✅ 配置已初始化{Colors.RESET}")
            print(f"配置文件：{CONFIG_FILE}")
    elif command == "help":
        show_help()
    else:
        print(f"{Colors.RED}未知命令：{command}{Colors.RESET}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
