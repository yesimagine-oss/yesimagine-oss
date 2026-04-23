// REST API Demo - Node.js 快速入門
// 功能：用戶管理 API (CRUD)

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// 中間件
app.use(cors());
app.use(helmet());
app.use(express.json());

// 模擬數據庫
let users = [
  { id: 1, name: '小明', email: 'xiao@example.com', age: 18 },
  { id: 2, name: '小紅', email: 'hong@example.com', age: 20 }
];

// 健康檢查
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// 獲取所有用戶
app.get('/api/users', (req, res) => {
  res.json({ success: true, data: users });
});

// 獲取單個用戶
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ success: false, error: '用戶不存在' });
  }
  res.json({ success: true, data: user });
});

// 創建用戶
app.post('/api/users', (req, res) => {
  const { name, email, age } = req.body;
  
  // 驗證
  if (!name || !email) {
    return res.status(400).json({ success: false, error: '姓名和郵箱必填' });
  }
  
  const newUser = {
    id: users.length + 1,
    name,
    email,
    age: age || 0
  };
  
  users.push(newUser);
  res.status(201).json({ success: true, data: newUser });
});

// 更新用戶
app.put('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ success: false, error: '用戶不存在' });
  }
  
  const { name, email, age } = req.body;
  if (name) user.name = name;
  if (email) user.email = email;
  if (age) user.age = age;
  
  res.json({ success: true, data: user });
});

// 刪除用戶
app.delete('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));
  if (index === -1) {
    return res.status(404).json({ success: false, error: '用戶不存在' });
  }
  
  users.splice(index, 1);
  res.json({ success: true, message: '刪除成功' });
});

// 404 處理
app.use((req, res) => {
  res.status(404).json({ success: false, error: '路由不存在' });
});

// 錯誤處理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, error: '服務器錯誤' });
});

// 啟動服務器
app.listen(PORT, () => {
  console.log(`🚀 REST API 服務器運行在 http://localhost:${PORT}`);
  console.log(`📚 API 文檔:`);
  console.log(`   GET    /health          - 健康檢查`);
  console.log(`   GET    /api/users       - 獲取所有用戶`);
  console.log(`   GET    /api/users/:id   - 獲取單個用戶`);
  console.log(`   POST   /api/users       - 創建用戶`);
  console.log(`   PUT    /api/users/:id   - 更新用戶`);
  console.log(`   DELETE /api/users/:id   - 刪除用戶`);
});
