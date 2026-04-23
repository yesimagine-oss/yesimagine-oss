#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气预报格式对比测试 - 三种格式独立展示
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# ============================================================================
# 天气数据获取（简化）
# ============================================================================

def get_weather_data(city_name: str) -> dict:
    """获取天气数据"""
    city_coords = {
        '济南': {'lat': 36.6512, 'lon': 117.1209},
        '威海': {'lat': 37.5128, 'lon': 122.1209},
    }
    
    coords = city_coords.get(city_name)
    if not coords:
        return None
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': coords['lat'],
        'longitude': coords['lon'],
        'current_weather': True,
        'daily': 'temperature_2m_max,temperature_2m_min,weathercode,uv_index_max',
        'hourly': 'temperature_2m,relative_humidity_2m',
        'timezone': 'Asia/Shanghai'
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    current = data.get('current_weather', {})
    hourly = data.get('hourly', {})
    current_hour = datetime.now().hour
    
    daily = data.get('daily', {})
    
    return {
        'city': city_name,
        'current_temp': current.get('temperature', '--'),
        'weather': '晴朗',
        'wind': f"{current.get('winddirection', '--')}° {current.get('windspeed', '--')}km/h",
        'humidity': hourly.get('relative_humidity_2m', ['--'])[current_hour],
        'temp_max': daily.get('temperature_2m_max', ['--'])[0],
        'temp_min': daily.get('temperature_2m_min', ['--'])[0],
        'uv': daily.get('uv_index_max', ['--'])[0],
    }

# ============================================================================
# 格式 1: 纯文本消息
# ============================================================================

def create_plain_text():
    """
    纯文本格式 - 优势：简洁、加载快、兼容性好
    适合：快速阅读、低带宽环境
    """
    now = datetime.now()
    
    text = f"""【天气预报】{now.strftime('%Y-%m-%d')}

济南：{get_weather_data('济南')['current_temp']}°C 晴 13~24°
威海：{get_weather_data('威海')['current_temp']}°C 多云 7~14°

紫外线：中等
建议：防晒、多喝水

详情：https://weather.com"""
    
    return {
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False)
    }

# ============================================================================
# 格式 2: 富文本消息（Post）
# ============================================================================

def create_post_message():
    """
    富文本格式 - 优势：多段落、支持@提及、支持链接和图片
    适合：详细报告、需要@特定用户
    """
    now = datetime.now()
    jinan = get_weather_data('济南')
    weihai = get_weather_data('威海')
    
    # 富文本内容（多段落）
    content = {
        "zh_cn": {
            "title": "📅 每日天气预报",
            "content": [
                [{"tag": "text", "text": f"日期：{now.strftime('%Y年%m月%d日 %A')}\n"}],
                [{"tag": "text", "text": "\n"}],
                
                # 济南
                [{"tag": "text", "text": "📍 济南\n"}],
                [{"tag": "text", "text": f"🌡️ 当前：{jinan['current_temp']}°C | {jinan['weather']}\n"}],
                [{"tag": "text", "text": f"💨 风力：{jinan['wind']}\n"}],
                [{"tag": "text", "text": f"💧 湿度：{jinan['humidity']}%\n"}],
                [{"tag": "text", "text": f"📊 今日：{jinan['temp_min']}~{jinan['temp_max']}°C\n"}],
                [{"tag": "text", "text": f"☀️ 紫外线：{jinan['uv']}（高）\n"}],
                [{"tag": "text", "text": "\n"}],
                
                [{"tag": "text", "text": "━━━━━━━━━━━━━━━━━━\n"}],
                [{"tag": "text", "text": "\n"}],
                
                # 威海
                [{"tag": "text", "text": "📍 威海\n"}],
                [{"tag": "text", "text": f"🌡️ 当前：{weihai['current_temp']}°C | {weihai['weather']}\n"}],
                [{"tag": "text", "text": f"💨 风力：{weihai['wind']}\n"}],
                [{"tag": "text", "text": f"💧 湿度：{weihai['humidity']}%\n"}],
                [{"tag": "text", "text": f"📊 今日：{weihai['temp_min']}~{weihai['temp_max']}°C\n"}],
                [{"tag": "text", "text": f"☀️ 紫外线：{weihai['uv']}（高）\n"}],
                [{"tag": "text", "text": "\n"}],
                
                [{"tag": "text", "text": "━━━━━━━━━━━━━━━━━━\n"}],
                [{"tag": "text", "text": "\n"}],
                
                # 生活建议
                [{"tag": "text", "text": "💡 生活建议:\n"}],
                [{"tag": "text", "text": "• 紫外线强，外出注意防晒\n"}],
                [{"tag": "text", "text": "• 昼夜温差大，早晚添衣\n"}],
                [{"tag": "text", "text": "• 沿海城市注意海风\n"}],
                [{"tag": "text", "text": "\n"}],
                
                [{"tag": "text", "text": "🤖 自动播报 | 每日 8:00 更新\n"}],
            ]
        }
    }
    
    return {
        "msg_type": "post",
        "content": json.dumps(content, ensure_ascii=False)
    }

# ============================================================================
# 格式 3: 卡片消息（Interactive Card）
# ============================================================================

def create_interactive_card():
    """
    卡片消息格式 - 优势：结构化、美观、可交互、支持按钮
    适合：专业报告、需要用户操作、品牌形象
    """
    now = datetime.now()
    jinan = get_weather_data('济南')
    weihai = get_weather_data('威海')
    
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "📅 每日天气预报"
            }
        },
        "elements": [
            # 日期信息
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**日期**: {now.strftime('%Y年%m月%d日 %A')}"
                }
            },
            {
                "tag": "hr"
            },
            
            # 济南天气
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📍 济南**\n当前温度：**{jinan['current_temp']}°C** | {jinan['weather']}\n风力：{jinan['wind']} | 湿度：{jinan['humidity']}%\n今日：{jinan['temp_min']}~{jinan['temp_max']}°C | 紫外线：{jinan['uv']}"
                }
            },
            {
                "tag": "hr"
            },
            
            # 威海天气
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📍 威海**\n当前温度：**{weihai['current_temp']}°C** | {weihai['weather']}\n风力：{weihai['wind']} | 湿度：{weihai['humidity']}%\n今日：{weihai['temp_min']}~{weihai['temp_max']}°C | 紫外线：{weihai['uv']}"
                }
            },
            {
                "tag": "hr"
            },
            
            # 生活建议
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**💡 生活建议**\n• 紫外线强，注意防晒\n• 温差大，早晚添衣\n• 多喝水，保持水分"
                }
            },
            
            # 按钮组
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📊 查看详细"
                        },
                        "url": "https://weather.com",
                        "type": "default"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "🔄 刷新"
                        },
                        "type": "primary"
                    }
                ]
            },
            
            # 底部
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "🤖 自动播报 | 每日 8:00 更新"
                    }
                ]
            }
        ]
    }
    
    return {
        "msg_type": "interactive",
        "card": card
    }

# ============================================================================
# 发送消息
# ============================================================================

def get_feishu_token(app_id: str, app_secret: str) -> str:
    """获取飞书 Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    result = response.json()
    return result.get('tenant_access_token')


def send_message(token: str, chat_id: str, message: dict, msg_type: str) -> bool:
    """发送消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "receive_id": chat_id,
        "msg_type": msg_type,
        "content": message.get("content") or json.dumps(message.get("card", {}), ensure_ascii=False)
    }
    
    params = {'receive_id_type': 'chat_id'}
    
    response = requests.post(url, headers=headers, params=params, json=payload, timeout=10)
    result = response.json()
    
    if result.get('code') != 0:
        log(f"❌ 发送失败：{result.get('msg')}")
        return False
    
    log(f"✅ {msg_type} 消息已发送")
    return True

# ============================================================================
# 主函数
# ============================================================================

def main():
    """发送三种格式的消息"""
    log("=" * 50)
    log("📊 天气预报格式对比测试")
    
    FEISHU_APP_ID = "cli_a929676f8bf81cc7"
    FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
    GROUP_CHAT_ID = "oc_55a027a0be1c6252a89177256f2210b9"
    
    # 获取 Token
    token = get_feishu_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    if not token:
        log("❌ Token 获取失败")
        return
    
    log(f"\n准备发送到群组：{GROUP_CHAT_ID}\n")
    
    # 格式 1: 纯文本
    log("1️⃣ 发送【纯文本消息】...")
    plain_msg = create_plain_text()
    send_message(token, GROUP_CHAT_ID, plain_msg, "text")
    
    # 等待一下
    import time
    time.sleep(1)
    
    # 格式 2: 富文本
    log("2️⃣ 发送【富文本消息（Post）】...")
    post_msg = create_post_message()
    send_message(token, GROUP_CHAT_ID, post_msg, "post")
    
    time.sleep(1)
    
    # 格式 3: 卡片
    log("3️⃣ 发送【卡片消息（Interactive）】...")
    card_msg = create_interactive_card()
    send_message(token, GROUP_CHAT_ID, card_msg, "interactive")
    
    log("\n✅ 三种格式已发送，请在飞书群组查看效果！")
    log("\n📋 格式对比:")
    log("  纯文本 - 简洁、快速")
    log("  富文本 - 多段落、@提及")
    log("  卡片 - 美观、可交互")

if __name__ == "__main__":
    main()
