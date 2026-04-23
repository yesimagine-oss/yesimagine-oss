# OpenClaw Hostinger 安装完整指南

**来源:** https://docs.openclaw.ai/install/hostinger  
**收录时间:** 2026-04-23 13:52 GMT+8  
**状态:** ✅ 完整 (可用于实际安装)  

---

## 📋 前置要求

| 项目 | 要求 | 说明 |
|------|------|------|
| **Hostinger 账户** | ✅ 必需 | [注册链接](https://hostinger.com) |
| **预计时间** | 5-10 分钟 | 1-Click 部署 |
| **技术门槛** | 🟢 低 | 无需命令行经验 |

---

## 🚀 两种安装方式

### 方式 A: 1-Click OpenClaw (推荐)

**适用场景:** 快速部署，无需管理服务器

| 特点 | 说明 |
|------|------|
| **基础设施** | Hostinger 托管 |
| **Docker 管理** | 自动处理 |
| **更新** | 自动更新 |
| **技术门槛** | 零配置 |

#### 安装步骤

**步骤 1: 购买并启动**

1. 访问 [Hostinger OpenClaw 页面](https://hostinger.com/openclaw)
2. 选择 Managed OpenClaw 计划
3. 完成结账

<Note>
**Ready-to-Use AI 积分选项:**
- ✅ 预购买积分，立即可用
- ✅ 无需外部 API 密钥
- ✅ 可立即开始聊天
- ❌ 或可自行提供 Anthropic/OpenAI/Google/xAI 密钥
</Note>

**步骤 2: 选择消息渠道**

| 渠道 | 配置方法 |
|------|----------|
| **WhatsApp** | 扫描设置向导中的二维码 |
| **Telegram** | 粘贴 BotFather 的机器人令牌 |

**步骤 3: 完成安装**

1. 点击 **Finish** 部署实例
2. 等待实例就绪
3. 从 hPanel 的 **OpenClaw Overview** 访问仪表盘

---

### 方式 B: OpenClaw on VPS

**适用场景:** 需要更多控制权

| 特点 | 说明 |
|------|------|
| **服务器** | Hostinger VPS |
| **管理方式** | Docker Manager (hPanel) |
| **灵活性** | 完全控制 |
| **技术门槛** | 中等 |

#### 安装步骤

**步骤 1: 购买 VPS**

1. 访问 [Hostinger OpenClaw 页面](https://hostinger.com/openclaw)
2. 选择 OpenClaw on VPS 计划
3. 完成结账

**步骤 2: 配置 OpenClaw**

VPS 配置完成后，填写以下字段：

| 配置项 | 说明 | 必需 |
|--------|------|------|
| **Gateway token** | 自动生成，保存备用 | ✅ |
| **WhatsApp number** | 带国家代码的号码 | ❌ |
| **Telegram bot token** | 来自 BotFather | ❌ |
| **API keys** | 未选择 AI 积分时需要 | ❌ |

**步骤 3: 启动 OpenClaw**

1. 点击 **Deploy**
2. 等待运行
3. 从 hPanel 点击 **Open** 访问仪表盘

---

## 🛠️ 管理操作

### 查看日志

```
hPanel → Docker Manager → Logs
```

### 重启容器

```
hPanel → Docker Manager → Restart
```

### 更新 OpenClaw

```
hPanel → Docker Manager → Update
```

**说明:** 点击 **Update** 自动拉取最新镜像

---

## ✅ 验证安装

**测试方法:**

1. 发送 "Hi" 到已连接的渠道
2. OpenClaw 应回复并引导初始设置

**验证命令:**

```bash
# 本地安装验证 (如适用)
openclaw --version
openclaw doctor
openclaw gateway status
```

---

## 🔧 常见问题排障

### 问题 1: 仪表盘无法加载

| 项目 | 内容 |
|------|------|
| **现象** | 访问仪表盘页面超时或空白 |
| **原因** | 容器正在配置中 |
| **解决** | 等待几分钟，检查 Docker Manager 日志 |

**步骤:**
```
1. 等待 2-5 分钟
2. hPanel → Docker Manager → Logs
3. 查看是否有错误
```

---

### 问题 2: Docker 容器持续重启

| 项目 | 内容 |
|------|------|
| **现象** | 容器启动后立即停止，循环重启 |
| **原因** | 配置错误 (缺失令牌、无效 API 密钥) |
| **解决** | 检查配置项 |

**步骤:**
```
1. hPanel → Docker Manager → Logs
2. 查找配置错误
3. 修复缺失的 tokens 或 API keys
4. 重启容器
```

---

### 问题 3: Telegram 机器人无响应

| 项目 | 内容 |
|------|------|
| **现象** | 发送消息到 Telegram 机器人无回复 |
| **原因** | 配对未完成 |
| **解决** | 在 OpenClaw 聊天中发送配对码 |

**步骤:**
```
1. 获取配对码 (从 OpenClaw 仪表盘)
2. 在 Telegram 中直接发送配对码
3. 等待确认回复
```

---

## 📊 配置参考

### 1-Click 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| **Gateway token** | 自动生成 | 用于 API 访问 |
| **WhatsApp** | 可选 | 扫描二维码连接 |
| **Telegram** | 可选 | 粘贴 Bot 令牌 |
| **AI 积分** | 可选 | 预购买或自行提供密钥 |

### VPS 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| **Gateway token** | 自动生成 | 保存备用 |
| **WhatsApp number** | 空 | 带国家代码 |
| **Telegram bot token** | 空 | 来自 BotFather |
| **API keys** | 空 | 未购买 AI 积分时需要 |

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **渠道配置** | https://docs.openclaw.ai/channels/ |
| **Gateway 配置** | https://docs.openclaw.ai/gateway/configuration-reference |
| **安装总览** | https://docs.openclaw.ai/install/ |
| **其他平台** | https://docs.openclaw.ai/install/ (VPS/Docker/K8s 等) |
| **本报告** | `RedAgentTeamllm-wiki/wiki/install/hostinger.md` |

---

## 📝 快速参考

### 1-Click vs VPS 对比

| 特性 | 1-Click | VPS |
|------|---------|-----|
| **部署速度** | ⚡ 5 分钟 | ⏱️ 10 分钟 |
| **技术门槛** | 🟢 零配置 | 🟡 中等 |
| **控制权** | 🟡 有限 | 🟢 完全 |
| **管理方式** | 自动 | Docker Manager |
| **更新** | 自动 | 手动点击 |
| **推荐场景** | 快速开始 | 生产环境 |

### 安装后必做

1. ✅ **验证安装** — 发送 "Hi" 测试
2. ✅ **配置渠道** — 连接 Telegram/WhatsApp
3. ✅ **保存 Gateway token** — 用于 API 访问
4. ✅ **设置 AI 密钥** — 如未购买积分
5. ✅ **查看文档** — 了解功能和使用

---

## 🎯 下一步

安装完成后：

| 任务 | 文档 |
|------|------|
| **连接更多渠道** | `RedAgentTeamllm-wiki/wiki/channels/` |
| **配置 Gateway** | `RedAgentTeamllm-wiki/wiki/gateway/configuration-reference.md` |
| **安全加固** | `RedAgentTeamllm-wiki/wiki/gateway/security.md` |
| **自定义配置** | `RedAgentTeamllm-wiki/raw/gateway/` |

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于 Hostinger 安装  
**最后更新:** 2026-04-23 13:52 GMT+8
