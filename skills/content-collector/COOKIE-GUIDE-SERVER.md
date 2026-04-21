# 🍪 微信 Cookie 導出指南（服務器版）

**問題**: 服務器沒有圖形界面，無法運行可見瀏覽器  
**解決方案**: 在本地電腦登錄微信，導出 Cookie 後上傳到服務器

---

## 📋 步驟總覽

1. **在本地電腦**（有瀏覽器的電腦）導出 Cookie
2. **複製 Cookie 文件**到服務器
3. **設置環境變量**並測試

---

## 🔧 步驟 1: 在本地電腦導出 Cookie

### 方法 A: 使用瀏覽器擴展（推薦）⭐⭐⭐⭐⭐

#### Chrome/Edge 用戶：

1. **安裝擴展**：
   - Chrome 網上應用店搜索 "EditThisCookie" 或 "Cookie Editor"
   - 安裝：https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

2. **登錄微信公眾號**：
   - 打開 https://mp.weixin.qq.com
   - 用微信掃碼或賬號密碼登錄
   - 確保能正常訪問後台

3. **導出 Cookie**：
   - 點擊瀏覽器工具欄的 EditThisCookie 圖標
   - 點擊 "Export"（導出）按鈕
   - 選擇 "JSON" 格式
   - 保存為 `wechat-cookies.json`

#### Firefox 用戶：

1. **安裝擴展**：
   - Firefox 附加组件商店搜索 "Cookie Quick Manager"
   - 安裝：https://addons.mozilla.org/firefox/addon/cookie-quick-manager/

2. **登錄並導出**：
   - 打開 https://mp.weixin.qq.com 並登錄
   - 打開 Cookie Quick Manager
   - 選擇所有 `.qq.com` 和 `.wechat.com` 的 Cookie
   - 導出為 JSON

---

### 方法 B: 使用開發者工具（無需安裝擴展）

#### Chrome/Edge：

1. **打開開發者工具**：
   - 訪問 https://mp.weixin.qq.com 並登錄
   - 按 `F12` 或右鍵 → 檢查

2. **找到 Cookie**：
   - 點擊 "Application"（應用程序）標籤
   - 左側展開 "Cookies" → 選擇 "https://mp.weixin.qq.com"

3. **複製 Cookie**：
   - 右鍵點擊任意 Cookie → "Copy" → "Copy All"
   - 或使用控制台命令：
   ```javascript
   // 在控制台運行
   JSON.stringify(document.cookie.split('; ').map(c => {
     const [name, value] = c.split('=');
     return {
       name: name,
       value: value,
       domain: '.qq.com',
       path: '/',
       httpOnly: true,
       secure: true
     };
   }))
   ```

4. **保存為 JSON 文件**：
   ```json
   [
     {
       "name": "slave_user",
       "value": "MzI...（很長）",
       "domain": ".qq.com",
       "path": "/"
     },
     ...
   ]
   ```

---

## 📤 步驟 2: 上傳 Cookie 到服務器

### 方法 A: 使用 SCP

```bash
# 在本地電腦執行
scp ~/Downloads/wechat-cookies.json admin@你的服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

### 方法 B: 使用 Feishu/微信發送

1. 本地電腦將 `wechat-cookies.json` 發送到飛書/微信
2. 在服務器上下載文件
3. 移動到正確位置：
```bash
mkdir -p ~/.openclaw/workspace/cookies
mv ~/Downloads/wechat-cookies.json ~/.openclaw/workspace/cookies/
```

### 方法 C: 直接粘貼內容

1. 在本地電腦打開 `wechat-cookies.json`
2. 複製全部內容
3. 在服務器上創建文件：
```bash
mkdir -p ~/.openclaw/workspace/cookies
nano ~/.openclaw/workspace/cookies/wechat-cookies.json
# 粘貼內容，按 Ctrl+X → Y → Enter 保存
```

---

## ✅ 步驟 3: 驗證並測試

### 1. 檢查 Cookie 文件

```bash
# 在服務器上
ls -la ~/.openclaw/workspace/cookies/
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20
```

應該看到類似：
```json
[
  {
    "name": "slave_user",
    "value": "MzI...（很長）",
    "domain": ".qq.com",
    ...
  }
]
```

### 2. 設置權限

```bash
chmod 600 ~/.openclaw/workspace/cookies/wechat-cookies.json
```

### 3. 啟用 Cookie 並測試

```bash
# 設置環境變量
export WECHAT_COOKIES_ENABLED=true

# 測試抓取
cd ~/.openclaw/workspace/skills/content-collector
node index.js "https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw"
```

---

## 🎯 成功標誌

```
🍪 正在載入 Cookie...
🔍 找到 15/150 個微信相關 Cookie
✅ 已載入 15 個 Cookie
✅ 找到正文選擇器：#js_content
✅ 標題：文章真實標題
📝 轉換為 Markdown...
✅ 收藏成功！
```

---

## 🐛 故障排查

### 問題 1: Cookie 文件格式錯誤

```bash
# 驗證 JSON 格式
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | python3 -m json.tool
```

如果報錯，說明 JSON 格式不對，需要重新導出。

### 問題 2: Cookie 已過期

Cookie 有效期通常 7-30 天。過期後：
1. 重新在本地電腦登錄微信公眾號
2. 重新導出 Cookie
3. 覆蓋舊文件

### 問題 3: 還是顯示「環境異常」

可能原因：
- Cookie 不完整（只導出了部分）
- 域名不對（應該是 `.qq.com` 或 `mp.weixin.qq.com`）
- 微信風控升級

**解決方案**：
```bash
# 檢查 Cookie 內容
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | grep -E "slave_user|slave_sid|uin|key"

# 應該看到這些關鍵 Cookie：
# - slave_user
# - slave_sid
# - uin
# - key
# - pass_ticket（可選）
```

---

## 📖 Cookie 文件示例

正確的格式應該類似：

```json
[
  {
    "name": "slave_user",
    "value": "MzI1Nj...（50-200 字符）",
    "domain": ".qq.com",
    "path": "/",
    "httpOnly": true,
    "secure": true
  },
  {
    "name": "slave_sid",
    "value": "cnp...（50-200 字符）",
    "domain": ".qq.com",
    "path": "/",
    "httpOnly": true,
    "secure": true
  },
  ...
]
```

---

## 💡 提示

- ✅ **Cookie 越新越好** - 剛登錄後立即導出
- ✅ **Cookie 越多越好** - 導出所有 `.qq.com` 相關的
- ✅ **包含關鍵 Cookie** - `slave_user`, `slave_sid`, `uin`, `key`
- ✅ **定期更新** - 每 1-2 週重新導出一次
- ❌ **不要分享** - Cookie 等於你的登錄憑證

---

**最後更新**: 2026-03-19  
**維護者**: 麻小 🦐
