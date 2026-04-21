#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应负载均衡器 - HTTP API 服务

提供 REST API 接口用于：
- Agent 管理
- 请求路由
- 指标导出
- 配置管理

运行:
    python3 http_api.py --port 8080
"""

import argparse
import json
import logging
from flask import Flask, request, jsonify, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2, RequestPriority

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 Flask 应用
app = Flask(__name__)

# 全局负载均衡器实例
lb: AdaptiveLoadBalancerV2 = None


def get_lb() -> AdaptiveLoadBalancerV2:
    """获取负载均衡器实例"""
    global lb
    if lb is None:
        lb = AdaptiveLoadBalancerV2()
    return lb


# ============ Agent 管理 ============

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """获取所有 Agent"""
    stats = get_lb().get_stats()
    return jsonify({
        "total": stats['total_agents'],
        "healthy": stats['healthy_agents'],
        "agents": stats['agents']
    })


@app.route('/api/agents', methods=['POST'])
def add_agent():
    """添加 Agent"""
    data = request.json
    
    if not data or 'agent_id' not in data or 'endpoint' not in data:
        return jsonify({"error": "Missing agent_id or endpoint"}), 400
    
    success = get_lb().add_agent(
        data['agent_id'],
        data['endpoint'],
        data.get('custom_factors')
    )
    
    if success:
        return jsonify({"status": "created", "agent_id": data['agent_id']}), 201
    else:
        return jsonify({"status": "exists", "agent_id": data['agent_id']}), 200


@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def remove_agent(agent_id):
    """移除 Agent"""
    success = get_lb().remove_agent(agent_id)
    
    if success:
        return jsonify({"status": "deleted", "agent_id": agent_id})
    else:
        return jsonify({"error": "Agent not found"}), 404


# ============ 请求路由 ============

@app.route('/api/select', methods=['POST'])
def select_agent():
    """选择最佳 Agent"""
    data = request.json or {}
    
    key = data.get('key')  # 用于一致性哈希
    priority_str = data.get('priority', 'NORMAL')
    
    # 解析优先级
    priority_map = {
        'LOW': RequestPriority.LOW,
        'NORMAL': RequestPriority.NORMAL,
        'HIGH': RequestPriority.HIGH,
        'CRITICAL': RequestPriority.CRITICAL
    }
    priority = priority_map.get(priority_str.upper(), RequestPriority.NORMAL)
    
    agent_id = get_lb().select_agent(key=key, priority=priority)
    
    if agent_id:
        agent = get_lb().agents[agent_id]
        return jsonify({
            "agent_id": agent_id,
            "endpoint": agent.endpoint,
            "weight": agent.weight,
            "score": agent.score,
            "status": agent.status.value
        })
    else:
        return jsonify({"error": "No healthy agents available"}), 503


@app.route('/api/record', methods=['POST'])
def record_request():
    """记录请求结果"""
    data = request.json
    
    if not data or 'agent_id' not in data or 'success' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    agent_id = data['agent_id']
    success = data['success']
    response_time = data.get('response_time', 0)
    
    get_lb().record_request(agent_id, success, response_time)
    
    return jsonify({"status": "recorded"})


# ============ 监控指标 ============

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus 指标"""
    return Response(generate_latest(get_lb().export_prometheus_metrics()),
                    mimetype=CONTENT_TYPE_LATEST)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    stats = get_lb().get_stats()
    return jsonify(stats)


@app.route('/api/scaling', methods=['GET'])
def get_scaling():
    """获取伸缩建议"""
    recommendation = get_lb().get_scaling_recommendation()
    return jsonify(recommendation)


# ============ 熔断器控制 ============

@app.route('/api/circuit/<agent_id>/reset', methods=['POST'])
def reset_circuit(agent_id):
    """重置 Agent 熔断器"""
    if agent_id not in get_lb().agents:
        return jsonify({"error": "Agent not found"}), 404
    
    get_lb().agents[agent_id].reset_circuit()
    return jsonify({"status": "reset", "agent_id": agent_id})


@app.route('/api/circuit/reset-all', methods=['POST'])
def reset_all_circuits():
    """重置所有熔断器"""
    get_lb().reset_circuit()
    return jsonify({"status": "all_reset"})


# ============ 健康检查 ============

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    stats = get_lb().get_stats()
    healthy = stats['healthy_agents'] > 0
    
    return jsonify({
        "status": "healthy" if healthy else "degraded",
        "agents": stats['total_agents'],
        "healthy_agents": stats['healthy_agents']
    }), 200 if healthy else 503


@app.route('/ready', methods=['GET'])
def ready():
    """就绪检查"""
    return jsonify({"status": "ready"}), 200


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(description='Adaptive Load Balancer HTTP API')
    parser.add_argument('--port', type=int, default=8080, help='HTTP 端口')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='监听地址')
    parser.add_argument('--qps-limit', type=float, default=100, help='QPS 限制')
    parser.add_argument('--circuit-threshold', type=float, default=0.3, help='熔断器阈值')
    
    args = parser.parse_args()
    
    # 初始化负载均衡器
    global lb
    lb = AdaptiveLoadBalancerV2(
        qps_limit=args.qps_limit,
        circuit_breaker_threshold=args.circuit_threshold
    )
    
    logger.info(f"启动 HTTP API 服务器：http://{args.host}:{args.port}")
    
    # 启动 Flask
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
