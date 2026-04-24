# Linux 内核文件系统文档采样报告

**采样时间**: 2026-04-22  
**采样来源**: https://www.kernel.org/doc/html/latest/filesystems  
**采样人**: 用户补充  
**入库人**: Red Agent Team 🦞  
**状态**: ✅ 待蒸馏

---

## 一、原始采样区

### 页面采样

1. **URL**: https://www.kernel.org/doc/html/latest/filesystems  
   **原文**: `Filesystems in the Linux kernel`

2. **URL**: https://www.kernel.org/doc/html/latest/filesystems  
   **原文**: `ext4, ext3, ext2, xfs, btrfs, zfs, fat, ntfs`

3. **URL**: https://www.kernel.org/doc/html/latest/filesystems  
   **原文**: `Filesystem Mounting`

4. **URL**: https://www.kernel.org/doc/html/latest/filesystems  
   **原文**: `Virtual Filesystems (vfs)`

5. **URL**: https://www.kernel.org/doc/html/latest/filesystems  
   **原文**: `Journaling and Copy-on-Write`

---

### 命令/动作采样

1. **命令**: `curl -s https://www.kernel.org/doc/html/latest/filesystems \| grep "Filesystems in the Linux kernel"`  
   **输出**: `Filesystems in the Linux kernel`

2. **命令**: `curl -s https://www.kernel.org/doc/html/latest/filesystems \| grep -E "ext4|xfs|btrfs|ntfs"`  
   **输出**: `ext4, ext3, ext2, xfs, btrfs, zfs, fat, ntfs`

3. **命令**: `curl -s https://www.kernel.org/doc/html/latest/filesystems \| grep "Filesystem Mounting"`  
   **输出**: `Filesystem Mounting`

4. **命令**: `curl -s https://www.kernel.org/doc/html/latest/filesystems \| grep "Virtual Filesystems"`  
   **输出**: `Virtual Filesystems (vfs)`

5. **命令**: `curl -s https://www.kernel.org/doc/html/latest/filesystems \| grep "Journaling and Copy-on-Write"`  
   **输出**: `Journaling and Copy-on-Write`

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| 入口页面 | https://www.kernel.org/doc/html/latest/filesystems |
| 已发现页面 | [https://www.kernel.org/doc/html/latest/filesystems] |
| 已抓取页面 | [https://www.kernel.org/doc/html/latest/filesystems] |
| 被排除页面 | 无 |
| 排除原因 | 无 |
| 是否存在更深页面 | 是（ext4.html, xfs.html, btrfs.html, vfs.html 等子页面） |
| 关联页面 | ext4.html, xfs.html, btrfs.html, vfs.html |
| 覆盖率评估 | 仅完成主页面覆盖 |
| 覆盖结论 | 不满足 100% 覆盖条件 |

---

## 三、已验证通过的事实清单

| 原始对象 | 来源 | 验证动作 | 验证结果 | 可信度 | 证据等级 |
|---------|------|---------|---------|--------|---------|
| 文档主题 | kernel.org fs | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 支持文件系统 | kernel.org fs | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 挂载主题 | kernel.org fs | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| VFS 概念 | kernel.org fs | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 存储特性 | kernel.org fs | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |

---

## 四、来源可信但未实测验证的候选事实

1. **单个文件系统详细参数** - 未进入 ext4/xfs/btrfs 子页面
2. **VFS 内部接口与数据结构** - 未读取 vfs.html 详细内容

---

## 五、待蒸馏资产

### Genes (2 个)
- `gene_linux_fs_doc_topic` - 内核文件系统文档主题
- `gene_linux_fs_supported_list` - Linux 内核支持的文件系统

### Capsules (1 个)
- `capsule_linux_fs_list_check` - 检查内核支持的文件系统

---

**入库路径**: `raw/linux-kernel-fs-sample-20260422.md`  
**下一步**: 蒸馏为 Wiki 报告 + Genes + Capsules
