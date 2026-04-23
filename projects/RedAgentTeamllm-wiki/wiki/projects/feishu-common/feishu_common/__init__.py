#!/usr/bin/env python3
"""
飞书公共模块库
Feishu Common Modules

包含所有项目共用的模块：
- Token 管理器
- 日志配置
- 错误处理
- 工具函数

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import sys
import time
import logging
import hashlib
import base64
import hmac
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Callable, TypeVar, Generic
from functools import wraps

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================================================
# 1. 类型定义
# ============================================================================

T = TypeVar('T')
F = TypeVar('F', bound=Callable)

# ============================================================================
# 2. Token 管理器
# ============================================================================

class FeishuTokenManager:
    """
    飞书 Token 管理器 - 自动获取和刷新 Token
    
    Attributes:
        app_id: 应用 ID
        app_secret: 应用 Secret
        app_access_token: 当前 Token
        token_expire_time: Token 过期时间
    """
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化 Token 管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_access_token: Optional[str] = None
        self.token_expire_time: float = 0
    
    def get_app_access_token(self) -> str:
        """
        获取应用 Access Token
        
        Returns:
            str: Access Token
            
        Raises:
            Exception: 获取 Token 失败
        """
        # 如果 Token 未过期，直接返回
        if self.app_access_token and time.time() < self.token_expire_time:
            return self.app_access_token
        
        # 获取新 Token
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 Token 失败：{result.get('msg')}")
            
            self.app_access_token = result["app_access_token"]
            # Token 有效期 2 小时，提前 10 分钟刷新
            self.token_expire_time = time.time() + 7200 - 600
            
            return self.app_access_token
        
        except Exception as e:
            raise Exception(f"获取 Token 失败：{e}")
    
    def refresh_token(self):
        """强制刷新 Token"""
        self.app_access_token = None
        self.token_expire_time = 0
        return self.get_app_access_token()
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

# ============================================================================
# 3. 日志配置
# ============================================================================

def setup_logging(
    name: str = __name__,
    level: str = "INFO",
    log_dir: str = "logs"
) -> logging.Logger:
    """
    配置日志
    
    Args:
        name: 日志名称
        level: 日志级别
        log_dir: 日志目录
        
    Returns:
        logging.Logger: 配置好的日志对象
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(name)

# ============================================================================
# 4. 错误处理
# ============================================================================

class FeishuError(Exception):
    """飞书 API 错误基类"""
    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.code = code

class TokenError(FeishuError):
    """Token 错误"""
    pass

class APIError(FeishuError):
    """API 调用错误"""
    pass

class PermissionError(FeishuError):
    """权限错误"""
    pass

def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始延迟（秒）
        backoff: 延迟倍数
        
    Returns:
        Callable: 装饰器函数
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    
    return decorator

def handle_api_errors(func: F) -> F:
    """
    API 错误处理装饰器
    
    Args:
        func: 被装饰的函数
        
    Returns:
        Callable: 装饰器函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            raise APIError("API 请求超时", code=504)
        except requests.exceptions.ConnectionError:
            raise APIError("网络连接错误", code=503)
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP 错误：{e}", code=e.response.status_code)
        except Exception as e:
            raise APIError(f"API 调用失败：{e}")
    
    return wrapper

# ============================================================================
# 5. 工具函数
# ============================================================================

def verify_signature(
    body: str,
    timestamp: str,
    nonce: str,
    signature: str,
    secret: str
) -> bool:
    """
    验证飞书签名
    
    Args:
        body: 请求体
        timestamp: 时间戳
        nonce: 随机数
        signature: 签名
        secret: 密钥
        
    Returns:
        bool: 签名是否有效
    """
    data = timestamp + nonce + secret
    expected_signature = base64.b64encode(
        hashlib.sha256(data.encode()).digest()
    ).decode()
    return signature == expected_signature

def parse_time(time_str: str, format: str = "%Y-%m-%d %H:%M") -> datetime:
    """
    解析时间字符串
    
    Args:
        time_str: 时间字符串
        format: 时间格式
        
    Returns:
        datetime: 解析后的时间对象
    """
    return datetime.strptime(time_str, format)

def format_time(dt: datetime, format: str = "%Y-%m-%d %H:%M") -> str:
    """
    格式化时间对象
    
    Args:
        dt: 时间对象
        format: 时间格式
        
    Returns:
        str: 格式化后的时间字符串
    """
    return dt.strftime(format)

def get_timestamp(dt: Optional[datetime] = None) -> int:
    """
    获取时间戳
    
    Args:
        dt: 时间对象（默认当前时间）
        
    Returns:
        int: 时间戳（秒）
    """
    if dt is None:
        dt = datetime.now()
    return int(dt.timestamp())

def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    时间戳转时间对象
    
    Args:
        timestamp: 时间戳（秒）
        
    Returns:
        datetime: 时间对象
    """
    return datetime.fromtimestamp(timestamp)

def batch_process(
    items: list,
    batch_size: int = 100,
    process_func: Callable = None,
    delay: float = 0.1
) -> list:
    """
    批量处理
    
    Args:
        items: 待处理列表
        batch_size: 每批数量
        process_func: 处理函数
        delay: 批次间延迟（秒）
        
    Returns:
        list: 处理结果列表
    """
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        if process_func:
            batch_results = [process_func(item) for item in batch]
            results.extend(batch_results)
        else:
            results.extend(batch)
        
        if i + batch_size < len(items):
            time.sleep(delay)
    
    return results

def safe_get(
    data: Dict,
    keys: list,
    default: Any = None
) -> Any:
    """
    安全获取嵌套字典值
    
    Args:
        data: 字典
        keys: 键列表
        default: 默认值
        
    Returns:
        Any: 获取的值
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current

# ============================================================================
# 6. 配置管理
# ============================================================================

class Config:
    """配置管理类"""
    
    def __init__(self, env_prefix: str = "FEISHU"):
        """
        初始化配置
        
        Args:
            env_prefix: 环境变量前缀
        """
        self.env_prefix = env_prefix
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            required: 是否必需
            
        Returns:
            Any: 配置值
            
        Raises:
            ValueError: 必需配置缺失
        """
        full_key = f"{self.env_prefix}_{key}"
        value = os.getenv(full_key, default)
        
        if required and value is None:
            raise ValueError(f"必需配置缺失：{full_key}")
        
        return value
    
    def get_int(self, key: str, default: int = 0, required: bool = False) -> int:
        """获取整数配置"""
        value = self.get(key, str(default), required)
        return int(value)
    
    def get_bool(self, key: str, default: bool = False, required: bool = False) -> bool:
        """获取布尔配置"""
        value = self.get(key, str(default).lower(), required)
        return value.lower() in ('true', '1', 'yes', 'on')

# ============================================================================
# 7. 数据库工具
# ============================================================================

class DatabaseMixin:
    """数据库工具混入类"""
    
    def __init__(self, db_path: str):
        """
        初始化数据库
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库（由子类实现）"""
        pass
    
    def execute(self, sql: str, params: tuple = ()) -> Any:
        """执行 SQL"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result
    
    def execute_many(self, sql: str, params_list: list) -> Any:
        """批量执行 SQL"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(sql, params_list)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result

# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # Token 管理器
    'FeishuTokenManager',
    
    # 日志配置
    'setup_logging',
    
    # 错误处理
    'FeishuError',
    'TokenError',
    'APIError',
    'PermissionError',
    'retry',
    'handle_api_errors',
    
    # 工具函数
    'verify_signature',
    'parse_time',
    'format_time',
    'get_timestamp',
    'timestamp_to_datetime',
    'batch_process',
    'safe_get',
    
    # 配置管理
    'Config',
    
    # 数据库工具
    'DatabaseMixin',
]
