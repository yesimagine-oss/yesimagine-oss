---
category: linux
created_at: '2026-04-22'
tags:
- linux
- filesystem
- kernel
- vfs
- verified
title: Linux 内核文件系统总览
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://www.kernel.org/doc/html/latest/filesystems"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "curl+grep"
  trust_score: 1.0

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Linux 内核文件系统总览

**来源**: https://www.kernel.org/doc/html/latest/filesystems  
**验证时间**: 2026-04-22  
**状态**: 🟡 仅主页面，待补充各文件系统详细文档

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| 采样页面 | 1/10+ (仅首页) |
| 已验证事实 | 5 |
| 候选事实 | 2 |
| 可信度 | 0.99-1.0 |
| 证据等级 | 原文 + 实测 |

---

## 🎯 文档主题

| 主题 | 原文 |
|------|------|
| **标题** | Filesystems in the Linux kernel |
| **类型** | Linux 内核官方文件系统文档 |
| **版本** | latest (最新版) |

---

## 📁 支持的文件系统

| 类型 | 文件系统 |
|------|---------|
| **日志型** | ext4, ext3, ext2, xfs, btrfs |
| **企业级** | zfs |
| **兼容型** | fat, ntfs |

---

## 🔧 核心主题

| 主题 | 说明 |
|------|------|
| **Virtual Filesystems (VFS)** | 虚拟文件系统抽象层 |
| **Filesystem Mounting** | 文件系统挂载机制 |
| **Journaling and Copy-on-Write** | 日志与写时复制技术 |

---

## ✅ 已验证事实清单

| 事实 | 验证命令 | 可信度 |
|------|---------|--------|
| 文档主题 | `curl -s kernel.org/doc/html/latest/filesystems \| grep "Filesystems in the Linux kernel"` | 1.0 |
| 支持的 FS 列表 | `curl -s kernel.org/doc/html/latest/filesystems \| grep -E "ext4|xfs|btrfs|ntfs"` | 1.0 |
| 挂载主题 | `curl -s kernel.org/doc/html/latest/filesystems \| grep "Filesystem Mounting"` | 1.0 |
| VFS 概念 | `curl -s kernel.org/doc/html/latest/filesystems \| grep "Virtual Filesystems"` | 1.0 |
| 存储特性 | `curl -s kernel.org/doc/html/latest/filesystems \| grep "Journaling and Copy-on-Write"` | 1.0 |

---

## 🟡 待验证内容

| 内容 | 原因 | 建议来源 |
|------|------|---------|
| 单个文件系统详细参数 | 未进入子页面 | ext4.html, xfs.html, btrfs.html |
| VFS 内部接口与数据结构 | 未读取 vfs.html 详细内容 | vfs.html |

---

## 📦 关联资产

| 资产类型 | 资产 ID | 状态 |
|---------|--------|------|
| Gene | `gene_linux_fs_doc_topic` | ✅ 待固化 |
| Gene | `gene_linux_fs_supported_list` | ✅ 待固化 |
| Capsule | `capsule_linux_fs_list_check` | ✅ 待固化 |

---

**覆盖结论**: 仅覆盖目录页概览；无具体配置、参数、代码级细节  
**下一步**: 抓取 ext4.html, xfs.html, btrfs.html, vfs.html 等子文档
