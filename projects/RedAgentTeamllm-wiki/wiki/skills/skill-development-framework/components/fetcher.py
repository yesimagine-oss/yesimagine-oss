#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetcher 组件 - 通用内容抓取器

支持多种抓取方案，自动选择最优
"""

import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Fetcher:
    """通用内容抓取器"""
    
    # 支持的抓取方法
    METHODS = ["auto", "jina", "playwright", "kimi"]
    
    @staticmethod
    def fetch(url: str, method: str = "auto", timeout: int = 30) -> Dict:
        """
        抓取内容
        
        Args:
            url: 目标 URL
            method: 抓取方法 (auto/jina/playwright/kimi)
            timeout: 超时时间（秒）
        
        Returns:
            {
                "title": str,           # 标题
                "markdown": str,        # Markdown 格式内容
                "html": str,            # 原始 HTML
                "source_url": str       # 原始 URL
            }
        
        Raises:
            ValueError: 无效的抓取方法
            requests.Timeout: 请求超时
            Exception: 其他错误
        """
        if method not in Fetcher.METHODS:
            raise ValueError(f"Invalid method: {method}. Must be one of {Fetcher.METHODS}")
        
        if method == "auto":
            return Fetcher._fetch_auto(url, timeout)
        elif method == "jina":
            return Fetcher._fetch_jina(url, timeout)
        elif method == "playwright":
            return Fetcher._fetch_playwright(url, timeout)
        elif method == "kimi":
            return Fetcher._fetch_kimi(url, timeout)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def _fetch_auto(url: str, timeout: int) -> Dict:
        """自动选择最优抓取方案"""
        logger.info(f"Auto fetching: {url}")
        
        # 优先级：kimi > jina > playwright
        methods = ["kimi", "jina", "playwright"]
        
        for method in methods:
            try:
                logger.info(f"Trying method: {method}")
                if method == "kimi":
                    return Fetcher._fetch_kimi(url, timeout)
                elif method == "jina":
                    return Fetcher._fetch_jina(url, timeout)
                elif method == "playwright":
                    return Fetcher._fetch_playwright(url, timeout)
            except Exception as e:
                logger.warning(f"Method {method} failed: {e}")
                continue
        
        raise Exception("All fetch methods failed")
    
    @staticmethod
    def _fetch_jina(url: str, timeout: int) -> Dict:
        """使用 Jina AI 抓取"""
        logger.info(f"Fetching with Jina: {url}")
        
        response = requests.get(
            f"https://r.jina.ai/{url}",
            timeout=timeout
        )
        response.raise_for_status()
        
        return {
            "title": "",  # Jina 不返回标题
            "markdown": response.text,
            "html": "",
            "source_url": url
        }
    
    @staticmethod
    def _fetch_kimi(url: str, timeout: int) -> Dict:
        """使用 Kimi AI 抓取"""
        logger.info(f"Fetching with Kimi: {url}")
        
        # 这里需要 Kimi API 集成
        # 示例代码：
        # response = kimi_fetch(url)
        # return response
        
        # 临时使用 Jina 作为替代
        return Fetcher._fetch_jina(url, timeout)
    
    @staticmethod
    def _fetch_playwright(url: str, timeout: int) -> Dict:
        """使用 Playwright 抓取（需要安装）"""
        logger.info(f"Fetching with Playwright: {url}")
        
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError("Playwright not installed. Run: pip install playwright")
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=timeout * 1000)
            
            title = page.title()
            html = page.content()
            markdown = Fetcher._html_to_markdown(html)
            
            browser.close()
            
            return {
                "title": title,
                "markdown": markdown,
                "html": html,
                "source_url": url
            }
    
    @staticmethod
    def _html_to_markdown(html: str) -> str:
        """HTML 转 Markdown"""
        try:
            import html2text
            h = html2text.HTML2Text()
            return h.handle(html)
        except ImportError:
            # 如果没有 html2text，返回原始 HTML
            logger.warning("html2text not installed, returning raw HTML")
            return html


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fetcher.py <url> [method]")
        sys.exit(1)
    
    url = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    try:
        result = Fetcher.fetch(url, method)
        print(f"Title: {result['title']}")
        print(f"Markdown length: {len(result['markdown'])}")
        print(f"HTML length: {len(result['html'])}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
