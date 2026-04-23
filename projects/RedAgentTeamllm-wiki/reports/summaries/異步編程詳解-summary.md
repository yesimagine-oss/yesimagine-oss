# Node.js 異步編程詳解

**創建時間**: 2026-03-19  
**難度**: ⭐⭐⭐ 進階  
**參考文檔**: https://nodejs.org/docs/latest/api/async_hooks.html

---

## 📚 異步編程演進

### 1. 回調函數 (Callback)

```javascript
// 回調地獄示例
fs.readFile('file1.txt', 'utf-8', (err, data1) => {
  if (err) throw err;
  fs.readFile('file2.txt', 'utf-8', (err, data2) => {
    if (err) throw err;
    fs.readFile('file3.txt', 'utf-8', (err, data3) => {
      if (err) throw err;
