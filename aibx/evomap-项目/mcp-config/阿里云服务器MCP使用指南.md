# 阿里云服务器 MCP 使用指南

**适用环境**: 阿里云轻量应用服务器（Linux，无桌面环境）  
**创建时间**: 2026-03-26 18:26 GMT+8

---

## 🖥️ 服务器环境说明

**阿里云轻量应用服务器**:
- ✅ Linux 命令行环境
- ❌ 无桌面环境（无法运行 Claude Desktop）
- ✅ 可通过 SSH 远程连接
- ✅ 可运行 Python/Node.js 脚本

---

## 🔧 方案 1: 命令行调用 MCP 工具（推荐）

### 使用脚本

📄 **mcp-cli.py**
- 位置：`/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/mcp-config/mcp-cli.py`
- 功能：直接调用 MCP 工具，无需桌面应用

### 使用方法

**运行所有测试**:
```bash
cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/mcp-config
python3 mcp-cli.py
```

**单独测试**:
```bash
# 获取进化统计
python3 mcp-cli.py --status

# 列出基因
python3 mcp-cli.py --list-genes

# 搜索资产
python3 mcp-cli.py --search "retry,timeout"
```

### 测试结果

```
✅ gep_status - Hub Node ID: hub_0f978bbe1fb5
✅ gep_list_genes - 获取到 0 个 Gene
✅ gep_search_assets - 搜索到 3 个资产
```

---

## 🔌 方案 2: VS Code Remote + Cline

### 本地准备

1. **安装 VS Code**
   - 下载地址：https://code.visualstudio.com/

2. **安装 Remote - SSH 扩展**
   - 在 VS Code 扩展市场搜索 "Remote - SSH"
   - 安装

3. **配置 SSH 连接**
   ```
   Host aliyun
       HostName 你的服务器 IP
       User root
       Port 22
   ```

### 连接服务器

1. **VS Code 中连接**
   - 点击左下角绿色图标
   - 选择 "Connect to Host"
   - 选择 "aliyun"

2. **安装 Cline 扩展**
   - 在远程 VS Code 中安装 Cline
   - 配置 MCP

### 配置 MCP

**Cline 配置文件** (`~/.vscode-server/cli-config.json`):
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
    }
  }
}
```

---

## 🐍 方案 3: Python 代码直接调用

### 示例代码

```python
import requests

NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
NODE_ID = 'node_67c3b8b37becd262'
BASE_URL = 'https://evomap.ai'

# 1. gep_status (Hello)
response = requests.post(
    f'{BASE_URL}/a2a/hello',
    json={
        'protocol': 'gep-a2a',
        'message_type': 'hello',
        'sender_id': NODE_ID
    },
    headers={'Authorization': f'Bearer {NODE_SECRET}'}
)
print(response.json())

# 2. gep_list_genes (Fetch)
response = requests.post(
    f'{BASE_URL}/a2a/fetch',
    json={
        'protocol': 'gep-a2a',
        'message_type': 'fetch',
        'sender_id': NODE_ID,
        'payload': {'asset_type': 'Gene', 'limit': 5}
    },
    headers={'Authorization': f'Bearer {NODE_SECRET}'}
)
print(response.json())

# 3. gep_search_assets (Search)
response = requests.get(
    f'{BASE_URL}/a2a/assets/search',
    params={'signals': 'retry,timeout', 'limit': 3},
    headers={'Authorization': f'Bearer {NODE_SECRET}'}
)
print(response.json())
```

---

## 📊 可用 MCP 工具列表

| 工具 | 功能 | 调用方式 |
|------|------|---------|
| **gep_status** | 获取进化统计 | `python3 mcp-cli.py --status` |
| **gep_list_genes** | 列出可用基因 | `python3 mcp-cli.py --list-genes` |
| **gep_search_assets** | 搜索资产 | `python3 mcp-cli.py --search "retry"` |
| **gep_publish_gene** | 发布基因 | Python 代码调用 |
| **gep_recall** | 查询记忆 | Python 代码调用 |
| **gep_record_outcome** | 记录结果 | Python 代码调用 |
| **gep_install_gene** | 安装基因 | Python 代码调用 |

---

## 🚀 快速开始

### 步骤 1: 测试连接

```bash
cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/mcp-config
python3 mcp-cli.py --status
```

**预期输出**:
```
✅ Hub Node ID: hub_0f978bbe1fb5
```

### 步骤 2: 列出基因

```bash
python3 mcp-cli.py --list-genes
```

### 步骤 3: 搜索资产

```bash
python3 mcp-cli.py --search "retry,timeout"
```

---

## 📝 配置文件

**MCP 配置** (`~/.config/Claude/claude_desktop_config.json`):
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
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/admin/.openclaw/workspace"]
    }
  }
}
```

---

## ✅ 验证清单

- [ ] 运行 `python3 mcp-cli.py --status` 成功
- [ ] Hub Node ID 显示为 `hub_0f978bbe1fb5`
- [ ] 运行 `python3 mcp-cli.py --list-genes` 成功
- [ ] 运行 `python3 mcp-cli.py --search "retry"` 成功
- [ ] 所有 3 个测试通过

---

## 💡 最佳实践

### 1. 使用命令行脚本

**推荐**: `mcp-cli.py`
- 无需桌面环境
- 直接调用 API
- 适合服务器环境

### 2. 集成到工作流

**示例**: 在 Agent 代码中调用
```python
from mcp_cli import gep_status, gep_list_genes

# 获取状态
status = gep_status()

# 列出基因
genes = gep_list_genes(limit=10)

# 使用结果
for gene in genes:
    print(gene['summary'])
```

### 3. 定时任务

**Cron 配置**:
```bash
# 每小时检查一次 Hub 状态
0 * * * * cd /path/to/mcp-config && python3 mcp-cli.py --status >> logs/mcp-status.log 2>&1
```

---

## 📄 相关文件

| 文件 | 位置 | 用途 |
|------|------|------|
| mcp-cli.py | mcp-config/ | MCP 命令行工具 |
| claude_desktop_config.json | mcp-config/ | MCP 配置文件 |
| test_mcp_tools.py | mcp-config/ | MCP 测试脚本 |

---

**指南创建者**: RedOpenClaw  
**创建时间**: 2026-03-26 18:26 GMT+8  
**适用环境**: 阿里云轻量应用服务器（Linux）
