#!/bin/bash
# 🧪 飞书文档功能测试脚本
# 用途：测试飞书文档创建、写入、上传功能

set -e

# ==================== 配置 ====================
USER_OPEN_ID="ou_f4919832188bcc630f8f257497fa93a4"  # 老胡的飞书用户 ID
TEST_DOC_TITLE="测试文档 - $(date +%Y-%m-%d-%H-%M-%S)"
TEST_CONTENT="# 测试文档\n\n这是通过 API 创建的测试文档。\n\n创建时间：$(date)"

# ==================== 颜色 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# ==================== 测试函数 ====================

test_create_doc() {
    log_info "测试 1: 创建飞书文档..."
    
    # 使用 feishu_doc 工具创建文档
    result=$(feishu_doc action=create title="$TEST_DOC_TITLE" owner_open_id="$USER_OPEN_ID" 2>&1) || true
    
    if echo "$result" | grep -q "error"; then
        log_error "创建失败：$result"
        return 1
    else
        log_success "创建成功"
        echo "$result"
        return 0
    fi
}

test_list_wiki_spaces() {
    log_info "测试 2: 列出知识库空间..."
    
    result=$(feishu_wiki action=spaces 2>&1) || true
    
    if echo "$result" | grep -q "error\|hint"; then
        log_warning "需要授权：$result"
        return 1
    else
        log_success "成功获取空间列表"
        echo "$result"
        return 0
    fi
}

test_drive_list() {
    log_info "测试 3: 列出云盘文件..."
    
    result=$(feishu_drive action=list 2>&1) || true
    
    if echo "$result" | grep -q "error"; then
        log_error "访问失败：$result"
        return 1
    else
        log_success "成功获取文件列表"
        echo "$result"
        return 0
    fi
}

check_permissions() {
    log_info "测试 4: 检查飞书应用权限..."
    
    result=$(feishu_app_scopes 2>&1)
    
    # 检查文档相关权限
    if echo "$result" | grep -q "docs:document"; then
        log_success "已有文档权限：docs:document"
    else
        log_warning "缺少文档权限"
    fi
    
    if echo "$result" | grep -q "docs:document:import"; then
        log_success "已有导入权限：docs:document:import"
    else
        log_warning "缺少导入权限"
    fi
    
    if echo "$result" | grep -q "docs:document.content:read"; then
        log_success "已有读取权限：docs:document.content:read"
    else
        log_warning "缺少读取权限"
    fi
    
    echo "$result"
}

show_instructions() {
    echo ""
    echo "=========================================="
    echo "📖 下一步操作"
    echo "=========================================="
    echo ""
    
    log_info "如果测试失败，请按照以下步骤配置："
    echo ""
    echo "1️⃣ 登录飞书开放平台"
    echo "   https://open.feishu.cn"
    echo ""
    echo "2️⃣ 进入企业自建应用"
    echo "   选择你的应用 → 权限管理"
    echo ""
    echo "3️⃣ 添加文档权限"
    echo "   - docs:document"
    echo "   - docs:document:write"
    echo "   - docs:document:create"
    echo ""
    echo "4️⃣ 发布应用并重新授权"
    echo ""
    echo "5️⃣ 重新运行测试"
    echo "   bash $0"
    echo ""
    
    log_info "详细配置指南："
    echo "   cat /home/admin/.openclaw/workspace/FEISHU-DOC-SETUP-GUIDE.md"
    echo ""
}

# ==================== 主程序 ====================

main() {
    echo "=========================================="
    echo "🧪 飞书文档功能测试"
    echo "=========================================="
    echo ""
    
    # 检查权限
    check_permissions
    echo ""
    
    # 测试各项功能
    test_passed=0
    test_failed=0
    
    if test_create_doc; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    echo ""
    
    if test_list_wiki_spaces; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    echo ""
    
    if test_drive_list; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    echo ""
    
    # 总结
    echo "=========================================="
    echo "📊 测试结果"
    echo "=========================================="
    echo ""
    log_info "通过：$test_passed"
    log_info "失败：$test_failed"
    echo ""
    
    if [ $test_failed -gt 0 ]; then
        show_instructions
    else
        log_success "所有测试通过！🎉"
    fi
}

main "$@"
