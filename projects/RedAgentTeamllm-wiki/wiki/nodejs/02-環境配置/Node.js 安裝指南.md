---
category: javascript
created_at: '2026-04-20'
tags:
- javascript
- auto-generated
title: Node.Js 安裝指南
type: article
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
# Node.js 安裝指南

**創建時間**: 2026-03-19  
**難度**: ⭐ 入門  
**參考文檔**: https://nodejs.org/en/download/

---

## 📋 系統要求

| 系統 | 要求 | 推薦 |
|------|------|------|
| **Linux** | 內核 4.0+ | 8.0+ |
| **macOS** | 10.15+ | 12.0+ |
| **Windows** | 10+ | 11+ |
| **內存** | 512MB | 2GB+ |
| **磁盤** | 500MB | 5GB+ |

---

## 🚀 安裝方法

### 方法 1: 官方安裝包 (推薦)

```bash
# 訪問官網下載
# https://nodejs.org/

# LTS 版本 (長期支持)
# Current 版本 (最新特性)

# 驗證安裝
node --version
npm --version
```

### 方法 2: 包管理器

#### Ubuntu/Debian

```bash
# 使用 NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 驗證
node --version
npm --version
```

#### CentOS/RHEL

```bash
# 使用 NodeSource
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs

# 驗證
node --version
npm --version
```

#### macOS

```bash
# 使用 Homebrew
brew install node

# 驗證
node --version
npm --version
```

### 方法 3: 版本管理工具 (推薦開發者)

#### nvm (Node Version Manager)

```bash
# 安裝 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安裝 Node.js
nvm install 20  # 安裝 v20
nvm use 20      # 使用 v20
nvm alias default 20  # 設置默認

# 切換版本
nvm install 18
nvm use 18

# 查看已安裝版本
nvm ls
```

#### fnm (Fast Node Manager)

```bash
# 安裝 fnm
curl -fsSL https://fnm.vercel.app/install | bash

# 安裝 Node.js
fnm use --install-if-missing 20

# 切換版本
fnm use 18
```

---

## ⚙️ 配置 npm

### 配置鏡像源

```bash
# 使用淘寶鏡像
npm config set registry https://registry.npmmirror.com

# 查看配置
npm config get registry

# 恢復官方源
npm config set registry https://registry.npmjs.org
```

### 全局包位置

```bash
# 查看全局包位置
npm root -g
npm bin -g

# 修改全局包位置 (可選)
npm config set prefix '~/.npm-global'

# 添加到 PATH
export PATH=~/.npm-global/bin:$PATH
```

---

## 📦 常用全局包

```bash
# 開發工具
npm install -g nodemon      # 自動重啟
npm install -g pm2          # 進程管理
npm install -g npx          # 執行包
npm install -g yarn         # 包管理器
npm install -g pnpm         # 包管理器

# 脚手架工具
npm install -g create-react-app
npm install -g express-generator
npm install -g vue-cli
npm install -g typescript

# 驗證安裝
nodemon --version
pm2 --version
```

---

## 🔍 驗證安裝

### 基礎驗證

```bash
# 檢查版本
node --version  # v20.x.x
npm --version   # 10.x.x

# 運行 Hello World
node -e "console.log('Hello World')"

# 創建測試項目
mkdir test-project && cd test-project
npm init -y
node -e "console.log(require('./package.json'))"
```

### 創建簡單服務器

```javascript
// test.js
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('服務器運行在 http://localhost:3000');
});
```

```bash
# 運行
node test.js

# 訪問
curl http://localhost:3000
```

---

## 🐛 常見問題

### 問題 1: 權限錯誤

```bash
# 錯誤：EACCES: permission denied
# 解決：修改全局包權限

sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules
```

### 問題 2: 版本衝突

```bash
# 使用 nvm 管理多版本
nvm install 18
nvm install 20
nvm use 20

# 或使用 n 管理
npm install -g n
n 20
```

### 問題 3: 網絡問題

```bash
# 配置鏡像源
npm config set registry https://registry.npmmirror.com

# 或使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install <package>
```

---

## 📖 參考資源

- **Node.js 官網**: https://nodejs.org/
- **npm 官網**: https://www.npmjs.com/
- **NodeSource**: https://nodesource.com/

---

**最後更新**: 2026-03-19


## 相關文檔

- [[Node.js-安裝指南]]
- [[Node.js 核心概念]]
- [[Node.js-核心概念]]
