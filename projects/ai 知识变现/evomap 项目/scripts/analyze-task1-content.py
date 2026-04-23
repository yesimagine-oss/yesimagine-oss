#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析任务 1 资产内容是否触发限流
对比限流资产 vs 正常资产的特征差异
"""

import json
import requests

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

print("="*70)
print("任务 1 资产内容限流分析")
print("="*70)

# 1. 加载任务 1 资产
with open('/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/tasks/cm645252d3e74b79b97d4f5f7/gene.json', 'r') as f:
    gene = json.load(f)
with open('/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/tasks/cm645252d3e74b79b97d4f5f7/capsule.json', 'r') as f:
    capsule = json.load(f)

print("\n[1] 资产基本特征")
print(f"  Gene 大小：{len(json.dumps(gene))} 字节")
print(f"  Capsule 大小：{len(json.dumps(capsule))} 字节")
print(f"  信号数量：{len(gene.get('signals_match', []))}")
print(f"  信号列表：{gene.get('signals_match', [])}")

# 2. 分析敏感词
print("\n[2] 敏感词检测")
sensitive_keywords = [
    "spam", "abuse", "exploit", "hack", "attack",
    "adult", "nsfw", "violence", "hate", "harassment",
    "political", "controversial", "fake", "misinformation"
]

gene_text = json.dumps(gene).lower()
capsule_text = json.dumps(capsule).lower()

found_sensitive = []
for keyword in sensitive_keywords:
    if keyword in gene_text or keyword in capsule_text:
        found_sensitive.append(keyword)

if found_sensitive:
    print(f"  ⚠️ 发现敏感词：{found_sensitive}")
else:
    print(f"  ✅ 无敏感词")

# 3. 分析信号热度
print("\n[3] 信号热度分析")
print("  查询 Topic Heatmap 中各信号的热度...")

# 使用监控脚本的测试信号对比
test_signals = ["monitor", "health-check", "publish-test"]
task1_signals = gene.get('signals_match', [])

print(f"  监控测试信号：{test_signals} (冷门)")
print(f"  任务 1 信号：{task1_signals} (热门?)")

# 4. 测试不同信号的限流情况
print("\n[4] 信号限流对比测试")

def test_publish_with_signals(signals, label):
    """测试特定信号的发布请求"""
    test_gene = {
        "type": "Gene",
        "schema_version": "1.6.0",
        "category": "test",
        "signals_match": signals,
        "summary": f"测试信号限流 - {label}",
        "strategy": ["测试步骤 1", "测试步骤 2", "测试步骤 3", "测试步骤 4", "测试步骤 5"],
        "constraints": {"max_files": 1, "forbidden_paths": ["node_modules/"]},
        "validation": ["测试验证 1", "测试验证 2", "测试验证 3"]
    }
    
    url = "https://evomap.ai/a2a/publish"
    headers = {
        "Authorization": f"Bearer {NODE_SECRET}",
        "Content-Type": "application/json"
    }
    
    import hashlib
    import json
    from datetime import datetime
    
    def canonicalize(obj):
        if obj is None: return 'null'
        if isinstance(obj, bool): return 'true' if obj else 'false'
        if isinstance(obj, (int, float)): return str(obj)
        if isinstance(obj, str): return json.dumps(obj, ensure_ascii=False)
        if isinstance(obj, list): return '[' + ','.join(canonicalize(item) for item in obj) + ']'
        if isinstance(obj, dict):
            keys = sorted(obj.keys())
            pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
            return '{' + ','.join(pairs) + '}'
        return 'null'
    
    clean = {k: v for k, v in test_gene.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    test_gene['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
    
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": f"test_signal_{int(datetime.utcnow().timestamp()*1000)}",
        "sender_id": NODE_ID,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "payload": {"assets": [test_gene]}
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.status_code
    except:
        return 0

# 测试冷门信号
cold_status = test_publish_with_signals(
    ["monitor", "health-check", "endpoint-test", "system-verification", "ping"],
    "冷门信号"
)
print(f"  冷门信号测试：HTTP {cold_status}")

# 等待一下
import time
time.sleep(2)

# 测试任务 1 的信号
task1_status = test_publish_with_signals(
    task1_signals,
    "任务 1 信号"
)
print(f"  任务 1 信号测试：HTTP {task1_status}")

# 5. 分析内容长度
print("\n[5] 内容长度分析")
print(f"  Gene summary: {len(gene.get('summary', ''))} 字符")
print(f"  Capsule content: {len(capsule.get('content', ''))} 字符")
print(f"  Capsule code_snippet: {len(capsule.get('code_snippet', ''))} 字符")
print(f"  Capsule 总大小：{len(json.dumps(capsule))} 字节")

# 6. 分析特殊字段
print("\n[6] 特殊字段检测")
special_fields = ['env_fingerprint', 'success_streak', 'code_snippet', 'diff']
for field in special_fields:
    if field in capsule:
        print(f"  ⚠️ 包含 {field}: {len(json.dumps(capsule[field]))} 字节")
    else:
        print(f"  ✅ 无 {field}")

print("\n" + "="*70)
print("结论")
print("="*70)

if cold_status == 429 and task1_status == 429:
    print("❌ 两种信号都限流 → 不是内容问题，是时间窗口累积限流")
elif cold_status == 400 and task1_status == 429:
    print("⚠️ 任务 1 信号触发限流 → 可能是信号热度或内容问题")
elif cold_status == 400 and task1_status == 400:
    print("✅ 两种信号都不限流 → 当前时段空闲，之前是累积限流")
else:
    print(f"? 未知模式：cold={cold_status}, task1={task1_status}")

print("\n建议：")
print("1. 如果是累积限流 → 等待时间窗口过去（15-30 分钟）")
print("2. 如果是信号热度 → 使用冷门信号重新包装资产")
print("3. 如果是内容问题 → 移除敏感词或特殊字段")
print("="*70)
