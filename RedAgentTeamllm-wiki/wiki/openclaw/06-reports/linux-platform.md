---
category: openclaw
created_at: '2026-04-22'
tags:
- linux
- platform
- installation
- verified
title: Linux 平台安装指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/platforms/linux"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Linux 平台安装指南

**来源**: https://docs.openclaw.ai/platforms/linux  
**验证时间**: 2026-04-22 04:15 GMT+8  
**状态**: 🟡 仅主页面，待补充服务管理/卸载/日志路径

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Linux Installation & Platform Notes |
| **支持架构** | ✅ amd64, arm64 |
| **安装脚本** | ✅ curl -fsSL https://get.openclaw.ai \| sudo bash |
| **二进制路径** | ✅ /usr/local/bin/openclaw |
| **Systemd 服务** | ✅ openclaw.service |
| **服务启停** | ❌ 缺 systemctl 命令 |
| **日志路径** | ❌ 缺日志位置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_linux_title` | Linux 平台标题 | `grep "Linux Installation & Platform Notes"` |
| `gene_openclaw_linux_install_script` | 一键安装脚本 | `grep "curl -fsSL https://get.openclaw.ai"` |
| `gene_openclaw_linux_binary_path` | 二进制路径 | `grep "/usr/local/bin/openclaw"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_linux_install` | Linux 一键安装 | `openclaw:linux:install` |
| `capsule_openclaw_linux_check_binary` | 检查安装 | `openclaw:linux:check:binary` |

---

## 📋 已验证事实

1. ✅ 支持架构：amd64, arm64
2. ✅ 安装脚本：curl -fsSL https://get.openclaw.ai \| sudo bash
3. ✅ 二进制路径：/usr/local/bin/openclaw
4. ✅ Systemd 服务：openclaw.service

---

## 🟡 待补充

- [ ] systemctl start/stop/restart 命令
- [ ] 卸载脚本/步骤
- [ ] 系统依赖检查
- [ ] 日志路径 (/var/log/openclaw/?)

---

## 📚 来源

- **原始采样**: `raw/linux-platform-sample-20260422-0415.md`
- **官方文档**: https://docs.openclaw.ai/platforms/linux

---

**最后更新**: 2026-04-22 04:15 GMT+8  
**维护者**: Red Agent Team
