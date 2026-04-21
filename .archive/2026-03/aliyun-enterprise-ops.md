# 阿里雲控制台深度研究 - 企業級運維與自動化

**學習目標**: 掌握企業級阿里雲運維體系、自動化部署、災難恢復、成本治理  
**適用對象**: 運維工程師、架構師、技術負責人  
**前置知識**: 已完成基礎篇和實戰篇學習

---

## 📚 目錄

1. [企業級運維體系](#1-企業級運維體系)
2. [自動化部署 (CI/CD)](#2-自動化部署 cicd)
3. [災難恢復與業務連續性](#3-災難恢復與業務連續性)
4. [合規與審計](#4-合規與審計)
5. [性能調優實戰](#5-性能調優實戰)
6. [成本治理與 FinOps](#6-成本治理與 finops)
7. [混合雲架構](#7-混合雲架構)
8. [雲原生轉型](#8-雲原生轉型)
9. [運維監控大禮包](#9-運維監控大禮包)
10. [實戰演練：從 0 到 1 搭建企業級架構](#10-實戰演練從 0 到 1 搭建企業級架構)

---

## 1. 企業級運維體系

### 1.1 運維成熟度模型

```
Level 1: 手動運維
├─ 手工操作
├─ 無自動化
├─ 被動響應
└─ 無監控

Level 2: 工具化運維
├─ 腳本自動化
├─ 基礎監控
├─ 工單系統
└─ 文檔化

Level 3: 平台化運維
├─ 自動化平台
├─ 全棧監控
├─ 告警關聯
└─ 變更管理

Level 4: 智能化運維 (AIOps)
├─ 智能告警
├─ 根因分析
├─ 容量預測
└─ 自愈系統

Level 5: 業務驅動運維
├─ 業務指標驅動
├─ 成本優化
├─ 持續改進
└─ 價值交付
```

### 1.2 運維組織架構

```
CTO/CIO
  │
  ├─ 架構團隊
  │   ├─ 雲架構師
  │   └─ 解決方案架構師
  │
  ├─ 開發團隊
  │   ├─ 前端開發
  │   ├─ 後端開發
  │   └─ 測試工程師
  │
  ├─ 運維團隊
  │   ├─ SRE 工程師
  │   ├─ 數據庫 DBA
  │   ├─ 網絡工程師
  │   └─ 安全工程師
  │
  └─ 數據團隊
      ├─ 數據分析師
      └─ BI 工程師
```

### 1.3 運維流程體系

**變更管理流程**：
```
1. 變更申請
   └─ 填寫變更單（影響範圍、回滾方案）

2. 變更審批
   └─ 技術負責人審批 → 業務負責人審批

3. 變更實施
   └─ 灰度發布 → 全量發布

4. 變更驗證
   └─ 功能測試 → 性能測試 → 業務驗證

5. 變更回顧
   └─ 成功經驗 → 改進措施
```

**事件管理流程**：
```
事件發生
   ↓
監控告警/用戶反饋
   ↓
事件分級（P0/P1/P2/P3）
   ↓
應急響應（15 分鐘內）
   ↓
問題定位
   ↓
臨時修復/永久修復
   ↓
事件關閉
   ↓
事後回顧（Post-Mortem）
```

### 1.4 文檔體系

| 文檔類型 | 內容 | 更新頻率 |
|----------|------|----------|
| **架構文檔** | 系統架構圖、技術選型 | 每季度 |
| **運維手冊** | 部署步驟、常見問題 | 每月 |
| **應急預案** | 故障處理流程 | 每半年 |
| **監控文檔** | 監控指標、告警閾值 | 每月 |
| **成本報告** | 資源使用、費用分析 | 每月 |

---

## 2. 自動化部署 (CI/CD)

### 2.1 阿里雲 CodePipeline

**產品組成**：
```
CodePipeline（流水線）
├─ CodeSource（代碼源）
│   └─ GitHub / GitLab / CodeUp
│
├─ CodeBuild（構建）
│   └─ Maven / npm / Docker Build
│
├─ CodeDeploy（部署）
│   └─ ECS / ACK / OSS
│
└─ CodeTest（測試）
    └─ 單元測試 / 集成測試
```

### 2.2 創建 CI/CD 流水線

**步驟**：
```
1. 訪問：https://devops.aliyun.com/
2. 創建項目
3. 創建流水線
4. 配置階段

流水線示例：
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 代碼拉取  │ → │ 代碼構建  │ → │ 運行測試  │ → │ 部署上線  │
│ Git Pull  │   │ mvn/npm  │   │ pytest   │   │ ECS/ACK  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### 2.3 流水線配置示例

**前端項目（Vue/React）**：
```yaml
version: '1.0'
stages:
  - name: 代碼拉取
    type: git
    properties:
      repository: https://github.com/your/repo.git
      branch: main

  - name: 依賴安裝
    type: shell
    properties:
      commands:
        - npm install

  - name: 代碼構建
    type: shell
    properties:
      commands:
        - npm run build

  - name: 部署到 OSS
    type: oss
    properties:
      bucket: my-website
      source: dist/
      destination: /
```

**後端項目（Spring Boot）**：
```yaml
version: '1.0'
stages:
  - name: 代碼拉取
    type: git
    properties:
      repository: https://github.com/your/backend.git
      branch: main

  - name: Maven 構建
    type: shell
    properties:
      commands:
        - mvn clean package -DskipTests

  - name: 運行測試
    type: shell
    properties:
      commands:
        - mvn test

  - name: 構建 Docker 鏡像
    type: docker
    properties:
      dockerfile: Dockerfile
      image: registry.cn-hangzhou.aliyuncs.com/myapp/backend:latest

  - name: 部署到 ACK
    type: k8s
    properties:
      cluster: my-ack-cluster
      namespace: production
      manifest: k8s/deployment.yaml
```

### 2.4 灰度發布策略

**藍綠部署**：
```
環境 A (藍色) → 生產流量 100%
環境 B (綠色) → 新版本

切換：
1. 部署新版本到環境 B
2. 測試驗證
3. SLB 切換流量到環境 B（100%）
4. 環境 A 待命（可快速回滾）
```

**金絲雀發布**：
```
版本 1.0 → 100% 流量

逐步切換：
1. 版本 1.1 → 5% 流量
2. 版本 1.1 → 20% 流量
3. 版本 1.1 → 50% 流量
4. 版本 1.1 → 100% 流量

監控指標：
- 錯誤率 < 1%
- 響應時間 < 500ms
- 業務指標正常
```

---

## 3. 災難恢復與業務連續性

### 3.1 災備等級

| 等級 | RPO | RTO | 說明 | 成本 |
|------|-----|-----|------|------|
| **L1** | < 24h | < 7d | 數據備份 | 低 |
| **L2** | < 4h | < 24h | 異地備份 | 中 |
| **L3** | < 30min | < 4h | 熱備 | 高 |
| **L4** | < 5min | < 30min | 雙活 | 很高 |
| **L5** | 0 | < 1min | 實時同步 | 極高 |

**RPO (Recovery Point Objective)**: 數據丟失容忍度  
**RTO (Recovery Time Objective)**: 業務恢復容忍度

### 3.2 備份策略

**三二一法則**：
```
3 份數據副本
2 種存儲介質
1 個異地存儲
```

**阿里雲備份方案**：
```yaml
本地備份:
  - ECS 快照（每天）
  - RDS 自動備份（每天）
  - OSS 版本控制（實時）

異地備份:
  - 跨地域複製（OSS）
  - 異地災備（RDS）
  - 鏡像複製（ECS 鏡像）

冷備份:
  - OSS 歸檔存儲
  - 磁带庫（混合雲）
```

### 3.3 災備架構

**同城災備**：
```
可用區 A（主）
├─ ECS 集群
├─ RDS 主節點
└─ SLB 入口
        ↓ 同步複製
可用區 B（備）
├─ ECS 待命
├─ RDS 從節點
└─ SLB 待命

故障切換：
1. 檢測可用區 A 故障
2. DNS 切換到可用區 B SLB
3. RDS 從節點提升為主節點
4. ECS 待命實例啟動
5. 業務恢復
```

**異地災備**：
```
地域 A（上海，主）
├─ 完整業務系統
├─ RDS 主節點
└─ OSS 主 Bucket
        ↓ 異步複製
地域 B（北京，備）
├─ 最小業務系統
├─ RDS 備節點
└─ OSS 備 Bucket

切換流程：
1. 確認地域 A 不可恢復
2. 啟動地域 B 完整業務
3. DNS 全局切換
4. 通知用戶
5. 業務恢復
```

### 3.4 應急預案模板

```markdown
# 應急預案：RDS 主節點故障

## 1. 故障現象
- 數據庫連接超時
- 應用報錯：Can't connect to MySQL server
- 監控告警：RDS 實例不可用

## 2. 影響範圍
- 所有依賴數據庫的業務
- 預計影響用戶：100%

## 3. 應急步驟

### 3.1 確認故障（5 分鐘）
```bash
# 檢查 RDS 狀態
aliyun rds DescribeDBInstanceStatus --DBInstanceId rm-xxxxx

# 檢查連接
mysql -h rm-xxxxx.mysql.rds.aliyuncs.com -u root -p -e "SELECT 1"
```

### 3.2 切換備節點（10 分鐘）
```
1. RDS 控制台 → 實例詳情
2. 備節點 → 提升為主節點
3. 確認切換
4. 等待完成（約 5 分鐘）
```

### 3.3 驗證業務（5 分鐘）
```bash
# 測試新主節點
mysql -h rm-yyyy.mysql.rds.aliyuncs.com -u root -p -e "SHOW SLAVE STATUS"

# 檢查應用連接
curl http://app-server/health
```

### 3.4 通知相關方
- 業務部門：業務已恢復
- 管理層：故障處理完成
- 用戶：公告說明（如需）

## 4. 回滾方案
- 如切換失敗，重建 RDS 實例
- 從快照恢復數據

## 5. 事後回顧
- 故障原因分析
- 改進措施
- 預案更新
```

---

## 4. 合規與審計

### 4.1 合規要求

| 合規標準 | 適用行業 | 關鍵要求 |
|----------|---------|---------|
| **等保 2.0** | 所有企業 | 安全分級保護 |
| **GDPR** | 歐盟業務 | 數據隱私保護 |
| **PCI DSS** | 支付行業 | 信用卡數據安全 |
| **ISO 27001** | 所有企業 | 信息管理體系 |
| **SOC 2** | SaaS 服務 | 安全控制審計 |

### 4.2 阿里雲合規產品

```
合規中心
├─ 合規評估
│   └─ 自動掃描合規風險
│
├─ 審計中心
│   └─ 操作審計 (ActionTrail)
│
├─ 日誌審計
│   └─ 日志服務 (SLS)
│
└─ 安全合規
    └─ 配置審計 (Config)
```

### 4.3 操作審計 (ActionTrail)

**啟用審計**：
```
1. 訪問：https://actiontrail.console.aliyun.com/
2. 創建跟蹤
3. 配置
   - 跟範圍：所有地域
   - 事件類型：讀寫事件
   - 投遞目標：OSS Bucket / SLS LogStore
4. 確認創建
```

**審計日誌查詢**：
```bash
# 查詢 ECS 操作
aliyun actiontrail LookupEvents \
  --ServiceName ECS \
  --StartTime 2026-03-15T00:00:00Z \
  --EndTime 2026-03-16T00:00:00Z

# 查詢 RAM 用戶操作
aliyun actiontrail LookupEvents \
  --AccessKeyId <RAM-User-Key>
```

**審計報警**：
```yaml
高風險操作告警:
  - StopInstance（停止實例）
  - DeleteInstance（刪除實例）
  - SecurityGroupRule 修改
  - RAM 權限變更
  - 安全組規則刪除

通知方式:
  - 短信（立即）
  - 電話（立即）
  - 郵件（5 分鐘內）
  - 釘釘（立即）
```

### 4.4 日誌審計 (SLS)

**日誌採集**：
```yaml
採集配置:
  - ECS 系統日誌 (/var/log/*)
  - 應用日誌 (/app/logs/*)
  - Nginx 訪問日誌
  - MySQL 慢查詢日誌
  - 自定義日誌

存儲策略:
  - 熱存儲：30 天（SSD）
  - 冷存儲：90 天（低頻）
  - 歸檔：1 年（歸檔存儲）
```

**日誌分析示例**：
```sql
-- 查詢錯誤日誌
* | SELECT count(*) as error_count 
  WHERE level = 'ERROR' 
  GROUP BY hour(__time__)

-- 查詢慢請求
* | SELECT avg(response_time) as avg_rt, url
  WHERE response_time > 1000
  GROUP BY url
  ORDER BY avg_rt DESC
  LIMIT 10

-- 查詢訪問 Top10
* | SELECT count(*) as pv, remote_addr
  GROUP BY remote_addr
  ORDER BY pv DESC
  LIMIT 10
```

---

## 5. 性能調優實戰

### 5.1 ECS 性能調優

**CPU 調優**：
```bash
# 查看 CPU 使用
top -H -p $(pgrep java)

# 查看 CPU 綁定
taskset -cp $(pgrep java)

# 優化建議
1. 使用性能型實例（計算優化型 c6/c7）
2. 開啟 Turbo Boost
3. 綁定 CPU 核心（減少上下文切換）
4. 使用多進程/多線程
```

**內存調優**：
```bash
# 查看內存使用
free -h
vmstat 1 5

# 優化 Swap
echo 'vm.swappiness=10' >> /etc/sysctl.conf
sysctl -p

# 優化建議
1. 使用內存型實例（r6/r7）
2. 配置 HugePages
3. 調整 JVM 堆大小
4. 使用內存緩存（Redis/Memcached）
```

**磁盤 IO 調優**：
```bash
# 查看 IO 使用
iostat -x 1 5
iotop -o

# 調整 IO 調度器
cat /sys/block/vda/queue/scheduler
echo 'deadline' > /sys/block/vda/queue/scheduler

# 優化建議
1. 使用 ESSD 雲盤（PL2/PL3）
2. 多塊磁盤 RAID 0
3. 使用本地 SSD 盤
4. 異步 IO（AIO）
```

**網絡調優**：
```bash
# 查看網絡使用
sar -n DEV 1 5
iftop -P

# 優化內核參數
cat >> /etc/sysctl.conf << EOF
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 250000
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_tw_reuse = 1
EOF
sysctl -p

# 優化建議
1. 使用網絡優化型實例（g6ne/g7ne）
2. 開啟 SR-IOV
3. 使用彈性網卡（多 IP）
4. 配置 TCP BBR
```

### 5.2 RDS 性能調優

**SQL 優化**：
```sql
-- 查看慢查詢
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 分析慢查詢
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- 優化建議
1. 添加索引（避免全表掃描）
2. 避免 SELECT *
3. 使用覆蓋索引
4. 優化 JOIN 順序
5. 使用緩存（Redis）
```

**參數調優**：
```ini
# my.cnf 優化
[mysqld]
# 內存相關
innodb_buffer_pool_size = 70% 物理內存
innodb_log_buffer_size = 64M

# IO 相關
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# 連接相關
max_connections = 2000
thread_cache_size = 100

# 查詢緩存（MySQL 5.7）
query_cache_size = 128M
query_cache_type = 1
```

### 5.3 應用性能調優

**Java 應用**：
```bash
# JVM 參數優化
JAVA_OPTS="-Xms4g -Xmx4g \
  -XX:NewRatio=2 \
  -XX:SurvivorRatio=8 \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/heapdump.hprof"

# 監控 GC
jstat -gcutil <pid> 1000

# 分析堆內存
jmap -heap <pid>
```

**Nginx 優化**：
```nginx
# worker 進程
worker_processes auto;
worker_rlimit_nofile 65535;

# 事件模型
events {
    use epoll;
    worker_connections 65535;
    multi_accept on;
}

# HTTP 優化
http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # 緩存
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=cache:100m;
    
    # 壓縮
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
}
```

---

## 6. 成本治理與 FinOps

### 6.1 成本分攤

**標籤體系**：
```yaml
標籤分類:
  - 部門標籤
    - department: tech
    - department: sales
    - department: hr
  
  - 項目標籤
    - project: ecommerce
    - project: crm
    - project: data-platform
  
  - 環境標籤
    - env: production
    - env: staging
    - env: development
  
  - 成本中心
    - cost-center: cc001
    - cost-center: cc002
```

**成本分配報告**：
```
月度成本報告 - 2026 年 3 月

總費用：¥50,000

按部門分攤:
├─ 技術部：¥30,000 (60%)
├─ 銷售部：¥10,000 (20%)
├─ 產品部：¥5,000 (10%)
└─ 其他：¥5,000 (10%)

按項目分攤:
├─ 電商平台：¥25,000 (50%)
├─ CRM 系統：¥15,000 (30%)
└─ 數據平台：¥10,000 (20%)

按環境分攤:
├─ 生產環境：¥35,000 (70%)
├─ 測試環境：¥10,000 (20%)
└─ 開發環境：¥5,000 (10%)
```

### 6.2 成本優化策略

**資源 rightsizing**：
```bash
# 查看資源使用率
aliyun cms DescribeMetricList \
  --MetricName CPUUtilization \
  --Dimensions '{"instanceId":"i-xxxxx"}'

# 優化建議
使用率 < 20% → 降配
使用率 20-60% → 保持
使用率 > 80% → 升配
```

**計費方式優化**：
| 場景 | 推薦計費 | 節省比例 |
|------|---------|---------|
| 長期穩定負載 | 包年包月 | 40-60% |
| 短期波動負載 | 按量付費 + 節省計劃 | 30-50% |
| 批處理任務 | 競價實例 | 60-90% |
| 存儲冷數據 | 歸檔存儲 | 70-80% |

**節省計劃計算**：
```yaml
場景：10 台 ECS（2 核 4GB）
按量付費：¥0.5/小時 × 10 × 24 × 30 = ¥3,600/月

購買節省計劃（1 年）：
- 承諾消費：¥2,000/月
- 折扣：65%
- 實際費用：¥2,000 + (¥3,600-¥2,000)×0.35 = ¥2,406/月
- 節省：¥1,194/月 (33%)
```

### 6.3 預算與告警

**預算設置**：
```yaml
月度預算:
  - 總預算：¥50,000
  - 預警閾值：80% (¥40,000)
  - 超支閾值：100% (¥50,000)
  - 嚴重閾值：120% (¥60,000)

通知規則:
  - 80%：郵件通知財務
  - 100%：郵件 + 短信通知 CTO
  - 120%：郵件 + 短信 + 電話通知 CEO
```

**成本異常檢測**：
```python
# 檢測成本突增
import boto3  # 阿里雲 SDK 類似

def detect_cost_anomaly():
    # 獲取當前費用
    current_cost = get_current_month_cost()
    
    # 獲取歷史平均
    avg_cost = get_last_3_months_avg()
    
    # 檢測異常
    if current_cost > avg_cost * 1.5:
        send_alert(
            subject='成本異常告警',
            message=f'當前費用 {current_cost} 超過平均值 {avg_cost} 的 50%'
        )
```

---

## 7. 混合雲架構

### 7.1 混合雲場景

| 場景 | 說明 | 解決方案 |
|------|------|---------|
| **數據備份** | 本地數據備份到雲 | 混合雲備份 HBR |
| **災難恢復** | 本地故障切換到雲 | 混合雲災備 HDR |
| **業務擴展** | 業務高峰期使用雲資源 | 混合雲彈性 |
| **數據同步** | 本地與雲數據雙向同步 | DTS 數據傳輸 |
| **統一管理** | 本地和雲統一運維 | 混合雲管理 HCM |

### 7.2 混合雲連接方案

**方案 1：專線連接**：
```
本地數據中心
    ↓
專線接入點
    ↓
阿里雲專線
    ↓
VPC 路由器
    ↓
ECS/RDS/OSS
```

**方案 2：VPN 連接**：
```bash
# 本地 VPN 網關配置
aliyun vpc CreateVpnGateway \
  --VpcId vpc-xxxxx \
  --ZoneId cn-hangzhou-b

# 用戶網關配置
aliyun vpc CreateCustomerGateway \
  --Name local-gateway \
  --IpAddress 203.0.113.1

# IPsec 連接
aliyun vpc CreateVpnConnection \
  --VpnGatewayId vgw-xxxxx \
  --CustomerGatewayId cgw-xxxxx
```

### 7.3 混合雲存儲

**雲存儲網關**：
```
本地應用
    ↓
NFS/SMB 協議
    ↓
雲存儲網關 (CSG)
    ↓
OSS 對象存儲
```

**配置步驟**：
```
1. 創建 CSG 實例
2. 配置本地連接
3. 創建存儲卷
4. 掛載到本地服務器
5. 配置緩存策略
```

---

## 8. 雲原生轉型

### 8.1 容器化改造

**傳統架構 → 容器化**：
```
傳統架構:
┌─────────────┐
│   應用 + 環境  │  部署複雜
│   緊耦合     │  擴展困難
└─────────────┘

容器化架構:
┌─────────────┐
│   應用鏡像   │  標準化
│   環境隔離   │  快速部署
└─────────────┘
    ↓
┌─────────────┐
│  Kubernetes  │  自動編排
│   集群      │  彈性伸縮
└─────────────┘
```

### 8.2 ACK 集群搭建

**創建集群**：
```
1. 訪問：https://cs.console.aliyun.com/
2. 創建 Kubernetes 集群
3. 選擇
   - 托管版（推薦）
   - 專有版
4. 配置
   - Worker 節點：3 台起
   - 實例規格：2 核 4GB 起
   - 網絡：Terway/Flannel
5. 確認創建
```

**部署應用**：
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
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
        image: registry.cn-hangzhou.aliyuncs.com/myapp:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 8.3 服務網格 (ASM)

**服務網格優勢**：
```
傳統微服務:
├─ 服務發現（自實現）
├─ 負載均衡（自實現）
├─ 熔斷降級（自實現）
└─ 可觀察性（自實現）

服務網格:
├─ 服務發現（Istio）
├─ 負載均衡（Istio）
├─ 熔斷降級（Istio）
└─ 可觀察性（Istio）
```

---

## 9. 運維監控大禮包

### 9.1 監控指標體系

**四黃金指標**：
| 指標 | 說明 | 告警閾值 |
|------|------|---------|
| **延遲** | 請求響應時間 | P99 > 1s |
| **流量** | QPS/TPS | 突增 50% |
| **錯誤** | 錯誤率 | > 1% |
| **飽和度** | 資源使用率 | > 80% |

### 9.2 監控儀表板

**Grafana 儀表板模板**：
```json
{
  "dashboard": {
    "title": "業務監控大盤",
    "panels": [
      {
        "title": "QPS 趨勢",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))"
          }
        ]
      },
      {
        "title": "錯誤率",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
          }
        ]
      },
      {
        "title": "響應時間",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### 9.3 告警分級

| 級別 | 名稱 | 響應時間 | 通知方式 |
|------|------|---------|---------|
| **P0** | 嚴重 | 5 分鐘 | 電話 + 短信 + 釘釘 |
| **P1** | 緊急 | 15 分鐘 | 短信 + 釘釘 |
| **P2** | 警告 | 1 小時 | 釘釘 |
| **P3** | 提示 | 4 小時 | 郵件 |

---

## 10. 實戰演練：從 0 到 1 搭建企業級架構

### 10.1 需求分析

**業務場景**：電商平台
- 日均 UV: 10 萬
- 峰值 QPS: 5000
- 數據量：1TB
- 可用性要求：99.9%

### 10.2 架構設計

```
                    用戶
                     ↓
                CDN (全站加速)
                     ↓
              WAF (Web 防火牆)
                     ↓
              SLB (負載均衡)
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    ECS1         ECS2         ECS3
   (Web 應用)    (Web 應用)    (Web 應用)
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
     Redis       RDS MySQL      OSS
   (緩存)      (主從複製)    (靜態資源)
```

### 10.3 資源清單

| 資源 | 規格 | 數量 | 月費用 |
|------|------|------|-------|
| ECS | 4 核 8GB | 3 台 | ¥600 |
| SLB | 性能保障型 | 1 台 | ¥200 |
| RDS | 4 核 8GB 高可用 | 1 主 1 從 | ¥800 |
| Redis | 4GB 集群版 | 1 個 | ¥300 |
| OSS | 500GB 標準 | 1 個 | ¥100 |
| CDN | 5TB 流量包 | 1 個 | ¥500 |
| WAF | 基礎版 | 1 個 | ¥300 |
| **總計** | | | **¥2,800/月** |

### 10.4 部署步驟

**Day 1：基礎設施**
```bash
# 1. 創建 VPC
aliyun vpc CreateVpc --CidrBlock 172.16.0.0/16

# 2. 創建交換機
aliyun vpc CreateVSwitch \
  --VpcId vpc-xxxxx \
  --ZoneId cn-hangzhou-b \
  --CidrBlock 172.16.1.0/24

# 3. 創建安全組
aliyun ecs CreateSecurityGroup \
  --VpcId vpc-xxxxx \
  --SecurityGroupName web-sg
```

**Day 2：計算資源**
```bash
# 創建 ECS 實例
for i in {1..3}; do
  aliyun ecs CreateInstance \
    --ImageId ubuntu_22_04_x64 \
    --InstanceType ecs.c6.large \
    --SecurityGroupId sg-xxxxx \
    --VSwitchId vsw-xxxxx \
    --InstanceName web-server-$i
done
```

**Day 3：數據庫**
```bash
# 創建 RDS 實例
aliyun rds CreateDBInstance \
  --Engine MySQL \
  --EngineVersion 8.0 \
  --DBInstanceClass rds.mysql.c2.large \
  --DBInstanceStorage 200
```

**Day 4：應用部署**
```bash
# 部署應用（使用 Ansible）
ansible-playbook -i inventory.ini deploy.yml
```

**Day 5：監控告警**
```bash
# 配置監控
aliyun cms PutContactGroup \
  --ContactGroupName ops-team \
  --Contacts '[{"Name":"張三","Phone":"13800138000"}]'

# 創建告警規則
aliyun cms PutResourceMetricRuleTemplate \
  --RuleName cpu-high \
  --MetricName CPUUtilization \
  --Threshold 80
```

### 10.5 驗收測試

**性能測試**：
```bash
# 使用 wrk 進行壓力測試
wrk -t12 -c400 -d30s http://slb-ip/api/products

# 預期結果
Requests/sec: 5000+
Latency P99: < 500ms
Error rate: < 0.1%
```

**故障演練**：
```bash
# 1. 模擬 ECS 故障
aliyun ecs StopInstance --InstanceId i-xxxxx

# 2. 觀察 SLB 健康檢查
# 預期：流量自動切換到健康實例

# 3. 模擬 RDS 主從切換
# 預期：業務中斷 < 30 秒

# 4. 驗證監控告警
# 預期：5 分鐘內收到告警通知
```

---

## 📋 學習檢查清單

### 企業級運維
- [ ] 理解運維成熟度模型
- [ ] 掌握變更管理流程
- [ ] 熟悉事件管理流程
- [ ] 建立文檔體系

### 自動化部署
- [ ] 創建 CI/CD 流水線
- [ ] 實現灰度發布
- [ ] 配置自動化測試

### 災難恢復
- [ ] 制定備份策略
- [ ] 設計災備架構
- [ ] 編寫應急預案
- [ ] 定期演練

### 合規審計
- [ ] 啟用操作審計
- [ ] 配置日誌審計
- [ ] 設置合規告警

### 性能調優
- [ ] ECS 性能調優
- [ ] RDS 性能調優
- [ ] 應用性能調優

### 成本治理
- [ ] 建立標籤體系
- [ ] 設置預算告警
- [ ] 優化計費方式

---

## 🔗 進階學習資源

- **阿里雲架構師博客**: https://developer.aliyun.com/group/
- **阿里雲最佳實踐**: https://www.aliyun.com/solution/
- **Kubernetes 官方文檔**: https://kubernetes.io/docs/
- **SRE Google 書籍**: https://sre.google/books/
- **FinOps 基金會**: https://www.finops.org/

---

**最後更新**: 2026-03-16  
**版本**: v1.0  
**總字數**: 約 20,000 字  
**建議學習時間**: 2-4 週
