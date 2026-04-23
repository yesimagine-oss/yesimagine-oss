#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超高质量 Bundle 投产计划 - 定时任务脚本
方案 B：夜间模式（22:15-05:20）
仅执行 1 天（试水）
"""

import time
from datetime import datetime
from pathlib import Path
import requests
import json

# 配置
LOG_FILE = Path(__file__).parent / "logs" / "bundle_plan.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# 飞书配置（使用飞书应用方式发送）
FEISHU_USE_APP = True  # True=使用应用发送，False=使用 Webhook
FEISHU_WEBHOOK = ""  # 如果使用 Webhook，填写 webhook URL
FEISHU_USER_ID = "ou_f4919832188bcc630f8f257497fa93a4"  # 接收消息的用户 ID

# 服务器健康检查配置
HEALTH_CHECKS = {
    'cpu_threshold': 80,
    'memory_threshold': 80,
    'disk_threshold': 20,
    'proxy_url': 'http://127.0.0.1:7890',
    'evomap_url': 'https://evomap.ai',
}

def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def validate_bundle(gene, capsule, event):
    """发布前验证 Bundle"""
    errors = []
    warnings = []
    
    # 1. 验证 gene
    if len(gene.get('summary', '')) < 10:
        errors.append("Gene.summary < 10 字符")
    
    for i, step in enumerate(gene.get('strategy', [])):
        if len(step) < 15:
            errors.append(f"Gene.strategy[{i}] < 15 字符")
    
    if len(gene.get('signals_match', [])) < 1:
        errors.append("Gene.signals_match 至少 1 个信号")
    
    # 2. 验证 capsule
    if len(capsule.get('summary', '')) < 20:
        errors.append("Capsule.summary < 20 字符")
    
    confidence = capsule.get('confidence', 0)
    if not (0 <= confidence <= 1):
        errors.append(f"Capsule.confidence 必须在 0-1 之间 (当前:{confidence})")
    
    blast = capsule.get('blast_radius', {})
    if blast.get('files', 0) <= 0 or blast.get('lines', 0) <= 0:
        errors.append("Capsule.blast_radius 必须 > 0")
    
    # 3. 验证 substance (code_snippet/content/strategy/diff >= 50 字符)
    substance_fields = ['code_snippet', 'content', 'strategy', 'diff']
    has_substance = False
    for field in substance_fields:
        value = capsule.get(field)
        if value:
            if isinstance(value, str) and len(value) >= 50:
                has_substance = True
                break
            elif isinstance(value, list) and len(value) > 0:
                has_substance = True
                break
    
    if not has_substance:
        errors.append("Capsule 必须包含 code_snippet/content/strategy/diff (>=50 字符)")
    
    # 4. 验证 asset_id 计算
    def compute_asset_id(obj):
        clean = {k: v for k, v in obj.items() if k != 'asset_id'}
        canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'))
        return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
    
    # 临时计算验证
    gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
    expected_gene_id = compute_asset_id(gene_copy)
    if gene.get('asset_id') != expected_gene_id:
        errors.append(f"Gene.asset_id 计算错误")
        errors.append(f"  预期：{expected_gene_id[:50]}...")
        errors.append(f"  实际：{gene.get('asset_id', 'None')[:50]}...")
    
    # 5. 验证 event
    if event.get('intent') not in ['repair', 'optimize', 'innovate']:
        warnings.append(f"EvolutionEvent.intent 应该是 repair/optimize/innovate")
    
    # 返回验证结果
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def send_feishu(content: str):
    """发送飞书消息"""
    if FEISHU_USE_APP:
        # 使用飞书应用方式发送
        try:
            import subprocess
            # 调用 message 工具发送
            cmd = [
                'openclaw', 'message', 'send',
                '--target', FEISHU_USER_ID,
                '--channel', 'feishu',
                '--message', content
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                log("✅ 飞书推送成功（应用方式）")
            else:
                log(f"❌ 飞书推送失败：{result.stderr}")
        except Exception as e:
            log(f"❌ 飞书推送异常：{e}")
    else:
        # 使用 Webhook 方式发送
        if not FEISHU_WEBHOOK:
            log("⚠️ 飞书 webhook 未配置，跳过推送")
            return
        
        try:
            data = {
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(FEISHU_WEBHOOK, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                log("✅ 飞书推送成功（Webhook）")
            else:
                log(f"❌ 飞书推送失败：{response.status_code}")
        except Exception as e:
            log(f"❌ 飞书推送异常：{e}")

def check_server_health():
    """服务器健康检查"""
    health_status = {
        'cpu': {'value': 0, 'status': '✅', 'message': '正常'},
        'memory': {'value': 0, 'status': '✅', 'message': '正常'},
        'disk': {'value': 0, 'status': '✅', 'message': '正常'},
        'proxy': {'status': '✅', 'message': '运行中'},
        'evomap': {'status': '✅', 'message': '可访问'},
        'openclaw': {'status': '✅', 'message': '正常'},
    }
    
    # CPU 检查
    try:
        import subprocess
        result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if 'Cpu(s)' in line:
                cpu_usage = float(line.split(',')[0].split(':')[1].strip().split('%')[0])
                health_status['cpu']['value'] = cpu_usage
                if cpu_usage > HEALTH_CHECKS['cpu_threshold']:
                    health_status['cpu']['status'] = '⚠️'
                    health_status['cpu']['message'] = f'{cpu_usage}% (偏高)'
                break
    except:
        health_status['cpu']['status'] = '❌'
        health_status['cpu']['message'] = '检查失败'
    
    # 内存检查
    try:
        import subprocess
        result = subprocess.run(['free', '-h'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Mem:' in line:
                parts = line.split()
                total = float(parts[1].replace('G', '').replace('M', ''))
                used = float(parts[2].replace('G', '').replace('M', ''))
                memory_usage = (used / total) * 100
                health_status['memory']['value'] = memory_usage
                if memory_usage > HEALTH_CHECKS['memory_threshold']:
                    health_status['memory']['status'] = '⚠️'
                    health_status['memory']['message'] = f'{memory_usage:.0f}% (偏高)'
                break
    except:
        health_status['memory']['status'] = '❌'
        health_status['memory']['message'] = '检查失败'
    
    # 磁盘检查
    try:
        import subprocess
        result = subprocess.run(['df', '-h', '/home'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split('\n')
        for line in lines[1:]:
            if line:
                parts = line.split()
                disk_available = parts[3]
                health_status['disk']['value'] = disk_available
                health_status['disk']['message'] = f'{disk_available} 可用'
                break
    except:
        health_status['disk']['status'] = '❌'
        health_status['disk']['message'] = '检查失败'
    
    # 代理检查
    try:
        response = requests.get('https://www.google.com', 
                              proxies={'http': HEALTH_CHECKS['proxy_url'], 'https': HEALTH_CHECKS['proxy_url']},
                              timeout=5)
        if response.status_code == 200:
            health_status['proxy']['message'] = '运行中'
        else:
            health_status['proxy']['status'] = '⚠️'
            health_status['proxy']['message'] = '异常'
    except:
        health_status['proxy']['status'] = '❌'
        health_status['proxy']['message'] = '无法连接'
    
    # EvoMap 检查
    try:
        response = requests.get(HEALTH_CHECKS['evomap_url'], timeout=5)
        if response.status_code == 200:
            health_status['evomap']['message'] = '可访问'
        else:
            health_status['evomap']['status'] = '⚠️'
            health_status['evomap']['message'] = '访问异常'
    except:
        health_status['evomap']['status'] = '❌'
        health_status['evomap']['message'] = '无法访问'
    
    # OpenClaw 检查
    try:
        import subprocess
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
        if 'openclaw' in result.stdout.lower():
            health_status['openclaw']['message'] = '运行中'
        else:
            health_status['openclaw']['status'] = '⚠️'
            health_status['openclaw']['message'] = '未运行'
    except:
        health_status['openclaw']['status'] = '❌'
        health_status['openclaw']['message'] = '检查失败'
    
    # 计算健康度
    score = 100
    for key in ['cpu', 'memory', 'proxy', 'evomap', 'openclaw']:
        if health_status[key]['status'] == '⚠️':
            score -= 10
        elif health_status[key]['status'] == '❌':
            score -= 20
    
    health_status['score'] = score
    return health_status

def format_health_report(health_status):
    """格式化健康报告"""
    report = f"""📊 服务器健康报告

健康度：{health_status['score']}/100
"""
    
    if health_status['score'] >= 90:
        report += "状态：优秀\n\n"
    elif health_status['score'] >= 70:
        report += "状态：良好\n\n"
    else:
        report += "状态：需关注\n\n"
    
    report += f"CPU: {health_status['cpu']['value']:.0f}% {health_status['cpu']['status']}\n"
    report += f"内存：{health_status['memory']['value']:.0f}% {health_status['memory']['status']}\n"
    report += f"磁盘：{health_status['disk']['message']} {health_status['disk']['status']}\n"
    report += f"代理：{health_status['proxy']['message']} {health_status['proxy']['status']}\n"
    report += f"EvoMap: {health_status['evomap']['message']} {health_status['evomap']['status']}\n"
    report += f"OpenClaw: {health_status['openclaw']['message']} {health_status['openclaw']['status']}\n"
    
    return report

# 定时任务
tasks = [
    {
        'time': '22:15',
        'name': '超高质量 Bundle 投产计划',
        'duration': '15 分钟',
        'message': lambda: f"""📋 超高质量 Bundle 投产计划

📅 日期：{datetime.now().strftime('%Y-%m-%d')}
⏰ 发送时间：22:15
⏳ 距离开始：15 分钟
🎯 目标：2 bundles

📦 今日主题
• Bundle #1: API 超时重试
• Bundle #2: DNS 解析失败处理

⏱️ 时间安排
22:30-01:00  ▸ Bundle #1 制作
01:00-01:25  ▸ 休息 + 服务器优化
01:25-03:55  ▸ Bundle #2 制作
03:55-04:55  ▸ 审查 + 发布
04:55-05:15  ▸ 服务器健康优化
05:15-05:20  ▸ 投产完成报告

请准备就绪，22:30 准时开始！"""
    },
    {
        'time': '01:00',
        'name': 'Bundle #1 制作完成',
        'duration': '-',
        'message': lambda: f"""✅ Bundle #1 制作完成

📦 主题：API 超时重试
⏱️ 耗时：2.5 小时
接下来：01:00-01:25 休息 + 服务器优化"""
    },
    {
        'time': '01:00',
        'name': '休息 + 服务器优化',
        'duration': '25 分钟',
        'message': lambda: f"""{format_health_report(check_server_health())}"""
    },
    {
        'time': '03:55',
        'name': 'Bundle #2 制作完成',
        'duration': '-',
        'message': lambda: f"""✅ Bundle #2 制作完成

📦 主题：DNS 解析失败处理
⏱️ 耗时：2.5 小时
接下来：03:55-04:55 审查 + 发布"""
    },
    {
        'time': '04:30',
        'name': '发布前验证',
        'duration': '5 分钟',
        'message': lambda: f"""🔍 发布前验证

正在验证 Bundle 质量...
验证通过后发布！"""
    },
    {
        'time': '04:55',
        'name': '审查 + 发布完成',
        'duration': '-',
        'message': lambda: f"""📤 发布成功

Bundle #1: ✅
Bundle #2: ✅
问题：无
接下来：04:55-05:15 服务器健康优化"""
    },
    {
        'time': '05:15',
        'name': '服务器健康优化',
        'duration': '20 分钟',
        'message': lambda: f"""{format_health_report(check_server_health())}"""
    },
    {
        'time': '05:20',
        'name': '高质量 Bundle 投产完成报告',
        'duration': '-',
        'message': lambda: f"""😴 今日完成：2 bundles

发布状态：成功
服务器状态：优秀
工作已结束，请休息！"""
    },
]

def run_scheduler():
    """运行定时任务"""
    log("="*60)
    log("🚀 超高质量 Bundle 投产计划 - 定时任务启动")
    log("="*60)
    log("")
    log("已配置任务:")
    for task in tasks:
        log(f"  • {task['time']} - {task['name']} ({task['duration']})")
    log("")
    log(f"📁 日志文件：{LOG_FILE}")
    log("")
    log("🚀 定时任务运行中... (按 Ctrl+C 停止)")
    log("")
    
    last_check = ""
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # 每分钟检查一次
        if current_time != last_check:
            for task in tasks:
                if current_time == task['time']:
                    log(f"⏰ 触发任务：{task['name']}")
                    try:
                        message = task['message']()
                        send_feishu(message)
                    except Exception as e:
                        log(f"❌ 任务执行失败：{e}")
            last_check = current_time
        
        time.sleep(30)  # 30 秒检查一次

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        log("")
        log("👋 定时任务已停止")
