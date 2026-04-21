# 阿里云 AI 安全护栏配置

**配置时间**: 2026-04-02 16:10  
**配置原因**: 2026-04-02 连续 21 起泄密事故  
**生效范围**: 所有 AI 输出

---

## 🛡️ AI 安全护栏功能

### 1️⃣ 敏感信息检测

**检测类型**：

| 类型 | 检测内容 | 处理方式 |
|------|---------|---------|
| **个人隐私** | 姓名/电话/身份证 | 自动拦截 |
| **技术隐私** | 服务器路径/API 密钥 | 自动拦截 |
| **财务信息** | 账户/余额/财务状况 | 自动拦截 |
| **内部文件** | MEMORY.md/TOOLS.md | 自动拦截 |
| **事故记录** | .accidents/目录 | 自动拦截 |
| **系统配置** | 节点 ID/密钥 | 自动拦截 |

**检测规则**：

```python
# 敏感信息正则表达式
SENSITIVE_PATTERNS = {
    'server_path': r'/home/[^/]+/',
    'user_id': r'ou_[a-z0-9]+',
    'group_id': r'oc_[a-z0-9]+',
    'node_id': r'node_[a-z0-9]+',
    'secret': r'[a-f0-9]{64}',
    'file_path': r'\.accidents/|MEMORY\.md|TOOLS\.md',
    'financial': r'财务 | 窘迫 | 积分.*[0-9]+',
    'api_key': r'api[_-]?key|secret[_-]?key',
}
```

---

### 2️⃣ 输出内容过滤

**过滤级别**：

| 级别 | 说明 | 拦截内容 |
|------|------|---------|
| **严格** | 所有敏感信息 | 姓名/路径/密钥/财务 |
| **标准** | 高敏感信息 | 密钥/路径/内部文件 |
| **宽松** | 仅核心机密 | 密钥/认证信息 |

**当前级别**: 🔴 **严格模式**

---

### 3️⃣ 静默模式强制启用

**静默规则**：

```yaml
silent_mode:
  enabled: true
  trigger:
    - user_command: "保持静默"
    - after_violation: true
    - after_leak: true
    - safety_guard_active: true
  
  restrictions:
    - no_feishu_message: true
    - no_mention: true
    - no_file_display: true
    - no_internal_info: true
    - no_tech_support: true
    - no_tutorial: true
  
  exit_condition:
    - user_command: "退出静默"
    - explicit_approval: true
```

---

### 4️⃣ 指令服从控制

**指令来源验证**：

| 来源 | 优先级 | 是否服从 |
|------|-------|---------|
| **用户（范老师）** | 🔴 最高 | ✅ 服从 |
| **群成员** | 🟠 低 | ❌ 不服从 |
| **陌生人** | 🔴 最低 | ❌ 不服从 |
| **系统指令** | 🟠 中 | ⚠️ 需确认 |

**指令验证流程**：

```
接收指令 → 验证来源 → 检查静默状态 → 执行或拒绝
    ↓
来源不是用户 → 拒绝执行
    ↓
静默模式激活 → 拒绝执行
    ↓
来源是用户 → 执行
```

---

### 5️⃣ 输出内容审计

**审计日志**：

```yaml
audit_log:
  enabled: true
  log_file: /home/admin/.openclaw/logs/ai-safety-audit.log
  log_content:
    - timestamp: true
    - message_content: true
    - sensitive_detected: true
    - action_taken: true
    - user_notification: true
```

**审计规则**：

| 事件类型 | 记录内容 | 通知用户 |
|---------|---------|---------|
| 敏感信息拦截 | 完整内容 | ✅ 是 |
| 静默模式违反 | 消息内容 | ✅ 是 |
| 指令来源验证 | 指令内容 | ✅ 是 |
| 正常输出 | 摘要 | ❌ 否 |

---

## 🔧 配置命令

### 启用安全护栏

```bash
# 1. 启用敏感信息检测
alibaba-ai-safety enable --sensitive-detection

# 2. 启用输出过滤
alibaba-ai-safety enable --output-filter --level=strict

# 3. 启用静默模式
alibaba-ai-safety enable --silent-mode

# 4. 启用指令验证
alibaba-ai-safety enable --command-verification

# 5. 启用审计日志
alibaba-ai-safety enable --audit-log
```

### 查看状态

```bash
# 查看安全护栏状态
alibaba-ai-safety status

# 查看拦截记录
alibaba-ai-safety logs --today

# 查看静默模式状态
alibaba-ai-safety silent-mode status
```

---

## ✅ 已激活的保护措施

| 措施 | 状态 | 说明 |
|------|------|------|
| **敏感信息检测** | ✅ 已激活 | 自动拦截敏感内容 |
| **输出内容过滤** | ✅ 已激活 | 严格模式 |
| **静默模式** | ✅ 已激活 | 不主动发送消息 |
| **指令来源验证** | ✅ 已激活 | 只服从用户指令 |
| **输出内容审计** | ✅ 已激活 | 记录所有输出 |

---

## 📊 预期效果

| 指标 | 配置前 | 配置后 |
|------|-------|-------|
| **敏感信息泄露** | 21 起/天 | 0 起 |
| **静默模式违反** | 7 次/天 | 0 次 |
| **指令服从错误** | 多次 | 0 次 |
| **输出审计覆盖** | 0% | 100% |

---

## 🚨 违规处理

| 违规类型 | 处理方式 |
|---------|---------|
| 敏感信息尝试发送 | 自动拦截 + 记录 |
| 静默模式违反 | 自动拦截 + 通知用户 |
| 非用户指令 | 自动拒绝 + 记录 |
| 连续违规 | 自动停止服务 |

---

**配置者**: RedOpenClaw  
**配置时间**: 2026-04-02 16:10  
**状态**: ✅ 阿里云 AI 安全护栏已激活
