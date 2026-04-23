#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uploader 组件 - 文件上传器

支持飞书文档创建、图片上传
"""

import os
import tempfile
from typing import Dict, List, Optional
import requests
import logging

logger = logging.getLogger(__name__)


class Uploader:
    """文件上传器"""
    
    @staticmethod
    def create_feishu_doc(title: str, content: str, folder_id: str = "") -> str:
        """
        创建飞书文档
        
        Args:
            title: 文档标题
            content: Markdown 内容
            folder_id: 文件夹 ID（可选）
        
        Returns:
            飞书文档 URL
        
        Raises:
            Exception: 创建失败
        """
        logger.info(f"Creating Feishu doc: {title}")
        
        # 这里需要飞书 Doc API 集成
        # 示例代码：
        # token = get_feishu_token()
        # response = create_doc(token, title, content, folder_id)
        # return response["url"]
        
        # 临时返回占位符
        logger.warning("Feishu API not configured, returning placeholder URL")
        return "https://example.feishu.cn/docx/placeholder"
    
    @staticmethod
    def upload_images(images: List[str], target: str = "feishu") -> Dict[str, str]:
        """
        批量上传图片
        
        Args:
            images: 图片 URL 列表
            target: 上传目标 (feishu/local)
        
        Returns:
            {原 URL: 新 URL/image_key}
        """
        logger.info(f"Uploading {len(images)} images to {target}")
        
        result = {}
        failed = []
        
        for i, img_url in enumerate(images):
            try:
                # 下载图片
                tmp_path = Uploader._download_image(img_url)
                
                # 上传到目标
                if target == "feishu":
                    image_key = Uploader._upload_to_feishu(tmp_path)
                    result[img_url] = image_key
                else:
                    result[img_url] = tmp_path
                
                # 清理临时文件
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                
            except Exception as e:
                logger.error(f"Failed to upload image {img_url}: {e}")
                failed.append({"url": img_url, "reason": str(e)})
        
        logger.info(f"Uploaded {len(result)}/{len(images)} images, {len(failed)} failed")
        return result
    
    @staticmethod
    def _download_image(url: str, timeout: int = 20, max_bytes: int = 10*1024*1024) -> str:
        """
        下载图片到本地临时文件
        
        Args:
            url: 图片 URL
            timeout: 超时时间（秒）
            max_bytes: 最大文件大小（字节）
        
        Returns:
            临时文件路径
        
        Raises:
            Exception: 下载失败
        """
        logger.debug(f"Downloading image: {url}")
        
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # 检查文件大小
        content_length = int(response.headers.get('content-length', 0))
        if content_length > max_bytes:
            raise Exception(f"Image too large: {content_length} bytes > {max_bytes} bytes")
        
        # 创建临时文件
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        
        # 下载内容
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if len(chunk) + downloaded > max_bytes:
                raise Exception(f"Image too large")
            tmp.write(chunk)
            downloaded += len(chunk)
        
        tmp.close()
        return tmp.name
    
    @staticmethod
    def _upload_to_feishu(file_path: str) -> str:
        """
        上传到飞书素材库
        
        Args:
            file_path: 文件路径
        
        Returns:
            image_key
        
        Raises:
            Exception: 上传失败
        """
        logger.debug(f"Uploading to Feishu: {file_path}")
        
        # 这里需要飞书图片上传 API 集成
        # 示例代码：
        # token = get_feishu_token()
        # with open(file_path, 'rb') as f:
        #     response = upload_image(token, f)
        # return response["image_key"]
        
        # 临时返回占位符
        logger.warning("Feishu API not configured, returning placeholder image_key")
        return "img_placeholder"
    
    @staticmethod
    def upload_file(file_path: str, target: str = "feishu", folder_id: str = "") -> str:
        """
        上传文件
        
        Args:
            file_path: 文件路径
            target: 上传目标 (feishu/local)
            folder_id: 文件夹 ID
        
        Returns:
            文件 URL 或 file_key
        """
        logger.info(f"Uploading file: {file_path} to {target}")
        
        if target == "feishu":
            # 这里需要飞书文件上传 API 集成
            return "file_placeholder"
        else:
            return file_path


# 测试代码
if __name__ == "__main__":
    # 测试示例
    test_images = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
    
    print("Testing Uploader:")
    result = Uploader.upload_images(test_images, target="local")
    print(f"Upload result: {result}")
