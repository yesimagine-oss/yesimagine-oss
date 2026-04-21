#!/bin/bash
# 第一梯队技能自动安装脚本
# 每小时安装一个技能，避免速率限制

SKILLS=("gog" "github" "notion" "openai-whisper" "brave-search" "obsidian" "nano-banana-pro" "nano-pdf" "telegram")
LOG_FILE="/home/admin/.openclaw/workspace/learning/skills-installation-log.md"
WAIT_TIME=3600  # 1 小时 = 3600 秒

echo "# 🚀 第一梯队技能自动安装日志" > $LOG_FILE
echo "" >> $LOG_FILE
echo "**启动时间:** $(date '+%Y-%m-%d %H:%M:%S GMT+8')" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "| # | 技能 | 状态 | 时间 | 说明 |" >> $LOG_FILE
echo "|---|------|------|------|------|" >> $LOG_FILE

cd /home/admin/.openclaw/workspace

for i in "${!SKILLS[@]}"; do
    skill="${SKILLS[$i]}"
    num=$((i + 1))
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "" >> $LOG_FILE
    echo "### 安装 #$num: $skill" >> $LOG_FILE
    echo "" >> $LOG_FILE
    echo "**时间:** $timestamp" >> $LOG_FILE
    echo "" >> $LOG_FILE
    echo "~~~bash" >> $LOG_FILE
    
    # 尝试安装
    output=$(clawhub install "$skill" 2>&1)
    exit_code=$?
    
    echo "$output" >> $LOG_FILE
    echo "~~~" >> $LOG_FILE
    echo "" >> $LOG_FILE
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ **状态:** 安装成功" >> $LOG_FILE
        echo "" >> $LOG_FILE
        # 验证安装
        if [ -d "/home/admin/.openclaw/workspace/skills/$skill" ]; then
            echo "📁 **位置:** /home/admin/.openclaw/workspace/skills/$skill" >> $LOG_FILE
            echo "" >> $LOG_FILE
            echo "📄 **文件:**" >> $LOG_FILE
            ls -la "/home/admin/.openclaw/workspace/skills/$skill/" 2>/dev/null | head -10 >> $LOG_FILE
        fi
    else
        echo "❌ **状态:** 安装失败" >> $LOG_FILE
        echo "" >> $LOG_FILE
        echo "**错误:** $output" >> $LOG_FILE
        
        # 检查是否速率限制
        if echo "$output" | grep -q "Rate limit"; then
            echo "" >> $LOG_FILE
            echo "⚠️ **原因:** ClawHub 速率限制" >> $LOG_FILE
            echo "⏰ **建议:** 等待 60 秒后重试..." >> $LOG_FILE
            
            # 重试一次
            sleep 60
            output_retry=$(clawhub install "$skill" 2>&1)
            exit_code_retry=$?
            
            echo "" >> $LOG_FILE
            echo "~~~bash" >> $LOG_FILE
            echo "$output_retry" >> $LOG_FILE
            echo "~~~" >> $LOG_FILE
            
            if [ $exit_code_retry -eq 0 ]; then
                echo "" >> $LOG_FILE
                echo "✅ **重试结果:** 成功！" >> $LOG_FILE
            else
                echo "" >> $LOG_FILE
                echo "❌ **重试结果:** 仍然失败，跳过此技能" >> $LOG_FILE
            fi
        fi
    fi
    
    echo "" >> $LOG_FILE
    echo "---" >> $LOG_FILE
    
    # 如果不是最后一个技能，等待 1 小时
    if [ $i -lt $((${#SKILLS[@]} - 1)) ]; then
        echo "" >> $LOG_FILE
        echo "⏰ **等待:** ${WAIT_TIME}秒 (1 小时) 后安装下一个技能..." >> $LOG_FILE
        echo "" >> $LOG_FILE
        
        # 实际等待
        sleep $WAIT_TIME
    fi
done

echo "" >> $LOG_FILE
echo "---" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "## ✅ 安装完成" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "**完成时间:** $(date '+%Y-%m-%d %H:%M:%S GMT+8')" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "### 总结" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "| 指标 | 数值 |" >> $LOG_FILE
echo "|------|------|" >> $LOG_FILE
echo "| 计划安装 | 9 个 |" >> $LOG_FILE
echo "| 成功安装 | 待统计 |" >> $LOG_FILE
echo "| 失败跳过 | 待统计 |" >> $LOG_FILE
echo "| 总耗时 | 约 8-9 小时 |" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "### 已安装技能列表" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "~~~bash" >> $LOG_FILE
ls -la /home/admin/.openclaw/workspace/skills/ 2>/dev/null | grep -E "^d" | awk '{print $9}' | grep -v "^\." >> $LOG_FILE
echo "~~~" >> $LOG_FILE

echo "" >> $LOG_FILE
echo "---" >> $LOG_FILE
echo "" >> $LOG_FILE
echo "**🎉 第一梯队技能安装完成!**" >> $LOG_FILE
