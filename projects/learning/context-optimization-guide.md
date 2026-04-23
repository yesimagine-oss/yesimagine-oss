# 🚀 Context 使用效率优化指南

_最大化 Skill 性能，最小化 context 占用_

**创建时间**: 2026-03-13

---

## 📊 Context 是公共资源

> "The context window is a public good."

每一份加载到 context 的内容都在占用有限资源。优化原则：
- ✅ 只加载必要内容
- ✅ 按需加载详细信息
- ✅ 脚本执行不占 context
- ✅ 参考文档延迟加载

---

## 🎯 三层加载机制优化

### Level 1: Metadata (始终加载 ~100 词)

**优化策略**:
```yaml
# ✅ 好的 description
description: |
  URL 短链接生成和管理技能。支持生成短链接、统计点击、管理链接列表。
  当用户需要缩短 URL、追踪链接点击、批量管理短链接时触发。
  示例："缩短这个链接""统计链接点击数""列出所有短链接"

# ❌ 差的 description
description: URL 技能  # 太简单，无触发场景
```

**最佳实践**:
- 包含功能描述 + 触发场景 + 使用示例
- 控制在 1024 字符以内
- 使用具体关键词便于匹配

---

### Level 2: SKILL.md 正文 (触发后加载 <5k 词)

**优化策略**:

#### 1. 保持精简 (<500 行)
```markdown
# ✅ 精简结构
## 概述 (1-2 句)
## 快速开始 (3-5 个示例)
## 核心任务 (按场景分类)
## 资源说明 (引用 references/)

# ❌ 臃肿结构
## 概述 (1 页)
## 背景介绍 (2 页)
## 设计理念 (1 页)
## 详细 API (10 页)  # 应移到 references/
```

#### 2. 使用渐进式披露
```markdown
## 基础用法
[核心内容，直接展示]

## 高级功能

### 表单填充
详见 [FORMS.md](references/forms.md)  # 按需加载

### API 参考
详见 [REFERENCE.md](references/api.md)  # 按需加载
```

#### 3. 明确引用说明
```markdown
## 资源

### scripts/
- `shorten.py`: 生成短链接，支持自定义别名和批量处理
- `stats.py`: 查看统计，包含详细点击记录

### references/
- `api-reference.md`: 完整 API 文档，包含所有参数和示例
  **何时读取**: 需要详细参数说明或高级用法时
- `workflows.md`: 工作流程详解
  **何时读取**: 处理复杂场景或故障排除时
```

---

### Level 3: 捆绑资源 (选择性加载)

#### scripts/ - 执行不占 context

**优势**:
```python
# ✅ 脚本可以被 AI 直接执行
uv run scripts/shorten.py https://example.com

# 无需读入 context，直接执行获取结果
```

**最佳实践**:
- 复杂逻辑放脚本
- 重复性代码放脚本
- 外部 API 调用放脚本
- 使用 uv inline metadata 声明依赖

#### references/ - 按需读入 context

**组织策略**:

##### 模式 1: 按功能分离
```
references/
├── api-reference.md    # API 详细文档
├── workflows.md        # 工作流程详解
├── troubleshooting.md  # 故障排除
└── examples.md         # 使用示例集合
```

##### 模式 2: 按领域分离
```
references/
├── aws.md      # AWS 部署模式
├── gcp.md      # GCP 部署模式
└── azure.md    # Azure 部署模式
```

##### 模式 3: 按用户类型分离
```
references/
├── beginner.md    # 新手指南
├── advanced.md    # 高级用法
└── admin.md       # 管理员配置
```

**加载提示**:
```markdown
在 SKILL.md 中明确说明：
- "需要详细参数时读取 `references/api-reference.md`"
- "遇到错误时读取 `references/troubleshooting.md`"
- "高级用法参考 `references/advanced.md`"
```

#### assets/ - 不读入 context

**用途**:
- 模板文件 (.pptx, .docx)
- 图片资源 (.png, .jpg)
- 字体文件 (.ttf, .woff2)
- 样板代码目录

**特点**: 直接用于输出，不占用 context

---

## 📐 文件组织策略

### 大文件拆分

**问题**: 单个文件超过 100 行

**解决**:
```markdown
# ❌ 单个大文件
api-reference.md (500 行)

# ✅ 拆分为多个文件
references/
├── api-authentication.md (50 行)
├── api-endpoints.md (100 行)
├── api-error-codes.md (80 行)
└── api-examples.md (100 行)
```

**SKILL.md 引用**:
```markdown
## API 参考

### 认证
详见 [api-authentication.md](references/api-authentication.md)

### 端点
详见 [api-endpoints.md](references/api-endpoints.md)
```

### 添加目录导航

**长文件 (>100 行)**:
```markdown
# API 参考

## 目录
1. [认证](#认证)
2. [端点列表](#端点列表)
3. [错误码](#错误码)
4. [示例](#示例)

## 认证
...

## 端点列表
...
```

---

## 🔍 触发条件优化

### description 关键词策略

**包含触发词**:
```yaml
description: |
  查询天气信息。使用 wttr.in 获取实时天气和预报。
  当用户询问天气、温度、降水、风力时触发。
  示例："北京今天天气如何？""周末会下雨吗？"
```

**触发词分析**:
- ✅ 天气、温度、降水、风力（功能词）
- ✅ 询问、如何（动作词）
- ✅ 北京、周末（场景词）

### 使用 triggers 字段（如支持）

```yaml
triggers:
  - "search for"
  - "search web"
  - "find information"
  - "look up"
```

---

## ⚡ 性能优化技巧

### 1. 脚本优先

```markdown
# ✅ 优先使用脚本
```bash
uv run scripts/process.py input.txt
```

# ❌ 避免在 SKILL.md 中写复杂代码
```python
def process_file(input_path):
    # 大量代码...
```
```

### 2. 条件加载

```markdown
## 高级功能

### 批量处理
仅在需要批量处理时读取 `references/batch-processing.md`

### API 集成
仅在需要 API 集成时读取 `references/api-integration.md`
```

### 3. 缓存友好

```markdown
# ✅ 稳定的文件结构
references/api-reference.md  # 不变的路径

# ❌ 频繁变动的结构
references/v1/api.md  # 版本化路径导致重复加载
```

### 4. 索引优化

```markdown
在 SKILL.md 中添加搜索提示：
"使用 grep 搜索 references/ 目录：
`grep -r 'authentication' references/`"
```

---

## 📊 优化效果对比

### 优化前
```
SKILL.md: 2000 行 (全部加载)
scripts/: 无
references/: 无
总 context: ~10000 词
```

### 优化后
```
SKILL.md: 400 行 (核心内容)
scripts/: 5 个脚本 (执行不占 context)
references/: 5 个文档 (按需加载)
总 context: ~2000 词 (基础) + 按需加载
节省：80% context
```

---

## ✅ 优化检查清单

### Metadata
- [ ] description 包含功能 + 场景 + 示例
- [ ] description ≤1024 字符
- [ ] 使用具体触发词
- [ ] 考虑添加 triggers 字段

### SKILL.md
- [ ] 保持 <500 行
- [ ] 使用渐进式披露
- [ ] 明确引用 references/
- [ ] 提供快速开始示例
- [ ] 删除冗余说明

### scripts/
- [ ] 复杂逻辑放脚本
- [ ] 使用 inline metadata
- [ ] 添加执行权限
- [ ] 提供 --help 支持

### references/
- [ ] 大文件拆分
- [ ] 添加目录导航
- [ ] 明确加载时机
- [ ] 保持单一职责

### 整体
- [ ] 无重复内容
- [ ] 结构清晰
- [ ] 便于导航
- [ ] 测试加载效果

---

## 🎯 实际案例

### clipboard-manager 优化分析

**当前结构**:
```
SKILL.md: 140 行 ✅
scripts/: 4 个脚本 ✅
references/: 空 ⚠️
```

**优化建议**:
1. 创建 `references/api-reference.md` - 详细 API 文档
2. 创建 `references/troubleshooting.md` - 故障排除
3. SKILL.md 中明确引用时机

**预期效果**:
- SKILL.md 可减少到 100 行
- 详细信息按需加载
- context 节省 ~30%

---

## 🔗 相关资源

- [Skill 开发完全指南](../skill-development-guide.md)
- [skill-creator SKILL.md](/opt/openclaw/skills/skill-creator/SKILL.md)
- [渐进式披露模式](../skill-development-guide.md#45-渐进式披露模式)

---

_优化无止境，持续改进！_

**最后更新**: 2026-03-13
