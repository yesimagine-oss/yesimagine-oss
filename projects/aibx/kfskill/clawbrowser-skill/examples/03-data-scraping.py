#!/usr/bin/env python3
"""
示例 3：數據抓取
"""

from browser_tool import ClawBrowser

browser = ClawBrowser(session_name="scrape")

# 打開列表頁
browser.open("https://example.com/products")

# 獲取快照
print("頁面元素：")
print(browser.snapshot())

# 提取產品信息
products = browser.extract(".product-name")
prices = browser.extract(".product-price")

print(f"\n找到 {len(products)} 個產品：")
for i, (name, price) in enumerate(zip(products, prices)):
    print(f"{i+1}. {name} - {price}")

browser.close()
