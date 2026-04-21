# 📦 Content Collector - Docker 化版本
# 使用 Playwright 官方鏡像，解決瀏覽器依賴問題
# 作者：麻小 | 創建：2026-03-19

# ==================== 基礎鏡像 ====================
# Playwright 官方鏡像，已預裝所有系統依賴和瀏覽器
FROM mcr.microsoft.com/playwright:v1.42.0-jammy

# ==================== 工作目錄 ====================
WORKDIR /app

# ==================== 安裝 Node.js 依賴 ====================
# 先複製 package 文件，利用 Docker 緩存層
COPY package*.json ./

# 安裝依賴（包括 Playwright）
RUN npm ci --only=production

# ==================== 複製源代碼 ====================
COPY index.js ./
COPY collector.py ./

# ==================== 安裝 Chromium（可選） ====================
# 官方鏡像已包含，但為了保險再執行一次
RUN npx playwright install chromium --with-deps

# ==================== 創建存儲目錄 ====================
RUN mkdir -p /app/collections/wechat/images \
             /app/collections/articles/images

# ==================== 環境變量 ====================
ENV COLLECTIONS_DIR=/app/collections
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV HOME=/root

# ==================== 健康檢查 ====================
# 檢查 Chromium 是否可用
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('playwright').chromium.launch()" || exit 1

# ==================== 啟動命令 ====================
# 支持兩種模式：
# 1. 命令行：node index.js "URL"
# 2. 交互模式：docker run -it 然後輸入 URL
CMD ["node", "index.js"]

# ==================== 鏡像信息 ====================
LABEL maintainer="麻小"
LABEL version="3.0.0-docker"
LABEL description="全自動內容收藏系統（Docker 化）"
LABEL tags="content-collector,wechat,playwright,docker"
