---
category: feishu
created_at: '2026-04-20'
tags:
- feishu
- auto-generated
title: Readme
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
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


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
