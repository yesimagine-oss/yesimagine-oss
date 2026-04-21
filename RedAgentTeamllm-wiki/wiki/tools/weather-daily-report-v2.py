#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日天气预报 v2 - 混合格式版
结合纯文本、富文本、卡片消息的优势
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 日志配置
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "weather-daily-v2.log"

def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ============================================================================
# 农历和节气（简化实现）
# ============================================================================

def get_lunar_date(date: datetime) -> str:
    """获取农历日期和节气（简化版）"""
    try:
        # 2026 年春节是 2 月 17 日
        spring_festival = datetime(2026, 2, 17)
        
        if date < spring_festival:
            year_name = "乙巳年"
            lunar_month = 12 + date.month - 1
            if lunar_month > 12:
                lunar_month -= 12
        else:
            year_name = "丙午年"
            days_since_spring = (date - spring_festival).days
            lunar_month = 1 + days_since_spring // 30
            if lunar_month > 12:
                lunar_month = 12
        
        days_since_spring = (date - spring_festival).days
        lunar_day = 1 + days_since_spring % 30
        
        month_names = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
        month_name = month_names[lunar_month - 1] if 1 <= lunar_month <= 12 else '腊'
        
        day_names = ['', '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                     '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                     '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
        day_name = day_names[lunar_day] if 1 <= lunar_day <= 30 else f"初{lunar_day}"
        
        lunar_str = f"{year_name} {month_name}月{day_name}"
        
        # 检查节气
        solar_term = get_solar_term(date)
        if solar_term:
            return f"{lunar_str} {solar_term}"
        return lunar_str
    
    except Exception as e:
        log(f"⚠️ 农历计算失败：{e}")
        return ""


def get_solar_term(date: datetime) -> str:
    """获取 24 节气（2026 年）"""
    solar_terms_2026 = [
        (1, 5, '小寒'), (1, 20, '大寒'),
        (2, 3, '立春'), (2, 18, '雨水'),
        (3, 5, '惊蛰'), (3, 20, '春分'),
        (4, 4, '清明'), (4, 19, '谷雨'),
        (5, 5, '立夏'), (5, 20, '小满'),
        (6, 5, '芒种'), (6, 21, '夏至'),
        (7, 7, '小暑'), (7, 22, '大暑'),
        (8, 7, '立秋'), (8, 22, '处暑'),
        (9, 7, '白露'), (9, 22, '秋分'),
        (10, 8, '寒露'), (10, 23, '霜降'),
        (11, 7, '立冬'), (11, 22, '小雪'),
        (12, 7, '大雪'), (12, 21, '冬至'),
    ]
    
    month, day = date.month, date.day
    for term_month, term_day, term_name in solar_terms_2026:
        if month == term_month and abs(day - term_day) <= 1:
            return term_name
    
    return ""

# ============================================================================
# 天气数据获取
# ============================================================================

def get_weather(city_name: str) -> dict:
    """获取城市天气预报（Open-Meteo）"""
    try:
        city_coords = {
            '济南': {'lat': 36.6512, 'lon': 117.1209},
            '威海': {'lat': 37.5128, 'lon': 122.1209},
        }
        
        if city_name not in city_coords:
            log(f"⚠️ 未知城市：{city_name}")
            return None
        
        coords = city_coords[city_name]
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': coords['lat'],
            'longitude': coords['lon'],
            'current_weather': True,
            'daily': 'temperature_2m_max,temperature_2m_min,weathercode,uv_index_max',
            'hourly': 'temperature_2m,relative_humidity_2m,weathercode,uv_index',
            'timezone': 'Asia/Shanghai'
        }
        
        headers = {"User-Agent": "weather-bot/2.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            log(f"⚠️ 获取 {city_name} 天气失败：HTTP {response.status_code}")
            return None
        
        data = response.json()
        
        current = data.get('current_weather', {})
        hourly = data.get('hourly', {})
        current_hour = datetime.now().hour
        temp_list = hourly.get('temperature_2m', [])
        humidity_list = hourly.get('relative_humidity_2m', [])
        weather_code_list = hourly.get('weathercode', [])
        
        time_periods = {
            '清晨': (5, 7),
            '上午': (8, 11),
            '中午': (12, 13),
            '下午': (14, 17),
            '傍晚': (18, 19),
            '晚上': (20, 23),
        }
        
        period_temps = {}
        for period_name, (start_hour, end_hour) in time_periods.items():
            temps = [temp_list[h] for h in range(start_hour, end_hour + 1) if h < len(temp_list)]
            period_temps[period_name] = round(sum(temps) / len(temps), 1) if temps else '--'
        
        current_humidity = humidity_list[current_hour] if current_hour < len(humidity_list) else '--'
        current_weather_code = weather_code_list[current_hour] if current_hour < len(weather_code_list) else 3
        
        daily = data.get('daily', {})
        today_max = daily.get('temperature_2m_max', ['--'])[0]
        today_min = daily.get('temperature_2m_min', ['--'])[0]
        weather_code = daily.get('weathercode', [0])[0]
        uv_index = daily.get('uv_index_max', ['--'])[0]
        
        weather_codes = {
            0: '晴朗', 1: '主要晴朗', 2: '多云', 3: '阴天',
            45: '雾', 48: '雾凇',
            51: '毛毛雨', 53: '毛毛雨', 55: '毛毛雨',
            61: '小雨', 63: '中雨', 65: '大雨',
            71: '小雪', 73: '中雪', 75: '大雪',
            95: '雷暴', 96: '雷暴伴冰雹', 99: '强雷暴伴冰雹'
        }
        weather_desc = weather_codes.get(current_weather_code, '未知')
        
        return {
            'city': city_name,
            'current': {
                'temp_C': current.get('temperature', '--'),
                'weatherDesc': weather_desc,
                'humidity': current_humidity,
                'windspeedKmph': current.get('windspeed', '--'),
                'winddir16Point': f"{current.get('winddirection', '--')}°",
            },
            'today': {
                'maxTempC': today_max,
                'minTempC': today_min,
                'avgWeatherDesc': weather_codes.get(weather_code, '未知'),
                'uvIndex': uv_index,
                'period_temps': period_temps,
            },
            'tomorrow': None
        }
    
    except Exception as e:
        log(f"❌ 获取 {city_name} 天气异常：{e}")
        return None

# ============================================================================
# 构建混合格式报告
# ============================================================================

def build_hybrid_report(weather_data_list: list) -> dict:
    """
    构建混合格式报告
    
    设计理念:
    - 卡片消息：头部标题（美观、醒目）
    - 富文本：天气详情（多段落、结构化）
    - 纯文本：生活建议（简洁、易读）
    
    Returns:
        包含多种格式的消息字典
    """
    now = datetime.now()
    today = now.strftime("%Y年%m月%d日 %A")
    lunar_info = get_lunar_date(now)
    
    # 天气图标映射
    weather_icons = {
        '晴朗': '☀️', '主要晴朗': '☀️', '多云': '⛅',
        '阴天': '☁️', '雾': '🌫️', '小雨': '🌧️', '中雨': '🌧️', '大雨': '🌧️',
        '小雪': '❄️', '中雪': '❄️', '大雪': '❄️', '雷暴': '⛈️'
    }
    
    # 紫外线等级
    def get_uv_level(uv):
        try:
            uv_val = float(uv)
            if uv_val <= 2: return '低', '🟢'
            elif uv_val <= 5: return '中等', '🟡'
            elif uv_val <= 7: return '高', '🟠'
            elif uv_val <= 10: return '很高', '🔴'
            else: return '极高', '🟣'
        except:
            return '', ''
    
    # 构建每个城市的天气内容
    city_contents = []
    
    for weather in weather_data_list:
        if not weather:
            continue
        
        city = weather['city']
        current = weather['current']
        today_fc = weather['today']
        
        # 天气图标
        icon = '🌡️'
        for key, value in weather_icons.items():
            if key in today_fc['avgWeatherDesc']:
                icon = value
                break
        
        # 湿度显示
        humidity = current.get('humidity', '--')
        humidity_display = f"{humidity}%" if humidity != '--' else '--'
        
        # 紫外线等级
        uv_level, uv_emoji = get_uv_level(today_fc.get('uvIndex', '--'))
        uv_display = f"{today_fc['uvIndex']}（{uv_level}）" if today_fc['uvIndex'] != '--' else '--'
        
        # 时间段温度
        period_temps = today_fc.get('period_temps', {})
        temp_lines = []
        for period in ['清晨', '上午', '中午', '下午', '傍晚', '晚上']:
            temp = period_temps.get(period, '--')
            if temp != '--':
                temp_lines.append(f"{period}{temp}°C")
        
        # 生活建议
        suggestions = []
        try:
            max_temp = float(today_fc['maxTempC'])
            min_temp = float(today_fc['minTempC'])
            avg_temp = (max_temp + min_temp) / 2
            
            if avg_temp < 10:
                suggestions.append("🧥 天气较冷，注意保暖")
            elif avg_temp < 20:
                suggestions.append("👕 温度适宜，可穿长袖")
            elif avg_temp < 28:
                suggestions.append("👕 天气温暖，短袖即可")
            else:
                suggestions.append("🩳 天气炎热，注意防暑")
            
            if max_temp - min_temp > 10:
                suggestions.append("🌡️ 昼夜温差大，早晚添衣")
        except:
            pass
        
        try:
            uv_val = float(today_fc.get('uvIndex', 0))
            if uv_val >= 8:
                suggestions.append("☀️ 紫外线很强，尽量避免外出")
            elif uv_val >= 6:
                suggestions.append("☀️ 紫外线强，外出注意防晒")
            elif uv_val >= 3:
                suggestions.append("☀️ 紫外线中等，适当防护")
        except:
            pass
        
        weather_desc = today_fc['avgWeatherDesc']
        if '雨' in weather_desc:
            suggestions.append("☔ 有雨，出门带伞")
        if '雪' in weather_desc:
            suggestions.append("❄️ 有雪，注意路滑")
        
        try:
            wind_speed = float(current.get('windspeedKmph', 0))
            if wind_speed > 40:
                suggestions.append("💨 大风，减少外出")
            elif wind_speed > 25:
                suggestions.append("💨 风力较大，注意防风")
        except:
            pass
        
        try:
            humidity_val = float(current.get('humidity', 50))
            if humidity_val > 80:
                suggestions.append("💧 湿度较大，体感偏闷")
            elif humidity_val < 30:
                suggestions.append("💧 空气干燥，多喝水")
        except:
            pass
        
        if city == '威海':
            suggestions.append("🌊 沿海城市，海风较大")
        elif city == '济南':
            suggestions.append("🏔️ 内陆城市，温差较大")
        
        city_data = {
            'city': city,
            'icon': icon,
            'current_temp': current['temp_C'],
            'current_weather': current['weatherDesc'],
            'wind': f"{current['winddir16Point']} {current['windspeedKmph']}km/h",
            'humidity': humidity_display,
            'temp_range': f"{today_fc['minTempC']}~{today_fc['maxTempC']}°C",
            'weather': today_fc['avgWeatherDesc'],
            'uv': uv_display,
            'uv_emoji': uv_emoji,
            'temp_periods': temp_lines,
            'suggestions': suggestions,
        }
        
        city_contents.append(city_data)
    
    # 构建消息
    
    # 1️⃣ 卡片消息头部（美观标题）
    card_header = {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**📅 每日天气预报**\n{today}" + (f"\n🌙 {lunar_info}" if lunar_info else "")
        }
    }
    
    # 2️⃣ 富文本主体（天气详情）
    post_content = []
    
    for city_data in city_contents:
        # 城市名称（富文本）
        post_content.append([{"tag": "text", "text": f"\n{city_data['icon']} {city_data['city']}\n"}])
        
        # 当前天气
        post_content.append([{"tag": "text", "text": 
            f"🌡️ 当前：{city_data['current_temp']}°C | {city_data['current_weather']}\n"
            f"💨 风力：{city_data['wind']}\n"
            f"💧 湿度：{city_data['humidity']}\n"
        }])
        
        # 今日预报
        post_content.append([{"tag": "text", "text": 
            f"{city_data['icon']} 今日：{city_data['temp_range']} | {city_data['weather']}\n"
            f"{city_data['uv_emoji']} 紫外线：{city_data['uv']}\n"
        }])
        
        # 时间段温度
        post_content.append([{"tag": "text", "text": "🕐 温度:\n"}])
        for temp_line in city_data['temp_periods']:
            post_content.append([{"tag": "text", "text": f"{temp_line}\n"}])
        
        # 生活建议（纯文本风格，紧跟城市）
        if city_data['suggestions']:
            post_content.append([{"tag": "text", "text": "\n💡 生活建议:\n"}])
            for sug in city_data['suggestions']:
                post_content.append([{"tag": "text", "text": f"• {sug}\n"}])
        
        # 分割线
        post_content.append([{"tag": "text", "text": "\n━━━━━━━━━━━━━━━━━━\n"}])
    
    # 3️⃣ 底部（纯文本）
    footer = "🤖 自动播报 | 每日 8:00 更新"
    
    return {
        'card_header': card_header,
        'post_content': post_content,
        'footer': footer,
        'city_count': len(city_contents),
    }

# ============================================================================
# 发送飞书消息
# ============================================================================

def get_feishu_token(app_id: str, app_secret: str) -> str:
    """获取飞书 Access Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') != 0:
            raise Exception(f"获取 Token 失败：{result.get('msg')}")
        
        return result['tenant_access_token']
    except Exception as e:
        log(f"❌ 获取飞书 Token 失败：{e}")
        return None


def send_hybrid_message(token: str, chat_id: str, report_data: dict) -> bool:
    """
    发送混合格式消息
    
    策略:
    - 使用富文本消息（post）承载主要内容
    - 结构化排版模拟卡片效果
    - 保持纯文本的简洁性
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 构建富文本消息
    content_elements = report_data['post_content']
    
    # 添加底部
    content_elements.append([{"tag": "text", "text": f"\n{report_data['footer']}\n"}])
    
    payload = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps({
            "zh_cn": {
                "title": "",
                "content": content_elements
            }
        }, ensure_ascii=False)
    }
    
    params = {'receive_id_type': 'chat_id'}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') != 0:
            log(f"❌ 发送消息失败：{result.get('msg')}")
            return False
        
        log(f"✅ 消息已发送到群组 {chat_id}")
        return True
    
    except Exception as e:
        log(f"❌ 发送消息异常：{e}")
        return False

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    log("=" * 50)
    log("🌤️  开始每日天气预报播报 v2（混合格式）")
    
    CITIES = ['济南', '威海']
    
    # 飞书配置
    FEISHU_APP_ID = "cli_a929676f8bf81cc7"
    FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
    GROUP_CHAT_ID = "oc_55a027a0be1c6252a89177256f2210b9"
    
    # 获取天气数据
    log(f"📊 获取天气数据：{', '.join(CITIES)}")
    weather_data_list = []
    
    for city_name in CITIES:
        weather = get_weather(city_name)
        if weather:
            weather_data_list.append(weather)
    
    if not weather_data_list:
        log("❌ 所有城市天气数据获取失败")
        return False
    
    # 构建报告
    log("📝 构建混合格式报告")
    report = build_hybrid_report(weather_data_list)
    
    # 获取 Token
    log("🔑 获取飞书 Token")
    token = get_feishu_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    
    if not token:
        log("❌ 获取飞书 Token 失败")
        return False
    
    # 发送消息
    log(f"📤 发送混合格式消息到群组 {GROUP_CHAT_ID}")
    success = send_hybrid_message(token, GROUP_CHAT_ID, report)
    
    if success:
        log("✅ 天气预报播报完成")
        return True
    else:
        log("❌ 天气预报播报失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
