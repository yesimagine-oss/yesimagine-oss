#!/usr/bin/env python3
"""
Serper.dev API 搜索工具
支持 10 种搜索类型：Web、图片、新闻、地图、地点、视频、购物、学术、专利、自动补全
"""

import argparse
import json
import os
import sys
import requests
from typing import Dict, Any, Optional

# API 配置
API_KEY = os.getenv("SERPER_API_KEY", "01529847d4aa3cf47b86ca87d28519110db06390")
BASE_URL = "https://google.serper.dev"

# 端点映射
ENDPOINTS = {
    "search": "/search",
    "images": "/images",
    "news": "/news",
    "maps": "/maps",
    "places": "/places",
    "videos": "/videos",
    "shopping": "/shopping",
    "scholar": "/scholar",
    "patents": "/patents",
    "autocomplete": "/autocomplete",
}

# 时间范围映射
TIME_RANGES = {
    "hour": "qdr:h",
    "day": "qdr:d",
    "week": "qdr:w",
    "month": "qdr:m",
    "year": "qdr:y",
}


def serper_request(
    endpoint: str,
    query: str,
    num: int = 10,
    location: Optional[str] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    time_range: Optional[str] = None,
) -> Dict[str, Any]:
    """发送 Serper API 请求"""
    url = f"{BASE_URL}{endpoint}"
    
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json",
    }
    
    payload: Dict[str, Any] = {"q": query}
    
    # 添加可选参数
    if num:
        payload["num"] = num
    if location:
        payload["location"] = location
    if country:
        payload["gl"] = country
    if language:
        payload["hl"] = language
    if time_range and time_range in TIME_RANGES:
        payload["tbs"] = TIME_RANGES[time_range]
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}", file=sys.stderr)
        sys.exit(1)


def format_results(results: Dict[str, Any], endpoint: str, format_type: str) -> str:
    """格式化搜索结果"""
    if format_type == "json":
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    # 格式化文本输出
    output = []
    
    if endpoint == "search":
        output.append(f"🔍 Web 搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("organic", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   {item.get('link', 'N/A')}")
            snippet = item.get('snippet', '')[:150]
            if snippet:
                output.append(f"   {snippet}...")
            output.append("")
    
    elif endpoint == "images":
        output.append(f"📷 图片搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("images", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   来源：{item.get('source', 'N/A')}")
            output.append(f"   {item.get('link', 'N/A')}")
            output.append("")
    
    elif endpoint == "news":
        output.append(f"🗞 新闻搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("news", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   来源：{item.get('source', 'N/A')} | {item.get('date', 'N/A')}")
            output.append(f"   {item.get('link', 'N/A')}")
            output.append("")
    
    elif endpoint == "maps":
        output.append(f"🗺 地图搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("places", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   地址：{item.get('address', 'N/A')}")
            output.append(f"   评分：{item.get('rating', 'N/A')} ({item.get('ratingCount', 0)} 条评价)")
            output.append(f"   类型：{item.get('type', 'N/A')}")
            output.append("")
    
    elif endpoint == "places":
        output.append(f"📍 地点搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("places", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   地址：{item.get('address', 'N/A')}")
            output.append(f"   评分：{item.get('rating', 'N/A')} ({item.get('ratingCount', 0)} 条评价)")
            output.append("")
    
    elif endpoint == "videos":
        output.append(f"🎥 视频搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("videos", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   频道：{item.get('channel', 'N/A')} | 时长：{item.get('duration', 'N/A')}")
            output.append(f"   {item.get('link', 'N/A')}")
            output.append("")
    
    elif endpoint == "shopping":
        output.append(f"🛍 购物搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("shopping", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   价格：{item.get('price', 'N/A')} | 商家：{item.get('source', 'N/A')}")
            output.append(f"   评分：{item.get('rating', 'N/A')} ({item.get('ratingCount', 0)} 条评价)")
            output.append("")
    
    elif endpoint == "scholar":
        output.append(f"📚 学术搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("organic", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   作者：{item.get('publicationInfo', {}).get('summary', 'N/A')}")
            output.append(f"   引用：{item.get('citedBy', 0)} 次")
            output.append(f"   {item.get('link', 'N/A')}")
            output.append("")
    
    elif endpoint == "patents":
        output.append(f"🔬 专利搜索结果：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("organic", [])[:10], 1):
            output.append(f"{i}. {item.get('title', 'N/A')}")
            output.append(f"   专利号：{item.get('publicationNumber', 'N/A')}")
            output.append(f"   发明人：{item.get('inventor', 'N/A')}")
            output.append(f"   授权日期：{item.get('grantDate', 'N/A')}")
            output.append("")
    
    elif endpoint == "autocomplete":
        output.append(f"🤔 搜索建议：{results.get('searchParameters', {}).get('q', '')}\n")
        for i, item in enumerate(results.get("suggestions", [])[:10], 1):
            output.append(f"{i}. {item.get('value', 'N/A')}")
        output.append("")
    
    # 添加 Credits 信息
    if "credits" in results:
        output.append(f"💳 消耗 Credits: {results['credits']}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Serper API 搜索工具")
    parser.add_argument("command", choices=ENDPOINTS.keys(), help="搜索类型")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("-n", "--num", type=int, default=10, help="结果数量 (默认：10)")
    parser.add_argument("--location", type=str, help="地理位置")
    parser.add_argument("--country", type=str, help="国家代码 (如：us, cn, gb)")
    parser.add_argument("--language", type=str, help="语言代码 (如：en, zh-CN)")
    parser.add_argument("--time-range", type=str, choices=TIME_RANGES.keys(), help="时间范围")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 发送请求
    endpoint = ENDPOINTS[args.command]
    results = serper_request(
        endpoint=endpoint,
        query=args.query,
        num=args.num,
        location=args.location,
        country=args.country,
        language=args.language,
        time_range=args.time_range,
    )
    
    # 输出结果
    output = format_results(results, args.command, args.format)
    print(output)


if __name__ == "__main__":
    main()
