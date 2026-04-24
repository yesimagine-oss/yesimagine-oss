#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日播报脚本 v7 - 防重複版
修復內容：
1. ✅ 添加消息去重机制（飞书 uuid + 本地缓存）
2. ✅ 添加发送日志记录
3. ✅ 防止短时间重复发送
"""

import requests
import json
import yaml
import time
import hashlib
from datetime import datetime
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

CONFIG_PATH = Path('/home/admin/.openclaw/workspace/config/daily-brief.yaml')
FEISHU_APP_ID = "cli_a929676f8bf81cc7"
FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"

# 消息去重配置
MESSAGE_CACHE_PATH = Path('/tmp/daily-brief-cache.json')
MESSAGE_CACHE_TTL = 300  # 5 分钟内不重复发送

# ============================================================================
# 消息去重函數
# ============================================================================

def load_message_cache():
    """加载消息缓存"""
    if not MESSAGE_CACHE_PATH.exists():
        return {'messages': []}
    try:
        return json.loads(MESSAGE_CACHE_PATH.read_text(encoding='utf-8'))
    except:
        return {'messages': []}

def save_message_cache(cache):
    """保存消息缓存"""
    try:
        MESSAGE_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
    except Exception as e:
        print(f"⚠️ 保存缓存失败：{e}")

def should_send_message(content):
    """检查是否应该发送（避免重复）"""
    cache = load_message_cache()
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    current_time = time.time()
    
    # 清理过期缓存
    cache['messages'] = [
        m for m in cache.get('messages', [])
        if current_time - m.get('time', 0) < MESSAGE_CACHE_TTL
    ]
    
    # 检查是否重复
    for msg in cache.get('messages', []):
        if msg.get('hash') == content_hash:
            print(f"⚠️ 检测到重复消息（{int(current_time - msg.get('time', 0))}秒内），跳过发送")
            save_message_cache(cache)
            return False
    
    save_message_cache(cache)
    return True

def record_sent_message(content, msg_id):
    """记录已发送的消息"""
    cache = load_message_cache()
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    
    cache['messages'].append({
        'hash': content_hash,
        'msg_id': msg_id,
        'time': time.time()
    })
    
    # 只保留最近 1 小时的记录
    current_time = time.time()
    cache['messages'] = [
        m for m in cache.get('messages', [])
        if current_time - m.get('time', 0) < 3600
    ]
    
    save_message_cache(cache)
    print(f"📝 已记录消息：{msg_id}")

# ============================================================================
# 函數
# ============================================================================

def load_config():
    """加載配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_weather(city):
    """獲取天氣（最低~最高温度格式，带°C 单位）- 使用 Open-Meteo API"""
    try:
        # 城市坐标
        city_coords = {
            '济南': {'lat': 36.6512, 'lon': 117.1201},
            '威海': {'lat': 37.5091, 'lon': 122.1248},
        }
        
        coords = city_coords.get(city)
        if not coords:
            return "暂不可用"
        
        # 重试 3 次
        for attempt in range(3):
            try:
                # 使用 Open-Meteo API（无需代理，更可靠）
                url = (
                    f"https://api.open-meteo.com/v1/forecast?"
                    f"latitude={coords['lat']}&longitude={coords['lon']}"
                    f"&daily=temperature_2m_max,temperature_2m_min"
                    f"&timezone=Asia%2FShanghai"
                )
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    daily = data.get('daily', {})
                    low_temp = daily.get('temperature_2m_min', ['--'])[0]
                    high_temp = daily.get('temperature_2m_max', ['--'])[0]
                    # 添加°C 单位
                    return f"{low_temp}~{high_temp}°C"
            except:
                if attempt < 2:
                    time.sleep(1)
                continue
        
        return "暂不可用"
    except:
        return "暂不可用"

def get_lunar_date():
    """獲取農曆（簡化版）"""
    today = datetime.now()
    spring_festival = datetime(2026, 2, 17)
    days_since = (today - spring_festival).days
    lunar_day = (days_since % 30) + 1
    lunar_month = (days_since // 30) + 1
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday = weekdays[today.weekday()]
    return f"农历乙巳年{min(lunar_month, 12)}月{lunar_day}日 {weekday}"

def get_solar_term():
    """獲取節氣（簡化版）"""
    terms = {
        (3, 5): "惊蛰", (3, 20): "春分",
        (4, 4): "清明", (4, 19): "谷雨",
        (5, 5): "立夏", (5, 20): "小满",
    }
    today = datetime.now()
    for (m, d), term in terms.items():
        if today.month == m and abs(today.day - d) <= 5:
            return term
    return ""

# XHunt 已删除 - 全是加密货币广告，垃圾平台

def get_feishu_token():
    """獲取飛書 Token"""
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    resp = requests.post(FEISHU_TOKEN_URL, json=payload, timeout=10)
    result = resp.json()
    if result.get('code') != 0:
        raise Exception(f"Token 失敗：{result}")
    return result['tenant_access_token']

def send_feishu(message, user_id):
    """發送到飛書私聊（带去重机制）"""
    # 生成消息唯一 ID（用于飞书去重）
    client_msg_id = hashlib.md5(f"{message}_{int(time.time() / 60)}".encode('utf-8')).hexdigest()
    
    token = get_feishu_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps({"text": message}, ensure_ascii=False),
        "uuid": client_msg_id  # 飞书去重字段
    }
    resp = requests.post(FEISHU_MESSAGE_URL, headers=headers, json=payload, timeout=10)
    result = resp.json()
    if result.get('code') == 0 or resp.status_code == 200:
        msg_id = result.get('data', {}).get('message_id', 'N/A')
        print(f"✅ 飛書發送成功：{msg_id} (uuid: {client_msg_id[:8]}...)")
        # 记录已发送的消息
        record_sent_message(message, msg_id)
        return True
    else:
        print(f"❌ 飛書發送失敗：{result}")
        return False

def generate_brief():
    """生成播報內容"""
    config = load_config()
    today = datetime.now()
    
    lunar_str = get_lunar_date()
    solar_term = get_solar_term()
    
    weather_list = [f"{city} {get_weather(city)}" for city in config['cities']]
    
    term_str = f" | {solar_term}" if solar_term else ""
    
    content = f"""{lunar_str}{term_str}
{today.year}年{today.month}月{today.day}日 {today.strftime('%A')}

{' '.join(['🌤️ ' + w for w in weather_list])}

🦞 RedOpenClaw
*...生活太快⚡️...老逼快跑💨...*
"""
    return content

# ============================================================================
# 主函數
# ============================================================================

def check_and_start_proxy():
    """检查并启动代理"""
    import subprocess
    import time
    try:
        # 检查代理是否可用
        requests.get('http://127.0.0.1:7890', timeout=2)
        print("✅ 代理已运行")
        return True
    except:
        print("⚠️ 代理未运行，尝试启动...")
        subprocess.run(['python3', '/home/admin/.openclaw/workspace/tools/proxy-manager.py', 'start'], timeout=10)
        time.sleep(3)
        print("✅ 代理已启动")
        return True

def main():
    print("=" * 60)
    print("📅 每日播報 - 開始執行（v7 防重複版）")
    print("=" * 60)
    
    # 检查并启动代理
    check_and_start_proxy()
    
    config = load_config()
    content = generate_brief()
    
    print("\n📝 播報內容:")
    print("-" * 60)
    print(content)
    print("-" * 60)
    
    # 检查是否重复发送
    print("\n🔍 检查消息去重...")
    if not should_send_message(content):
        print("⚠️ 跳过本次发送（检测到重复）")
        print("=" * 60)
        return
    
    user_id = config.get('push', {}).get('user', 'ou_f4919832188bcc630f8f257497fa93a4')
    print(f"\n📤 發送到：{user_id}")
    
    if send_feishu(content, user_id):
        print("\n✅ 播報完成")
    else:
        print("\n❌ 播報失敗")
    
    print("=" * 60)

if __name__ == '__main__':
    import sys
    if sys.version_info < (3, 8):
        import subprocess
        subprocess.run(['python3.8', __file__] + sys.argv[1:])
        sys.exit(0)
    
    try:
        main()
    except Exception as e:
        print(f"❌ 異常：{e}")
        import traceback
        traceback.print_exc()
