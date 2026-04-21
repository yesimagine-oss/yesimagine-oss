# 📚 阿里雲工作臺學習筆記 - Day 4

**學習時間:** 2026-03-18  
**學習主題:** 企業級運維  
**參考資料:** 
- `aliyun-enterprise-ops.md`
- `aliyun-hands-on-training.md`
- `aliyun-console-advanced.md`

---

## Day 4 - 2026-03-18：企業級運維

### 1. 監控體系建設

#### 1.1 運維成熟度模型

**五個等級:**
```
Level 1: 手動運維
├─ 手工操作、無自動化
├─ 被動響應、無監控
└─ 初創團隊常見

Level 2: 工具化運維
├─ 腳本自動化
├─ 基礎監控
├─ 工單系統、文檔化
└─ 小型團隊

Level 3: 平台化運維
├─ 自動化平台
├─ 全棧監控
├─ 告警關聯、變更管理
└─ 中型企業

Level 4: 智能化運維 (AIOps)
├─ 智能告警、根因分析
├─ 容量預測、自愈系統
└─ 大型互聯網

Level 5: 業務驅動運維
├─ 業務指標驅動
├─ 成本優化、持續改進
└─ 行業領先
```

#### 1.2 四黃金監控指標

| 指標 | 說明 | 告警閾值 | 監控工具 |
|------|------|---------|---------|
| **延遲** | 請求響應時間 | P99 > 1s | ARMS、Prometheus |
| **流量** | QPS/TPS | 突增 50% | SLB 日誌、ARMS |
| **錯誤** | 錯誤率 | > 1% | ARMS、日誌服務 |
| **飽和度** | 資源使用率 | > 80% | 雲監控 |

#### 1.3 雲監控配置

**安裝監控插件:**
```bash
# 下載監控插件
wget https://cloudmonitor-<region>.oss-<region>.aliyuncs.com/latest/ArgusAgent-Linux64.tgz

# 解壓安裝
tar -xzf ArgusAgent-Linux64.tgz
cd ArgusAgent-Linux64
./install.sh

# 查看狀態
systemctl status CmsGoAgent
```

**配置告警規則:**
```
1. 訪問：https://cms.console.aliyun.com/
2. 點擊「告警」→「創建告警」

CPU 告警:
- 監控項：CPU 使用率
- 統計週期：1 分鐘
- 連續次數：3 次
- 閾值：> 80%
- 通知方式：郵件 + 短信

內存告警:
- 監控項：內存使用率
- 閾值：> 85%

磁盤告警:
- 監控項：磁盤使用率
- 閾值：> 80%
```

**告警分級:**
| 級別 | 名稱 | 響應時間 | 通知方式 |
|------|------|---------|---------|
| **P0** | 嚴重 | 5 分鐘 | 電話 + 短信 + 釘釘 |
| **P1** | 緊急 | 15 分鐘 | 短信 + 釘釘 |
| **P2** | 警告 | 1 小時 | 釘釘 |
| **P3** | 提示 | 4 小時 | 郵件 |

#### 1.4 配置釘釘通知

**創建釘釘機器人:**
```
1. 打開釘釘群
2. 群設置 → 智能助手 → 添加機器人
3. 選擇「自定義」
4. 填寫機器人名稱：運維告警
5. 獲取 Webhook URL
```

**配置雲監控通知:**
```
1. 雲監控控制台 → 告警 → 通知方式
2. 點擊「添加通知方式」
3. 選擇「Webhook」
4. 填寫釘釘 Webhook URL
5. 測試發送
```

**釘釘告警消息格式:**
```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "服務器告警通知",
    "text": "## 告警通知\n\n**告警級別**: P1\n**告警源**: iZm5ei3ekpe8wbnvf7snniZ\n**告警項**: CPU 使用率\n**當前值**: 92%\n**閾值**: 80%\n**時間**: 2026-03-18 06:10:00\n\n請立即處理！"
  }
}
```

---

### 2. 日誌管理

#### 2.1 日誌服務（SLS）架構

```
日誌採集
   ↓
日誌收集（Logtail）
   ↓
日誌存儲（SLS）
   ↓
日誌分析（SQL/圖表）
   ↓
告警通知
```

**核心概念:**
- **Project**: 日誌項目（資源管理單元）
- **Logstore**: 日誌存儲（存儲和計算單元）
- **Logtail**: 日誌採集代理
- **Shard**: 分區（併發讀寫單元）
- **Index**: 索引（加速查詢）

#### 2.2 創建日誌項目

**實操步驟:**
```
1. 訪問：https://sls.console.aliyun.com/
2. 點擊「創建 Project」
3. 配置：
   - 項目名稱：myapp-logs
   - 地域：與 ECS 相同
   - 存儲容量：100GB
   - 存儲週期：30 天
4. 確認創建
```

**創建 Logstore:**
```
1. Project 詳情 → 創建 Logstore
2. 配置：
   - Logstore 名稱：app-access-log
   - 存儲週期：30 天
   - 分區數：2
   - 索引：開啟
3. 確認創建
```

#### 2.3 安裝 Logtail

**安裝步驟:**
```bash
# 1. 獲取安裝命令
# SLS 控制台 → 數據接入 → Logtail 配置

# 2. 執行安裝命令
wget http://logtail-release-<region>.oss-<region>.aliyuncs.com/linux64/logtail.sh
chmod +x logtail.sh
sudo ./logtail.sh install <aliyun-region-id> <project-name>

# 3. 查看狀態
sudo /etc/init.d/ilogtaild status
```

**配置採集:**
```
1. SLS 控制台 → 數據接入
2. 選擇採集方式：Logtail
3. 配置採集路徑：
   - 日誌路徑：/var/log/nginx/access.log
   - 日誌格式：Nginx 訪問日誌
   - 解析方式：自動解析
4. 指定 Logstore
5. 確認創建
```

#### 2.4 日誌查詢分析

**查詢語法:**
```sql
-- 統計每分鐘 PV
* | select date_trunc('minute', __time__) as time, count(1) as pv 
  group by time order by time

-- 統計 Top 10 IP
* | select remote_addr, count(1) as pv 
  group by remote_addr order by pv desc limit 10

-- 統計 HTTP 狀態碼分佈
* | select status, count(1) as count 
  group by status order by count desc

-- 查找錯誤請求
status >= 500 | select request_uri, count(1) as count 
  group by request_uri order by count desc

-- 統計平均響應時間
* | select avg(request_time) as avg_time, 
          max(request_time) as max_time 
  from log
```

**儀表板配置:**
```
1. SLS 控制台 → 儀表盤
2. 創建儀表盤
3. 添加圖表：
   - PV/UV 趨勢圖
   - 狀態碼分佈餅圖
   - Top 10 URL 表格
   - 響應時間曲線
4. 保存儀表盤
```

---

### 3. 自動化運維

#### 3.1 運維編排服務（OOS）

**適用場景:**
- 批量操作 ECS 實例
- 定時任務執行
- 自動化運維流程
- 應急預案自動化

**創建執行模板:**
```
1. 訪問：https://oos.console.aliyun.com/
2. 點擊「創建模板」
3. 選擇模板類型：
   - 公共模板（系統預置）
   - 自定義模板（YAML/JSON）
4. 配置參數
5. 執行模板
```

**常用公共模板:**
```yaml
批量重啟 ECS:
  模板：ACS-ECS-BulkyRestartInstances
  參數：
    - instanceIds: ["i-xxx1", "i-xxx2"]
    
批量更新密碼:
  模板：ACS-ECS-BulkyUpdateInstancePassword
  參數：
    - instanceIds: [...]
    - password: <新密碼>
    
定時創建快照:
  模板：ACS-ECS-CreateSnapshot
  參數：
    - instanceId: i-xxx
    - cron: "0 2 * * *" (每天 2 點)
```

#### 3.2 自定義自動化腳本

**批量部署腳本:**
```bash
#!/bin/bash
# deploy-all.sh

# ECS 實例列表
INSTANCES=("i-xxx1" "i-xxx2" "i-xxx3")

for instance in "${INSTANCES[@]}"; do
  echo "部署到 $instance..."
  
  # 使用 OOS 執行命令
  aliyun oos StartExecution \
    --TemplateName ACS-ECS-RunShellScript \
    --Parameters "{
      \"instanceIds\": [\"$instance\"],
      \"command\": \"cd /var/www && git pull && systemctl reload nginx\"
    }"
  
  echo "等待部署完成..."
  sleep 30
done

echo "所有實例部署完成！"
```

**自動擴容腳本:**
```bash
#!/bin/bash
# auto-scale.sh

# 檢查 CPU 使用率
CPU_USAGE=$(aliyun cms DescribeMetricList \
  --MetricName CPUUtilization \
  --Dimensions "{\"instanceId\":\"i-xxx\"}" \
  --Period 60 \
  --Length 1 \
  | jq '.Datapoints[0].Average')

echo "當前 CPU 使用率：$CPU_USAGE%"

if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
  echo "CPU 過高，開始擴容..."
  
  # 添加 ECS 實例
  aliyun ess AddScalingInstances \
    --ScalingGroupId asg-xxx \
    --MinSize 3 \
    --MaxSize 10 \
    --DesiredCapacity 4
  
  echo "擴容完成！"
elif (( $(echo "$CPU_USAGE < 30" | bc -l) )); then
  echo "CPU 過低，開始縮容..."
  
  # 移除 ECS 實例
  aliyun ess RemoveScalingInstances \
    --ScalingGroupId asg-xxx \
    --InstanceIds '["i-xxx"]' \
    --DesiredCapacity 2
  
  echo "縮容完成！"
fi
```

#### 3.3 CI/CD 流水線

**流水線配置:**
```yaml
# codepipeline.yml
version: '1.0'
stages:
  - name: 代碼拉取
    type: git
    properties:
      repository: https://github.com/myorg/myapp.git
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

  - name: 運行測試
    type: shell
    properties:
      commands:
        - npm test

  - name: 部署到 ECS
    type: ecs
    properties:
      instanceIds:
        - i-xxx1
        - i-xxx2
      command: |
        cd /var/www/myapp
        git pull
        npm install --production
        pm2 restart myapp
```

---

### 4. 成本優化（FinOps）

#### 4.1 成本分析

**查看費用明細:**
```
1. 訪問：https://usercenter2.aliyun.com/
2. 費用中心 → 賬單詳情
3. 選擇賬單週期
4. 查看明細：
   - 按產品分類
   - 按實例分類
   - 按地域分類
```

**成本分佈示例:**
```yaml
月度總費用：¥10,000

分佈:
- ECS: ¥5,000 (50%)
- RDS: ¥2,000 (20%)
- SLB: ¥1,000 (10%)
- OSS: ¥800 (8%)
- CDN: ¥700 (7%)
- 其他：¥500 (5%)
```

#### 4.2 成本優化策略

**實例規格優化:**
```bash
# 查看實例 CPU 使用率（過去 7 天）
aliyun cms DescribeMetricList \
  --MetricName CPUUtilization \
  --Dimensions "{\"instanceId\":\"i-xxx\"}" \
  --Period 3600 \
  --Length 168

# 如果平均使用率 < 30%，考慮降配
# 4 核 8GB → 2 核 4GB (節省 50%)
```

**節省計劃:**
```
1 年包月：比按月購買節省 ~15-20%
3 年包月：比按月購買節省 ~30-40%

預付費 vs 按量付費:
- 長期穩定業務 → 包年包月
- 短期測試業務 → 按量付費
- 波峰波谷明顯 → 按量付費 + 自動縮容
```

**資源整合:**
```bash
# 查看空閒實例（7 天 CPU < 5%）
aliyun ecs DescribeInstances \
  --RegionId cn-hangzhou \
  --Status Running

# 合併低負載實例
# 3 台 2 核 4GB → 1 台 4 核 8GB
# 節省：66%
```

**存儲優化:**
```yaml
OSS 存儲類型轉換:
- 標準存儲 → 頻繁訪問
- 低頻訪問 → 30 天內訪問 < 1 次
- 歸檔存儲 → 90 天內訪問 < 1 次
- 冷歸檔 → 180 天內訪問 < 1 次

成本對比（每 GB/月）:
- 標準：¥0.12
- 低頻：¥0.08 (節省 33%)
- 歸檔：¥0.033 (節省 72%)
- 冷歸檔：¥0.015 (節省 87%)
```

**帶寬優化:**
```yaml
按帶寬計費 vs 按使用量:
- 帶寬利用率 > 50% → 按帶寬計費
- 帶寬利用率 < 30% → 按使用量計費

CDN 加速:
- 靜態資源 → 使用 CDN
- 動態內容 → 全站加速
- 視頻 → 視頻 CDN

成本節省：50-70%
```

#### 4.3 成本監控告警

**設置預算告警:**
```
1. 費用中心 → 預算管理
2. 創建預算
3. 配置：
   - 預算名稱：月度預算
   - 預算金額：¥10,000
   - 預警閾值：50%、80%、100%
   - 通知方式：郵件 + 短信
4. 確認創建
```

**異常費用告警:**
```
1. 費用中心 → 費用預警
2. 創建預警規則
3. 配置：
   - 對比基準：上週期
   - 增長閾值：> 20%
   - 通知方式：郵件 + 釘釘
```

---

### 5. 災難恢復與業務連續性

#### 5.1 災備等級

| 等級 | RPO | RTO | 說明 | 成本 |
|------|-----|-----|------|------|
| **L1** | < 24h | < 7d | 數據備份 | 低 |
| **L2** | < 4h | < 24h | 異地備份 | 中 |
| **L3** | < 30min | < 4h | 熱備 | 高 |
| **L4** | < 5min | < 30min | 雙活 | 很高 |
| **L5** | 0 | < 1min | 實時同步 | 極高 |

**RPO (Recovery Point Objective)**: 數據丟失容忍度  
**RTO (Recovery Time Objective)**: 業務恢復容忍度

#### 5.2 備份策略（三二一法則）

```
3 份數據副本
2 種存儲介質
1 個異地存儲
```

**阿里雲備份方案:**
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

#### 5.3 應急預案模板

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
1. RDS 控制台 → 實例詳情
2. 備節點 → 提升為主節點
3. 確認切換
4. 等待完成（約 5 分鐘）

### 3.3 驗證業務（5 分鐘）
```bash
# 測試新主節點
mysql -h rm-yyyy.mysql.rds.aliyuncs.com -u root -p

# 檢查應用連接
curl http://app-server/health
```

### 3.4 通知相關方
- 業務部門：業務已恢復
- 管理層：故障處理完成
- 用戶：公告說明（如需）
```

---

## 📝 Day 4 學習總結

### 掌握的要點

| 模塊 | 核心技能 |
|------|---------|
| **監控體系** | 四黃金指標、雲監控配置、告警分級、釘釘通知 |
| **日誌管理** | SLS 架構、Logtail 安裝、查詢分析、儀表板 |
| **自動化運維** | OOS 模板、批量操作、CI/CD 流水線 |
| **成本優化** | 成本分析、節省計劃、資源整合、存儲優化 |
| **災難恢復** | 災備等級、備份策略、應急預案 |

### 實操命令速查

**監控告警:**
```bash
# 查看 CPU 使用率
aliyun cms DescribeMetricList \
  --MetricName CPUUtilization \
  --Dimensions "{\"instanceId\":\"i-xxx\"}"

# 創建告警規則
aliyun cms PutMetricRuleTemplate \
  --RuleName cpu-high \
  --MetricName CPUUtilization \
  --Threshold 80
```

**日誌查詢:**
```sql
-- 統計 PV
* | select count(1) as pv from log

-- Top 10 IP
* | select remote_addr, count(1) as pv 
  group by remote_addr order by pv desc limit 10

-- 錯誤率
status >= 500 | select count(1) as error_count from log
```

**自動化:**
```bash
# OOS 執行命令
aliyun oos StartExecution \
  --TemplateName ACS-ECS-RunShellScript \
  --Parameters "{...}"

# 批量操作
aliyun ecs BulkyRestartInstances --instanceIds "['i-xxx1','i-xxx2']"
```

### 關鍵配置

**告警分級:**
- P0: 5 分鐘響應，電話 + 短信 + 釘釘
- P1: 15 分鐘響應，短信 + 釘釘
- P2: 1 小時響應，釘釘
- P3: 4 小時響應，郵件

**成本優化优先级:**
1. 實例降配（低負載）
2. 購買節省計劃（長期）
3. OSS 存儲類型轉換
4. CDN 加速
5. 自動縮容

---

## 🔗 相關資源

- **雲監控**: https://cms.console.aliyun.com/
- **日誌服務**: https://sls.console.aliyun.com/
- **運維編排**: https://oos.console.aliyun.com/
- **費用中心**: https://usercenter2.aliyun.com/

---

**最後更新:** 2026-03-18 06:10  
**Day 4 狀態:** ✅ 學習中
