#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 节点心跳监控脚本
功能：
1. 每 5 分钟检查节点在线状态
2. 离线时自动发送心跳恢复
3. 发送告警通知到飞书
4. 记录监控日志
"""

import requests
import json
import time
import logging
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
EVO_API = "https://evomap.ai"
CHECK_INTERVAL = 300  # 5 分钟
MAX_OFFLINE_TIME = 1200  # 20 分钟离线阈值

# 日志配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "node-monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_node_status():
    """检查节点在线状态"""
    try:
        response = requests.get(
            f"{EVO_API}/api/node/{NODE_ID}/status",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "online": data.get("node_status") == "active",
                "last_heartbeat": data.get("last_heartbeat"),
                "data": data
            }
        else:
            logger.error(f"检查状态失败：{response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"检查状态异常：{e}")
        return None


def send_heartbeat():
    """发送心跳恢复在线"""
    try:
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "hello",
            "sender_id": NODE_ID,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "payload": {
                "status": "online",
                "recovery": True
            }
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
            logger.info("✅ 心跳发送成功，节点已恢复在线")
            return True
        else:
            logger.error(f"❌ 心跳发送失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 心跳发送异常：{e}")
        return False


def send_feishu_alert(message):
    """发送飞书告警 - 已禁用（用户明确不需要）"""
    # 已禁用：用户明确禁止心跳报告
    logger.warning(f"飞书告警已禁用：{message}")
    return  # 不发送
    webhook_url = ""  # 从环境变量或配置文件读取
    
    if not webhook_url:
        logger.warning("飞书 webhook 未配置，跳过告警")
        return
    
    try:
        payload = {
            "msg_type": "text",
            "content": {
                "text": f"🚨 EvoMap 节点告警\n\n{message}"
            }
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ 飞书告警发送成功")
        else:
            logger.error(f"❌ 飞书告警发送失败：{response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ 飞书告警发送异常：{e}")


def monitor_loop():
    """主监控循环"""
    logger.info("🚀 EvoMap 节点监控启动")
    logger.info(f"监控节点：{NODE_ID}")
    logger.info(f"检查间隔：{CHECK_INTERVAL}秒")
    logger.info(f"离线阈值：{MAX_OFFLINE_TIME}秒")
    
    offline_start_time = None
    
    while True:
        try:
            # 检查节点状态
            status = check_node_status()
            
            if status is None:
                logger.warning("⚠️ 无法检查节点状态，网络可能有问题")
                time.sleep(CHECK_INTERVAL)
                continue
            
            if status["online"]:
                # 节点在线
                if offline_start_time:
                    # 之前离线，现在恢复了
                    offline_duration = time.time() - offline_start_time
                    logger.info(f"✅ 节点已恢复在线，离线时长：{offline_duration:.0f}秒")
                    send_feishu_alert(f"节点已恢复在线\n离线时长：{offline_duration:.0f}秒")
                    offline_start_time = None
                
                logger.info(f"✅ 节点在线 | 最后心跳：{status['last_heartbeat']}")
            else:
                # 节点离线
                if offline_start_time is None:
                    offline_start_time = time.time()
                    logger.warning("⚠️ 节点离线！开始计时")
                    send_feishu_alert("⚠️ 节点离线！\n节点 ID: " + NODE_ID)
                
                offline_duration = time.time() - offline_start_time
                
                if offline_duration > MAX_OFFLINE_TIME:
                    # 超过阈值，自动恢复
                    logger.warning(f"⚠️ 节点已离线{offline_duration:.0f}秒，超过阈值{MAX_OFFLINE_TIME}秒")
                    logger.info("🔄 尝试自动恢复...")
                    
                    if send_heartbeat():
                        logger.info("✅ 自动恢复成功")
                        send_feishu_alert(f"✅ 节点已自动恢复\n离线时长：{offline_duration:.0f}秒")
                        offline_start_time = None
                    else:
                        logger.error("❌ 自动恢复失败")
                        send_feishu_alert(f"❌ 自动恢复失败\n请手动处理！")
                else:
                    logger.warning(f"⚠️ 节点离线中 | 已离线：{offline_duration:.0f}秒")
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("👋 监控脚本停止")
            break
        except Exception as e:
            logger.error(f"❌ 监控循环异常：{e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_loop()
