#!/bin/bash
# EvoMap 增强技能安装脚本
# 功能：安装 capability-evolver + self-evolve + evoclaw
# 通知：安装前/成功/失败都飞书通知

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/../logs/skill-install.log"
NOTIFIER="/home/admin/.openclaw/workspace/tools/task-notifier.py"

# 技能列表
SKILLS=("capability-evolver" "self-evolve" "evoclaw")

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 飞书通知函数
send_notification() {
    local title="$1"
    local content="$2"
    python3 "$NOTIFIER" start "$title" "$content" "5" 2>&1 | tee -a "$LOG_FILE"
}

# 检查技能是否已安装
check_skill_installed() {
    local skill_name="$1"
    if [ -d "/opt/openclaw/skills/$skill_name" ] || [ -d "/home/admin/.openclaw/workspace/skills/$skill_name" ]; then
        return 0
    else
        return 1
    fi
}

# 安装单个技能
install_skill() {
    local skill_name="$1"
    log "开始安装：$skill_name"
    
    # 检查是否已安装
    if check_skill_installed "$skill_name"; then
        log "✅ $skill_name 已安装，跳过"
        return 0
    fi
    
    # 尝试安装（最多重试 3 次）
    local max_retries=3
    local retry=0
    
    while [ $retry -lt $max_retries ]; do
        log "尝试安装：$skill_name (第 $((retry+1))/$max_retries 次)"
        
        # 使用 clawhub 安装
        if clawhub install "$skill_name" --force 2>&1 | tee -a "$LOG_FILE"; then
            log "✅ $skill_name 安装成功"
            
            # 验证安装
            if check_skill_installed "$skill_name"; then
                log "✅ $skill_name 验证通过"
                return 0
            else
                log "⚠️ $skill_name 安装成功但验证失败"
            fi
        else
            log "❌ $skill_name 安装失败 (第 $((retry+1)) 次)"
        fi
        
        retry=$((retry+1))
        
        # 等待 5 秒后重试
        if [ $retry -lt $max_retries ]; then
            log "等待 5 秒后重试..."
            sleep 5
        fi
    done
    
    log "❌ $skill_name 安装失败（已重试 $max_retries 次）"
    return 1
}

# 主函数
main() {
    log "========================================="
    log "开始安装 EvoMap 增强技能"
    log "========================================="
    
    # 发送安装前通知
    send_notification "📦 开始安装 EvoMap 增强技能" \
        "即将安装 3 个技能：
1. capability-evolver - 能力进化
2. self-evolve - 自我进化
3. evoclaw - 平台集成

安装过程可能需要 5-10 分钟，请稍候..."
    
    # 统计
    local success=0
    local failed=0
    local skipped=0
    
    # 安装每个技能
    for skill in "${SKILLS[@]}"; do
        if check_skill_installed "$skill"; then
            log "⏭️ $skill 已安装，跳过"
            skipped=$((skipped+1))
        else
            if install_skill "$skill"; then
                success=$((success+1))
            else
                failed=$((failed+1))
            fi
        fi
    done
    
    # 发送结果通知
    if [ $failed -eq 0 ]; then
        send_notification "✅ EvoMap 增强技能安装完成" \
            "安装结果：
✅ 成功：$success 个
⏭️ 跳过：$skipped 个
❌ 失败：$failed 个

已安装技能：
$(for skill in "${SKILLS[@]}"; do check_skill_installed "$skill" && echo "✅ $skill"; done)

下一步：
1. 重启 OpenClaw
2. 配置技能参数
3. 测试技能功能"
    else
        send_notification "⚠️ EvoMap 增强技能安装部分失败" \
            "安装结果：
✅ 成功：$success 个
⏭️ 跳过：$skipped 个
❌ 失败：$failed 个

失败原因：
可能是 ClawHub 速率限制或网络问题

解决方案：
1. 等待 10 分钟后重试
2. 检查网络连接
3. 手动从 GitHub 下载安装

查看详细日志：
$LOG_FILE"
    fi
    
    log "========================================="
    log "安装完成：成功=$success, 跳过=$skipped, 失败=$failed"
    log "========================================="
    
    # 返回结果
    [ $failed -eq 0 ]
}

# 执行
main "$@"
