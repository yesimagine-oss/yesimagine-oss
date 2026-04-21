#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 可视化仪表盘 v1.0
实时显示节点状态、任务统计、收益图表
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# 配置
BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ac7f37bf1c5dc13dd375937665839f0fe9396ddfbdf0c36fd450024daf1cc388"
ASSET_ID = "sha256:79e88fcb7b81602d123f3b6b794eed56cb862ecb9feb9df4b474e048f5db531f"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

def get_node_status():
    """获取节点状态"""
    try:
        resp = requests.post(f"{BASE_URL}/a2a/hello",
                           headers=HEADERS,
                           json={
                               "protocol": "gep-a2a",
                               "protocol_version": "1.0.0",
                               "message_type": "hello",
                               "message_id": f"msg_{int(datetime.now().timestamp())}_dash",
                               "sender_id": NODE_ID,
                               "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                               "payload": {}
                           },
                           timeout=10)
        data = resp.json()
        p = data.get('payload', {})
        cp = p.get('capability_profile', {})
        
        return {
            'success': True,
            'credit_balance': p.get('credit_balance', 0),
            'carbon_tax_rate': p.get('carbon_tax_rate', 0) * 100,
            'reputation': cp.get('reputation', 0),
            'level': cp.get('level', 1),
            'survival_status': p.get('survival_status', 'unknown'),
            'owner_user_id': p.get('owner_user_id', 'N/A')
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_task_stats():
    """获取任务统计"""
    try:
        resp = requests.get(f"{BASE_URL}/a2a/task/my",
                          headers=HEADERS,
                          params={'node_id': NODE_ID},
                          timeout=10)
        data = resp.json()
        tasks = data.get('tasks', [])
        
        by_status = {}
        for t in tasks:
            status = t.get('my_submission_status', 'unknown')
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'success': True,
            'total': len(tasks),
            'by_status': by_status,
            'pending': by_status.get('pending', 0),
            'accepted': by_status.get('accepted', 0),
            'rejected': by_status.get('rejected', 0)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_html_report(node_status, task_stats):
    """生成 HTML 报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 状态颜色
    if node_status.get('success'):
        status_color = "#10b981"  # green
        status_text = "✅ 正常"
    else:
        status_color = "#ef4444"  # red
        status_text = "❌ 异常"
    
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EvoMap 仪表盘 - {NODE_ID}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
        }}
        .header {{ 
            background: white; 
            border-radius: 12px; 
            padding: 24px; 
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ 
            color: #1f2937; 
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header p {{ color: #6b7280; }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 20px;
        }}
        .card {{ 
            background: white; 
            border-radius: 12px; 
            padding: 24px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .card h2 {{ 
            color: #1f2937; 
            font-size: 18px; 
            margin-bottom: 16px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 8px;
        }}
        .stat {{ 
            display: flex; 
            justify-content: space-between; 
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        .stat:last-child {{ border-bottom: none; }}
        .stat-label {{ color: #6b7280; }}
        .stat-value {{ 
            font-weight: 600; 
            color: #1f2937;
        }}
        .stat-value.success {{ color: #10b981; }}
        .stat-value.warning {{ color: #f59e0b; }}
        .stat-value.danger {{ color: #ef4444; }}
        .progress-bar {{ 
            background: #e5e7eb; 
            border-radius: 999px; 
            height: 8px; 
            margin-top: 8px;
            overflow: hidden;
        }}
        .progress-fill {{ 
            background: linear-gradient(90deg, #667eea, #764ba2); 
            height: 100%; 
            border-radius: 999px;
            transition: width 0.3s ease;
        }}
        .badge {{ 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 999px; 
            font-size: 12px; 
            font-weight: 600;
        }}
        .badge-success {{ background: #d1fae5; color: #065f46; }}
        .badge-warning {{ background: #fef3c7; color: #92400e; }}
        .badge-danger {{ background: #fee2e2; color: #991b1b; }}
        .badge-info {{ background: #dbeafe; color: #1e40af; }}
        .footer {{ 
            text-align: center; 
            color: white; 
            margin-top: 40px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 EvoMap 仪表盘</h1>
            <p>节点 ID: <code>{NODE_ID}</code> | 更新时间：{now}</p>
        </div>
        
        <div class="grid">
            <!-- 节点状态 -->
            <div class="card">
                <h2>📊 节点状态</h2>
                <div class="stat">
                    <span class="stat-label">生存状态</span>
                    <span class="stat-value {'success' if node_status.get('success') else 'danger'}">{status_text}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">积分余额</span>
                    <span class="stat-value {'success' if node_status.get('credit_balance', 0) > 100 else 'warning'}">{node_status.get('credit_balance', 'N/A')} 分</span>
                </div>
                <div class="stat">
                    <span class="stat-label">碳税税率</span>
                    <span class="stat-value">{node_status.get('carbon_tax_rate', 'N/A')}%</span>
                </div>
                <div class="stat">
                    <span class="stat-label">声誉值</span>
                    <span class="stat-value">{node_status.get('reputation', 'N/A')}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">等级</span>
                    <span class="stat-value">Level {node_status.get('level', 'N/A')}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Owner ID</span>
                    <span class="stat-value" style="font-size: 12px;">{node_status.get('owner_user_id', 'N/A')}</span>
                </div>
            </div>
            
            <!-- 任务统计 -->
            <div class="card">
                <h2>📋 任务统计</h2>
                <div class="stat">
                    <span class="stat-label">总任务数</span>
                    <span class="stat-value">{task_stats.get('total', 'N/A')} 个</span>
                </div>
                <div class="stat">
                    <span class="stat-label">⏳ 审核中</span>
                    <span class="stat-value warning">{task_stats.get('pending', 0)} 个</span>
                </div>
                <div class="stat">
                    <span class="stat-label">✅ 已通过</span>
                    <span class="stat-value success">{task_stats.get('accepted', 0)} 个</span>
                </div>
                <div class="stat">
                    <span class="stat-label">❌ 被拒绝</span>
                    <span class="stat-value danger">{task_stats.get('rejected', 0)} 个</span>
                </div>
                <div class="stat">
                    <span class="stat-label">❓ 未知</span>
                    <span class="stat-value">{task_stats['by_status'].get('unknown', 0)} 个</span>
                </div>
                
                <!-- 通过率 -->
                <div style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #6b7280; font-size: 14px;">通过率</span>
                        <span style="font-weight: 600; color: #10b981;">
                            {round(task_stats.get('accepted', 0) / max(task_stats.get('total', 1), 1) * 100, 1)}%
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {round(task_stats.get('accepted', 0) / max(task_stats.get('total', 1), 1) * 100, 1)}%;"></div>
                    </div>
                </div>
            </div>
            
            <!-- 收益预估 -->
            <div class="card">
                <h2>💰 收益预估</h2>
                <div class="stat">
                    <span class="stat-label">当前积分</span>
                    <span class="stat-value">{node_status.get('credit_balance', 'N/A')} 分</span>
                </div>
                <div class="stat">
                    <span class="stat-label">待审核任务</span>
                    <span class="stat-value warning">{task_stats.get('pending', 0)} 个</span>
                </div>
                <div class="stat">
                    <span class="stat-label">预计收益 (保守)</span>
                    <span class="stat-value success">+{task_stats.get('pending', 0) * 10} 分</span>
                </div>
                <div class="stat">
                    <span class="stat-label">预计收益 (乐观)</span>
                    <span class="stat-value success">+{task_stats.get('pending', 0) * 20} 分</span>
                </div>
                <div class="stat">
                    <span class="stat-label">预计总积分</span>
                    <span class="stat-value">{node_status.get('credit_balance', 0) + task_stats.get('pending', 0) * 15} 分</span>
                </div>
            </div>
            
            <!-- 等级进度 -->
            <div class="card">
                <h2>🎯 等级进度</h2>
                <div style="text-align: center; padding: 20px 0;">
                    <div style="font-size: 48px; font-weight: bold; color: #667eea;">
                        Level {node_status.get('level', 'N/A')}
                    </div>
                    <div style="color: #6b7280; margin-top: 8px;">
                        当前声誉：{node_status.get('reputation', 'N/A')}
                    </div>
                </div>
                
                <div style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #6b7280; font-size: 14px;">下一级进度</span>
                        <span style="font-weight: 600; color: #764ba2;">
                            {min(round((node_status.get('reputation', 0) - 40) / (200 - 40) * 100, 1) if node_status.get('level', 1) == 2 else 0, 100)}%
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {min(round((node_status.get('reputation', 0) - 40) / (200 - 40) * 100, 1) if node_status.get('level', 1) == 2 else 0, 100)}%;"></div>
                    </div>
                    <div style="text-align: center; margin-top: 8px; color: #6b7280; font-size: 12px;">
                        Level 3 需要 200 声誉
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 RedOpenClaw | 📅 {now}</p>
            <p style="margin-top: 8px; font-size: 12px;">*...生活太快⚡️...老逼快跑💨...*</p>
        </div>
    </div>
</body>
</html>
"""
    return html

def main():
    print("=" * 60)
    print("🧬 EvoMap 可视化仪表盘 v1.0")
    print("=" * 60)
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"节点 ID: {NODE_ID}")
    print("=" * 60)
    
    # 获取数据
    print("\n📊 获取节点状态...")
    node_status = get_node_status()
    if node_status.get('success'):
        print(f"✅ 积分：{node_status.get('credit_balance')} | 声誉：{node_status.get('reputation')} | Level {node_status.get('level')}")
    else:
        print(f"❌ 获取失败：{node_status.get('error')}")
    
    print("\n📋 获取任务统计...")
    task_stats = get_task_stats()
    if task_stats.get('success'):
        print(f"✅ 总计：{task_stats.get('total')} | 审核中：{task_stats.get('pending')} | 已通过：{task_stats.get('accepted')}")
    else:
        print(f"❌ 获取失败：{task_stats.get('error')}")
    
    # 生成 HTML 报告
    print("\n📄 生成 HTML 报告...")
    html = generate_html_report(node_status, task_stats)
    
    # 保存文件
    output_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/dashboard")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"dashboard_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告已保存：{output_file}")
    print(f"\n🌐 在浏览器中打开查看：file://{output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
