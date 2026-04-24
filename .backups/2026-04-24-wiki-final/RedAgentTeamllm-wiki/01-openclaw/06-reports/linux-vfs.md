---
category: linux
created_at: '2026-04-22'
tags:
- linux
- vfs
- filesystem
- kernel
- verified
title: Linux VFS 虚拟文件系统
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://www.kernel.org/doc/html/latest/filesystems/vfs.html"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "curl+grep"
  trust_score: 1.0

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面核心对象覆盖"
---

# Linux VFS 虚拟文件系统

**来源**: https://www.kernel.org/doc/html/latest/filesystems/vfs.html  
**验证时间**: 2026-04-22  
**状态**: 🟡 仅核心对象，待补充 API 与流程

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| 采样页面 | 1 (VFS 主页面) |
| 已验证事实 | 5 |
| 候选事实 | 3 |
| 可信度 | 0.99-1.0 |
| 证据等级 | 原文 + 实测 |

---

## 🎯 VFS 定位

| 特性 | 说明 |
|------|------|
| **全称** | Virtual Filesystem (虚拟文件系统) |
| **类型** | 内核抽象层 |
| **用途** | 统一接口访问不同文件系统 |

---

## 📦 核心对象

| 对象 | 说明 |
|------|------|
| **inode** | 索引节点，代表文件系统对象 |
| **dentry** | 目录项，用于路径查找 |
| **file** | 打开文件描述结构 |
| **super_block** | 超级块，代表已挂载文件系统 |

---

## ✅ 已验证事实清单

| 事实 | 验证命令 | 可信度 |
|------|---------|--------|
| VFS 文档标题 | `curl -s kernel.org/.../vfs.html \| grep "Virtual Filesystem"` | 1.0 |
| inode 对象 | `curl -s kernel.org/.../vfs.html \| grep -w "inode"` | 1.0 |
| dentry 对象 | `curl -s kernel.org/.../vfs.html \| grep -w "dentry"` | 1.0 |
| file 对象 | `curl -s kernel.org/.../vfs.html \| grep -w "file"` | 1.0 |
| super_block 对象 | `curl -s kernel.org/.../vfs.html \| grep -w "super_block"` | 1.0 |

---

## 🟡 待验证内容

| 内容 | 原因 | 建议来源 |
|------|------|---------|
| 对象关系与操作接口 | 未抓取结构体定义 | vfs.html 子章节 |
| 系统调用与回调函数 | 未提取 syscall | vfs.html API 章节 |
| 挂载与路径查找流程 | 未读取执行流程 | vfs.html 流程章节 |

---

## 📦 关联资产

| 资产类型 | 资产 ID | 状态 |
|---------|--------|------|
| Gene | `gene_vfs_overview_title` | ✅ 已固化 |
| Gene | `gene_vfs_core_objects` | ✅ 已固化 |
| Capsule | `capsule_vfs_check_core_objects` | ✅ 已固化 |

---

**覆盖结论**: 仅抓取核心对象名称；无结构体、接口、流程等详细信息  
**下一步**: 抓取对象关系、API 接口、执行流程章节
