#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章专业收集器 - 主逻辑

使用技能开发组件库快速开发
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# 添加组件库路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'components'))

from fetcher import Fetcher
from parser import Parser
from classifier import Classifier
from uploader import Uploader
from indexer import Indexer
from notifier import Notifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def collect_article(url: str, config: dict, simple: bool = False, method: str = "auto"):
    """
    收集单篇文章
    
    Args:
        url: 文章 URL
        config: 配置字典
        simple: 是否简化模式（不上传飞书）
        method: 抓取方法
    
    Returns:
        处理结果字典
    """
    logger.info(f"Starting collection: {url}")
    
    try:
        # ========== Step 1: 抓取 ==========
        logger.info(f"Step 1: Fetching content (method={method})...")
        raw = Fetcher.fetch(url, method=method, timeout=60)
        logger.info(f"✅ Fetch success, length: {len(raw['markdown'])}")
        
        # ========== Step 2: 解析 ==========
        logger.info("Step 2: Parsing content...")
        parsed = Parser.parse(raw)
        logger.info(f"✅ Parse success, images: {len(parsed['images'])}")
        
        # ========== Step 3: 分类 ==========
        logger.info("Step 3: Classifying...")
        category = Classifier.classify(parsed["content"], parsed["title"])
        logger.info(f"✅ Category: {category}")
        
        # ========== Step 4: 处理图片 ==========
        image_stats = {"total": 0, "success": 0, "failed": 0}
        if parsed["images"] and not simple:
            logger.info("Step 4: Processing images...")
            image_keys = Uploader.upload_images(parsed["images"], target="feishu")
            parsed["content"] = Parser.replace_images(parsed["content"], image_keys)
            
            # 追加 HTML-only 图片
            if len(image_keys) < len(parsed["images"]):
                extra_images = [(f"image_{i}", key) for i, key in enumerate(image_keys.values())]
                parsed["content"] = Parser.append_images(parsed["content"], extra_images)
            
            image_stats = {
                "total": len(parsed["images"]),
                "success": len(image_keys),
                "failed": len(parsed["images"]) - len(image_keys)
            }
            logger.info(f"✅ Images: {image_stats['success']}/{image_stats['total']}")
        
        # ========== Step 5: 创建文档 ==========
        doc_url = ""
        if not simple:
            logger.info("Step 5: Creating Feishu doc...")
            today = datetime.now().strftime("%Y-%m-%d")
            doc_title = f"{category} {parsed['title']} | {today}"
            
            doc_content = f"""# {doc_title}

> 📌 **元信息**
> - 来源：{parsed['metadata']['source_url']}
> - 收录时间：{parsed['metadata']['fetch_time']}
> - 内容分类：{category}
> - 字数：{parsed['metadata']['word_count']}
> - 图片处理：成功 {image_stats['success']}/{image_stats['total']}

---

## 📋 核心要点

{Parser.extract_key_points(parsed['content'], 5)}

---

## 📝 正文内容

{parsed['content']}

---

## 🔗 相关链接

- 原文链接：{url}

---

📅 **收录时间**：{today}  
🏷️ **分类**：{category}  
🔖 **关键词**：待提取
"""
            
            doc_url = Uploader.create_feishu_doc(doc_title, doc_content, config.get("folder_id", ""))
            logger.info(f"✅ Doc created: {doc_url}")
        
        # ========== Step 6: 更新索引 ==========
        record_id = ""
        if not simple and config.get("app_token") and config.get("table_id"):
            logger.info("Step 6: Updating index...")
            record_id = Indexer.update_bitable(
                app_token=config.get("app_token", ""),
                table_id=config.get("table_id", ""),
                fields={
                    "关键词": "微信，公众号，文章",
                    "内容分类": category,
                    "文档标题": parsed["title"],
                    "来源": "微信公众号",
                    "核心要点": "自动收录",
                    "飞书文档链接": {"link": doc_url, "text": "飞书文档"},
                    "原链接": {"link": url, "text": "原文链接"},
                    "图片数量": image_stats["total"],
                    "图片处理状态": f"{image_stats['success']}/{image_stats['total']} 成功",
                    "图片失败数": image_stats["failed"]
                }
            )
            logger.info(f"✅ Index updated: {record_id}")
        
        # ========== Step 7: 发送通知 ==========
        logger.info("Step 7: Sending notification...")
        if not simple:
            Notifier.send_success(category, parsed["title"], doc_url)
        logger.info("✅ Notification sent")
        
        # ========== 完成 ==========
        logger.info("🎉 Collection completed!")
        
        return {
            "status": "success",
            "title": parsed["title"],
            "category": category,
            "doc_url": doc_url,
            "record_id": record_id,
            "image_stats": image_stats,
            "content_length": len(parsed["content"])
        }
    
    except Exception as e:
        logger.error(f"❌ Collection failed: {e}")
        
        # 发送失败通知
        Notifier.send_failure(str(e))
        
        return {
            "status": "error",
            "error": str(e),
            "url": url
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="微信公众号文章收集器")
    parser.add_argument("url", help="文章 URL")
    parser.add_argument("--simple", action="store_true", help="简化模式（不上传飞书）")
    parser.add_argument("--category", help="手动指定分类")
    parser.add_argument("--method", choices=["auto", "chrome", "playwright"], default="auto", help="抓取方法")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 配置
    config = {
        "app_token": os.environ.get("FEISHU_APP_TOKEN", ""),
        "table_id": os.environ.get("FEISHU_TABLE_ID", ""),
        "space_id": os.environ.get("FEISHU_SPACE_ID", ""),
        "folder_id": ""
    }
    
    # 执行收集
    result = collect_article(args.url, config, args.simple, args.method)
    
    # 输出结果
    if result["status"] == "success":
        print(f"\n✅ 收录完成")
        print(f"\n📄 {result['category']} {result['title']}")
        if result['doc_url']:
            print(f"\n🔗 查看飞书文档 → {result['doc_url']}")
    else:
        print(f"\n❌ 收录失败")
        print(f"⚠️ 错误：{result['error']}")


if __name__ == "__main__":
    main()
