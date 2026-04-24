---
category: docker
created_at: '2026-04-14'
tags:
- docker
- docker
- 完整學習路線圖
- '2026'
- deploy
- k8s
title: Docker Complete Roadmap
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 🐳 Docker 完整學習路線圖 (2026 版)

**創建時間:** 2026-03-19  
**適用對象:** 已掌握 Docker 基礎，希望進階到生產級水平  
**預計時長:** 8-12 週 (200-300 小時)  
**目標水平:** 企業級容器化專家

---

## 📊 學習路徑總覽

```
第一階段：基礎鞏固 (1 週)
  ├─ Docker 核心概念複習
  ├─ 高級命令技巧
  └─ 故障排查能力提升

第二階段：Kubernetes 核心 (4 週) ⭐⭐⭐⭐⭐
  ├─ K8s 基礎架構
  ├─ Pod 和 Deployment
  ├─ Service 和網絡
  └─ 配置和存儲

第三階段：生產實戰 (3 週) ⭐⭐⭐⭐⭐
  ├─ 性能優化
  ├─ 安全加固
  └─ 監控告警

第四階段：CI/CD 集成 (2 週) ⭐⭐⭐⭐
  ├─ GitHub Actions
  ├─ GitLab CI/CD
  └─ 自動化部署

第五階段：進階主題 (2-4 週) ⭐⭐⭐
  ├─ 服務網格 (Istio)
  ├─ 混合雲部署
  └─ 容器平台開發
```

---

## 第一階段：基礎鞏固 (Week 1)

### 目標
- 熟練掌握所有 Docker 高級命令
- 能獨立排查常見問題
- 理解容器底層原理

### 學習內容

#### Day 1-2: 高級命令技巧

**鏡像優化:**
```bash
# 查看鏡像分層
docker history <image>

# 清理懸掛鏡像
docker image prune -a

# 導出/導入鏡像
docker save -o image.tar <image>
docker load -i image.tar

# 多架構鏡像
docker buildx build --platform linux/amd64,linux/arm64 -t myimage .
```

**容器調試:**
```bash
# 進入運行中的容器
docker exec -it <container> /bin/bash

# 查看容器資源使用
docker stats

# 查看容器詳細信息
docker inspect <container>

# 複製文件
docker cp <container>:/path/file ./local/path
```

**網絡診斷:**
```bash
# 查看網絡
docker network ls
docker network inspect <network>

# 創建自定義網絡
docker network create --driver bridge mynet

# 連接容器到網絡
docker network connect mynet <container>
```

#### Day 3-4: 故障排查實戰

**常見問題和解決方案:**

| 問題 | 排查步驟 | 解決方案 |
|------|---------|---------|
| 容器無法啟動 | `docker logs`, `docker inspect` | 檢查配置、權限 |
| 端口衝突 | `docker port`, `netstat` | 更改端口或停止衝突服務 |
| 存儲空間不足 | `docker system df` | 清理懸掛資源 |
| 網絡不通 | `docker network inspect` | 檢查防火牆、路由 |
| 內存溢出 | `docker stats` | 設置資源限制 |

**實戰演練:**
```bash
# 1. 模擬容器崩潰
docker run --name crash-test alpine sh -c "sleep 5 && exit 1"

# 2. 查看日誌
docker logs crash-test

# 3. 檢查退出碼
docker inspect crash-test | grep ExitCode

# 4. 重啟策略
docker run --restart=always ...
```

#### Day 5-7: 原理深入

**理解底層技術:**
- Namespaces (隔離)
- Cgroups (資源限制)
- UnionFS (分層文件系統)
- Network Namespace (網絡隔離)

**實踐:**
```bash
# 查看命名空間
ls -l /proc/$(pidof docker)/ns/

# 查看 cgroups
docker run --rm --cpus="1.5" --memory="512m" alpine free -h
```

### 驗收標準
- [ ] 能在 5 分鐘內定位並解決常見容器問題
- [ ] 理解 Docker 架構和底層原理
- [ ] 熟練使用所有高級命令

---

## 第二階段：Kubernetes 核心 (Week 2-5) ⭐⭐⭐⭐⭐

### Week 2: K8s 基礎

#### Day 1-2: 架構和概念

**核心組件:**
```
┌─────────────────────────────────────────┐
│          Control Plane                   │
│  ┌────────┐  ┌──────────┐  ┌─────────┐ │
│  │API     │  │Scheduler │  │Controller│ │
│  │Server  │  │          │  │Manager  │ │
│  └────────┘  └──────────┘  └─────────┘ │
│           ┌──────────────┐              │
│           │    etcd      │              │
│           └──────────────┘              │
└─────────────────────────────────────────┘
                    │
                    │
┌───────────────────┼───────────────────┐
│         Worker Nodes                    │
│  ┌────────┐  ┌──────────┐  ┌─────────┐ │
│  │Kubelet │  │  Kube-   │  │Container│ │
│  │        │  │  proxy   │  │ Runtime │ │
│  └────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────┘
```

**安裝本地環境:**
```bash
# 使用 Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 啟動集群
minikube start

# 安裝 kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 驗證
kubectl cluster-info
kubectl get nodes
```

#### Day 3-5: Pod 和 Deployment

**Pod 基礎:**
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

**Deployment 管理:**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: nginx:1.21
        ports:
        - containerPort: 80
```

**常用命令:**
```bash
# 創建
kubectl apply -f deployment.yaml

# 查看
kubectl get pods
kubectl get deployments
kubectl describe pod <pod-name>

# 擴展
kubectl scale deployment myapp-deployment --replicas=5

# 更新
kubectl set image deployment/myapp-deployment myapp=nginx:1.22

# 回滾
kubectl rollout undo deployment/myapp-deployment

# 查看歷史
kubectl rollout history deployment/myapp-deployment
```

#### Day 6-7: 實戰練習

**部署 WordPress:**
```yaml
# wordpress-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
spec:
  replicas: 1
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
      - name: wordpress
        image: wordpress:latest
        ports:
        - containerPort: 80
        env:
        - name: WORDPRESS_DB_HOST
          value: mysql
        - name: WORDPRESS_DB_USER
          value: wordpress
        - name: WORDPRESS_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
```

### Week 3: Service 和網絡

#### Service 類型

**ClusterIP (默認):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**NodePort (外部訪問):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
  type: NodePort
```

**LoadBalancer (雲提供商):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

#### Ingress (HTTP 路由)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Week 4: 配置和存儲

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgresql://localhost:5432/mydb"
  LOG_LEVEL: "info"
  config.json: |
    {
      "feature_flags": {
        "new_ui": true
      }
    }
```

#### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_PASSWORD: "super-secret-password"
  API_KEY: "api-key-value"
```

#### PersistentVolume

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### Week 5: 綜合實戰

**項目：部署微服務應用**
```
項目結構:
├─ frontend/        (React 應用)
├─ backend/         (Node.js API)
├─ database/        (PostgreSQL)
└─ k8s/            (K8s 配置)
    ├─ namespace.yaml
    ├─ configmap.yaml
    ├─ secret.yaml
    ├─ database-deployment.yaml
    ├─ backend-deployment.yaml
    ├─ frontend-deployment.yaml
    ├─ services.yaml
    └─ ingress.yaml
```

### 驗收標準
- [ ] 能獨立部署複雜應用到 K8s
- [ ] 理解 Service 和網絡模型
- [ ] 掌握配置管理和存儲
- [ ] 能進行基本的故障排查

---

## 第三階段：生產實戰 (Week 6-8) ⭐⭐⭐⭐⭐

### Week 6: 性能優化

#### 鏡像優化

**多階段構建:**
```dockerfile
# 構建階段
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 運行階段
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

**優化技巧:**
```dockerfile
# ✅ 好的做法
FROM node:18-alpine
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# ❌ 壞的做法
FROM node:18
COPY . .
RUN npm install
```

#### 資源管理

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### 水平自動伸縮 (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Week 7: 安全加固

#### 安全最佳實踐

**最小權限原則:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  capabilities:
    drop:
      - ALL
```

**網絡策略:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**Secret 管理:**
```bash
# 使用外部 Secret 管理工具
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password='S3cr3t'
```

#### 安全掃描

```bash
# 使用 Trivy 掃描鏡像
trivy image myapp:latest

# 使用 Docker Scout
docker scout cve myapp:latest
```

### Week 8: 監控告警

#### Prometheus + Grafana

**部署 Prometheus:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-monitor
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
```

**關鍵指標:**
- CPU 使用率
- 內存使用率
- 請求延遲
- 錯誤率
- Pod 重啟次數

#### 告警規則

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
spec:
  groups:
  - name: myapp
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status="500"}[5m]) > 0.1
      for: 5m
      annotations:
        summary: "高錯誤率"
        description: "錯誤率超過 10%"
```

### 驗收標準
- [ ] 能優化鏡像大小和構建速度
- [ ] 掌握資源限制和自動伸縮
- [ ] 實施安全最佳實踐
- [ ] 配置完整的監控告警

---

## 第四階段：CI/CD 集成 (Week 9-10) ⭐⭐⭐⭐

### Week 9: GitHub Actions

#### 基礎工作流

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: myapp:${{ github.sha }}
        cache-from: type=registry,ref=myapp:buildcache
        cache-to: type=registry,ref=myapp:buildcache,mode=max
```

#### 多環境部署

```yaml
deploy:
  needs: build
  runs-on: ubuntu-latest
  environment: production
  steps:
  - name: Deploy to K8s
    uses: azure/k8s-deploy@v4
    with:
      manifests: |
        k8s/deployment.yaml
      images: |
        myapp:${{ github.sha }}
```

### Week 10: GitLab CI/CD

#### GitLab CI 配置

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm install
    - npm test

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
  only:
    - main
```

### 驗收標準
- [ ] 能配置完整的 CI/CD 流水線
- [ ] 實現自動化測試和部署
- [ ] 掌握多環境管理

---

## 第五階段：進階主題 (Week 11-14) ⭐⭐⭐

### 可選方向

#### 服務網格 (Istio)
- 流量管理
- 熔斷降級
- 可觀察性

#### 混合雲部署
- 多集群管理
- 邊緣計算
- 雲原生架構

#### 容器平台開發
- Operator 開發
- 自定義 CRD
- 平台工具鏈

---

## 📚 推薦資源

### 官方文檔
- [Docker 官方](https://docs.docker.com/) ⭐⭐⭐⭐⭐
- [Kubernetes 官方](https://kubernetes.io/docs/) ⭐⭐⭐⭐⭐
- [Helm 官方](https://helm.sh/docs/) ⭐⭐⭐⭐

### 中文教程
- [Docker 從入門到實踐](https://yeasy.gitbook.io/docker_practice/) ⭐⭐⭐⭐⭐
- [Kubernetes 中文指南](https://kubernetes.io/zh-cn/docs/) ⭐⭐⭐⭐⭐
- [極客時間 - Kubernetes 實戰](https://time.geekbang.org/) ⭐⭐⭐⭐

### 實戰平台
- [Play with Kubernetes](https://labs.play-with-k8s.com/)
- [Katacoda](https://www.katacoda.com/courses/kubernetes)
- [Cloud Native Playground](https://play.cloud-native.io/)

### 書籍推薦
- 《Kubernetes 權威指南》⭐⭐⭐⭐⭐
- 《Docker 技術入門與實戰》⭐⭐⭐⭐
- 《雲原生模式》⭐⭐⭐⭐

### 視頻課程
- B 站：「Kubernetes 從入門到實戰」
- YouTube:「Kubernetes Tutorial for Beginners」
- Udemy:「Docker and Kubernetes: The Complete Guide」

---

## 🎯 實戰項目清單

### 初級項目
- [ ] 容器化個人博客
- [ ] 部署 WordPress
- [ ] 搭建開發環境

### 中級項目
- [ ] 微服務應用部署 (前端 + 後端 + 數據庫)
- [ ] CI/CD 流水線搭建
- [ ] 監控告警系統

### 高級項目
- [ ] 多環境部署 (dev/staging/prod)
- [ ] 自動伸縮和滾動更新
- [ ] 服務網格實施

---

## 📝 學習記錄模板

```markdown
## Week X - YYYY-MM-DD

### 學習內容
- 

### 實踐練習
```bash

```

### 遇到的問題
1. 

### 解決方案
1. 

### 下周計劃
- 

### 收穫和感悟

```

---

## ✅ 學習檢查清單

### 基礎階段
- [ ] Docker 高級命令
- [ ] 故障排查能力
- [ ] 底層原理理解

### Kubernetes 階段
- [ ] Pod 和 Deployment
- [ ] Service 和 Ingress
- [ ] ConfigMap 和 Secret
- [ ] 存儲管理

### 生產實戰階段
- [ ] 性能優化
- [ ] 安全加固
- [ ] 監控告警

### CI/CD 階段
- [ ] GitHub Actions
- [ ] GitLab CI/CD
- [ ] 自動化部署

### 進階階段
- [ ] 服務網格基礎
- [ ] 多集群管理
- [ ] 平台開發經驗

---

**總預計時長:** 200-300 小時  
**完成後水平:** 企業級容器化專家  
**認證建議:** CKA (Certified Kubernetes Administrator)

**創建者:** RedOpenClaw  
**最後更新:** 2026-03-19  
**下次覆盤:** 每周末

## 參考

- [[Knowledge Files Complete List]]
- [[Asset01 Docker Layer Cache]]


## 相關文檔

- [[knowledge-files-complete-list]]
- [[docker_layer_cache]]
- [[asset01_docker_layer_cache]]
