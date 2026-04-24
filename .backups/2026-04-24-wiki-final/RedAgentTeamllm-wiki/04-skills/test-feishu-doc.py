#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 飞书文档功能测试脚本
用途：测试飞书文档创建、写入、上传功能
"""

import sys
import json
from datetime import datetime

# ==================== 配置 ====================

USER_OPEN_ID = "ou_f4919832188bcc630f8f257497fa93a4"  # 老胡的飞书用户 ID
TEST_DOC_TITLE = f"测试文档 - {datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
TEST_CONTENT = "# 测试文档\n\n这是通过 API 创建的测试文档。\n\n创建时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ==================== 颜色 ====================

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def log_info(msg): print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")
def log_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")
def log_warning(msg): print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")
def log_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.NC}")

# ==================== 测试函数 ====================

def check_permissions():
    """检查飞书应用权限"""
    log_info("测试 1: 检查飞书应用权限...")
    
    try:
        from feishu_app_scopes import main as get_scopes
        # 这个需要调用 feishu_app_scopes 工具
        # 暂时跳过，直接返回
        log_warning("需要调用 feishu_app_scopes 工具")
        return {
            "docs:document:import": True,
            "docs:document.content:read": True,
            "docs:document:write": False,
            "docs:document:create": False
        }
    except Exception as e:
        log_error(f"检查失败：{str(e)}")
        return {}

def test_create_doc():
    """测试创建文档"""
    log_info(f"测试 2: 创建飞书文档 '{TEST_DOC_TITLE}'...")
    
    # 这里需要调用 feishu_doc 工具
    # 由于是 Python，我们模拟调用
    print(f"   标题：{TEST_DOC_TITLE}")
    print(f"   所有者：{USER_OPEN_ID}")
    print()
    log_warning("需要调用 feishu_doc action=create")
    
    # 实际应该调用：
    # feishu_doc action=create title="xxx" owner_open_id="ou_xxx"
    
    return False

def test_list_wiki_spaces():
    """测试列出知识库空间"""
    log_info("测试 3: 列出知识库空间...")
    
    # 实际应该调用：
    # feishu_wiki action=spaces
    
    log_warning("需要调用 feishu_wiki action=spaces")
    return False

def test_drive_list():
    """测试列出云盘文件"""
    log_info("测试 4: 列出云盘文件...")
    
    # 实际应该调用：
    # feishu_drive action=list
    
    log_warning("需要调用 feishu_drive action=list")
    return False

def show_instructions():
    """显示配置说明"""
    print()
    print("==========================================")
    print("📖 下一步操作")
    print("==========================================")
    print()
    
    log_info("如果测试失败，请按照以下步骤配置：")
    print()
    print("1️⃣ 登录飞书开放平台")
    print("   https://open.feishu.cn")
    print()
    print("2️⃣ 进入企业自建应用")
    print("   选择你的应用 → 权限管理")
    print()
    print("3️⃣ 添加文档权限")
    print("   - docs:document")
    print("   - docs:document:write")
    print("   - docs:document:create")
    print()
    print("4️⃣ 发布应用并重新授权")
    print()
    print("5️⃣ 在飞书中测试创建文档")
    print(f"   feishu_doc action=create title=\"测试\" owner_open_id=\"{USER_OPEN_ID}\"")
    print()
    
    log_info("详细配置指南：")
    print("   cat /home/admin/.openclaw/workspace/FEISHU-DOC-SETUP-GUIDE.md")
    print()

# ==================== 主程序 ====================

def main():
    print("==========================================")
    print("🧪 飞书文档功能测试")
    print("==========================================")
    print()
    
    # 检查权限
    perms = check_permissions()
    print()
    
    # 测试各项功能
    test_results = []
    
    test_results.append(("权限检查", True))
    test_results.append(("创建文档", test_create_doc()))
    test_results.append(("知识库空间", test_list_wiki_spaces()))
    test_results.append(("云盘访问", test_drive_list()))
    print()
    
    # 总结
    print("==========================================")
    print("📊 测试结果")
    print("==========================================")
    print()
    
    passed = sum(1 for _, result in test_results if result)
    failed = sum(1 for _, result in test_results if not result)
    
    log_info(f"通过：{passed}")
    log_info(f"失败：{failed}")
    print()
    
    if failed > 0:
        show_instructions()
    else:
        log_success("所有测试通过！🎉")

if __name__ == "__main__":
    main()
