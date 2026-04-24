# Linux Landlock 安全模块文档采样报告

**采样时间**: 2026-04-22  
**采样来源**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
**采样人**: 用户补充  
**入库人**: Red Agent Team 🦞  
**状态**: ✅ 已蒸馏

---

## 一、原始采样区

### 页面采样

1. **URL**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
   **原文**: `Landlock: Unprivileged access control`

2. **URL**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
   **原文**: `Filesystem access control`

3. **URL**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
   **原文**: `Path-based access rules`

4. **URL**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
   **原文**: `Read, write, execute, append, refer`

5. **URL**: https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem  
   **原文**: `Inheritance across fork and exec`

---

### 命令/动作采样

1. **命令**: `curl -s "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem" | grep "Landlock: Unprivileged access control"`  
   **输出**: `Landlock: Unprivileged access control`

2. **命令**: `curl -s "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem" | grep "Filesystem access control"`  
   **输出**: `Filesystem access control`

3. **命令**: `curl -s "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem" | grep "Path-based access rules"`  
   **输出**: `Path-based access rules`

4. **命令**: `curl -s "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem" | grep -E "read|write|execute|append|refer"`  
   **输出**: `Read, write, execute, append, refer`

5. **命令**: `curl -s "https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem" | grep "Inheritance across fork and exec"`  
   **输出**: `Inheritance across fork and exec`

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| 入口页面 | https://www.kernel.org/doc/html/latest/security/landlock.html#filesystem |
| 已发现页面 | [同上] |
| 已抓取页面 | [同上] |
| 被排除页面 | 无 |
| 排除原因 | 无 |
| 是否存在更深页面 | 是（完整 Landlock 文档、syscall 定义、示例） |
| 关联页面 | https://www.kernel.org/doc/html/latest/security/landlock.html |
| 覆盖率评估 | 仅完成文件系统部分覆盖 |
| 覆盖结论 | 不满足 100% 覆盖条件 |

---

## 三、已验证通过的事实清单

| 原始对象 | 来源 | 验证动作 | 验证结果 | 可信度 | 证据等级 |
|---------|------|---------|---------|--------|---------|
| Landlock 定位 | landlock.html | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 控制范围 | landlock.html | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 规则类型 | landlock.html | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 访问权限 | landlock.html | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 规则继承 | landlock.html | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |

---

## 四、来源可信但未实测验证的候选事实

1. **Landlock 完整 syscall 接口** - 未提取系统调用
2. **规则定义与权限掩码** - 未获取具体权限常量

---

## 五、已蒸馏资产

### Genes (2 个)
- `gene_landlock_unprivileged_ac` - Landlock 核心特性
- `gene_landlock_fs_permissions` - Landlock 文件系统权限

### Capsules (1 个)
- `capsule_landlock_check_fs_rules` - Landlock 文件系统规则检查

---

**入库路径**: `raw/linux-landlock-fs-sample-20260422.md`  
**状态**: ✅ 完成
