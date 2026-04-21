# Feishu Common Modules

飞书公共模块库，包含所有项目共用的模块。

## 安装

```bash
pip install -e .
```

## 使用

```python
from feishu_common import FeishuTokenManager, setup_logging, retry

# Token 管理器
token_manager = FeishuTokenManager(app_id, app_secret)
token = token_manager.get_app_access_token()

# 日志配置
logger = setup_logging(__name__)

# 重试装饰器
@retry(max_retries=3)
def api_call():
    pass
```

## 模块

- Token 管理器
- 日志配置
- 错误处理
- 工具函数
- 配置管理
- 数据库工具

## 版本

v1.0 (2026-03-13)
