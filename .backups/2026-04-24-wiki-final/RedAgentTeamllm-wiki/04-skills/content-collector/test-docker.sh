#!/bin/bash
# 🧪 Content Collector - Docker 測試腳本
# 作者：麻小 | 創建：2026-03-19
# 用途：快速測試 Docker 環境下的抓取功能

set -e

# ==================== 配置 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="content-collector:latest"
CONTAINER_NAME="content-collector-test"

# 測試 URL 列表
TEST_URLS=(
    "https://mp.weixin.qq.com/s/4pFM8ILPNOzfw9G_9rV5Dw"
    "https://mp.weixin.qq.com/s/r8F0kXGzGQOvXqWqzjXxXg"
)

# ==================== 顏色輸出 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# ==================== 函數 ====================

# 檢查 Docker 是否可用
check_docker() {
    log_info "檢查 Docker 環境..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker 未運行或無權限"
        exit 1
    fi
    
    log_success "Docker 環境正常"
}

# 構建鏡像
build_image() {
    log_info "構建 Docker 鏡像..."
    
    cd "$SCRIPT_DIR"
    
    if docker image inspect "$IMAGE_NAME" &> /dev/null; then
        log_warning "鏡像已存在，是否重新構建？(y/n)"
        read -r response
        if [[ "$response" != "y" ]]; then
            log_success "使用現有鏡像"
            return
        fi
    fi
    
    docker build -t "$IMAGE_NAME" .
    
    if [ $? -eq 0 ]; then
        log_success "鏡像構建成功"
    else
        log_error "鏡像構建失敗"
        exit 1
    fi
}

# 測試單個 URL
test_url() {
    local url="$1"
    local test_num="$2"
    
    log_info "測試 #$test_num: $url"
    
    # 運行容器
    docker run --rm \
        --name "$CONTAINER_NAME" \
        -v ~/.openclaw/workspace/collections:/app/collections \
        -e COLLECTIONS_DIR=/app/collections \
        -e TZ=Asia/Shanghai \
        --network host \
        "$IMAGE_NAME" \
        node index.js "$url"
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_success "測試 #$test_num 成功"
        return 0
    else
        log_error "測試 #$test_num 失敗 (exit code: $exit_code)"
        return 1
    fi
}

# 清理舊容器
cleanup() {
    log_info "清理舊容器..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
}

# 顯示幫助
show_help() {
    cat << EOF
📦 Content Collector - Docker 測試腳本

用法：
  $0 [選項]

選項:
  -b, --build      只構建鏡像，不測試
  -t, --test URL   測試指定 URL
  -a, --all        測試所有預設 URL
  -c, --clean      清理測試容器
  -h, --help       顯示幫助

示例:
  $0                    # 使用預設 URL 測試
  $0 -b                 # 只構建鏡像
  $0 -t "https://..."   # 測試指定 URL
  $0 -a                 # 測試所有 URL

EOF
}

# ==================== 主程序 ====================

main() {
    # 解析參數
    BUILD_ONLY=false
    TEST_URL=""
    TEST_ALL=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -b|--build)
                BUILD_ONLY=true
                shift
                ;;
            -t|--test)
                TEST_URL="$2"
                shift 2
                ;;
            -a|--all)
                TEST_ALL=true
                shift
                ;;
            -c|--clean)
                cleanup
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知參數：$1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 執行
    check_docker
    cleanup
    
    if [ "$BUILD_ONLY" = true ]; then
        build_image
        exit 0
    fi
    
    build_image
    
    if [ -n "$TEST_URL" ]; then
        test_url "$TEST_URL" 1
    elif [ "$TEST_ALL" = true ]; then
        local i=1
        for url in "${TEST_URLS[@]}"; do
            test_url "$url" $i
            ((i++))
        done
    else
        # 預設測試第一個 URL
        test_url "${TEST_URLS[0]}" 1
    fi
    
    log_success "測試完成！"
    log_info "查看收藏內容：ls -la ~/.openclaw/workspace/collections/wechat/"
}

main "$@"
