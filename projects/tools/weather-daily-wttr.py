#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日天气预报 - 使用 wttr.in (weather skill 推荐)
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
LOG_FILE = LOG_DIR / "weather-daily.log"

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

# ============================================================================
# 农历和节气
# ============================================================================

def get_lunar_date(date: datetime) -> str:
    """获取农历日期（简化版）"""
    try:
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
        solar_term = get_solar_term(date)
        
        if solar_term:
            return f"{lunar_str} {solar_term}"
        return lunar_str
    except:
        return ""

def get_solar_term(date: datetime) -> str:
    """获取 24 节气"""
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
# 天气数据获取（Open-Meteo API - 更可靠）
# ============================================================================

# 城市坐标（纬度，经度）
CITY_COORDS = {
    '济南': {'lat': 36.6512, 'lon': 117.1201},
    '威海': {'lat': 37.5091, 'lon': 122.1248},
}

def get_weather(city_name: str) -> dict:
    """获取城市天气预报（Open-Meteo API）"""
    try:
        coords = CITY_COORDS.get(city_name)
        if not coords:
            log(f"❌ 未知城市：{city_name}")
            return None
        
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={coords['lat']}&longitude={coords['lon']}"
            f"&current_weather=true"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
            f"&hourly=relativehumidity_2m,windspeed_10m,winddirection_10m"
            f"&timezone=Asia%2FShanghai"
        )
        
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            log(f"❌ API 返回错误：{response.status_code}")
            return None
        
        data = response.json()
        current = data.get('current_weather', {})
        daily = data.get('daily', {})
        hourly = data.get('hourly', {})
        
        # 获取当前小时的湿度和风力
        current_hour = datetime.now().hour
        humidity = hourly.get('relativehumidity_2m', ['--'])[current_hour] if hourly else '--'
        wind_speed = hourly.get('windspeed_10m', ['--'])[current_hour] if hourly else '--'
        wind_dir = hourly.get('winddirection_10m', ['--'])[current_hour] if hourly else '--'
        
        # 天气代码转换
        weather_codes = {
            0: '晴朗', 1: '主要晴朗', 2: '多云', 3: '阴天',
            45: '雾', 48: '雾凇',
            51: '毛毛雨', 53: '毛毛雨', 55: '毛毛雨',
            61: '小雨', 63: '中雨', 65: '大雨',
            71: '小雪', 73: '中雪', 75: '大雪',
            80: '阵雨', 81: '中阵雨', 82: '大阵雨',
            95: '雷雨', 96: '雷阵雨', 99: '强雷阵雨'
        }
        
        weather_code = current.get('weathercode', 3)
        weather_desc = weather_codes.get(weather_code, '多云')
        
        return {
            'city': city_name,
            'current': {
                'temp_C': str(current.get('temperature', '--')),
                'weatherDesc': weather_desc,
                'humidity': str(humidity) + '%' if humidity != '--' else '--',
                'windspeedKmph': str(wind_speed) if wind_speed != '--' else '--',
                'winddir16Point': str(wind_dir) + '°' if wind_dir != '--' else '--',
                'uvIndex': str(current.get('is_day', 1)),  # 简化处理
                'visibility': '--',
                'pressure': '--',
                'FeelsLikeC': str(current.get('temperature', '--')),
            },
            'today': {
                'maxTempC': str(daily.get('temperature_2m_max', ['--'])[0]),
                'minTempC': str(daily.get('temperature_2m_min', ['--'])[0]),
                'avgWeatherDesc': weather_desc,
            },
        }
    except Exception as e:
        log(f"❌ 获取 {city_name} 天气异常：{e}")
        return None

# ============================================================================
# 构建报告
# ============================================================================

def build_weather_report(weather_data_list: list) -> str:
    """构建天气报告"""
    now = datetime.now()
    today = now.strftime("%Y年%m月%d日 %A")
    lunar_info = get_lunar_date(now)
    date_line = f"📅 {today}\n🌙 {lunar_info}" if lunar_info else f"📅 {today}"
    
    report = f"{date_line}\n\n"
    
    weather_icons = {
        'Sunny': '☀️', 'Clear': '☀️', 'Partly Cloudy': '⛅',
        'Cloudy': '☁️', 'Overcast': '☁️', 'Mist': '🌫️', 'Fog': '🌫️',
        'Patchy rain': '🌦️', 'Moderate rain': '🌧️', 'Heavy rain': '🌧️',
        'Snow': '❄️', 'Thunderstorm': '⛈️'
    }
    
    for weather in weather_data_list:
        if not weather:
            continue
        
        city = weather['city']
        current = weather['current']
        today_fc = weather['today']
        
        icon = weather_icons.get(today_fc['avgWeatherDesc'], '🌡️')
        
        # 紫外线等级
        try:
            uv = float(current['uvIndex'])
            if uv <= 2: uv_level = '低'
            elif uv <= 5: uv_level = '中等'
            elif uv <= 7: uv_level = '高'
            elif uv <= 10: uv_level = '很高'
            else: uv_level = '极高'
            uv_display = f"{uv}（{uv_level}）"
        except:
            uv_display = current['uvIndex']
        
        report += f"""📍 {city}

🌡️ 当前：{current['temp_C']}°C | {current['weatherDesc']}
💨 风力：{current['winddir16Point']} {current['windspeedKmph']}km/h
💧 湿度：{current['humidity']}%

{icon} 今日：{today_fc['minTempC']}~{today_fc['maxTempC']}°C | {today_fc['avgWeatherDesc']}
☀️ 紫外线：{uv_display}

"""
        
        # 生活建议
        suggestions = []
        
        try:
            avg_temp = (float(today_fc['maxTempC']) + float(today_fc['minTempC'])) / 2
            if avg_temp < 10:
                suggestions.append("🧥 天气较冷，注意保暖")
            elif avg_temp < 20:
                suggestions.append("👕 温度适宜，可穿长袖")
            elif avg_temp < 28:
                suggestions.append("👕 天气温暖，短袖即可")
            else:
                suggestions.append("🩳 天气炎热，注意防暑")
            
            if float(today_fc['maxTempC']) - float(today_fc['minTempC']) > 10:
                suggestions.append("🌡️ 昼夜温差大，早晚添衣")
        except:
            pass
        
        try:
            uv = float(current['uvIndex'])
            if uv >= 8:
                suggestions.append("☀️ 紫外线很强，尽量避免外出")
            elif uv >= 6:
                suggestions.append("☀️ 紫外线强，外出注意防晒")
            elif uv >= 3:
                suggestions.append("☀️ 紫外线中等，适当防护")
        except:
            pass
        
        weather_desc = today_fc['avgWeatherDesc']
        if 'rain' in weather_desc.lower() or '雨' in weather_desc:
            suggestions.append("☔ 有雨，出门带伞")
        
        try:
            wind = float(current['windspeedKmph'])
            if wind > 40:
                suggestions.append("💨 大风，减少外出")
            elif wind > 25:
                suggestions.append("💨 风力较大，注意防风")
        except:
            pass
        
        try:
            humidity = float(current['humidity'])
            if humidity > 80:
                suggestions.append("💧 湿度较大，体感偏闷")
            elif humidity < 30:
                suggestions.append("💧 空气干燥，多喝水")
        except:
            pass
        
        if city == '威海':
            suggestions.append("🌊 沿海城市，海风较大")
        elif city == '济南':
            suggestions.append("🏔️ 内陆城市，温差较大")
        
        if suggestions:
            report += "💡 生活建议:\n"
            for sug in suggestions:
                report += f"• {sug}\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━\n\n"
    
    report += "🤖 自动播报 | 每日 8:00 更新\n"
    return report

# ============================================================================
# 发送飞书消息
# ============================================================================

def get_feishu_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    result = response.json()
    return result.get('tenant_access_token')

def send_feishu_message(token: str, chat_id: str, content: str) -> bool:
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    lines = content.split('\n')
    content_elements = [[{"tag": "text", "text": f"{line}\n"}] for line in lines if line.strip()]
    
    payload = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps({"zh_cn": {"title": "", "content": content_elements}}, ensure_ascii=False)
    }
    
    response = requests.post(url, headers=headers, params={'receive_id_type': 'chat_id'}, json=payload, timeout=10)
    result = response.json()
    
    if result.get('code') != 0:
        log(f"❌ 发送失败：{result.get('msg')}")
        return False
    
    log(f"✅ 消息已发送")
    return True

# ============================================================================
# 主函数
# ============================================================================

def main():
    log("=" * 50)
    log("🌤️  开始每日天气预报播报（wttr.in）")
    
    CITIES = ['济南', '威海']
    FEISHU_APP_ID = "cli_a929676f8bf81cc7"
    FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
    GROUP_CHAT_ID = "oc_55a027a0be1c6252a89177256f2210b9"
    
    log(f"📊 获取天气数据：{', '.join(CITIES)}")
    weather_data_list = [get_weather(city) for city in CITIES]
    weather_data_list = [w for w in weather_data_list if w]
    
    if not weather_data_list:
        log("❌ 天气数据获取失败")
        return False
    
    log("📝 构建天气报告")
    report = build_weather_report(weather_data_list)
    
    log("🔑 获取飞书 Token")
    token = get_feishu_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    if not token:
        return False
    
    log(f"📤 发送到群组 {GROUP_CHAT_ID}")
    return send_feishu_message(token, GROUP_CHAT_ID, report)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
