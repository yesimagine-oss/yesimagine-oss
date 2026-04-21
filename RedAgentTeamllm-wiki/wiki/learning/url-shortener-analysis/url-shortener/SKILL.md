---
description: URL 短链接生成和管理技能。支持生成短链接、统计点击、管理链接列表。 当用户需要缩短 URL、追踪链接点击、批量管理短链接时触发。 示例："缩短这个链接""统计链接点击数""列出所有短链接"
name: url-shortener

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
# URL Shortener

## 概述
提供完整的 URL 短链接管理能力，包括生成、统计、列表和删除操作。
支持本地存储和多种短链接服务后端。

## 快速开始

### 生成短链接
```bash
uv run scripts/shorten.py https://example.com/very/long/url
# 输出：https://short.link/abc123
```

### 查看统计
```bash
uv run scripts/stats.py abc123
# 输出：点击数、来源、时间分布
```

### 列出所有链接
```bash
uv run scripts/list.py
# 输出：所有短链接及其统计
```

## 核心任务

### 1. 生成短链接

**基本用法**:
```bash
uv run scripts/shorten.py <长 URL>
```

**自定义别名**:
```bash
uv run scripts/shorten.py <长 URL> --alias my-custom-link
```

**批量生成**:
```bash
uv run scripts/shorten.py --batch urls.txt
```

**工作流程**:
1. 验证 URL 格式
2. 检查是否已存在
3. 生成短码（随机或自定义）
4. 存储映射关系到本地数据库
5. 返回短链接

### 2. 查看统计

**查看单个链接**:
```bash
uv run scripts/stats.py <短码>
```

**查看链接详情**:
```bash
uv run scripts/stats.py <短码> --detail
```

**统计信息包括**:
- 总点击数
- 独立访客数
- 来源分布（referrer）
- 时间分布（按日/周/月）
- 地理位置（如有）

### 3. 管理链接

**列出所有链接**:
```bash
uv run scripts/list.py
uv run scripts/list.py --limit 20
uv run scripts/list.py --sort clicks
```

**删除链接**:
```bash
uv run scripts/delete.py <短码>
uv run scripts/delete.py <短码> --confirm  # 跳过确认
```

**导出链接**:
```bash
uv run scripts/export.py --format json
uv run scripts/export.py --format csv -o links.csv
```

**生成 QR 码**:
```bash
uv run scripts/qr.py <短码>
uv run scripts/qr.py <短码> -o custom-qr.png
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SHORTENER_DB_PATH` | 数据库文件路径 | `~/.url-shortener/links.db` |
| `SHORTENER_DOMAIN` | 短链接域名 | `short.link` |
| `SHORTENER_CODE_LENGTH` | 短码长度 | `6` |

### 配置文件

在 `~/.url-shortener/config.json` 中配置:

```json
{
  "domain": "your-domain.com",
  "code_length": 6,
  "analytics": true,
  "track_referrer": true,
  "track_geo": false
}
```

## 数据模型

### 链接记录

```json
{
  "short_code": "abc123",
  "original_url": "https://example.com/long/url",
  "created_at": "2026-03-13T10:00:00Z",
  "clicks": 42,
  "unique_visitors": 35,
  "last_clicked": "2026-03-13T15:30:00Z"
}
```

### 点击记录

```json
{
  "short_code": "abc123",
  "clicked_at": "2026-03-13T15:30:00Z",
  "ip_hash": "hashed_ip",
  "referrer": "https://twitter.com",
  "user_agent": "Mozilla/5.0...",
  "country": "US"
}
```

## 脚本说明

### scripts/

| 脚本 | 功能 | 示例 |
|------|------|------|
| `shorten.py` | 生成短链接 | `uv run scripts/shorten.py <url>` |
| `list.py` | 列出链接 | `uv run scripts/list.py` |
| `stats.py` | 查看统计 | `uv run scripts/stats.py <code>` |
| `delete.py` | 删除链接 | `uv run scripts/delete.py <code>` |
| `export.py` | 导出数据 | `uv run scripts/export.py --format json` |
| `qr.py` | 生成 QR 码 | `uv run scripts/qr.py <code>` |

## API 使用（可选）

如果提供 HTTP API:

### 生成短链接
```bash
curl -X POST https://your-api.com/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 查看统计
```bash
curl https://your-api.com/stats/<short_code>
```

## 最佳实践

### 安全性
- 验证所有输入 URL
- 防止短码预测（使用足够长度）
- 对 IP 地址进行哈希处理
- 实施速率限制

### 性能
- 使用缓存加速热门链接
- 定期清理过期数据
- 索引数据库查询字段

### 隐私
- 不存储原始 IP 地址
- 提供匿名统计选项
- 遵守 GDPR 要求

## 故障排除

### 常见问题

**Q: 短链接无法访问？**
- 检查重定向服务是否运行
- 验证域名配置
- 查看服务器日志

**Q: 统计数据不准确？**
- 检查跟踪脚本是否加载
- 验证浏览器是否阻止跟踪
- 考虑广告拦截器影响

**Q: 数据库锁定？**
- 检查是否有其他进程访问
- 增加超时时间
- 考虑使用 WAL 模式

---

_提示：详细 API 参考见 `references/api-reference.md`_

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]
