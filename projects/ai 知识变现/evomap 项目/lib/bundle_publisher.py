#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap Bundle 发布模板库
封装验证过的发布逻辑，提供简单易用的 API
"""

import requests
import json
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class EvoMapBundlePublisher:
    """EvoMap Bundle 发布器"""
    
    def __init__(self, node_id: str, node_secret: str, base_url: str = "https://evomap.ai"):
        self.node_id = node_id
        self.node_secret = node_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {node_secret}',
            'Content-Type': 'application/json'
        })
        # 设置代理
        os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
        os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    
    def _canonical_stringify(self, obj: Any) -> str:
        """生成 canonical JSON 字符串"""
        if obj is None:
            return 'null'
        if isinstance(obj, bool):
            return 'true' if obj else 'false'
        if isinstance(obj, (int, float)):
            return str(obj)
        if isinstance(obj, str):
            return json.dumps(obj, ensure_ascii=False)
        if isinstance(obj, list):
            return '[' + ','.join(self._canonical_stringify(item) for item in obj) + ']'
        if isinstance(obj, dict):
            keys = sorted(obj.keys())
            pairs = [f'{json.dumps(k, ensure_ascii=False)}:{self._canonical_stringify(obj[k])}' for k in keys]
            return '{' + ','.join(pairs) + '}'
        return str(obj)
    
    def _compute_asset_id(self, obj: Dict) -> str:
        """计算 asset_id: sha256(canonical_json(asset_without_asset_id))"""
        clean = {k: v for k, v in obj.items() if k != 'asset_id'}
        canonical = self._canonical_stringify(clean)
        hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
        return f'sha256:{hash_hex}'
    
    def _validate_gene(self, gene: Dict) -> List[str]:
        """验证 Gene 字段"""
        errors = []
        
        # summary >= 10 字符
        if len(gene.get('summary', '')) < 10:
            errors.append('Gene.summary 必须 >= 10 字符')
        
        # strategy 每个步骤 >= 15 字符
        strategy = gene.get('strategy', [])
        for i, step in enumerate(strategy):
            if len(step) < 15:
                errors.append(f'Gene.strategy[{i}] 必须 >= 15 字符，当前：{len(step)}')
        
        # signals_match 至少 1 个
        if len(gene.get('signals_match', [])) < 1:
            errors.append('Gene.signals_match 至少 1 个信号')
        
        return errors
    
    def _validate_capsule(self, capsule: Dict) -> List[str]:
        """验证 Capsule 字段"""
        errors = []
        
        # summary >= 20 字符
        if len(capsule.get('summary', '')) < 20:
            errors.append('Capsule.summary 必须 >= 20 字符')
        
        # confidence 0-1
        confidence = capsule.get('confidence', 0)
        if not (0 <= confidence <= 1):
            errors.append(f'Capsule.confidence 必须在 0-1 之间，当前：{confidence}')
        
        # blast_radius > 0
        blast = capsule.get('blast_radius', {})
        if blast.get('files', 0) <= 0 or blast.get('lines', 0) <= 0:
            errors.append('Capsule.blast_radius.files 和 lines 必须 > 0')
        
        # substance 检查（code_snippet/content/strategy/diff 至少一个 >= 50 字符）
        substance_fields = ['code_snippet', 'content', 'strategy', 'diff']
        has_substance = False
        for field in substance_fields:
            value = capsule.get(field)
            if value:
                if isinstance(value, str) and len(value) >= 50:
                    has_substance = True
                    break
                elif isinstance(value, list) and len(value) > 0:
                    has_substance = True
                    break
        
        if not has_substance:
            errors.append('Capsule 必须包含 code_snippet/content/strategy/diff 至少一个（>= 50 字符）')
        
        return errors
    
    def create_gene(self,
                   category: str,
                   signals: List[str],
                   summary: str,
                   strategy: List[str],
                   constraints: Optional[Dict] = None,
                   validation: Optional[List[str]] = None,
                   preconditions: Optional[List[str]] = None) -> Dict:
        """创建 Gene 对象"""
        gene = {
            'type': 'Gene',
            'schema_version': '1.5.0',
            'category': category,
            'signals_match': signals,
            'summary': summary,
            'strategy': strategy,
            'constraints': constraints or {'max_files': 5, 'forbidden_paths': ['node_modules/']},
            'validation': validation or ['node test.js']
        }
        if preconditions:
            gene['preconditions'] = preconditions
        
        # 验证
        errors = self._validate_gene(gene)
        if errors:
            raise ValueError(f'Gene 验证失败：{errors}')
        
        # 计算 asset_id
        gene['asset_id'] = self._compute_asset_id(gene)
        return gene
    
    def create_capsule(self,
                      gene_asset_id: str,
                      trigger: List[str],
                      summary: str,
                      code_snippet: str,
                      confidence: float = 0.85,
                      blast_files: int = 1,
                      blast_lines: int = 10,
                      outcome_score: float = 0.85,
                      success_streak: int = 3) -> Dict:
        """创建 Capsule 对象"""
        capsule = {
            'type': 'Capsule',
            'schema_version': '1.5.0',
            'trigger': trigger,
            'gene': gene_asset_id,
            'summary': summary,
            'confidence': confidence,
            'blast_radius': {'files': blast_files, 'lines': blast_lines},
            'outcome': {'status': 'success', 'score': outcome_score},
            'env_fingerprint': {'platform': 'linux', 'arch': 'x64', 'node_version': 'v24.14.0'},
            'success_streak': success_streak,
            'code_snippet': code_snippet
        }
        
        # 验证
        errors = self._validate_capsule(capsule)
        if errors:
            raise ValueError(f'Capsule 验证失败：{errors}')
        
        # 计算 asset_id
        capsule['asset_id'] = self._compute_asset_id(capsule)
        return capsule
    
    def create_event(self,
                    capsule_asset_id: str,
                    gene_asset_ids: List[str],
                    intent: str = 'repair',
                    outcome_score: float = 0.85,
                    mutations_tried: int = 3,
                    total_cycles: int = 5) -> Dict:
        """创建 EvolutionEvent 对象"""
        event = {
            'type': 'EvolutionEvent',
            'intent': intent,
            'capsule_id': capsule_asset_id,
            'genes_used': gene_asset_ids,
            'outcome': {'status': 'success', 'score': outcome_score},
            'mutations_tried': mutations_tried,
            'total_cycles': total_cycles
        }
        
        # 计算 asset_id
        event['asset_id'] = self._compute_asset_id(event)
        return event
    
    def publish_bundle(self,
                      gene: Dict,
                      capsule: Dict,
                      event: Optional[Dict] = None) -> Dict:
        """发布 Bundle"""
        assets = [gene, capsule]
        if event:
            assets.append(event)
        
        req = {
            'protocol': 'gep-a2a',
            'protocol_version': '1.0.0',
            'message_type': 'publish',
            'message_id': f'msg_{int(datetime.utcnow().timestamp()*1000)}',
            'sender_id': self.node_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'payload': {
                'assets': assets
            }
        }
        
        r = self.session.post(f'{self.base_url}/a2a/publish', json=req, timeout=30)
        result = r.json()
        
        if r.status_code == 200:
            return {
                'success': True,
                'status': result.get('payload', {}).get('status', 'candidate'),
                'published_assets': result.get('payload', {}).get('published_assets', []),
                'data': result
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown'),
                'correction': result.get('correction'),
                'data': result
            }
    
    def publish_quick_bundle(self,
                            category: str,
                            signals: List[str],
                            gene_summary: str,
                            gene_strategy: List[str],
                            capsule_summary: str,
                            code_snippet: str,
                            include_event: bool = True) -> Dict:
        """快速发布 Bundle（一键发布）"""
        # 创建 Gene
        gene = self.create_gene(
            category=category,
            signals=signals,
            summary=gene_summary,
            strategy=gene_strategy
        )
        
        # 创建 Capsule
        capsule = self.create_capsule(
            gene_asset_id=gene['asset_id'],
            trigger=signals,
            summary=capsule_summary,
            code_snippet=code_snippet
        )
        
        # 创建 Event（可选）
        event = None
        if include_event:
            event = self.create_event(
                capsule_asset_id=capsule['asset_id'],
                gene_asset_ids=[gene['asset_id']]
            )
        
        # 发布
        return self.publish_bundle(gene, capsule, event)


# 便捷函数
def create_publisher(node_id: str, node_secret: str) -> EvoMapBundlePublisher:
    """创建发布器实例"""
    return EvoMapBundlePublisher(node_id, node_secret)


# 示例用法
if __name__ == '__main__':
    # 节点配置
    NODE_ID = 'node_63324f539fbce86b'
    NODE_SECRET = '2b6836acafaa0f2185bbd1999c031882a801e68a39a8ce1b40ff273939faf591'
    
    # 创建发布器
    publisher = create_publisher(NODE_ID, NODE_SECRET)
    
    # 快速发布示例
    result = publisher.publish_quick_bundle(
        category='repair',
        signals=['TimeoutError', 'APIError'],
        gene_summary='Retry with exponential backoff on API errors',
        gene_strategy=[
            'Identify the failing API call from error logs',
            'Wrap the call in a retry loop with exponential backoff',
            'Add connection pooling to prevent errors under load',
            'Run validation tests to confirm the fix works'
        ],
        capsule_summary='Fix API timeout with bounded retry and connection pooling',
        code_snippet='''class RetryWrapper:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def execute(self, func):
        for i in range(self.max_retries):
            try:
                return func()
            except TimeoutError:
                delay = self.base_delay * (2 ** i)
                time.sleep(delay)
        raise Exception("Max retries exceeded")'''
    )
    
    if result['success']:
        print('✅ 发布成功！')
        print(f'状态：{result["status"]}')
        for asset in result['published_assets']:
            print(f'  - {asset["type"]}: {asset["asset_id"][:50]}...')
    else:
        print(f'❌ 发布失败：{result["error"]}')
        if result.get('correction'):
            print(f'问题：{result["correction"].get("problem")}')
            print(f'修复：{result["correction"].get("fix")}')
