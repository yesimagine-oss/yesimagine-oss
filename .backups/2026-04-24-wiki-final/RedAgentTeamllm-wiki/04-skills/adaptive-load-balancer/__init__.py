#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptive Load Balancer Skill - 主模块

提供负载均衡器的统一接口和配置管理。
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Optional

# 导入核心实现
from .adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2, RequestPriority, AgentStatus

# 日志配置
logger = logging.getLogger(__name__)

# 全局实例
_instance: Optional[AdaptiveLoadBalancerV2] = None
_config: Optional[Dict] = None


def get_config() -> Dict:
    """获取配置"""
    global _config
    
    if _config is None:
        config_path = Path(__file__).parent / 'config' / 'adaptive_lb.yaml'
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                _config = yaml.safe_load(f)
        else:
            # 默认配置
            _config = {
                'load_balancer': {
                    'qps_limit': 100,
                    'circuit_breaker_threshold': 0.3,
                    'circuit_breaker_timeout': 30,
                    'health_check_interval': 5,
                    'weight_update_interval': 10
                },
                'agents': []
            }
    
    return _config


def get_instance() -> AdaptiveLoadBalancerV2:
    """获取负载均衡器单例实例"""
    global _instance
    
    if _instance is None:
        config = get_config()['load_balancer']
        
        _instance = AdaptiveLoadBalancerV2(
            qps_limit=config.get('qps_limit', 100),
            circuit_breaker_threshold=config.get('circuit_breaker_threshold', 0.3),
            circuit_breaker_timeout=config.get('circuit_breaker_timeout', 30),
            health_check_interval=config.get('health_check_interval', 5),
            weight_update_interval=config.get('weight_update_interval', 10)
        )
        
        # 添加配置的 Agent
        for agent_config in get_config().get('agents', []):
            _instance.add_agent(
                agent_config['id'],
                agent_config['endpoint'],
                agent_config.get('custom_factors')
            )
        
        logger.info("Adaptive Load Balancer 实例已创建")
    
    return _instance


def create_balancer(
    qps_limit: float = 100,
    circuit_breaker_threshold: float = 0.3,
    circuit_breaker_timeout: int = 30,
    health_check_interval: float = 5,
    weight_update_interval: float = 10
) -> AdaptiveLoadBalancerV2:
    """
    创建新的负载均衡器实例
    
    Args:
        qps_limit: QPS 限制
        circuit_breaker_threshold: 熔断器触发阈值
        circuit_breaker_timeout: 熔断器超时（秒）
        health_check_interval: 健康检查间隔（秒）
        weight_update_interval: 权重更新间隔（秒）
    
    Returns:
        AdaptiveLoadBalancerV2 实例
    """
    lb = AdaptiveLoadBalancerV2(
        qps_limit=qps_limit,
        circuit_breaker_threshold=circuit_breaker_threshold,
        circuit_breaker_timeout=circuit_breaker_timeout,
        health_check_interval=health_check_interval,
        weight_update_interval=weight_update_interval
    )
    
    logger.info(f"创建新的负载均衡器实例：qps_limit={qps_limit}")
    return lb


def reset_instance():
    """重置单例实例"""
    global _instance
    _instance = None
    logger.info("负载均衡器实例已重置")


# 快捷函数
def add_agent(agent_id: str, endpoint: str, custom_factors: Optional[Dict] = None):
    """添加 Agent"""
    return get_instance().add_agent(agent_id, endpoint, custom_factors)


def select_agent(key: Optional[str] = None, priority: RequestPriority = RequestPriority.NORMAL):
    """选择 Agent"""
    return get_instance().select_agent(key, priority)


def record_request(agent_id: str, success: bool, response_time: float):
    """记录请求"""
    return get_instance().record_request(agent_id, success, response_time)


def get_stats():
    """获取统计"""
    return get_instance().get_stats()


def export_prometheus_metrics():
    """导出 Prometheus 指标"""
    return get_instance().export_prometheus_metrics()


def get_scaling_recommendation():
    """获取伸缩建议"""
    return get_instance().get_scaling_recommendation()


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            stats = get_stats()
            print(f"总 Agent 数：{stats['total_agents']}")
            print(f"健康：{stats['healthy_agents']}")
            print(f"降级：{stats['degraded_agents']}")
            print(f"不健康：{stats['unhealthy_agents']}")
            
        elif command == "metrics":
            print(export_prometheus_metrics())
            
        elif command == "scaling":
            recommendation = get_scaling_recommendation()
            print(f"建议：{recommendation['action']}")
            print(f"原因：{recommendation['reason']}")
            
        else:
            print(f"未知命令：{command}")
            print("可用命令：stats, metrics, scaling")
    else:
        print("Adaptive Load Balancer Skill")
        print("用法：python -m skills.adaptive_load_balancer <command>")
        print("命令：stats, metrics, scaling")
