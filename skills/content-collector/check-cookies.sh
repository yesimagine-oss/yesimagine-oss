#!/bin/bash
# 🍪 Cookie 上傳和驗證腳本
# 用途：自動檢查 Cookie 是否正確配置

set -e

# ==================== 配置 ====================
COOKIES_DIR="$HOME/.openclaw/workspace/cookies"
COOKIES_FILE="$COOKIES_DIR/wechat-cookies.json"
SKILL_DIR="$HOME/.openclaw/workspace/skills/content-collector"
TEST_URL="https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw"

# ==================== 顏色 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# ==================== 檢查函數 ====================

check_cookies_file() {
    log_info "檢查 Cookie 文件..."
    
    if [ ! -d "$COOKIES_DIR" ]; then
        log_error "Cookie 目錄不存在：$COOKIES_DIR"
        log_info "創建目錄..."
        mkdir -p "$COOKIES_DIR"
        log_success "目錄已創建"
        return 1
    fi
    
    if [ ! -f "$COOKIES_FILE" ]; then
        log_error "Cookie 文件不存在：$COOKIES_FILE"
        log_info "請先按照教程導出 Cookie："
        echo "   cd $SKILL_DIR"
        echo "   cat QUICK-COOKIE-GUIDE.md"
        return 1
    fi
    
    log_success "Cookie 文件存在"
    
    # 檢查文件大小
    local size=$(stat -f%z "$COOKIES_FILE" 2>/dev/null || stat -c%s "$COOKIES_FILE" 2>/dev/null || echo "0")
    if [ "$size" -lt 100 ]; then
        log_error "Cookie 文件太小（$size 字節），可能為空或格式錯誤"
        return 1
    fi
    
    log_info "文件大小：$size 字節"
    return 0
}

check_cookies_format() {
    log_info "檢查 Cookie 格式..."
    
    # 驗證 JSON 格式
    if ! python3 -m json.tool "$COOKIES_FILE" > /dev/null 2>&1; then
        log_error "Cookie 文件格式錯誤，不是有效的 JSON"
        log_info "請重新導出 Cookie"
        return 1
    fi
    
    log_success "JSON 格式正確"
    
    # 檢查關鍵 Cookie
    log_info "檢查關鍵 Cookie..."
    
    local has_slave_user=$(grep -c '"name": "slave_user"' "$COOKIES_FILE" || echo "0")
    local has_slave_sid=$(grep -c '"name": "slave_sid"' "$COOKIES_FILE" || echo "0")
    
    if [ "$has_slave_user" -gt 0 ]; then
        log_success "找到 slave_user Cookie"
    else
        log_warning "未找到 slave_user Cookie"
    fi
    
    if [ "$has_slave_sid" -gt 0 ]; then
        log_success "找到 slave_sid Cookie"
    else
        log_warning "未找到 slave_sid Cookie"
    fi
    
    # 統計 Cookie 數量
    local total_cookies=$(grep -c '"name":' "$COOKIES_FILE" || echo "0")
    log_info "總共找到 $total_cookies 個 Cookie"
    
    if [ "$total_cookies" -lt 5 ]; then
        log_warning "Cookie 數量較少，可能不完整"
    fi
    
    return 0
}

check_permissions() {
    log_info "檢查文件權限..."
    
    local perms=$(stat -c%a "$COOKIES_FILE" 2>/dev/null || stat -f%OLp "$COOKIES_FILE" 2>/dev/null || echo "644")
    
    if [ "$perms" != "600" ]; then
        log_warning "當前權限：$perms（建議 600）"
        log_info "設置安全權限..."
        chmod 600 "$COOKIES_FILE"
        log_success "權限已設置為 600"
    else
        log_success "權限正確（600）"
    fi
}

test_collection() {
    log_info "測試抓取功能..."
    echo ""
    
    # 設置環境變量
    export WECHAT_COOKIES_ENABLED=true
    export WECHAT_COOKIES_PATH="$COOKIES_FILE"
    
    log_info "使用測試 URL: $TEST_URL"
    log_info "開始抓取..."
    echo ""
    
    cd "$SKILL_DIR"
    
    # 運行抓取（最多等待 90 秒）
    if timeout 90 node index.js "$TEST_URL" 2>&1; then
        echo ""
        log_success "測試成功！"
        return 0
    else
        echo ""
        log_error "測試失敗"
        log_info "可能原因："
        echo "   1. Cookie 已過期 - 請重新導出"
        echo "   2. Cookie 不完整 - 確保包含 slave_user 和 slave_sid"
        echo "   3. 微信風控 - 等待一段時間再試"
        return 1
    fi
}

show_instructions() {
    echo ""
    echo "=========================================="
    echo "📖 下一步操作"
    echo "=========================================="
    echo ""
    
    if [ ! -f "$COOKIES_FILE" ]; then
        log_info "Cookie 文件不存在，請按照以下步驟操作："
        echo ""
        echo "1️⃣ 在本地電腦（Windows/Mac）："
        echo "   - 安裝 Chrome 擴展 'EditThisCookie'"
        echo "   - 訪問 https://mp.weixin.qq.com 並登錄"
        echo "   - 導出 Cookie 為 JSON 文件"
        echo ""
        echo "2️⃣ 上傳到服務器："
        echo "   scp ~/Downloads/wechat-cookies.json admin@服務器 IP:$COOKIES_FILE"
        echo ""
        echo "3️⃣ 重新運行此腳本："
        echo "   bash $0"
        echo ""
    else
        log_info "Cookie 已配置，可以開始使用："
        echo ""
        echo "📦 抓取單篇文章："
        echo "   export WECHAT_COOKIES_ENABLED=true"
        echo "   node $SKILL_DIR/index.js \"https://mp.weixin.qq.com/s/xxx\""
        echo ""
        echo "📚 查看完整教程："
        echo "   cat $SKILL_DIR/QUICK-COOKIE-GUIDE.md"
        echo ""
    fi
}

# ==================== 主程序 ====================

main() {
    echo "=========================================="
    echo "🍪 微信 Cookie 配置檢查工具"
    echo "=========================================="
    echo ""
    
    # 檢查 Cookie 文件
    if ! check_cookies_file; then
        show_instructions
        exit 1
    fi
    
    # 檢查格式
    if ! check_cookies_format; then
        show_instructions
        exit 1
    fi
    
    # 檢查權限
    check_permissions
    
    echo ""
    log_success "✅ Cookie 配置檢查通過！"
    echo ""
    
    # 詢問是否測試
    read -p "是否立即測試抓取功能？(y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_collection
    else
        log_info "跳過測試"
    fi
    
    show_instructions
}

main "$@"
