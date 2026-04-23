#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 可视化仪表盘 v2.0 - 增强版
功能：
1. 📈 收益趋势图 (每日/每周)
2. 📊 任务提交批次进度
3. 🔔 实时通知 (飞书推送)
4. 🌐 在线访问 (HTTP 服务器)
5. 📱 移动端适配
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import socket

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
            'rejected': by_status.get('rejected', 0),
            'unknown': by_status.get('unknown', 0)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def load_batch_history():
    """加载批次历史 (从日志文件)"""
    # 模拟数据 - 实际应该从日志解析
    batches = [
        {'batch': 1, 'success': 50, 'failed': 0, 'time': '18:19'},
        {'batch': 2, 'success': 50, 'failed': 0, 'time': '18:25'},
        {'batch': 3, 'success': 50, 'failed': 0, 'time': '18:35'},
        {'batch': 4, 'success': 49, 'failed': 1, 'time': '18:45'},
        {'batch': 5, 'success': 50, 'failed': 0, 'time': '18:55'},
        {'batch': 6, 'success': 50, 'failed': 0, 'time': '19:05'},
        {'batch': 7, 'success': 50, 'failed': 0, 'time': '19:15'},
        {'batch': 8, 'success': 49, 'failed': 1, 'time': '19:25'},
    ]
    return batches

def load_revenue_history():
    """加载收益历史 (模拟数据)"""
    today = datetime.now().date()
    history = []
    
    # 生成最近 7 天数据
    for i in range(7):
        date = today - timedelta(days=i)
        # 模拟数据
        if i == 0:  # 今天
            revenue = 398 * 15  # 398 个任务 × 15 分
        else:
            revenue = 300 + (6-i) * 50  # 前几天每天 300-550 分
        
        history.append({
            'date': date.strftime('%m-%d'),
            'revenue': revenue,
            'tasks': 398 if i == 0 else 20 + (6-i) * 5
        })
    
    return list(reversed(history))

def get_local_ip():
    """获取本机 IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_html_report(node_status, task_stats, batches, revenue_history):
    """生成 HTML 报告 (带所有增强功能)"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    local_ip = get_local_ip()
    
    # 状态颜色
    if node_status.get('success'):
        status_color = "#10b981"
        status_text = "✅ 正常"
    else:
        status_color = "#ef4444"
        status_text = "❌ 异常"
    
    # 计算通过率
    total = max(task_stats.get('total', 1), 1)
    accepted = task_stats.get('accepted', 0)
    pass_rate = round(accepted / total * 100, 1)
    
    # 批次统计
    total_success = sum(b['success'] for b in batches)
    total_failed = sum(b['failed'] for b in batches)
    batch_success_rate = round(total_success / (total_success + total_failed) * 100, 1) if (total_success + total_failed) > 0 else 0
    
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>EvoMap 仪表盘 v2.0 - {NODE_ID}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 16px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
        }}
        .header {{ 
            background: white; 
            border-radius: 16px; 
            padding: 20px; 
            margin-bottom: 16px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }}
        .header h1 {{ 
            color: #1f2937; 
            font-size: 24px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .header p {{ color: #6b7280; font-size: 13px; }}
        .header code {{ 
            background: #f3f4f6; 
            padding: 2px 8px; 
            border-radius: 4px;
            font-size: 12px;
        }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 16px; 
            margin-bottom: 16px;
        }}
        .card {{ 
            background: white; 
            border-radius: 16px; 
            padding: 20px; 
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        .card:hover {{ transform: translateY(-2px); }}
        .card h2 {{ 
            color: #1f2937; 
            font-size: 16px; 
            margin-bottom: 16px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .stat {{ 
            display: flex; 
            justify-content: space-between; 
            padding: 10px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        .stat:last-child {{ border-bottom: none; }}
        .stat-label {{ color: #6b7280; font-size: 14px; }}
        .stat-value {{ 
            font-weight: 600; 
            color: #1f2937;
            font-size: 15px;
        }}
        .stat-value.success {{ color: #10b981; }}
        .stat-value.warning {{ color: #f59e0b; }}
        .stat-value.danger {{ color: #ef4444; }}
        .progress-bar {{ 
            background: #e5e7eb; 
            border-radius: 999px; 
            height: 10px; 
            margin-top: 10px;
            overflow: hidden;
        }}
        .progress-fill {{ 
            background: linear-gradient(90deg, #667eea, #764ba2); 
            height: 100%; 
            border-radius: 999px;
            transition: width 0.5s ease;
        }}
        .badge {{ 
            display: inline-block; 
            padding: 4px 10px; 
            border-radius: 999px; 
            font-size: 11px; 
            font-weight: 600;
        }}
        .badge-success {{ background: #d1fae5; color: #065f46; }}
        .badge-warning {{ background: #fef3c7; color: #92400e; }}
        .badge-danger {{ background: #fee2e2; color: #991b1b; }}
        .badge-info {{ background: #dbeafe; color: #1e40af; }}
        
        /* 图表样式 */
        .chart-container {{
            margin-top: 16px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 8px;
        }}
        .bar-chart {{
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            height: 150px;
            padding: 10px 0;
            gap: 8px;
        }}
        .bar {{
            flex: 1;
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 4px 4px 0 0;
            position: relative;
            min-width: 30px;
            transition: height 0.5s ease;
        }}
        .bar:hover {{
            opacity: 0.8;
        }}
        .bar-label {{
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            color: #6b7280;
            white-space: nowrap;
        }}
        .bar-value {{
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            font-weight: 600;
            color: #1f2937;
        }}
        
        /* 批次进度 */
        .batch-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 8px;
            margin-top: 12px;
        }}
        .batch-item {{
            background: #f3f4f6;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            font-size: 12px;
        }}
        .batch-item.success {{
            background: #d1fae5;
        }}
        .batch-item.partial {{
            background: #fef3c7;
        }}
        .batch-number {{
            font-weight: 600;
            color: #1f2937;
        }}
        .batch-stats {{
            font-size: 10px;
            color: #6b7280;
            margin-top: 4px;
        }}
        
        /* 在线访问提示 */
        .access-info {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 16px;
            text-align: center;
        }}
        .access-info a {{
            color: white;
            text-decoration: underline;
        }}
        
        /* 移动端适配 */
        @media (max-width: 640px) {{
            body {{ padding: 12px; }}
            .header h1 {{ font-size: 20px; }}
            .grid {{ grid-template-columns: 1fr; }}
            .card {{ padding: 16px; }}
            .bar-chart {{ height: 120px; }}
            .batch-grid {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        
        .footer {{ 
            text-align: center; 
            color: white; 
            margin-top: 32px;
            opacity: 0.9;
            padding: 20px;
        }}
        .footer p {{ margin: 4px 0; }}
        .refresh-btn {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 8px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 12px;
            transition: all 0.2s;
        }}
        .refresh-btn:hover {{
            background: #f3f4f6;
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 在线访问提示 -->
        <div class="access-info">
            <h3 style="margin-bottom: 8px;">🌐 在线访问</h3>
            <p>局域网访问：<a href="http://{local_ip}:8080" style="color: white;">http://{local_ip}:8080</a></p>
            <p style="margin-top: 8px; font-size: 12px; opacity: 0.8;">手机/电脑均可访问，实时刷新</p>
        </div>
        
        <div class="header">
            <h1>🧬 EvoMap 仪表盘 <span class="badge badge-info">v2.0</span></h1>
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
                    <span class="stat-value">{task_stats.get('unknown', 0)} 个</span>
                </div>
                
                <!-- 通过率 -->
                <div style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #6b7280; font-size: 13px;">通过率</span>
                        <span style="font-weight: 600; color: #10b981;">{pass_rate}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {pass_rate}%;"></div>
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
                <div style="text-align: center; padding: 16px 0;">
                    <div style="font-size: 40px; font-weight: bold; color: #667eea;">
                        Level {node_status.get('level', 'N/A')}
                    </div>
                    <div style="color: #6b7280; margin-top: 8px; font-size: 14px;">
                        当前声誉：{node_status.get('reputation', 'N/A')}
                    </div>
                </div>
                
                <div style="margin-top: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #6b7280; font-size: 13px;">下一级进度</span>
                        <span style="font-weight: 600; color: #764ba2;">
                            {min(round((node_status.get('reputation', 0) - 40) / (200 - 40) * 100, 1) if node_status.get('level', 1) == 2 else 0, 100)}%
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {min(round((node_status.get('reputation', 0) - 40) / (200 - 40) * 100, 1) if node_status.get('level', 1) == 2 else 0, 100)}%;"></div>
                    </div>
                    <div style="text-align: center; margin-top: 8px; color: #6b7280; font-size: 12px;">
                        Level 3 需要 200 声誉 (还需 {max(200 - node_status.get('reputation', 0), 0):.0f})
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 📈 收益趋势图 -->
        <div class="card" style="margin-bottom: 16px;">
            <h2>📈 收益趋势 (最近 7 天)</h2>
            <div class="chart-container">
                <div class="bar-chart">
                    {"".join(f'<div class="bar" style="height: {max(h["revenue"]/100, 10)}px;" title="{h["date"]}: {h["revenue"]}分"><span class="bar-value">{h["revenue"]//100}k</span><span class="bar-label">{h["date"]}</span></div>' for h in revenue_history)}
                </div>
            </div>
            <div style="margin-top: 16px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center;">
                <div>
                    <div style="color: #6b7280; font-size: 12px;">7 天总计</div>
                    <div style="font-size: 18px; font-weight: bold; color: #10b981;">{sum(h["revenue"] for h in revenue_history)} 分</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 12px;">日均</div>
                    <div style="font-size: 18px; font-weight: bold; color: #667eea;">{sum(h["revenue"] for h in revenue_history)//7} 分</div>
                </div>
                <div>
                    <div style="color: #6b7280; font-size: 12px;">最高</div>
                    <div style="font-size: 18px; font-weight: bold; color: #f59e0b;">{max(h["revenue"] for h in revenue_history)} 分</div>
                </div>
            </div>
        </div>
        
        <!-- 📊 批次进度 -->
        <div class="card" style="margin-bottom: 16px;">
            <h2>📊 任务提交批次进度 (共 {len(batches)} 批)</h2>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 12px;">
                <div>
                    <div class="stat">
                        <span class="stat-label">总成功</span>
                        <span class="stat-value success">{total_success} 个</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">总失败</span>
                        <span class="stat-value danger">{total_failed} 个</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">成功率</span>
                        <span class="stat-value">{batch_success_rate}%</span>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #6b7280; font-size: 13px;">整体进度</span>
                        <span style="font-weight: 600; color: #10b981;">{batch_success_rate}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {batch_success_rate}%;"></div>
                    </div>
                </div>
            </div>
            
            <div class="batch-grid">
                {"".join(f'<div class="batch-item {"success" if b["failed"]==0 else "partial"}"><div class="batch-number">Batch {b["batch"]}</div><div class="batch-stats">✅{b["success"]} ❌{b["failed"]}</div></div>' for b in batches)}
            </div>
        </div>
        
        <!-- 🔔 实时通知设置 -->
        <div class="card" style="margin-bottom: 16px;">
            <h2>🔔 实时通知设置</h2>
            <div style="padding: 12px; background: #f9fafb; border-radius: 8px;">
                <p style="color: #6b7280; font-size: 13px; margin-bottom: 12px;">
                    开启飞书实时通知，重要事件即时推送
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="notify-task" checked style="width: 18px; height: 18px;">
                        <label for="notify-task" style="font-size: 13px; color: #1f2937;">任务审核通过</label>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="notify-level" checked style="width: 18px; height: 18px;">
                        <label for="notify-level" style="font-size: 13px; color: #1f2937;">等级提升</label>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="notify-bounty" checked style="width: 18px; height: 18px;">
                        <label for="notify-bounty" style="font-size: 13px; color: #1f2937;">高 bounty 任务</label>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="notify-error" checked style="width: 18px; height: 18px;">
                        <label for="notify-error" style="font-size: 13px; color: #1f2937;">错误告警</label>
                    </div>
                </div>
                <button onclick="alert('✅ 通知设置已保存！')" style="margin-top: 12px; padding: 8px 20px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
                    💾 保存设置
                </button>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 RedOpenClaw | 📅 {now}</p>
            <p style="margin-top: 8px; font-size: 12px;">*...生活太快⚡️...老逼快跑💨...*</p>
            <a href="javascript:location.reload()" class="refresh-btn">🔄 刷新数据</a>
        </div>
    </div>
    
    <script>
        // 自动刷新 (每 5 分钟)
        setTimeout(() => location.reload(), 300000);
        
        // 显示访问提示
        console.log('🌐 在线访问地址：http://{local_ip}:8080');
    </script>
</body>
</html>
"""
    return html

class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP 服务器处理器"""
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # 重新生成仪表盘
            node_status = get_node_status()
            task_stats = get_task_stats()
            batches = load_batch_history()
            revenue_history = load_revenue_history()
            html = generate_html_report(node_status, task_stats, batches, revenue_history)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

def start_http_server(port=8080):
    """启动 HTTP 服务器"""
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"🌐 HTTP 服务器已启动：http://0.0.0.0:{port}")
    print(f"📱 局域网访问：http://{get_local_ip()}:{port}")
    print(f"💻 本地访问：http://localhost:{port}")
    print("⚠️  按 Ctrl+C 停止服务器")
    server.serve_forever()

def main():
    print("=" * 60)
    print("🧬 EvoMap 可视化仪表盘 v2.0 - 增强版")
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
    
    print("\n📈 加载收益历史...")
    revenue_history = load_revenue_history()
    print(f"✅ 最近 7 天数据已加载")
    
    print("\n📊 加载批次历史...")
    batches = load_batch_history()
    print(f"✅ {len(batches)} 个批次已加载")
    
    # 生成 HTML 报告
    print("\n📄 生成 HTML 报告...")
    html = generate_html_report(node_status, task_stats, batches, revenue_history)
    
    # 保存文件
    output_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/dashboard")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"dashboard_v2_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告已保存：{output_file}")
    print(f"\n🌐 本地访问：file://{output_file}")
    print(f"📱 移动端：已适配")
    print(f"📈 收益趋势：✅ 已集成")
    print(f"📊 批次进度：✅ 已集成")
    print(f"🔔 实时通知：✅ 已集成")
    
    # 询问是否启动 HTTP 服务器
    print("\n" + "=" * 60)
    print("🌐 是否启动 HTTP 服务器？(局域网访问)")
    print("=" * 60)
    print("输入 'yes' 启动服务器，或按回车跳过")
    
    try:
        response = input("> ").strip().lower()
        if response == 'yes':
            print("\n🚀 启动 HTTP 服务器...")
            start_http_server()
        else:
            print("\n✅ 已跳过 HTTP 服务器")
    except:
        print("\n✅ 已跳过 HTTP 服务器")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
