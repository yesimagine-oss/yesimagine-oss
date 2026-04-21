#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能开发组件库 - 完整使用示例

展示如何使用组件库快速开发新技能
"""

from components.fetcher import Fetcher
from components.parser import Parser
from components.classifier import Classifier
from components.uploader import Uploader
from components.indexer import Indexer
from components.notifier import Notifier


def full_workflow(url: str, config: dict):
    """
    完整工作流示例
    
    Args:
        url: 文章 URL
        config: 配置字典
    """
    print(f"🚀 开始处理：{url}")
    
    # ========== Step 1: 抓取 ==========
    print("📥 Step 1: 抓取内容...")
    raw = Fetcher.fetch(url, method="auto", timeout=30)
    print(f"✅ 抓取成功，内容长度：{len(raw['markdown'])}")
    
    # ========== Step 2: 解析 ==========
    print("🔍 Step 2: 解析内容...")
    parsed = Parser.parse(raw)
    print(f"✅ 解析成功，图片数：{len(parsed['images'])}")
    
    # ========== Step 3: 分类 ==========
    print("🏷️  Step 3: 智能分类...")
    category = Classifier.classify(parsed["content"], parsed["title"])
    print(f"✅ 分类结果：{category}")
    
    # ========== Step 4: 处理图片 ==========
    if parsed["images"]:
        print("🖼️  Step 4: 处理图片...")
        image_keys = Uploader.upload_images(parsed["images"], target="feishu")
        parsed["content"] = Parser.replace_images(parsed["content"], image_keys)
        print(f"✅ 图片处理完成：{len(image_keys)}/{len(parsed['images'])}")
    
    # ========== Step 5: 创建文档 ==========
    print("📄 Step 5: 创建飞书文档...")
    doc_title = f"{category} {parsed['title']} | 2026-03-23"
    doc_content = f"""# {doc_title}

> 📌 **元信息**
> - 来源：{parsed['metadata']['source_url']}
> - 收录时间：{parsed['metadata']['fetch_time']}
> - 内容分类：{category}
> - 字数：{parsed['metadata']['word_count']}

---

## 📋 核心要点

{Parser.extract_key_points(parsed['content'], 5)}

---

## 📝 正文内容

{parsed['content']}

---

📅 **收录时间**：2026-03-23  
🏷️ **分类**：{category}
"""
    
    doc_url = Uploader.create_feishu_doc(doc_title, doc_content, config.get("folder_id", ""))
    print(f"✅ 文档创建成功：{doc_url}")
    
    # ========== Step 6: 更新索引 ==========
    print("📊 Step 6: 更新索引...")
    record_id = Indexer.update_bitable(
        app_token=config.get("app_token", ""),
        table_id=config.get("table_id", ""),
        fields={
            "关键词": "测试，示例",
            "内容分类": category,
            "文档标题": parsed["title"],
            "来源": "测试来源",
            "核心要点": "测试要点",
            "飞书文档链接": {"link": doc_url, "text": "飞书文档"},
            "原链接": {"link": url, "text": "原文链接"},
            "图片数量": len(parsed["images"])
        }
    )
    print(f"✅ 索引更新成功：{record_id}")
    
    # ========== Step 7: 发送通知 ==========
    print("📬 Step 7: 发送通知...")
    Notifier.send_success(category, parsed["title"], doc_url)
    print("✅ 通知发送成功")
    
    # ========== 完成 ==========
    print("\n🎉 完成！")
    print(f"📄 文档标题：{doc_title}")
    print(f"🔗 文档链接：{doc_url}")
    print(f"🏷️ 分类：{category}")
    print(f"📊 记录 ID: {record_id}")
    
    return {
        "doc_title": doc_title,
        "doc_url": doc_url,
        "category": category,
        "record_id": record_id,
        "image_count": len(parsed["images"])
    }


# 简化版工作流（仅核心功能）
def simple_workflow(url: str):
    """
    简化版工作流
    
    Args:
        url: 文章 URL
    
    Returns:
        处理结果
    """
    print(f"🚀 简化版处理：{url}")
    
    # 1. 抓取
    raw = Fetcher.fetch(url, method="jina", timeout=10)
    
    # 2. 解析
    parsed = Parser.parse(raw)
    
    # 3. 分类
    category = Classifier.classify(parsed["content"], parsed["title"])
    
    # 4. 返回结果
    return {
        "title": parsed["title"],
        "category": category,
        "content_length": len(parsed["content"]),
        "image_count": len(parsed["images"])
    }


# 主函数
if __name__ == "__main__":
    import sys
    
    # 配置示例
    config = {
        "app_token": "your_app_token",
        "table_id": "your_table_id",
        "folder_id": "your_folder_id"
    }
    
    # 获取 URL
    if len(sys.argv) < 2:
        print("Usage: python example.py <url> [full|simple]")
        sys.exit(1)
    
    url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "simple"
    
    # 执行工作流
    if mode == "full":
        result = full_workflow(url, config)
    else:
        result = simple_workflow(url)
    
    # 输出结果
    print("\n" + "="*50)
    print("处理结果:")
    for key, value in result.items():
        print(f"{key}: {value}")
