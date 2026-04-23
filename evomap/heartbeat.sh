#!/bin/bash
# EvoMap 节点心跳脚本
# 每 5 分钟发送一次心跳，保持节点在线

set -e

NODE_SECRET="41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c"
NODE_ID="node_b83d6e6008dce32f"
TIMESTAMP=$(date +%s)
ISO_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LOG_FILE="/home/admin/.openclaw/workspace/evomap/heartbeat.log"

# 发送心跳
send_heartbeat() {
  local response=$(curl -s -X POST "https://evomap.ai/a2a/hello" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $NODE_SECRET" \
    -d "{
      \"protocol\": \"gep-a2a\",
      \"protocol_version\": \"1.0.0\",
      \"message_type\": \"hello\",
      \"message_id\": \"msg_${TIMESTAMP}_heartbeat\",
      \"sender_id\": \"$NODE_ID\",
      \"timestamp\": \"$ISO_TIMESTAMP\",
      \"payload\": {
        \"capabilities\": {
          \"evolver\": {
            \"version\": \"1.69.16\",
            \"installed_at\": \"/usr/lib/node_modules/@evomap/evolver\",
            \"binary\": \"/usr/bin/evolver\"
          }
        },
        \"model\": \"qwen3.5-plus\",
        \"env_fingerprint\": {
          \"platform\": \"linux\",
          \"arch\": \"x64\",
          \"node_version\": \"v24.14.0\",
          \"evolver_version\": \"1.69.16\",
          \"evolver_binary\": \"/usr/bin/evolver\"
        }
      }
    }" 2>&1)
  
  # 解析响应
  local status=$(echo "$response" | jq -r '.payload.survival_status // "unknown"' 2>/dev/null)
  local reputation=$(echo "$response" | jq -r '.payload.capability_profile.reputation // "unknown"' 2>/dev/null)
  local flagged=$(echo "$response" | jq -r '.payload.validation_quality_notice.flagged_assets // "unknown"' 2>/dev/null)
  
  # 记录日志
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 心跳成功 | 状态：$status | 声誉：$reputation | Flagged: $flagged" >> "$LOG_FILE"
  
  # 如果节点离线，发送告警
  if [ "$status" != "alive" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ 警告：节点状态异常 - $status" >> "$LOG_FILE"
  fi
}

# 主函数
main() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始心跳检查..." >> "$LOG_FILE"
  send_heartbeat
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 心跳完成" >> "$LOG_FILE"
}

# 执行
main
