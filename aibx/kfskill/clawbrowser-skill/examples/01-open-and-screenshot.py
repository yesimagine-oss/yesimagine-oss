#!/usr/bin/env python3
"""
示例 1：打開網頁並截圖
"""

from browser_tool import ClawBrowser

# 創建瀏覽器實例
browser = ClawBrowser(session_name="demo")

# 打開網頁
browser.open("https://example.com")

# 等待加載
browser.wait("networkidle")

# 截圖
browser.screenshot("example.png")

# 關閉
browser.close()

print("✅ 完成！截圖已保存為 example.png")
