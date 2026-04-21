#!/usr/bin/env node
/**
 * 練習 2: HTTP 服務器
 * 功能：創建功能完整的 HTTP 服務器，支持路由和靜態文件
 */

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
  
  // PUT 快捷方式
  put(path, handler) {
    return this.route('PUT', path, handler);
  }
  
  // DELETE 快捷方式
  delete(path, handler) {
    return this.route('DELETE', path, handler);
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
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon'
      };
      
      res.writeHead(200, { 
        'Content-Type': mimeTypes[ext] || 'text/plain; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      });
      res.end(content);
    } catch (err) {
      // 404
      res.writeHead(404, { 
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      });
      res.end(JSON.stringify({ 
        error: '404 Not Found',
        path: pathname 
      }, null, 2));
    }
  }
  
  // 發送 JSON
  sendJSON(res, data, status = 200) {
    res.writeHead(status, { 
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify(data, null, 2));
  }
  
  // 發送錯誤
  sendError(res, err, status = 500) {
    res.writeHead(status, { 
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify({ 
      error: err.message,
      stack: err.stack 
    }, null, 2));
  }
  
  // 啟動服務器
  start() {
    return new Promise((resolve, reject) => {
      this.server.listen(this.port, () => {
        const message = `
╔════════════════════════════════════════╗
║     HTTP 服務器已啟動                    ║
╠════════════════════════════════════════╣
║ 地址：http://localhost:${String(this.port).padEnd(19)}║
║ 時間：${new Date().toLocaleString('zh-CN').padEnd(20)}║
╚════════════════════════════════════════╝
        `;
        console.log(message);
        resolve();
      });
      
      this.server.on('error', reject);
    });
  }
  
  // 停止服務器
  stop() {
    return new Promise((resolve) => {
      this.server.close(() => {
        console.log('✅ 服務器已停止');
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
    app.sendJSON(res, { 
      time: new Date().toISOString(),
      timezone: 'Asia/Shanghai'
    });
  });
  
  app.get('/api/users', (req, res) => {
    app.sendJSON(res, { 
      users: [
        { id: 1, name: 'Alice', email: 'alice@example.com' },
        { id: 2, name: 'Bob', email: 'bob@example.com' },
        { id: 3, name: 'Charlie', email: 'charlie@example.com' }
      ]
    });
  });
  
  app.get('/api/users/:id', (req, res) => {
    const userId = req.url.split('/').pop();
    app.sendJSON(res, { 
      user: { 
        id: parseInt(userId), 
        name: `User ${userId}`,
        email: `user${userId}@example.com`
      }
    });
  });
  
  app.post('/api/echo', async (req, res) => {
    let body = '';
    for await (const chunk of req) {
      body += chunk;
    }
    
    try {
      const data = JSON.parse(body);
      app.sendJSON(res, { 
        message: '收到數據',
        received: data 
      });
    } catch (err) {
      app.sendJSON(res, { 
        message: '收到數據（純文本）',
        received: body 
      }, 200);
    }
  });
  
  app.get('/api/stats', (req, res) => {
    app.sendJSON(res, {
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      nodeVersion: process.version,
      platform: process.platform
    });
  });
  
  app.get('/', (req, res) => {
    app.sendJSON(res, {
      message: '歡迎使用 HTTP 服務器',
      endpoints: [
        'GET /api/time',
        'GET /api/users',
        'GET /api/users/:id',
        'POST /api/echo',
        'GET /api/stats'
      ]
    });
  });
  
  await app.start();
  
  // 優雅關閉
  process.on('SIGINT', async () => {
    console.log('\n👋 正在關閉服務器...');
    await app.stop();
    process.exit(0);
  });
}

// 如果直接運行則執行 main
if (require.main === module) {
  main().catch(err => {
    console.error('啟動失敗:', err);
    process.exit(1);
  });
}

module.exports = SimpleHTTPServer;
