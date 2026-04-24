---
category: javascript
created_at: '2026-04-14'
tags:
- javascript
- node
- js
- 深度學習與實踐完整指南
- guide
title: Nodejs Complete Guide
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
# 📚 Node.js 深度學習與實踐完整指南

**創建時間:** 2026-03-18 17:06 GMT+8  
**學習目標:** 全面掌握 Node.js 核心概念、異步編程、模塊系統、Express 框架及實戰應用  
**預計時長:** 120 分鐘（深度研究 + 實踐練習）  
**Node.js 版本:** v24.14.0  
**npm 版本:** 11.9.0

---

## 📊 學習路徑總覽

```
第一階段：核心基礎 (30 分鐘)
  ├─ 1.1 Node.js 架構與運行原理
  ├─ 1.2 模塊系統深度解析
  └─ 1.3 事件循環機制

第二階段：異步編程 (30 分鐘)
  ├─ 2.1 Callback → Promise → Async/Await
  ├─ 2.2 事件驅動編程
  └─ 2.3 Stream 流式處理

第三階段：核心模塊 (25 分鐘)
  ├─ 3.1 fs 文件系統
  ├─ 3.2 path 路徑處理
  ├─ 3.3 http/https 服務器
  └─ 3.4 EventEmitter 事件發射器

第四階段：Express 框架 (20 分鐘)
  ├─ 4.1 Express 基礎與路由
  ├─ 4.2 中間件機制
  └─ 4.3 RESTful API 設計

第五階段：實戰練習 (15 分鐘)
  ├─ 5.1 文件批處理工具
  ├─ 5.2 HTTP 服務器
  ├─ 5.3 RESTful API
  └─ 5.4 日誌系統
```

---

## 第一階段：核心基礎

### 1.1 Node.js 架構與運行原理

#### 核心概念

```
┌─────────────────────────────────────┐
│           Node.js 應用               │
├─────────────────────────────────────┤
│         V8 JavaScript 引擎          │
├─────────────────────────────────────┤
│         Libuv (事件循環)             │
├─────────────────────────────────────┤
│      C/C++ 綁定 (Binding)            │
├─────────────────────────────────────┤
│         操作系統 API                  │
└─────────────────────────────────────┘
```

#### 關鍵特性

| 特性 | 說明 | 優勢 |
|------|------|------|
| **單線程** | 主線程單一，避免鎖競爭 | 簡單、無死鎖 |
| **非阻塞 I/O** | I/O 操作異步執行 | 高併發、高性能 |
| **事件驅動** | 回調函數處理事件 | 響應式、高效 |
| **V8 引擎** | Google Chrome 同款 | 快速執行 |

#### 適用場景

✅ **適合:**
- API 服務器
- 實時應用（聊天、遊戲）
- 文件處理工具
- 爬蟲與自動化
- 微服務

❌ **不適合:**
- CPU 密集型計算
- 複雜數據分析
- 機器學習訓練

---

### 1.2 模塊系統深度解析

#### CommonJS 模塊（Node.js 默認）

```javascript
// math.js - 模塊定義
const PI = 3.14159;

function add(a, b) {
  return a + b;
}

function multiply(a, b) {
  return a * b;
}

// 導出
module.exports = {
  PI,
  add,
  multiply
};

// 或者單獨導出
module.exports.add = add;
module.exports.multiply = multiply;
```

```javascript
// app.js - 使用模塊
const math = require('./math');
// 或者解構
const { add, multiply, PI } = require('./math');

console.log(add(2, 3));        // 5
console.log(multiply(2, 3));   // 6
console.log(PI);               // 3.14159
```

#### ES6 Modules（現代方式）

```javascript
// math.mjs - ES6 模塊
export const PI = 3.14159;

export function add(a, b) {
  return a + b;
}

export function multiply(a, b) {
  return a * b;
}

// 默認導出
export default class Calculator {
  // ...
}
```

```javascript
// app.mjs - 使用 ES6 模塊
import math, { add, multiply, PI } from './math.mjs';

// package.json 需要設置
{
  "type": "module"  // 啟用 ES6 模塊
}
```

#### 內置模塊 vs 第三方模塊 vs 本地模塊

```javascript
// 1. 內置模塊（無需安裝）
const fs = require('fs');
const path = require('path');
const http = require('http');

// 2. 第三方模塊（需要 npm install）
const express = require('express');
const axios = require('axios');

// 3. 本地模塊（相對路徑）
const myModule = require('./myModule');
const utils = require('../utils/helper');
```

#### 模塊加載機制

```
require('module') 加載順序：
1. 核心模塊（fs, path, http 等）
2. node_modules 中的模塊
   - 當前目錄的 node_modules
   - 父目錄的 node_modules（逐級向上）
   - 全局 node_modules
3. 本地文件（.js, .json, .node）
```

---

### 1.3 事件循環機制（Event Loop）

#### 事件循環六個階段

```
   ┌───────────────────────────┐
┌─>│           timers          │  setTimeout, setInterval
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  系統操作回調
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │  內部使用
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll            │  I/O 回調、文件操作
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check           │  setImmediate
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──│      close callbacks      │  close 事件回調
   └───────────────────────────┘
```

#### 實踐示例

```javascript
// 事件循環順序測試
console.log('1. 同步代碼開始');

setTimeout(() => {
  console.log('2. setTimeout (timers 階段)');
}, 0);

setImmediate(() => {
  console.log('3. setImmediate (check 階段)');
});

Promise.resolve().then(() => {
  console.log('4. Promise.then (微任務)');
});

process.nextTick(() => {
  console.log('5. nextTick (優先級最高)');
});

console.log('6. 同步代碼結束');

// 輸出順序：
// 1. 同步代碼開始
// 6. 同步代碼結束
// 5. nextTick (優先級最高)
// 4. Promise.then (微任務)
// 2. setTimeout (timers 階段)
// 3. setImmediate (check 階段)
```

#### 微任務 vs 宏任務

```javascript
// 微任務（Microtasks）- 優先執行
- Promise.then/catch/finally
- process.nextTick
- queueMicrotask()

// 宏任務（Macrotasks）- 後續執行
- setTimeout
- setInterval
- setImmediate
- I/O 操作
```

---

## 第二階段：異步編程

### 2.1 Callback → Promise → Async/Await 進化

#### Callback（回調函數）- 傳統方式

```javascript
const fs = require('fs');

// 回調地獄示例
fs.readFile('file1.txt', 'utf8', (err, data1) => {
  if (err) throw err;
  
  fs.readFile('file2.txt', 'utf8', (err, data2) => {
    if (err) throw err;
    
    fs.readFile('file3.txt', 'utf8', (err, data3) => {
      if (err) throw err;
      
      console.log(data1, data2, data3);
    });
  });
});
```

**問題:** 回調地獄、錯誤處理複雜、代碼難讀

#### Promise（承諾）- 現代方式

```javascript
const fs = require('fs').promises;

// Promise 鏈式調用
fs.readFile('file1.txt', 'utf8')
  .then(data1 => {
    console.log('File 1:', data1);
    return fs.readFile('file2.txt', 'utf8');
  })
  .then(data2 => {
    console.log('File 2:', data2);
    return fs.readFile('file3.txt', 'utf8');
  })
  .then(data3 => {
    console.log('File 3:', data3);
  })
  .catch(err => {
    console.error('讀取失敗:', err);
  });
```

**Promise 三種狀態:**
- `pending` - 進行中
- `fulfilled` - 成功
- `rejected` - 失敗

#### Async/Await（異步等待）- 最佳實踐

```javascript
const fs = require('fs').promises;

// Async/Await 寫法（推薦）
async function readFiles() {
  try {
    const data1 = await fs.readFile('file1.txt', 'utf8');
    console.log('File 1:', data1);
    
    const data2 = await fs.readFile('file2.txt', 'utf8');
    console.log('File 2:', data2);
    
    const data3 = await fs.readFile('file3.txt', 'utf8');
    console.log('File 3:', data3);
    
    return { data1, data2, data3 };
  } catch (err) {
    console.error('讀取失敗:', err);
    throw err;
  }
}

// 調用
readFiles();
```

**優勢:** 代碼像同步、錯誤處理簡單、易於調試

---

### 2.2 Promise 高級用法

#### Promise.all（並行執行）

```javascript
const fs = require('fs').promises;

async function readAllFiles() {
  try {
    // 三個文件同時讀取（並行）
    const [data1, data2, data3] = await Promise.all([
      fs.readFile('file1.txt', 'utf8'),
      fs.readFile('file2.txt', 'utf8'),
      fs.readFile('file3.txt', 'utf8')
    ]);
    
    console.log('全部讀取完成');
    return { data1, data2, data3 };
  } catch (err) {
    console.error('任一失敗:', err);
    throw err;
  }
}
```

#### Promise.race（競賽）

```javascript
async function fetchWithTimeout(url, timeoutMs) {
  const fetchPromise = fetch(url);
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('超時')), timeoutMs);
  });
  
  // 哪個先完成就用哪個
  return Promise.race([fetchPromise, timeoutPromise]);
}
```

#### Promise.allSettled（全部完成）

```javascript
async function readFilesSafe() {
  const results = await Promise.allSettled([
    fs.readFile('file1.txt', 'utf8'),
    fs.readFile('file2.txt', 'utf8'),
    fs.readFile('file3.txt', 'utf8')
  ]);
  
  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      console.log(`File ${index + 1} 成功:`, result.value);
    } else {
      console.error(`File ${index + 1} 失敗:`, result.reason);
    }
  });
}
```

---

### 2.3 Stream 流式處理

#### Stream 四種類型

| 類型 | 說明 | 示例 |
|------|------|------|
| **Readable** | 可讀流 | fs.createReadStream |
| **Writable** | 可寫流 | fs.createWriteStream |
| **Duplex** | 雙向流 | net.Socket |
| **Transform** | 轉換流 | zlib.createGzip |

#### Readable Stream（可讀流）

```javascript
const fs = require('fs');

// 創建可讀流
const readStream = fs.createReadStream('large-file.txt', {
  encoding: 'utf8',
  highWaterMark: 1024  // 每次讀取 1KB
});

// 事件監聽
readStream.on('data', (chunk) => {
  console.log('收到數據塊:', chunk.length);
});

readStream.on('end', () => {
  console.log('讀取完成');
});

readStream.on('error', (err) => {
  console.error('讀取錯誤:', err);
});
```

#### Writable Stream（可寫流）

```javascript
const fs = require('fs');

const writeStream = fs.createWriteStream('output.txt');

// 寫入數據
writeStream.write('第一行\n');
writeStream.write('第二行\n');
writeStream.write('第三行\n');

// 結束寫入
writeStream.end();

// 事件
writeStream.on('finish', () => {
  console.log('寫入完成');
});

writeStream.on('error', (err) => {
  console.error('寫入錯誤:', err);
});
```

#### Pipe（管道）- 流式處理

```javascript
const fs = require('fs');
const zlib = require('zlib');

// 讀取 → 壓縮 → 寫入（管道連接）
fs.createReadStream('input.txt')
  .pipe(zlib.createGzip())  // 壓縮
  .pipe(fs.createWriteStream('input.txt.gz'));

console.log('文件壓縮中...');
```

#### 異步迭代器（現代方式）

```javascript
const fs = require('fs');

async function processLargeFile() {
  const readStream = fs.createReadStream('large-file.txt', 'utf8');
  
  // 使用 for await...of 迭代
  for await (const chunk of readStream) {
    console.log('處理數據塊:', chunk.length);
    // 處理邏輯
  }
  
  console.log('處理完成');
}
```

---

## 第三階段：核心模塊

### 3.1 fs 文件系統

#### 同步 vs 異步

```javascript
const fs = require('fs');
const fsPromises = require('fs').promises;

// 同步（阻塞，不推薦）
const data = fs.readFileSync('file.txt', 'utf8');
console.log(data);

// 異步（回調）
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// 異步（Promise，推薦）
async function readFile() {
  const data = await fsPromises.readFile('file.txt', 'utf8');
  console.log(data);
}
```

#### 常用文件操作

```javascript
const fs = require('fs').promises;
const path = require('path');

async function fileOperations() {
  // 1. 讀取文件
  const content = await fs.readFile('file.txt', 'utf8');
  
  // 2. 寫入文件（覆蓋）
  await fs.writeFile('output.txt', 'Hello World', 'utf8');
  
  // 3. 追加內容
  await fs.appendFile('output.txt', '\n追加內容', 'utf8');
  
  // 4. 複製文件
  await fs.copyFile('source.txt', 'dest.txt');
  
  // 5. 重命名/移動
  await fs.rename('old.txt', 'new.txt');
  
  // 6. 刪除文件
  await fs.unlink('delete-me.txt');
  
  // 7. 創建目錄
  await fs.mkdir('new-folder', { recursive: true });
  
  // 8. 刪除目錄
  await fs.rmdir('empty-folder');
  
  // 9. 讀取目錄
  const files = await fs.readdir('./');
  console.log('文件列表:', files);
  
  // 10. 獲取文件信息
  const stats = await fs.stat('file.txt');
  console.log('文件大小:', stats.size);
  console.log('創建時間:', stats.birthtime);
  console.log('是否文件:', stats.isFile());
}
```

#### 實戰：批量文件處理

```javascript
const fs = require('fs').promises;
const path = require('path');

async function batchProcessFiles(directory, extension) {
  try {
    // 1. 讀取目錄
    const files = await fs.readdir(directory);
    
    // 2. 過濾指定擴展名
    const targetFiles = files.filter(file => 
      file.endsWith(extension)
    );
    
    console.log(`找到 ${targetFiles.length} 個 ${extension} 文件`);
    
    // 3. 批量處理
    const results = await Promise.all(
      targetFiles.map(async (file) => {
        const filePath = path.join(directory, file);
        const content = await fs.readFile(filePath, 'utf8');
        
        // 處理邏輯（示例：統計字數）
        const wordCount = content.split(/\s+/).length;
        
        return {
          file,
          wordCount,
          size: content.length
        };
      })
    );
    
    // 4. 生成報告
    const report = results.map(r => 
      `${r.file}: ${r.wordCount} 字，${r.size} 字節`
    ).join('\n');
    
    await fs.writeFile(
      path.join(directory, 'report.txt'),
      report,
      'utf8'
    );
    
    console.log('處理完成，報告已生成');
    return results;
    
  } catch (err) {
    console.error('批量處理失敗:', err);
    throw err;
  }
}

// 使用
batchProcessFiles('./docs', '.md');
```

---

### 3.2 path 路徑處理

#### 常用方法

```javascript
const path = require('path');

// 1. 路徑拼接（推薦，跨平台）
const fullPath = path.join('/home', 'user', 'documents', 'file.txt');
// Linux: /home/user/documents/file.txt
// Windows: \home\user\documents\file.txt

// 2. 解析路徑
const parsed = path.parse('/home/user/file.txt');
console.log(parsed);
// {
//   root: '/',
//   dir: '/home/user',
//   base: 'file.txt',
//   ext: '.txt',
//   name: 'file'
// }

// 3. 格式化路徑
const formatted = path.format({
  dir: '/home/user',
  base: 'file.txt'
});
// '/home/user/file.txt'

// 4. 獲取文件名
const basename = path.basename('/home/user/file.txt');
// 'file.txt'

const basenameNoExt = path.basename('/home/user/file.txt', '.txt');
// 'file'

// 5. 獲取目錄名
const dirname = path.dirname('/home/user/file.txt');
// '/home/user'

// 6. 獲取擴展名
const extname = path.extname('/home/user/file.txt');
// '.txt'

// 7. 判斷是否絕對路徑
path.isAbsolute('/home/user');  // true
path.isAbsolute('user/file');   // false

// 8. 路徑規範化
path.normalize('/home//user/../user/./file.txt');
// '/home/user/file.txt'

// 9. 解析相對路徑
path.relative('/home/user', '/home/user/docs/file.txt');
// 'docs/file.txt'

// 10. 當前腳本目錄
console.log(__dirname);  // 當前腳本所在目錄
console.log(__filename); // 當前腳本完整路徑
```

#### 實戰：構建跨平台路徑

```javascript
const path = require('path');

class PathBuilder {
  constructor(baseDir = __dirname) {
    this.baseDir = baseDir;
  }
  
  // 構建項目內路徑
  project(...paths) {
    return path.join(this.baseDir, ...paths);
  }
  
  // 構建 src 目錄路徑
  src(...paths) {
    return path.join(this.baseDir, 'src', ...paths);
  }
  
  // 構建 dist 目錄路徑
  dist(...paths) {
    return path.join(this.baseDir, 'dist', ...paths);
  }
  
  // 構建配置文件路徑
  config(filename) {
    return path.join(this.baseDir, 'config', filename);
  }
  
  // 獲取文件擴展名
  getExtension(filePath) {
    return path.extname(filePath).slice(1);
  }
  
  // 更改文件擴展名
  changeExtension(filePath, newExt) {
    const dir = path.dirname(filePath);
    const name = path.basename(filePath, path.extname(filePath));
    return path.join(dir, `${name}.${newExt}`);
  }
}

// 使用
const paths = new PathBuilder();
console.log(paths.src('utils', 'helper.js'));
console.log(paths.config('app.json'));
```

---

### 3.3 http/https 服務器

#### 創建 HTTP 服務器（原生）

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // 1. 獲取請求信息
  const { method, url, headers } = req;
  
  console.log(`${method} ${url}`);
  
  // 2. 設置響應頭
  res.writeHead(200, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  });
  
  // 3. 發送響應
  const response = {
    message: 'Hello World',
    timestamp: new Date().toISOString(),
    path: url
  };
  
  res.end(JSON.stringify(response, null, 2));
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`服務器運行在 http://localhost:${PORT}`);
});
```

#### 路由處理

```javascript
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;
  
  // 設置 JSON 響應
  const sendJSON = (data, status = 200) => {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  };
  
  // 路由匹配
  if (method === 'GET' && pathname === '/') {
    sendJSON({ message: '首頁' });
  } 
  else if (method === 'GET' && pathname === '/api/users') {
    sendJSON({ users: ['Alice', 'Bob', 'Charlie'] });
  }
  else if (method === 'POST' && pathname === '/api/users') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const newUser = JSON.parse(body);
      sendJSON({ message: '用戶創建成功', user: newUser }, 201);
    });
  }
  else if (method === 'GET' && pathname.startsWith('/api/users/')) {
    const id = pathname.split('/').pop();
    sendJSON({ id, name: `User ${id}` });
  }
  else {
    sendJSON({ error: '404 Not Found' }, 404);
  }
});

server.listen(3000, () => {
  console.log('HTTP 服務器運行在 http://localhost:3000');
});
```

#### HTTPS 服務器

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};

const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('Hello over HTTPS!');
});

server.listen(443, () => {
  console.log('HTTPS 服務器運行在 https://localhost:443');
});
```

---

### 3.4 EventEmitter 事件發射器

#### 基礎用法

```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();

// 1. 註冊事件監聽
myEmitter.on('event', () => {
  console.log('事件被觸發！');
});

// 2. 觸發事件
myEmitter.emit('event');

// 3. 帶參數的事件
myEmitter.on('greet', (name, age) => {
  console.log(`你好，${name}，今年${age}歲`);
});

myEmitter.emit('greet', '小明', 25);

// 4. 一次性監聽
myEmitter.once('once-event', () => {
  console.log('只會執行一次');
});

myEmitter.emit('once-event');  // 會執行
myEmitter.emit('once-event');  // 不會執行

// 5. 移除監聽
const listener = () => console.log('監聽中...');
myEmitter.on('remove-event', listener);
myEmitter.emit('remove-event');  // 會執行

myEmitter.removeListener('remove-event', listener);
myEmitter.emit('remove-event');  // 不會執行

// 6. 錯誤事件（特殊）
myEmitter.on('error', (err) => {
  console.error('發生錯誤:', err);
});

myEmitter.emit('error', new Error('出錯了'));
```

#### 實戰：日誌系統

```javascript
const EventEmitter = require('events');
const fs = require('fs').promises;

class Logger extends EventEmitter {
  constructor(logFile) {
    super();
    this.logFile = logFile;
    
    // 註冊事件處理
    this.on('log', this.writeLog.bind(this));
    this.on('error', this.handleError.bind(this));
  }
  
  // 日誌級別
  info(message) {
    this.emit('log', 'INFO', message);
  }
  
  warn(message) {
    this.emit('log', 'WARN', message);
  }
  
  error(message) {
    this.emit('log', 'ERROR', message);
  }
  
  // 寫入日誌
  async writeLog(level, message) {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] [${level}] ${message}\n`;
    
    try {
      await fs.appendFile(this.logFile, logLine);
      console.log(logLine.trim());
    } catch (err) {
      this.emit('error', err);
    }
  }
  
  // 錯誤處理
  async handleError(err) {
    console.error('日誌系統錯誤:', err);
    await fs.appendFile(
      this.logFile,
      `[${new Date().toISOString()}] [SYSTEM] ${err.message}\n`
    );
  }
}

// 使用
const logger = new Logger('./app.log');
logger.info('應用啟動');
logger.warn('警告信息');
logger.error('錯誤信息');
```

---

## 第四階段：Express 框架

### 4.1 Express 基礎與路由

#### 安裝與初始化

```bash
# 安裝 Express
npm install express

# 初始化項目
npm init -y
```

#### Hello World

```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(PORT, () => {
  console.log(`服務器運行在 http://localhost:${PORT}`);
});
```

#### 路由方法

```javascript
const express = require('express');
const app = express();

// GET 請求
app.get('/users', (req, res) => {
  res.json({ message: '獲取用戶列表' });
});

// POST 請求
app.post('/users', (req, res) => {
  res.json({ message: '創建新用戶' });
});

// PUT 請求
app.put('/users/:id', (req, res) => {
  res.json({ message: `更新用戶 ${req.params.id}` });
});

// DELETE 請求
app.delete('/users/:id', (req, res) => {
  res.json({ message: `刪除用戶 ${req.params.id}` });
});

// 路徑參數
app.get('/users/:id/posts/:postId', (req, res) => {
  const { id, postId } = req.params;
  res.json({ userId: id, postId });
});

// 查詢參數
app.get('/search', (req, res) => {
  const { q, page, limit } = req.query;
  res.json({ query: q, page, limit });
});

// 萬能路由（最後定義）
app.all('*', (req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.listen(3000);
```

#### Express Router（模塊化路由）

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

// GET /users
router.get('/', (req, res) => {
  res.json({ message: '用戶列表' });
});

// GET /users/:id
router.get('/:id', (req, res) => {
  res.json({ id: req.params.id });
});

// POST /users
router.post('/', (req, res) => {
  res.json({ message: '創建新用戶' });
});

module.exports = router;
```

```javascript
// app.js
const express = require('express');
const app = express();
const userRoutes = require('./routes/users');

// 使用路由模塊
app.use('/api/users', userRoutes);

app.listen(3000);
// 訪問：http://localhost:3000/api/users
```

---

### 4.2 中間件機制

#### 中間件概念

```
請求 → 中間件 1 → 中間件 2 → 路由處理 → 響應
```

#### 自定義中間件

```javascript
const express = require('express');
const app = express();

// 日誌中間件
const logger = (req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  next();  // 必須調用 next() 繼續
};

// 認證中間件
const auth = (req, res, next) => {
  const token = req.headers.authorization;
  
  if (token === 'secret-token') {
    req.user = { id: 1, name: 'Admin' };  // 添加到 request
    next();
  } else {
    res.status(401).json({ error: '未授權' });
  }
};

// 錯誤處理中間件（四個參數）
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: '服務器錯誤' });
};

// 使用中間件
app.use(logger);
app.use('/api', auth);

app.get('/', (req, res) => {
  res.json({ message: 'Hello' });
});

app.use(errorHandler);
app.listen(3000);
```

#### 常用第三方中間件

```javascript
const express = require('express');
const app = express();

// 1. 解析 JSON
app.use(express.json());

// 2. 解析 URL 編碼
app.use(express.urlencoded({ extended: true }));

// 3. 靜態文件服務
app.use(express.static('public'));

// 4. CORS（跨域）
const cors = require('cors');
app.use(cors());

// 5. 壓縮
const compression = require('compression');
app.use(compression());

// 6. 日誌
const morgan = require('morgan');
app.use(morgan('combined'));

app.listen(3000);
```

---

### 4.3 RESTful API 設計

#### RESTful 原則

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | /api/users | 獲取所有用戶 |
| GET | /api/users/:id | 獲取單個用戶 |
| POST | /api/users | 創建新用戶 |
| PUT | /api/users/:id | 更新用戶（全量） |
| PATCH | /api/users/:id | 更新用戶（部分） |
| DELETE | /api/users/:id | 刪除用戶 |

#### 完整示例

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// 模擬數據庫
let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];
let nextId = 3;

// GET /api/users - 獲取所有用戶
app.get('/api/users', (req, res) => {
  res.json({ users });
});

// GET /api/users/:id - 獲取單個用戶
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  
  if (!user) {
    return res.status(404).json({ error: '用戶不存在' });
  }
  
  res.json({ user });
});

// POST /api/users - 創建新用戶
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  
  // 驗證
  if (!name || !email) {
    return res.status(400).json({ error: 'name 和 email 必填' });
  }
  
  const newUser = { id: nextId++, name, email };
  users.push(newUser);
  
  res.status(201).json({ user: newUser });
});

// PUT /api/users/:id - 全量更新
app.put('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  
  if (!user) {
    return res.status(404).json({ error: '用戶不存在' });
  }
  
  const { name, email } = req.body;
  user.name = name;
  user.email = email;
  
  res.json({ user });
});

// PATCH /api/users/:id - 部分更新
app.patch('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  
  if (!user) {
    return res.status(404).json({ error: '用戶不存在' });
  }
  
  const { name, email } = req.body;
  if (name) user.name = name;
  if (email) user.email = email;
  
  res.json({ user });
});

// DELETE /api/users/:id - 刪除用戶
app.delete('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  
  if (index === -1) {
    return res.status(404).json({ error: '用戶不存在' });
  }
  
  users.splice(index, 1);
  res.json({ message: '刪除成功' });
});

app.listen(3000, () => {
  console.log('RESTful API 服務器運行在 http://localhost:3000');
});
```

---

## 第五階段：實戰練習

### 練習 1: 文件批處理工具

**目標:** 批量處理指定目錄下的文件

```javascript
// file-processor.js
const fs = require('fs').promises;
const path = require('path');

class FileProcessor {
  constructor(directory) {
    this.directory = directory;
  }
  
  // 獲取所有文件
  async getFiles(extension = null) {
    const files = await fs.readdir(this.directory);
    
    if (extension) {
      return files.filter(f => f.endsWith(extension));
    }
    
    return files;
  }
  
  // 批量讀取
  async readAll(extension = null) {
    const files = await this.getFiles(extension);
    
    const results = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        const content = await fs.readFile(filePath, 'utf8');
        return { file, content };
      })
    );
    
    return results;
  }
  
  // 批量統計
  async getStats(extension = null) {
    const files = await this.getFiles(extension);
    
    const stats = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        const fileStats = await fs.stat(filePath);
        const content = await fs.readFile(filePath, 'utf8');
        
        return {
          file,
          size: fileStats.size,
          lines: content.split('\n').length,
          words: content.split(/\s+/).length,
          created: fileStats.birthtime,
          modified: fileStats.mtime
        };
      })
    );
    
    return stats;
  }
  
  // 批量替換
  async replaceAll(searchStr, replaceStr, extension = null) {
    const files = await this.getFiles(extension);
    
    const results = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        let content = await fs.readFile(filePath, 'utf8');
        
        const originalLength = content.length;
        content = content.replace(new RegExp(searchStr, 'g'), replaceStr);
        
        if (originalLength !== content.length) {
          await fs.writeFile(filePath, content, 'utf8');
          return { file, changed: true };
        }
        
        return { file, changed: false };
      })
    );
    
    const changedCount = results.filter(r => r.changed).length;
    console.log(`修改了 ${changedCount} 個文件`);
    
    return results;
  }
  
  // 生成報告
  async generateReport(extension = null) {
    const stats = await this.getStats(extension);
    
    const totalSize = stats.reduce((sum, s) => sum + s.size, 0);
    const totalLines = stats.reduce((sum, s) => sum + s.lines, 0);
    const totalWords = stats.reduce((sum, s) => sum + s.words, 0);
    
    const report = `
文件統計報告
============
文件總數：${stats.length}
總大小：${(totalSize / 1024).toFixed(2)} KB
總行數：${totalLines}
總字數：${totalWords}

文件詳情:
${stats.map(s => 
  `${s.file}: ${s.size} 字節，${s.lines} 行，${s.words} 字`
).join('\n')}
`.trim();
    
    const reportPath = path.join(this.directory, 'report.txt');
    await fs.writeFile(reportPath, report, 'utf8');
    
    console.log(report);
    return report;
  }
}

// 使用示例
async function main() {
  const processor = new FileProcessor('./docs');
  
  // 獲取所有 Markdown 文件
  const mdFiles = await processor.getFiles('.md');
  console.log('Markdown 文件:', mdFiles);
  
  // 生成統計報告
  await processor.generateReport('.md');
  
  // 批量替換
  await processor.replaceAll('old-text', 'new-text', '.md');
}

main();
```

---

### 練習 2: HTTP 服務器

**目標:** 創建功能完整的 HTTP 服務器

```javascript
// http-server.js
const http = require('http');
const fs = require('fs').promises;
const path = require('path');
const url = require('url');

class SimpleHTTPServer {
  constructor(port = 3000, publicDir = 'public') {
    this.port = port;
    this.publicDir = publicDir;
    this.routes = new Map();
    
    this.server = http.createServer(this.handleRequest.bind(this));
  }
  
  // 註冊路由
  route(method, path, handler) {
    const key = `${method.toUpperCase()} ${path}`;
    this.routes.set(key, handler);
    return this;
  }
  
  // GET 快捷方式
  get(path, handler) {
    return this.route('GET', path, handler);
  }
  
  // POST 快捷方式
  post(path, handler) {
    return this.route('POST', path, handler);
  }
  
  // 處理請求
  async handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    const method = req.method;
    
    const log = `[${new Date().toISOString()}] ${method} ${pathname}`;
    console.log(log);
    
    // 1. 檢查註冊的路由
    const routeKey = `${method} ${pathname}`;
    const handler = this.routes.get(routeKey);
    
    if (handler) {
      try {
        await handler(req, res, parsedUrl);
      } catch (err) {
        this.sendError(res, err);
      }
      return;
    }
    
    // 2. 靜態文件服務
    try {
      const filePath = path.join(this.publicDir, pathname === '/' ? 'index.html' : pathname);
      const content = await fs.readFile(filePath);
      const ext = path.extname(filePath);
      
      const mimeTypes = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif'
      };
      
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'text/plain' });
      res.end(content);
    } catch (err) {
      // 404
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    }
  }
  
  // 發送 JSON
  sendJSON(res, data, status = 200) {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  }
  
  // 發送錯誤
  sendError(res, err, status = 500) {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: err.message }));
  }
  
  // 啟動服務器
  start() {
    return new Promise((resolve, reject) => {
      this.server.listen(this.port, () => {
        console.log(`服務器運行在 http://localhost:${this.port}`);
        resolve();
      });
      
      this.server.on('error', reject);
    });
  }
  
  // 停止服務器
  stop() {
    return new Promise((resolve) => {
      this.server.close(() => {
        console.log('服務器已停止');
        resolve();
      });
    });
  }
}

// 使用示例
async function main() {
  const app = new SimpleHTTPServer(3000);
  
  // API 路由
  app.get('/api/time', (req, res) => {
    app.sendJSON(res, { time: new Date().toISOString() });
  });
  
  app.get('/api/users', (req, res) => {
    app.sendJSON(res, { 
      users: [
        { id: 1, name: 'Alice' },
        { id: 2, name: 'Bob' }
      ]
    });
  });
  
  app.post('/api/echo', async (req, res) => {
    let body = '';
    for await (const chunk of req) {
      body += chunk;
    }
    app.sendJSON(res, { received: body });
  });
  
  await app.start();
}

main();
```

---

### 練習 3: RESTful API 完整示例

**目標:** 創建任務管理 API

```javascript
// task-api.js
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// 模擬數據庫
let tasks = [
  { id: 1, title: '學習 Node.js', completed: false, priority: 'high' },
  { id: 2, title: '完成項目', completed: true, priority: 'medium' }
];
let nextId = 3;

// 中間件：驗證
const validateTask = (req, res, next) => {
  const { title } = req.body;
  
  if (!title || title.trim().length === 0) {
    return res.status(400).json({ error: '標題不能為空' });
  }
  
  next();
};

// GET /api/tasks - 獲取所有任務
app.get('/api/tasks', (req, res) => {
  const { completed, priority } = req.query;
  
  let filtered = tasks;
  
  if (completed !== undefined) {
    const isCompleted = completed === 'true';
    filtered = filtered.filter(t => t.completed === isCompleted);
  }
  
  if (priority) {
    filtered = filtered.filter(t => t.priority === priority);
  }
  
  res.json({ tasks: filtered, total: filtered.length });
});

// GET /api/tasks/:id - 獲取單個任務
app.get('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ error: '任務不存在' });
  }
  
  res.json({ task });
});

// POST /api/tasks - 創建新任務
app.post('/api/tasks', validateTask, (req, res) => {
  const { title, priority = 'medium' } = req.body;
  
  const newTask = {
    id: nextId++,
    title,
    completed: false,
    priority
  };
  
  tasks.push(newTask);
  res.status(201).json({ task: newTask });
});

// PUT /api/tasks/:id - 更新任務
app.put('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ error: '任務不存在' });
  }
  
  const { title, completed, priority } = req.body;
  if (title) task.title = title;
  if (completed !== undefined) task.completed = completed;
  if (priority) task.priority = priority;
  
  res.json({ task });
});

// DELETE /api/tasks/:id - 刪除任務
app.delete('/api/tasks/:id', (req, res) => {
  const index = tasks.findIndex(t => t.id === parseInt(req.params.id));
  
  if (index === -1) {
    return res.status(404).json({ error: '任務不存在' });
  }
  
  tasks.splice(index, 1);
  res.json({ message: '刪除成功' });
});

// PATCH /api/tasks/:id/toggle - 切換完成狀態
app.patch('/api/tasks/:id/toggle', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ error: '任務不存在' });
  }
  
  task.completed = !task.completed;
  res.json({ task });
});

// 統計信息
app.get('/api/stats', (req, res) => {
  const total = tasks.length;
  const completed = tasks.filter(t => t.completed).length;
  const pending = total - completed;
  
  res.json({
    total,
    completed,
    pending,
    completionRate: total > 0 ? ((completed / total) * 100).toFixed(1) + '%' : '0%'
  });
});

app.listen(PORT, () => {
  console.log(`任務管理 API 運行在 http://localhost:${PORT}`);
  console.log(`API 文檔：http://localhost:${PORT}/api/stats`);
});
```

**測試命令:**

```bash
# 獲取所有任務
curl http://localhost:3000/api/tasks

# 創建新任務
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"新任務","priority":"high"}'

# 獲取單個任務
curl http://localhost:3000/api/tasks/1

# 更新任務
curl -X PUT http://localhost:3000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# 切換完成狀態
curl -X PATCH http://localhost:3000/api/tasks/1/toggle

# 刪除任務
curl -X DELETE http://localhost:3000/api/tasks/1

# 獲取統計
curl http://localhost:3000/api/stats
```

---

### 練習 4: 日誌系統

**目標:** 創建可擴展的日誌系統

```javascript
// logger.js
const EventEmitter = require('events');
const fs = require('fs').promises;
const path = require('path');

// 日誌級別
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

class Logger extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.logFile = options.logFile || './app.log';
    this.level = options.level || LogLevel.INFO;
    this.console = options.console !== false;
    
    // 確保日誌目錄存在
    this.init();
  }
  
  async init() {
    const dir = path.dirname(this.logFile);
    try {
      await fs.mkdir(dir, { recursive: true });
    } catch (err) {
      console.error('創建日誌目錄失敗:', err);
    }
  }
  
  // 格式化日誌
  format(level, message, meta = {}) {
    const timestamp = new Date().toISOString();
    const metaStr = Object.keys(meta).length > 0 ? ` ${JSON.stringify(meta)}` : '';
    return `[${timestamp}] [${level}] ${message}${metaStr}`;
  }
  
  // 寫入日誌
  async write(level, message, meta) {
    const logLine = this.format(level, message, meta) + '\n';
    
    // 控制台輸出
    if (this.console) {
      const consoleMethod = level.toLowerCase();
      console[consoleMethod]?.(logLine.trim());
    }
    
    // 文件寫入
    try {
      await fs.appendFile(this.logFile, logLine);
      this.emit('log', { level, message, meta, timestamp: new Date() });
    } catch (err) {
      this.emit('error', err);
    }
  }
  
  // 日誌方法
  debug(message, meta) {
    if (this.level <= LogLevel.DEBUG) {
      this.write('DEBUG', message, meta);
    }
  }
  
  info(message, meta) {
    if (this.level <= LogLevel.INFO) {
      this.write('INFO', message, meta);
    }
  }
  
  warn(message, meta) {
    if (this.level <= LogLevel.WARN) {
      this.write('WARN', message, meta);
    }
  }
  
  error(message, meta) {
    if (this.level <= LogLevel.ERROR) {
      this.write('ERROR', message, meta);
    }
  }
  
  // 創建子日誌器
  child(meta) {
    const childLogger = new Logger({
      logFile: this.logFile,
      level: this.level,
      console: this.console
    });
    
    // 轉發事件
    childLogger.on('log', (data) => {
      data.meta = { ...meta, ...data.meta };
      this.emit('log', data);
    });
    
    return childLogger;
  }
  
  // 讀取日誌
  async read(lines = 100) {
    try {
      const content = await fs.readFile(this.logFile, 'utf8');
      const allLines = content.split('\n').filter(l => l.trim());
      return allLines.slice(-lines);
    } catch (err) {
      return [];
    }
  }
  
  // 清空日誌
  async clear() {
    await fs.writeFile(this.logFile, '');
    this.info('日誌已清空');
  }
}

// 使用示例
async function main() {
  const logger = new Logger({
    logFile: './logs/app.log',
    level: LogLevel.DEBUG,
    console: true
  });
  
  // 監聽日誌事件
  logger.on('log', (data) => {
    console.log('日誌事件:', data.level, data.message);
  });
  
  // 各種級別的日誌
  logger.debug('調試信息', { module: 'auth' });
  logger.info('應用啟動', { version: '1.0.0' });
  logger.warn('警告信息', { code: 'W001' });
  logger.error('錯誤信息', { error: 'Something failed' });
  
  // 創建子日誌器
  const dbLogger = logger.child({ module: 'database' });
  dbLogger.info('數據庫連接成功');
  
  // 讀取日誌
  const recentLogs = await logger.read(10);
  console.log('最近 10 條日誌:', recentLogs);
}

main();
```

---

## 📝 學習總結

### 核心知識點

| 模塊 | 關鍵概念 | 重要性 |
|------|---------|--------|
| **模塊系統** | CommonJS、ES6 Modules、require、export | ⭐⭐⭐⭐⭐ |
| **事件循環** | Timers、Poll、Check、微任務 | ⭐⭐⭐⭐⭐ |
| **異步編程** | Callback、Promise、Async/Await | ⭐⭐⭐⭐⭐ |
| **Stream** | Readable、Writable、Pipe | ⭐⭐⭐⭐ |
| **文件系統** | fs.readFile、fs.writeFile、批量處理 | ⭐⭐⭐⭐ |
| **HTTP 服務器** | http.createServer、路由、中間件 | ⭐⭐⭐⭐⭐ |
| **Express** | 路由、中間件、RESTful API | ⭐⭐⭐⭐⭐ |
| **EventEmitter** | on、emit、事件驅動 | ⭐⭐⭐⭐ |

### 實戰技能

✅ **已掌握:**
- 模塊化代碼組織
- 異步編程最佳實踐
- 文件批量處理
- HTTP 服務器構建
- RESTful API 設計
- 中間件開發
- 日誌系統實現

### 下一步學習方向

- [ ] **數據庫集成** - MongoDB、PostgreSQL
- [ ] **身份認證** - JWT、OAuth
- [ ] **測試** - Jest、Mocha
- [ ] **部署** - Docker、Kubernetes
- [ ] **性能優化** - 緩存、集群
- [ ] **TypeScript** - 類型安全

---

## 🔗 參考資源

### 官方文檔
- [Node.js 官方文檔](https://nodejs.org/docs/)
- [Express 官方文檔](https://expressjs.com/)
- [npm 官方文檔](https://docs.npmjs.com/)

### 中文教程
- [Node.js 中文網](https://nodejs.org/zh-cn/)
- [Express 中文教程](https://www.expressjs.com.cn/)

### 實戰項目
- [Node.js 最佳實踐](https://github.com/goldbergyoni/nodebestpractices)
- [Express 生成器](https://expressjs.com/en/starter/generator.html)

---

**完成時間:** 2026-03-18 17:06-19:06  
**總學習時長:** 120 分鐘  
**代碼行數:** 1000+ 行  
**實踐練習:** 4 個完整項目

## 參考

- [[Knowledge Files Complete List]]


## 相關文檔

- [[knowledge-files-complete-list]]
- [[INSTALL-VALIDATOR-GUIDE]]
- [[ULTIMATE-COMPLETE-REPORT]]
