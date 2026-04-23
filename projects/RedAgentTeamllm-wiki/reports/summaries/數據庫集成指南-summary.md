# Node.js 數據庫集成指南

**創建時間**: 2026-03-19  
**難度**: ⭐⭐ 中級  
**參考文檔**: https://mongoosejs.com/

---

## 📊 MongoDB 集成

### 安裝與連接

```bash
npm install mongoose
```

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb', {
