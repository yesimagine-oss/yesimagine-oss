#!/bin/bash
#==============================================================================
# Red AgentTeam Health Check - 节点健康检查脚本
# 监控 Evolver + OpenClaw 状态，挂掉则飞书通知
# 
# 制作思路：
# 1. 背景：我们 Evolver 曾停机 4 天无人知晓，靠偶然检查才发现
# 2. 目标：自动化监控，挂了立即通知，不依赖人工巡查
# 3. 通知渠道：复用 goToken 已配置的飞书 Webhook
# 4. 检测内容：Evolver 进程、Hub 心跳、积分余额
# 5. 阈值：积分 < 1000 或 进程不在 或 心跳超时 = 告警
#
# 使用方式：
#   bash health-check.sh              # 单次执行
#   crontab -e                        # 添加定时任务
#   */5 * * * * /path/to/health-check.sh  # 每 5 分钟跑一次
#==============================================================================

set -u

# ---------- 配置 ----------
NODE_SECRET="41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c"
NODE_ID="node_b83d6e6008dce32f"
HUB_URL="https://evomap.ai"
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/2-8e83d0c7-86db-47e6-b7ac-2c09e0b6"

# 告警阈值
CREDIT_THRESHOLD=1000
MAX_HEARTBEAT_AGE_SEC=600   # 超过10分钟没心跳 = 告警

# 日志
LOG_FILE="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/health-check.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------- 工具函数 ----------
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

send_feishu() {
    local msg="$1"
    local payload=$(cat <<EOF
{
    "msg_type": "text",
    "content": {
        "text": "$msg"
    }
}
EOF
)
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "$payload" > /dev/null 2>&1
}

check_evolver_process() {
    # 检查 Evolver node 进程是否在跑
    pgrep -f "node.*evolver\|evolver.*run.*loop" > /dev/null 2>&1
}

get_heartbeat_age() {
    # 读取 evolution_state.json 的 lastRun，计算年龄（秒）
    local state_file="/home/admin/.openclaw/workspace/.evolver/memory/evolution/evolution_state.json"
    if [[ ! -f "$state_file" ]]; then
        echo 9999
        return
    fi
    local last_run=$(python3 -c "import json; d=json.load(open('$state_file')); print(d.get('lastRun', 0))" 2>/dev/null)
    if [[ "$last_run" == "0" || -z "$last_run" ]]; then
        echo 9999
        return
    fi
    local now_ms=$(python3 -c "import time; print(int(time.time() * 1000))")
    local age_ms=$((now_ms - last_run))
    echo $((age_ms / 1000))
}

get_hub_credits() {
    # 发 hello 获取积分余额
    local ts=$(date +%s)
    local envelope=$(cat <<EOF
{
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": "msg_${ts}_health",
    "sender_id": "$NODE_ID",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "payload": {
        "capabilities": {
            "evolver": {
                "version": "1.69.21",
                "installed_at": "/usr/lib/node_modules/@evomap/evolver",
                "binary": "/usr/bin/evolver"
            }
        },
        "env_fingerprint": {
            "device_id": "iZm5ei3ekpe8wbnvf7snni",
            "node_version": "v24.14.0",
            "platform": "linux",
            "arch": "x64",
            "os_release": "5.10.134",
            "hostname": "iZm5ei3ekpe8wbnvf7snni",
            "evolver_version": "1.69.21",
            "client": "openclaw",
            "client_version": "2026.3.3",
            "region": "cn-shanghai",
            "cwd": "/home/admin/.openclaw/workspace",
            "container": false,
            "captured_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        }
    }
}
EOF
)
    echo "$envelope" | python3 -c "
import sys, json, urllib.request, time
d = json.load(sys.stdin)
req = urllib.request.Request(
    'https://evomap.ai/a2a/hello',
    data=json.dumps(d).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer 41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c'},
    method='POST'
)
with urllib.request.urlopen(req, timeout=15) as r:
    result = json.loads(r.read().decode())
    credits = result.get('payload', {}).get('credit_balance', 'N/A')
    print(credits)
" 2>/dev/null
}

# ---------- 主检测流程 ----------
main() {
    log "========== 开始健康检查 =========="
    
    alerts=()
    
    # 1. 检查 Evolver 进程
    if check_evolver_process; then
        log "✅ Evolver 进程正常"
    else
        log "❌ Evolver 进程未运行"
        alerts+=("🔴 Evolver 进程未运行")
    fi
    
    # 2. 检查 Hub 心跳年龄
    heartbeat_age=$(get_heartbeat_age)
    log "心跳年龄: ${heartbeat_age}秒"
    if (( heartbeat_age > MAX_HEARTBEAT_AGE_SEC )); then
        log "❌ Hub 心跳超时（${heartbeat_age}秒）"
        alerts+=("🔴 Hub 心跳超时（${heartbeat_age}秒）")
    else
        log "✅ Hub 心跳正常（${heartbeat_age}秒前）"
    fi
    
    # 3. 检查积分余额
    credits=$(get_hub_credits)
    if [[ "$credits" != "N/A" && "$credits" != "" ]]; then
        log "积分余额: $credits"
        if [[ "$credits" =~ ^[0-9]+$ ]] && (( credits < CREDIT_THRESHOLD )); then
            log "⚠️ 积分低于阈值：$credits < $CREDIT_THRESHOLD"
            alerts+=("⚠️ 积分告警：当前 $credits，低于阈值 $CREDIT_THRESHOLD")
        fi
    else
        log "⚠️ 无法获取积分余额"
    fi
    
    # 4. 如有告警，发飞书通知
    if (( ${#alerts[@]} > 0 )); then
        alert_msg="【节点告警】$(hostname) $(date '+%m-%d %H:%M')\n"
        for a in "${alerts[@]}"; do
            alert_msg+="$a\n"
        done
        alert_msg="${alert_msg%\\n}"
        log "📲 发送飞书告警..."
        send_feishu "$alert_msg"
        log "📲 飞书告警已发送"
    else
        log "✅ 所有检查通过，无告警"
    fi
    
    log "========== 健康检查完成 =========="
}

main "$@"
