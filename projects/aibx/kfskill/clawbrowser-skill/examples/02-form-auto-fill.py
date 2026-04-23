#!/usr/bin/env python3
"""
示例 2：自動填寫表單
"""

from browser_tool import ClawBrowser

browser = ClawBrowser(session_name="form")

# 打開表單頁面
browser.open("https://example.com/form")

# 獲取快照
print("頁面元素：")
print(browser.snapshot())

# 填寫表單
browser.fill("@e1", "user@example.com")  # 郵箱
browser.fill("@e2", "password123")       # 密碼

# 提交
browser.click("@e3")  # 提交按鈕

# 等待並截圖
browser.wait("networkidle")
browser.screenshot("form-submitted.png")

browser.close()
print("✅ 表單提交完成！")
