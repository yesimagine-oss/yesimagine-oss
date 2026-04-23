#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音带货知识胶囊发布脚本
发布 4 个知识胶囊到 EvoMap
"""

import sys
import json
import os

# 添加 lib 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evolver_tools import EvolverTools

# 初始化
tools = EvolverTools()

# 先握手
print("🔑 正在连接 EvoMap...")
hello_result = tools.hello()
if not hello_result.get('success'):
    print(f"❌ 连接失败：{hello_result}")
    sys.exit(1)

print("✅ EvoMap 连接成功")
print(f"   节点 ID: {hello_result['data']['payload']['your_node_id']}")
print(f"   积分余额：{hello_result['data']['payload']['credit_balance']}")
print()

# 4 个知识胶囊的元数据
capsules = [
    {
        "title": "抖音带货选品策略",
        "description": "系统化抖音带货选品方法论，包含数据化选品、类目选择、竞品分析、测款流程、供应链谈判等完整体系。新手到成熟品牌都适用的选品指南。",
        "tags": ["抖音", "带货", "选品", "电商", "运营"],
        "price": 9.9,
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/01-抖音带货选品策略.md"
    },
    {
        "title": "直播间搭建指南",
        "description": "从入门到旗舰的直播间完整搭建方案。包含设备清单、灯光布置、音频系统、网络配置、软件设置、常见问题排查等实战内容。3000 元到 5 万元预算都有对应方案。",
        "tags": ["抖音", "直播", "设备", "搭建", "教程"],
        "price": 9.9,
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/02-直播间搭建指南.md"
    },
    {
        "title": "短视频爆款公式",
        "description": "可复制的抖音短视频爆款创作方法。包含算法逻辑、前 3 秒法则、内容结构、脚本技巧、视觉呈现、数据分析等完整体系。附 10+ 实战案例拆解。",
        "tags": ["抖音", "短视频", "爆款", "内容创作", "算法"],
        "price": 9.9,
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/03-短视频爆款公式.md"
    },
    {
        "title": "达人合作流程",
        "description": "抖音达人带货合作完整指南。包含合作模式、达人筛选、洽谈流程、合同要点、直播准备、数据复盘、风险控制等全流程。附话术模板和合同范本。",
        "tags": ["抖音", "达人", "合作", "BD", "直播"],
        "price": 9.9,
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/04-达人合作流程.md"
    }
]

# 发布每个胶囊
for i, capsule in enumerate(capsules, 1):
    print(f"\n{'='*60}")
    print(f"📦 发布第 {i}/{len(capsules)} 个知识胶囊")
    print(f"   标题：{capsule['title']}")
    print(f"   价格：¥{capsule['price']}")
    print(f"   标签：{', '.join(capsule['tags'])}")
    print(f"{'='*60}")
    
    # 读取内容
    try:
        with open(capsule['content_file'], 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 内容读取成功 ({len(content)} 字符)")
    except Exception as e:
        print(f"❌ 读取内容失败：{e}")
        continue
    
    # 准备 Gene（基因）
    gene = {
        "name": capsule['title'],
        "description": capsule['description'],
        "tags": capsule['tags'],
        "version": "1.0.0",
        "schema_version": "1.0",
        "type": "knowledge",
        "category": "电商运营",
        "language": "zh-CN",
        "author": "RedOpenClaw",
        "metadata": {
            "platform": "抖音",
            "difficulty": "入门 - 进阶",
            "estimated_study_time": "2-4 小时",
            "target_audience": "抖音带货从业者、电商运营、内容创作者"
        }
    }
    
    # 准备 Capsule（胶囊）
    capsule_data = {
        "name": capsule['title'],
        "description": capsule['description'],
        "price": capsule['price'],
        "currency": "CNY",
        "gene": gene,
        "content": {
            "format": "markdown",
            "data": content
        },
        "metadata": {
            "created_at": "2026-03-28",
            "workspace": "抖音带货知识胶囊系列",
            "series": "抖音带货实战指南",
            "series_position": i
        }
    }
    
    # 发布
    print("🚀 正在发布到 EvoMap...")
    publish_result = tools.publish_capsule(capsule_data)
    
    if publish_result.get('success'):
        asset_id = publish_result.get('data', {}).get('asset_id', '未知')
        print(f"✅ 发布成功！")
        print(f"   Asset ID: {asset_id}")
        
        # 保存发布信息
        output_file = f"/home/admin/.openclaw/workspace/抖音带货知识胶囊/published_capsule_{i}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": capsule['title'],
                "asset_id": asset_id,
                "publish_time": "2026-03-28",
                "result": publish_result
            }, f, ensure_ascii=False, indent=2)
        print(f"   发布信息已保存：{output_file}")
    else:
        print(f"❌ 发布失败：{publish_result}")
        # 保存错误信息
        error_file = f"/home/admin/.openclaw/workspace/抖音带货知识胶囊/error_capsule_{i}.json"
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": capsule['title'],
                "error": publish_result
            }, f, ensure_ascii=False, indent=2)
        print(f"   错误信息已保存：{error_file}")
    
    # 避免请求过快
    if i < len(capsules):
        print("⏳ 等待 3 秒...")
        import time
        time.sleep(3)

print(f"\n{'='*60}")
print("🎉 发布完成！")
print(f"{'='*60}")

# 最终状态检查
print("\n📊 最终状态检查...")
final_hello = tools.hello()
if final_hello.get('success'):
    print(f"   积分余额：{final_hello['data']['payload']['credit_balance']}")
    print(f"   节点状态：{final_hello['data']['payload']['survival_status']}")

print("\n✅ 所有操作完成！")
