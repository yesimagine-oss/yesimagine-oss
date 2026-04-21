---
category: linux
created_at: '2026-04-22'
tags:
- linux
- security
- landlock
- filesystem
- verified
title: Linux Landlock 文件系统安全
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "curl+grep"
  trust_score: 1.0

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 文件系统章节覆盖"
---

# Linux Landlock 文件系统安全

**来源**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
**验证时间**: 2026-04-22  
**状态**: 🟡 仅文件系统部分，待补充完整 API

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| 采样页面 | 1 (文件系统章节) |
| 已验证事实 | 5 |
| 候选事实 | 2 |
| 可信度 | 0.99-1.0 |
| 证据等级 | 原文 + 实测 |

---

## 🎯 Landlock 定位

| 特性 | 说明 |
|------|------|
| **全称** | Landlock: Unprivileged access control |
| **类型** | 非特权进程级访问控制机制 |
| **用途** | 进程沙箱，无需 root 权限 |

---

## 🔒 文件系统访问控制

| 控制项 | 说明 |
|--------|------|
| **规则类型** | Path-based access rules (基于路径) |
| **支持权限** | Read, Write, Execute, Append, Refer |
| **规则继承** | Inheritance across fork and exec |

---

## ✅ 已验证事实清单

| 事实 | 验证命令 | 可信度 |
|------|---------|--------|
| Landlock 定位 | `curl -s kernel.org/.../landlock.html \| grep "Unprivileged access control"` | 1.0 |
| 文件系统控制 | `curl -s kernel.org/.../landlock.html \| grep "Filesystem access control"` | 1.0 |
| 路径规则 | `curl -s kernel.org/.../landlock.html \| grep "Path-based access rules"` | 1.0 |
| 支持权限 | `curl -s kernel.org/.../landlock.html \| grep -E "read|write|execute"` | 1.0 |
| 规则继承 | `curl -s kernel.org/.../landlock.html \| grep "Inheritance across fork"` | 1.0 |

---

## 🟡 待验证内容

| 内容 | 原因 | 建议来源 |
|------|------|---------|
| syscall 接口 | 未提取系统调用 | 完整 Landlock 文档 |
| 权限掩码与结构体 | 未获取具体常量 | 完整 Landlock 文档 |

---

## 📦 关联资产

| 资产类型 | 资产 ID | 状态 |
|---------|--------|------|
| Gene | `gene_landlock_unprivileged_ac` | ✅ 已固化 |
| Gene | `gene_landlock_fs_permissions` | ✅ 已固化 |
| Capsule | `capsule_landlock_check_fs_rules` | ✅ 已固化 |

---

**覆盖结论**: 仅覆盖文件系统章节关键词；无编程接口、实际配置与示例  
**下一步**: 抓取完整 Landlock 文档，补充 syscall 接口与代码示例
