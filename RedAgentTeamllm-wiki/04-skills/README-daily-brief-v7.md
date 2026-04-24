---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 每日播报
- v7
- 防重复版
- api
title: Readme Daily Brief V7
type: general
version: '1.0'

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
# 每日播报 v7 - 防重复版

**更新时间**: 2026-04-01  
**版本**: v7  
**修复内容**: 消息去重机制

---

## 🛡️ 防重复机制

### 双重去重保障

| 层级 | 机制 | 说明 |
|------|------|------|
| **本地缓存** | 5 分钟内容去重 | 相同内容 5 分钟内不发送 |
| **飞书 API** | uuid 字段去重 | 飞书服务端去重 |

### 工作原理

```
生成内容 → 计算 MD5 → 检查缓存 → 无重复则发送 → 记录到缓存
                ↓
           有重复 → 跳过发送
```

### 缓存配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 缓存文件 | `/tmp/daily-brief-cache.json` | 临时缓存 |
| 去重时间窗 | 300 秒（5 分钟） | 5 分钟内不重复 |
| 缓存清理 | 3600 秒（1 小时） | 1 小时后自动清理 |

---

## 📝 使用示例

### 正常运行

```bash
python3 tools/daily-brief.py
```

**输出**:
```
📅 每日播報 - 開始執行（v7 防重複版）
🔍 检查消息去重...
📤 發送到：ou_xxx
✅ 飛書發送成功：om_xxx (uuid: b0b083f5...)
📝 已记录消息：om_xxx
✅ 播報完成
```

### 重复发送（被阻止）

```bash
python3 tools/daily-brief.py
```

**输出**:
```
📅 每日播報 - 開始執行（v7 防重複版）
🔍 检查消息去重...
⚠️ 检测到重复消息（10 秒内），跳过发送
⚠️ 跳过本次发送（检测到重复）
```

---

## 🔧 维护

### 查看缓存

```bash
cat /tmp/daily-brief-cache.json | python3 -m json.tool
```

### 清除缓存

```bash
rm /tmp/daily-brief-cache.json
```

### 查看日志

```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep daily-brief
```

---

## 📊 技术细节

### 消息唯一性计算

```python
content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
```

### 飞书去重字段

```python
client_msg_id = hashlib.md5(f"{message}_{int(time.time() / 60)}".encode('utf-8')).hexdigest()
payload = {
    "receive_id": user_id,
    "msg_type": "text",
    "content": json.dumps({"text": message}),
    "uuid": client_msg_id  # 飞书去重
}
```

### 缓存结构

```json
{
  "messages": [
    {
      "hash": "abc123...",
      "msg_id": "om_xxx",
      "time": 1711958400
    }
  ]
}
```

---

## 🚨 故障排查

### 问题：重复发送

**检查**:
1. 缓存文件是否存在：`ls -la /tmp/daily-brief-cache.json`
2. 缓存内容是否有效：`cat /tmp/daily-brief-cache.json`
3. 系统时间是否正确：`date`

**解决**:
```bash
# 清除缓存重试
rm /tmp/daily-brief-cache.json
python3 tools/daily-brief.py
```

### 问题：发送失败

**检查**:
1. 飞书 Token 是否有效
2. 用户 ID 是否正确
3. 网络是否正常

**日志**:
```bash
grep "daily-brief" /tmp/openclaw/openclaw-*.log | tail -20
```

---

## 📈 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v7 | 2026-04-01 | ✅ 添加防重复机制 |
| v6 | 2026-03-XX | 纯文本天气版 |
| v5 | 2026-03-XX | 飞书私聊版 |

---

**维护者**: RedOpenClaw  
**文档**: `tools/README-daily-brief-v7.md`

## 參考

- [[Readme]]
- [[Readme]]


## 相關文檔

- [[README]]
- [[clawbrowser-readme]]
- [[README]]
