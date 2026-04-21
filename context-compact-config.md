# ✅ 分级触发机制配置完成

**配置时间**: 2026-03-27 10:02  
**配置文件**: `~/.openclaw/config.yaml`

---

## 📊 触发级别

| 阈值 | 动作 | 通知内容 |
|------|------|---------|
| **70%** | 🟡 仅通知 | "上下文使用 {percent}%，可以考虑清理" |
| **80%** | 🟠 建议 | "建议压缩。运行：openclaw session compact --keep-last 100" |
| **90%** | 🔴 自动压缩 | "已自动压缩并导出备份" |

---

## 🛡️ 安全机制

### 自动导出（压缩前备份）
- **路径**: `~/workspace/sessions/YYYY-MM-DD-HHMM.md`
- **格式**: Markdown
- **内容**: 完整会话记录

### 保留策略
- **70-89%**: 保留最近 100 条消息
- **90%+**: 保留最近 50 条消息
- **代码块**: 自动压缩（可配置）

### 通知渠道
- **飞书**: `ou_f4919832188bcc630f8f257497fa93a4`
- **时间**: 触发时立即通知

---

## 🔍 手动检查

```bash
# 检查当前状态
openclaw session status

# 手动压缩（保留 100 条）
openclaw session compact --keep-last 100

# 导出会话
openclaw session export --to ~/workspace/sessions/backup.md
```

---

## 📈 当前状态

| 指标 | 值 | 状态 |
|------|-----|------|
| 上下文使用 | 166k/1.0m (17%) | ✅ 健康 |
| 距离 70% | 53% | ✅ 充足 |
| 距离 90% | 73% | ✅ 非常安全 |

**预估**: 可继续使用 **5-10 倍** 当前工作量

---

## 🎯 下一步

1. ✅ 配置已完成
2. ✅ 自动监控已启用
3. ✅ 导出目录已创建
4. ⏳ 等待触发（当前无需操作）

---

## 📝 配置摘要

```yaml
session:
  auto_compact: true
  triggers:
    - threshold: 0.7  # 70% 通知
    - threshold: 0.8  # 80% 建议
    - threshold: 0.9  # 90% 自动压缩
  
  compact:
    keep_last_n: 100
    compress_code: true
  
  export:
    auto_export: true
    export_path: "~/workspace/sessions/"
```

---

**配置完成！系统会自动监控，达到阈值时通知您。** 🎉
