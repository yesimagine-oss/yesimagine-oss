#!/bin/bash

#############################################
# EvoMap steipete 技能批量安装脚本
# 创建日期：2026-03-14
# 自动处理速率限制，逐个安装技能
#############################################

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 技能列表（按优先级排序）
# 可以根据需要调整顺序或增删
SKILLS=(
    "gog"                    # Google Workspace - 最高优先级
    "notion"                 # Notion API - 最高优先级
    "obsidian"               # Obsidian 集成 - 最高优先级
    "github"                 # GitHub CLI - 高优先级
    "nano-pdf"               # PDF 编辑 - 高优先级
    "nano-banana-pro"        # 图像生成 - 中优先级
    "openai-whisper"         # 语音转文字 - 中优先级
    "trello"                 # Trello 管理 - 中优先级
    "slack"                  # Slack 集成 - 低优先级
    "discord"                # Discord 集成 - 低优先级
    "tmux"                   # tmux 控制 - 低优先级
    "1password"              # 1Password CLI - 低优先级
)

# 配置
MAX_RETRIES=3                # 最大重试次数
WAIT_BETWEEN_SKILLS=600      # 技能间等待时间（秒）= 10 分钟
WAIT_ON_RATE_LIMIT=300       # 速率限制等待时间（秒）= 5 分钟

# 统计
INSTALLED=0
FAILED=0
SKIPPED=0

# 日志文件
LOG_FILE="/home/admin/.openclaw/workspace/install-steipete-$(date +%Y%m%d-%H%M%S).log"

# 开始信息
echo "============================================="
echo "  steipete 技能批量安装脚本"
echo "  创建日期：2026-03-14"
echo "============================================="
echo ""
log_info "日志文件：$LOG_FILE"
log_info "技能总数：${#SKILLS[@]}"
log_info "技能间等待：${WAIT_BETWEEN_SKILLS}秒"
log_info "速率限制等待：${WAIT_ON_RATE_LIMIT}秒"
echo ""

# 记录开始时间
START_TIME=$(date +%s)

# 主安装循环
for i in "${!SKILLS[@]}"; do
    SKILL="${SKILLS[$i]}"
    SKILL_NUM=$((i + 1))
    
    echo ""
    echo "============================================="
    log_info "正在安装技能 [$SKILL_NUM/${#SKILLS[@]}]: $SKILL"
    echo "============================================="
    
    # 检查是否已安装
    if clawhub list 2>&1 | grep -q "^$SKILL[[:space:]]"; then
        log_warning "$SKILL 已经安装，跳过"
        ((SKIPPED++))
        continue
    fi
    
    # 尝试安装（支持重试）
    RETRY=0
    INSTALLED_SUCCESSFULLY=false
    
    while [ $RETRY -lt $MAX_RETRIES ]; do
        if [ $RETRY -gt 0 ]; then
            log_info "第 $RETRY 次重试安装 $SKILL..."
        fi
        
        # 执行安装
        OUTPUT=$(clawhub install "$SKILL" 2>&1)
        EXIT_CODE=$?
        
        # 记录到日志文件
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Install $SKILL (attempt $((RETRY+1))):" >> "$LOG_FILE"
        echo "$OUTPUT" >> "$LOG_FILE"
        echo "---" >> "$LOG_FILE"
        
        if [ $EXIT_CODE -eq 0 ]; then
            log_success "✅ $SKILL 安装成功"
            ((INSTALLED++))
            INSTALLED_SUCCESSFULLY=true
            break
        elif echo "$OUTPUT" | grep -q "Rate limit exceeded"; then
            log_warning "⚠️  速率限制，等待 ${WAIT_ON_RATE_LIMIT}秒后重试..."
            sleep $WAIT_ON_RATE_LIMIT
            ((RETRY++))
        elif echo "$OUTPUT" | grep -q "Already installed"; then
            log_warning "⚠️  $SKILL 已经安装，跳过"
            ((SKIPPED++))
            INSTALLED_SUCCESSFULLY=true
            break
        else
            log_error "❌ $SKILL 安装失败"
            echo "$OUTPUT"
            ((RETRY++))
        fi
    done
    
    # 检查最终结果
    if [ "$INSTALLED_SUCCESSFULLY" = false ]; then
        log_error "❌ $SKILL 安装失败（已重试 $MAX_RETRIES 次）"
        ((FAILED++))
    fi
    
    # 如果不是最后一个技能，等待一段时间
    if [ $i -lt $((${#SKILLS[@]} - 1)) ]; then
        log_info "等待 ${WAIT_BETWEEN_SKILLS}秒后继续安装下一个技能..."
        echo ""
        
        # 倒计时显示
        for SECONDS_LEFT in $(seq $WAIT_BETWEEN_SKILLS -10 10); do
            if [ $((SECONDS_LEFT % 60)) -eq 0 ]; then
                MINUTES=$((SECONDS_LEFT / 60))
                echo -ne "\r等待时间：${MINUTES}分钟   "
            fi
            sleep 10
        done
        echo ""
    fi
done

# 计算总耗时
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))
SECONDS=$((DURATION % 60))

# 最终报告
echo ""
echo "============================================="
echo "  安装完成报告"
echo "============================================="
echo ""
log_info "总技能数：${#SKILLS[@]}"
log_success "成功安装：$INSTALLED"
log_warning "跳过：$SKIPPED"
log_error "失败：$FAILED"
echo ""
log_info "总耗时：${HOURS}小时${MINUTES}分钟${SECONDS}秒"
log_info "日志文件：$LOG_FILE"
echo ""

# 显示已安装的技能列表
echo "============================================="
echo "  当前已安装的 steipete 技能"
echo "============================================="
clawhub list 2>&1 | grep -E "(gog|notion|obsidian|github|nano-pdf|nano-banana-pro|openai-whisper|trello|slack|discord|tmux|1password)" || echo "未找到相关技能"
echo ""

# 生成报告文件
REPORT_FILE="/home/admin/.openclaw/workspace/install-report-$(date +%Y%m%d-%H%M%S).md"
cat > "$REPORT_FILE" << EOF
# steipete 技能安装报告

**安装日期:** $(date '+%Y-%m-%d %H:%M:%S')

## 统计信息

| 项目 | 数量 |
|------|------|
| 总技能数 | ${#SKILLS[@]} |
| 成功安装 | $INSTALLED |
| 跳过 | $SKIPPED |
| 失败 | $FAILED |
| 总耗时 | ${HOURS}小时${MINUTES}分钟${SECONDS}秒 |

## 技能列表

\`\`\`
$(clawhub list 2>&1)
\`\`\`

## 详细日志

请查看：$LOG_FILE

EOF

log_info "安装报告已保存到：$REPORT_FILE"
echo ""
echo "============================================="
echo "  脚本执行完成"
echo "============================================="
