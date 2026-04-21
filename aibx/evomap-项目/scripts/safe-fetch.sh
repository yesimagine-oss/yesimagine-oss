#!/bin/bash
# 安全获取热门资产脚本 - 带积分检查

echo "=============================================="
echo "📚 安全获取热门资产"
echo "=============================================="

# 检查积分
python3 /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/credit_protect.py

# 询问用户
echo ""
read -p "是否继续获取热门资产？(消耗 100 积分) [y/N]: " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo "📤 执行获取..."
    # 恢复临时脚本
    mv /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/asset_browser.py.disabled \
       /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/asset_browser.py.tmp
    
    # 运行一次
    python3 /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/asset_browser.py.tmp
    
    # 重新禁用
    mv /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/asset_browser.py.tmp \
       /home/admin/.openclaw/workspace/aibx/evomap-项目/lib/asset_browser.py.disabled
    
    echo "✅ 获取完成，脚本已重新禁用"
else
    echo "❌ 操作已取消"
fi
