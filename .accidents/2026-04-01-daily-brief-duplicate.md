# 2026-04-01 每日播报重复发送事故

**发生时间**: 2026-04-01 08:30  
**事故级别**: 🟡 P2 轻微  
**影响范围**: 飞书私聊消息重复发送  

---

## 📋 事故经过

用户收到两条**完全相同**的每日播报消息：

```
农历乙巳年 2 月 14 日 星期三 | 清明
2026 年 4 月 1 日 Wednesday

🌤️ 济南 9.3~20.3°C 🌤️ 威海 7.6~10.4°C

🦞 RedOpenClaw
*...生活太快⚡️...老逼快跑💨...*
```

两条消息内容、格式、时间戳完全一致。

---

## 🔍 调查结果

### 排除的原因

| 可能原因 | 调查结果 | 状态 |
|---------|---------|------|
| cron 配置重复 | 只有一个 `daily-brief-private` 任务 | ❌ 排除 |
| 脚本重复调用 | 日志显示只执行一次（08:30:00-08:30:32） | ❌ 排除 |
| 脚本重试逻辑 | `send_feishu` 函数无重试机制 | ❌ 排除 |
| weather 脚本误发 | `weather-daily-wttr.py` 发送到群组，格式不同 | ❌ 排除 |

### 日志证据

```json
// 08:30:00 - 任务开始
"sessionKey=agent:main:cron:daily-brief-private"

// 08:30:32 - 任务完成（单次）
"jobId":"daily-brief-private","consecutiveErrors":1
```

**结论**: 系统层面只执行了一次，但用户收到两条消息。

---

## 🔎 可能原因

### 1. 飞书 API 重试机制（最可能）

飞书开放平台可能有**消息去重失败**的问题：
- API 请求超时但实际已发送
- OpenClaw 重试导致重复
- 飞书侧消息去重机制失效

### 2. 网络问题导致重复提交

- 第一次请求超时
- 自动重试发送相同消息
- 飞书未正确去重

### 3. cron 任务重复触发（可能性低）

- Gateway 重启导致 cron 调度器重复触发
- 但日志只显示一次执行记录

---

## 🛠️ 解决方案

### 立即修复

1. ✅ **添加消息去重机制** - 在发送前检查最近 N 分钟是否发送过相同内容
2. ⏳ **添加消息 ID 追踪** - 记录已发送的消息 ID，避免重复
3. ⏳ **优化重试逻辑** - 仅在确认失败时重试，超时不重试

### 技术实现

**方案 1: 本地消息缓存**
```python
# 在 daily-brief.py 中添加
MESSAGE_CACHE = Path('/tmp/daily-brief-sent.json')

def should_send(content_hash):
    """检查是否应该发送（避免重复）"""
    if not MESSAGE_CACHE.exists():
        return True
    
    cache = json.loads(MESSAGE_CACHE.read_text())
    # 检查 5 分钟内是否发送过相同内容
    five_min_ago = time.time() - 300
    for msg in cache.get('messages', []):
        if msg['hash'] == content_hash and msg['time'] > five_min_ago:
            return False
    return True

def record_sent(content_hash, msg_id):
    """记录已发送的消息"""
    cache = MESSAGE_CACHE.exists() and json.loads(MESSAGE_CACHE.read_text()) or {'messages': []}
    cache['messages'].append({'hash': content_hash, 'msg_id': msg_id, 'time': time.time()})
    # 只保留最近 1 小时的记录
    cache['messages'] = [m for m in cache['messages'] if time.time() - m['time'] < 3600]
    MESSAGE_CACHE.write_text(json.dumps(cache))
```

**方案 2: 飞书消息去重**
```python
# 使用 client_msg_id 进行去重
import hashlib
client_msg_id = hashlib.md5(content.encode()).hexdigest()
payload = {
    "receive_id": user_id,
    "msg_type": "text",
    "content": json.dumps({"text": content}, ensure_ascii=False),
    "uuid": client_msg_id  # 飞书支持的去重字段
}
```

---

## 📊 影响评估

| 维度 | 评估 |
|------|------|
| **用户体验** | 中 - 收到重复消息会造成困扰 |
| **数据完整性** | 低 - 不影响其他功能 |
| **系统稳定性** | 低 - 不影响服务运行 |
| **重复频率** | 偶发 - 首次发现 |

---

## 📝 改进措施

### 短期（本周）

1. ⏳ **添加消息去重机制** - 所有发送消息的脚本都加上
2. ⏳ **添加发送日志** - 记录每次发送的详细内容、时间、消息 ID
3. ⏳ **测试重试场景** - 模拟网络超时，验证不会重复发送

### 长期（本月）

1. ⏳ **统一消息发送模块** - 抽取公共的 `message_sender.py`
2. ⏳ **添加消息队列** - 避免并发发送
3. ⏳ **监控重复率** - 统计重复发送的比例

---

## 🔗 相关文件

- 脚本：`tools/daily-brief.py`
- 配置：`~/.openclaw/cron/jobs.json`
- 日志：`/tmp/openclaw/openclaw-2026-04-01.log`
- 事故索引：`.accidents/README.md`

---

## ✅ 修复验证

**修复时间**: 2026-04-01 08:58  
**修复版本**: v7 防重複版

### 测试结果

| 测试 | 结果 | 说明 |
|------|------|------|
| 第一次发送 | ✅ 成功 | 消息 ID: `om_x100b53f2996e38a0b21629f5f2b0ecb` |
| 第二次发送（10 秒后） | ✅ 被阻止 | "检测到重复消息（10 秒内），跳过发送" |
| 本地缓存 | ✅ 正常 | `/tmp/daily-brief-cache.json` 已记录 |
| 飞书去重 | ✅ 启用 | 使用 `uuid` 字段 |

### 修复内容

1. ✅ **本地消息缓存** - 5 分钟内不发送相同内容
2. ✅ **飞书 uuid 去重** - 使用 `uuid` 字段让飞书 API 去重
3. ✅ **发送日志记录** - 记录消息 ID 和时间
4. ✅ **缓存自动清理** - 1 小时后自动清理旧记录

---

**记录时间**: 2026-04-01 08:55  
**更新时间**: 2026-04-01 08:58 (已修复)  
**记录者**: RedOpenClaw  
**状态**: ✅ 已修复并验证

🦞 RedOpenClaw
*...生活太快⚡️...老逼快跑💨...*
