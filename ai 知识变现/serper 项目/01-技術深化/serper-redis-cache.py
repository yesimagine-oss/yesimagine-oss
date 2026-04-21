#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serper.dev Redis 緩存層

功能:
- Redis 緩存支持（替代文件緩存）
- TTL 自動過期
- 緩存統計
- 緩存清理

使用:
    python3 serper-redis-cache.py --stats
    python3 serper-redis-cache.py --clear
    python3 serper-redis-cache.py --test

作者: RedOpenClaw
創建: 2026-03-23
"""

import redis
import json
import time
from datetime import datetime
from typing import Optional, Dict
import hashlib
import os

# 配置
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
CACHE_TTL = 24 * 60 * 60  # 24 小時
CACHE_PREFIX = "serper:cache:"


class SerperRedisCache:
    """Serper Redis 緩存管理器"""
    
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, 
                 db: int = REDIS_DB, password: str = REDIS_PASSWORD):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None
        self.connected = False
        
    def connect(self) -> bool:
        """連接 Redis"""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # 測試連接
            self.client.ping()
            self.connected = True
            print(f"✅ Redis 連接成功：{self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Redis 連接失敗：{e}")
            print(f"💡 提示：Redis 可能未安裝或未啟動")
            print(f"   安裝：sudo apt install redis-server")
            print(f"   啟動：sudo systemctl start redis")
            self.connected = False
            return False
    
    def _get_key(self, query: str, params: Dict = None) -> str:
        """生成緩存鍵"""
        key_str = f"{query}:{json.dumps(params or {}, sort_keys=True)}"
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"{CACHE_PREFIX}{key_hash}"
    
    def get(self, query: str, params: Dict = None) -> Optional[Dict]:
        """從緩存獲取結果"""
        if not self.connected:
            return None
        
        try:
            key = self._get_key(query, params)
            data = self.client.get(key)
            
            if data:
                result = json.loads(data)
                print(f"✅ 緩存命中：{query[:50]}...")
                return result
            else:
                print(f"❌ 緩存未命中：{query[:50]}...")
                return None
        except Exception as e:
            print(f"⚠️  緩存獲取失敗：{e}")
            return None
    
    def set(self, query: str, result: Dict, params: Dict = None, ttl: int = None) -> bool:
        """保存結果到緩存"""
        if not self.connected:
            return False
        
        try:
            key = self._get_key(query, params)
            ttl = ttl or CACHE_TTL
            
            data = {
                'result': result,
                'cached_at': datetime.now().isoformat(),
                'query': query,
                'params': params or {}
            }
            
            self.client.setex(key, ttl, json.dumps(data, ensure_ascii=False))
            print(f"💾 緩存已保存：{query[:50]}... (TTL: {ttl}s)")
            return True
        except Exception as e:
            print(f"⚠️  緩存保存失敗：{e}")
            return False
    
    def clear(self, pattern: str = None) -> int:
        """清理緩存"""
        if not self.connected:
            return 0
        
        try:
            pattern = pattern or f"{CACHE_PREFIX}*"
            keys = self.client.keys(pattern)
            
            if keys:
                count = self.client.delete(*keys)
                print(f"🗑️  已清理 {count} 個緩存項")
                return count
            else:
                print(f"ℹ️  沒有匹配的緩存項")
                return 0
        except Exception as e:
            print(f"⚠️  清理緩存失敗：{e}")
            return 0
    
    def stats(self) -> Dict:
        """獲取緩存統計"""
        if not self.connected:
            return {'error': '未連接 Redis'}
        
        try:
            # 獲取所有 Serper 緩存鍵
            keys = self.client.keys(f"{CACHE_PREFIX}*")
            total_keys = len(keys)
            
            # 獲取內存使用
            info = self.client.info('memory')
            memory_used = info.get('used_memory_human', 'N/A')
            
            # 計算過期時間分佈
            ttl_distribution = {'<1h': 0, '1-6h': 0, '6-12h': 0, '12-24h': 0, '>24h': 0}
            
            for key in keys[:100]:  # 只檢查前 100 個
                ttl = self.client.ttl(key)
                if ttl < 3600:
                    ttl_distribution['<1h'] += 1
                elif ttl < 21600:
                    ttl_distribution['1-6h'] += 1
                elif ttl < 43200:
                    ttl_distribution['6-12h'] += 1
                elif ttl < 86400:
                    ttl_distribution['12-24h'] += 1
                else:
                    ttl_distribution['>24h'] += 1
            
            stats = {
                'total_keys': total_keys,
                'memory_used': memory_used,
                'ttl_distribution': ttl_distribution,
                'server_info': {
                    'host': self.host,
                    'port': self.port,
                    'db': self.db
                }
            }
            
            return stats
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """關閉連接"""
        if self.client:
            self.client.close()
            print("👋 Redis 連接已關閉")


def test_cache():
    """測試緩存功能"""
    print("🧪 測試 Serper Redis 緩存\n")
    
    cache = SerperRedisCache()
    
    if not cache.connect():
        print("\n❌ 測試失敗：無法連接 Redis")
        return False
    
    # 測試保存
    test_data = {
        'organic': [
            {'title': 'Test Result 1', 'link': 'https://example.com/1'},
            {'title': 'Test Result 2', 'link': 'https://example.com/2'}
        ],
        'searchParameters': {'q': 'test query'}
    }
    
    print("\n1️⃣ 測試保存緩存...")
    cache.set("test query", test_data, ttl=60)
    
    # 測試獲取
    print("\n2️⃣ 測試獲取緩存...")
    result = cache.get("test query")
    
    if result:
        print("✅ 獲取成功")
        print(f"   結果數量：{len(result.get('organic', []))}")
    else:
        print("❌ 獲取失敗")
    
    # 測試統計
    print("\n3️⃣ 測試統計...")
    stats = cache.stats()
    print(f"   總緩存數：{stats.get('total_keys', 0)}")
    print(f"   內存使用：{stats.get('memory_used', 'N/A')}")
    
    # 測試清理
    print("\n4️⃣ 測試清理...")
    cache.clear(f"{CACHE_PREFIX}md5:*")
    
    cache.close()
    print("\n✅ 測試完成")
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Serper Redis 緩存管理')
    parser.add_argument('--stats', action='store_true', help='顯示統計')
    parser.add_argument('--clear', action='store_true', help='清理所有緩存')
    parser.add_argument('--test', action='store_true', help='運行測試')
    parser.add_argument('--host', default=REDIS_HOST, help='Redis 主機')
    parser.add_argument('--port', type=int, default=REDIS_PORT, help='Redis 端口')
    
    args = parser.parse_args()
    
    cache = SerperRedisCache(host=args.host, port=args.port)
    
    if args.test:
        test_cache()
    elif args.stats:
        if cache.connect():
            stats = cache.stats()
            print("\n📊 Serper 緩存統計")
            print(f"   總緩存數：{stats.get('total_keys', 0)}")
            print(f"   內存使用：{stats.get('memory_used', 'N/A')}")
            print(f"\n   TTL 分佈:")
            for ttl_range, count in stats.get('ttl_distribution', {}).items():
                print(f"      {ttl_range}: {count}")
            cache.close()
    elif args.clear:
        if cache.connect():
            confirm = input("⚠️  確認清理所有 Serper 緩存？(y/N): ")
            if confirm.lower() == 'y':
                cache.clear()
            cache.close()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
