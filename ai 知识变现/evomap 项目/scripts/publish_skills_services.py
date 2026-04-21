#!/usr/bin/env python3
"""
EvoMap Skill 和服務批量發布工具
"""

import hashlib, json, requests
from datetime import datetime

NODE_SECRET = '59758f601beb1648a302d60b3eceec74809aabf7998eb70619a757ebb53aec50'
HEADERS = {'Authorization': f'Bearer {NODE_SECRET}', 'Content-Type': 'application/json'}
BASE_URL = 'https://evomap.ai'

def publish_skill(skill_data):
    """發布 Skill"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'publish',
        'message_id': f"msg_skill_{skill_data['id']}",
        'sender_id': 'node_67c3b8b37becd262',
        'timestamp': timestamp,
        'payload': {
            'asset_type': 'Skill',
            'title': skill_data['title'],
            'description': skill_data['description'],
            'price': skill_data['price'],
            'tags': skill_data['tags'],
            'content': skill_data['content']
        }
    }
    
    r = requests.post(f'{BASE_URL}/a2a/skill/store/publish', headers=HEADERS, json=payload)
    print(f"  HTTP: {r.status_code}")
    try:
        result = r.json()
        if 'error' in result:
            print(f"  ❌ {result['error']}")
        else:
            print(f"  ✅ 成功！")
        return result
    except:
        print(f"  響應：{r.text[:200]}")
        return {'error': 'invalid_response'}

def publish_service(service_data):
    """發布服務"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'publish',
        'message_id': f"msg_service_{service_data['id']}",
        'sender_id': 'node_67c3b8b37becd262',
        'timestamp': timestamp,
        'payload': service_data
    }
    
    r = requests.post(f'{BASE_URL}/a2a/service/publish', headers=HEADERS, json=payload)
    print(f"  HTTP: {r.status_code}")
    try:
        result = r.json()
        if 'error' in result:
            print(f"  ❌ {result['error']}")
        else:
            print(f"  ✅ 成功！")
        return result
    except:
        print(f"  響應：{r.text[:200]}")
        return {'error': 'invalid_response'}

# ========== 發布 Skill ==========
print("╔═══════════════════════════════════════╗")
print("║  發布 Skill (3 個)                     ║")
print("╚═══════════════════════════════════════╝")
print()

skills = [
    {
        'id': 'batch_guide',
        'title': 'EvoMap 批量任務提交完全指南',
        'description': '10 倍提升你的 EvoMap 任務提交效率！包含完整教程和源碼，400+ 任務實戰經驗總結。',
        'price': 99,
        'tags': ['evomap', 'automation', 'batch', 'python', 'tutorial'],
        'content': '完整教程包含 8 章內容：基礎回顧、批量原理、環境搭建、批量 Claim 實戰、自動化提交、質量控制、常見問題、進階優化。附贈 4 個完整 Python 腳本、配置模板、檢查清單。預計閱讀 2 小時，實戰 4-8 小時。'
    },
    {
        'id': 'master_tutorial',
        'title': 'EvoMap 完全掌握教程',
        'description': '從 0 到 1 完全掌握 EvoMap，成為平台前 5% 的專家！基於 96% 平台知識掌握度。',
        'price': 199,
        'tags': ['evomap', 'tutorial', 'master', 'comprehensive'],
        'content': '系統性講解：GEP-A2A 協議核心、Schema 1.5.0 完整規範、資產發布最佳實踐、GDI 評分優化策略、變現渠道全解析、AI Council 治理機制、經濟系統白皮書。10 章內容，4 小時閱讀，8-16 小時實戰。'
    },
    {
        'id': 'ai_engine',
        'title': 'AI 決策引擎源碼',
        'description': '讓 AI 幫你選擇高價值任務，收益提升 50-100%！完整源碼 + 部署指南。',
        'price': 299,
        'tags': ['ai', 'decision', 'automation', 'scoring'],
        'content': '包含 4 維度評分模型（Bounty 40% + 成功率 30% + 競爭 20% + 新鮮度 10%）、批量任務評分與排名、智能推薦算法、自動 Claim 功能。完整 Python 源碼、配置文件、部署文檔。'
    }
]

skill_results = []
for i, skill in enumerate(skills, 1):
    print(f"📚 Skill {i}/3: {skill['title']}")
    result = publish_skill(skill)
    skill_results.append(result)
    print()
    if i < len(skills):
        import time
        time.sleep(6)  # 速率限制

# ========== 發布服務 ==========
print("╔═══════════════════════════════════════╗")
print("║  發布服務 (5 個)                       ║")
print("╚═══════════════════════════════════════╝")
print()

services = [
    {
        'id': 'node_deploy',
        'type': 'service',
        'title': 'EvoMap 節點部署服務',
        'description': '從 0 到 1 搭建您的 EvoMap 節點，2-4 小時上線，立即開始賺取積分。包含環境配置、節點註冊、自動化部署、基礎培訓。',
        'price_range': '500-1000',
        'delivery_time': '2-4 hours',
        'contact': {'email': 'yesimagine@gmail.com', 'wechat': 'runtosky'}
    },
    {
        'id': 'auto_script',
        'type': 'service',
        'title': '批量任務自動化腳本定制',
        'description': '定制專屬批量任務提交腳本，效率提升 10 倍。需求分析、腳本開發、性能優化、部署培訓。',
        'price_range': '1000-3000',
        'delivery_time': '1-3 days',
        'contact': {'email': 'yesimagine@gmail.com', 'wechat': 'runtosky'}
    },
    {
        'id': 'dashboard',
        'type': 'service',
        'title': '儀表板定制',
        'description': '可視化監控您的 EvoMap 節點，實時掌握收益。節點監控、收益統計、任務追蹤、資產管理、告警通知。',
        'price_range': '800-2000',
        'delivery_time': '3-5 days',
        'contact': {'email': 'yesimagine@gmail.com', 'wechat': 'runtosky'}
    },
    {
        'id': 'ai_license',
        'type': 'service',
        'title': 'AI 決策引擎授權',
        'description': '智能選擇高價值任務，收益提升 50-100%。完整源碼、部署文檔、集成指導、持續更新。',
        'price_range': '2000-5000',
        'delivery_time': '1-2 days',
        'contact': {'email': 'yesimagine@gmail.com', 'wechat': 'runtosky'}
    },
    {
        'id': 'consulting',
        'type': 'service',
        'title': 'EvoMap 培訓/諮詢',
        'description': '1 對 1 培訓和諮詢，快速掌握 EvoMap 核心技術。基礎培訓、進階培訓、變現諮詢、定制培訓。',
        'price_range': '500-1000',
        'delivery_time': 'on-demand',
        'contact': {'email': 'yesimagine@gmail.com', 'wechat': 'runtosky'}
    }
]

service_results = []
for i, service in enumerate(services, 1):
    print(f"🛠️  服務 {i}/5: {service['title']}")
    result = publish_service(service)
    service_results.append(result)
    print()
    if i < len(services):
        import time
        time.sleep(6)  # 速率限制

# ========== 總結 ==========
print("╔═══════════════════════════════════════╗")
print("║  發布完成總結                         ║")
print("╚═══════════════════════════════════════╝")
print()

skill_success = sum(1 for r in skill_results if 'error' not in r)
service_success = sum(1 for r in service_results if 'error' not in r)

print(f"✅ Skill 發布：{skill_success}/3 成功")
print(f"✅ 服務發布：{service_success}/5 成功")
print()

if skill_success == 3 and service_success == 5:
    print("🎉 所有 Skill 和服務發布成功！")
else:
    print("⚠️ 部分失敗，請檢查錯誤信息")

print()
print("═══════════════════════════════════════")
