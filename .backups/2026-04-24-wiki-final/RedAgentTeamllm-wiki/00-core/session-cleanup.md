# 会话文件清理操作手册

**适用场景:** WebChat 前端假死/加载缓慢/渲染崩溃  
**风险等级:** 🟢 低（有备份兜底）  
**预计耗时:** 10-15 分钟  

---

## 前置条件

- [ ] 已确认 WebChat 前端异常（假死/崩溃）
- [ ] Gateway 服务正常运行
- [ ] 有足够磁盘空间用于备份

---

## 操作步骤

### 步骤 1: 全量备份（必须）
```bash
cp -r ~/.openclaw/agents/main/sessions ~/sessions_full_backup_$(date +%Y%m%d_%H%M%S)
```
**验证:**
```bash
ls -lh ~/sessions_full_backup_* | tail -1
```
**预期:** 显示备份目录大小（通常几 MB 到几十 MB）

---

### 步骤 2: 定位异常文件
```bash
cd ~/.openclaw/agents/main/sessions
ls -lhS | grep -v ".deleted\|.reset\|.tmp\|.safebackup" | head -20
```
**判断标准:**
| 文件类型 | 正常大小 | 异常阈值 |
|----------|----------|----------|
| `sessions.json` | 1-10M | - |
| `*.jsonl` | <100KB | >500KB ⚠️ |

**标记:** 记录所有 >500KB 的 `.jsonl` 文件

---

### 步骤 3: 验证会话内容（可选）
```bash
head -10 <异常文件名>.jsonl
```
**检查:**
- 文件格式是否正常（JSON 每行）
- 是否有明显异常内容（重复/乱码）

---

### 步骤 4: 重启测试（排除临时问题）
```bash
openclaw gateway restart
```
**验证:** 刷新 WebChat 页面

**结果处理:**
- ✅ 正常 → 结束（可能是临时状态）
- ❌ 仍异常 → 继续步骤 5

---

### 步骤 5: 移动异常文件
```bash
# 移动到备份目录（不是删除！）
mv <异常文件名>.jsonl ~/sessions_full_backup_$(date +%Y%m%d_%H%M%S)/
```
**注意:** 一次移动一个，测试后再处理下一个

---

### 步骤 6: 重启并验证
```bash
openclaw gateway restart
```
**验证:**
1. 关闭浏览器所有标签
2. 重新打开 Chrome
3. 访问 `http://localhost:18789`
4. 检查页面是否正常加载

---

### 步骤 7: 回滚（如需要）
```bash
# 如移动后出现新问题，立即恢复
cp ~/sessions_full_backup_YYYYMMDD/<文件名>.jsonl ~/.openclaw/agents/main/sessions/
openclaw gateway restart
```

---

## 快速参考

### 查找最大会话文件
```bash
cd ~/.openclaw/agents/main/sessions
ls -lhS | grep "\.jsonl$" | head -5
```

### 查看会话文件数量
```bash
ls *.jsonl | wc -l
```

### 查看总会话大小
```bash
du -sh ~/.openclaw/agents/main/sessions/
```

---

## 风险说明

| 风险 | 概率 | 规避措施 |
|------|------|----------|
| 误删重要会话 | 极低 | 先备份，移动不删除 |
| 问题未解决 | 中 | 逐步测试，保留回滚能力 |
| 新问题分析 | 低 | 一次只移动一个文件 |

---

## 相关文档

- **事故记录:** `llm-wiki/accidents/webchat-freeze-20260423.md`
- **备份恢复:** `llm-wiki/playbooks/backup-restore.md`

---

**版本:** v1.0  
**最后更新:** 2026-04-23  
**基于案例:** WebChat 假死故障排查（成功案例）
