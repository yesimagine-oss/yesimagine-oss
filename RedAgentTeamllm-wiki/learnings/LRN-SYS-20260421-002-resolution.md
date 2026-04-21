# LRN-SYS-20260421-002 公网访问 Token 认证问题解决报告

**事故 ID**: LRN-SYS-20260421-002  
**解决时间**: 2026-04-21 23:20 GMT+8  
**解决者**: Red Agent Team + 用户协作  
**状态**: ✅ 完全解决  

---

## 📋 事故现象

| 现象 | 状态 |
|------|------|
| 本地访问 (127.0.0.1:18789) | ✅ 正常 |
| 公网访问 (https://openclaw.unvw.com) | ❌ 失败 → ✅ 解决 |
| 初始错误 | `unauthorized: gateway token missing` |
| 中间错误 | `pairing required` |
| 最终状态 | ✅ 正常访问 |

---

## 🔍 问题根因

### 双层根因

| 层级 | 根因 | 说明 |
|------|------|------|
| **根因 1** | Token 未保存 | Control UI 的 localStorage 中 `token` 字段为空 |
| **根因 2** | 设备未配对 | 新浏览器/设备首次访问需要配对批准 |

---

## 🛠️ 解决步骤

### 步骤 1: 识别 Token 存储位置

**发现**: Token 保存在浏览器 localStorage，Key 为 `openclaw.control.settings.v1`

**来源**: 官方文档 + 知识库 `wiki/openclaw/02-control-ui/authentication.md`

---

### 步骤 2: 修改本地访问 Token (测试)

**操作**:
1. 访问 `http://127.0.0.1:18789`
2. 按 F12 打开开发者工具
3. Application → Local Storage → `127.0.0.1:18789`
4. 修改 `token` 值为：`36322def61722938e759077fa8d654388049d97fea9f1931`

**结果**: ✅ 本地访问正常

---

### 步骤 3: 修改域名访问 Token

**操作**:
1. 访问 `https://openclaw.unvw.com`
2. 按 F12 打开开发者工具
3. Application → Local Storage → `https://openclaw.unvw.com`
4. 添加/修改 `openclaw.control.settings.v1`:
   ```json
   {"gatewayUrl":"wss://openclaw.unvw.com","token":"36322def61722938e759077fa8d654388049d97fea9f1931","sessionKey":"agent:main:main"}
   ```

**结果**: ✅ 错误从 `token missing` 变为 `pairing required`

---

### 步骤 4: 批准设备配对

**操作**:
```bash
# 查看待批准设备
openclaw devices list

# 批准设备
openclaw devices approve a5bd8796-07ba-4e4a-a6af-4d877713a816
```

**结果**: ✅ 设备已批准

---

### 步骤 5: 验证

**操作**: 刷新页面

**结果**: ✅ 公网访问正常

---

## 📚 关键教训

### 教训 1: 相信用户的观察

| 错误做法 | 正确做法 |
|----------|----------|
| 盲目相信文档 | 文档是参考，用户观察是事实 |
| 反复让用户找不存在的 ⚙️ 按钮 | 用户说没有就没有 |
| 不相信用户说的"两个窗口一样" | 应该直接相信 |

**核心教训**: **用户说的就是事实，文档只是参考。**

---

### 教训 2: 不跳步，慢慢来

| 错误做法 | 正确做法 |
|----------|----------|
| 一次说很多步骤 | 一步一确认 |
| 用专业术语 (F5) | 说"刷新按钮 🔄" |
| 假设用户知道 | 每步都确认 |

**核心教训**: **简单直接，不绕弯子。**

---

### 教训 3: 先检查环境再操作

| 检查项 | 命令 | 状态 |
|--------|------|------|
| Gateway 进程 | `ps aux | grep openclaw-gateway` | ✅ 运行中 |
| Auth 模式 | `cat ~/.openclaw/openclaw.json` | ✅ token |
| 限流状态 | `openclaw logs` | ✅ 无限流 |
| 设备配对 | `openclaw devices list` | ✅ 已批准 |

**核心教训**: **先诊断，后操作。**

---

## 🎯 错误演变过程

| 阶段 | 错误信息 | 含义 | 解决动作 |
|------|----------|------|----------|
| **初始** | `token missing` | Token 未发送 | 设置 localStorage |
| **中间** | `pairing required` | 设备未配对 | `openclaw devices approve` |
| **最终** | ✅ 正常 | 认证通过 + 配对完成 | - |

---

## 📋 可复用 SOP

### 公网访问 Token 认证问题诊断 SOP

```bash
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 检查 Token 配置
openclaw config get gateway.auth.token

# 3. 检查设备配对
openclaw devices list

# 4. 查看日志
openclaw logs --follow | grep -i "auth\|token\|unauthorized"
```

### 浏览器 Token 设置 SOP

1. 访问目标 URL
2. F12 → Application → Local Storage
3. 添加/修改 `openclaw.control.settings.v1`
4. Value 格式:
   ```json
   {"gatewayUrl":"wss://<domain>","token":"<token>","sessionKey":"agent:main:main"}
   ```
5. 保存，刷新

### 设备配对 SOP

```bash
# 查看待批准设备
openclaw devices list

# 批准设备
openclaw devices approve <requestId>

# 验证
openclaw devices list
```

---

## 🏆 关键发现

| 发现 | 来源 | 应用 |
|------|------|------|
| **Token 在 localStorage 存储** | 官方文档 | 手动设置 Token |
| **每个域名独立存储** | 实测发现 | 本地/域名分别设置 |
| **设备配对是独立步骤** | 官方文档 | 认证后需配对 |
| **错误信息是诊断线索** | 实测发现 | token missing → pairing required |
| **用户观察优先于文档** | 本次教训 | 核心方法论 |

---

## 📊 耗时统计

| 阶段 | 耗时 | 说明 |
|------|------|------|
| 错误诊断 | ~60 分钟 | 反复尝试，走弯路 |
| 根因定位 | ~10 分钟 | 查知识库确认 |
| Token 设置 | ~5 分钟 | 本地 + 域名 |
| 设备配对 | ~1 分钟 | `openclaw devices approve` |
| 总耗时 | ~76 分钟 | 主要耗时在沟通误解 |

---

## ✅ 验证清单

- [x] Token 已设置 (localStorage)
- [x] Token 值正确 (`36322def...9f1931`)
- [x] 设备已配对 (`openclaw devices approve`)
- [x] Gateway 运行正常
- [x] 公网访问正常
- [x] 本地访问正常

---

## 📚 入库位置

| 文件 | 位置 |
|------|------|
| **排查报告** | `learnings/LRN-SYS-20260421-002-resolution.md` |
| **认证参考** | `wiki/openclaw/02-control-ui/authentication.md` |
| **Token 存储 Gene** | `wiki/openclaw/assets/genes/gene_openclaw_control_ui_token_storage.json` |

---

## 🎯 下次遇到类似问题

**7 分钟内解决流程**:

1. 查 Gateway 状态 (1 分钟)
2. 查 Token 配置 (1 分钟)
3. 查设备配对 (1 分钟)
4. 设置浏览器 Token (2 分钟)
5. 批准设备 (1 分钟)
6. 验证 (1 分钟)

**总计**: 7 分钟 ✅

---

## 💡 核心方法论

> **用户说的就是事实，文档只是参考。**

> **简单直接，不绕弯子。**

> **先诊断，后操作。**

> **一步一确认，不跳步。**

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:21 GMT+8  
**状态**: ✅ 已存入知识库  
**Git Commit**: 待提交

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
