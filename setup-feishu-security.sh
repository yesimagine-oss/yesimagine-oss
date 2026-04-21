#!/bin/bash
# 飞书安全策略快速配置脚本

echo "🔐 飞书安全策略配置"
echo "===================="
echo ""

# 创建配置目录
echo "📁 创建配置目录..."
mkdir -p ~/.openclaw/workspace/.config/security
mkdir -p ~/.openclaw/workspace/logs/security

# 创建安全配置文件
echo "📝 创建安全配置文件..."
cat > ~/.openclaw/workspace/.config/security/feishu-security.json << 'EOF'
{
  "sync": {
    "enabled": true,
    "sync_work_progress": true,
    "sync_task_result": true,
    "sync_error_notify": true,
    "sync_group_messages": false,
    "sync_private_messages": false
  },
  "security": {
    "group_types": {
      "private": {"level": "top_secret", "sync": true},
      "internal": {"level": "sensitive", "sync": false},
      "external": {"level": "internal", "sync": false}
    }
  },
  "permission": {
    "user_private": {"answer": true, "execute": true},
    "user_internal": {"answer": true, "sanitize": true},
    "user_external": {"answer": true, "public_only": true},
    "other_internal": {"answer": false, "require_approval": true},
    "other_external": {"answer": false, "require_approval": false}
  },
  "responses": {
    "skill_show_internal": "📋 技能展示\n\n说出你的需求，我给你找对应技能。\n\n目前支持:\n• 信息搜索 (Google/微信)\n• 内容摘要 (URL/文件)\n• 自动化任务\n• 数据分析\n• 文档处理\n\n请描述你的具体需求~",
    "skill_show_external": "💡 看起来你什么也没教会我，你要加油喔！\n\n不过我可以帮你:\n• 信息搜索\n• 内容摘要\n• 简单问答\n\n如果需要更多帮助，请联系管理员获取完整技能列表~",
    "help_request_template": "@用户 您好，[群类型] 有成员需要帮助：\n\n[问题摘要]\n\n是否可以提供帮助？🤔"
  },
  "timeout": {
    "approval_wait_minutes": 5,
    "reminder_minutes": 2,
    "auto_reject": true
  }
}
EOF

# 创建日志目录结构
echo "📂 创建日志目录..."
touch ~/.openclaw/workspace/logs/security/access.log
touch ~/.openclaw/workspace/logs/security/operation.log
touch ~/.openclaw/workspace/logs/security/sync.log
touch ~/.openclaw/workspace/logs/security/audit.log

# 设置权限
echo "🔒 设置文件权限..."
chmod 600 ~/.openclaw/workspace/.config/security/feishu-security.json
chmod 700 ~/.openclaw/workspace/logs/security/

# 验证配置
echo ""
echo "✅ 验证配置..."
if [ -f ~/.openclaw/workspace/.config/security/feishu-security.json ]; then
    echo "✅ 安全配置文件已创建"
else
    echo "❌ 安全配置文件创建失败"
    exit 1
fi

if [ -d ~/.openclaw/workspace/logs/security ]; then
    echo "✅ 安全日志目录已创建"
else
    echo "❌ 安全日志目录创建失败"
    exit 1
fi

echo ""
echo "===================="
echo "🎉 配置完成！"
echo ""
echo "📋 配置文件位置:"
echo "   ~/.openclaw/workspace/.config/security/feishu-security.json"
echo ""
echo "📂 日志文件位置:"
echo "   ~/.openclaw/workspace/logs/security/"
echo ""
echo "📖 查看完整文档:"
echo "   ~/.openclaw/workspace/FEISHU-SECURITY-STRATEGY.md"
echo ""
