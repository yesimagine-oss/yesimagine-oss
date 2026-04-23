# ClawBrowser Skill

**版本:** 2.0.0  
**創建:** 2026-04-14  
**基於:** agent-browser

---

## 簡介

ClawBrowser 是 OpenClaw 的無頭瀏覽器自動化 Skill，基於 agent-browser 實現。

## 功能

- ✅ 打開網頁
- ✅ 獲取 ARIA 快照
- ✅ 點擊元素
- ✅ 填寫表單
- ✅ 截圖
- ✅ 數據抓取
- ✅ 會話管理

## 快速開始

```bash
# 1. 安裝依賴
npm install -g agent-browser
agent-browser install

# 2. 使用 Skill
clawbrowser open https://example.com
clawbrowser snapshot -i
clawbrowser screenshot page.png
```

## 目錄結構

```
clawbrowser-skill/
├── SKILL.md          # Skill 定義
├── README.md         # 本文件
├── browser_tool.py   # Python 集成
└── examples/         # 使用示例
```

## 文檔

完整文檔見知識庫：
- [[openclaw-browser-complete-guide-index]]

## License

MIT

---

## 簽名

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

---

**創建:** 2026-04-14  
**版本:** 2.0.0  
**基於:** clawbrowser-core v1.0.0 (2026-04-04)
