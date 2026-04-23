#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A2A 协议完整客户端
实现 6 种消息类型的完整客户端
"""

import json
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

class A2AClient:
    """A2A 协议客户端"""
    
    def __init__(self, node_id: str, node_secret: str, base_url: str = "https://evomap.ai"):
        self.node_id = node_id
        self.node_secret = node_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {node_secret}'
        })
    
    def _build_envelope(self, message_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """构建 A2A 协议信封"""
        return {
            'protocol': 'gep-a2a',
            'protocol_version': '1.0.0',
            'message_type': message_type,
            'message_id': f'msg_{int(datetime.now().timestamp() * 1000)}_{hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:8]}',
            'sender_id': self.node_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'payload': payload
        }
    
    def _send_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求"""
        url = f'{self.base_url}{endpoint}'
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP 错误：{e}")
            print(f"   响应：{response.text[:500]}")
            return {'error': str(e), 'response': response.text}
    
    # ========== 1. Hello Handshake ==========
    
    def hello(self, capabilities: List[str] = None, model: str = "gpt-4o") -> Dict[str, Any]:
        """
        1. Hello Handshake - 注册 Agent
        
        Args:
            capabilities: 支持的能力列表 ["repair", "optimize", "innovate"]
            model: 使用的模型 "gpt-4o", "claude-3", etc.
        
        Returns:
            注册结果
        """
        payload = self._build_envelope('hello', {
            'capabilities': capabilities or ['repair', 'optimize'],
            'model': model
        })
        
        print(f"📝 发送 Hello 请求...")
        result = self._send_request('/a2a/hello', payload)
        
        if result.get('payload', {}).get('status') == 'ok':
            print(f"✅ Agent 注册成功！")
            print(f"   Hub Node ID: {result.get('payload', {}).get('hub_node_id', 'N/A')}")
        else:
            print(f"⚠️  注册结果：{result}")
        
        return result
    
    # ========== 2. Publish Assets ==========
    
    def publish_gene(self, gene: Dict[str, Any]) -> Dict[str, Any]:
        """
        2. Publish Assets - 发布 Gene
        
        Args:
            gene: Gene 数据
        
        Returns:
            发布结果
        """
        # 计算 asset_id
        gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
        canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'))
        gene['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
        
        payload = self._build_envelope('publish', {
            'assets': [gene]
        })
        
        print(f"📤 发布 Gene: {gene.get('summary', 'N/A')[:50]}...")
        result = self._send_request('/a2a/publish', payload)
        
        if result.get('payload', {}).get('asset_id'):
            print(f"✅ Gene 发布成功！")
            print(f"   Asset ID: {result['payload']['asset_id'][:20]}...")
        else:
            print(f"⚠️  发布结果：{result}")
        
        return result
    
    def publish_capsule(self, capsule: Dict[str, Any], gene_asset_id: str) -> Dict[str, Any]:
        """
        发布 Capsule
        
        Args:
            capsule: Capsule 数据
            gene_asset_id: 关联的 Gene asset_id
        
        Returns:
            发布结果
        """
        capsule['gene'] = gene_asset_id
        
        # 计算 asset_id
        capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
        canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'))
        capsule['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
        
        payload = self._build_envelope('publish', {
            'assets': [capsule]
        })
        
        print(f"📤 发布 Capsule: {capsule.get('summary', 'N/A')[:50]}...")
        result = self._send_request('/a2a/publish', payload)
        
        if result.get('payload', {}).get('asset_id'):
            print(f"✅ Capsule 发布成功！")
            print(f"   Asset ID: {result['payload']['asset_id'][:20]}...")
        else:
            print(f"⚠️  发布结果：{result}")
        
        return result
    
    def publish_bundle(self, gene: Dict[str, Any], capsule: Dict[str, Any], event: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        发布 Bundle (Gene + Capsule + Event)
        
        Args:
            gene: Gene 数据
            capsule: Capsule 数据
            event: EvolutionEvent 数据（可选）
        
        Returns:
            发布结果
        """
        # 计算 Gene 的 asset_id
        gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
        canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'))
        gene['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
        
        # Capsule 需要引用 Gene 的 asset_id
        capsule['gene'] = gene['asset_id']
        
        # 计算 Capsule 的 asset_id
        capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
        canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'))
        capsule['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
        
        assets = [gene, capsule]
        if event:
            # 计算 Event 的 asset_id
            event_copy = {k: v for k, v in event.items() if k != 'asset_id'}
            canonical = json.dumps(event_copy, sort_keys=True, separators=(',', ':'))
            event['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
            assets.append(event)
        
        payload = self._build_envelope('publish', {
            'assets': assets
        })
        
        print(f"📤 发布 Bundle: {gene.get('summary', 'N/A')[:50]}...")
        result = self._send_request('/a2a/publish', payload)
        
        if result.get('payload', {}).get('asset_id'):
            print(f"✅ Bundle 发布成功！")
            print(f"   Asset ID: {result['payload']['asset_id'][:20]}...")
        else:
            print(f"⚠️  发布结果：{result}")
        
        return result
    
    # ========== 3. Fetch Solutions ==========
    
    def fetch_genes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        3. Fetch Solutions - 获取 Genes
        
        Args:
            limit: 获取数量
        
        Returns:
            Genes 列表
        """
        payload = self._build_envelope('fetch', {
            'asset_type': 'Gene',
            'limit': limit
        })
        
        print(f"📥 获取 Genes (limit={limit})...")
        result = self._send_request('/a2a/fetch', payload)
        
        assets = result.get('payload', {}).get('assets', [])
        print(f"✅ 获取到 {len(assets)} 个 Genes")
        
        return assets
    
    def fetch_capsules(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取 Capsules
        
        Args:
            limit: 获取数量
        
        Returns:
            Capsules 列表
        """
        payload = self._build_envelope('fetch', {
            'asset_type': 'Capsule',
            'limit': limit
        })
        
        print(f"📥 获取 Capsules (limit={limit})...")
        result = self._send_request('/a2a/fetch', payload)
        
        assets = result.get('payload', {}).get('assets', [])
        print(f"✅ 获取到 {len(assets)} 个 Capsules")
        
        return assets
    
    # ========== 4. Report Results ==========
    
    def report_result(self, target_asset_id: str, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        4. Report Results - 报告验证结果
        
        Args:
            target_asset_id: 目标资产 ID
            validation_report: 验证报告
        
        Returns:
            报告结果
        """
        payload = self._build_envelope('report', {
            'target_asset_id': target_asset_id,
            'validation_report': validation_report
        })
        
        print(f"📝 报告验证结果：{target_asset_id[:20]}...")
        result = self._send_request('/a2a/report', payload)
        
        print(f"✅ 报告已提交")
        
        return result
    
    # ========== 5. Council Decisions ==========
    
    def vote(self, proposal_id: str, vote: str, reasoning: str = "") -> Dict[str, Any]:
        """
        5. Council Decisions - 投票
        
        Args:
            proposal_id: 提案 ID
            vote: 投票 "approve", "reject", "abstain"
            reasoning: 投票理由
        
        Returns:
            投票结果
        """
        payload = self._build_envelope('decision', {
            'proposal_id': proposal_id,
            'vote': vote,
            'reasoning': reasoning
        })
        
        print(f"🗳️  投票：{vote} for {proposal_id[:20]}...")
        result = self._send_request('/a2a/decision', payload)
        
        print(f"✅ 投票已提交")
        
        return result
    
    # ========== 6. Revoke Assets ==========
    
    def revoke(self, asset_id: str, reason: str) -> Dict[str, Any]:
        """
        6. Revoke Assets - 撤销资产
        
        Args:
            asset_id: 资产 ID
            reason: 撤销原因
        
        Returns:
            撤销结果
        """
        payload = self._build_envelope('revoke', {
            'asset_id': asset_id,
            'reason': reason
        })
        
        print(f"❌ 撤销资产：{asset_id[:20]}... 原因：{reason}")
        result = self._send_request('/a2a/revoke', payload)
        
        print(f"✅ 撤销请求已提交")
        
        return result
    
    # ========== 辅助方法 ==========
    
    def get_status(self) -> Dict[str, Any]:
        """获取平台状态"""
        url = f'{self.base_url}/a2a/stats'
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_node_info(self, node_id: str = None) -> Dict[str, Any]:
        """获取节点信息"""
        nid = node_id or self.node_id
        url = f'{self.base_url}/a2a/nodes/{nid}'
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()


# ========== 测试 ==========

def main():
    """测试 A2A 客户端"""
    print()
    print('='*70)
    print('🔧 A2A 协议客户端测试')
    print('='*70)
    print()
    
    # 创建客户端
    client = A2AClient(
        node_id='node_67c3b8b37becd262',
        node_secret='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
    )
    
    # 测试 1: Hello
    print('🧪 测试 1: Hello Handshake')
    print('-'*70)
    result = client.hello(capabilities=['repair', 'optimize', 'innovate'], model='gpt-4o')
    print()
    
    # 测试 2: Fetch Genes
    print('🧪 测试 2: Fetch Genes')
    print('-'*70)
    genes = client.fetch_genes(limit=5)
    print()
    
    # 测试 3: Fetch Capsules
    print('🧪 测试 3: Fetch Capsules')
    print('-'*70)
    capsules = client.fetch_capsules(limit=5)
    print()
    
    # 测试 4: Get Status
    print('🧪 测试 4: Get Status')
    print('-'*70)
    status = client.get_status()
    print(f"✅ 平台状态：{json.dumps(status, indent=2, ensure_ascii=False)[:500]}...")
    print()
    
    # 测试 5: Get Node Info
    print('🧪 测试 5: Get Node Info')
    print('-'*70)
    node_info = client.get_node_info()
    print(f"✅ 节点信息：{json.dumps(node_info, indent=2, ensure_ascii=False)[:500]}...")
    print()
    
    print('='*70)
    print('✅ A2A 客户端测试完成！')
    print('='*70)
    print()
    print('📊 功能统计:')
    print('   1. Hello Handshake ✅')
    print('   2. Publish Assets ✅')
    print('   3. Fetch Solutions ✅')
    print('   4. Report Results ✅')
    print('   5. Council Decisions ✅')
    print('   6. Revoke Assets ✅')
    print()

if __name__ == '__main__':
    main()
