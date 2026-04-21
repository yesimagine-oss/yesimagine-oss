# 🍪 5 分鐘導出微信 Cookie（圖文教程）

**適用**: Windows/Mac 本地電腦  
**時間**: 5 分鐘  
**難度**: ⭐⭐（需要安裝擴展）

---

## 🚀 快速開始（推薦方法）

### 方法 1: 使用 EditThisCookie 擴展（最簡單）⭐⭐⭐⭐⭐

#### 第 1 步：安裝擴展（1 分鐘）

**Chrome/Edge 用戶：**
1. 打開 Chrome 網上應用店
2. 搜索 "EditThisCookie"
3. 點擊 "添加至 Chrome"

或直接訪問：
```
https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
```

**Firefox 用戶：**
1. 打開 Firefox 附加组件商店
2. 搜索 "Cookie Quick Manager"
3. 點擊 "添加到 Firefox"

或直接訪問：
```
https://addons.mozilla.org/firefox/addon/cookie-quick-manager/
```

---

#### 第 2 步：登錄微信公眾號（2 分鐘）

1. 打開瀏覽器
2. 訪問：https://mp.weixin.qq.com
3. 使用微信掃碼或輸入賬號密碼登錄
4. 確保能正常進入後台（看到"新的創作"等菜單）

**✅ 成功標誌：**
- 右上角顯示你的公眾號頭像
- 能看到"發表文章"、"內容管理"等菜單
- 不是"環境異常"頁面

---

#### 第 3 步：導出 Cookie（1 分鐘）

**使用 EditThisCookie（Chrome）：**

1. 點擊瀏覽器右上角的 🍪 Cookie 圖標
2. 在彈出窗口中，點擊 **"Export"** 按鈕（圖標像個向下箭頭）
3. 選擇 **"JSON"** 格式
4. 瀏覽器會自動下載 `cookies.txt` 或 `cookies.json` 文件

**使用 Cookie Quick Manager（Firefox）：**

1. 按 `F12` 打開開發者工具
2. 找到 "Cookie Quick Manager" 標籤
3. 選擇所有 `.qq.com` 開頭的 Cookie
4. 右鍵 → "Export" → "JSON"
5. 保存為 `wechat-cookies.json`

---

#### 第 4 步：檢查 Cookie 文件（30 秒）

打開剛下載的文件，應該看到類似：

```json
[
  {
    "domain": ".qq.com",
    "expirationDate": 1234567890,
    "hostOnly": false,
    "httpOnly": true,
    "name": "slave_user",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "MzI1Nj..."
  },
  {
    "domain": ".qq.com",
    "name": "slave_sid",
    "value": "cnp..."
  }
]
```

**✅ 關鍵檢查：**
- 文件是 **JSON 數組**（以 `[` 開頭）
- 包含 `slave_user` 和 `slave_sid`
- `domain` 是 `.qq.com` 或 `mp.weixin.qq.com`
- 至少有 **10-20 個 Cookie**

---

## 📤 上傳到服務器

### 方法 A: 使用 SCP（推薦）⭐⭐⭐⭐⭐

**Windows 用戶（使用 PowerShell）：**
```powershell
# 下載目錄
$cookieFile = "$env:USERPROFILE\Downloads\wechat-cookies.json"

# 上傳到服務器（替換成你的服務器 IP）
scp $cookieFile admin@你的服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

**Mac 用戶（使用終端）：**
```bash
# 上傳到服務器
scp ~/Downloads/wechat-cookies.json admin@你的服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

**需要輸入服務器密碼**，輸入後文件就會上傳。

---

### 方法 B: 使用 Feishu 飛書（無需命令）⭐⭐⭐⭐

1. **在本地電腦**：
   - 打開飛書
   - 找到"文件"功能
   - 上傳 `wechat-cookies.json`

2. **在服務器上**：
   - 打開飛書網頁版或客戶端
   - 下載剛才上傳的文件
   - 移動到正確位置：
   ```bash
   mkdir -p ~/.openclaw/workspace/cookies
   mv ~/Downloads/wechat-cookies.json ~/.openclaw/workspace/cookies/
   ```

---

### 方法 C: 手動複製粘貼（萬一無法上傳）⭐⭐⭐

1. **在本地電腦**：
   - 用記事本打開 `wechat-cookies.json`
   - 全選（Ctrl+A）→ 複製（Ctrl+C）

2. **在服務器上**：
   ```bash
   # 創建目錄
   mkdir -p ~/.openclaw/workspace/cookies
   
   # 創建文件
   nano ~/.openclaw/workspace/cookies/wechat-cookies.json
   
   # 粘貼內容（Ctrl+Shift+V 或右鍵粘貼）
   # 按 Ctrl+X → Y → Enter 保存
   ```

---

## ✅ 驗證並測試

### 在服務器上執行：

```bash
# 1. 檢查 Cookie 文件
ls -la ~/.openclaw/workspace/cookies/

# 2. 查看內容（前 20 行）
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20

# 3. 設置環境變量
export WECHAT_COOKIES_ENABLED=true

# 4. 測試抓取
cd ~/.openclaw/workspace/skills/content-collector
node index.js "https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw"
```

**✅ 成功輸出：**
```
🍪 正在載入 Cookie...
🔍 找到 15/150 個微信相關 Cookie
✅ 已載入 15 個 Cookie
📦 開始收藏：https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw
✅ 找到正文選擇器：#js_content
✅ 標題：文章真實標題
✅ 收藏成功！
```

---

## 🐛 常見問題

### Q1: 下載的文件不是 JSON 格式？

**EditThisCookie** 有時會下載 `.txt` 文件，沒關係：
```bash
# 重命名文件
mv ~/Downloads/cookies.txt ~/.openclaw/workspace/cookies/wechat-cookies.json
```

---

### Q2: Cookie 文件是空的或只有幾個？

**原因**：還沒登錄就導出了

**解決方案**：
1. 確保已登錄微信公眾號後台
2. 刷新頁面（F5）
3. 再次導出 Cookie

---

### Q3: 找不到 `slave_user` 或 `slave_sid`？

**原因**：可能導出了錯誤的域名

**解決方案**：
1. 確保訪問的是 `https://mp.weixin.qq.com`
2. 在擴展中過濾 `.qq.com` 的 Cookie
3. 重新導出

---

### Q4: 上傳後還是失敗？

檢查 Cookie 是否過期：
```bash
# 查看 Cookie 中的關鍵字段
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | grep -E "slave_user|slave_sid"
```

如果輸出為空，說明 Cookie 文件有問題，需要重新導出。

---

## 📞 需要幫助？

如果遇到問題，請提供：

1. **Cookie 文件前 20 行**（隱藏敏感值）：
   ```bash
   cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20
   ```

2. **錯誤信息**：
   ```bash
   # 完整錯誤輸出
   node index.js "https://mp.weixin.qq.com/s/xxx" 2>&1
   ```

3. **使用的擴展名稱和版本**

---

## 🔒 安全提醒

- ✅ Cookie 文件設置為僅所有者可讀：`chmod 600 ~/.openclaw/workspace/cookies/wechat-cookies.json`
- ✅ 不要上傳到 GitHub 等公開倉庫
- ✅ 不要分享給他人
- ✅ 定期更新（每 1-2 週）
- ❌ 不要在公共電腦操作

---

**教程版本**: 1.0  
**最後更新**: 2026-03-19  
**維護者**: 麻小 🦐
