---
category: llm
created_at: '2026-04-14'
tags:
- llm
- clawhub
- 发布准备清单
- api
title: Publishing Checklist
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
# 📦 ClawHub 发布准备清单

**技能**: clipboard-manager  
**版本**: 1.0.0  
**准备时间**: 2026-03-13

---

## ✅ 发布前检查

### 1. 技能结构验证

- [x] SKILL.md 存在且格式正确
- [x] scripts/ 目录包含功能脚本
- [x] 无示例文件残留
- [x] 所有脚本有执行权限
- [x] 无 symlinks

### 2. 代码质量检查

- [x] 所有脚本有 shebang
- [x] 使用 uv inline metadata 声明依赖
- [x] 错误处理完善
- [x] CLI 参数清晰
- [x] 文档完整

### 3. 安全检查

- [x] 无外部 API 调用
- [x] 无凭证请求
- [x] 无敏感文件访问
- [x] 本地存储（SQLite）
- [x] 无网络请求

### 4. 文档完整性

- [x] SKILL.md 包含：
  - 清晰的 description
  - 触发场景说明
  - 使用示例
  - 配置说明
  - 故障排除

---

## 📋 发布命令

### 登录 ClawHub
```bash
clawhub login
clawhub whoami
```

### 发布技能
```bash
cd /home/admin/.openclaw/workspace/skills

clawhub publish ./clipboard-manager \
  --slug clipboard-manager \
  --name "Clipboard Manager" \
  --version 1.0.0 \
  --changelog "Initial release: save, list, search, copy clipboard history with auto-categorization"
```

### 验证发布
```bash
clawhub search "clipboard"
clawhub list
```

---

## 🏷️ 技能元数据

**建议的发布信息**:

```json
{
  "name": "Clipboard Manager",
  "slug": "clipboard-manager",
  "version": "1.0.0",
  "description": "剪贴板历史管理技能。支持保存、搜索、分类和快速复制剪贴板内容。",
  "author": "OpenClaw Agent",
  "license": "MIT",
  "tags": ["clipboard", "productivity", "history", "search"],
  "category": "Productivity",
  "changelog": "Initial release: save, list, search, copy clipboard history with auto-categorization"
}
```

---

## 📊 技能统计

| 指标 | 数值 |
|------|------|
| 总大小 | 11KB |
| 脚本数量 | 4 |
| 代码行数 | ~500 |
| 依赖包 | rich, pyperclip |
| 支持功能 | 保存/列出/搜索/复制 |

---

## 🔗 相关资源

- ClawHub: https://clawhub.com
- 文档：/opt/openclaw/docs/tools/clawhub.md
- 技能目录：/home/admin/.openclaw/workspace/skills/clipboard-manager/

---

**发布状态**: 准备就绪  
**下一步**: 执行 clawhub publish 命令

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[evomap-asset-publishing]]
- [[signature-checklist]]
- [[feishu-checklist]]
