---
category: javascript
created_at: '2026-04-20'
tags:
- javascript
- auto-generated
title: Node.Js 核心概念
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
# Node.js 核心概念

**創建時間**: 2026-03-19  
**難度**: ⭐ 入門  
**參考文檔**: https://nodejs.org/docs/latest/api/

---

## 📚 Node.js 簡介

### 什麼是 Node.js？

Node.js 是一個基於 Chrome V8 引擎的 JavaScript 運行時，具有以下特點：
- **異步非阻塞 I/O**
- **事件驅動**
- **單線程**
- **跨平台**

### Node.js 能幹什麼？

| 應用場景 | 說明 | 示例 |
|---------|------|------|
| **Web 應用** | 後端服務器 | Express、Koa |
| **API 服務** | RESTful/GraphQL API | 接口開發 |
| **實時應用** | WebSocket 通信 | Socket.IO |
| **命令行工具** | CLI 工具開發 | npm 包 |
| **微服務** | 服務拆分 | Docker + Node.js |
| **數據處理** | 流式處理 | Stream |

---

## 🔧 環境配置

### 安裝 Node.js

```bash
# 查看版本
node --version
npm --version

# 升級 npm
npm install -g npm@latest

# 安裝常用全局包
npm install -g nodemon pm2 npx
```

### 初始化項目

```bash
# 創建項目
mkdir my-project && cd my-project
npm init -y

# 安裝依賴
npm install express
npm install -D nodemon jest eslint

# 項目結構
my-project/
├── package.json
├── src/
│   ├── index.js
│   ├── routes/
│   ├── controllers/
│   └── models/
└── tests/
```

---

## 📦 核心模塊

### 1. fs (文件系統)

```javascript
const fs = require('fs').promises;

// 讀取文件
const content = await fs.readFile('file.txt', 'utf-8');

// 寫入文件
await fs.writeFile('output.txt', 'Hello World');

// 檢查文件是否存在
try {
  await fs.access('file.txt');
  console.log('文件存在');
} catch {
  console.log('文件不存在');
}
```

### 2. path (路徑)

```javascript
const path = require('path');

// 路徑拼接
const fullPath = path.join(__dirname, 'src', 'index.js');

// 獲取擴展名
const ext = path.extname('file.txt'); // .txt

// 獲取文件名
const base = path.basename('/path/to/file.txt'); // file.txt
```

### 3. http (HTTP 服務器)

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ message: 'Hello World' }));
});

server.listen(3000, () => {
  console.log('服務器運行在 http://localhost:3000');
});
```

### 4. events (事件發射器)

```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const emitter = new MyEmitter();

// 監聽事件
emitter.on('event', (data) => {
  console.log('事件觸發:', data);
});

// 發送事件
emitter.emit('event', { message: 'Hello' });
```

### 5. stream (流)

```javascript
const fs = require('fs');

// 讀取流
const readStream = fs.createReadStream('large-file.txt');

// 寫入流
const writeStream = fs.createWriteStream('output.txt');

// 管道
readStream.pipe(writeStream);
```

---

## 🔄 異步編程

### 回調函數

```javascript
fs.readFile('file.txt', 'utf-8', (err, data) => {
  if (err) throw err;
  console.log(data);
});
```

### Promise

```javascript
fs.promises.readFile('file.txt', 'utf-8')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

### async/await (推薦)

```javascript
async function readFile() {
  try {
    const data = await fs.readFile('file.txt', 'utf-8');
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

---

## 🌐 Express 框架

### 基礎示例

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// GET 路由
app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});

// POST 路由
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  res.status(201).json({ id: 1, name, email });
});

app.listen(3000, () => {
  console.log('服務器運行在 http://localhost:3000');
});
```

### 中間件

```javascript
// 自定義中間件
const logger = (req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
};

app.use(logger);

// 錯誤處理中間件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: '服務器錯誤' });
});
```

---

## 📊 數據庫集成

### MongoDB (Mongoose)

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb');

const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  age: Number
});

const User = mongoose.model('User', userSchema);

// 創建用戶
const user = await User.create({ name: '小明', email: 'xiao@example.com', age: 18 });

// 查詢用戶
const users = await User.find({ age: { $gte: 18 } });
```

### MySQL (mysql2)

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb'
});

// 查詢
const [rows] = await pool.query('SELECT * FROM users WHERE age >= ?', [18]);

// 插入
const [result] = await pool.query('INSERT INTO users (name, email) VALUES (?, ?)', ['小明', 'xiao@example.com']);
```

### Redis (ioredis)

```javascript
const Redis = require('ioredis');
const redis = new Redis();

// 設置
await redis.set('key', 'value');

// 獲取
const value = await redis.get('key');

// 過期時間
await redis.setex('key', 3600, 'value'); // 1 小時過期
```

---

## 🔒 安全配置

### JWT 認證

```javascript
const jwt = require('jsonwebtoken');

// 生成 token
const token = jwt.sign({ userId: 1 }, 'secret-key', { expiresIn: '7d' });

// 驗證 token
const decoded = jwt.verify(token, 'secret-key');

// 中間件
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  try {
    req.user = jwt.verify(token, 'secret-key');
    next();
  } catch {
    res.status(401).json({ error: '未授權' });
  }
};
```

### CORS

```javascript
const cors = require('cors');

app.use(cors({
  origin: 'https://example.com',
  credentials: true
}));
```

### Helmet (安全頭部)

```javascript
const helmet = require('helmet');
app.use(helmet());
```

---

## 📋 最佳實踐

### 項目結構

```
project/
├── src/
│   ├── index.js          # 入口文件
│   ├── config/           # 配置文件
│   ├── controllers/      # 控制器
│   ├── models/           # 模型
│   ├── routes/           # 路由
│   ├── middleware/       # 中間件
│   └── utils/            # 工具函數
├── tests/                # 測試文件
├── .env                  # 環境變量
├── .gitignore
├── package.json
└── README.md
```

### 環境變量

```javascript
// .env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/mydb
JWT_SECRET=your-secret-key
NODE_ENV=development

// 使用
require('dotenv').config();
const port = process.env.PORT;
```

### 錯誤處理

```javascript
// 自定義錯誤類
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
  }
}

// 全局錯誤處理
app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({
    status: err.status,
    message: err.message
  });
});
```

---

## 📖 參考資源

- **官方文檔**: https://nodejs.org/docs/latest/api/
- **Express 文檔**: https://expressjs.com/
- **Node.js 最佳實踐**: https://github.com/goldbergyoni/nodebestpractices

---

**最後更新**: 2026-03-19


## 相關文檔

- [[Node.js 安裝指南]]
- [[Node.js-安裝指南]]
- [[Node.js-核心概念]]
