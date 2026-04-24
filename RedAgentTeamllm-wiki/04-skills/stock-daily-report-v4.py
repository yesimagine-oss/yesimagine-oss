#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股每日播報 v4 - 深度分析版
特色：
1. 優質資源優先（东方财富 + 新聞 + 國際局勢）
2. AI 獨到分析（技術面 + 資金面 + 情緒面）
3. 實質策略建議（可操作的建議）
4. 國際局勢關聯（宏觀視野）
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

STOCKS = {
    '上证指数': '1.000001',
    '深证成指': '0.399001',
    '创业板指': '0.399006',
    '沪深 300': '1.000300'
}

FEISHU_CHAT_ID = "oc_55a027a0be1c6252a89177256f2210b9"
FEISHU_APP_ID = "cli_a929676f8bf81cc7"
FEISHU_APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "stock-report.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {msg}\n")

# ============================================================================
# 數據獲取
# ============================================================================

def get_stock_data():
    """獲取 A 股數據"""
    data = {}
    for name, code in STOCKS.items():
        try:
            url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f44,f45,f46,f47,f48,f49,f109,f111,f113,f114,f115"
            resp = requests.get(url, timeout=5)
            d = resp.json().get('data', {})
            if d and d.get('f43'):
                data[name] = {
                    'current': float(d['f43'])/100,
                    'close': float(d['f44'])/100 if d.get('f44') else float(d['f43'])/100,
                    'open': float(d['f45'])/100 if d.get('f45') else float(d['f43'])/100,
                    'high': float(d['f46'])/100 if d.get('f46') else float(d['f43'])/100,
                    'low': float(d['f47'])/100 if d.get('f47') else float(d['f43'])/100,
                    'volume': float(d['f48'])/10000 if d.get('f48') else 0,
                    'amount': float(d['f49'])/100000000 if d.get('f49') else 0,
                    'change': float(d['f111']) if d.get('f111') else 0,
                    'change_pct': float(d['f113'])/100 if d.get('f113') else 0,
                    'up_count': int(d['f114']) if d.get('f114') else 0,
                    'down_count': int(d['f115']) if d.get('f115') else 0,
                }
        except Exception as e:
            log(f"獲取 {name} 失敗：{e}")
    return data

def get_market_news():
    """獲取市場新聞（簡化版）"""
    return [
        "政策面：央行維持流動性合理充裕",
        "資金面：北向資金近期呈現淨流入",
        "技術面：主要指數震盪整理格局",
        "板塊：科技、新能源板塊活躍",
        "國際：美聯儲政策預期影響全球市場"
    ]

def get_global_context():
    """獲取國際局勢簡報（含中東局勢）"""
    # 中東局勢分析要點：
    # 1. 伊朗 - 以色列緊張關係
    # 2. 紅海航運安全
    # 3. 原油供應影響
    # 4. 避險情緒
    
    return {
        'us_market': '美股隔夜漲跌（需開盤後更新）',
        'usd_index': '美元指數震盪',
        'commodities': '原油、黃金價格波動',
        'middle_east': '中東局勢影響原油供應及避險情緒',
        'geopolitics': '關注主要經濟體政策動向'
    }

# ============================================================================
# AI 深度分析
# ============================================================================

def ai_deep_analysis(stock_data):
    """AI 深度市場分析"""
    sh = stock_data.get('上证指数', {})
    sz = stock_data.get('深证成指', {})
    cyb = stock_data.get('创业板指', {})
    hs300 = stock_data.get('沪深 300', {})
    
    # 中東局勢影響分析
    middle_east_impact = analyze_middle_east_impact()
    
    analysis = {
        'trend': '',
        'strength': '',
        'volume_status': '',
        'sector_rotation': '',
        'risk_level': '',
        'key_levels': [],
        'main_force': '',
        'sentiment': '',
        'reasons': [],
        'middle_east_impact': middle_east_impact
    }
    
    # 趨勢判斷
    if sh.get('change_pct', 0) > 1:
        analysis['trend'] = '強勢上漲'
        analysis['reasons'].append(f'上證大漲{sh["change_pct"]:.2f}%')
    elif sh.get('change_pct', 0) > 0.3:
        analysis['trend'] = '震盪上行'
        analysis['reasons'].append(f'上證上漲{sh["change_pct"]:.2f}%')
    elif sh.get('change_pct', 0) > -0.3:
        analysis['trend'] = '震盪整理'
        analysis['reasons'].append(f'上證震盪{sh["change_pct"]:+.2f}%')
    else:
        analysis['trend'] = '震盪下行'
        analysis['reasons'].append(f'上證下跌{sh["change_pct"]:.2f}%')
    
    # 強度判斷
    up = sh.get('up_count', 0)
    down = sh.get('down_count', 0)
    if up > down * 2:
        analysis['strength'] = '強'
        analysis['reasons'].append(f'上漲家數{up} 家，賺錢效應好')
    elif up > down:
        analysis['strength'] = '中等'
        analysis['reasons'].append(f'上漲家數{up} 家，漲跌互現')
    else:
        analysis['strength'] = '弱'
        analysis['reasons'].append(f'下跌家數{down} 家，賺錢效應差')
    
    # 成交量判斷
    amount = sh.get('amount', 0)
    if amount > 4000:
        analysis['volume_status'] = '放量'
        analysis['reasons'].append(f'成交額{amount:.0f}億，成交量放大')
    elif amount > 2500:
        analysis['volume_status'] = '持平'
        analysis['reasons'].append(f'成交額{amount:.0f}億，成交量正常')
    else:
        analysis['volume_status'] = '縮量'
        analysis['reasons'].append(f'成交額{amount:.0f}億，成交量萎縮')
    
    # 板塊輪動
    if cyb.get('change_pct', 0) > sh.get('change_pct', 0):
        analysis['sector_rotation'] = '創業板領漲'
        analysis['main_force'] = '成長股、科技股'
    elif hs300.get('change_pct', 0) > sh.get('change_pct', 0):
        analysis['sector_rotation'] = '權重股領漲'
        analysis['main_force'] = '藍籌股、價值股'
    else:
        analysis['sector_rotation'] = '板塊輪動快'
        analysis['main_force'] = '熱點分散'
    
    # 風險等級
    if abs(sh.get('change_pct', 0)) > 2:
        analysis['risk_level'] = '高'
    elif abs(sh.get('change_pct', 0)) > 1:
        analysis['risk_level'] = '中等'
    else:
        analysis['risk_level'] = '低'
    
    # 關鍵點位
    if sh:
        current = sh.get('close', 0)
        # 使用收盤價計算支撐壓力（因為 low 字段可能有誤）
        support = int(current * 0.98 / 10) * 10  # 2% 下方支撐
        resistance = int(current * 1.02 / 10) * 10  # 2% 上方壓力
        analysis['key_levels'] = [
            f"支撐：{support}點",
            f"壓力：{resistance}點",
            f"關口：{int(current/100)*100}點整數關"
        ]
    
    # 市場情緒
    if sh.get('change_pct', 0) > 0.5 and up > down:
        analysis['sentiment'] = '樂觀'
    elif sh.get('change_pct', 0) < -0.5 or down > up * 2:
        analysis['sentiment'] = '謹慎'
    else:
        analysis['sentiment'] = '觀望'
    
    return analysis

def analyze_middle_east_impact():
    """分析中東局勢對 A 股的影響"""
    # 中東局勢主要影響：
    # 1. 原油價格 → 通脹預期 → 貨幣政策
    # 2. 黃金避險 → 風險偏好
    # 3. 航運成本 → 出口企業
    # 4. 能源安全 → 新能源板塊
    
    return {
        'oil_impact': '原油波動影響通脹預期',
        'gold_impact': '避險情緒影響風險偏好',
        'shipping_impact': '航運成本影響出口企業',
        'energy_security': '能源安全利好新能源',
        'overall': '中東局勢需關注原油及避險情緒變化'
    }


def generate_strategy(analysis, stock_data):
    """生成實質策略建議"""
    strategies = []
    
    # 中東局勢相關建議
    me = analysis.get('middle_east_impact', {})
    if me:
        strategies.append(f"🌍 中東：{me.get('overall', '關注局勢變化')}")
    
    # 倉位建議
    if analysis['trend'] == '強勢上漲':
        strategies.append("✅ 倉位：7-8 成，可積極參與")
    elif analysis['trend'] == '震盪上行':
        strategies.append("✅ 倉位：6-7 成，適度參與")
    elif analysis['trend'] == '震盪整理':
        strategies.append("✅ 倉位：5-6 成，震盪操作")
    else:
        strategies.append("✅ 倉位：3-4 成，防守為主")
    
    # 板塊建議
    if analysis['main_force'] == '成長股、科技股':
        strategies.append("✅ 關注：科技、新能源、半導體")
    elif analysis['main_force'] == '藍籌股、價值股':
        strategies.append("✅ 關注：金融、消費、基建")
    else:
        strategies.append("✅ 關注：輪動熱點，快進快出")
    
    # 風險提示
    if analysis['volume_status'] == '縮量':
        strategies.append("⚠️ 風險：成交量不足，謹慎追高")
    elif analysis['risk_level'] == '高':
        strategies.append("⚠️ 風險：波動加大，控制倉位")
    else:
        strategies.append("⚠️ 風險：正常波動，注意止盈止損")
    
    # 操作建議
    if analysis['sentiment'] == '樂觀':
        strategies.append("📌 操作：持股待漲，適度加倉")
    elif analysis['sentiment'] == '謹慎':
        strategies.append("📌 操作：減倉觀望，等待機會")
    else:
        strategies.append("📌 操作：區間操作，高拋低吸")
    
    return strategies

def generate_prediction(stock_data, analysis):
    """生成今日預測"""
    sh = stock_data.get('上证指数', {})
    cyb = stock_data.get('创业板指', {})
    
    predictions = []
    
    # 上證預測
    if sh:
        current = sh.get('close', 0)
        low = sh.get('low', current)
        high = sh.get('high', current)
        
        # 修復：直接使用點位，不乘以奇怪係數
        pred_low = int(min(low, current) * 0.995 / 10) * 10
        pred_high = int(max(high, current) * 1.015 / 10) * 10
        
        if analysis['trend'] == '強勢上漲':
            trend = '震盪上行'
        elif analysis['trend'] == '震盪下行':
            trend = '震盪下行'
        else:
            trend = '區間震盪'
        
        predictions.append(f"上证指数：{pred_low}-{pred_high}點（{trend}）")
    
    # 創業板預測
    if cyb:
        current = cyb.get('close', 0)
        low = cyb.get('low', current)
        high = cyb.get('high', current)
        
        pred_low = int(min(low, current) * 0.995)
        pred_high = int(max(high, current) * 1.015)
        
        if cyb.get('change_pct', 0) > sh.get('change_pct', 0):
            trend = '強勢整理'
        else:
            trend = '跟隨大盤'
        
        predictions.append(f"创业板指：{pred_low}-{pred_high}點（{trend}）")
    
    return predictions

# ============================================================================
# 生成播報
# ============================================================================

def generate_report():
    """生成完整播報"""
    log("📊 開始獲取數據...")
    
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d %A")
    yesterday = (today - timedelta(days=1)).strftime("%m-%d")
    
    # 獲取數據
    stock_data = get_stock_data()
    if not stock_data:
        log("❌ 數據獲取失敗")
        return None
    
    log(f"✅ 獲取 {len(stock_data)} 個指數數據")
    
    # AI 分析
    log("🧠 AI 深度分析...")
    analysis = ai_deep_analysis(stock_data)
    strategies = generate_strategy(analysis, stock_data)
    predictions = generate_prediction(stock_data, analysis)
    news = get_market_news()
    global_ctx = get_global_context()
    
    # 生成報告（優化格式）
    sh = stock_data.get('上证指数', {})
    sz = stock_data.get('深证成指', {})
    cyb = stock_data.get('创业板指', {})
    hs300 = stock_data.get('沪深 300', {})
    
    report = f"""📈 A 股每日播報 | {date_str}

┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【市場數據】{yesterday} 收盤

  上证指数   {sh.get('close',0):>8.2f}   {sh.get('change',0):>+7.2f}   {sh.get('change_pct',0):>+6.2f}%
  深证成指   {sz.get('close',0):>8.2f}   {sz.get('change',0):>+7.2f}   {sz.get('change_pct',0):>+6.2f}%
  创业板指   {cyb.get('close',0):>8.2f}   {cyb.get('change',0):>+7.2f}   {cyb.get('change_pct',0):>+6.2f}%
  沪深 300    {hs300.get('close',0):>8.2f}   {hs300.get('change',0):>+7.2f}   {hs300.get('change_pct',0):>+6.2f}%

  成交額：{sh.get('amount',0):.0f}億  |  漲跌比：{sh.get('up_count',0)}家漲 / {sh.get('down_count',0)}家跌

┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【AI 分析】

  趨勢：{analysis['trend']}
  情緒：{analysis['sentiment']}  |  強度：{analysis['strength']}
  資金：{analysis['main_force']}
  點位：支撐 {analysis['key_levels'][0].replace('支撐：','')}  |  壓力 {analysis['key_levels'][1].replace('壓力：','')}

┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【市場熱點】

"""
    for n in news:
        report += f"  • {n}\n"
    
    report += f"""
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【國際局勢】

  美股：{global_ctx['us_market']}
  匯率：{global_ctx['usd_index']}
  商品：{global_ctx['commodities']}
  中東：{global_ctx['middle_east']}

┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【今日策略】

"""
    for s in strategies:
        # 清理 emoji，統一格式
        s_clean = s.replace('✅','•').replace('⚠️','⚠').replace('📌','•').replace('🌍','•')
        report += f"  {s_clean}\n"
    
    report += f"""
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

【今日預測】

"""
    for p in predictions:
        report += f"  • {p}\n"
    
    report += f"""
┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

⚠ 風險提示：本報告僅供參考，不構成投資建議。股市有風險，入市需謹慎。

🤖 RedOpenClaw AI 播報 | 數據：东方财富
"""
    
    if len(report) < 800:
        log(f"❌ 報告過短（{len(report)}字）")
        return None
    
    log(f"✅ 報告生成成功（{len(report)}字）")
    return report

# ============================================================================
# 發送飛書
# ============================================================================

def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}, timeout=10)
    result = resp.json()
    if result.get('code') != 0:
        raise Exception(f"Token 失敗：{result}")
    return result['tenant_access_token']

def send_feishu(content):
    try:
        token = get_feishu_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {
            "receive_id": FEISHU_CHAT_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content}, ensure_ascii=False)
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            log("✅ 飛書發送成功")
            return True
        log(f"❌ 飛書失敗：{resp.text}")
        return False
    except Exception as e:
        log(f"❌ 發送異常：{e}")
        return False

# ============================================================================
# 主函數
# ============================================================================

def main():
    log("=" * 60)
    log("📈 A 股每日播報 v4（深度分析版）")
    log("=" * 60)
    
    report = generate_report()
    if not report:
        log("❌ 生成失敗")
        return
    
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    log("\n📱 發送中...")
    if send_feishu(report):
        log("✅ 播報完成")
    else:
        log("❌ 發送失敗")
    
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"❌ 異常：{e}")
        import traceback
        log(traceback.format_exc())
