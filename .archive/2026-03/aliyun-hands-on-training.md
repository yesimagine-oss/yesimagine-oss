# 阿里雲控制台實操訓練營

**學習目標**: 通過實戰演練，熟練掌握阿里雲控制台操作，具備獨立運維能力  
**學習方式**: 邊學邊做，每個章節都有實操任務  
**預計時間**: 14 天（每天 2-3 小時）  
**適用對象**: 運維工程師、開發人員、技術負責人

---

## 📋 訓練營大綱

| 階段 | 天數 | 主題 | 實操項目 |
|------|------|------|---------|
| **階段 1** | Day 1-3 | 基礎操作 | 實例創建、環境配置 |
| **階段 2** | Day 4-7 | 核心服務 | SLB、RDS、OSS 實戰 |
| **階段 3** | Day 8-10 | 高級應用 | 監控、自動化、安全 |
| **階段 4** | Day 11-14 | 綜合實戰 | 完整項目部署 |

---

## 🎯 階段 1：基礎操作 (Day 1-3)

### Day 1：控制台熟悉與實例創建

#### 任務 1.1：登錄與界面熟悉 (30 分鐘)

**操作步驟**：
```
1. 訪問控制台：https://swas.console.aliyun.com/
2. 使用阿里雲賬號登錄
3. 熟悉界面佈局
   - 左側導航欄
   - 實例列表區
   - 快捷操作區
   - 監控概覽區
```

**檢查清單**：
- [ ] 成功登錄控制台
- [ ] 找到實例列表
- [ ] 查看實例詳情
- [ ] 了解區域和可用區概念

#### 任務 1.2：創建第一台實例 (1 小時)

**實操步驟**：
```
1. 點擊「創建實例」
2. 選擇配置：
   - 地域：華東 1（杭州）
   - 實例規格：2 核 2GB
   - 系統鏡像：Ubuntu 22.04
   - 數據盤：40GB SSD
   - 帶寬：5Mbps
3. 設置登錄密碼
4. 確認訂單並支付
5. 等待實例創建完成（約 3-5 分鐘）
```

**驗證步驟**：
```bash
# 本地終端 SSH 連接
ssh root@<實例公網 IP>

# 輸入密碼登錄
# 成功後查看系統信息
uname -a
lsb_release -a
```

#### 任務 1.3：基礎環境配置 (1 小時)

**實操腳本**：
```bash
#!/bin/bash
# init-server.sh - 服務器初始化腳本

# 1. 更新系統
apt-get update && apt-get upgrade -y

# 2. 安裝常用工具
apt-get install -y vim curl wget git htop net-tools

# 3. 配置 SSH
sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
systemctl restart sshd

# 4. 創建普通用戶
adduser deploy
usermod -aG sudo deploy

# 5. 設置時區
timedatectl set-timezone Asia/Shanghai

# 6. 查看配置
echo "=== 系統信息 ==="
hostnamectl
echo "=== 磁盤使用 ==="
df -h
echo "=== 內存使用 ==="
free -h
```

**執行步驟**：
```bash
# 上傳腳本
scp init-server.sh root@<IP>:/root/

# SSH 登錄執行
ssh root@<IP>
bash /root/init-server.sh
```

**作業**：
- [ ] 完成實例創建
- [ ] 成功 SSH 連接
- [ ] 執行初始化腳本
- [ ] 截圖保存實例詳情頁

---

### Day 2：防火牆與安全配置

#### 任務 2.1：配置防火牆規則 (45 分鐘)

**實操步驟**：
```
1. 進入實例詳情頁
2. 點擊「防火牆」標籤
3. 添加規則：

規則 1 - SSH:
- 端口：2222
- 協議：TCP
- 授權對象：您的家庭 IP/32
- 描述：SSH 管理

規則 2 - HTTP:
- 端口：80
- 協議：TCP
- 授權對象：0.0.0.0/0
- 描述：Web 服務

規則 3 - HTTPS:
- 端口：443
- 協議：TCP
- 授權對象：0.0.0.0/0
- 描述：HTTPS 服務

規則 4 - 應用端口:
- 端口：8080
- 協議：TCP
- 授權對象：0.0.0.0/0
- 描述：應用服務
```

**驗證步驟**：
```bash
# 查看防火牆規則
iptables -L -n

# 測試端口連通性
telnet <IP> 80
nc -zv <IP> 443
```

#### 任務 2.2：配置 SSH 密鑰認證 (45 分鐘)

**生成密鑰**：
```bash
# 本地生成 SSH 密鑰
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公鑰
cat ~/.ssh/id_ed25519.pub
```

**上傳公鑰**：
```bash
# 複製公鑰到服務器
ssh-copy-id -p 2222 root@<IP>

# 或手動添加
ssh root@<IP>
mkdir -p ~/.ssh
echo "你的公鑰內容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**測試密鑰登錄**：
```bash
# 使用密鑰登錄（無需密碼）
ssh -p 2222 root@<IP>

# 禁用密碼登錄（提高安全性）
sudo vim /etc/ssh/sshd_config
# 修改：PasswordAuthentication no
sudo systemctl restart sshd
```

#### 任務 2.3：安裝配置 Fail2Ban (30 分鐘)

**安裝與配置**：
```bash
# 安裝 Fail2Ban
apt-get install -y fail2ban

# 創建配置文件
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
EOF

# 啟動服務
systemctl enable fail2ban
systemctl start fail2ban

# 查看狀態
systemctl status fail2ban
fail2ban-client status sshd
```

**作業**：
- [ ] 配置 4 條防火牆規則
- [ ] 實現 SSH 密鑰登錄
- [ ] 安裝 Fail2Ban
- [ ] 截圖保存防火牆配置

---

### Day 3：快照備份與系統還原

#### 任務 3.1：創建手動快照 (30 分鐘)

**實操步驟**：
```
1. 進入實例詳情頁
2. 點擊「快照」標籤
3. 點擊「創建快照」
4. 填寫信息：
   - 快照名稱：before-app-deploy
   - 描述：應用部署前備份
   - 磁盤：系統盤
5. 確認創建
6. 等待完成（約 5-10 分鐘）
```

**驗證**：
```
- 查看快照列表
- 確認快照狀態為「完成」
- 記錄快照 ID
```

#### 任務 3.2：配置自動快照策略 (30 分鐘)

**實操步驟**：
```
1. 進入磁盤詳情頁
2. 點擊「自動快照策略」
3. 創建策略：
   - 策略名稱：daily-backup
   - 執行時間：02:00
   - 重複日期：每天
   - 保留天數：7 天
4. 應用到磁盤
5. 確認應用
```

**驗證命令**：
```bash
# 查看自動快照任務
aliyun ecs DescribeAutoSnapshotPolicyEx \
  --RegionId cn-hangzhou
```

#### 任務 3.3：系統還原演練 (1 小時)

**模擬故障**：
```bash
# 故意刪除重要文件
sudo rm -rf /etc/nginx
sudo rm -f /var/log/syslog

# 驗證文件已刪除
ls /etc/nginx
# 應該顯示：No such file or directory
```

**使用快照還原**：
```
1. 停止實例
2. 進入快照列表
3. 選擇之前的快照
4. 點擊「回滾磁盤」
5. 確認操作
6. 等待完成
7. 啟動實例
```

**驗證還原**：
```bash
# SSH 登錄驗證
ssh root@<IP>

# 檢查文件是否恢復
ls /etc/nginx
# 應該顯示配置文件

# 檢查日誌
ls /var/log/syslog
```

**作業**：
- [ ] 創建手動快照
- [ ] 配置自動快照策略
- [ ] 完成系統還原演練
- [ ] 記錄還原時間和步驟

---

## 🎯 階段 2：核心服務 (Day 4-7)

### Day 4：Web 服務部署實戰

#### 任務 4.1：安裝配置 Nginx (1 小時)

**安裝 Nginx**：
```bash
# 添加 Nginx 倉庫
apt-get install -y curl gnupg2 ca-certificates lsb-release
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
  | tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
  | tee /etc/apt/sources.list.d/nginx.list

# 安裝 Nginx
apt-get update
apt-get install -y nginx

# 啟動服務
systemctl enable nginx
systemctl start nginx
systemctl status nginx
```

**配置虛擬主機**：
```bash
# 創建網站目錄
mkdir -p /var/www/myapp
cat > /var/www/myapp/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>我的應用</title></head>
<body>
<h1>歡迎訪問！</h1>
<p>這是我的第一個 Web 應用</p>
<p>服務器時間：<?php echo date('Y-m-d H:i:s'); ?></p>
</body>
</html>
EOF

# 創建 Nginx 配置
cat > /etc/nginx/conf.d/myapp.conf << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/myapp;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
EOF

# 測試配置
nginx -t

# 重載配置
systemctl reload nginx
```

**驗證**：
```bash
# 本地測試
curl http://localhost

# 遠程測試
curl http://<實例 IP>

# 瀏覽器訪問
# http://<實例 IP>
```

#### 任務 4.2：安裝配置 PHP (45 分鐘)

**安裝 PHP**：
```bash
# 添加 PHP 倉庫
apt-get install -y software-properties-common
add-apt-repository ppa:ondrej/php -y
apt-get update

# 安裝 PHP 和常用擴展
apt-get install -y php8.2 php8.2-fpm php8.2-mysql \
  php8.2-curl php8.2-gd php8.2-mbstring php8.2-xml \
  php8.2-zip php8.2-intl

# 啟動 PHP-FPM
systemctl enable php8.2-fpm
systemctl start php8.2-fpm
systemctl status php8.2-fpm
```

**創建測試頁面**：
```bash
# 創建 PHP 測試文件
cat > /var/www/myapp/info.php << 'EOF'
<?php
phpinfo();
?>
EOF

# 設置權限
chown -R www-data:www-data /var/www/myapp
chmod -R 755 /var/www/myapp
```

**驗證**：
```bash
# 訪問 PHP 信息頁
curl http://<IP>/info.php

# 應該看到 PHP 配置信息
```

#### 任務 4.3：部署 WordPress (1 小時)

**準備數據庫**：
```bash
# 安裝 MySQL 客戶端
apt-get install -y mysql-client

# 連接 RDS（或本地 MySQL）
mysql -h <RDS 地址> -u root -p

# 創建數據庫
CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8mb4;
CREATE USER 'wpuser'@'%' IDENTIFIED BY '強密碼';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'%';
FLUSH PRIVILEGES;
EXIT;
```

**下載配置 WordPress**：
```bash
# 下載 WordPress
cd /var/www
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
mv wordpress myapp
rm latest.tar.gz

# 配置 WordPress
cd /var/www/myapp
cp wp-config-sample.php wp-config.php

# 編輯配置文件
vim wp-config.php
# 修改以下內容：
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wpuser' );
define( 'DB_PASSWORD', '強密碼' );
define( 'DB_HOST', '<RDS 地址>' );

# 設置權限
chown -R www-data:www-data /var/www/myapp
chmod -R 755 /var/www/myapp
```

**完成安裝**：
```
1. 瀏覽器訪問：http://<IP>
2. 選擇語言：簡體中文
3. 填寫網站信息
4. 安裝 WordPress
5. 登錄後台
```

**作業**：
- [ ] 成功安裝 Nginx
- [ ] 成功安裝 PHP
- [ ] 部署 WordPress
- [ ] 截圖保存網站首頁

---

### Day 5：RDS 雲數據庫實戰

#### 任務 5.1：創建 RDS 實例 (45 分鐘)

**實操步驟**：
```
1. 訪問：https://rds.console.aliyun.com/
2. 點擊「創建實例」
3. 選擇配置：
   - 地域：與 ECS 相同
   - 引擎：MySQL 8.0
   - 系列：高可用版
   - 規格：2 核 4GB
   - 存儲：100GB SSD
   - 可用區：隨機分配
4. 設置白名單：
   - 添加 ECS 內網 IP
   - 添加本地 IP（用於管理）
5. 設置賬號密碼
6. 確認訂單
```

**驗證連接**：
```bash
# 從 ECS 連接
mysql -h <RDS 內網地址> -u root -p

# 測試創建數據庫
CREATE DATABASE testdb;
SHOW DATABASES;
EXIT;
```

#### 任務 5.2：配置數據庫參數 (45 分鐘)

**修改參數**：
```
1. RDS 控制台 → 參數設置
2. 修改參數：

性能相關:
- max_connections: 2000
- innodb_buffer_pool_size: 70% 內存
- innodb_flush_log_at_trx_commit: 2

日誌相關:
- slow_query_log: ON
- long_query_time: 2

3. 點擊「應用參數」
4. 等待重啟生效
```

**驗證**：
```sql
-- 查看參數
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- 查看慢查詢
SHOW VARIABLES LIKE 'slow_query_log';
```

#### 任務 5.3：數據備份與恢復 (1 小時)

**創建備份**：
```
1. RDS 控制台 → 備份恢復
2. 點擊「備份實例」
3. 選擇備份方式：邏輯備份
4. 確認備份
5. 等待完成
```

**數據恢復演練**：
```bash
# 1. 創建測試數據
mysql -h <RDS 地址> -u root -p << 'EOF'
CREATE DATABASE backup_test;
USE backup_test;
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100)
);
INSERT INTO users VALUES (1, '張三', 'zhangsan@test.com');
INSERT INTO users VALUES (2, '李四', 'lisi@test.com');
SELECT * FROM users;
EOF

# 2. 記錄數據

# 3. 模擬數據丟失
mysql -h <RDS 地址> -u root -p << 'EOF'
DROP DATABASE backup_test;
SHOW DATABASES;
EOF

# 4. 從備份恢復
# RDS 控制台 → 備份恢復 → 恢復實例
# 選擇備份集 → 恢復到新實例

# 5. 驗證數據
mysql -h <新 RDS 地址> -u root -p << 'EOF'
USE backup_test;
SELECT * FROM users;
EOF
```

**作業**：
- [ ] 創建 RDS 實例
- [ ] 配置數據庫參數
- [ ] 完成備份恢復演練
- [ ] 記錄恢復時間

---

### Day 6：OSS 對象存儲實戰

#### 任務 6.1：創建 Bucket (30 分鐘)

**實操步驟**：
```
1. 訪問：https://oss.console.aliyun.com/
2. 點擊「創建 Bucket」
3. 配置：
   - 名稱：myapp-storage（全局唯一）
   - 地域：與 ECS 相同
   - 權限：私有
   - 存儲類型：標準存儲
4. 確認創建
```

#### 任務 6.2：使用 ossutil 管理 OSS (1 小時)

**安裝配置**：
```bash
# 下載 ossutil
wget https://gosspublic.alicdn.com/ossutil/1.7.13/ossutil64
chmod +x ossutil64
mv ossutil64 /usr/local/bin/ossutil

# 配置
ossutil config
# 輸入：
# Endpoint: oss-cn-hangzhou.aliyuncs.com
# AccessKeyID: <您的 AK>
# AccessKeySecret: <您的 SK>
```

**上傳下載**：
```bash
# 上傳文件
ossutil cp /var/www/myapp/wp-content/uploads oss://myapp-storage/uploads -r

# 上傳網站靜態資源
ossutil cp /var/www/myapp/wp-content/themes oss://myapp-storage/themes -r

# 下載文件
ossutil cp oss://myapp-storage/uploads/image.jpg ./image.jpg

# 列出文件
ossutil ls oss://myapp-storage

# 刪除文件
ossutil rm oss://myapp-storage/uploads/old-image.jpg
```

#### 任務 6.3：配置 CDN 加速 (1 小時)

**實操步驟**：
```
1. 訪問：https://cdn.console.aliyun.com/
2. 點擊「添加域名」
3. 配置：
   - 加速域名：static.yourdomain.com
   - 業務類型：圖片小文件
   - 源站類型：OSS 域名
   - 源站地址：myapp-storage.oss-cn-hangzhou.aliyuncs.com
4. 確認添加
5. 配置 CNAME
   - 到域名解析處添加 CNAME 記錄
   - 值為 CDN 分配的域名
```

**驗證**：
```bash
# 查看 CDN 狀態
curl -I http://static.yourdomain.com/image.jpg

# 應該看到 X-Cache 頭顯示 HIT 或 MISS
```

**作業**：
- [ ] 創建 OSS Bucket
- [ ] 使用 ossutil 上傳文件
- [ ] 配置 CDN 加速
- [ ] 測試 CDN 訪問

---

### Day 7：SLB 負載均衡實戰

#### 任務 7.1：創建第二台 ECS (30 分鐘)

**實操步驟**：
```
1. 使用第一台 ECS 的快照創建鏡像
2. 使用鏡像創建第二台 ECS
3. 配置相同的安全組規則
4. 記錄兩台 ECS 的內網 IP
```

#### 任務 7.2：創建 SLB 實例 (45 分鐘)

**實操步驟**：
```
1. 訪問：https://slb.console.aliyun.com/
2. 點擊「創建實例」
3. 配置：
   - 地域：與 ECS 相同
   - 實例規格：性能保障型
   - 網絡類型：VPC
   - 帶寬：按使用量
4. 確認創建
```

#### 任務 7.3：配置監聽和後端服務器 (1 小時)

**配置監聽**：
```
1. SLB 控制台 → 實例詳情
2. 點擊「聽眾」標籤
3. 點擊「添加監聽」
4. 配置：
   - 協議：HTTP
   - 端口：80
   - 後端協議：HTTP
   - 後端端口：80
   - 健康檢查：開啟
   - 檢查路徑：/
   - 檢查間隔：5 秒
5. 確認添加
```

**添加後端服務器**：
```
1. 點擊「後端服務器」標籤
2. 點擊「添加後端服務器」
3. 選擇兩台 ECS
4. 設置權重：都為 100
5. 確認添加
```

**驗證**：
```bash
# 多次請求 SLB
for i in {1..10}; do
  curl http://<SLB 公網 IP>
  echo ""
done

# 應該看到請求被分發到兩台服務器
```

**作業**：
- [ ] 創建第二台 ECS
- [ ] 創建 SLB 實例
- [ ] 配置負載均衡
- [ ] 驗證流量分發

---

## 🎯 階段 3：高級應用 (Day 8-10)

### Day 8：監控與告警實戰

#### 任務 8.1：配置雲監控 (1 小時)

**安裝監控插件**：
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

**配置告警規則**：
```
1. 訪問：https://cms.console.aliyun.com/
2. 點擊「告警」→「創建告警」
3. 配置 CPU 告警：
   - 監控項：CPU 使用率
   - 統計週期：1 分鐘
   - 連續次數：3 次
   - 閾值：> 80%
   - 通知方式：郵件 + 短信
4. 配置內存告警：
   - 監控項：內存使用率
   - 閾值：> 85%
5. 配置磁盤告警：
   - 監控項：磁盤使用率
   - 閾值：> 80%
```

**驗證告警**：
```bash
# 模擬 CPU 高負載
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &

# 等待 3-5 分鐘，應該收到告警通知

# 停止壓力測試
pkill yes
```

#### 任務 8.2：配置釘釘通知 (45 分鐘)

**創建釘釘機器人**：
```
1. 打開釘釘群
2. 群設置 → 智能助手 → 添加機器人
3. 選擇「自定義」
4. 填寫機器人名稱
5. 獲取 Webhook URL
```

**配置雲監控通知**：
```
1. 雲監控控制台 → 告警 → 通知方式
2. 點擊「添加通知方式」
3. 選擇「Webhook」
4. 填寫釘釘 Webhook URL
5. 測試發送
```

**作業**：
- [ ] 安裝監控插件
- [ ] 配置 3 個告警規則
- [ ] 配置釘釘通知
- [ ] 測試告警觸發

---

### Day 9：自動化部署實戰

#### 任務 9.1：配置 Git 倉庫 (45 分鐘)

**創建 GitHub 倉庫**：
```
1. 訪問 GitHub
2. 創建新倉庫：myapp-deploy
3. 初始化 README
4. 克隆到本地
```

**準備部署腳本**：
```bash
#!/bin/bash
# deploy.sh

# 拉取代碼
git pull origin main

# 安裝依賴
composer install --no-dev --optimize-autoloader
npm install --production

# 執行遷移
php artisan migrate --force

# 清除緩存
php artisan cache:clear
php artisan config:cache

# 重載 PHP-FPM
systemctl reload php8.2-fpm

echo "部署完成！"
```

#### 任務 9.2：配置 GitHub Actions (1 小時)

**創建 workflow 文件**：
```yaml
# .github/workflows/deploy.yml
name: Deploy to Aliyun

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Aliyun
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_IP }}
        username: root
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        port: 2222
        script: |
          cd /var/www/myapp
          git pull origin main
          composer install --no-dev
          php artisan migrate --force
          systemctl reload php8.2-fpm
```

**配置 Secrets**：
```
1. GitHub 倉庫 → Settings → Secrets
2. 添加：
   - SERVER_IP: 服務器 IP
   - SSH_PRIVATE_KEY: SSH 私鑰
```

**測試部署**：
```bash
# 本地修改代碼
echo "<!-- 測試部署 -->" >> index.php

# 提交推送
git add .
git commit -m "測試自動部署"
git push origin main

# 查看 GitHub Actions 執行狀態
# 訪問：https://github.com/用戶/倉庫/actions
```

**作業**：
- [ ] 創建 Git 倉庫
- [ ] 編寫部署腳本
- [ ] 配置 GitHub Actions
- [ ] 測試自動部署

---

### Day 10：安全加固實戰

#### 任務 10.1：配置 WAF 防火牆 (1 小時)

**實操步驟**：
```
1. 訪問：https://waf.console.aliyun.com/
2. 購買 WAF 實例（可選免費版）
3. 添加域名
4. 配置防護規則：
   - SQL 注入防護
   - XSS 防護
   - Webshell 防護
   - CC 攻擊防護
5. 修改 DNS 解析
   - 將域名 CNAME 到 WAF 提供的地址
```

#### 任務 10.2：配置 SSL 證書 (45 分鐘)

**申請免費證書**：
```
1. 訪問：https://ssl.console.aliyun.com/
2. 點擊「免費證書」
3. 申請證書：
   - 域名：yourdomain.com
   - 驗證方式：DNS 驗證
4. 添加 DNS 記錄
5. 等待驗證通過
6. 下載證書
```

**配置 HTTPS**：
```bash
# 上傳證書到服務器
scp cert.pem root@<IP>:/etc/ssl/
scp key.pem root@<IP>:/etc/ssl/

# 配置 Nginx
cat > /etc/nginx/conf.d/https.conf << 'EOF'
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    root /var/www/myapp;
    index index.php index.html;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}

# HTTP 強制跳轉 HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
EOF

# 測試並重載
nginx -t
systemctl reload nginx
```

**作業**：
- [ ] 配置 WAF 防護
- [ ] 申請 SSL 證書
- [ ] 配置 HTTPS
- [ ] 測試強制跳轉

---

## 🎯 階段 4：綜合實戰 (Day 11-14)

### Day 11-14：完整電商平台部署

#### 項目需求

**業務場景**：
- 電商網站
- 日均訪問：1000 UV
- 商品數量：500+
- 訂單系統
- 用戶系統
- 支付對接

#### 技術架構

```
                    用戶
                     ↓
                CDN 加速
                     ↓
              WAF 防火牆
                     ↓
              SLB 負載均衡
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
   (緩存)      (主從複製)    (商品圖片)
```

#### 部署清單

**Day 11：基礎設施**
- [ ] 創建 VPC 網絡
- [ ] 創建 3 台 ECS 實例
- [ ] 配置安全組
- [ ] 安裝基礎環境

**Day 12：數據庫與緩存**
- [ ] 創建 RDS 實例
- [ ] 創建 Redis 實例
- [ ] 導入數據庫結構
- [ ] 配置連接池

**Day 13：應用部署**
- [ ] 部署電商系統代碼
- [ ] 配置負載均衡
- [ ] 配置 CDN 加速
- [ ] 配置 SSL 證書

**Day 14：監控與驗收**
- [ ] 配置監控告警
- [ ] 壓力測試
- [ ] 故障演練
- [ ] 文檔整理

---

## 📋 實操考核清單

### 基礎技能 (必考)

- [ ] 創建 ECS 實例
- [ ] SSH 連接配置
- [ ] 防火牆規則配置
- [ ] 快照創建與還原
- [ ] 基礎環境搭建

### 核心技能 (必考)

- [ ] Nginx 配置與優化
- [ ] PHP 環境搭建
- [ ] RDS 數據庫管理
- [ ] OSS 文件存儲
- [ ] SLB 負載均衡

### 高級技能 (選考)

- [ ] 監控告警配置
- [ ] CI/CD 流水線
- [ ] WAF 安全防護
- [ ] SSL 證書配置
- [ ] 自動化腳本

### 綜合實戰 (必考)

- [ ] 完整項目部署
- [ ] 故障排查能力
- [ ] 性能優化能力
- [ ] 文檔編寫能力

---

## 🏆 畢業項目

### 項目要求

獨立部署一個完整的 Web 應用，包括：

1. **基礎設施**
   - 至少 2 台 ECS 實例
   - SLB 負載均衡
   - RDS 數據庫
   - OSS 存儲

2. **應用部署**
   - Web 服務器（Nginx/Apache）
   - 運行環境（PHP/Node.js/Python）
   - 數據庫連接
   - 緩存配置

3. **安全配置**
   - 防火牆規則
   - SSH 密鑰認證
   - SSL 證書
   - 備份策略

4. **監控運維**
   - 監控指標
   - 告警通知
   - 日誌收集
   - 自動化部署

### 提交材料

- [ ] 架構圖
- [ ] 部署文檔
- [ ] 運維手冊
- [ ] 應急預案
- [ ] 成本預算
- [ ] 演示視頻

---

## 📚 參考資源

### 官方文檔
- [阿里雲幫助中心](https://help.aliyun.com/)
- [API 文檔](https://next.api.aliyun.com/)
- [最佳實踐](https://www.aliyun.com/solution/)

### 社區資源
- [阿里雲開發者社區](https://developer.aliyun.com/)
- [GitHub 示例](https://github.com/aliyun)

### 工具下載
- [ossutil](https://help.aliyun.com/document_detail/50452.html)
- [CLI 工具](https://help.aliyun.com/document_detail/119477.html)
- [監控插件](https://help.aliyun.com/document_detail/97644.html)

---

**祝學習順利！有任何問題隨時詢問！** 🚀

**最後更新**: 2026-03-16  
**版本**: v1.0  
**實操項目**: 20+  
**預計完成時間**: 14 天
