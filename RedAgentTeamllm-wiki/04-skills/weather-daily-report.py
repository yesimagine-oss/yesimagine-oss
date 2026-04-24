#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日天气预报 - 飞书群组播报
功能：每日 8:00 发送济南/威海天气预报到指定飞书群组
"""

import sys
import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 农历和节气（简化实现，无需外部库）
LUNAR_AVAILABLE = True  # 使用内置简化版本

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 日志配置
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "weather-daily.log"

# ============================================================================
# 农历节气工具
# ============================================================================

def get_lunar_date(date: datetime) -> str:
    """
    获取农历日期和节气（简化版，基于 2026 年）
    
    Returns:
        农历字符串，如 "二月初八 惊蛰"
    """
    try:
        # 2026 年农历数据（简化版，仅当年有效）
        # 2026 年春节是 2 月 17 日（农历正月初一）
        spring_festival = datetime(2026, 2, 17)
        
        if date < spring_festival:
            # 春节前，属于农历乙巳年（蛇年）
            year_name = "乙巳年"
            # 估算月份（简化）
            lunar_month = 12 + date.month - 1
            if lunar_month > 12:
                lunar_month -= 12
        else:
            # 春节后，属于农历丙午年（马年）
            year_name = "丙午年"
            # 从春节开始计算农历月份
            days_since_spring = (date - spring_festival).days
            lunar_month = 1 + days_since_spring // 30
            if lunar_month > 12:
                lunar_month = 12
        
        # 农历日期（简化估算，从春节开始计算天数）
        spring_festival = datetime(2026, 2, 17)
        days_since_spring = (date - spring_festival).days
        lunar_day = 1 + days_since_spring % 30
        
        # 农历月份名称
        month_names = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
        month_name = month_names[lunar_month - 1] if 1 <= lunar_month <= 12 else '腊'
        
        # 农历日期名称
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
    """
    获取 24 节气（基于日期范围）
    
    2026 年节气日期（近似值）
    """
    # 2026 年节气日期表
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
    
    # 检查是否是节气日（前后 1 天）
    month, day = date.month, date.day
    for term_month, term_day, term_name in solar_terms_2026:
        if month == term_month and abs(day - term_day) <= 1:
            return term_name
    
    return ""

def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ============================================================================
# 1. 获取天气数据（使用 weather skill）
# ============================================================================

def get_weather(city_name: str) -> dict:
    """
    获取城市天气预报（使用 wttr.in - weather skill 推荐）
    
    Args:
        city_name: 城市名称（中文）
    
    Returns:
        天气数据字典
    """
    try:
        # wttr.in API（免费，无需 Key，支持中文）
        url = f"https://wttr.in/{city_name}?format=j1"
        headers = {"User-Agent": "weather-bot/1.0"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            log(f"⚠️ 获取 {city_name} 天气失败：HTTP {response.status_code}")
            return None
        
        data = response.json()
        
        # 提取当前天气
        current = data.get('current_condition', [{}])[0]
        
        # 提取今日预报
        weather_today = data.get('weather', [{}])[0]
        weather_tomorrow = data.get('weather', [{}])[1] if len(data.get('weather', [])) > 1 else {}
        
        # 提取小时数据（用于时间段温度）
        hourly = weather_today.get('hourly', [])
        
        # 定义时间段（24 小时制）
        time_periods = {
            '清晨': (5, 7),
            '上午': (8, 11),
            '中午': (12, 13),
            '下午': (14, 17),
            '傍晚': (18, 19),
            '晚上': (20, 23),
        }
        
        # 获取各时间段温度
        period_temps = {}
        for period_name, (start_hour, end_hour) in time_periods.items():
            temps = []
            for h in range(start_hour, end_hour + 1):
                if h < len(hourly):
                    temps.append(float(hourly[h].get('temp_C', 0)))
            if temps:
                period_temps[period_name] = round(sum(temps) / len(temps), 1)
            else:
                period_temps[period_name] = '--'
        
        # 天气描述
        weather_desc = current.get('weatherDesc', [{}])[0].get('value', '未知')
        
        return {
            'city': city_name,
            'current': {
                'temp_C': current.get('temp_C', '--'),
                'weatherDesc': weather_desc,
                'humidity': current.get('humidity', '--'),
                'windspeedKmph': current.get('windspeedKmph', '--'),
                'winddir16Point': current.get('winddir16Point', '--'),
                'pressure': current.get('pressure', '--'),  # 气压
                'visibility': current.get('visibility', '--'),  # 能见度
                'uvIndex': current.get('uvIndex', '--'),  # 紫外线
                'FeelsLikeC': current.get('FeelsLikeC', '--'),  # 体感温度
            },
            'today': {
                'maxTempC': weather_today.get('maxtempC', '--'),
                'minTempC': weather_today.get('mintempC', '--'),
                'avgWeatherDesc': weather_today.get('avgWeatherDesc', [{}])[0].get('value', '未知'),
                'uvIndex': current.get('uvIndex', '--'),
                'period_temps': period_temps,
                'sunrise': weather_today.get('astronomy', [{}])[0].get('sunrise', '--'),
                'sunset': weather_today.get('astronomy', [{}])[0].get('sunset', '--'),
                'moon_phase': weather_today.get('astronomy', [{}])[0].get('moon_phase', '--'),
            },
            'tomorrow': {
                'maxTempC': weather_tomorrow.get('maxtempC', '--'),
                'minTempC': weather_tomorrow.get('mintempC', '--'),
                'weatherDesc': weather_tomorrow.get('avgWeatherDesc', [{}])[0].get('value', '--'),
            } if weather_tomorrow else None
        }
    
    except Exception as e:
        log(f"❌ 获取 {city_name} 天气异常：{e}")
        return None


# ============================================================================
# 2. 构建天气报告
# ============================================================================

def build_weather_report(weather_data_list: list) -> str:
    """
    构建天气报告文本
    
    Args:
        weather_data_list: 多个城市的天气数据列表
    
    Returns:
        格式化的天气报告
    """
    now = datetime.now()
    today = now.strftime("%Y年%m月%d日 %A")
    
    # 获取农历和节气
    lunar_info = get_lunar_date(now)
    if lunar_info:
        date_line = f"📅 {today}\n🌙 {lunar_info}"
    else:
        date_line = f"📅 {today}"
    
    report = f"""{date_line}

"""
    
    for weather in weather_data_list:
        if not weather:
            continue
        
        city = weather['city']
        current = weather['current']
        today_fc = weather['today']
        tomorrow_fc = weather.get('tomorrow')
        
        # 天气图标
        weather_icons = {
            '晴朗': '☀️', '主要晴朗': '☀️', '多云': '⛅',
            '阴天': '☁️', '雾': '🌫️', '雾凇': '🌫️',
            '毛毛雨': '🌦️', '小雨': '🌧️', '中雨': '🌧️', '大雨': '🌧️',
            '小雪': '❄️', '中雪': '❄️', '大雪': '❄️',
            '雷暴': '⛈️', '雷暴伴冰雹': '⛈️', '强雷暴伴冰雹': '⛈️'
        }
        
        icon = '🌡️'
        for key, value in weather_icons.items():
            if key in today_fc['avgWeatherDesc']:
                icon = value
                break
        
        # 湿度显示
        humidity = current.get('humidity', '--')
        if humidity == '--' or humidity == '':
            humidity_display = '--'
        else:
            humidity_display = f"{humidity}%"
        
        # 紫外线等级
        uv = today_fc.get('uvIndex', '--')
        if uv != '--':
            try:
                uv_val = float(uv)
                if uv_val <= 2:
                    uv_level = '低'
                elif uv_val <= 5:
                    uv_level = '中等'
                elif uv_val <= 7:
                    uv_level = '高'
                elif uv_val <= 10:
                    uv_level = '很高'
                else:
                    uv_level = '极高'
                uv_display = f"{uv_val}（{uv_level}）"
            except:
                uv_display = uv
        else:
            uv_display = uv
        
        # 时间段温度显示（竖排）
        period_temps = today_fc.get('period_temps', {})
        temp_lines = []
        for period in ['清晨', '上午', '中午', '下午', '傍晚', '晚上']:
            temp = period_temps.get(period, '--')
            if temp != '--':
                temp_lines.append(f"{period}{temp}°C")
        
        temp_display = "\n".join(temp_lines)
        
        report += f"""📍 {city}

🌡️ 当前：{current['temp_C']}°C | {current['weatherDesc']}
💨 风力：{current['winddir16Point']} {current['windspeedKmph']}km/h
💧 湿度：{humidity_display}

{icon} 今日：{today_fc['minTempC']}~{today_fc['maxTempC']}°C | {today_fc['avgWeatherDesc']}
☀️ 紫外线：{uv_display}
🕐 温度：
{temp_display}

"""
        
        # 为当前城市生成生活建议
        suggestions = []
        
        # 温度建议
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
            
            # 温差建议
            temp_diff = max_temp - min_temp
            if temp_diff > 10:
                suggestions.append("🌡️ 昼夜温差大，早晚添衣")
        except:
            pass
        
        # 紫外线建议
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
        
        # 天气状况建议
        weather_desc = today_fc['avgWeatherDesc']
        if '雨' in weather_desc:
            suggestions.append("☔ 有雨，出门带伞")
        if '雪' in weather_desc:
            suggestions.append("❄️ 有雪，注意路滑")
        if '雾' in weather_desc:
            suggestions.append("🌫️ 有雾，注意出行安全")
        if '雷暴' in weather_desc:
            suggestions.append("⛈️ 雷暴天气，避免外出")
        
        # 风力建议
        try:
            wind_speed = float(current.get('windspeedKmph', 0))
            if wind_speed > 40:
                suggestions.append("💨 大风，减少外出")
            elif wind_speed > 25:
                suggestions.append("💨 风力较大，注意防风")
        except:
            pass
        
        # 湿度建议
        try:
            humidity = float(current.get('humidity', 50))
            if humidity > 80:
                suggestions.append("💧 湿度较大，体感偏闷")
            elif humidity < 30:
                suggestions.append("💧 空气干燥，多喝水")
        except:
            pass
        
        # 城市特定建议
        if city == '威海':
            suggestions.append("🌊 沿海城市，海风较大")
        elif city == '济南':
            suggestions.append("🏔️ 内陆城市，温差较大")
        
        # 输出城市建议（紧跟在该城市天气后面）
        if suggestions:
            report += "💡 生活建议:\n"
            for sug in suggestions:
                report += f"• {sug}\n"
            report += "\n"
        
        report += "━━━━━━━━━━━━━━━━━━\n\n"
    
    report += "🤖 自动播报 | 每日 8:00 更新\n"
    
    return report


# ============================================================================
# 3. 发送飞书消息
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


def send_feishu_group_message(token: str, chat_id: str, content: str) -> bool:
    """
    发送飞书群组消息
    
    Args:
        token: Access Token
        chat_id: 群组 ID
        content: 消息内容
    
    Returns:
        发送是否成功
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 构建富文本消息
    lines = content.split('\n')
    content_elements = []
    
    for line in lines:
        if line.strip():
            content_elements.append([{"tag": "text", "text": f"{line}\n"}])
    
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
    
    # 使用 chat_id 类型发送群组消息
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
# 4. 主函数
# ============================================================================

def main():
    """主函数"""
    log("=" * 50)
    log("🌤️  开始每日天气预报播报")
    
    # 配置（城市名称）
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
    log("📝 构建天气报告")
    report = build_weather_report(weather_data_list)
    
    # 获取 Token
    log("🔑 获取飞书 Token")
    token = get_feishu_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    
    if not token:
        log("❌ 获取飞书 Token 失败")
        return False
    
    # 发送消息
    log(f"📤 发送消息到群组 {GROUP_CHAT_ID}")
    success = send_feishu_group_message(token, GROUP_CHAT_ID, report)
    
    if success:
        log("✅ 天气预报播报完成")
        print(report)
        return True
    else:
        log("❌ 天气预报播报失败")
        return False


# ============================================================================
# CLI 入口
# ============================================================================

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
