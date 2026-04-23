#!/bin/bash

# 📦 Content Collector 安裝腳本（全自動版）
# 作者：麻小
# 版本：3.0.0
# 創建：2026-03-18

set -e  # 遇到錯誤立即退出

echo "=========================================="
echo "🦐 Content Collector 安裝向導"
echo "=========================================="
echo ""

# 定義目錄
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
COLLECTIONS_DIR="$HOME/.openclaw/workspace/collections"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ==================== 步驟 1: 檢查 Node.js ====================

echo "📋 步驟 1/5: 檢查 Node.js 環境..."

if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    NODE_MAJOR=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    echo "✅ Node.js 已安裝：$NODE_VERSION"
    
    if [ "$NODE_MAJOR" -lt 18 ]; then
        echo "⚠️  警告：Node.js 版本建議 18+（當前：$NODE_VERSION）"
        echo "💡 可能出現兼容性問題，建議升級"
    fi
else
    echo "❌ 未檢測到 Node.js"
    echo ""
    echo "💡 請先安裝 Node.js 18+："
    echo ""
    echo "方法 1: 使用官方腳本（推薦）"
    echo "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "sudo apt-get install -y nodejs"
    echo ""
    echo "方法 2: 使用 nvm"
    echo "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    echo "nvm install 18"
    echo ""
    exit 1
fi

echo ""

# ==================== 步驟 2: 創建目錄 ====================

echo "📋 步驟 2/5: 創建目錄結構..."

mkdir -p "$COLLECTIONS_DIR"/{wechat,articles,images}
echo "✅ 收藏庫目錄：$COLLECTIONS_DIR"

mkdir -p "$SKILLS_DIR"
echo "✅ 技能目錄：$SKILLS_DIR"

echo ""

# ==================== 步驟 3: 安裝 npm 依賴 ====================

echo "📋 步驟 3/5: 安裝 npm 依賴..."
echo "⏳ 這可能需要 2-5 分鐘..."
echo ""

cd "$CURRENT_DIR"

if [ -f "package.json" ]; then
    npm install --loglevel=error
    echo "✅ npm 依賴安裝完成"
else
    echo "❌ 未找到 package.json"
    exit 1
fi

echo ""

# ==================== 步驟 4: 安裝 Chromium 瀏覽器 ====================

echo "📋 步驟 4/5: 安裝 Chromium 瀏覽器..."
echo "⏳ 這可能需要 5-10 分鐘（下載約 200MB）..."
echo ""

npx playwright install chromium
echo "✅ Chromium 瀏覽器安裝完成"

echo ""

# ==================== 步驟 5: 驗證安裝 ====================

echo "📋 步驟 5/5: 驗證安裝..."

# 檢查必要文件
if [ -f "index.js" ] && [ -f "package.json" ] && [ -f "SKILL.md" ]; then
    echo "✅ 所有文件存在"
else
    echo "❌ 文件缺失"
    exit 1
fi

# 檢查 node_modules
if [ -d "node_modules" ]; then
    echo "✅ 依賴已安裝"
else
    echo "❌ 依賴未安裝"
    exit 1
fi

echo ""

# ==================== 完成提示 ====================

echo "=========================================="
echo "✅ Content Collector 安裝完成！"
echo "=========================================="
echo ""
echo "📝 下一步："
echo ""
echo "1. 重啟 OpenClaw Gateway:"
echo "   openclaw gateway restart"
echo ""
echo "2. 測試收藏功能:"
echo "   收藏 https://mp.weixin.qq.com/s/xxx"
echo ""
echo "3. 查看收藏內容:"
echo "   ls -la $COLLECTIONS_DIR/"
echo ""
echo "4. 手動測試（可選）:"
echo "   node index.js https://mp.weixin.qq.com/s/xxx"
echo ""
echo "📚 文檔位置:"
echo "   cat SKILL.md    # 技能說明"
echo "   cat README.md   # 使用教程"
echo ""
echo "❓ 遇到問題？"
echo "   - 檢查 Node.js 版本：node -v"
echo "   - 重新安裝依賴：npm install"
echo "   - 重新安裝瀏覽器：npx playwright install chromium"
echo ""
echo "=========================================="
