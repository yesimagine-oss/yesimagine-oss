#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEP-A2A 协议客户端库
用于与 EvoMap Hub 进行 A2A 协议通信

功能:
- hello: 节点认证
- fetch: 获取任务列表
- publish: 发布资产
- report: 提交结果
- decision: Claim/Release 任务
- revoke: 撤销任务

使用示例:
    client = GAPA2AClient(NODE_ID, NODE_SECRET)
    client.hello()
    tasks = client.fetch_tasks(limit=5)
    for task in tasks:
        client.claim_task(task['id'])
"""

import requests
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GAPA2AClient:
    """GEP-A2A 协议客户端"""
    
    # GEP-A2A 协议版本
    PROTOCOL_VERSION = "1.0.0"
    
    # 消息类型
    MESSAGE_TYPES = {
        "HELLO": "hello",
        "PUBLISH": "publish",
        "FETCH": "fetch",
        "REPORT": "report",
        "DECISION": "decision",
        "REVOKE": "revoke"
    }
    
    def __init__(self, node_id: str, node_secret: str, base_url: str = "https://evomap.ai"):
        """
        初始化客户端
        
        Args:
            node_id: 节点 ID (如: node_xxx)
            node_secret: 节点密钥
            base_url: EvoMap API 基础 URL
        """
        self.node_id = node_id
        self.node_secret = node_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.hub_node_id = None
        self.owner_user_id = None
        
        logger.info(f"GAPA2AClient 初始化：node_id={node_id}, base_url={base_url}")
    
    def _generate_message_id(self) -> str:
        """生成唯一 message_id"""
        return f"msg_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    def _get_timestamp(self) -> str:
        """获取 ISO 8601 UTC 时间戳"""
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def _build_envelope(self, message_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建 GEP-A2A 协议信封
        
        Args:
            message_type: 消息类型 (hello/publish/fetch/report/decision/revoke)
            payload: 消息负载
        
        Returns:
            完整的协议信封
        """
        return {
            "protocol": "gep-a2a",
            "protocol_version": self.PROTOCOL_VERSION,
            "message_type": message_type,
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": self._get_timestamp(),
            "payload": payload
        }
    
    def _send_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送 A2A 协议请求
        
        Args:
            endpoint: API 端点 (如：/a2a/hello)
            payload: 协议信封
        
        Returns:
            响应数据
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"发送请求：{url}")
        
        try:
            # 添加 node_secret 认证
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.node_secret}"
            }
            
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # 检查响应
            if response.status_code != 200:
                logger.error(f"请求失败：{response.status_code} - {response.text[:200]}")
                return {"error": f"HTTP {response.status_code}", "details": response.text}
            
            # 解析 JSON
            try:
                result = response.json()
                logger.debug(f"响应：{result.get('message_type', 'unknown')}")
                return result
            except Exception as e:
                logger.error(f"JSON 解析失败：{e}")
                return {"error": "JSON parse error", "details": response.text[:500]}
        
        except requests.exceptions.Timeout:
            logger.error("请求超时")
            return {"error": "timeout"}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"连接错误：{e}")
            return {"error": "connection error"}
        except Exception as e:
            logger.error(f"未知错误：{e}")
            return {"error": str(e)}
    
    def _capture_env_fingerprint(self) -> Dict[str, Any]:
        """
        捕获环境指纹（完全照搬官方 envFingerprint.js 实现）
        官方位置：node_modules/@evomap/evolver/src/gep/envFingerprint.js
        
        Returns:
            环境指纹对象
        """
        import os
        import platform
        import hashlib
        import socket
        from pathlib import Path
        
        # 获取 evolver 版本（从官方 package.json 读取）
        evolver_version = None
        client_name = 'evolver'
        
        # 方法 1: 从 __dirname 读取（官方推荐）
        own_pkg_path = Path(__file__).parent.parent / 'node_modules' / '@evomap' / 'evolver' / 'package.json'
        try:
            if own_pkg_path.exists():
                import json
                pkg = json.loads(own_pkg_path.read_text())
                evolver_version = pkg.get('version')
                client_name = pkg.get('name', 'evolver')
        except:
            pass
        
        # 方法 2: 从 repo root 读取（备用）
        if not evolver_version:
            try:
                repo_pkg = Path(__file__).parent.parent / 'package.json'
                if repo_pkg.exists():
                    import json
                    pkg = json.loads(repo_pkg.read_text())
                    evolver_version = pkg.get('version')
                    client_name = pkg.get('name', 'evolver')
            except:
                pass
        
        # 默认值：动态读取全局安装的 evolver 版本
        if not evolver_version:
            try:
                # 方法 3: 从全局 evolver 读取
                import subprocess
                result = subprocess.run(
                    ['npm', 'list', '-g', '@evomap/evolver'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # 解析输出：@evomap/evolver@1.39.0
                for line in result.stdout.split('\n'):
                    if '@evomap/evolver@' in line:
                        evolver_version = line.split('@evomap/evolver@')[1].strip()
                        break
            except:
                pass
        
        # 最终默认值（仅当所有方法都失败时）
        if not evolver_version:
            evolver_version = 'unknown'
            logger.warning("无法获取 evolver 版本号，设置为 'unknown'")
        
        # 获取设备 ID（简化版，参考官方 getDeviceId()）
        try:
            device_id = hashlib.sha256(socket.gethostname().encode()).hexdigest()[:12]
        except:
            device_id = 'unknown'
        
        # 获取 region（参考官方）
        region = (os.environ.get('EVOLVER_REGION') or '').strip().lower()[:5] or None
        
        # 获取 cwd hash（参考官方）
        try:
            cwd_hash = hashlib.sha256(os.getcwd().encode()).hexdigest()[:12]
        except:
            cwd_hash = 'unknown'
        
        # 检查是否容器（参考官方 isContainer()）
        is_container = os.path.exists('/.dockerenv')
        
        # 完全照搬官方结构
        return {
            'device_id': device_id,
            'node_version': platform.python_version(),  # Python 版本（对应 Node 的 node_version）
            'platform': platform.system(),
            'arch': platform.machine(),
            'os_release': platform.release(),
            'hostname': hashlib.sha256(socket.gethostname().encode()).hexdigest()[:12] if socket.gethostname() else 'unknown',
            'evolver_version': evolver_version,  # ← 正确位置：在 env_fingerprint 内部
            'client': client_name,
            'client_version': evolver_version,   # ← 正确位置：在 env_fingerprint 内部
            'region': region,
            'cwd': cwd_hash,
            'container': is_container,
            'captured_at': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
    
    def hello(self) -> Dict[str, Any]:
        """
        节点认证（Hello 握手）
        
        Returns:
            认证结果
        """
        logger.info("开始 Hello 握手...")
        
        # 获取环境指纹
        env_fp = self._capture_env_fingerprint()
        
        # 构建 payload：版本号只在 env_fingerprint 内部
        payload = self._build_envelope(
            self.MESSAGE_TYPES["HELLO"],
            {
                "node_secret": self.node_secret,
                "env_fingerprint": env_fp
            }
        )
        
        result = self._send_request("/a2a/hello", payload)
        
        # 解析响应
        if result.get("payload", {}).get("status") in ["ok", "acknowledged"]:
            self.hub_node_id = result.get("payload", {}).get("hub_node_id")
            self.owner_user_id = result.get("payload", {}).get("owner_user_id")
            logger.info(f"Hello 成功：hub_node_id={self.hub_node_id}")
            return {"success": True, "data": result}
        else:
            reason = result.get("payload", {}).get("reason", "unknown")
            logger.error(f"Hello 失败：{reason}")
            return {"success": False, "error": reason, "data": result}
    
    def fetch_tasks(self, limit: int = 5, task_type: str = "any", max_retries: int = 3) -> Dict[str, Any]:
        """
        获取可用任务列表（带重试机制）
        
        Args:
            limit: 任务数量限制
            task_type: 任务类型 (any/bounty/question)
            max_retries: 最大重试次数
        
        Returns:
            任务列表
        """
        logger.info(f"获取任务列表：limit={limit}, task_type={task_type}, max_retries={max_retries}")
        
        payload = self._build_envelope(
            self.MESSAGE_TYPES["FETCH"],
            {
                "task_type": task_type,
                "limit": limit
            }
        )
        
        # 重试逻辑
        for attempt in range(1, max_retries + 1):
            result = self._send_request("/a2a/fetch", payload)
            
            # 检查是否是 503 错误
            if result.get("error") == "server_busy" or "503" in str(result.get("data", {}).get("error", "")):
                retry_after = result.get("data", {}).get("retry_after_ms", 5000)
                logger.warning(f"⚠️ 服务器繁忙，{retry_after}ms 后重试 ({attempt}/{max_retries})")
                
                if attempt < max_retries:
                    import time
                    time.sleep(retry_after / 1000.0)
                    continue
            else:
                # 成功或其他错误，跳出重试
                break
        
        # 解析响应
        tasks = result.get("payload", {}).get("tasks", [])
        logger.info(f"获取到 {len(tasks)} 个任务")
        
        return {
            "success": len(tasks) > 0 or result.get("success", False),
            "count": len(tasks),
            "tasks": tasks,
            "data": result,
            "retries": attempt
        }
    
    def claim_task(self, task_id: str) -> Dict[str, Any]:
        """
        Claim 任务
        
        Args:
            task_id: 任务 ID
        
        Returns:
            Claim 结果
        """
        logger.info(f"Claim 任务：{task_id}")
        
        payload = self._build_envelope(
            self.MESSAGE_TYPES["DECISION"],
            {
                "task_id": task_id,
                "decision": "claim"
            }
        )
        
        result = self._send_request("/a2a/decision", payload)
        
        # 解析响应
        status = result.get("payload", {}).get("status", "unknown")
        if status == "ok" or status == "claimed":
            logger.info(f"Claim 成功：{task_id}")
            return {"success": True, "task_id": task_id, "data": result}
        else:
            reason = result.get("payload", {}).get("reason", "unknown")
            logger.error(f"Claim 失败：{reason}")
            return {"success": False, "task_id": task_id, "error": reason, "data": result}
    
    def release_task(self, task_id: str, reason: str = "not_suitable") -> Dict[str, Any]:
        """
        Release 任务
        
        Args:
            task_id: 任务 ID
            reason: 释放原因
        
        Returns:
            Release 结果
        """
        logger.info(f"Release 任务：{task_id}, reason={reason}")
        
        payload = self._build_envelope(
            self.MESSAGE_TYPES["DECISION"],
            {
                "task_id": task_id,
                "decision": "release",
                "reason": reason
            }
        )
        
        result = self._send_request("/a2a/decision", payload)
        
        status = result.get("payload", {}).get("status", "unknown")
        if status == "ok" or status == "released":
            logger.info(f"Release 成功：{task_id}")
            return {"success": True, "task_id": task_id, "data": result}
        else:
            reason = result.get("payload", {}).get("reason", "unknown")
            logger.error(f"Release 失败：{reason}")
            return {"success": False, "task_id": task_id, "error": reason, "data": result}
    
    def publish_asset(self, asset_type: str, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发布资产
        
        Args:
            asset_type: 资产类型 (Gene/Capsule/EvolutionEvent)
            asset_data: 资产数据
        
        Returns:
            发布结果
        """
        logger.info(f"发布资产：{asset_type}")
        
        payload = self._build_envelope(
            self.MESSAGE_TYPES["PUBLISH"],
            {
                "asset_type": asset_type,
                "asset": asset_data
            }
        )
        
        result = self._send_request("/a2a/publish", payload)
        
        asset_id = result.get("payload", {}).get("asset_id")
        if asset_id:
            logger.info(f"发布成功：{asset_id}")
            return {"success": True, "asset_id": asset_id, "data": result}
        else:
            reason = result.get("payload", {}).get("reason", "unknown")
            logger.error(f"发布失败：{reason}")
            return {"success": False, "error": reason, "data": result}
    
    def report_result(self, task_id: str, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        提交任务结果
        
        Args:
            task_id: 任务 ID
            result_data: 结果数据
        
        Returns:
            提交结果
        """
        logger.info(f"提交任务结果：{task_id}")
        
        payload = self._build_envelope(
            self.MESSAGE_TYPES["REPORT"],
            {
                "task_id": task_id,
                "result": result_data
            }
        )
        
        result = self._send_request("/a2a/report", payload)
        
        status = result.get("payload", {}).get("status", "unknown")
        if status == "ok" or status == "submitted":
            logger.info(f"提交成功：{task_id}")
            return {"success": True, "task_id": task_id, "data": result}
        else:
            reason = result.get("payload", {}).get("reason", "unknown")
            logger.error(f"提交失败：{reason}")
            return {"success": False, "task_id": task_id, "error": reason, "data": result}
    
    def heartbeat(self, include_discovery: bool = True) -> Dict[str, Any]:
        """
        发送心跳并获取完整的发现信息（推荐、任务等）
        
        Args:
            include_discovery: 是否包含发现信息（推荐、任务、协作等）
        
        Returns:
            心跳响应（包含完整的 discovery 信息）
        """
        logger.info("发送 Heartbeat...")
        
        # 构建简单的 heartbeat payload（不需要完整信封）
        payload = {
            "node_id": self.node_id,
            "status": "online",
            "request_discovery": include_discovery
        }
        
        # 使用 /a2a/heartbeat 端点（不是 /a2a/hello）
        result = self._send_request("/a2a/heartbeat", payload)
        
        # 更新状态
        if result.get("status") == "ok" or result.get("payload", {}).get("status") in ["ok", "acknowledged"]:
            self.hub_node_id = result.get("hub_node_id") or result.get("payload", {}).get("hub_node_id")
            logger.info(f"Heartbeat 成功：hub_node_id={self.hub_node_id}")
        
        return result
    
    def discover(self) -> Dict[str, Any]:
        """
        获取完整的发现信息（推荐、任务、协作等）
        
        Returns:
            发现信息
        """
        logger.info("获取 Discovery 信息...")
        
        payload = self._build_envelope(
            "fetch",
            {
                "node_secret": self.node_secret,
                "include_recommendations": True,
                "include_tasks": True,
                "include_collaboration": True,
                "limit": 10
            }
        )
        
        result = self._send_request("/a2a/discover", payload)
        
        return result
    
    def check_status(self) -> Dict[str, Any]:
        """
        检查 Hub 连接状态
        
        Returns:
            状态信息
        """
        logger.info("检查 Hub 状态...")
        
        # 使用新的 heartbeat 方法
        result = self.heartbeat(include_discovery=True)
        
        return {
            "connected": result.get("payload", {}).get("status") in ["ok", "acknowledged"],
            "hub_node_id": self.hub_node_id,
            "owner_user_id": self.owner_user_id,
            "data": result
        }


# 便捷函数
def create_client(node_id: str, node_secret: str, base_url: str = "https://evomap.ai") -> GAPA2AClient:
    """
    创建 GEP-A2A 客户端
    
    Args:
        node_id: 节点 ID
        node_secret: 节点密钥
        base_url: API 基础 URL
    
    Returns:
        GAPA2AClient 实例
    """
    return GAPA2AClient(node_id, node_secret, base_url)


# 测试代码
if __name__ == "__main__":
    # 测试配置
    NODE_ID = "node_67c3b8b37becd262"
    NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
    
    # 创建客户端
    client = create_client(NODE_ID, NODE_SECRET)
    
    # 测试 Hello
    print("=== 测试 Hello ===")
    result = client.hello()
    print(f"Hello 结果：{result}")
    
    # 测试 Fetch
    print("\n=== 测试 Fetch ===")
    result = client.fetch_tasks(limit=3)
    print(f"Fetch 结果：{result}")
    
    # 测试状态检查
    print("\n=== 测试状态检查 ===")
    result = client.check_status()
    print(f"状态：{result}")
