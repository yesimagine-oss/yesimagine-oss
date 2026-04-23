#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 自动任务 Claim 脚本 v2（三层混合方案）

功能:
1. 优先使用 GEP-A2A API Claim 任务
2. API 失败时自动切换到浏览器模式
3. 飞书通知开始/成功/卡点/结束

使用:
    python3 auto-claim-task-v2.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from gep_a2a_client import GAPA2AClient
import logging

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "auto-claim-v2.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
CLAIM_LIMIT = 3  # 每次 Claim 3 个任务


def send_feishu_notification(title: str, content: str, status: str = "info"):
    """发送飞书通知"""
    emojis = {
        "success": "✅",
        "info": "📋",
        "warning": "⚠️",
        "error": "❌"
    }
    
    try:
        import subprocess
        message = f"{emojis.get(status, '📋')} {title}\n\n{content}"
        
        result = subprocess.Popen(
            ["python3", "/home/admin/.openclaw/workspace/tools/task-notifier.py",
             "start", title, message, "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate()
        
        if result.returncode == 0:
            logger.info("✅ 飞书通知发送成功")
        else:
            logger.error(f"❌ 飞书通知发送失败：{stderr}")
    
    except Exception as e:
        logger.error(f"❌ 飞书通知发送异常：{e}")


def claim_with_api(client: GAPA2AClient, limit: int = 3):
    """
    使用 API Claim 任务
    
    Returns:
        (success: bool, claimed_count: int)
    """
    logger.info("🔌 使用 API 模式 Claim 任务...")
    
    # 1. Hello 认证
    hello_result = client.hello()
    if not hello_result.get("success"):
        logger.error(f"Hello 失败：{hello_result.get('error')}")
        return False, 0
    
    logger.info(f"✅ Hello 成功：hub_node_id={client.hub_node_id}")
    
    # 2. Fetch 任务
    fetch_result = client.fetch_tasks(limit=limit)
    if not fetch_result.get("success") or fetch_result.get("count", 0) == 0:
        logger.warning("⚠️ 没有可用任务")
        return True, 0
    
    tasks = fetch_result.get("tasks", [])
    logger.info(f"✅ 获取到 {len(tasks)} 个任务")
    
    # 3. Claim 任务
    claimed_count = 0
    for task in tasks[:limit]:
        task_id = task.get("task_id") or task.get("id")
        if not task_id:
            continue
        
        claim_result = client.claim_task(task_id)
        if claim_result.get("success"):
            claimed_count += 1
            logger.info(f"✅ Claim 成功：{task_id}")
        else:
            logger.warning(f"⚠️ Claim 失败：{task_id} - {claim_result.get('error')}")
    
    return True, claimed_count


def claim_with_browser():
    """
    使用浏览器 Claim 任务（备用方案）
    
    Returns:
        (success: bool, claimed_count: int)
    """
    logger.info("🌐 使用浏览器模式 Claim 任务...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 访问任务页面
            page.goto("https://evomap.ai/bounties", wait_until="networkidle")
            
            # 获取任务卡片
            task_cards = page.query_selector_all('.task-card, [data-testid="task-card"]')
            
            if not task_cards:
                logger.warning("⚠️ 没有找到任务卡片")
                browser.close()
                return False, 0
            
            # Claim 前 3 个任务
            claimed_count = 0
            for i, card in enumerate(task_cards[:CLAIM_LIMIT]):
                try:
                    # 点击 Claim 按钮
                    claim_button = card.query_selector('button:has-text("Claim"), button:has-text("claim")')
                    if claim_button:
                        claim_button.click()
                        claimed_count += 1
                        logger.info(f"✅ Claim 成功：任务 {i+1}")
                except Exception as e:
                    logger.warning(f"⚠️ Claim 失败：{e}")
            
            browser.close()
            return True, claimed_count
    
    except ImportError:
        logger.error("❌ Playwright 未安装，无法使用浏览器模式")
        return False, 0
    except Exception as e:
        logger.error(f"❌ 浏览器模式失败：{e}")
        return False, 0


def auto_claim():
    """自动 Claim 主流程（三层混合模式）"""
    logger.info("🚀 开始自动 Claim 任务（三层混合模式）")
    
    # 1. 发送开始通知
    send_feishu_notification(
        "🎯 EvoMap 任务 Claim 开始",
        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"模式：API + 浏览器混合模式\n"
        f"目标：Claim {CLAIM_LIMIT} 个任务\n"
        f"节点：{NODE_ID}"
    )
    
    # 2. 创建 API 客户端
    client = GAPA2AClient(NODE_ID, NODE_SECRET)
    
    # 3. 优先使用 API
    success, claimed_count = claim_with_api(client, limit=CLAIM_LIMIT)
    
    if success and claimed_count > 0:
        # API 成功
        logger.info(f"✅ API 模式成功：Claim {claimed_count} 个任务")
        
        send_feishu_notification(
            "✅ 任务 Claim 成功",
            f"模式：API\n"
            f"成功：{claimed_count} 个任务\n"
            f"节点：{NODE_ID}"
        )
        
        return
    
    # 4. API 失败时使用浏览器
    logger.warning("⚠️ API 模式失败，切换到浏览器模式...")
    
    success, browser_claimed = claim_with_browser()
    
    if success and browser_claimed > 0:
        logger.info(f"✅ 浏览器模式成功：Claim {browser_claimed} 个任务")
        
        send_feishu_notification(
            "✅ 任务 Claim 成功（浏览器模式）",
            f"模式：浏览器自动化\n"
            f"成功：{browser_claimed} 个任务\n"
            f"节点：{NODE_ID}"
        )
        
        return
    
    # 5. 双模式均失败
    logger.error("❌ 双模式均失败")
    
    send_feishu_notification(
        "❌ 任务 Claim 失败",
        f"模式：API + 浏览器\n"
        f"API 结果：{'成功' if success else '失败'}\n"
        f"浏览器结果：{'成功' if browser_claimed else '失败'}\n"
        f"请手动检查或联系管理员",
        "error"
    )


if __name__ == "__main__":
    auto_claim()
