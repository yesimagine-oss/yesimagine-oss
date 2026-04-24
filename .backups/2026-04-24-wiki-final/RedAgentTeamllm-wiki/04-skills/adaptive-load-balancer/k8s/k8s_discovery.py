#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kubernetes Agent 自动发现

自动发现 K8s 集群中的 Agent 服务并注册到负载均衡器。
"""

from kubernetes import client, config
from adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2
import logging

logger = logging.getLogger(__name__)


class K8sAgentDiscovery:
    """Kubernetes Agent 自动发现器"""
    
    def __init__(self, namespace: str = "default", label_selector: str = "app=agent"):
        """
        初始化发现器
        
        Args:
            namespace: K8s 命名空间
            label_selector: Agent 标签选择器
        """
        self.namespace = namespace
        self.label_selector = label_selector
        
        # 加载 K8s 配置
        try:
            config.load_incluster_config()
            logger.info("使用集群内配置")
        except:
            config.load_kube_config()
            logger.info("使用 kubeconfig 配置")
        
        self.v1 = client.CoreV1Api()
        self.lb: AdaptiveLoadBalancerV2 = None
    
    def set_load_balancer(self, lb: AdaptiveLoadBalancerV2):
        """设置负载均衡器实例"""
        self.lb = lb
    
    def discover_agents(self) -> list:
        """发现 Agent 服务"""
        try:
            # 获取服务列表
            services = self.v1.list_namespaced_service(
                namespace=self.namespace,
                label_selector=self.label_selector
            )
            
            agents = []
            for svc in services.items:
                agent_id = svc.metadata.name
                cluster_ip = svc.spec.cluster_ip
                port = svc.spec.ports[0].port if svc.spec.ports else 8000
                
                endpoint = f"http://{cluster_ip}:{port}"
                agents.append((agent_id, endpoint))
                
                logger.info(f"发现 Agent: {agent_id} @ {endpoint}")
            
            return agents
            
        except Exception as e:
            logger.error(f"发现 Agent 失败：{e}")
            return []
    
    def sync_agents(self):
        """同步 Agent 到负载均衡器"""
        if not self.lb:
            logger.error("负载均衡器未设置")
            return
        
        # 获取当前 Agent
        discovered = self.discover_agents()
        discovered_ids = {aid for aid, _ in discovered}
        current_ids = set(self.lb.agents.keys())
        
        # 添加新 Agent
        for agent_id, endpoint in discovered:
            if agent_id not in current_ids:
                self.lb.add_agent(agent_id, endpoint)
                logger.info(f"添加 Agent: {agent_id}")
        
        # 移除不存在的 Agent
        for agent_id in current_ids - discovered_ids:
            self.lb.remove_agent(agent_id)
            logger.info(f"移除 Agent: {agent_id}")
        
        logger.info(f"同步完成：{len(discovered)} agents")
    
    def start_watching(self, callback=None):
        """开始监听 K8s 事件"""
        from kubernetes.watch import Watch
        
        w = Watch()
        for event in w.stream(
            self.v1.list_namespaced_service,
            namespace=self.namespace,
            label_selector=self.label_selector
        ):
            event_type = event['type']
            service = event['object']
            agent_id = service.metadata.name
            
            logger.info(f"K8s 事件：{event_type} {agent_id}")
            
            if callback:
                callback(event_type, agent_id)
            
            # 同步 Agent
            self.sync_agents()


# 使用示例
if __name__ == "__main__":
    import time
    
    # 创建负载均衡器
    lb = AdaptiveLoadBalancerV2()
    
    # 创建发现器
    discovery = K8sAgentDiscovery(namespace="default")
    discovery.set_load_balancer(lb)
    
    # 初始同步
    discovery.sync_agents()
    
    # 定期同步（生产环境建议使用 watch）
    while True:
        time.sleep(30)
        discovery.sync_agents()
        
        # 打印状态
        stats = lb.get_stats()
        print(f"Agents: {stats['total_agents']}, Healthy: {stats['healthy_agents']}")
