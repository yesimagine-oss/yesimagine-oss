#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 飞书邮件通知脚本
用途：邮件发送成功/失败后，通过飞书通知用户
"""

import sys
import json
import os
from datetime import datetime

# ==================== 配置 ====================

# 飞书机器人 Webhook URL（需要从飞书开放平台获取）
# 格式：https://open.feishu.cn/open-apis/bot/v2/hook/xxx
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

# 或者使用飞书应用方式
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

# ==================== 通知函数 ====================

def send_feishu_notification(status, to_email, subject, content="", error_msg="", from_email="yesimagine@gmail.com"):
    """
    发送飞书通知
    
    Args:
        status: "success" 或 "failed"
        to_email: 收件人邮箱
        subject: 邮件主题
        content: 邮件内容预览（可选）
        error_msg: 错误信息（失败时）
        from_email: 发件人邮箱
    """
    
    # 生成通知内容
    if status == "success":
        message = build_success_message(from_email, to_email, subject, content)
    else:
        message = build_failed_message(from_email, to_email, subject, error_msg)
    
    # 打印消息（用于测试）
    print("📱 飞书通知内容：")
    print(json.dumps(message, ensure_ascii=False, indent=2))
    print()
    
    # 如果有 Webhook，发送飞书消息
    if FEISHU_WEBHOOK:
        return send_via_webhook(FEISHU_WEBHOOK, message)
    elif FEISHU_APP_ID and FEISHU_APP_SECRET:
        return send_via_app(message)
    else:
        print("⚠️  未配置飞书 Webhook 或应用，跳过发送")
        print("💡 提示：设置 FEISHU_WEBHOOK 环境变量")
        return True

def build_success_message(from_email, to_email, subject, content=""):
    """构建成功通知消息"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 内容预览（最多 100 字符）
    preview = content[:100] + "..." if len(content) > 100 else content
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "✅ 邮件发送成功"
                },
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**发件人**:\n{from_email}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**收件人**:\n{to_email}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**主题**:\n{subject}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**发送时间**:\n{now}"
                            }
                        }
                    ]
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**邮件内容预览**:\n{preview}"
                    }
                }
            ]
        }
    }
    
    return message

def build_failed_message(from_email, to_email, subject, error_msg=""):
    """构建失败通知消息"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 错误原因分析
    error_analysis = analyze_error(error_msg)
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "❌ 邮件发送失败"
                },
                "template": "red"
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**发件人**:\n{from_email}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**收件人**:\n{to_email}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**主题**:\n{subject}"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**发送时间**:\n{now}"
                            }
                        }
                    ]
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**失败原因**:\n{error_analysis['reason']}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**解决方案**:\n{error_analysis['solution']}"
                    }
                }
            ]
        }
    }
    
    return message

def analyze_error(error_msg):
    """分析错误信息，提供解决方案"""
    
    error_lower = error_msg.lower()
    
    if "authentication" in error_lower or "认证" in error_lower:
        return {
            "reason": "认证失败：邮箱账号或授权码错误",
            "solution": "1. 检查 Gmail 授权码是否正确\n2. 重新生成应用专用密码\n3. 联系管理员更新配置"
        }
    elif "connection" in error_lower or "连接" in error_lower:
        return {
            "reason": "连接失败：无法连接到 SMTP 服务器",
            "solution": "1. 检查服务器网络连接\n2. 检查防火墙设置\n3. 稍后重试"
        }
    elif "timeout" in error_lower or "超时" in error_lower:
        return {
            "reason": "连接超时：SMTP 服务器响应超时",
            "solution": "1. 检查网络连接\n2. 检查 SMTP 服务器状态\n3. 稍后重试"
        }
    elif "recipient" in error_lower or "收件人" in error_lower:
        return {
            "reason": "收件人无效：邮箱地址格式错误",
            "solution": "1. 检查邮箱地址格式\n2. 确认收件人邮箱正确"
        }
    else:
        return {
            "reason": error_msg if error_msg else "未知错误",
            "solution": "1. 检查错误日志\n2. 联系技术支持\n3. 稍后重试"
        }

def send_via_webhook(webhook_url, message):
    """通过 Webhook 发送飞书消息"""
    
    try:
        import requests
        
        response = requests.post(
            webhook_url,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print("✅ 飞书通知发送成功")
                return True
            else:
                print(f"❌ 飞书通知发送失败：{result}")
                return False
        else:
            print(f"❌ 飞书 API 返回错误：{response.status_code}")
            print(response.text)
            return False
            
    except ImportError:
        print("❌ 缺少 requests 库，请安装：pip install requests")
        return False
    except Exception as e:
        print(f"❌ 发送飞书通知失败：{str(e)}")
        return False

def send_via_app(message):
    """通过飞书应用发送消息（需要 access_token）"""
    
    # 这个需要实现 OAuth 流程，暂时跳过
    print("⚠️  飞书应用方式暂未实现，请使用 Webhook")
    return False

# ==================== 命令行接口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="📧 飞书邮件通知脚本")
    parser.add_argument("--status", required=True, choices=["success", "failed"], help="发送状态")
    parser.add_argument("--to", required=True, help="收件人邮箱")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--content", default="", help="邮件内容（成功时）")
    parser.add_argument("--error", default="", help="错误信息（失败时）")
    parser.add_argument("--from", dest="from_email", default="yesimagine@gmail.com", help="发件人邮箱")
    
    args = parser.parse_args()
    
    # 发送通知
    success = send_feishu_notification(
        status=args.status,
        to_email=args.to,
        subject=args.subject,
        content=args.content,
        error_msg=args.error,
        from_email=args.from_email
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
