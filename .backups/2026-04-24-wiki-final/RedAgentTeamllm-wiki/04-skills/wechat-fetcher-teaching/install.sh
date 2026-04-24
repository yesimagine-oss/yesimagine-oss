#!/bin/bash

# 📱 WeChat Fetcher 安裝腳本
# 作者：麻小
# 版本：1.0.0
# 創建：2026-03-18

set -e  # 遇到錯誤立即退出

echo "🦐 開始安裝 WeChat Fetcher..."
echo ""

# 定義目錄
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
COLLECTIONS_DIR="$HOME/.openclaw/workspace/collections"

# 確保目錄存在
echo "📁 檢查目錄結構..."
mkdir -p "$SKILLS_DIR"
mkdir -p "$COLLECTIONS_DIR"/{wechat,wechat/images}
echo "✅ 目錄就緒"
echo ""

# 檢查 Python
echo "🐍 檢查 Python 環境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ 未找到 Python3，請先安裝"
    exit 1
fi
echo ""

# 安裝 Python 依賴
if [ -f "requirements.txt" ]; then
    echo "📦 安裝 Python 依賴..."
    pip3 install -r requirements.txt
    echo "✅ 依賴安裝完成"
else
    echo "ℹ️  無需額外依賴"
fi
echo ""

# 設置執行權限
echo "🔧 設置執行權限..."
chmod +x collector.py 2>/dev/null || true
chmod +x test/test_collector.py 2>/dev/null || true
echo "✅ 權限設置完成"
echo ""

# 運行測試
echo "🧪 運行測試..."
if python3 test/test_collector.py; then
    echo "✅ 測試通過"
else
    echo "⚠️  測試失敗，但安裝繼續"
fi
echo ""

# 驗證安裝
echo "🔍 驗證安裝..."
if [ -f "SKILL.md" ] && [ -f "collector.py" ] && [ -f "README.md" ]; then
    echo "✅ 所有文件存在"
else
    echo "❌ 文件缺失"
    exit 1
fi
echo ""

# 完成提示
echo "=========================================="
echo "✅ WeChat Fetcher 安裝完成！"
echo "=========================================="
echo ""
echo "📝 下一步："
echo "1. 重啟 OpenClaw Gateway:"
echo "   openclaw gateway restart"
echo ""
echo "2. 測試抓取功能:"
echo "   抓取微信文章 https://mp.weixin.qq.com/s/xxx"
echo ""
echo "3. 查看抓取的內容:"
echo "   ls -la ~/.openclaw/workspace/collections/wechat/"
echo ""
echo "📚 學習文檔："
echo "   cat README.md       # 原理文檔"
echo "   cat LEARN.md        # 學習路徑"
echo "   cat collector.py    # 源碼（帶注釋）"
echo ""
echo "=========================================="
