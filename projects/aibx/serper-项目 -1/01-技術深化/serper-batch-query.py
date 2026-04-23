#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serper.dev 並發查詢工具

功能:
- 批量並發查詢（支持 100+ 並發）
- 結果緩存（Redis/TTL）
- 錯誤重試（指數退避）
- 進度追蹤

使用:
    python3 serper-batch-query.py "keyword1" "keyword2" ... -n 100
    python3 serper-batch-query.py --file keywords.txt -c 50

作者: RedOpenClaw
創建: 2026-03-23
"""

import asyncio
import aiohttp
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from pathlib import Path

# 配置
API_KEY = os.getenv('SERPER_API_KEY', '01529847d4aa3cf47b86ca87d28519110db06390')
API_URL = "https://google.serper.dev/search"
DEFAULT_CONCURRENCY = 10  # 默認並發數
MAX_CONCURRENCY = 100  # 最大並發數
CACHE_TTL = 24 * 60 * 60  # 緩存 TTL（秒）= 24 小時
MAX_RETRIES = 3  # 最大重試次數

# 緩存目錄
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / "cache" / "serper"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class SerperBatchQuery:
    """Serper 批量查詢工具"""
    
    def __init__(self, concurrency: int = DEFAULT_CONCURRENCY, use_cache: bool = True):
        self.concurrency = min(concurrency, MAX_CONCURRENCY)
        self.use_cache = use_cache
        self.session = None
        self.results = []
        self.errors = []
        self.cache_hits = 0
        self.cache_misses = 0
        
    def _get_cache_key(self, query: str, params: Dict = None) -> str:
        """生成緩存鍵"""
        key_str = f"{query}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """獲取緩存文件路徑"""
        return CACHE_DIR / f"{cache_key}.json"
    
    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """從緩存加載結果"""
        if not self.use_cache:
            return None
        
        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 檢查 TTL
            cached_time = datetime.fromisoformat(data['_cached_at'])
            if datetime.now() - cached_time > timedelta(seconds=CACHE_TTL):
                cache_path.unlink()  # 過期刪除
                return None
            
            self.cache_hits += 1
            return data
        except Exception as e:
            print(f"⚠️  緩存加載失敗：{e}")
            return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """保存結果到緩存"""
        if not self.use_cache:
            return
        
        try:
            cache_path = self._get_cache_path(cache_key)
            data['_cached_at'] = datetime.now().isoformat()
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.cache_misses += 1
        except Exception as e:
            print(f"⚠️  緩存保存失敗：{e}")
    
    async def _query_single(self, query: str, params: Dict = None, retry_count: int = 0) -> Dict:
        """單次查詢（異步）"""
        cache_key = self._get_cache_key(query, params)
        
        # 嘗試從緩存加載
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return {
                'query': query,
                'result': cached_result,
                'from_cache': True,
                'success': True
            }
        
        # API 查詢
        try:
            payload = {"q": query, **(params or {})}
            
            async with self.session.post(
                API_URL,
                headers={
                    'X-API-KEY': API_KEY,
                    'Content-Type': 'application/json'
                },
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # 保存到緩存
                    self._save_to_cache(cache_key, result)
                    
                    return {
                        'query': query,
                        'result': result,
                        'from_cache': False,
                        'success': True
                    }
                elif response.status == 429:  # 速率限制
                    if retry_count < MAX_RETRIES:
                        wait_time = (2 ** retry_count) * 1.0  # 指數退避
                        print(f"⚠️  速率限制，等待 {wait_time:.1f}秒後重試...")
                        await asyncio.sleep(wait_time)
                        return await self._query_single(query, params, retry_count + 1)
                    else:
                        return {
                            'query': query,
                            'error': '速率限制（429）',
                            'success': False
                        }
                else:
                    error_text = await response.text()
                    return {
                        'query': query,
                        'error': f'HTTP {response.status}: {error_text}',
                        'success': False
                    }
                    
        except asyncio.TimeoutError:
            if retry_count < MAX_RETRIES:
                wait_time = (2 ** retry_count) * 1.0
                print(f"⏱️  超時，等待 {wait_time:.1f}秒後重試...")
                await asyncio.sleep(wait_time)
                return await self._query_single(query, params, retry_count + 1)
            else:
                return {
                    'query': query,
                    'error': '超時',
                    'success': False
                }
        except Exception as e:
            return {
                'query': query,
                'error': str(e),
                'success': False
            }
    
    async def query_batch(self, queries: List[str], params: Dict = None, 
                         show_progress: bool = True) -> List[Dict]:
        """批量查詢"""
        self.results = []
        self.errors = []
        self.cache_hits = 0
        self.cache_misses = 0
        
        start_time = time.time()
        
        # 創建信號量控制並發
        semaphore = asyncio.Semaphore(self.concurrency)
        
        async def limited_query(query: str):
            async with semaphore:
                return await self._query_single(query, params)
        
        # 創建任務
        tasks = [limited_query(query) for query in queries]
        
        # 執行並顯示進度
        if show_progress:
            print(f"🚀 開始批量查詢：{len(queries)} 個關鍵詞，並發數：{self.concurrency}")
            print(f"📊 預計時間：{len(queries) / self.concurrency * 2:.1f}秒\n")
        
        # 執行所有任務
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 處理結果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = {
                    'query': queries[i],
                    'error': str(result),
                    'success': False
                }
                self.errors.append(error_result)
                self.results.append(error_result)
            else:
                self.results.append(result)
                if not result.get('success'):
                    self.errors.append(result)
        
        # 統計
        elapsed = time.time() - start_time
        success_count = len([r for r in self.results if r.get('success')])
        
        if show_progress:
            print(f"\n✅ 查詢完成！")
            print(f"📊 統計:")
            print(f"   - 總數：{len(queries)}")
            print(f"   - 成功：{success_count}")
            print(f"   - 失敗：{len(self.errors)}")
            print(f"   - 緩存命中：{self.cache_hits}")
            print(f"   - 緩存未命中：{self.cache_misses}")
            print(f"   - 用時：{elapsed:.2f}秒")
            print(f"   - 平均速度：{elapsed / len(queries) * 1000:.1f}ms/查詢")
        
        return self.results
    
    def save_results(self, output_path: str, format: str = 'json'):
        """保存結果"""
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"💾 結果已保存到：{output_path}")
        elif format == 'csv':
            import csv
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Query', 'Success', 'From Cache', 'Error', 'Results Count'])
                for r in self.results:
                    result_data = r.get('result', {})
                    results_count = len(result_data.get('organic', []))
                    writer.writerow([
                        r['query'],
                        r.get('success', False),
                        r.get('from_cache', False),
                        r.get('error', ''),
                        results_count
                    ])
            print(f"💾 CSV 結果已保存到：{output_path}")


async def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Serper 批量查詢工具')
    parser.add_argument('queries', nargs='*', help='查詢關鍵詞')
    parser.add_argument('-f', '--file', help='從文件讀取關鍵詞（每行一個）')
    parser.add_argument('-n', '--count', type=int, default=DEFAULT_CONCURRENCY, 
                       help=f'並發數（默認：{DEFAULT_CONCURRENCY}）')
    parser.add_argument('-o', '--output', help='輸出文件路徑')
    parser.add_argument('--format', choices=['json', 'csv'], default='json',
                       help='輸出格式（默認：json）')
    parser.add_argument('--no-cache', action='store_true', help='禁用緩存')
    parser.add_argument('--location', help='地理位置（如：Beijing,China）')
    parser.add_argument('--gl', help='國家代碼（如：cn,us）')
    parser.add_argument('--hl', help='語言代碼（如：zh,en）')
    
    args = parser.parse_args()
    
    # 收集查詢
    queries = list(args.queries)
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            file_queries = [line.strip() for line in f if line.strip()]
            queries.extend(file_queries)
    
    if not queries:
        print("❌ 請提供查詢關鍵詞或使用 -f 指定文件")
        parser.print_help()
        return
    
    # 構建參數
    params = {}
    if args.location:
        params['location'] = args.location
    if args.gl:
        params['gl'] = args.gl
    if args.hl:
        params['hl'] = args.hl
    
    # 創建查詢工具
    tool = SerperBatchQuery(concurrency=args.count, use_cache=not args.no_cache)
    
    # 創建 HTTP 會話
    async with aiohttp.ClientSession() as session:
        tool.session = session
        
        # 執行批量查詢
        results = await tool.query_batch(queries, params)
    
    # 保存結果
    if args.output:
        tool.save_results(args.output, format=args.format)
    else:
        # 顯示前 5 個結果
        print(f"\n📄 前 5 個結果預覽:")
        for r in results[:5]:
            if r.get('success'):
                result_data = r.get('result', {})
                organic = result_data.get('organic', [])
                print(f"\n🔍 {r['query']}:")
                for i, item in enumerate(organic[:3], 1):
                    print(f"   {i}. {item.get('title', 'N/A')}")
                    print(f"      {item.get('link', 'N/A')}")
            else:
                print(f"\n❌ {r['query']}: {r.get('error', '未知錯誤')}")


if __name__ == '__main__':
    asyncio.run(main())
