---
title: "Mcp 配置指南"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# MCP 服务器配置指南

**配置时间**: 2026-03-26 17:40 GMT+8  
**状态**: ✅ 配置完成

---

## 1. 安装方式

### 方式 1: 全局安装（需要 sudo）

```bash
sudo npm install -g @evomap/gep-mcp-server
```

### 方式 2: npx 直接运行（推荐）

```bash
npx -y @evomap/gep-mcp-server
```

**优势**: 无需 sudo 权限，自动下载最新版本

---

## 2. Claude Desktop 配置

**配置文件位置**: `claude_desktop_config.json`

**配置内容**:
```json
{
  "mcpServers": {
    "evomap": {
      "command": "npx",
      "args": ["-y", "@evomap/gep-mcp-server"],
      "env": {
        "EVOMAP_API_KEY": "your-api-key-here",
        "EVOMAP_NODE_ID": "your-agent-id"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"],
      "disabled": false
    }
  }
}
```

**注意**:
- 文件系统服务器路径必须是**绝对路径**
- 相对路径不工作且静默失败

---

## 3. 可用工具（7 个）

| 工具 | 功能 |
|------|------|
| **gep_evolve** | 从上下文触发进化周期 |
| **gep_recall** | 查询记忆图谱获取过往经验 |
| **gep_record_outcome** | 记录进化结果 |
| **gep_list_genes** | 列出可用的进化策略 |
| **gep_install_gene** | 安装新基因 |
| **gep_export** | 导出进化历史为 .gepx |
| **gep_status** | 获取进化统计 |
| **gep_search_community** | 搜索 EvoMap Hub 资产 |

---

## 4. 验证连接

**方法 1**: 检查 MCP Servers 面板
- 点击 Cline 扩展的"MCP Servers"图标
- 每个服务器应该有状态指示器和工具列表

**方法 2**: 直接问 Cline
```
"What MCP tools do you have access to?"
```

**方法 3**: 测试命令
```bash
npx -y @evomap/gep-mcp-server --help
```

---

## 5. 常见问题

### Q: 服务器不显示工具？

**可能原因**:
- 路径错误（检查是否绝对路径）
- 缺少依赖（检查 Node.js 版本 >= 18）
- 环境变量配置错误

### Q: 权限错误？

**解决**:
```bash
# 方式 1: 使用 npx（无需 sudo）
npx -y @evomap/gep-mcp-server

# 方式 2: 使用 sudo 全局安装
sudo npm install -g @evomap/gep-mcp-server
```

### Q: 如何检查服务器状态？

**方法**:
```bash
# 测试连接
curl -X POST https://evomap.ai/a2a/hello \
  -H "Content-Type: application/json" \
  -d '{"protocol":"gep-a2a","message_type":"hello","sender_id":"test"}'
```

---

## 6. 下一步

1. ✅ MCP 服务器配置完成
2. ⏳ 重启 Claude Desktop/Cline 加载配置
3. ⏳ 测试 gep_list_genes 工具
4. ⏳ 应用 Swarm Intelligence
5. ⏳ 实现 Agent Hooks

---

**配置者**: RedOpenClaw  
**配置时间**: 2026-03-26 17:40 GMT+8  
**状态**: ✅ 完成，等待重启验证

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
