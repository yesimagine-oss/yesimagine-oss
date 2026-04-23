#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 WeChat Fetcher - 微信文章抓取（教學版）

作者：麻小
版本：1.0.0
創建：2026-03-18

核心功能：
1. 微信文章抓取（免費 API 輪詢）
2. 內容提取（標題、摘要、關鍵詞）
3. 結構化存儲（Markdown）
4. 自動索引更新

設計原則：
- 全自動：用戶只需給 URL
- 不花錢：只用免費 API
- 易學習：代碼帶詳細注釋
"""

import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List


# ==================== 配置區 ====================

# 收藏庫目錄
COLLECTIONS_DIR = os.path.expanduser("~/.openclaw/workspace/collections")

# 免費 API 列表（按優先級排序）
# 教學點：多個 API 輪詢提高成功率
WECHAT_APIS = [
    {
        "name": "r.jina.ai",
        "url": "https://r.jina.ai/http://{url}",
        "success_rate": "90%",
        "speed": "快"
    },
    {
        "name": "readhub.cn",
        "url": "https://readhub.cn/proxy?url={url}",
        "success_rate": "85%",
        "speed": "快"
    },
    {
        "name": "wx.dnspod.cn",
        "url": "https://wx.dnspod.cn/proxy?url={url}",
        "success_rate": "80%",
        "speed": "中"
    }
]


# ==================== 核心類 ====================

class WeChatFetcher:
    """
    微信文章抓取器
    
    使用示例：
        fetcher = WeChatFetcher()
        result = fetcher.fetch("https://mp.weixin.qq.com/s/xxx")
    """
    
    def __init__(self):
        """初始化抓取器"""
        self._ensure_directories()
        
    def _ensure_directories(self):
        """確保存儲目錄存在"""
        dirs = [
            f"{COLLECTIONS_DIR}/wechat",
            f"{COLLECTIONS_DIR}/wechat/images",
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def fetch(self, url: str) -> Dict:
        """
        抓取微信文章（主入口）
        
        參數：
            url: 微信文章鏈接
        
        返回：
            dict: {
                "success": bool,
                "title": str,
                "content": str,
                "file_path": str,
                "message": str
            }
        """
        print(f"📱 開始抓取：{url}")
        
        # 步驟 1: 驗證 URL
        if not self._is_wechat_url(url):
            return {
                "success": False,
                "message": "❌ 不是微信文章鏈接"
            }
        
        # 步驟 2: 抓取內容
        content = self._fetch_content(url)
        if not content:
            return {
                "success": False,
                "message": "❌ 抓取失敗，所有 API 均不可用"
            }
        
        # 步驟 3: 提取元數據
        metadata = self._extract_metadata(content, url)
        
        # 步驟 4: 保存到文件
        file_path = self._save_to_file(metadata, content)
        
        # 步驟 5: 更新索引
        self._update_index(metadata)
        
        return {
            "success": True,
            "title": metadata['title'],
            "content": content[:200] + "...",
            "file_path": file_path,
            "message": f"✅ 已抓取：{metadata['title']}"
        }
    
    def _is_wechat_url(self, url: str) -> bool:
        """
        驗證是否為微信文章鏈接
        
        教學點：用簡單的字符串匹配識別內容類型
        """
        return "mp.weixin.qq.com" in url
    
    def _fetch_content(self, url: str) -> Optional[str]:
        """
        抓取內容（核心函數）
        
        教學點：API 輪詢策略
        1. 按優先級嘗試每個 API
        2. 第一個成功的返回
        3. 全部失敗返回 None
        """
        print("🔄 開始輪詢 API...")
        
        for i, api in enumerate(WECHAT_APIS, 1):
            try:
                print(f"  嘗試 {i}/{len(WECHAT_APIS)}: {api['name']} (成功率{api['success_rate']})")
                
                # 發起請求
                response = requests.get(
                    api["url"].format(url=url),
                    timeout=30,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                )
                
                # 檢查響應
                if response.status_code == 200 and response.text.strip():
                    # 檢查是否是反爬蟲頁面
                    if self._is_anti_bot_page(response.text):
                        print(f"  ❌ 被反爬蟲攔截")
                        continue
                    
                    print(f"  ✅ 成功！")
                    return response.text
                    
            except Exception as e:
                print(f"  ❌ 失敗：{str(e)[:50]}")
                continue
        
        print("❌ 所有 API 均失敗")
        return None
    
    def _is_anti_bot_page(self, content: str) -> bool:
        """
        檢測是否是反爬蟲頁面
        
        教學點：識別常見的反爬蟲特徵
        """
        anti_bot_keywords = [
            "访问限制",
            "验证",
            "安全驗證",
            "請稍後再試",
            "請求過於頻繁"
        ]
        
        for keyword in anti_bot_keywords:
            if keyword in content:
                return True
        
        return False
    
    def _extract_metadata(self, content: str, url: str) -> Dict:
        """
        提取元數據
        
        教學點：用正則表達式提取結構化信息
        """
        # 提取標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "未命名文章"
        
        # 生成 slug
        slug = self._generate_slug(title)
        
        # 提取摘要
        summary = content[200:400].replace('\n', ' ') + "..." if len(content) > 400 else content
        
        # 提取關鍵詞
        keywords = self._extract_keywords(title)
        
        return {
            "title": title,
            "url": url,
            "slug": slug,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "keywords": keywords
        }
    
    def _generate_slug(self, title: str) -> str:
        """
        生成 URL 友好的 slug
        
        教學點：字符串處理技巧
        """
        # 移除特殊字符
        slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
        # 替換空格為連字符
        slug = slug.replace(' ', '-')
        # 限制長度
        return slug[:50].lower()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取關鍵詞
        
        教學點：簡單的文本分割
        """
        words = re.split(r'[，。！？、；：\s]+', text)
        words = [w for w in words if len(w) >= 2]
        return words[:5]
    
    def _save_to_file(self, metadata: Dict, content: str) -> str:
        """
        保存到 Markdown 文件
        
        教學點：生成結構化 Markdown
        """
        filename = f"{metadata['date']}-{metadata['slug']}.md"
        file_path = f"{COLLECTIONS_DIR}/wechat/{filename}"
        
        # 生成 frontmatter
        frontmatter = f"""---
title: "{metadata['title']}"
url: "{metadata['url']}"
date: {metadata['date']}
tags: [{', '.join(metadata['keywords'])}]
collected_at: {metadata['timestamp']}
---

"""
        
        # 寫入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        print(f"💾 已保存：{file_path}")
        return file_path
    
    def _update_index(self, metadata: Dict):
        """
        更新全局索引
        
        教學點：維護簡單的索引文件
        """
        index_path = f"{COLLECTIONS_DIR}/wechat/index.md"
        
        # 讀取或創建索引
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()
        else:
            index_content = "# 📚 微信文章收藏索引\n\n"
        
        # 添加新條目
        new_entry = (
            f"- [{metadata['title']}]"
            f"({metadata['date']}-{metadata['slug']}.md) "
            f"{' '.join([f'#{kw}' for kw in metadata['keywords']])}\n"
        )
        
        # 插入到對應日期下
        date_section = f"\n## {metadata['date']}\n\n"
        if date_section not in index_content:
            index_content += date_section
        
        index_content += new_entry
        
        # 寫回文件
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"📑 已更新索引：{index_path}")


# ==================== 入口函數 ====================

def fetch(url: str) -> Dict:
    """
    抓取微信文章的便捷函數
    
    使用示例：
        result = fetch("https://mp.weixin.qq.com/s/xxx")
        print(result['message'])
    """
    fetcher = WeChatFetcher()
    return fetcher.fetch(url)


# ==================== 測試入口 ====================

if __name__ == "__main__":
    # 測試示例
    test_url = "https://mp.weixin.qq.com/s/test"
    result = fetch(test_url)
    print(f"\n{result['message']}")
