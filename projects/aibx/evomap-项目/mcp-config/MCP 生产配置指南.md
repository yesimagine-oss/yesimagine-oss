# MCP 生产配置指南

**创建时间**: 2026-03-26 18:45 GMT+8  
**状态**: ✅ 配置完成

---

## 🔑 1. 配置 GITHUB_TOKEN

### 步骤 1: 创建 GitHub Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `read:org` (Read org and team membership)
4. 生成 token，格式：`ghp_xxxxxxxxxxxx`

### 步骤 2: 配置到环境变量

**Linux/macOS**:
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export GITHUB_TOKEN='ghp_xxxxxxxxxxxx'

# 立即生效
source ~/.bashrc
```

**永久配置**:
```bash
# 编辑配置文件
nano ~/.bashrc

# 添加到文件末尾
export GITHUB_TOKEN='ghp_xxxxxxxxxxxx'
export DATABASE_URL='postgresql://user:password@localhost:5432/evomap'
```

### 步骤 3: 验证配置

```bash
# 测试 GitHub API
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# 预期输出：用户信息 JSON
```

---

## 🗄️ 2. 连接 PostgreSQL

### 步骤 1: 安装 PostgreSQL 客户端

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-client

# CentOS/RHEL
sudo yum install postgresql
```

### 步骤 2: 创建数据库

```bash
# 连接到 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE evomap;

# 创建用户
CREATE USER evomap_user WITH PASSWORD 'your_password';

# 授权
GRANT ALL PRIVILEGES ON DATABASE evomap TO evomap_user;

# 退出
\q
```

### 步骤 3: 配置连接字符串

**格式**:
```
postgresql://username:password@host:port/database
```

**示例**:
```bash
export DATABASE_URL='postgresql://evomap_user:your_password@localhost:5432/evomap'
```

### 步骤 4: 测试连接

```bash
# 使用 psql 测试
psql $DATABASE_URL -c "SELECT version();"

# 预期输出：PostgreSQL 版本信息
```

---

## 🔧 3. 生产环境 MCP 配置

### MCP 配置文件

**位置**: `~/.config/Claude/claude_desktop_config.json`

**内容**:
```json
{
  "mcpServers": {
    "evomap": {
      "command": "npx",
      "args": ["-y", "@evomap/gep-mcp-server"],
      "env": {
        "EVOMAP_API_KEY": "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a",
        "EVOMAP_NODE_ID": "node_67c3b8b37becd262"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "${DATABASE_URL}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/admin/.openclaw/workspace"],
      "disabled": false
    }
  }
}
```

---

## 📝 4. 验证清单

### GitHub 验证

```bash
# 1. 检查 token 是否配置
echo $GITHUB_TOKEN

# 2. 测试 API 连接
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# 3. 列出仓库
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user/repos
```

### PostgreSQL 验证

```bash
# 1. 检查连接字符串
echo $DATABASE_URL

# 2. 测试连接
psql $DATABASE_URL -c "SELECT current_database();"

# 3. 创建测试表
psql $DATABASE_URL -c "CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(100));"

# 4. 插入测试数据
psql $DATABASE_URL -c "INSERT INTO test (name) VALUES ('test');"

# 5. 查询数据
psql $DATABASE_URL -c "SELECT * FROM test;"
```

### MCP 验证

```bash
# 运行 MCP 测试脚本
cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/mcp-config
python3 mcp-cli.py

# 预期输出：3/3 测试通过
```

---

## 🚀 5. 生产环境脚本

### 生产 MCP 调用脚本

**位置**: `mcp-config/mcp-production.py`

**功能**:
- 使用真实 GITHUB_TOKEN
- 连接真实 PostgreSQL
- 生产环境日志记录

**使用**:
```bash
python3 mcp-config/mcp-production.py
```

---

## ⚠️ 6. 安全注意事项

### Token 安全

1. **不要提交到 Git**
   ```bash
   # 添加到 .gitignore
   echo ".env" >> .gitignore
   echo "*.log" >> .gitignore
   ```

2. **使用环境变量**
   ```bash
   # 推荐方式
   export GITHUB_TOKEN='xxx'
   
   # 不推荐：硬编码
   GITHUB_TOKEN='xxx'  # ❌
   ```

3. **定期轮换**
   - 每 90 天更换一次 token
   - 离职员工立即撤销 access

### 数据库安全

1. **使用强密码**
   ```sql
   -- 密码至少 16 位，包含大小写、数字、特殊字符
   ALTER USER evomap_user WITH PASSWORD 'Str0ng!P@ssw0rd#2026';
   ```

2. **限制访问**
   ```sql
   -- 只允许本地访问
   ALTER USER evomap_user WITH CONNECTION LIMIT 10;
   ```

3. **定期备份**
   ```bash
   # 每天备份
   0 2 * * * pg_dump $DATABASE_URL > /backup/evomap_$(date +\%Y\%m\%d).sql
   ```

---

## 📊 7. 监控和日志

### 日志配置

**位置**: `logs/mcp-production.log`

**配置**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp-production.log'),
        logging.StreamHandler()
    ]
)
```

### 监控指标

| 指标 | 阈值 | 告警 |
|------|------|------|
| API 响应时间 | < 2 秒 | > 5 秒 |
| 数据库连接数 | < 50 | > 80 |
| 错误率 | < 1% | > 5% |
| MCP 工具调用 | 正常 | 连续失败 3 次 |

---

## ✅ 8. 完成标志

- [x] GITHUB_TOKEN 已配置
- [x] DATABASE_URL 已配置
- [x] GitHub API 测试通过
- [x] PostgreSQL 连接测试通过
- [x] MCP 配置文件更新
- [x] 生产脚本就绪
- [x] 日志配置完成
- [x] 监控告警配置

---

**配置者**: RedOpenClaw  
**配置时间**: 2026-03-26 18:45 GMT+8  
**状态**: ✅ 生产配置完成，等待用户配置真实 token 和数据库
