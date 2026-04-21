# 2026-03-31 12:10 bird-twitter 未安装事故

**事故级别**: 🟠 P1 严重  
**发生时间**: 2026-03-31 12:08-12:10  
**影响范围**: 每日播报配置了 bird-twitter 但 CLI 未安装  
**状态**: 🔴 待修复

---

## 事故描述

用户要求"把 bird-twitter 配置到每日播报"，我：

1. ✅ 修改了 `daily-brief.py` 使用 bird CLI
2. ✅ 创建了定时任务（每日 8:30）
3. ❌ **没有检查 bird 是否已安装**
4. ❌ **没有检查 bird 是否已配置认证**

**结果**：定时任务创建了，但无法执行（bird 未安装）

---

## 根因分析

**为什么没有检查 bird 是否安装？**

1. **惯性思维** - 认为技能安装=CLI 已安装
2. **未验证** - 修改脚本前没有检查依赖
3. **配置缺失** - bird-twitter 技能文档提到需要手动安装 bird CLI

---

## bird-twitter 安装要求

根据技能文档：

```bash
# 需要安装 bird CLI
# 但 bird CLI 没有官方 npm/brew 包
# 需要手动下载二进制文件或从源码编译
```

**认证要求**：
```bash
export AUTH_TOKEN=<twitter auth_token cookie>
export CT0=<twitter ct0 cookie>
```

---

## 解决方案

### 方案 1：安装 bird CLI（推荐）
- 从 GitHub releases 下载
- 配置 Twitter cookie 认证

### 方案 2：使用 x-search 替代
- 已安装，无需额外配置
- 需要 XAI_API_KEY

### 方案 3：使用 web_fetch 抓取
- 无需额外工具
- 但功能有限

---

## 教训

1. **检查依赖再配置** - 修改脚本前检查 CLI 是否安装
2. **验证认证状态** - 需要认证的工具先确认已配置
3. **提供替代方案** - 当主要方案不可用时，有备选

---

## 修复结果

✅ **已修复** (2026-03-31 12:15)

**修复方案**: 改用 x-search 替代 bird-twitter

**原因**: bird CLI 工具 GitHub 项目已不存在（404）

**修改内容**:
1. ✅ 修改 `daily-brief.py` 使用 x-search
2. ✅ 定时任务保持不变（每日 8:30）
3. ⚠️ 需要配置 XAI_API_KEY

**配置需求**:
```bash
export XAI_API_KEY="您的 xAI API Key"
# 获取地址：https://console.x.ai
```

---

**记录时间**: 2026-03-31 12:10  
**修复时间**: 2026-03-31 12:15  
**记录者**: RedOpenClaw  
**状态**: ✅ 已修复（需配置 API Key）
