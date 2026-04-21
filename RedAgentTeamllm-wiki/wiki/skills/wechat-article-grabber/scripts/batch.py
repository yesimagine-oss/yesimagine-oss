#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
批量抓取微信公众号文章
"""

import sys
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from grab import grab_article, save_to_file

def process_url(url: str, output_dir: str, args):
    """处理单个 URL"""
    print(f"\n📱 处理：{url}")
    
    # 生成输出文件名
    output_file = Path(output_dir) / f"{url.split('/')[-1]}.md"
    
    # 抓取
    result = grab_article(url, method=args.method, cookie_file=args.cookie)
    
    if result['success']:
        save_to_file(result['content'], str(output_file))
        return {'url': url, 'success': True, 'file': str(output_file)}
    else:
        return {'url': url, 'success': False, 'error': result.get('error')}

def main():
    parser = argparse.ArgumentParser(description='批量抓取微信公众号文章')
    parser.add_argument('-i', '--input', required=True, help='URL 列表文件')
    parser.add_argument('-o', '--output', default='./output', help='输出目录')
    parser.add_argument('-m', '--method', default='auto', help='抓取方法')
    parser.add_argument('--cookie', help='Cookie 文件路径')
    parser.add_argument('-w', '--workers', type=int, default=5, help='并发数')
    parser.add_argument('--dedup', action='store_true', help='去重')
    
    args = parser.parse_args()
    
    # 读取 URL 列表
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ 文件不存在：{input_file}")
        return 1
    
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 读取到 {len(urls)} 个 URL")
    
    # 去重
    if args.dedup:
        urls = list(dict.fromkeys(urls))
        print(f"✅ 去重后：{len(urls)} 个 URL")
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 输出目录：{output_dir}")
    print(f"🔧 并发数：{args.workers}")
    print("-" * 60)
    
    # 并发处理
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_url, url, str(output_dir), args): url
            for url in urls
        }
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"✅ 成功：{result['url']} → {result['file']}")
            else:
                print(f"❌ 失败：{result['url']} - {result.get('error', '未知错误')}")
    
    # 统计
    print("\n" + "=" * 60)
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    print(f"📊 统计：成功 {success_count}/{len(results)}, 失败 {fail_count}")
    print(f"✅ 成功率：{success_count/len(results)*100:.1f}%")
    print("=" * 60)
    
    return 0 if success_count > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
