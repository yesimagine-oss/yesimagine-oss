#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股每日播報腳本 v3 - 代理按需開啟版
功能：
1. 按需開啟代理
2. 獲取 A 股數據（上證 + 深證 + 創業板）
3. AI 技術分析 + 策略建議
4. 飛書群組推送

修復內容：
- ✅ 代理按需開啟（不再說「代理沒開」）
- ✅ 數據驗證
- ✅ 內容質量檢查
- ✅ AI 分析建議
- ✅ 錯誤處理

執行時間：每日 09:00
推送群組：oc_55a027a0be1c6252a89177256f2210b9
"""

import requests
import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

# ============================================================================
# 配置
# ============================================================================

# 股票指數代碼（东方财富格式：市場。代碼）
STOCKS = {
    '上证指数': '1.000001',
    '深证成指': '0.399001',
    '创业板指': '0.399006',
    '沪深 300': '1.000300'
}

# 代理配置
PROXY = 'http://127.0.0.1:7890'
PROXY_SCRIPT = Path(__file__).parent / "proxy-on-demand.py"

# 飛書配置
FEISHU_CHAT_ID = "oc_55a027a0be1c6252a89177256f2210b9"
FEISHU_APP_ID = "cli_a929676f8bf81cc7"
FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"

# 日誌配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "stock-report.log"

def log(message: str):
    """記錄日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ============================================================================
# 代理管理（按需開啟）
# ============================================================================

def check_proxy_status() -> bool:
    """檢查代理是否運行"""
    try:
        response = requests.get("https://www.google.com", 
                              proxies={'http': PROXY, 'https': PROXY}, 
                              timeout=3)
        return response.status_code == 200
    except:
        return False


def ensure_proxy() -> bool:
    """確保代理已開啟（按需啟動）"""
    if check_proxy_status():
        return True
    
    log("⚠️ 代理未運行，正在開啟...")
    
    try:
        # 使用 mihomo-manager 開啟代理
        mihomo_script = Path(__file__).parent / "mihomo-manager.py"
        if mihomo_script.exists():
            result = subprocess.Popen(
                ["python3", str(mihomo_script), "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=30)
            
            if result.returncode == 0:
                log("✅ 代理已開啟")
                time.sleep(3)
                return check_proxy_status()
            else:
                log(f"❌ 代理開啟失敗：{stderr}")
                return False
        else:
            log("❌ mihomo-manager.py 不存在")
            return False
    except Exception as e:
        log(f"❌ 代理開啟異常：{e}")
        return False


# 初始化時確保代理可用
if ensure_proxy():
    os.environ['HTTP_PROXY'] = PROXY
    os.environ['HTTPS_PROXY'] = PROXY
    os.environ['http_proxy'] = PROXY
    os.environ['https_proxy'] = PROXY
    log("✅ 代理已配置")
else:
    log("⚠️ 代理未可用，將使用備用 API")

# ============================================================================
# 獲取股票數據
# ============================================================================

def get_stock_data(stock_code: str, retry: int = 3) -> Optional[Dict]:
    """
    獲取股票數據（东方财富 API - 无需代理，數據穩定）
    """
    # 东方财富 API（无需代理，返回 JSON）
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={stock_code}&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://quote.eastmoney.com/'
    }
    
    for attempt in range(retry):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                data = result.get('data', {})
                
                if data and data.get('f43'):  # 當前價格
                    return {
                        'name': stock_code,
                        'current': float(data['f43']) / 100,  # 轉換為實際價格
                        'close': float(data['f44']) / 100 if data.get('f44') else float(data['f43']) / 100,  # 昨日收盤
                        'open': float(data['f45']) / 100 if data.get('f45') else 0,
                        'high': float(data['f46']) / 100 if data.get('f46') else 0,
                        'low': float(data['f47']) / 100 if data.get('f47') else 0,
                        'volume': int(data['f48']) if data.get('f48') else 0,
                        'amount': float(data['f49']) / 100000000 if data.get('f49') else 0,  # 轉換為億
                    }
            
            log(f"   嘗試 {attempt+1}/{retry}：數據無效")
            
        except Exception as e:
            log(f"   嘗試 {attempt+1}/{retry}：{e}")
    
    return None


def calculate_change(current: float, close: float) -> float:
    """計算漲跌幅"""
    if close == 0:
        return 0
    return ((current - close) / close) * 100

# ============================================================================
# AI 分析建議
# ============================================================================

def ai_analyze_market(stocks_data: Dict) -> Dict:
    """AI 市場分析"""
    analysis = {
        'sentiment': '震盪',
        'volume_trend': '持平',
        'main_force': '-',
        'technical': '-',
        'suggestion': '謹慎操作',
        'reasons': []
    }
    
    sh = stocks_data.get('上证指数', {})
    if sh:
        change = calculate_change(sh['current'], sh['close'])
        
        if change > 1:
            analysis['sentiment'] = '偏多'
            analysis['reasons'].append(f'上證大漲{change:.2f}%')
        elif change < -1:
            analysis['sentiment'] = '偏空'
            analysis['reasons'].append(f'上證大跌{change:.2f}%')
        else:
            analysis['sentiment'] = '震盪'
            analysis['reasons'].append(f'上證震盪{change:+.2f}%')
        
        if sh['current'] > 3000:
            analysis['technical'] = '站穩 3000 點關口'
        else:
            analysis['technical'] = '3000 點下方震盪'
        
        amount = sh.get('amount', 0)
        if amount > 400000000000:
            analysis['volume_trend'] = '放大'
        elif amount < 200000000000:
            analysis['volume_trend'] = '萎縮'
        else:
            analysis['volume_trend'] = '持平'
    
    cyb = stocks_data.get('创业板指', {})
    if cyb:
        change = calculate_change(cyb['current'], cyb['close'])
        if change > 2:
            analysis['main_force'] = '創業板領漲'
        elif change < -2:
            analysis['main_force'] = '創業板領跌'
    
    if analysis['sentiment'] == '偏多':
        analysis['suggestion'] = '6-7 成倉位，可積極'
    elif analysis['sentiment'] == '偏空':
        analysis['suggestion'] = '3-4 成倉位，防守'
    else:
        analysis['suggestion'] = '5-6 成倉位，震盪操作'
    
    return analysis


def generate_prediction(stocks_data: Dict) -> Dict:
    """生成今日預測"""
    predictions = {}
    
    for name, data in stocks_data.items():
        if not data:
            continue
        
        current = data['current']
        high = data['high']
        low = data['low']
        
        pred_low = round(low * 0.995, 2) if low > 0 else 0
        pred_high = round(high * 1.015, 2) if high > 0 else 0
        
        change = calculate_change(current, data['close'])
        if change > 0.5:
            trend = '震盪上行'
        elif change < -0.5:
            trend = '震盪下行'
        else:
            trend = '震盪'
        
        predictions[name] = {
            'low': pred_low,
            'high': pred_high,
            'trend': trend
        }
    
    return predictions

# ============================================================================
# 生成報告
# ============================================================================

def generate_report() -> Optional[str]:
    """生成播報內容"""
    log("📊 開始獲取股票數據...")
    
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d %A")
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    
    current_hour = today.hour
    current_minute = today.minute
    is_market_open = (
        (current_hour == 9 and current_minute >= 30) or
        (current_hour == 10) or
        (current_hour == 11 and current_minute <= 30) or
        (current_hour >= 13 and current_hour < 15)
    )
    market_status = "已開盤" if is_market_open else "未開盤（09:30）"
    
    stocks_data = {}
    for name, code in STOCKS.items():
        log(f"   獲取 {name} ({code})...")
        data = get_stock_data(code)
        if data:
            stocks_data[name] = data
            log(f"   ✅ {name}: {data['current']:.2f}")
        else:
            log(f"   ❌ {name} 數據獲取失敗")
    
    if '上证指数' not in stocks_data:
        log("❌ 上證指數數據獲取失敗，停止生成報告")
        return None
    
    log("🧠 進行 AI 分析...")
    analysis = ai_analyze_market(stocks_data)
    predictions = generate_prediction(stocks_data)
    
    report = f"""📈 A 股每日播報 | {today_str}

━━━━━━━━━━━━━━━━━━
📊 核心數據（昨日收盤）
━━━━━━━━━━━━━━━━━━
市場狀態：{market_status}

"""
    
    for name in ['上证指数', '深证成指', '创业板指']:
        data = stocks_data.get(name)
        if not data:
            continue
        
        change = calculate_change(data['current'], data['close'])
        change_sign = '+' if change >= 0 else ''
        emoji = '📈' if change > 0 else '📉' if change < 0 else '➡️'
        
        report += f"{emoji} {name}：{data['current']:.2f} ({change_sign}{change:.2f}%)\n"
    
    sh = stocks_data.get('上证指数')
    if sh and sh.get('amount', 0) > 0:
        amount = sh['amount'] / 100000000
        report += f"\n💰 上證成交：{amount:.0f}億 {analysis['volume_trend']}"
    else:
        report += f"\n💰 上證成交：待開盤後更新"
    
    report += f"""

━━━━━━━━━━━━━━━━━━
🧠 AI 市場分析
━━━━━━━━━━━━━━━━━━
【市場情緒】{analysis['sentiment']} - {'；'.join(analysis['reasons'])}
【技術面】{analysis['technical']}
【資金面】{analysis['main_force']}

━━━━━━━━━━━━━━━━━━
💡 今日策略建議
━━━━━━━━━━━━━━━━━━
✅ 倉位：{analysis['suggestion']}
✅ 關注：科技、新能源、消費板塊
⚠️ 風險：{'成交量' if analysis['volume_trend'] == '萎縮' else '追高'}風險

━━━━━━━━━━━━━━━━━━
🔮 今日預測
━━━━━━━━━━━━━━━━━━
"""
    
    for name in ['上证指数', '创业板指']:
        pred = predictions.get(name)
        if pred and pred['low'] > 0 and pred['high'] > 0:
            report += f"{name}：{pred['low']:.0f}-{pred['high']:.0f}（{pred['trend']}）\n"
        else:
            report += f"{name}：待開盤後分析\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━
📌 風險提示
━━━━━━━━━━━━━━━━━━
• 預測僅供參考，不構成投資建議
• 股市有風險，入市需謹慎
• 結合個人風險承受能力決策

━━━━━━━━━━━━━━━━━━
🤖 AI 播報 | 數據：东方财富 | 分析：RedOpenClaw
"""
    
    if len(report.strip()) < 500:
        log(f"❌ 報告內容過短（{len(report)}字），停止發送")
        return None
    
    if "上证指数" not in report:
        log("❌ 報告缺少上證指數數據，停止發送")
        return None
    
    log(f"✅ 報告生成成功（{len(report)}字）")
    return report

# ============================================================================
# 發送飛書消息
# ============================================================================

def get_feishu_token() -> str:
    """獲取飛書 Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    response = requests.post(url, json=payload, timeout=10)
    result = response.json()
    if result.get('code') != 0:
        raise Exception(f"獲取飛書 Token 失敗：{result}")
    return result['tenant_access_token']


def send_feishu_message(content: str) -> bool:
    """發送飛書消息到群組"""
    try:
        token = get_feishu_token()
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "receive_id": FEISHU_CHAT_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content}, ensure_ascii=False)
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 0 or response.status_code == 200:
            log("✅ 飛書消息發送成功")
            return True
        else:
            log(f"❌ 飛書消息發送失敗：{result}")
            return False
            
    except Exception as e:
        log(f"❌ 飛書消息發送異常：{e}")
        return False

# ============================================================================
# 主函數
# ============================================================================

def main():
    """主函數"""
    log("=" * 60)
    log("📈 開始 A 股每日播報 v3（代理按需開啟）")
    log("=" * 60)
    
    report = generate_report()
    
    if not report:
        log("❌ 報告生成失敗，已停止發送")
        log("=" * 60)
        return
    
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    log("\n📱 發送飛書消息...")
    success = send_feishu_message(report)
    
    if success:
        log("✅ A 股播報完成")
    else:
        log("❌ A 股播報失敗，請檢查配置")
    
    log("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("⚠️ 用戶中斷執行")
    except Exception as e:
        log(f"❌ 腳本執行異常：{e}")
        import traceback
        log(traceback.format_exc())
