#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 飞书邮件发送机器人
用途：通过飞书命令发送邮件（支持 Gmail 和腾讯企业邮）

使用方式：
  python3 send-email.py --to xxx@example.com --subject "主题" --content "内容"
"""

import smtplib
import argparse
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path

# ==================== 配置 ====================

# Gmail 配置
GMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "yesimagine@gmail.com",
    "password": "lqswobvyqzjkqfwu"  # 应用专用密码（去掉空格）
}

# 腾讯企业邮配置
TENCENT_CONFIG = {
    "smtp_server": "smtp.exmail.qq.com",
    "smtp_port": 465,
    "email": "red@unvw.com",
    "password": "6NWETmGDsE2RWfiC"  # 客户端授权码
}

# ==================== 发送函数 ====================

def send_email(to_email, subject, content, from_email=None, use_gmail=True):
    """
    发送邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        content: 邮件内容（支持 HTML）
        from_email: 发件人名称（可选）
        use_gmail: 是否使用 Gmail（默认 True，否则用腾讯企业邮）
    """
    
    # 选择配置
    config = GMAIL_CONFIG if use_gmail else TENCENT_CONFIG
    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    email = config["email"]
    password = config["password"]
    
    print(f"📧 准备发送邮件...")
    print(f"   发件人：{email}")
    print(f"   收件人：{to_email}")
    print(f"   主题：{subject}")
    print(f"   服务器：{smtp_server}:{smtp_port}")
    
    try:
        # 创建邮件
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{from_email or email} <{email}>"
        msg["To"] = to_email
        msg["Subject"] = Header(subject, "utf-8")
        
        # 添加内容（纯文本 + HTML）
        text_part = MIMEText(content, "plain", "utf-8")
        msg.attach(text_part)
        
        # 如果是 HTML 内容，也添加 HTML 版本
        if content.strip().startswith("<"):
            html_part = MIMEText(content, "html", "utf-8")
            msg.attach(html_part)
        
        # 连接服务器并发送
        print(f"\n🔌 连接 SMTP 服务器...")
        
        if smtp_port == 465:
            # SSL 连接（腾讯企业邮）
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        else:
            # TLS 连接（Gmail）
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.starttls()
        
        server.login(email, password)
        
        print(f"✅ 登录成功")
        print(f"📤 发送邮件...")
        
        server.send_message(msg)
        server.quit()
        
        print(f"\n✅ 邮件发送成功！")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(f"\n❌ 认证失败：邮箱账号或授权码错误")
        return False
    except smtplib.SMTPConnectError:
        print(f"\n❌ 连接失败：无法连接到 SMTP 服务器")
        print(f"   请检查网络连接或防火墙设置")
        return False
    except smtplib.SMTPException as e:
        print(f"\n❌ 发送失败：{str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ 未知错误：{str(e)}")
        return False

# ==================== 命令行接口 ====================

def main():
    parser = argparse.ArgumentParser(description="📧 飞书邮件发送机器人")
    
    parser.add_argument("--to", required=True, help="收件人邮箱")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--content", required=True, help="邮件内容")
    parser.add_argument("--from", dest="from_name", default=None, help="发件人名称（可选）")
    parser.add_argument("--use-gmail", action="store_true", default=True, help="使用 Gmail（默认）")
    parser.add_argument("--use-tencent", action="store_true", help="使用腾讯企业邮")
    
    args = parser.parse_args()
    
    # 选择邮件服务
    use_gmail = not args.use_tencent
    
    # 发送邮件
    success = send_email(
        to_email=args.to,
        subject=args.subject,
        content=args.content,
        from_email=args.from_name,
        use_gmail=use_gmail
    )
    
    # 返回状态码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
