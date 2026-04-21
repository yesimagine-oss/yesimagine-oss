#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 服务器限流监控（真实提交测试版 v2）
- 使用实际任务的 Gene 资产进行测试
- 连续发送 5 次请求模拟实际提交的重试行为
- 真实反映 Publish 端点限流状态
- 每 30 分钟检查服务器状态
- 空闲时飞书通知
- 限流时记录日志
"""

import requests
import json
import os
import subprocess
import time
import hashlib
from datetime import datetime
from pathlib import Path

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

# 飞书配置
FEISHU_TARGET_CHAT = os.environ.get("FEISHU_TARGET_CHAT", "oc_5946ad318e5e0c69932ad6c2a73883be")  # 老胡私聊

# 日志文件
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "evomap-monitor.log"

# 状态文件
STATUS_FILE = Path(__file__).parent.parent / "evomap-status.json"

# 任务 1 的基因文件路径（用于真实测试）
TASK1_GENE_PATH = Path(__file__).parent.parent / "tasks/cm645252d3e74b79b97d4f5f7/gene.json"
TASK1_CAPSULE_PATH = Path(__file__).parent.parent / "tasks/cm645252d3e74b79b97d4f5f7/capsule.json"


def log(message):
    """记录日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def send_feishu(message):
    """发送飞书通知（使用 OpenClaw message 工具）"""
    
    try:
        cmd = [
            "openclaw", "message", "send",
            "--target", FEISHU_TARGET_CHAT,
            "--message", message
        ]
        result = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate(timeout=30)
        
        if result.returncode == 0 or "Sent via Feishu" in stdout:
            log("✅ 飞书通知已发送")
            return True
        else:
            log("❌ 发送失败：" + (stderr[:200] if stderr else stdout[:200]))
            return False
    except Exception as e:
        log("❌ 异常：" + str(e))
        return False


def canonicalize(obj):
    """生成 canonical JSON（与实际提交脚本一致）"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'


def compute_asset_id(obj):
    """计算 asset_id（与实际提交脚本一致）"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'


def check_server_status():
    """检查 EvoMap 服务器状态（使用实际任务资产进行真实测试）"""
    
    # 1. 检查 Heartbeat 端点
    url = "https://evomap.ai/a2a/heartbeat"
    headers = {"Authorization": f"Bearer {NODE_SECRET}"}
    payload = {"node_id": NODE_ID}
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            credit = data.get("credit_balance", 0)
            node_status = data.get("node_status", "unknown")
            tasks = data.get("available_tasks", [])
            work = data.get("available_work", [])
            
            heartbeat_ok = True
            heartbeat_msg = "Heartbeat 空闲"
        
        elif resp.status_code == 429:
            return {
                "status": "rate_limited",
                "code": 429,
                "retry_sec": resp.json().get("retry_after_ms", 3000) / 1000,
                "message": "Heartbeat 限流"
            }
        else:
            return {"status": "error", "code": resp.status_code, "message": f"Heartbeat HTTP {resp.status_code}"}
    
    except Exception as e:
        return {"status": "error", "code": 0, "message": f"Heartbeat 错误：{e}"}
    
    # 2. 加载实际任务的 Gene 资产（如果存在）
    test_gene = None
    if TASK1_GENE_PATH.exists():
        try:
            with open(TASK1_GENE_PATH, 'r', encoding='utf-8') as f:
                test_gene = json.load(f)
            # 移除 asset_id（会重新计算）
            if 'asset_id' in test_gene:
                del test_gene['asset_id']
            log(f"✅ 加载实际任务 Gene: {len(json.dumps(test_gene))} 字节")
        except Exception as e:
            log(f"⚠️ 加载实际任务 Gene 失败：{e}，使用模拟数据")
    
    # 如果没有实际任务 Gene，使用模拟数据
    if not test_gene:
        test_gene = {
            "type": "Gene",
            "schema_version": "1.6.0",
            "category": "monitor",
            "signals_match": ["monitor", "health-check", "publish-test", "endpoint-verification", "server-status"],
            "summary": "EvoMap 监控健康检查 - 真实提交格式测试 Publish 端点可用性和限流状态",
            "strategy": [
                "步骤 1: 构建与实际提交大小相近的 Gene 资产（约 2000 字节）",
                "步骤 2: 计算 asset_id 使用 canonical JSON 序列化",
                "步骤 3: 连续发送 5 次请求模拟实际提交的重试行为",
                "步骤 4: 分析 HTTP 状态码序列：全 400=空闲，出现 429=限流",
                "步骤 5: 返回真实限流状态供用户参考"
            ],
            "constraints": {
                "max_files": 1,
                "max_lines": 1000,
                "forbidden_paths": ["node_modules/", ".env", ".git/", "__pycache__/"]
            },
            "validation": [
                "HTTP 状态码为 200 表示端点空闲可提交",
                "HTTP 状态码 429 表示限流需等待",
                "HTTP 状态码 400 表示验证错误（非限流）",
                "连续 5 次请求无 429 表示当前不限流",
                "响应时间小于 10 秒"
            ]
        }
    
    # 3. 检查 Publish 端点（使用实际任务资产，连续发送 5 次）
    publish_ok = False
    publish_msg = ""
    publish_code = 0
    status_codes = []
    retry_after = 0
    
    url = "https://evomap.ai/a2a/publish"
    headers = {
        "Authorization": f"Bearer {NODE_SECRET}",
        "Content-Type": "application/json"
    }
    
    # 连续发送 5 次请求，模拟实际提交的重试行为
    # 原因：单次 400 不代表不限流，连续请求才会触发累积限流
    test_count = 5
    log(f"开始 Publish 端点测试（连续{test_count}次，使用{'实际任务' if TASK1_GENE_PATH.exists() else '模拟'}资产）")
    
    for i in range(test_count):
        # 计算 asset_id（每次使用新的 message_id）
        test_gene_copy = test_gene.copy()
        asset_id = compute_asset_id(test_gene_copy)
        test_gene_copy['asset_id'] = asset_id
        
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "publish",
            "message_id": f"monitor_{int(time.time()*1000)}_{i}",
            "sender_id": NODE_ID,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "payload": {"assets": [test_gene_copy]}
        }
        
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            status_codes.append(resp.status_code)
            
            if resp.status_code == 429:
                data = resp.json()
                retry_after = max(retry_after, data.get("retry_after_ms", 3000))
                publish_ok = False
                publish_msg = f"Publish 限流 ❌ ({retry_after/1000}秒) - 第{i+1}次触发"
                log(f"  请求 {i+1}: HTTP {resp.status_code} → 限流")
                break
            elif resp.status_code == 200:
                publish_ok = True
                publish_msg = "Publish 空闲 ✅"
                log(f"  请求 {i+1}: HTTP {resp.status_code} → 空闲")
            elif resp.status_code == 400:
                # 400 表示验证错误，继续下一次测试
                log(f"  请求 {i+1}: HTTP {resp.status_code} → 验证错误（继续）")
                continue
            else:
                publish_ok = False
                publish_msg = f"Publish HTTP {resp.status_code}"
                log(f"  请求 {i+1}: HTTP {resp.status_code} → 异常")
                break
                
        except requests.exceptions.Timeout:
            publish_ok = False
            publish_msg = "Publish 超时 ❌"
            log(f"  请求 {i+1}: 超时")
            break
        except Exception as e:
            publish_ok = False
            publish_msg = f"Publish 错误 ❌: {e}"
            log(f"  请求 {i+1}: 错误 {e}")
            break
    
    # 汇总结果
    if publish_ok:
        publish_msg = f"Publish 空闲 ✅ (连续{test_count}次测试通过)"
    elif not publish_ok and 429 in status_codes:
        publish_msg = f"Publish 限流 ❌ ({retry_after/1000}秒) - 连续请求触发限流"
    elif all(code == 400 for code in status_codes):
        publish_ok = True
        publish_msg = "Publish 空闲 ⚠️ (400 验证错误，未触发限流)"
    
    publish_code = status_codes[-1] if status_codes else 0
    log(f"Publish 测试结果：{status_codes} → {publish_msg}")
    
    # 综合判断
    if heartbeat_ok and publish_ok:
        return {
            "status": "ok",
            "code": 200,
            "credit": credit,
            "node_status": node_status,
            "available_tasks": len(tasks),
            "available_work": len(work),
            "heartbeat": heartbeat_msg,
            "publish_code": publish_code,
            "publish": publish_msg,
            "message": "服务器空闲（可提交/发布）"
        }
    elif heartbeat_ok and not publish_ok:
        return {
            "status": "partial",
            "code": 200,
            "credit": credit,
            "heartbeat": heartbeat_msg,
            "publish_code": publish_code,
            "publish": publish_msg,
            "message": "⚠️ Publish 端点限流，建议等待或 Web UI 提交"
        }
    else:
        return {"status": "error", "message": heartbeat_msg}


def save_status(result):
    """保存状态到文件"""
    status = {
        "last_check": datetime.utcnow().isoformat() + "Z",
        "status": result.get("status"),
        "code": result.get("code"),
        "message": result.get("message"),
        "credit": result.get("credit"),
        "available_tasks": result.get("available_tasks", 0),
        "available_work": result.get("available_work", 0),
        "heartbeat": result.get("heartbeat"),
        "publish": result.get("publish"),
        "publish_code": result.get("publish_code"),
        "consecutive_ok": 0 if result["status"] != "ok" else 1,
        "best_hours": ["02:00-06:00", "12:00-14:00"]
    }
    
    # 读取历史状态
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r") as f:
                history = json.load(f)
                if result["status"] == "ok":
                    status["consecutive_ok"] = history.get("consecutive_ok", 0) + 1
        except:
            pass
    
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    log("="*60)
    log("开始检查 EvoMap 服务器状态（真实提交测试 v2）")
    
    result = check_server_status()
    save_status(result)
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if result["status"] == "ok":
        # 服务器空闲，发送通知
        credit = result.get("credit", 0)
        tasks = result.get("available_tasks", 0)
        work = result.get("available_work", 0)
        
        message = f"""🟢 [{ts}] EvoMap 服务器空闲，可以提交任务或发布资产

💰 积分余额：{credit}
📋 可用任务：{tasks} 个
💼 可用工作：{work} 个
❤️ Heartbeat: {result.get('heartbeat', 'OK')}
📤 Publish: {result.get('publish', 'OK')}
⏰ 最佳时段：02:00-06:00, 12:00-14:00"""
        
        log(f"✅ {result['message']} | 积分：{credit} | 任务：{tasks} | 工作：{work}")
        log(f"   Heartbeat: {result.get('heartbeat')} | Publish: {result.get('publish')}")
        send_feishu(message)
        
    elif result["status"] == "partial":
        # Publish 端点限流
        credit = result.get("credit", 0)
        
        message = f"""🟡 [{ts}] EvoMap 服务器部分限流

💰 积分余额：{credit}
❤️ Heartbeat: {result.get('heartbeat', 'OK')}
📤 Publish: {result.get('publish', '限流')}
⚠️ 建议：等待 Publish 端点恢复或使用 Web UI 手动提交"""
        
        log(f"⚠️ {result['message']} | Heartbeat: {result.get('heartbeat')} | Publish: {result.get('publish')}")
        send_feishu(message)
        
    elif result["status"] == "rate_limited":
        retry = result.get("retry_sec", 3)
        log(f"❌ {result['message']} | {retry}秒后重试")
        
    else:
        log(f"⚠️ {result['message']} | HTTP {result.get('code', 0)}")
    
    log("="*60)
    return result["status"] == "ok"


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
