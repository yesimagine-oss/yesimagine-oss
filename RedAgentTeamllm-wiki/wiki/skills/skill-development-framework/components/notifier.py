#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notifier 组件 - 消息通知器

支持飞书消息、邮件、Webhook 通知
"""

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Notifier:
    """消息通知器"""
    
    # 通知渠道
    CHANNELS = ["feishu", "email", "webhook"]
    
    @staticmethod
    def send_success(category: str, title: str, doc_url: str, channel: str = "feishu"):
        """
        发送成功通知
        
        Args:
            category: 分类
            title: 标题
            doc_url: 文档 URL
            channel: 通知渠道
        """
        logger.info(f"Sending success notification via {channel}")
        
        message = Notifier._build_success_message(category, title, doc_url)
        
        if channel == "feishu":
            Notifier._send_feishu_message(message)
        elif channel == "email":
            Notifier._send_email("收录完成", message)
        elif channel == "webhook":
            Notifier._send_webhook("success", {"category": category, "title": title, "url": doc_url})
        else:
            logger.error(f"Unknown channel: {channel}")
    
    @staticmethod
    def send_failure(error_message: str, channel: str = "feishu"):
        """
        发送失败通知
        
        Args:
            error_message: 错误信息
            channel: 通知渠道
        """
        logger.info(f"Sending failure notification via {channel}")
        
        message = Notifier._build_failure_message(error_message)
        
        if channel == "feishu":
            Notifier._send_feishu_message(message)
        elif channel == "email":
            Notifier._send_email("收录失败", message)
        elif channel == "webhook":
            Notifier._send_webhook("failure", {"error": error_message})
        else:
            logger.error(f"Unknown channel: {channel}")
    
    @staticmethod
    def send_custom_message(msg_type: str, content: Dict, channel: str = "feishu"):
        """
        发送自定义通知
        
        Args:
            msg_type: 消息类型
            content: 消息内容
            channel: 通知渠道
        """
        logger.info(f"Sending custom message via {channel}")
        
        if channel == "feishu":
            Notifier._send_feishu_message(content, msg_type)
        elif channel == "email":
            Notifier._send_email(msg_type, content)
        elif channel == "webhook":
            Notifier._send_webhook(msg_type, content)
        else:
            logger.error(f"Unknown channel: {channel}")
    
    @staticmethod
    def _build_success_message(category: str, title: str, doc_url: str) -> str:
        """构建成功消息"""
        return f"""✅ 收录完成

📄 {category} {title}

💡 文档亮点：
• 完整内容收录
• 自动分类整理
• 图片自动处理

🔗 查看飞书文档 → {doc_url}
"""
    
    @staticmethod
    def _build_failure_message(error_message: str) -> str:
        """构建失败消息"""
        return f"""❌ 收录失败

⚠️ 错误信息：
{error_message}

请检查：
• 链接是否有效
• 网络是否正常
• 权限是否充足
"""
    
    @staticmethod
    def _send_feishu_message(content: str, msg_type: str = "text"):
        """发送飞书消息"""
        logger.debug(f"Sending Feishu message: {content[:100]}...")
        
        # 这里需要飞书消息 API 集成
        # 示例代码：
        # token = get_feishu_token()
        # send_message(token, content, msg_type)
        
        logger.warning("Feishu API not configured, message skipped")
    
    @staticmethod
    def _send_email(subject: str, content: str):
        """发送邮件"""
        logger.debug(f"Sending email: {subject}")
        
        # 这里需要邮件 API 集成
        # 示例代码：
        # send_email(subject, content)
        
        logger.warning("Email API not configured, email skipped")
    
    @staticmethod
    def _send_webhook(event_type: str, data: Dict):
        """发送 Webhook"""
        logger.debug(f"Sending webhook: {event_type}")
        
        # 这里需要 Webhook API 集成
        # 示例代码：
        # requests.post(webhook_url, json={"type": event_type, "data": data})
        
        logger.warning("Webhook not configured, webhook skipped")


# 测试代码
if __name__ == "__main__":
    # 测试示例
    print("Testing Notifier:")
    
    # 测试成功通知
    Notifier.send_success(
        category="📖 技术教程",
        title="Python 安装指南",
        doc_url="https://example.feishu.cn/docx/xxx"
    )
    print("Success notification sent")
    
    # 测试失败通知
    Notifier.send_failure("链接无效")
    print("Failure notification sent")
