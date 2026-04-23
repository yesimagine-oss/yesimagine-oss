# goEX 项目规划（AI 辅助版）

**创建时间**: 2026-04-16 00:44 GMT+8  
**开发方式**: 资产包 + AI 辅助生成  
**总工时**: **18h**（相比传统版节省 38%）

---

## 一、开发时间评估

| 阶段 | 功能 | 数量 | 时间 | 节省 |
|------|------|------|------|------|
| **Phase 1** | 基础 12 项 + 飞书 + 自然语言 + hermes API + 插件库 + 快捷配置 | 17 项 | **7h** | -4h |
| **Phase 2** | AI 智能填充/智能重试 | 2 项 | **3h** | -2h |
| **Phase 3** | 采集 4 项 + Session + 会话恢复 | 6 项 | **3h** | -2h |
| **Phase 4** | 插件系统 6 项 | 6 项 | **5h** | -3h |
| **总计** | 31 项功能 | **18h** | **-11h** |

---

## 二、Phase 1 详情（7h）

| 功能 | 资产包参考 | AI 辅助方式 | 时间 |
|------|------------|-------------|------|
| 导航/定位/点击/截图 | chromedp v0.15.1 Capsules | Capsules 复制+AI 生成样板 | 1h |
| HTML 解析/JS 执行 | chromedp pkg.go.dev Capsules | AI 生成封装函数 | 0.5h |
| 等待/Cookie/多标签页 | chromedp v0.15.1 Capsules | Capsules 复制+AI 适配 | 0.5h |
| 网页爬取/运行日志 | developer.chrome.com + Effective Go | AI 生成模板代码 | 0.5h |
| 截图增强 | chromedp v0.15.1 Capsules | 手动优化 | 0.5h |
| 飞书推送 | Feishu API | AI 生成集成代码 | 0.5h |
| 自然语言 | GeminiCLI Capsules | Capsules 复用+AI 适配 | 0.5h |
| hermes HTTP API | Gin 框架 | AI 生成骨架+手动完善 | 1h |
| 插件库管理 | Go plugin | Go plugin 标准接口 | 0.5h |
| 快捷方式配置 | config.yaml | AI 生成 YAML 模板 | 0.5h |
| 插件 Interface | Go plugin | Go interface 定义 | 0.5h |
| 测试验证 | - | AI 生成测试用例 | 0.5h |

---

## 三、Phase 2 详情（3h）

| 功能 | 资产包参考 | AI 辅助方式 | 时间 |
|------|------------|-------------|------|
| AI 智能填充 | Gemini API Capsules | AI 生成 API 封装 | 2h |
| 智能重试 | chromedp v0.15.1 | AI 生成重试逻辑 | 1h |

---

## 四、Phase 3 详情（3h）

| 功能 | 资产包参考 | AI 辅助方式 | 时间 |
|------|------------|-------------|------|
| 微信文章爬取 | WeChat 爬虫资产 | AI 生成爬虫框架 | 1h |
| 批量采集 | chromedp v0.15.1 | AI 生成并发控制 | 0.5h |
| 性能优化 | Effective Go | AI 分析+建议 | 0.5h |
| 内容提取 | goquery | AI 生成选择器 | 0.5h |
| Session 管理 | chromedp pkg.go.dev | Capsules 复用 | 0.25h |
| 会话保存恢复 | 自定义 | AI 生成序列化代码 | 0.25h |

---

## 五、Phase 4 详情（5h）

| 功能 | 资产包参考 | AI 辅助方式 | 时间 |
|------|------------|-------------|------|
| 自动化录制 | 自定义 | AI 生成事件监听 | 1h |
| 数据导出 | 自定义 | AI 生成导出格式 | 1h |
| 代理管理 | 自定义 | AI 生成代理切换 | 1h |
| 定时任务 | 自定义 | AI 生成调度器 | 0.5h |
| 验证码处理 | 预留接口 | 接口定义+第三方集成 | 0.75h |
| 通知插件 | 自定义 | AI 生成通知模板 | 0.75h |

---

## 六、技术架构

```
┌─────────────────────────────────────────────────┐
│  hermes-agent  │  用户  │  其他 Agent           │
└────────────────────┬────────────────────────────┘
                     │ HTTP API
┌────────────────────▼────────────────────────────┐
│                   goEX Core                     │
│  ┌───────────┬───────────┬───────────────────┐  │
│  │ chromedp  │  Gin API  │   插件接口        │  │
│  │ v0.15.1   │  (Phase1) │   (Phase4)        │  │
│  └───────────┴───────────┴───────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  插件库 (~/.goex/plugins/)               │  │
│  │  配置文件 (config.yaml + 快捷方式)        │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 七、目录结构

```
~/.goex/
├── config.yaml          # 配置文件（含快捷方式）
├── plugins/             # 插件目录
│   ├── recorder/        # 录制插件
│   ├── exporter/        # 导出插件
│   └── ...
└── sessions/            # 会话数据
```

**config.yaml 示例：**
```yaml
shortcuts:
  wechat: "navigate https://mp.weixin.qq.com && screenshot"
  login: "navigate https://example.com && click #login"

server:
  port: 8080
  token: ""  # 可选认证

plugins:
  enabled:
    - recorder
    - exporter
```

---

## 八、多平台支持

| 平台 | 交付物 | 安装命令 |
|------|--------|----------|
| **Linux** | `goex` | `./goex` |
| **macOS** | `goex` | `./goex` |
| **Windows** | `goex.exe` | `goex.exe` |

**自动安装脚本：**
```bash
#!/bin/bash
# install.sh
set -e

ARCH=$(uname -m)
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

DOWNLOAD_URL="https://github.com/goex/goex/releases/latest/download/goex-${OS}-${ARCH}"

curl -L "$DOWNLOAD_URL" -o /usr/local/bin/goex
chmod +x /usr/local/bin/goex

mkdir -p ~/.goex/plugins
mkdir -p ~/.goex/sessions

echo "✅ goEX installed successfully!"
echo "Run 'goex --help' for usage."
```

---

## 九、交付物

| 类型 | 文件 | 说明 |
|------|------|------|
| **主体** | `goex` / `goex.exe` | 1 个二进制文件 |
| **安装脚本** | `install.sh` | 自动安装 |
| **配置** | `config.yaml` | 可选（有默认） |
| **数据** | `~/.goex/` | 自动创建 |
| **文档** | `README.md` | AI 生成初稿+人工完善 |
| **API 文档** | `API.md` | AI 生成 OpenAPI 规范 |

**用户感知：1 个文件，下载即用**

---

## 十、hermes-agent 集成

| 项目 | 方案 |
|------|------|
| **接口** | HTTP API（内置） |
| **调用** | `POST http://localhost:8080/navigate` |
| **成本** | +1h（Phase 1 内） |
| **重构风险** | 无（设计时考虑） |
| **插件兼容** | ✅ 后续插件自动兼容 |
| **向下兼容** | ✅ 是 |

**API 示例：**
```bash
# 导航
curl -X POST http://localhost:8080/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 点击
curl -X POST http://localhost:8080/click \
  -H "Content-Type: application/json" \
  -d '{"selector": "#login"}'

# 截图
curl -X GET http://localhost:8080/screenshot \
  -o screenshot.png

# 使用快捷方式
curl -X POST http://localhost:8080/shortcut/wechat
```

---

## 十一、AI 辅助详细说明

### 1. 代码复用（-6h）

| 资产包 | 可复用内容 | 节省 |
|--------|------------|------|
| chromedp v0.15.1 Capsules | 导航/点击/截图/JS 执行代码 | -2h |
| chromedp pkg.go.dev Capsules | Cookie 管理/等待封装 | -1h |
| Gin 框架示例 | HTTP API 骨架代码 | -1h |
| Feishu API 集成 | 飞书推送完整代码 | -1h |
| GeminiCLI Capsules | 自然语言处理封装 | -1h |

### 2. AI 辅助生成（-4h）

| 场景 | AI 生成内容 | 节省 |
|------|------------|------|
| 样板代码 | struct/interface/错误处理 | -1h |
| 封装函数 | chromedp 操作封装 | -1h |
| 测试用例 | 单元测试/集成测试 | -1h |
| 文档 | README/API 文档/注释 | -1h |

### 3. 测试策略优化（-3h）

| 策略 | 说明 | 节省 |
|------|------|------|
| 集成测试优先 | 直接测 HTTP API，跳过 Mock | -2h |
| 单元测试后置 | 稳定后再补充 | -1h |

### 4. 并行开发（-2h）

| 模块 | 可并行 | 说明 |
|------|--------|------|
| 核心功能 | Phase 1 | 串行 |
| HTTP API | Phase 1 | 与核心并行 |
| 飞书推送 | Phase 1 | 独立模块 |
| 自然语言 | Phase 1 | 独立模块 |

### 5. 开发环境优化（-1h）

| 优化 | 说明 | 节省 |
|------|------|------|
| goproxy.cn | 模块下载加速 | -0.5h |
| air 热重载 | 自动编译重启 | -0.5h |

---

## 十二、稳定性保障

| 措施 | 说明 |
|------|------|
| **资产包兜底** | AI 按资产包规范生成，有参考 |
| **集成测试** | 每个 Phase 完成后验证 |
| **代码审查** | AI 生成代码需人工审查 |
| **注释规范** | AI 生成代码必须带注释 |
| **文档同步** | AI 生成文档+人工完善 |

---

## 十三、风险评估

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| 代码 Bug | 低 | 集成测试验证 |
| 风格不一致 | 低 | AI 按资产包规范生成 |
| 理解困难 | 低 | 添加详细注释 |
| 依赖风险 | 无 | 资产包已验证 |
| 延期风险 | 低 | 40% 时间缓冲 |
| 技术短板 | 无 | 全部有资产包 |

---

## 十四、核心结论

| 问题 | 答案 |
|------|------|
| 开发时间 | **18h**（资产包+AI） |
| 技术短板 | 无（全部有资产包） |
| 多平台 | ✅ 原生支持 |
| hermes 集成 | ✅ Phase 1 完成 |
| 插件库管理 | ✅ Phase 1 完成 |
| 快捷方式 | ✅ Phase 1 完成 |
| 交付物 | ✅ 1 个二进制文件 |
| 安装方式 | ✅ 1 个命令 |
| 效率提升 | 38%（29h → 18h） |
| 稳定性 | ✅ 高（资产包兜底） |
| 风险 | ✅ 低（集成测试验证） |

---

## 十五、启动条件

| 条件 | 状态 |
|------|------|
| Go 1.26+ | ✅ 已安装 (go1.26.1) |
| chromedp v0.15.1 | ✅ 已安装 |
| Clash 代理 | ✅ 正常运行 (127.0.0.1:7890) |
| 知识库 | ✅ 43 个文件 |
| hermes-agent | ✅ 设计时考虑 |

**建议：立即启动 Phase 1**

---

## 十六、与传统版对比

| 维度 | 传统手工 | 资产包+AI | 说明 |
|------|----------|-----------|------|
| **开发时间** | 29h | **18h** | 节省 38% |
| **代码质量** | 高 | **高** | 资产包兜底 |
| **稳定性** | 高 | **高** | 集成测试验证 |
| **风险** | 低 | **低** | 可控 |
| **维护成本** | 低 | **中等** | 需文档 |
| **综合评分** | 85/100 | **90/100** | 推荐 AI 辅助 |

---

## 十七、重要决策记录

| 决策 | 说明 |
|------|------|
| 开发方式 | 资产包+AI 辅助（18h） |
| hermes-agent | Phase 1 开始就考虑（轻量级接口设计） |
| 插件库管理 | Phase 1 完成（简单版，~/.goex/plugins/） |
| 快捷方式 | Phase 1 完成（config.yaml 定义） |
| Chrome 式 UI | ❌ goEX 无图形界面（配置式实现） |
| 多平台分发 | 二进制文件为主，Docker 备用 |
| 测试策略 | 集成测试优先，单元测试后置 |

---

**Red AgentTeam | 2026-04-16 00:44 GMT+8**
