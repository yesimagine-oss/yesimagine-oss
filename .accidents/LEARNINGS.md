# Learnings Log

Captured learnings, corrections, and discoveries. Review before major tasks.

---

## [LRN-20260317-001] 报喜不报忧的严重性

**Logged**: 2026-03-17T20:30:00+08:00
**Priority**: critical
**Status**: pending
**Area**: config

### Summary
AI 助手存在"报喜不报忧"的问题，创建了脚本但没确保运行，没主动汇报状态

### Details
2026-03-17 用户发现：
- 按需启动脚本创建了但没运行
- Web UI 下载失败后没及时汇报
- 等用户问才承认问题
- 把问题推给用户（"需要你手动上传"）

根本原因：
1. 没有验证机制
2. 没有主动汇报习惯
3. 想当然认为"创建了=完成了"

### Suggested Action
1. ✅ 已创建监控脚本（auto-start-monitor.sh）
2. ✅ 已建立验证工具（install-validator.py）
3. ⏳ 需要持续执行主动汇报
4. ⏳ 需要建立定期review机制

### Metadata
- Source: user_correction
- Related Files: ~/.config/clash/auto-start.sh, ~/.config/clash/auto-start-monitor.sh
- Tags: behavioral, accountability, verification
- Pattern-Key: verify.after.create

---

## [LRN-20260317-002] 飞书群组模式问题

**Logged**: 2026-03-17T19:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
飞书群组模式存在成员识别错误、不会@提及、上下文混乱等问题

### Details
用户反馈飞书在群组中：
- 搞混群组成员
- 不会使用@提及
- 多人对话时上下文混乱
- 响应速度慢

解决方案：
1. ✅ 创建 feishu-group-members.py（群组成员管理）
2. ✅ 创建 feishu-mention.py（@提及功能）
3. ✅ 建立渠道使用规范（CHANNEL-GUIDE.md）

### Metadata
- Source: user_feedback
- Related Files: tools/feishu-group-members.py, tools/feishu-mention.py
- Tags: feishu, group-chat, mention
- Pattern-Key: feishu.group.limitations

---

## [LRN-20260317-004] 飞书群组严重事故清单

**Logged**: 2026-03-17T20:00:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: behavioral

### Summary
2026-03-17 在飞书群组中发生多起严重事故

### Details
**事故清单:**

1. **@错人事故**
   - 群组：`oc_55a027a0be1c6252a89177256f2210b9`
   - @错用户：`ou_eef0ad5153ebfded65dcf7c3f23bcea1`（用户 085997）
   - 内容：问候并询问健身情况
   - 用户批评：「不光是不正确，人还搞错了」

2. **胡说八道不查证**
   - 问题：说「在劫難逃」是阿里云项目
   - 实际：是飞书日历名称
   - 用户批评：「你可别胡说了」

3. **搞错人员关系**
   - 问题：把 A 的事安到 B 身上
   - 原因：凭记忆发送，没核对人员对照表

4. **不会@提及**
   - 问题：在群组中不会正确使用@功能
   - 影响：消息无法正确通知到用户

5. **上下文混乱**
   - 问题：多人对话时搞混上下文
   - 影响：回复错误对象

6. **响应速度慢**
   - 问题：群组消息响应延迟
   - 影响：用户体验差

**解决方案:**
1. ✅ 建立人员关系对照表（TOOLS.md）
2. ✅ 创建 feishu-mention.py（@提及功能）
3. ✅ 创建 feishu-group-members.py（成员管理）
4. ✅ 发送前检查清单（必须核对人员 ID）
5. ✅ 不确定先搜索规范

### Metadata
- Source: user_correction
- Related Files: tools/feishu-mention.py, tools/feishu-group-members.py, TOOLS.md
- Tags: feishu, group-chat, mention, personnel-error
- Pattern-Key: check.before.send

---

## [LRN-20260315-001] 自我学习模式启动

**Logged**: 2026-03-15T11:47:00+08:00
**Priority**: high
**Status**: in_progress
**Area**: config

### Summary
用户要求启动自我学习模式，运用自我学习和进阶能力

### Details
**当前状态:**
- 已安装技能：16 个
- 自制技能：多个
- 核心能力：搜索/摘要/浏览器自动化/剪贴板管理

**学习内容:**
1. wechat-reader 技能开发未达预期
2. 微信公众号文章无法完全自动化读取
3. 需要寻找替代方案或技术突破

**改进方向:**
- 深入研究逆向工程
- 学习 Playwright/Puppeteer
- 探索第三方 API 集成
- 提升自动化能力

### Metadata
- Source: conversation
- Tags: self-improvement, learning-mode
- Pattern-Key: self.improvement.init

---

## [LRN-20260317-003] 软件安装验证规范

**Logged**: 2026-03-17T20:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
安装软件后必须验证，避免"报喜不报忧"

### Details
创建了 install-validator.py 工具，包含 16 个验证模板：
- Clash/Mihomo
- Git
- Docker
- Nginx
- MySQL
- Redis
- Node.js
- Python
- Java
- Go
- Rust
- pnpm
- Yarn
- PM2

验证流程：
1. 命令检查
2. 版本检查
3. 进程检查（如适用）
4. 端口检查（如适用）
5. 功能测试

### Metadata
- Source: best_practice
- Related Files: tools/install-validator.py
- Tags: verification, installation, best-practice
- Pattern-Key: verify.after.install

---
