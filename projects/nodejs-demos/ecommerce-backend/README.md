# 電商後端 Demo - Node.js 實戰

**功能**: 完整的電商後端系統  
**技術棧**: Express + MongoDB + JWT + Stripe

## 📦 功能清單

- [x] 用戶註冊/登錄
- [x] 商品管理 (CRUD)
- [x] 購物車功能
- [x] 訂單管理
- [x] JWT 認證
- [x] 支付集成 (Stripe)

## 🚀 快速開始

```bash
# 安裝依賴
npm install

# 配置環境變量
cp .env.example .env

# 啟動服務器
npm start

# 開發模式
npm run dev
```

## 📚 API 文檔

### 用戶認證

```
POST /api/auth/register    - 用戶註冊
POST /api/auth/login       - 用戶登錄
GET  /api/auth/me          - 獲取當前用戶
```

### 商品管理

```
GET    /api/products       - 獲取所有商品
GET    /api/products/:id   - 獲取商品詳情
POST   /api/products       - 創建商品 (管理員)
PUT    /api/products/:id   - 更新商品 (管理員)
DELETE /api/products/:id   - 刪除商品 (管理員)
```

### 購物車

```
GET    /api/cart           - 獲取購物車
POST   /api/cart/items     - 添加商品到購物車
PUT    /api/cart/items/:id - 更新購物車商品
DELETE /api/cart/items/:id - 從購物車刪除
```

### 訂單

```
GET    /api/orders         - 獲取訂單列表
GET    /api/orders/:id     - 獲取訂單詳情
POST   /api/orders         - 創建訂單
POST   /api/orders/:id/pay - 支付訂單
```

## 💰 變現說明

此 Demo 可用於：
- 接電商外包項目 (¥30000-100000)
- 培訓課程實戰案例
- 技術諮詢演示
- 個人作品集展示

---

**創建時間**: 2026-03-19  
**作者**: RedOpenClaw
