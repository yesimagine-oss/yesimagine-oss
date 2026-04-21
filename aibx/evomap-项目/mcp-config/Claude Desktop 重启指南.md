# Claude Desktop 重启指南

**创建时间**: 2026-03-26 18:15 GMT+8  
**状态**: ✅ 指南完成

---

## 🖥️ 为什么需要本地重启

**Claude Desktop 是桌面应用**，运行在您的本地机器上（Mac/Windows），而不是服务器上。

**服务器限制**:
- ❌ 无法访问本地桌面应用
- ❌ 无法重启本地进程
- ✅ 可以创建配置文件

---

## 📋 重启步骤

### 步骤 1: 复制配置文件

**源文件**:
```
/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/mcp-config/claude_desktop_config.json
```

**目标位置**:

**macOS**:
```bash
cp /path/to/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```powershell
Copy-Item "C:\path\to\claude_desktop_config.json" "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Linux**:
```bash
cp /path/to/claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json
```

---

### 步骤 2: 重启 Claude Desktop

**方法 1: 完全重启**
1. 关闭 Claude Desktop 应用
2. 等待 5 秒
3. 重新打开 Claude Desktop

**方法 2: 重新加载配置**
- 某些版本支持 Command+R (Mac) 或 Ctrl+R (Windows) 重新加载配置

---

### 步骤 3: 验证 MCP 配置

**验证命令**:
在 Claude Desktop 对话框中输入：
```
What MCP tools do you have access to?
```

**预期响应**:
```
I have access to the following MCP tools:
- evomap: gep_evolve, gep_recall, gep_list_genes, ...
- filesystem: read_file, write_file, list_directory, ...
```

---

## 🔧 故障排查

### 问题 1: 配置不生效

**可能原因**:
- 配置文件路径错误
- JSON 格式错误
- 权限问题

**解决方案**:
```bash
# 检查文件是否存在
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 验证 JSON 格式
cat claude_desktop_config.json | python3 -m json.tool
```

### 问题 2: MCP 工具不显示

**可能原因**:
- Node.js 版本过低（需要 >= 18）
- npx 无法下载
- 网络问题

**解决方案**:
```bash
# 检查 Node.js 版本
node --version

# 手动测试 npx
npx -y @evomap/gep-mcp-server --help
```

### 问题 3: 权限错误

**macOS**:
```bash
chmod 644 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```powershell
icacls "$env:APPDATA\Claude\claude_desktop_config.json" /grant Users:R
```

---

## 📝 配置文件内容

**当前配置**:
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
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/admin/.openclaw/workspace"],
      "disabled": false
    }
  }
}
```

**注意**:
- 文件系统路径需要修改为您的实际工作目录
- API Key 和 Node ID 已配置好

---

## ✅ 验证清单

重启后，请验证以下项目：

- [ ] Claude Desktop 成功启动
- [ ] MCP Servers 面板显示 2 个服务器
- [ ] evomap 服务器状态为绿色
- [ ] filesystem 服务器状态为绿色
- [ ] 可以调用 gep_list_genes 工具
- [ ] 可以读取工作目录文件

---

## 🚀 下一步

重启并验证后：

1. **测试 MCP 工具**
   ```
   请列出所有可用的进化策略
   ```

2. **集成 Hooks**
   - 使用 HookManager 装饰 Agent
   - 配置日志和重试

3. **应用 Swarm Intelligence**
   - 选择复杂任务
   - 使用 Diverge-Converge 模式

---

**指南创建者**: RedOpenClaw  
**创建时间**: 2026-03-26 18:15 GMT+8  
**状态**: ✅ 完成，等待用户本地操作
