#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "flask", "cryptography"]
# ///
"""
飞书 OAuth 2.0 完整实现
Feishu OAuth 2.0 Complete Implementation

功能:
- 授权码模式
- Token 管理
- 用户信息获取
- Token 刷新
- 安全存储

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import json
import time
import secrets
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet

# ============================================================================
# 1. OAuth 配置
# ============================================================================

class OAuthConfig:
    """OAuth 配置类"""
    
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.redirect_uri = os.getenv("FEISHU_REDIRECT_URI", "http://localhost:5000/oauth/callback")
        self.secret_key = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
        
        self.auth_base_url = "https://open.feishu.cn/open-apis/authen/v1"
        
        if not all([self.app_id, self.app_secret]):
            raise ValueError("请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")

# ============================================================================
# 2. Token 管理器
# ============================================================================

class TokenManager:
    """
    Token 管理器 - 自动刷新 Token
    
    Attributes:
        access_token: Access Token
        refresh_token: Refresh Token
        expires_at: 过期时间
    """
    
    def __init__(self, access_token: str, refresh_token: str, expires_in: int):
        """
        初始化 Token 管理器
        
        Args:
            access_token: Access Token
            refresh_token: Refresh Token
            expires_in: 有效期（秒）
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        # 提前 5 分钟刷新
        self.expires_at = time.time() + expires_in - 300
    
    def is_expired(self) -> bool:
        """检查 Token 是否过期"""
        return time.time() >= self.expires_at
    
    def get_access_token(self) -> str:
        """获取有效的 Access Token"""
        if self.is_expired():
            raise Exception("Token 已过期，请重新授权")
        return self.access_token
    
    def update(self, access_token: str, refresh_token: str, expires_in: int):
        """更新 Token"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = time.time() + expires_in - 300

# ============================================================================
# 3. 飞书 OAuth 客户端
# ============================================================================

class FeishuOAuthClient:
    """
    飞书 OAuth 客户端
    
    Methods:
        get_authorization_url: 获取授权 URL
        get_access_token: 获取 Access Token
        refresh_access_token: 刷新 Access Token
        get_user_info: 获取用户信息
    """
    
    def __init__(self, config: Optional[OAuthConfig] = None):
        """
        初始化 OAuth 客户端
        
        Args:
            config: OAuth 配置
        """
        self.config = config or OAuthConfig()
        self.token_manager: Optional[TokenManager] = None
    
    def get_authorization_url(self, state: Optional[str] = None) -> tuple:
        """
        获取授权 URL
        
        Args:
            state: 状态参数（防 CSRF）
        
        Returns:
            tuple: (授权 URL, state)
        """
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "app_id": self.config.app_id,
            "redirect_uri": self.config.redirect_uri,
            "state": state,
            "response_type": "code"
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"{self.config.auth_base_url}/authorize?{query_string}"
        
        return auth_url, state
    
    def get_access_token(self, code: str) -> Dict[str, Any]:
        """
        用授权码换取 Access Token
        
        Args:
            code: 授权码
        
        Returns:
            dict: Token 信息
        """
        url = f"{self.config.auth_base_url}/access_token"
        
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.config.app_id,
            "client_secret": self.config.app_secret,
            "redirect_uri": self.config.redirect_uri
        }
        
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取 Token 失败：{result.get('msg')}")
        
        token_data = result["data"]
        
        # 创建 Token 管理器
        self.token_manager = TokenManager(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_in=token_data["expires_in"]
        )
        
        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
            "token_type": token_data["token_type"]
        }
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """
        刷新 Access Token
        
        Returns:
            dict: 新 Token 信息
        """
        if not self.token_manager:
            raise Exception("没有可用的 Refresh Token")
        
        url = f"{self.config.auth_base_url}/refresh_access_token"
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.token_manager.refresh_token,
            "client_id": self.config.app_id,
            "client_secret": self.config.app_secret
        }
        
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"刷新 Token 失败：{result.get('msg')}")
        
        token_data = result["data"]
        
        # 更新 Token 管理器
        self.token_manager.update(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_in=token_data["expires_in"]
        )
        
        return token_data
    
    def get_access_token_safe(self) -> str:
        """安全获取 Access Token（自动刷新）"""
        if not self.token_manager:
            raise Exception("未授权，请先登录")
        
        if self.token_manager.is_expired():
            self.refresh_access_token()
        
        return self.token_manager.get_access_token()
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        获取用户信息
        
        Returns:
            dict: 用户信息
        """
        access_token = self.get_access_token_safe()
        
        url = f"{self.config.auth_base_url}/user_info"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers, timeout=10)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取用户信息失败：{result.get('msg')}")
        
        return result["data"]
    
    def logout(self):
        """退出登录"""
        self.token_manager = None

# ============================================================================
# 4. 加密工具
# ============================================================================

class TokenEncryptor:
    """Token 加密器"""
    
    def __init__(self, secret_key: str):
        """
        初始化加密器
        
        Args:
            secret_key: 密钥
        """
        self.cipher = Fernet(secret_key.encode() if isinstance(secret_key, str) else secret_key)
    
    def encrypt(self, token: str) -> bytes:
        """加密 Token"""
        return self.cipher.encrypt(token.encode())
    
    def decrypt(self, encrypted_token: bytes) -> str:
        """解密 Token"""
        return self.cipher.decrypt(encrypted_token).decode()

# ============================================================================
# 5. 命令行示例
# ============================================================================

def main():
    """命令行示例"""
    print("=" * 60)
    print("飞书 OAuth 2.0 完整实现")
    print("=" * 60)
    print()
    
    # 初始化客户端
    client = FeishuOAuthClient()
    
    # 生成授权 URL
    auth_url, state = client.get_authorization_url()
    
    print("1. 访问以下授权 URL:")
    print(f"   {auth_url}")
    print()
    print("2. 登录并授权")
    print()
    print("3. 复制回调 URL 中的 code 参数")
    print()
    
    code = input("请输入授权码 (code): ").strip()
    
    try:
        # 获取 Token
        token_info = client.get_access_token(code)
        
        print("\n✅ 获取 Token 成功!")
        print(f"   Access Token: {token_info['access_token'][:50]}...")
        print(f"   Refresh Token: {token_info['refresh_token'][:50]}...")
        print(f"   有效期：{token_info['expires_in']} 秒")
        print()
        
        # 获取用户信息
        user_info = client.get_user_info()
        
        print("✅ 用户信息:")
        print(f"   用户 ID: {user_info.get('user_id')}")
        print(f"   姓名：{user_info.get('name')}")
        print(f"   邮箱：{user_info.get('email')}")
        print(f"   手机号：{user_info.get('mobile')}")
        print()
        
        # 测试 Token 刷新
        print("测试 Token 刷新...")
        new_token_info = client.refresh_access_token()
        print(f"✅ Token 刷新成功!")
        print(f"   新 Access Token: {new_token_info['access_token'][:50]}...")
        print()
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")

if __name__ == "__main__":
    main()
