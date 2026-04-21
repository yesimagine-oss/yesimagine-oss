# 📚 阿里雲工作臺學習筆記 - Day 3

**學習時間:** 2026-03-18  
**學習主題:** 實戰訓練 - Web 應用部署  
**參考資料:** 
- `aliyun-hands-on-training.md`
- `aliyun-swas-deep-study.md`
- `aliyun-enterprise-ops.md`

---

## Day 3 - 2026-03-18：實戰訓練

### 1. 部署 Web 應用（Nginx + PHP + MySQL）

#### 1.1 安裝配置 Nginx

**安裝步驟:**
```bash
# 1. 添加 Nginx 官方倉庫
apt-get install -y curl gnupg2 ca-certificates lsb-release
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
  | tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
  | tee /etc/apt/sources.list.d/nginx.list

# 2. 安裝 Nginx
apt-get update
apt-get install -y nginx

# 3. 啟動服務
systemctl enable nginx
systemctl start nginx
systemctl status nginx
```

**驗證安裝:**
```bash
# 查看版本
nginx -v

# 測試配置文件
nginx -t

# 本地訪問
curl http://localhost
# 應該看到 Nginx 歡迎頁面
```

#### 1.2 配置虛擬主機

**創建網站目錄:**
```bash
mkdir -p /var/www/myapp
```

**創建測試頁面:**
```html
<!-- /var/www/myapp/index.html -->
<!DOCTYPE html>
<html>
<head><title>我的應用</title></head>
<body>
<h1>歡迎訪問！</h1>
<p>這是我的第一個 Web 應用</p>
<p>服務器時間：<?php echo date('Y-m-d H:i:s'); ?></p>
</body>
</html>
```

**Nginx 配置文件:**
```nginx
# /etc/nginx/conf.d/myapp.conf
server {
    listen 80;
    server_name _;
    root /var/www/myapp;
    index index.html index.htm index.php;

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
```

**重載配置:**
```bash
nginx -t                  # 測試配置
systemctl reload nginx    # 重載配置
```

#### 1.3 安裝配置 PHP

**安裝 PHP 和擴展:**
```bash
# 1. 添加 PHP 倉庫
apt-get install -y software-properties-common
add-apt-repository ppa:ondrej/php -y
apt-get update

# 2. 安裝 PHP 8.2 和常用擴展
apt-get install -y php8.2 php8.2-fpm php8.2-mysql \
  php8.2-curl php8.2-gd php8.2-mbstring php8.2-xml \
  php8.2-zip php8.2-intl

# 3. 啟動 PHP-FPM
systemctl enable php8.2-fpm
systemctl start php8.2-fpm
systemctl status php8.2-fpm
```

**創建 PHP 測試頁:**
```php
<?php
// /var/www/myapp/info.php
phpinfo();
?>
```

**設置權限:**
```bash
chown -R www-data:www-data /var/www/myapp
chmod -R 755 /var/www/myapp
```

**驗證:**
```bash
curl http://<實例 IP>/info.php
# 應該看到 PHP 配置信息
```

#### 1.4 部署 WordPress

**準備數據庫:**
```bash
# 安裝 MySQL 客戶端
apt-get install -y mysql-client

# 連接數據庫（RDS 或本地 MySQL）
mysql -h <數據庫地址> -u root -p

# 創建數據庫和用戶
CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8mb4;
CREATE USER 'wpuser'@'%' IDENTIFIED BY '強密碼';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'%';
FLUSH PRIVILEGES;
EXIT;
```

**下載配置 WordPress:**
```bash
# 1. 下載 WordPress
cd /var/www
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
mv wordpress myapp
rm latest.tar.gz

# 2. 配置文件
cd /var/www/myapp
cp wp-config-sample.php wp-config.php

# 3. 編輯 wp-config.php
vim wp-config.php
# 修改：
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wpuser' );
define( 'DB_PASSWORD', '強密碼' );
define( 'DB_HOST', '<數據庫地址>' );

# 4. 設置權限
chown -R www-data:www-data /var/www/myapp
chmod -R 755 /var/www/myapp
```

**完成安裝:**
```
1. 瀏覽器訪問：http://<實例 IP>
2. 選擇語言：簡體中文
3. 填寫網站信息（網站標題、管理員賬號、密碼、郵箱）
4. 安裝 WordPress
5. 登錄後台：http://<IP>/wp-admin
```

---

### 2. 配置數據庫（RDS 或自建）

#### 2.1 創建 RDS 實例

**實操步驟:**
```
1. 訪問：https://rds.console.aliyun.com/
2. 點擊「創建實例」
3. 選擇配置：
   - 地域：與 ECS 相同（內網互通）
   - 引擎：MySQL 8.0
   - 系列：高可用版
   - 規格：2 核 4GB（入門）
   - 存儲：100GB SSD
   - 可用區：隨機分配
4. 設置白名單：
   - 添加 ECS 內網 IP
   - 添加本地 IP（用於管理）
5. 設置賬號密碼
6. 確認訂單並支付
```

**驗證連接:**
```bash
# 從 ECS 連接（內網）
mysql -h <RDS 內網地址> -u root -p

# 測試創建數據庫
CREATE DATABASE testdb;
SHOW DATABASES;
EXIT;
```

#### 2.2 配置數據庫參數

**修改參數:**
```
1. RDS 控制台 → 參數設置
2. 修改參數：

性能相關:
- max_connections: 2000
- innodb_buffer_pool_size: 70% 內存
- innodb_flush_log_at_trx_commit: 2（性能優先）

日誌相關:
- slow_query_log: ON
- long_query_time: 2（秒）

3. 點擊「應用參數」
4. 等待重啟生效
```

**驗證參數:**
```sql
-- 查看參數
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'slow_query_log';
```

#### 2.3 數據備份與恢復

**創建備份:**
```
1. RDS 控制台 → 備份恢復
2. 點擊「備份實例」
3. 選擇備份方式：邏輯備份 / 物理備份
4. 確認備份
5. 等待完成
```

**數據恢復演練:**
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

# 2. 記錄數據（截圖或保存）

# 3. 模擬數據丟失
mysql -h <RDS 地址> -u root -p << 'EOF'
DROP DATABASE backup_test;
SHOW DATABASES;
EOF

# 4. 從備份恢復
# RDS 控制台 → 備份恢復 → 恢復實例
# 選擇備份集 → 恢復到新實例 / 原實例

# 5. 驗證數據
mysql -h <恢復後地址> -u root -p << 'EOF'
USE backup_test;
SELECT * FROM users;
EOF
```

---

### 3. 搭建開發環境

#### 3.1 安裝 Git

```bash
# 安裝 Git
apt-get install -y git

# 配置 Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 生成 SSH 密鑰
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# 複製公鑰到 GitHub/GitLab
```

#### 3.2 安裝 Node.js（前端開發）

```bash
# 安裝 Node.js（使用 NodeSource）
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# 驗證
node -v
npm -v

# 安裝常用全局包
npm install -g yarn pm2
```

#### 3.3 安裝 Docker（容器化開發）

```bash
# 安裝 Docker
curl -fsSL https://get.docker.com | bash
systemctl enable docker
systemctl start docker

# 添加用戶到 docker 組
usermod -aG docker $USER

# 驗證
docker --version
docker run hello-world
```

#### 3.4 安裝常用開發工具

```bash
# 安裝工具
apt-get install -y \
  vim \
  curl \
  wget \
  git \
  htop \
  net-tools \
  jq \
  tree \
  zip \
  unzip \
  build-essential

# 安裝 Redis 客戶端
apt-get install -y redis-tools

# 安裝 MySQL 客戶端
apt-get install -y mysql-client
```

---

### 4. 備份與恢復實戰

#### 4.1 系統快照備份

**創建手動快照:**
```
1. 實例詳情頁 → 快照 → 創建快照
2. 選擇磁盤：系統盤
3. 填寫名稱：before-app-deploy
4. 描述：應用部署前備份
5. 確認創建
6. 等待完成（5-10 分鐘）
```

**配置自動快照策略:**
```
1. 磁盤詳情頁 → 自動快照策略
2. 創建策略：
   - 名稱：daily-backup
   - 時間：02:00
   - 重複：每天
   - 保留：7 天
3. 應用到磁盤
```

#### 4.2 數據庫備份

**RDS 自動備份:**
```
- 自動備份：每天一次，保留 7-730 天
- 手動備份：隨時創建，長期保留
- 備份下載：可下載到本地
```

**MySQL 手動備份:**
```bash
# 全庫備份
mysqldump -h <RDS 地址> -u root -p \
  --all-databases > all-databases.sql

# 單庫備份
mysqldump -h <RDS 地址> -u root -p \
  wordpress > wordpress.sql

# 壓縮備份
mysqldump -h <RDS 地址> -u root -p \
  wordpress | gzip > wordpress.sql.gz

# 恢復數據
mysql -h <RDS 地址> -u root -p < wordpress.sql
zcat wordpress.sql.gz | mysql -h <RDS 地址> -u root -p
```

#### 4.3 文件備份

**使用 rsync 備份:**
```bash
# 備份到本地
rsync -avz -e ssh root@<IP>:/var/www/myapp /backup/

# 備份到 OSS
ossutil cp /var/www/myapp oss://myapp-storage/backup -r
```

**使用 tar 打包:**
```bash
# 創建備份包
tar -czf myapp-backup-$(date +%Y%m%d).tar.gz /var/www/myapp

# 解壓備份
tar -xzf myapp-backup-20260318.tar.gz -C /
```

#### 4.4 系統還原演練

**使用快照還原:**
```
1. 停止實例（必須）
2. 快照詳情頁 → 創建磁盤
3. 選擇原實例
4. 確認還原（會覆蓋現有數據）
5. 啟動實例
6. 驗證還原結果
```

**驗證還原:**
```bash
# SSH 登錄
ssh root@<IP>

# 檢查文件
ls /var/www/myapp
ls /etc/nginx

# 檢查數據庫
mysql -h <RDS 地址> -u root -p
SHOW DATABASES;
```

---

## 📝 Day 3 學習總結

### 掌握的要點

| 模塊 | 核心技能 |
|------|---------|
| **Web 部署** | Nginx 安裝、PHP 配置、WordPress 部署 |
| **數據庫** | RDS 創建、參數配置、備份恢復 |
| **開發環境** | Git、Node.js、Docker、常用工具 |
| **備份恢復** | 系統快照、數據庫備份、文件備份、還原演練 |

### 實操命令速查

**Nginx:**
```bash
systemctl status nginx      # 查看狀態
systemctl reload nginx      # 重載配置
nginx -t                    # 測試配置
```

**PHP:**
```bash
systemctl status php8.2-fpm # 查看狀態
php -v                      # 查看版本
```

**MySQL:**
```bash
mysqldump -h <地址> -u root -p wordpress > backup.sql
mysql -h <地址> -u root -p < backup.sql
```

**備份:**
```bash
tar -czf backup.tar.gz /path/to/backup
tar -xzf backup.tar.gz -C /
```

### 關鍵配置

**Nginx 虛擬主機:**
```nginx
server {
    listen 80;
    server_name _;
    root /var/www/myapp;
    
    location ~ \.php$ {
        fastcgi_pass unix:/run/php/php-fpm.sock;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

**WordPress 數據庫配置:**
```php
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wpuser' );
define( 'DB_PASSWORD', '強密碼' );
define( 'DB_HOST', '<RDS 地址>' );
```

### 待深入研究的內容

- [ ] Nginx 性能優化（緩存、Gzip）
- [ ] PHP-FPM 調優
- [ ] MySQL 性能調優
- [ ] Redis 緩存配置
- [ ] CDN 加速配置
- [ ] HTTPS 證書配置

---

## 🔗 相關資源

- **Nginx 官方文檔**: https://nginx.org/en/docs/
- **WordPress 文檔**: https://wordpress.org/support/
- **阿里雲 RDS**: https://help.aliyun.com/product/26216.html
- **阿里雲 OSS**: https://help.aliyun.com/product/31815.html

---

**最後更新:** 2026-03-18 06:00  
**Day 3 狀態:** ✅ 學習中
