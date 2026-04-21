# ⏳ simplify-and-harden 安装说明

**更新时间**: 2026-03-13 21:40 GMT+8

---

## 📊 当前状态

| 技能 | 状态 | 原因 |
|------|------|------|
| **self-improving-agent** | ✅ 已安装可用 | 完整安装 |
| **simplify-and-harden** | ⏳ 等待安装 | ClawHub 速率限制 |

---

## ⚠️ 安装失败原因

```
ClawHub API 速率限制 (Rate limit exceeded)

原因:
- 短时间内多次请求 ClawHub API
- 安装 self-improving-agent 时已使用配额
- 需要等待配额重置
```

---

## 🔧 解决方案

### 方案 1: 等待后重试（推荐）

```bash
# 等待 1 小时后重试
sleep 3600 && clawhub install simplify-and-harden

# 或者明天再试（速率限制通常 24 小时重置）
# 明天执行：
clawhub install simplify-and-harden
```

### 方案 2: 手动安装（备选）

```bash
# 1. 克隆 pskoett 的技能仓库
cd /tmp
git clone https://github.com/pskoett/pskoett-ai-skills.git

# 2. 复制 simplify-and-harden 到技能目录
cp -r pskoett-ai-skills/skills/simplify-and-harden \
    /home/admin/.openclaw/workspace/skills/

# 3. 验证安装
ls -la /home/admin/.openclaw/workspace/skills/simplify-and-harden/
```

### 方案 3: 使用技能元数据直接下载

```bash
# 技能信息:
# ownerId: kn70cjr952qdec1nx70zs6wefn7ynq2t
# slug: simplify-and-harden
# version: 1.0.1

# 等待 ClawHub 速率限制解除后:
clawhub install simplify-and-harden --force
```

---

## 📋 技能信息

```
名称：simplify-and-harden
版本：1.0.1
所有者：pskoett (kn70cjr952qdec1nx70zs6wefn7ynq2t)
功能：编码完成后自我审查
流程:
  1. Simplify Pass - 简化代码
  2. Harden Pass - 强化代码
  3. Micro-documentation Pass - 微文档
```

---

## ✅ self-improving-agent 已就绪

```
状态：✅ 已安装且可用
版本：v1.0.11
位置：/home/admin/.openclaw/workspace/skills/self-improving-agent/

功能:
✅ 学习日志记录
✅ 错误日志记录
✅ 功能请求记录
✅ Hook 自动提醒
✅ 错误自动检测
✅ 技能提取工具

立即可用！
```

---

## 📝 建议行动

### 现在可以做

```
□ 开始使用 self-improving-agent
□ 记录今天的学习到 .learnings/
□ 等待 simplify-and-harden 速率限制解除
```

### 明天做

```
□ 重试安装 simplify-and-harden
□ 学习 simplify-and-harden 的使用
□ 结合两个技能使用
```

---

**更新时间**: 2026-03-13 21:40 GMT+8  
**建议**: 先使用 self-improving-agent，simplify-and-harden 明天再安装
