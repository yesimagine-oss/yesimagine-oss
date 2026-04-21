# 🐳 Content Collector - Docker 部署指南

**版本**: 3.0.0-docker  
**創建**: 2026-03-19  
**作者**: 麻小

---

## 📋 目錄

1. [快速開始](#快速開始)
2. [構建鏡像](#構建鏡像)
3. [使用方式](#使用方式)
4. [故障排查](#故障排查)
5. [生產部署](#生產部署)

---

## 🚀 快速開始

### 前提條件

- Docker 20.10+
- Docker Compose v2.0+
- 至少 2GB 可用內存
- 至少 500MB 磁盤空間

### 一鍵測試

```bash
# 進入技能目錄
cd ~/.openclaw/workspace/skills/content-collector

# 運行測試腳本
bash test-docker.sh -a
```

---

## 🔨 構建鏡像

### 手動構建

```bash
cd ~/.openclaw/workspace/skills/content-collector

# 構建鏡像
docker build -t content-collector:latest .

# 查看鏡像
docker images | grep content-collector
```

### 使用測試腳本

```bash
bash test-docker.sh --build
```

---

## 📖 使用方式

### 方式 1: 命令行模式（測試用）

```bash
# 抓取單篇文章
docker run --rm \
  -v ~/.openclaw/workspace/collections:/app/collections \
  -e COLLECTIONS_DIR=/app/collections \
  --network host \
  content-collector:latest \
  node index.js "https://mp.weixin.qq.com/s/xxx"
```

### 方式 2: 使用測試腳本

```bash
# 測試指定 URL
bash test-docker.sh -t "https://mp.weixin.qq.com/s/xxx"

# 測試所有預設 URL
bash test-docker.sh -a
```

### 方式 3: Docker Compose（生產用）

```bash
# 啟動服務模式（HTTP API）
docker-compose up -d collector-api

# 查看日誌
docker-compose logs -f collector-api

# 測試 API
curl -X POST http://localhost:3000/collect \
  -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/xxx"}'

# 停止服務
docker-compose down
```

### 方式 4: 定時任務模式

```bash
# 啟動定時抓取（每天 9 點）
docker-compose up -d collector-cron

# 查看日誌
docker-compose logs -f collector-cron
```

---

## 🐛 故障排查

### 問題 1: 構建失敗

```bash
# 清理 Docker 緩存
docker builder prune -a

# 重新構建
docker build --no-cache -t content-collector:latest .
```

### 問題 2: 容器啟動失敗

```bash
# 查看容器日誌
docker logs content-collector-cli

# 進入容器調試
docker run -it --rm \
  content-collector:latest \
  /bin/bash
```

### 問題 3: 抓取失敗

```bash
# 啟用調試模式
docker run --rm \
  -v ~/.openclaw/workspace/collections:/app/collections \
  -e DEBUG=true \
  --network host \
  content-collector:latest \
  node index.js "https://mp.weixin.qq.com/s/xxx"

# 查看調試截圖（如果有）
docker run --rm \
  -v /tmp:/tmp \
  content-collector:latest \
  cat /tmp/wechat-debug.png
```

### 問題 4: 權限問題

```bash
# 確保收藏目錄可寫
chmod -R 755 ~/.openclaw/workspace/collections

# 或使用 root 運行
docker run --rm \
  -u root \
  -v ~/.openclaw/workspace/collections:/app/collections \
  content-collector:latest \
  node index.js "https://..."
```

### 問題 5: 網絡問題（中國大陸）

```bash
# 使用代理
docker run --rm \
  -e HTTP_PROXY=http://proxy:port \
  -e HTTPS_PROXY=http://proxy:port \
  -v ~/.openclaw/workspace/collections:/app/collections \
  --network host \
  content-collector:latest \
  node index.js "https://..."
```

---

## 🏭 生產部署

### Docker Compose 完整配置

```yaml
version: '3.8'

services:
  collector:
    image: content-collector:latest
    container_name: content-collector-prod
    
    volumes:
      - /data/collections:/app/collections
    
    environment:
      - COLLECTIONS_DIR=/app/collections
      - TZ=Asia/Shanghai
    
    network_mode: host
    
    restart: unless-stopped
    
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### 系統服務（systemd）

```ini
# /etc/systemd/system/content-collector.service
[Unit]
Description=Content Collector Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/docker-compose -f /path/to/docker-compose.yml up -d
ExecStop=/usr/bin/docker-compose -f /path/to/docker-compose.yml down
User=root

[Install]
WantedBy=multi-user.target
```

```bash
# 啟用服務
sudo systemctl enable content-collector
sudo systemctl start content-collector
sudo systemctl status content-collector
```

---

## 📊 性能優化

### 鏡像大小優化

當前鏡像約 1.2GB，可通過以下方式優化：

1. **多階段構建** - 減少最終鏡像大小
2. **使用 Alpine** - 但可能缺少系統依賴
3. **清理緩存** - `npm cache clean --force`

### 啟動速度優化

1. **預拉取鏡像** - `docker pull content-collector:latest`
2. **使用本地卷** - 避免網絡存儲
3. **調整超時** - 根據網絡情況調整

---

## 📝 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 3.0.0-docker | 2026-03-19 | 首次 Docker 化 |
| 3.0.0 | 2026-03-18 | Playwright 版本 |

---

## 📞 支持

- 問題反饋：GitHub Issues
- 文檔：`README.md`
- 技能文檔：`SKILL.md`
