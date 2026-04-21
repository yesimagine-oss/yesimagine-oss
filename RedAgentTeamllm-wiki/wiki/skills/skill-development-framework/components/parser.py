#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser 组件 - 通用内容解析器

支持 HTML 转 Markdown、图片提取、元数据提取
"""

import re
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Parser:
    """通用内容解析器"""
    
    # 图片提取正则
    IMG_MD_PATTERN = re.compile(r'!\[(.*?)\]\(([^)]+)\)')
    IMG_HTML_PATTERN = re.compile(r'<img[^>]+(?:src|data-src|data-original)=["\']([^"\']+)["\']', re.I)
    IMG_SRCSET_PATTERN = re.compile(r'<img[^>]+srcset=["\']([^"\']+)["\']', re.I)
    
    @staticmethod
    def parse(raw: Dict, format: str = "markdown") -> Dict:
        """
        解析内容
        
        Args:
            raw: 原始内容（Fetcher 返回值）
            format: 输出格式 (markdown/html/json)
        
        Returns:
            {
                "title": str,           # 标题
                "content": str,         # 处理后的内容
                "metadata": Dict,       # 元数据
                "images": List[str]     # 图片 URL 列表
            }
        """
        logger.info(f"Parsing content, format: {format}")
        
        return {
            "title": raw.get("title", ""),
            "content": raw.get("markdown", raw.get("content", "")),
            "metadata": Parser._extract_metadata(raw),
            "images": Parser._extract_images(raw)
        }
    
    @staticmethod
    def _extract_metadata(raw: Dict) -> Dict:
        """提取元数据"""
        return {
            "source_url": raw.get("source_url", ""),
            "fetch_time": datetime.now().isoformat(),
            "word_count": len(raw.get("markdown", "")),
            "has_images": bool(Parser._extract_images(raw))
        }
    
    @staticmethod
    def _extract_images(raw: Dict) -> List[str]:
        """提取图片 URL"""
        html = raw.get("html", "")
        markdown = raw.get("markdown", "")
        
        images = []
        
        # 从 Markdown 提取
        for alt, ref in Parser.IMG_MD_PATTERN.findall(markdown):
            if ref and ref not in images:
                images.append(ref)
        
        # 从 HTML 提取
        for ref in Parser.IMG_HTML_PATTERN.findall(html):
            if ref and ref not in images:
                images.append(ref)
        
        # 从 srcset 提取
        for srcset_value in Parser.IMG_SRCSET_PATTERN.findall(html):
            candidate = Parser._pick_srcset_candidate(srcset_value)
            if candidate and candidate not in images:
                images.append(candidate)
        
        logger.info(f"Extracted {len(images)} images")
        return images
    
    @staticmethod
    def _pick_srcset_candidate(srcset_value: str) -> str:
        """从 srcset 选择最佳图片"""
        # 示例："a.jpg 1x, b.jpg 2x" 或 "a.jpg 480w, b.jpg 1080w"
        parts = [x.strip() for x in (srcset_value or "").split(",") if x.strip()]
        if not parts:
            return ""
        
        # 选择最后一个（通常是最清晰的）
        return parts[-1].split(" ")[0].strip()
    
    @staticmethod
    def replace_images(content: str, image_key_map: Dict[str, str]) -> str:
        """
        替换图片 URL 为飞书 image_key
        
        Args:
            content: Markdown 内容
            image_key_map: {原 URL: 飞书 image_key}
        
        Returns:
            替换后的内容
        """
        logger.info(f"Replacing {len(image_key_map)} images")
        
        processed = content
        for src, image_key in image_key_map.items():
            processed = processed.replace(f"({src})", f"({image_key})")
        
        return processed
    
    @staticmethod
    def append_images(content: str, images: List[tuple]) -> str:
        """
        追加图片到文末
        
        Args:
            content: Markdown 内容
            images: [(alt, image_key), ...]
        
        Returns:
            追加后的内容
        """
        if not images:
            return content
        
        lines = ["", "---", "", "## 🖼️ 原文配图（自动抓取）", ""]
        for alt, image_key in images:
            lines.append(f"![{alt}]({image_key})")
        
        return content + "\n".join(lines)
    
    @staticmethod
    def extract_key_points(content: str, max_points: int = 5) -> List[str]:
        """
        提取核心要点
        
        Args:
            content: 内容文本
            max_points: 最大要点数
        
        Returns:
            要点列表
        """
        # 简单实现：提取前 N 个非空行
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        return lines[:max_points]
    
    @staticmethod
    def html_to_markdown(html: str) -> str:
        """HTML 转 Markdown"""
        try:
            import html2text
            h = html2text.HTML2Text()
            return h.handle(html)
        except ImportError:
            logger.warning("html2text not installed, returning raw HTML")
            return html


# 测试代码
if __name__ == "__main__":
    # 测试示例
    raw = {
        "title": "测试文章",
        "markdown": "这是内容 ![图片](https://example.com/image.jpg)",
        "html": '<img src="https://example.com/image.jpg">',
        "source_url": "https://example.com"
    }
    
    parsed = Parser.parse(raw)
    print(f"Title: {parsed['title']}")
    print(f"Content length: {len(parsed['content'])}")
    print(f"Images: {parsed['images']}")
    print(f"Metadata: {parsed['metadata']}")
