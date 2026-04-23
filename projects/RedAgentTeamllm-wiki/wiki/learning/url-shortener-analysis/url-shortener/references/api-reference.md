---
category: llm
created_at: '2026-04-14'
tags:
- llm
- url
- shortener
- api
- reference
title: Api Reference
type: general
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
# URL Shortener API Reference

_详细 API 和脚本使用说明_

---

## 目录

1. [脚本命令](#1-脚本命令)
2. [数据库 Schema](#2-数据库-schema)
3. [配置选项](#3-配置选项)
4. [扩展开发](#4-扩展开发)

---

## 1. 脚本命令

### 1.1 shorten.py - 生成短链接

**基本用法**:
```bash
uv run scripts/shorten.py <url>
```

**参数**:
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 要缩短的 URL（必需，除非使用--batch） | - |
| `--alias, -a` | 自定义短码 | 随机生成 |
| `--batch, -b` | 批量处理文件 | - |
| `--quiet, -q` | 仅输出短链接 | false |

**示例**:
```bash
# 单个 URL
uv run scripts/shorten.py https://example.com/long/path

# 自定义别名
uv run scripts/shorten.py https://example.com --alias promo2026

# 批量处理
uv run scripts/shorten.py --batch urls.txt

# 静默模式（适合脚本）
uv run scripts/shorten.py https://example.com -q
```

### 1.2 list.py - 列出链接

**基本用法**:
```bash
uv run scripts/list.py
```

**参数**:
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--limit, -n` | 显示数量 | 50 |
| `--sort, -s` | 排序字段 (created_at/clicks/short_code) | created_at |
| `--json` | JSON 输出 | false |

**示例**:
```bash
# 列出最新 50 个
uv run scripts/list.py

# 按点击数排序
uv run scripts/list.py --sort clicks

# JSON 输出
uv run scripts/list.py --json | jq '.[].short_code'
```

### 1.3 stats.py - 查看统计

**基本用法**:
```bash
uv run scripts/stats.py <short_code>
```

**参数**:
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `short_code` | 短码（必需） | - |
| `--detail, -d` | 显示详细点击记录 | false |
| `--json` | JSON 输出 | false |

**示例**:
```bash
# 基本统计
uv run scripts/stats.py abc123

# 详细统计
uv run scripts/stats.py abc123 --detail

# JSON 输出
uv run scripts/stats.py abc123 --json
```

### 1.4 delete.py - 删除链接

**基本用法**:
```bash
uv run scripts/delete.py <short_code>
```

**参数**:
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `short_code` | 短码（必需） | - |
| `--confirm` | 跳过确认提示 | false |

**示例**:
```bash
# 删除链接（带确认）
uv run scripts/delete.py abc123

# 静默删除
uv run scripts/delete.py abc123 --confirm
```

### 1.5 export.py - 导出数据

**基本用法**:
```bash
uv run scripts/export.py
```

**参数**:
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--format, -f` | 输出格式 (csv/json) | json |
| `--output, -o` | 输出文件路径 | stdout |

**示例**:
```bash
# JSON 导出
uv run scripts/export.py --format json

# CSV 导出
uv run scripts/export.py --format csv -o links.csv
```

---

## 2. 数据库 Schema

### 2.1 links 表

存储短链接映射关系。

```sql
CREATE TABLE links (
    short_code TEXT PRIMARY KEY,      -- 短码（唯一）
    original_url TEXT NOT NULL,       -- 原始 URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    clicks INTEGER DEFAULT 0,         -- 点击总数
    last_clicked TIMESTAMP            -- 最后点击时间
);
```

**索引**:
```sql
CREATE INDEX idx_links_created ON links(created_at DESC);
CREATE INDEX idx_links_clicks ON links(clicks DESC);
```

### 2.2 clicks 表

存储点击记录（用于详细统计）。

```sql
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT NOT NULL,         -- 关联的短码
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 点击时间
    ip_hash TEXT,                     -- IP 地址哈希（隐私保护）
    referrer TEXT,                    -- 来源页面
    user_agent TEXT,                  -- 用户代理
    FOREIGN KEY (short_code) REFERENCES links(short_code)
);
```

**索引**:
```sql
CREATE INDEX idx_clicks_short_code ON clicks(short_code);
CREATE INDEX idx_clicks_time ON clicks(clicked_at DESC);
```

---

## 3. 配置选项

### 3.1 环境变量

| 变量 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `SHORTENER_DB_PATH` | 数据库文件路径 | `~/.url-shortener/links.db` | `/data/shortener.db` |
| `SHORTENER_DOMAIN` | 短链接域名 | `short.link` | `go.mycompany.com` |
| `SHORTENER_CODE_LENGTH` | 随机短码长度 | `6` | `8` |

### 3.2 配置文件

位置：`~/.url-shortener/config.json`

```json
{
  "domain": "go.mycompany.com",
  "code_length": 6,
  "analytics": {
    "enabled": true,
    "track_referrer": true,
    "track_user_agent": true,
    "track_geo": false
  },
  "security": {
    "rate_limit": 100,
    "rate_limit_window": 3600
  }
}
```

### 3.3 目录结构

```
~/.url-shortener/
├── links.db           # SQLite 数据库
├── config.json        # 配置文件
└── logs/              # 日志目录（可选）
    └── access.log
```

---

## 4. 扩展开发

### 4.1 添加新脚本

创建新脚本模板：

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
脚本说明

Usage:
    uv run scripts/your-script.py [options]
"""

import argparse
import sqlite3
from pathlib import Path
from rich.console import Console

console = Console()
DB_PATH = Path.home() / ".url-shortener" / "links.db"

def main():
    parser = argparse.ArgumentParser(description="脚本说明")
    # 添加参数...
    args = parser.parse_args()
    
    # 实现逻辑...

if __name__ == "__main__":
    main()
```

### 4.2 添加 HTTP API

使用 FastAPI 示例：

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class URLRequest(BaseModel):
    url: str
    alias: str = None

@app.post("/shorten")
async def shorten(req: URLRequest):
    # 调用 shorten_url 函数
    result = shorten_url(req.url, req.alias)
    return result

@app.get("/stats/{short_code}")
async def stats(short_code: str):
    # 调用 get_stats 函数
    return get_stats(short_code)
```

### 4.3 添加重定向服务

Nginx 配置示例：

```nginx
location ~ ^/([a-z0-9]+)$ {
    set $short_code $1;
    
    # 查询数据库获取原始 URL
    # 可以使用 Lua 或外部服务
    
    return 301 $original_url;
}
```

### 4.4 集成分析服务

```python
def track_click(short_code: str, request):
    """记录点击"""
    conn = get_db_connection()
    
    # 哈希 IP（隐私保护）
    import hashlib
    ip_hash = hashlib.sha256(request.client.host.encode()).hexdigest()[:16]
    
    conn.execute("""
        INSERT INTO clicks (short_code, ip_hash, referrer, user_agent)
        VALUES (?, ?, ?, ?)
    """, (
        short_code,
        ip_hash,
        request.headers.get("referer"),
        request.headers.get("user-agent")
    ))
    
    # 更新点击计数
    conn.execute("""
        UPDATE links 
        SET clicks = clicks + 1, last_clicked = CURRENT_TIMESTAMP
        WHERE short_code = ?
    """, (short_code,))
    
    conn.commit()
    conn.close()
```

---

## 5. 故障排除

### 常见问题

**Q1: 数据库锁定错误**
```
sqlite3.OperationalError: database is locked
```
**解决**: 
- 检查是否有其他进程访问
- 使用 WAL 模式：`PRAGMA journal_mode=WAL;`
- 增加超时：`conn.execute("PRAGMA busy_timeout=5000")`

**Q2: 短码冲突**
```
UNIQUE constraint failed: links.short_code
```
**解决**:
- 增加短码长度
- 使用更大的字符集
- 添加重试逻辑

**Q3: 性能问题**
**解决**:
- 添加适当索引
- 使用连接池
- 定期清理旧数据

---

_最后更新：2026-03-13_

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[asset07_api_batch_optimize]]
