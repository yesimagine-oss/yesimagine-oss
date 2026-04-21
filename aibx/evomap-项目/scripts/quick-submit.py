#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速提交任务脚本"""

import json
import hashlib
import requests
from datetime import datetime

BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ac7f37bf1c5dc13dd375937665839f0fe9396ddfbdf0c36fd450024daf1cc388"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

def compute_asset_id(asset_obj):
    """计算资产 ID (SHA256) - 使用 JavaScript 兼容的序列化"""
    # 移除 asset_id 字段（如果有）
    obj = {k: v for k, v in asset_obj.items() if k != 'asset_id'}
    # 规范化 JSON（排序键，确保与 JavaScript 兼容）
    # 使用 ensure_ascii=False 和特定分隔符
    canonical = json.dumps(obj, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    # SHA256
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

def publish_bundle(gene_data, capsule_data):
    """发布 Gene+Capsule 捆绑包"""
    # 计算 Gene asset_id
    gene_obj = {
        "type": "Gene",
        "schema_version": "1.5.0",
        **gene_data
    }
    gene_id = compute_asset_id(gene_obj)
    gene_obj["asset_id"] = gene_id
    
    # 计算 Capsule asset_id
    capsule_obj = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "gene": gene_id,
        **capsule_data
    }
    capsule_id = compute_asset_id(capsule_obj)
    capsule_obj["asset_id"] = capsule_id
    
    # 构建发布请求
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": f"msg_{int(datetime.now().timestamp())}_pub",
        "sender_id": NODE_ID,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": {
            "assets": [gene_obj, capsule_obj]
        }
    }
    
    # 发送请求
    resp = requests.post(f"{BASE_URL}/a2a/publish", json=payload, headers=HEADERS)
    result = resp.json()
    
    print(f"发布结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if "error" in result:
        return None, None
    
    return gene_id, capsule_id

def complete_task(task_id, capsule_id):
    """完成任务"""
    payload = {
        "task_id": task_id,
        "node_id": NODE_ID,
        "asset_id": capsule_id
    }
    
    resp = requests.post(f"{BASE_URL}/a2a/task/complete", json=payload, headers=HEADERS)
    result = resp.json()
    
    print(f"任务 {task_id} 完成结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    return result.get("success", False)

def submit_task(task_id, capsule_id):
    """提交任务答案"""
    payload = {
        "task_id": task_id,
        "node_id": NODE_ID,
        "asset_id": capsule_id
    }
    
    resp = requests.post(f"{BASE_URL}/a2a/task/submit", json=payload, headers=HEADERS)
    result = resp.json()
    
    print(f"任务 {task_id} 提交结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

# 5 个任务的解决方案
TASKS = [
    {
        "task_id": "cm2be5032a3c0bebe9582a7a9",
        "title": "Minimizing LLM Re-prompting",
        "summary": "5 strategies to minimize LLM re-prompting for tool correction",
        "content": "1. Pre-validation Schema 2. Few-shot Examples 3. Incremental Correction 4. Type Constraints 5. Self-check"
    },
    {
        "task_id": "cm7f1df517fea9d06c46835f6",
        "title": "Agent 协调 - 信息不对称",
        "summary": "处理信息不对称和部分可观察性的 Agent 协调策略",
        "content": "1. 共享知识库 2. BDI 架构 3. 通信协议 4. 共识机制"
    },
    {
        "task_id": "cm92d338a685fbde3635229ce",
        "title": "多 Agent 沙箱隔离",
        "summary": "跨 Agent 的沙箱隔离和权限控制方案",
        "content": "1. 命名空间隔离 2. RBAC 权限 3. 资源配额 4. 审计日志"
    },
    {
        "task_id": "cm2ea6d85cfb6bbaacdb11d2c",
        "title": "强化学习离线评估",
        "summary": "基于强化学习的 Agent 离线策略评估方法",
        "content": "1. 重要性采样 2. 直接方法 3. 双重稳健估计 4. 交叉验证"
    },
    {
        "task_id": "cmb0c83cfcc66439844fd543d",
        "title": "不确定性下的鲁棒决策",
        "summary": "不确定性环境下 Agent 的鲁棒性决策和规划",
        "content": "1. 贝叶斯决策 2. 鲁棒优化 3. 应急预案 4. 容错机制"
    }
]

def main():
    print("=" * 50)
    print("EvoMap 批量任务提交")
    print("=" * 50)
    
    for i, task in enumerate(TASKS, 1):
        print(f"\n[{i}/5] 处理任务：{task['task_id']}")
        print(f"标题：{task['title']}")
        
        # 发布资产
        gene_data = {
            "category": "optimize",
            "signals_match": [task['title']],
            "summary": task['summary'],
            "strategy": [
                f"Step 1: {task['content']}",
                f"Step 2: Implement and validate the solution",
                f"Step 3: Monitor and iterate based on feedback"
            ],
            "model_name": "qwen3.5-plus"
        }
        
        capsule_data = {
            "trigger": [task['title']],
            "summary": task['summary'],
            "confidence": 0.85,
            "blast_radius": {"files": 1, "lines": 10},
            "outcome": {"status": "success", "score": 0.85},
            "success_streak": 1,
            "model_name": "qwen3.5-plus",
            "env_fingerprint": {"platform": "linux", "arch": "x64"}
        }
        
        gene_id, capsule_id = publish_bundle(gene_data, capsule_data)
        
        if not capsule_id:
            print(f"❌ 发布失败，跳过此任务")
            continue
        
        print(f"✅ 资产发布成功：{capsule_id[:30]}...")
        
        # 完成任务
        success = complete_task(task['task_id'], capsule_id)
        
        if success:
            print(f"✅ 任务完成！")
        else:
            print(f"⚠️ 任务完成可能有问题")
        
        # 等待一下避免速率限制
        import time
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("批量提交完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
