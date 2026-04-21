#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetcher 组件 - 使用 Chrome Extension Relay 抓取微信文章

核心优势：
- 使用用户已登录的 Chrome Session
- 绕过人机验证
- 无需代理
"""

import subprocess
import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class Fetcher:
    """微信文章抓取器 - Chrome Extension Relay 方案"""
    
    # 支持的抓取方法
    METHODS = ["auto", "chrome", "playwright"]
    
    @staticmethod
    def fetch(url: str, method: str = "auto", timeout: int = 60) -> Dict:
        """
        抓取内容
        
        Args:
            url: 目标 URL
            method: 抓取方法 (auto/chrome/playwright)
            timeout: 超时时间（秒）
        
        Returns:
            {
                "title": str,           # 标题
                "markdown": str,        # Markdown 格式内容
                "html": str,            # 原始 HTML
                "source_url": str,      # 原始 URL
                "metadata": dict        # 元数据
            }
        """
        if method not in Fetcher.METHODS:
            raise ValueError(f"Invalid method: {method}. Must be one of {Fetcher.METHODS}")
        
        if method == "auto":
            return Fetcher._fetch_chrome(url, timeout)  # auto 默认用 chrome
        elif method == "chrome":
            return Fetcher._fetch_chrome(url, timeout)
        elif method == "playwright":
            return Fetcher._fetch_playwright(url, timeout)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def _fetch_chrome(url: str, timeout: int) -> Dict:
        """
        使用 Chrome Extension Relay 抓取（推荐）
        
        优势：
        - 使用用户已登录的 Session
        - 绕过人机验证
        - 无需代理
        """
        logger.info(f"Fetching with Chrome Relay: {url}")
        
        try:
            # Step 1: 先用 browser open 打开链接
            logger.info(f"Opening URL in Chrome profile...")
            open_result = subprocess.run(
                [
                    "openclaw", "browser",
                    "--browser-profile", "chrome",
                    "open", url
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            if open_result.returncode != 0:
                raise Exception(f"Failed to open URL: {open_result.stderr}")
            
            # Step 2: 等待页面加载后抓取 snapshot
            import time
            time.sleep(3)  # 等待页面加载
            
            logger.info(f"Capturing snapshot...")
            snapshot_result = subprocess.run(
                [
                    "openclaw", "browser",
                    "--browser-profile", "chrome",
                    "snapshot",
                    "--format", "ai"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )
            
            if snapshot_result.returncode == 0:
                content = snapshot_result.stdout.decode('utf-8') if isinstance(snapshot_result.stdout, bytes) else snapshot_result.stdout
                
                # 提取标题（AI snapshot 格式需要解析）
                # AI snapshot 通常第一行是标题或页面描述
                lines = content.strip().split('\n')
                title = lines[0].strip() if lines else ""
                
                return {
                    "title": title,
                    "markdown": content,
                    "html": "",
                    "source_url": url,
                    "metadata": {
                        "method": "chrome_relay",
                        "profile": "chrome",
                        "authenticated": True
                    }
                }
            else:
                error_msg = snapshot_result.stderr.decode('utf-8') if isinstance(snapshot_result.stderr, bytes) else snapshot_result.stderr
                raise Exception(f"Chrome Relay failed: {error_msg}")
        
        except subprocess.TimeoutExpired:
            raise Exception(f"Chrome Relay timeout after {timeout}s")
        except FileNotFoundError:
            raise Exception("OpenClaw CLI not found")
    
    @staticmethod
    def _fetch_playwright(url: str, timeout: int) -> Dict:
        """
        使用 Playwright 抓取（兜底方案）
        
        注意：此方案可能遇到人机验证
        """
        logger.info(f"Fetching with Playwright (fallback): {url}")
        
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError("Playwright not installed")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage"
                ],
                proxy={"server": "http://127.0.0.1:7890"}
            )
            page = browser.new_page()
            
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0"
            })
            
            page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            
            # 检查是否是验证页面
            content = page.content()
            if "环境异常" in content or "验证" in content:
                browser.close()
                raise Exception("Detected CAPTCHA page - Chrome Relay required")
            
            title = page.title()
            html = content
            markdown = Fetcher._html_to_markdown(html)
            
            browser.close()
            
            return {
                "title": title,
                "markdown": markdown,
                "html": html,
                "source_url": url,
                "metadata": {"method": "playwright", "authenticated": False}
            }
    
    @staticmethod
    def _html_to_markdown(html: str) -> str:
        """HTML 转 Markdown"""
        try:
            import html2text
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            return h.handle(html)
        except ImportError:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text(separator='\n', strip=True)
            except ImportError:
                return html


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fetcher.py <url> [method]")
        sys.exit(1)
    
    url = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "chrome"
    
    try:
        result = Fetcher.fetch(url, method)
        print(f"Title: {result['title']}")
        print(f"Markdown length: {len(result['markdown'])}")
        print(f"Method: {result['metadata']['method']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
