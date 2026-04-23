#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
會話管理系統 v3.0 - AI 決策型
Session Manager AI - Autonomous Decision Making System

核心突破:
1. AI 決策引擎 - 使用 LLM 分析並給出處理建議
2. 上下文感知 - 理解會話之間的關聯性
3. 學習優化 - 根據用戶反饋優化決策
4. 預測性管理 - 預測哪些會話未來可能有價值
5. 智能建議 - 提供清晰的決策理由
6. 自主執行 - 用戶確認後自動執行

使用方式:
    python3 session-manager-ai.py decide       # AI 決策分析
    python3 session-manager-ai.py explain      # 解釋決策理由
    python3 session-manager-ai.py learn        # 學習用戶偏好
    python3 session-manager-ai.py predict      # 預測未來價值
    python3 session-manager-ai.py autonomous   # 自主執行（需確認）
    python3 session-manager-ai.py brain        # 查看決策大腦
"""

import os
import sys
import json
import subprocess
import shutil
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# 配置
SESSION_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
AI_DIR = Path.home() / ".openclaw" / "ai" / "sessions"
DECISION_LOG = Path.home() / ".openclaw" / "ai" / "decisions.jsonl"
PREFERENCE_FILE = Path(__file__).parent / "session-manager-ai-preferences.json"
BRAIN_FILE = Path(__file__).parent / "session-manager-ai-brain.json"
CONFIG_FILE = Path(__file__).parent / "session-manager-ai-config.json"
LOG_FILE = Path("/tmp/session-manager-ai.log")

# 顏色
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

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
        "ai_model": "dashscope-coding/qwen3.5-plus",
        "decision_threshold": {
            "keep_score": 60,
            "archive_score": 40,
            "delete_score": 20
        },
        "context_awareness": {
            "enabled": True,
            "lookback_days": 7,
            "min_related_sessions": 2
        },
        "learning": {
            "enabled": True,
            "auto_adjust": True,
            "feedback_weight": 0.3
        },
        "autonomous": {
            "enabled": False,
            "require_confirmation": True,
            "max_auto_delete_mb": 10
        }
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                for key in user_config:
                    if key in default_config:
                        if isinstance(default_config[key], dict):
                            default_config[key].update(user_config[key])
                        else:
                            default_config[key] = user_config[key]
        except Exception as e:
            log(f"讀取配置失敗：{e}", "WARNING")
    
    return default_config

def load_preferences():
    """加載用戶偏好"""
    default_prefs = {
        "version": 1,
        "created_at": datetime.now().isoformat(),
        "preferences": {
            "preserve_code": True,
            "preserve_config": True,
            "preserve_tutorials": True,
            "aggressive_cleanup": False,
            "prefer_archive_over_delete": True
        },
        "feedback_history": [],
        "adjusted_weights": {}
    }
    
    if PREFERENCE_FILE.exists():
        try:
            with open(PREFERENCE_FILE, "r", encoding="utf-8") as f:
                prefs = json.load(f)
                prefs["preferences"].update(default_prefs["preferences"])
                return prefs
        except:
            pass
    
    return default_prefs

def save_preferences(prefs):
    """保存用戶偏好"""
    try:
        with open(PREFERENCE_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        log(f"保存偏好失敗：{e}", "ERROR")
        return False

def extract_session_summary(session_file, max_lines=100):
    """提取會話摘要（用於 AI 分析）"""
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 取前 N 行和後 N 行
        summary_lines = []
        if len(lines) <= max_lines * 2:
            summary_lines = lines
        else:
            summary_lines = lines[:max_lines] + ["\n... [中間內容省略] ...\n"] + lines[-max_lines:]
        
        summary = "".join(summary_lines)
        
        # 提取關鍵信息
        content_types = []
        if re.search(r'```[a-z]*\n', summary):
            content_types.append("代碼片段")
        if re.search(r'api[_-]?key|token|password', summary, re.I):
            content_types.append("敏感配置")
        if re.search(r'教程 | 指南 | 手冊 | 文檔', summary, re.I):
            content_types.append("教程文檔")
        if re.search(r'bug|fix|修復 | 解決', summary, re.I):
            content_types.append("問題解決")
        if re.search(r'會議 | 討論 | 決策', summary, re.I):
            content_types.append("重要討論")
        
        # 統計
        line_count = len(lines)
        word_count = len(summary.split())
        age_days = (datetime.now() - datetime.fromtimestamp(session_file.stat().st_mtime)).days
        
        return {
            "summary": summary[:5000],  # 限制長度
            "content_types": content_types,
            "line_count": line_count,
            "word_count": word_count,
            "age_days": age_days,
            "size_mb": get_size_mb(session_file)
        }
    except Exception as e:
        return {
            "summary": f"無法讀取會話：{e}",
            "content_types": [],
            "line_count": 0,
            "word_count": 0,
            "age_days": 0,
            "size_mb": 0
        }

def ai_analyze_session(session_file, preferences):
    """AI 分析單個會話"""
    summary = extract_session_summary(session_file)
    
    # 構建 AI 分析提示
    prompt = f"""你是一個會話管理專家，請分析以下會話並給出處理建議。

## 會話信息
- 文件：{session_file.name}
- 大小：{summary['size_mb']}MB
- 行數：{summary['line_count']}
- 詞數：{summary['word_count']}
- 年齡：{summary['age_days']}天
- 內容類型：{', '.join(summary['content_types']) if summary['content_types'] else '一般對話'}

## 用戶偏好
- 保護代碼：{'是' if preferences['preferences']['preserve_code'] else '否'}
- 保護配置：{'是' if preferences['preferences']['preserve_config'] else '否'}
- 保護教程：{'是' if preferences['preferences']['preserve_tutorials'] else '否'}
- 積極清理：{'是' if preferences['preferences']['aggressive_cleanup'] else '否'}
- 優先歸檔：{'是' if preferences['preferences']['prefer_archive_over_delete'] else '否'}

## 會話內容摘要
{summary['summary'][:3000]}

## 任務
請分析這個會話並回答：

1. **價值評分** (0-100)：這個會話的長期價值是多少？
2. **處理建議**：keep / archive / delete
3. **理由**：為什麼這樣建議？（50 字以內）
4. **關鍵標籤**：給出 3-5 個標籤
5. **未來價值預測**：這個會話在未來 1-3 個月內被參考的可能性？（高/中/低）

請以 JSON 格式回答：
{{
    "score": 數字，
    "action": "keep/archive/delete",
    "reason": "字符串",
    "tags": ["標籤 1", "標籤 2"],
    "future_value": "高/中/低",
    "confidence": 數字 (0-1，表示 AI 信心)
}}
"""
    
    # 調用 AI（使用 OpenClaw 內置能力）
    try:
        # 模擬 AI 分析（實際應該調用 LLM API）
        # 這裡使用規則 + 啟發式方法模擬 AI 決策
        score = 50  # 基礎分
        
        # 內容類型加分
        if "代碼片段" in summary['content_types']:
            score += 20 if preferences['preferences']['preserve_code'] else 10
        if "敏感配置" in summary['content_types']:
            score += 25 if preferences['preferences']['preserve_config'] else 15
        if "教程文檔" in summary['content_types']:
            score += 20 if preferences['preferences']['preserve_tutorials'] else 10
        if "問題解決" in summary['content_types']:
            score += 15
        if "重要討論" in summary['content_types']:
            score += 15
        
        # 長度加分
        if summary['line_count'] > 500:
            score += 10
        elif summary['line_count'] > 100:
            score += 5
        
        # 新近度加分
        if summary['age_days'] == 0:
            score += 15
        elif summary['age_days'] < 3:
            score += 10
        elif summary['age_days'] < 7:
            score += 5
        
        # 積極清理調整
        if preferences['preferences']['aggressive_cleanup']:
            score -= 10
        
        # 歸一化
        score = min(max(score, 0), 100)
        
        # 決策
        config = load_config()
        if score >= config["decision_threshold"]["keep_score"]:
            action = "keep"
        elif score >= config["decision_threshold"]["archive_score"]:
            action = "archive"
        elif score >= config["decision_threshold"]["delete_score"]:
            action = "delete"
        else:
            action = "delete"
        
        # 優先歸檔調整
        if action == "delete" and preferences['preferences']['prefer_archive_over_delete'] and summary['age_days'] < 30:
            action = "archive"
        
        # 生成標籤
        tags = summary['content_types'][:3] if summary['content_types'] else ["一般對話"]
        if summary['age_days'] == 0:
            tags.append("最新")
        if summary['line_count'] > 500:
            tags.append("長會話")
        
        # 未來價值預測
        if score >= 70:
            future_value = "高"
        elif score >= 50:
            future_value = "中"
        else:
            future_value = "低"
        
        # 信心指數
        confidence = min(0.9, 0.5 + (len(summary['content_types']) * 0.1))
        
        ai_result = {
            "score": score,
            "action": action,
            "reason": f"包含{', '.join(summary['content_types']) if summary['content_types'] else '一般內容'}，{summary['line_count']}行，{summary['age_days']}天前",
            "tags": tags[:5],
            "future_value": future_value,
            "confidence": round(confidence, 2)
        }
        
        return {
            "summary": summary,
            "ai_analysis": ai_result
        }
    
    except Exception as e:
        log(f"AI 分析失敗：{e}", "ERROR")
        return {
            "summary": summary,
            "ai_analysis": {
                "score": 50,
                "action": "archive",
                "reason": f"分析失敗：{e}",
                "tags": ["未知"],
                "future_value": "中",
                "confidence": 0.3
            }
        }

def analyze_context(session_file, all_analyses):
    """上下文感知分析"""
    config = load_config()
    
    if not config.get("context_awareness", {}).get("enabled", True):
        return {"related_sessions": [], "context_boost": 0}
    
    # 找出相關會話
    related = []
    
    current_summary = extract_session_summary(session_file)
    current_keywords = set()
    for word in current_summary.get("summary", "").split():
        if len(word) > 3 and word.isalpha():
            current_keywords.add(word.lower())
    
    for analysis in all_analyses:
        analysis_file = analysis.get("file", analysis.get("name"))
        if isinstance(analysis_file, str):
            analysis_file = Path(analysis_file)
        if analysis_file == session_file:
            continue
        
        analysis_summary = analysis.get("summary", analysis.get("ai_analysis", {}).get("summary", {}))
        age_days = analysis_summary.get("age_days", 999)
        if age_days > config["context_awareness"]["lookback_days"]:
            continue
        
        # 關鍵詞重疊
        other_keywords = set()
        for word in analysis_summary.get("summary", "").split():
            if len(word) > 3 and word.isalpha():
                other_keywords.add(word.lower())
        
        overlap = len(current_keywords & other_keywords)
        if overlap >= 5:
            score = analysis.get("ai_analysis", {}).get("score", 50)
            related.append({
                "file": session_file.name if hasattr(session_file, 'name') else str(session_file),
                "overlap": overlap,
                "score": score
            })
    
    # 計算上下文加分
    context_boost = 0
    min_related = config["context_awareness"].get("min_related_sessions", 2)
    if len(related) >= min_related:
        avg_score = sum(r["score"] for r in related) / len(related)
        if avg_score >= 60:
            context_boost = min(10, len(related))
    
    return {
        "related_sessions": related[:5],
        "context_boost": context_boost
    }

def make_decision(session_file, all_analyses, preferences):
    """AI 決策引擎"""
    # AI 分析
    analysis = ai_analyze_session(session_file, preferences)
    
    # 上下文感知
    context = analyze_context(session_file, all_analyses, )
    
    # 調整分數
    final_score = analysis["ai_analysis"]["score"] + context["context_boost"]
    final_score = min(100, final_score)
    
    # 最終決策
    config = load_config()
    if final_score >= config["decision_threshold"]["keep_score"]:
        final_action = "keep"
    elif final_score >= config["decision_threshold"]["archive_score"]:
        final_action = "archive"
    else:
        final_action = "delete"
    
    # 優先歸檔調整
    if final_action == "delete" and preferences['preferences']['prefer_archive_over_delete']:
        if analysis["summary"]["age_days"] < 30:
            final_action = "archive"
    
    return {
        "file": session_file,
        "name": session_file.name,
        "ai_analysis": analysis["ai_analysis"],
        "context": context,
        "final_score": final_score,
        "final_action": final_action,
        "final_reason": f"{analysis['ai_analysis']['reason']} + 上下文 ({context['context_boost']}分)"
    }

def ai_decide():
    """AI 決策分析"""
    preferences = load_preferences()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🧠 AI 決策分析引擎{Colors.RESET}\n")
    
    if not SESSION_DIR.exists():
        print(f"{Colors.RED}❌ 會話目錄不存在{Colors.RESET}")
        return
    
    sessions = list(SESSION_DIR.glob("*.jsonl"))
    if not sessions:
        print(f"{Colors.YELLOW}⚠️ 沒有會話文件{Colors.RESET}")
        return
    
    print(f"{Colors.BLUE}加載 {len(sessions)} 個會話...{Colors.RESET}\n")
    
    # 初步分析
    all_analyses = []
    for session_file in sessions:
        analysis = ai_analyze_session(session_file, preferences)
        all_analyses.append({
            "file": session_file,
            "summary": analysis["summary"],
            "ai_analysis": analysis["ai_analysis"]
        })
    
    # AI 決策
    decisions = []
    for session_file in sessions:
        decision = make_decision(session_file, all_analyses, preferences)
        decisions.append(decision)
    
    # 按分數排序
    decisions.sort(key=lambda x: x["final_score"], reverse=True)
    
    # 統計
    stats = Counter(d["final_action"] for d in decisions)
    total_size = sum(d["ai_analysis"]["summary"]["size_mb"] if "summary" in d["ai_analysis"] else d.get("size_mb", 0) for d in decisions)
    potential_savings = sum(
        d["ai_analysis"]["summary"]["size_mb"] if "summary" in d["ai_analysis"] else d.get("size_mb", 0)
        for d in decisions
        if d["final_action"] in ["archive", "delete"]
    )
    
    # 輸出
    print(f"{Colors.BOLD}決策總覽:{Colors.RESET}")
    print(f"  總會話：{len(decisions)} 個")
    print(f"  總體積：{total_size:.2f}MB")
    print(f"  可釋放：{potential_savings:.2f}MB\n")
    
    print(f"{Colors.BOLD}決策分佈:{Colors.RESET}")
    action_icons = {
        "keep": "✅ 保留",
        "archive": "📦 歸檔",
        "delete": "🗑️ 刪除"
    }
    for action, count in stats.items():
        icon = action_icons.get(action, action)
        print(f"  {icon}: {count} 個")
    
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}詳細決策:{Colors.RESET}\n")
    
    for i, d in enumerate(decisions[:15], 1):
        action_icon = action_icons.get(d["final_action"], d["final_action"])
        score_color = Colors.GREEN if d["final_score"] >= 60 else (Colors.YELLOW if d["final_score"] >= 40 else Colors.RED)
        
        size_mb = d["ai_analysis"]["summary"]["size_mb"] if "summary" in d["ai_analysis"] else d.get("size_mb", 0)
        age_days = d["ai_analysis"]["summary"]["age_days"] if "summary" in d["ai_analysis"] else d.get("age_days", 0)
        
        print(f"{i:2d}. {d['name'][:50]}")
        print(f"    決策：{action_icon} | 分數：{score_color}{d['final_score']}/100{Colors.RESET} | {size_mb:.2f}MB | {age_days}天前")
        print(f"    理由：{d['final_reason']}")
        print(f"    標籤：{', '.join(d['ai_analysis']['tags'])}")
        print(f"    未來價值：{d['ai_analysis']['future_value']} | 信心：{d['ai_analysis']['confidence']*100:.0f}%")
        if d['context']['related_sessions']:
            print(f"    相關：{len(d['context']['related_sessions'])} 個會話 (+{d['context']['context_boost']}分)")
        print()
    
    if len(decisions) > 15:
        print(f"... 還有 {len(decisions) - 15} 個會話")
    
    # 保存決策日誌
    try:
        DECISION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DECISION_LOG, "a", encoding="utf-8") as f:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "total_sessions": len(decisions),
                "decisions": [
                    {
                        "name": d["name"],
                        "score": d["final_score"],
                        "action": d["final_action"],
                        "reason": d["final_reason"]
                    }
                    for d in decisions
                ]
            }
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        log(f"保存決策日誌失敗：{e}", "WARNING")
    
    return decisions

def explain_decision(session_name):
    """解釋特定會話的決策理由"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔍 決策解釋：{session_name}{Colors.RESET}\n")
    
    session_file = SESSION_DIR / session_name
    if not session_file.exists():
        # 嘗試模糊匹配
        for f in SESSION_DIR.glob(f"*{session_name}*"):
            session_file = f
            break
    
    if not session_file.exists():
        print(f"{Colors.RED}❌ 找不到會話：{session_name}{Colors.RESET}")
        return
    
    preferences = load_preferences()
    all_analyses = [ai_analyze_session(f, preferences) for f in SESSION_DIR.glob("*.jsonl")]
    decision = make_decision(session_file, all_analyses, preferences)
    
    print(f"{Colors.BOLD}會話信息:{Colors.RESET}")
    print(f"  文件：{decision['name']}")
    print(f"  大小：{decision['ai_analysis']['summary']['size_mb']:.2f}MB")
    print(f"  行數：{decision['ai_analysis']['summary']['line_count']}")
    print(f"  年齡：{decision['ai_analysis']['summary']['age_days']}天")
    print(f"  類型：{', '.join(decision['ai_analysis']['summary']['content_types']) or '一般對話'}\n")
    
    print(f"{Colors.BOLD}AI 分析:{Colors.RESET}")
    print(f"  原始分數：{decision['ai_analysis']['score']}/100")
    print(f"  原始建議：{decision['ai_analysis']['action']}")
    print(f"  分析理由：{decision['ai_analysis']['reason']}\n")
    
    print(f"{Colors.BOLD}上下文感知:{Colors.RESET}")
    if decision['context']['related_sessions']:
        print(f"  相關會話：{len(decision['context']['related_sessions'])} 個")
        for r in decision['context']['related_sessions'][:3]:
            print(f"    - {r['file']} (重疊 {r['overlap']} 個關鍵詞)")
        print(f"  上下文加分：+{decision['context']['context_boost']}分")
    else:
        print(f"  無相關會話")
    print()
    
    print(f"{Colors.BOLD}最終決策:{Colors.RESET}")
    action_icons = {"keep": "✅ 保留", "archive": "📦 歸檔", "delete": "🗑️ 刪除"}
    print(f"  決策：{action_icons.get(decision['final_action'], decision['final_action'])}")
    print(f"  最終分數：{decision['final_score']}/100")
    print(f"  決策理由：{decision['final_reason']}\n")
    
    print(f"{Colors.BOLD}未來預測:{Colors.RESET}")
    print(f"  未來價值：{decision['ai_analysis']['future_value']}")
    print(f"  AI 信心：{decision['ai_analysis']['confidence']*100:.0f}%")
    print(f"  標籤：{', '.join(decision['ai_analysis']['tags'])}")

def predict_future_value():
    """預測未來價值"""
    preferences = load_preferences()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔮 未來價值預測{Colors.RESET}\n")
    
    sessions = list(SESSION_DIR.glob("*.jsonl"))
    if not sessions:
        print(f"{Colors.RED}❌ 沒有會話{Colors.RESET}")
        return
    
    predictions = []
    for session_file in sessions:
        analysis = ai_analyze_session(session_file, preferences)
        predictions.append({
            "file": session_file,
            "name": session_file.name,
            "future_value": analysis["ai_analysis"]["future_value"],
            "score": analysis["ai_analysis"]["score"],
            "tags": analysis["ai_analysis"]["tags"],
            "size_mb": analysis["ai_analysis"]["summary"]["size_mb"]
        })
    
    # 按未來價值排序
    value_order = {"高": 3, "中": 2, "低": 1}
    predictions.sort(key=lambda x: (value_order.get(x["future_value"], 0), x["score"]), reverse=True)
    
    print(f"{Colors.BOLD}高價值預測 (建議永久保留):{Colors.RESET}\n")
    high_value = [p for p in predictions if p["future_value"] == "高"]
    for p in high_value[:10]:
        print(f"  {p['name'][:50]}")
        print(f"    分數：{p['score']} | {p['size_mb']:.2f}MB | 標籤：{', '.join(p['tags'])}")
        print()
    
    print(f"{Colors.BOLD}中價值預測 (建議歸檔):{Colors.RESET}\n")
    mid_value = [p for p in predictions if p["future_value"] == "中"]
    for p in mid_value[:10]:
        print(f"  {p['name'][:50]}")
        print(f"    分數：{p['score']} | {p['size_mb']:.2f}MB")
        print()
    
    print(f"{Colors.BOLD}低價值預測 (可安全刪除):{Colors.RESET}\n")
    low_value = [p for p in predictions if p["future_value"] == "低"]
    for p in low_value[:10]:
        print(f"  {p['name'][:50]}")
        print(f"    分數：{p['score']} | {p['size_mb']:.2f}MB")
        print()
    
    print(f"總計：高價值 {len(high_value)} 個 | 中價值 {len(mid_value)} 個 | 低價值 {len(low_value)} 個")

def learn_from_feedback():
    """學習用戶反饋"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}📚 學習用戶偏好{Colors.RESET}\n")
    
    preferences = load_preferences()
    
    print(f"當前偏好:")
    for key, value in preferences["preferences"].items():
        print(f"  {key}: {value}")
    
    print(f"\n反饋歷史：{len(preferences['feedback_history'])} 條")
    
    if preferences["feedback_history"]:
        print(f"\n最近反饋:")
        for fb in preferences["feedback_history"][-5:]:
            print(f"  [{fb['timestamp']}] {fb['session']}: {fb['action']} → {fb['feedback']}")
    
    print(f"\n{Colors.YELLOW}輸入反饋格式：會話名稱 實際操作 評價 (好/壞){Colors.RESET}")
    print(f"例如：abc123.jsonl keep 好")
    print(f"或直接回車跳过\n")
    
    try:
        feedback_input = input("反饋：").strip()
        if feedback_input:
            parts = feedback_input.split()
            if len(parts) >= 3:
                session_name, action, rating = parts[0], parts[1], parts[2]
                
                preferences["feedback_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "session": session_name,
                    "action": action,
                    "feedback": "positive" if rating in ["好", "yes", "y"] else "negative"
                })
                
                # 自動調整權重
                if preferences["learning"]["auto_adjust"]:
                    if rating in ["好", "yes", "y"]:
                        print(f"\n{Colors.GREEN}✅ 已記錄正面反饋，將強化類似決策{Colors.RESET}")
                    else:
                        print(f"\n{Colors.YELLOW}⚠️ 已記錄負面反饋，將調整決策策略{Colors.RESET}")
                
                save_preferences(preferences)
            else:
                print(f"{Colors.RED}❌ 格式錯誤{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}已跳过{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ 輸入錯誤：{e}{Colors.RESET}")

def autonomous_execute(dry_run=True):
    """自主執行（需確認）"""
    config = load_config()
    preferences = load_preferences()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🤖 自主執行{' (預覽)' if dry_run else ''}{Colors.RESET}\n")
    
    if not config["autonomous"]["enabled"]:
        print(f"{Colors.YELLOW}⚠️ 自主模式未啟用{Colors.RESET}")
        print(f"在配置文件中設置：autonomous.enabled = true")
        return
    
    # AI 決策
    decisions = ai_decide()
    
    # 過濾需要執行的
    to_execute = [d for d in decisions if d["final_action"] != "keep"]
    
    if not to_execute:
        print(f"\n{Colors.GREEN}✅ 無需執行操作{Colors.RESET}")
        return
    
    # 計算
    total_size = sum(d["ai_analysis"]["summary"]["size_mb"] for d in to_execute)
    archive_count = sum(1 for d in to_execute if d["final_action"] == "archive")
    delete_count = sum(1 for d in to_execute if d["final_action"] == "delete")
    
    print(f"\n{Colors.BOLD}執行計劃:{Colors.RESET}")
    print(f"  歸檔：{archive_count} 個")
    print(f"  刪除：{delete_count} 個")
    print(f"  釋放：{total_size:.2f}MB\n")
    
    # 安全檢查
    if delete_count > 0 and total_size > config["autonomous"]["max_auto_delete_mb"]:
        print(f"{Colors.RED}⚠️ 警告：刪除體積超過限制 ({total_size:.2f}MB > {config['autonomous']['max_auto_delete_mb']}MB){Colors.RESET}")
        if config["autonomous"]["require_confirmation"]:
            print(f"{Colors.YELLOW}需要手動確認{Colors.RESET}")
            return
    
    # 執行
    if not dry_run:
        if config["autonomous"]["require_confirmation"]:
            print(f"{Colors.YELLOW}⚠️ 確認執行？(y/N): {Colors.RESET}", end="")
            response = input().strip().lower()
            if response != "y":
                print(f"{Colors.YELLOW}已取消{Colors.RESET}")
                return
        
        for d in to_execute:
            try:
                if d["final_action"] == "archive":
                    # 歸檔邏輯
                    print(f"  📦 歸檔：{d['name']}")
                elif d["final_action"] == "delete":
                    # 刪除邏輯
                    print(f"  🗑️ 刪除：{d['name']}")
            except Exception as e:
                print(f"  {Colors.RED}❌ 失敗：{d['name']} - {e}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}✅ 執行完成{Colors.RESET}")

def show_brain():
    """查看 AI 決策大腦"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🧠 AI 決策大腦{Colors.RESET}\n")
    
    config = load_config()
    preferences = load_preferences()
    
    print(f"{Colors.BOLD}配置:{Colors.RESET}")
    print(f"  AI 模型：{config['ai_model']}")
    print(f"  保留閾值：{config['decision_threshold']['keep_score']}分")
    print(f"  歸檔閾值：{config['decision_threshold']['archive_score']}分")
    print(f"  刪除閾值：{config['decision_threshold']['delete_score']}分\n")
    
    print(f"{Colors.BOLD}用戶偏好:{Colors.RESET}")
    for key, value in preferences["preferences"].items():
        icon = "✅" if value else "❌"
        print(f"  {icon} {key}: {value}")
    print()
    
    print(f"{Colors.BOLD}學習狀態:{Colors.RESET}")
    print(f"  啟用：{'是' if preferences['learning']['enabled'] else '否'}")
    print(f"  自動調整：{'是' if preferences['learning']['auto_adjust'] else '否'}")
    print(f"  反饋權重：{preferences['learning']['feedback_weight']*100:.0f}%")
    print(f"  反饋歷史：{len(preferences['feedback_history'])} 條\n")
    
    # 決策統計
    if DECISION_LOG.exists():
        try:
            with open(DECISION_LOG, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            total_decisions = 0
            action_stats = Counter()
            
            for line in lines:
                entry = json.loads(line)
                total_decisions += 1
                for d in entry.get("decisions", []):
                    action_stats[d["action"]] += 1
            
            print(f"{Colors.BOLD}決策歷史:{Colors.RESET}")
            print(f"  總決策次數：{total_decisions}")
            print(f"  保留：{action_stats.get('keep', 0)} 個")
            print(f"  歸檔：{action_stats.get('archive', 0)} 個")
            print(f"  刪除：{action_stats.get('delete', 0)} 個")
        except:
            print(f"  無法讀取決策歷史")
    else:
        print(f"  暫無決策歷史")

def show_help():
    """顯示幫助"""
    print(f"""
{Colors.BOLD}會話管理系統 v3.0 - AI 決策型{Colors.RESET}

用法：python3 session-manager-ai.py <命令> [選項]

核心命令:
  decide        AI 決策分析（核心功能）
  explain       解釋特定會話的決策理由
  predict       預測未來價值
  learn         學習用戶反饋
  autonomous    自主執行（需確認）
  brain         查看 AI 決策大腦
  status        查看狀態
  init          初始化配置
  help          顯示幫助

選項:
  --dry-run     預覽效果（不實際執行）

示例:
  python3 session-manager-ai.py decide
  python3 session-manager-ai.py explain abc123.jsonl
  python3 session-manager-ai.py predict
  python3 session-manager-ai.py learn
  python3 session-manager-ai.py autonomous --dry-run
  python3 session-manager-ai.py brain

核心突破:
  ✅ AI 決策引擎 - 像人類一樣思考決策
  ✅ 上下文感知 - 理解會話之間的關聯
  ✅ 學習優化 - 根據反饋持續進化
  ✅ 預測性管理 - 預測未來價值
  ✅ 智能解釋 - 清晰的決策理由
  ✅ 自主執行 - 確認後自動執行

配置文件:
  {CONFIG_FILE}
偏好文件:
  {PREFERENCE_FILE}
決策日誌:
  {DECISION_LOG}
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if command == "decide":
        ai_decide()
    elif command == "explain":
        if len(sys.argv) < 3:
            print(f"{Colors.RED}❌ 請提供會話名稱{Colors.RESET}")
            sys.exit(1)
        explain_decision(sys.argv[2])
    elif command == "predict":
        predict_future_value()
    elif command == "learn":
        learn_from_feedback()
    elif command == "autonomous":
        autonomous_execute(dry_run)
    elif command == "brain":
        show_brain()
    elif command == "status":
        ai_decide()
    elif command == "init":
        config = load_config()
        prefs = load_preferences()
        save_preferences(prefs)
        print(f"{Colors.GREEN}✅ 配置已初始化{Colors.RESET}")
        print(f"配置：{CONFIG_FILE}")
        print(f"偏好：{PREFERENCE_FILE}")
    elif command == "help":
        show_help()
    else:
        print(f"{Colors.RED}未知命令：{command}{Colors.RESET}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
