#!/usr/bin/env node
/**
 * 練習 3: RESTful API - 任務管理系統
 * 功能：完整的 CRUD 操作，支持過濾、統計
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 中間件
app.use(express.json());

// 請求日誌
app.use((req, res, next) => {
  const timestamp = new Date().toLocaleString('zh-CN');
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  next();
});

// CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// 模擬數據庫
let tasks = [
  { 
    id: 1, 
    title: '學習 Node.js 基礎', 
    completed: false, 
    priority: 'high',
    description: '掌握模塊系統、異步編程、事件循環',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  { 
    id: 2, 
    title: '完成實踐練習', 
    completed: true, 
    priority: 'medium',
    description: '完成 4 個實踐項目',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  { 
    id: 3, 
    title: '學習 Express 框架', 
    completed: false, 
    priority: 'medium',
    description: '掌握路由、中間件、RESTful API',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];
let nextId = 4;

// ===== 驗證中間件 =====
const validateTask = (req, res, next) => {
  const { title } = req.body;
  
  if (!title || title.trim().length === 0) {
    return res.status(400).json({ 
      error: '驗證失敗',
      message: '標題不能為空',
      field: 'title'
    });
  }
  
  if (title.length > 200) {
    return res.status(400).json({ 
      error: '驗證失敗',
      message: '標題不能超過 200 字',
      field: 'title'
    });
  }
  
  const validPriorities = ['low', 'medium', 'high'];
  if (req.body.priority && !validPriorities.includes(req.body.priority)) {
    return res.status(400).json({ 
      error: '驗證失敗',
      message: `優先級必須是 ${validPriorities.join(', ')} 之一`,
      field: 'priority'
    });
  }
  
  next();
};

// ===== 路由 =====

// GET /api/tasks - 獲取所有任務（支持過濾）
app.get('/api/tasks', (req, res) => {
  const { completed, priority, sort } = req.query;
  
  let filtered = [...tasks];
  
  // 過濾完成狀態
  if (completed !== undefined) {
    const isCompleted = completed === 'true';
    filtered = filtered.filter(t => t.completed === isCompleted);
  }
  
  // 過濾優先級
  if (priority) {
    filtered = filtered.filter(t => t.priority === priority);
  }
  
  // 排序
  if (sort === 'priority') {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    filtered.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
  } else if (sort === 'created') {
    filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }
  
  res.json({ 
    success: true,
    tasks: filtered, 
    total: filtered.length,
    filters: { completed, priority, sort }
  });
});

// GET /api/tasks/:id - 獲取單個任務
app.get('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ 
      success: false,
      error: '未找到',
      message: `任務 ${req.params.id} 不存在` 
    });
  }
  
  res.json({ success: true, task });
});

// POST /api/tasks - 創建新任務
app.post('/api/tasks', validateTask, (req, res) => {
  const { title, description, priority = 'medium' } = req.body;
  
  const newTask = {
    id: nextId++,
    title,
    description: description || '',
    completed: false,
    priority,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  
  tasks.push(newTask);
  
  res.status(201).json({ 
    success: true,
    message: '任務創建成功',
    task: newTask 
  });
});

// PUT /api/tasks/:id - 全量更新任務
app.put('/api/tasks/:id', validateTask, (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ 
      success: false,
      error: '未找到',
      message: `任務 ${req.params.id} 不存在` 
    });
  }
  
  const { title, description, completed, priority } = req.body;
  task.title = title;
  task.description = description || task.description;
  task.completed = completed !== undefined ? completed : task.completed;
  task.priority = priority || task.priority;
  task.updatedAt = new Date().toISOString();
  
  res.json({ 
    success: true,
    message: '任務更新成功',
    task 
  });
});

// PATCH /api/tasks/:id - 部分更新任務
app.patch('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ 
      success: false,
      error: '未找到',
      message: `任務 ${req.params.id} 不存在` 
    });
  }
  
  const { title, description, completed, priority } = req.body;
  
  if (title !== undefined) task.title = title;
  if (description !== undefined) task.description = description;
  if (completed !== undefined) task.completed = completed;
  if (priority !== undefined) task.priority = priority;
  
  task.updatedAt = new Date().toISOString();
  
  res.json({ 
    success: true,
    message: '任務部分更新成功',
    task 
  });
});

// PATCH /api/tasks/:id/toggle - 切換完成狀態
app.patch('/api/tasks/:id/toggle', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  
  if (!task) {
    return res.status(404).json({ 
      success: false,
      error: '未找到',
      message: `任務 ${req.params.id} 不存在` 
    });
  }
  
  task.completed = !task.completed;
  task.updatedAt = new Date().toISOString();
  
  res.json({ 
    success: true,
    message: `任務已${task.completed ? '完成' : '重新開始'}`,
    task 
  });
});

// DELETE /api/tasks/:id - 刪除任務
app.delete('/api/tasks/:id', (req, res) => {
  const index = tasks.findIndex(t => t.id === parseInt(req.params.id));
  
  if (index === -1) {
    return res.status(404).json({ 
      success: false,
      error: '未找到',
      message: `任務 ${req.params.id} 不存在` 
    });
  }
  
  const deleted = tasks.splice(index, 1)[0];
  
  res.json({ 
    success: true,
    message: '任務刪除成功',
    deleted 
  });
});

// GET /api/stats - 統計信息
app.get('/api/stats', (req, res) => {
  const total = tasks.length;
  const completed = tasks.filter(t => t.completed).length;
  const pending = total - completed;
  
  const byPriority = {
    high: tasks.filter(t => t.priority === 'high').length,
    medium: tasks.filter(t => t.priority === 'medium').length,
    low: tasks.filter(t => t.priority === 'low').length
  };
  
  const completionRate = total > 0 ? ((completed / total) * 100).toFixed(1) + '%' : '0%';
  
  res.json({
    success: true,
    stats: {
      total,
      completed,
      pending,
      completionRate,
      byPriority,
      averageTasksPerPriority: (total / 3).toFixed(1)
    }
  });
});

// GET /api/health - 健康檢查
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    taskCount: tasks.length
  });
});

// 404 處理
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: '未找到',
    message: `路由 ${req.method} ${req.url} 不存在`,
    availableEndpoints: [
      'GET /api/tasks',
      'GET /api/tasks/:id',
      'POST /api/tasks',
      'PUT /api/tasks/:id',
      'PATCH /api/tasks/:id',
      'PATCH /api/tasks/:id/toggle',
      'DELETE /api/tasks/:id',
      'GET /api/stats',
      'GET /api/health'
    ]
  });
});

// 錯誤處理
app.use((err, req, res, next) => {
  console.error('服務器錯誤:', err);
  res.status(500).json({
    success: false,
    error: '服務器錯誤',
    message: err.message
  });
});

// 啟動服務器
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   任務管理 RESTful API                 ║
╠════════════════════════════════════════╣
║ 地址：http://localhost:${String(PORT).padEnd(18)}║
║ 時間：${new Date().toLocaleString('zh-CN').padEnd(20)}║
╠════════════════════════════════════════╣
║ 可用端點：                             ║
║ GET    /api/tasks       - 獲取任務列表  ║
║ GET    /api/tasks/:id   - 獲取單個任務  ║
║ POST   /api/tasks       - 創建新任務   ║
║ PUT    /api/tasks/:id   - 更新任務     ║
║ PATCH  /api/tasks/:id   - 部分更新     ║
║ DELETE /api/tasks/:id   - 刪除任務     ║
║ GET    /api/stats       - 統計信息     ║
║ GET    /api/health      - 健康檢查     ║
╚════════════════════════════════════════╝
  `);
});

// 優雅關閉
process.on('SIGINT', () => {
  console.log('\n👋 正在關閉服務器...');
  process.exit(0);
});
