---
category: javascript
created_at: '2026-04-20'
tags:
- javascript
- auto-generated
title: Express 實戰
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
# Node.js Web 開發實戰

**創建時間**: 2026-03-19  
**難度**: ⭐⭐⭐ 進階  
**參考文檔**: https://expressjs.com/

---

## 🌐 Express 框架

### 快速開始

```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(PORT, () => {
  console.log(`服務器運行在 http://localhost:${PORT}`);
});
```

### 路由管理

```javascript
const express = require('express');
const router = express.Router();

// GET 路由
router.get('/users', (req, res) => {
  res.json({ users: [] });
});

// POST 路由
router.post('/users', (req, res) => {
  const { name, email } = req.body;
  res.status(201).json({ id: 1, name, email });
});

// PUT 路由
router.put('/users/:id', (req, res) => {
  const { id } = req.params;
  const data = req.body;
  res.json({ id, ...data });
});

// DELETE 路由
router.delete('/users/:id', (req, res) => {
  const { id } = req.params;
  res.json({ message: `Deleted user ${id}` });
});

module.exports = router;
```

---

## 📦 常用中間件

### 第三方中間件

```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');

const app = express();

// CORS
app.use(cors());

// 安全頭部
app.use(helmet());

// 日誌
app.use(morgan('combined'));

// 壓縮
app.use(compression());

// JSON 解析
app.use(express.json());

// URL 編碼
app.use(express.urlencoded({ extended: true }));
```

### 自定義中間件

```javascript
// 日誌中間件
const logger = (req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
};

// 認證中間件
const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: '未授權' });
  }
  try {
    req.user = jwt.verify(token, 'secret');
    next();
  } catch {
    res.status(401).json({ error: '無效 token' });
  }
};

// 使用
app.use(logger);
app.get('/api/protected', auth, (req, res) => {
  res.json({ user: req.user });
});
```

---

## 🗄️ 數據庫集成

### MongoDB + Mongoose

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb');

const userSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  age: Number,
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// CRUD 操作
// 創建
const user = await User.create({ name: '小明', email: 'xiao@example.com' });

// 查詢
const users = await User.find({ age: { $gte: 18 } });
const user = await User.findById(id);

// 更新
const user = await User.findByIdAndUpdate(id, { age: 19 }, { new: true });

// 刪除
await User.findByIdAndDelete(id);
```

### MySQL + mysql2

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10
});

// 查詢
const [rows] = await pool.query('SELECT * FROM users WHERE age >= ?', [18]);

// 插入
const [result] = await pool.query(
  'INSERT INTO users (name, email) VALUES (?, ?)',
  ['小明', 'xiao@example.com']
);

// 事務
const connection = await pool.getConnection();
try {
  await connection.beginTransaction();
  await connection.query('UPDATE accounts SET balance = balance - 100 WHERE id = 1');
  await connection.query('UPDATE accounts SET balance = balance + 100 WHERE id = 2');
  await connection.commit();
} catch (err) {
  await connection.rollback();
  throw err;
} finally {
  connection.release();
}
```

### Redis + ioredis

```javascript
const Redis = require('ioredis');
const redis = new Redis();

// 設置
await redis.set('key', 'value');
await redis.setex('key', 3600, 'value'); // 1 小時過期

// 獲取
const value = await redis.get('key');

// 緩存示例
async function getUser(id) {
  const cacheKey = `user:${id}`;
  
  // 嘗試從緩存獲取
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // 從數據庫獲取
  const user = await db.findById(id);
  
  // 寫入緩存
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  
  return user;
}
```

---

## 🔒 安全實踐

### JWT 認證

```javascript
const jwt = require('jsonwebtoken');

// 生成 token
function generateToken(user) {
  return jwt.sign(
    { userId: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
}

// 驗證 token
function verifyToken(token) {
  return jwt.verify(token, process.env.JWT_SECRET);
}

// 認證中間件
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: '未授權' });
  }
  
  const token = authHeader.split(' ')[1];
  try {
    req.user = verifyToken(token);
    next();
  } catch (err) {
    res.status(401).json({ error: '無效 token' });
  }
}
```

### 輸入驗證

```javascript
const { body, param, query, validationResult } = require('express-validator');

app.post('/api/users',
  body('name').trim().notEmpty().withMessage('姓名必填'),
  body('email').isEmail().withMessage('郵箱格式錯誤'),
  body('age').optional().isInt({ min: 0, max: 150 }).withMessage('年齡無效'),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    // 處理有效數據
    const { name, email, age } = req.body;
    res.status(201).json({ id: 1, name, email, age });
  }
);
```

### 速率限制

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分鐘
  max: 100, // 每個 IP 最多 100 次請求
  message: '請求過於頻繁，請稍後再試'
});

app.use('/api/', limiter);

// 登錄限制
const loginLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 小時
  max: 5, // 每小時最多 5 次登錄嘗試
  message: '登錄嘗試次數過多，請 1 小時後再試'
});

app.post('/api/login', loginLimiter, (req, res) => {
  // 登錄邏輯
});
```

---

## 📊 性能優化

### 緩存策略

```javascript
// 內存緩存
const cache = new Map();

function cacheMiddleware(duration) {
  return (req, res, next) => {
    const key = req.originalUrl;
    const cached = cache.get(key);
    
    if (cached && cached.expire > Date.now()) {
      return res.json(cached.data);
    }
    
    res.json = (data) => {
      cache.set(key, { data, expire: Date.now() + duration });
      return res.send(data);
    };
    
    next();
  };
}

// 使用
app.get('/api/users', cacheMiddleware(60000), (req, res) => {
  res.json({ users: [] });
});
```

### 壓縮響應

```javascript
const compression = require('compression');
app.use(compression());
```

### 集群模式

```javascript
const cluster = require('cluster');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  console.log(`Master ${process.pid} started, ${numCPUs} workers`);
  
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  
  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  require('./app'); // 啟動應用
}
```

---

## 📖 參考資源

- **Express 官網**: https://expressjs.com/
- **Express 中間件**: https://expressjs.com/en/resources/middleware.html
- **Node.js 最佳實踐**: https://github.com/goldbergyoni/nodebestpractices

---

**最後更新**: 2026-03-19


## 相關文檔

- [[Express-實戰]]
