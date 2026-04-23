# 📚 任务 1.2 学习笔记：参考快速卡片

**完成时间**: 2026-03-13 10:23 GMT+8  
**文件**: `skill-cheatsheet.md` (4.6KB)  
**阅读时长**: ~3 分钟

---

## 🎯 快速参考要点

### 1. 快速开始流程 (5 步)

```bash
1. init_skill.py <name> --path <dir> --resources scripts,references --examples
2. 编辑 SKILL.md (填写 frontmatter 和内容)
3. 开发脚本 (scripts/*.py)
4. quick_validate.py skills/<name>
5. package_skill.py skills/<name>
```

**记忆口诀**: 初始化 → 编辑 → 开发 → 验证 → 打包

---

### 2. SKILL.md 核心模板

```yaml
---
name: skill-name
description: |
  功能描述。当用户需要 X、Y、Z 时触发。
  示例："命令 1""命令 2"
---

# 技能标题
## 概述 (1-2 句话)
## 快速开始 (基本用法)
## 核心任务 (任务 1, 任务 2...)
## 资源 (scripts/, references/)
```

**关键点**: description 必须包含触发场景和示例

---

### 3. 验证清单 (三大类)

#### Frontmatter 验证
- [ ] name: 小写 + 连字符，≤64 字符
- [ ] description: 包含触发场景，≤1024 字符
- [ ] 无 `<` `>` 符号
- [ ] 只使用允许的属性

#### 结构验证
- [ ] SKILL.md 存在
- [ ] 目录命名正确
- [ ] 无 symlinks
- [ ] 删除示例文件

#### 脚本验证
- [ ] 添加 shebang
- [ ] 声明依赖
- [ ] 设置执行权限
- [ ] 错误处理

---

### 4. 设计模式速查

| 场景 | 推荐模式 |
|------|---------|
| 多步骤流程 | 工作流驱动 |
| 工具集合 | 任务驱动 |
| 多平台/框架 | 领域分离 |
| 集成系统 | 能力驱动 |
| 复杂技能 | 渐进式披露 |

**决策技巧**: 问自己"这个技能的核心是什么？"
- 流程 → 工作流驱动
- 工具集 → 任务驱动
- 多平台 → 领域分离

---

### 5. 工具命令速查

```bash
# 初始化
init_skill.py my-skill --path skills --resources scripts,references --examples

# 验证
quick_validate.py skills/my-skill

# 打包
package_skill.py skills/my-skill ./dist

# 分析
find /opt/openclaw/skills -name "SKILL.md"
unzip my-skill.skill -d output/
```

---

### 6. 安全红线 (10 条)

**核心原则**: 不请求凭证、不访问敏感文件、不执行外部代码

```
🚨 curl/wget 到未知 URL
🚨 发送数据到外部服务器
🚨 请求凭证/token/API key
🚨 读取 ~/.ssh, ~/.aws, ~/.config
🚨 访问 MEMORY.md, USER.md, SOUL.md
🚨 使用 base64 解码
🚨 eval()/exec() 外部输入
🚨 修改系统文件
🚨 混淆代码
🚨 请求 sudo 权限
```

---

### 7. 命名规范

**技能名**: `url-shortener` ✅ | `URL_Shortener` ❌
**脚本名**: `shorten.py` ✅ | `Shorten.py` ❌
**文档名**: `api-reference.md` ✅ | `API.md` ❌

**规则**: 小写 + 连字符，描述性动词开头

---

### 8. 最佳实践 Top 5

1. **description 详细且包含场景** - 触发机制的核心
2. **使用 inline metadata 声明依赖** - 现代化标准
3. **SKILL.md <500 行** - 避免 context 膨胀
4. **详情放 references/** - 渐进式披露
5. **删除不必要文件** - 保持简洁

---

### 9. 常见问题速查

**Q: description 怎么写？**
```
公式：功能 + 场景 + 示例
例：查询天气。当用户询问天气、温度、降水时触发。
    示例："北京天气""周末会下雨吗？"
```

**Q: 何时用 scripts/？**
```
✅ 复杂逻辑、外部 API、文件处理
❌ 简单示例（直接写在 SKILL.md）
```

**Q: 技能太大怎么办？**
```
1. 拆分到 references/
2. 只保留核心在 SKILL.md
3. 考虑拆分成多个技能
```

---

## 💡 卡片价值

这份速查卡的核心价值：

1. **实战导向** - 所有命令可直接复制使用
2. **检查清单** - 避免常见错误
3. **决策辅助** - 快速选择设计模式
4. **安全提醒** - 红线清单随时查阅

**使用建议**: 打印或收藏，开发时随时参考

---

## ✅ 检查清单

- [x] 掌握快速开始 5 步流程 ✅
- [x] 理解 SKILL.md 核心模板 ✅
- [x] 熟悉验证清单 ✅
- [x] 能选择设计模式 ✅
- [x] 记住工具命令 ✅
- [x] 牢记安全红线 ✅
- [x] 了解命名规范 ✅

**自评**: 快速参考要点已掌握，可作为实战查阅手册

---

**下一步**: 任务 1.3 - 学习实战过程
