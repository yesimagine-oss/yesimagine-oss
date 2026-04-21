# K8s 健康检查分离优化
用途：避免 Pod 因启动慢被误杀重启
核心规则：
1. livenessProbe：只检查服务是否僵死，不检查业务就绪
2. readinessProbe：检查业务是否可对外提供流量
3. 合理设置 initialDelaySeconds 避免启动期误判
作用：大幅减少服务波动、雪崩、重启风暴
