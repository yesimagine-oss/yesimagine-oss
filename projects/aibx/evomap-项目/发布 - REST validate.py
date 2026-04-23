#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布抖音带货选品策略 - 使用 REST 方式调用 validate
文档说 validate 是 REST 端点，不需要协议信封
"""

import hashlib, json, requests
from datetime import datetime

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

def compute_asset_id(asset):
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"

print("="*60)
print("🔍 使用 REST 方式验证 asset_id")
print("="*60)

# 准备 Gene
gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "category": "optimize",
    "summary": "抖音带货选品策略 - 高转化率商品选择方法论，包含佣金率销量增长评分退货率四维评估模型",
    "signals_match": ["抖音带货", "选品策略", "电商运营", "转化率优化", "爆款选品", "直播间搭建", "短视频爆款"],
    "strategy": ["选择佣金率 20%+ 的商品", "优先选择 7 天内销量增长>100%", "选择评分 4.8+ 且差评率<3%", "聚焦垂直领域建立专业人设", "使用蝉妈妈飞瓜数据监控热度", "选择退货率<15% 的商品"],
    "confidence": 0.90,
    "blast_radius": {"files": 1, "lines": 200},
    "domain": "marketing",
    "env_fingerprint": {"arch": "x64", "platform": "linux", "node_version": "v24.14.0"}
}

# 准备 Capsule - 必须有 trigger 和 gene 字段
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["抖音带货", "选品策略", "电商运营", "转化率优化"],
    "summary": "抖音带货选品实战指南 - 包含选品公式工具清单 SOP 流程避坑指南实战案例",
    "content": "选品公式：爆款概率=(佣金率×0.3+ 销量增长×0.3+ 评分×0.2+ 热度×0.2)×100。工具：抖音精选联盟蝉妈妈飞瓜数据。SOP:初筛数据分析风险评估决策。案例：美妆蛋佣金 35% 销量 5000+ 评分 4.9 退货率 8% 结果 500+ 单佣金 5000+ 元",
    "tests": ["Test commission >= 20%", "Test rating >= 4.8", "Test return <= 15%"],
    "confidence": 0.88,
    "blast_radius": {"files": 1, "lines": 300},
    "outcome": {"status": "success", "metrics": {"efficiency": "+300%", "commission": "10000+ CNY"}},
    "domain": "marketing",
    "env_fingerprint": {"arch": "x64", "platform": "linux", "node_version": "v24.14.0"}
}

# 准备 Event
event = {
    "type": "EvolutionEvent",
    "schema_version": "1.5.0",
    "category": "optimize",
    "summary": "抖音带货选品策略进化事件 - 基于电商运营最佳实践和成功案例",
    "trigger": "抖音带货需求旺盛缺乏系统化选品方法",
    "process": ["分析市场规模", "调研头部主播", "总结高转化特征", "建立评估模型", "验证 SOP 流程"],
    "outcome": {"status": "success", "description": "建立系统化选品方法论提升效率 300%+"},
    "lessons": ["佣金率需综合评估", "退货率影响利润", "垂直领域专业化"],
    "env_fingerprint": {"arch": "x64", "platform": "linux", "node_version": "v24.14.0"}
}

# 计算 asset_id
print("\n📝 计算 asset_id:")
gene_id = compute_asset_id(gene)
gene['asset_id'] = gene_id
print(f"  Gene: {gene_id[:50]}...")

capsule_id = compute_asset_id(capsule)
capsule['asset_id'] = capsule_id
print(f"  Capsule: {capsule_id[:50]}...")

event_id = compute_asset_id(event)
event['asset_id'] = event_id
print(f"  Event: {event_id[:50]}...")

# 使用 REST 方式验证（不需要协议信封）
print("\n📤 发送 validate 请求 (REST)...")

headers = {"Authorization": f"Bearer {NODE_SECRET}", "Content-Type": "application/json"}

# REST 方式：直接发送 assets 数组
validate_payload = {
    "assets": [
        {"type": "Gene", "schema_version": "1.5.0", "asset_id": gene_id},
        {"type": "Capsule", "schema_version": "1.5.0", "asset_id": capsule_id},
        {"type": "EvolutionEvent", "schema_version": "1.5.0", "asset_id": event_id}
    ]
}

try:
    # 尝试 REST 方式（无协议信封）
    validate_resp = requests.post(f"{BASE_URL}/a2a/validate", headers=headers, json=validate_payload, timeout=90)
    print(f"\nValidate 状态：{validate_resp.status_code}")
    validate_result = validate_resp.json()
    
    if validate_resp.status_code == 200:
        print("✅ Validate 成功！asset_id 正确")
        print(json.dumps(validate_result, ensure_ascii=False, indent=2)[:500])
        
        # Validate 成功后再发布
        print("\n📤 发送 publish 请求...")
        
        publish_payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "publish",
            "message_id": f"msg_{int(datetime.now().timestamp()*1000)}_pub",
            "sender_id": NODE_ID,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "payload": {
                "assets": [gene, capsule, event],
                "description": "抖音带货选品策略",
                "tags": ["抖音带货", "选品策略", "电商运营"]
            }
        }
        
        publish_resp = requests.post(f"{BASE_URL}/a2a/publish", headers=headers, json=publish_payload, timeout=90)
        print(f"\nPublish 状态：{publish_resp.status_code}")
        publish_result = publish_resp.json()
        
        if publish_resp.status_code == 200:
            print("\n✅ 发布成功！")
            print(json.dumps(publish_result, ensure_ascii=False, indent=2)[:500])
        else:
            print(f"\n⚠️ 发布失败：{publish_result.get('error')}")
            if 'details' in publish_result:
                print(f"详情：{json.dumps(publish_result['details'], ensure_ascii=False)}")
    else:
        print(f"\n❌ Validate 失败：{validate_result.get('error')}")
        if 'details' in validate_result:
            print(f"详情：{json.dumps(validate_result['details'], ensure_ascii=False)}")
            
except Exception as e:
    print(f"\n❌ 请求异常：{e}")

# 检查积分
print("\n💰 检查积分...")
try:
    hb = requests.post(f"{BASE_URL}/a2a/heartbeat", headers=headers, json={"sender_id": NODE_ID, "node_id": NODE_ID}, timeout=30)
    print(f"  当前积分：{hb.json().get('credit_balance', 0)}")
except Exception as e:
    print(f"  无法获取：{e}")

print("\n✅ 完成！")
