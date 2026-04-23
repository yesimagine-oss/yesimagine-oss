#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 心跳监控优化脚本
单进程长运行模式，替代每 5 分钟启动新进程
"""

import requests
import time
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
EVO_API = "https://evomap.ai"
INTERVAL = 300  # 5 分钟

# 日志配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "node-heartbeat-daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 运行标志
running = True

def signal_handler(sig, frame):
    """信号处理"""
    global running
    logger.info("🛑 收到终止信号，准备退出...")
    running = False

def send_heartbeat():
    """发送心跳"""
    try:
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "hello",
            "sender_id": NODE_ID,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "payload": {"status": "online"}
        }
        
        response = requests.post(
            f"{EVO_API}/a2a/heartbeat",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {NODE_SECRET}"
            },
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("✅ 心跳发送成功")
            return True
        else:
            logger.error(f"❌ 心跳失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 心跳异常：{e}")
        return False

def check_node_status():
    """检查节点状态"""
    try:
        response = requests.get(
            f"{EVO_API}/a2a/nodes/{NODE_ID}",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            logger.info(f"📊 节点状态：{status}")
            return status
        else:
            logger.error(f"❌ 获取状态失败：{response.status_code}")
            return 'error'
            
    except Exception as e:
        logger.error(f"❌ 获取状态异常：{e}")
        return 'error'

def main():
    """主函数"""
    global running
    
    # 注册信号处理
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("🚀 EvoMap 心跳监控守护进程启动")
    logger.info(f"⏱️  心跳间隔：{INTERVAL}秒")
    logger.info(f"🆔 节点 ID: {NODE_ID}")
    
    iteration = 0
    while running:
        iteration += 1
        start_time = datetime.now()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 第 {iteration} 次心跳检查")
        logger.info(f"🕐 时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 发送心跳
        heartbeat_success = send_heartbeat()
        
        # 检查状态
        node_status = check_node_status()
        
        # 记录统计
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"⏱️  本次耗时：{elapsed:.2f}秒")
        
        # 等待下次执行
        if running:
            sleep_time = max(0, INTERVAL - elapsed)
            logger.info(f"😴 等待 {sleep_time:.0f}秒...")
            time.sleep(sleep_time)
    
    logger.info("✅ 守护进程已退出")

if __name__ == "__main__":
    main()
