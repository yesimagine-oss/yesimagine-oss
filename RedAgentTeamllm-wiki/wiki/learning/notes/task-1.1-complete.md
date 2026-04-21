---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 任务
- 学习笔记
- 阅读完整指南
- guide
title: Task 1.1 Complete
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
# 📚 任务 1.1 学习笔记：阅读完整指南

**完成时间**: 2026-03-13 10:20 GMT+8  
**文件**: `skill-development-guide.md` (18KB)  
**阅读时长**: ~5 分钟

---

## 🧠 核心收获

### 1. Skill 本质理解

> **关键理念**: Skill 不是教 AI"是什么"，而是教 AI"怎么做"——提供程序性知识（procedural knowledge）

这是理解 Skill 设计的核心。Skill 不是百科全书，而是操作手册。

### 2. 三层加载机制

```
Level 1: Metadata (始终加载) → 触发判断
    ↓
Level 2: SKILL.md 正文 (触发后加载) → 核心指导
    ↓
Level 3: 捆绑资源 (按需加载) → 详细参考
```

**设计精髓**: 渐进式披露，避免 context 膨胀

### 3. 触发机制关键

**description 是主要触发机制**，必须包含：
- ✅ 功能描述
- ✅ 使用场景（WHEN）
- ✅ 具体示例

**示例对比**:
```yaml
# ❌ 差的描述
description: 天气查询技能

# ✅ 好的描述
description: |
  查询天气信息。使用 wttr.in 获取实时天气和预报。
  当用户询问天气、温度、降水、风力时触发。
  示例："北京今天天气如何？""周末会下雨吗？"
```

### 4. 五大设计模式

| 模式 | 适用场景 | 关键特征 |
|------|---------|---------|
| 工作流驱动 | 多步骤流程 | 决策树 + 步骤说明 |
| 任务驱动 | 工具集合 | 任务分类 + 命令说明 |
| 领域分离 | 多平台/框架 | SKILL.md 导航 + references 分离 |
| 能力驱动 | 集成系统 | 编号能力列表 |
| 渐进式披露 | 复杂技能 | 核心精简 + references 详情 |

### 5. 开发工作流

```
理解需求 → 规划结构 → 初始化 → 实现 → 验证 → 打包 → 测试 → 迭代
```

**关键工具**:
- `init_skill.py` - 初始化
- `quick_validate.py` - 验证
- `package_skill.py` - 打包

### 6. 安全红线

**15 条立即拒绝的红线**，核心原则：
- 不请求凭证
- 不访问敏感文件
- 不执行外部代码
- 不修改系统文件

### 7. 最佳实践要点

**命名**:
- 小写 + 连字符
- ≤64 字符
- 描述性动词开头

**文档**:
- SKILL.md <500 行
- 详情放 references/
- 明确说明何时读取

**脚本**:
- 使用 uv inline metadata
- 添加 shebang
- 设置执行权限

---

## 💡 关键洞察

### 洞察 1: Context 是公共资源
> "The context window is a public good."

每一份加载到 context 的内容都在占用有限的资源。Skill 设计必须考虑 token 效率。

### 洞察 2: 触发在 description，不在正文
很多新手会把"何时使用"写在 SKILL.md 正文中，但正文只在触发后才加载。触发判断只看 frontmatter 的 description。

### 洞察 3: 脚本可以不读入 context
scripts/ 中的脚本可以被 AI 直接执行，无需读入 context。这是 token 优化的关键技巧。

### 洞察 4: 渐进式披露是核心设计原则
```
SKILL.md: 核心工作流 (<500 行)
    ↓ 需要时
references/: 详细文档 (按需读取)
```

---

## 📝 待深入理解的问题

1. **如何精确控制 description 的触发效果？**
   - 需要实验不同描述的触发率

2. **references/ 文件如何被 AI 发现并读取？**
   - 需要在 SKILL.md 中明确说明

3. **多脚本技能如何组织依赖关系？**
   - 需要研究 skill-creator 的实现

4. **如何测试技能的触发效果？**
   - 需要建立测试流程

---

## ✅ 检查清单

完成本指南后，我应该能够：

- [x] 解释 Skill 的三层加载机制 ✅
- [x] 创建符合规范的 SKILL.md ✅
- [x] 编写可执行的 Python 脚本 ✅
- [x] 使用工具链初始化/验证/打包 ✅
- [x] 选择合适的设计模式 ✅
- [x] 进行安全审查 ✅
- [x] 发布技能到 ClawHub ✅

**自评**: 理论理解完成，需要实践巩固

---

## 🔗 关联知识

- [知识库 - Skill 架构](../learning/knowledge-base.md#skill-架构)
- [知识库 - 触发机制](../learning/knowledge-base.md#触发机制)
- [知识库 - 设计模式](../learning/knowledge-base.md#设计模式)

---

**下一步**: 任务 1.2 - 阅读快速卡片

## 參考

- [[Asset05 Task Solution Template]]


## 相關文檔

- [[evomap_task_template]]
- [[knowledge-files-complete-list]]
- [[task_solution_template]]
