# 🎓 Skill 开发实战学习笔记

_记录从零开始创建 url-shortener 技能的完整过程_

**日期**: 2026-03-13  
**技能**: url-shortener  
**状态**: ✅ 完成打包

---

## 📋 开发过程回顾

### 阶段 1: 初始化

```bash
# 使用官方工具初始化技能
python3 /opt/openclaw/skills/skill-creator/scripts/init_skill.py url-shortener \
  --path /home/admin/.openclaw/workspace/skills \
  --resources scripts,references \
  --examples
```

**输出结构**:
```
url-shortener/
├── SKILL.md (模板)
├── scripts/example.py
└── references/api_reference.md
```

**学到的**:
- ✅ 工具自动创建标准目录结构
- ✅ 生成带有 TODO 占位符的模板
- ✅ 示例文件帮助理解格式

---

### 阶段 2: 编写 SKILL.md

**关键决策**:
1. **触发条件设计** - 明确说明何时使用
2. **结构选择** - 采用任务驱动模式
3. **详细程度** - 核心内容 + references 延伸阅读

**Frontmatter**:
```yaml
---
name: url-shortener
description: |
  URL 短链接生成和管理技能。支持生成短链接、统计点击、管理链接列表。
  当用户需要缩短 URL、追踪链接点击、批量管理短链接时触发。
  示例："缩短这个链接""统计链接点击数""列出所有短链接"
---
```

**学到的**:
- ✅ description 是主要触发机制，必须详细
- ✅ 包含具体使用场景和示例
- ✅ 不要使用 `<` `>` 符号
- ✅ name 必须小写 + 连字符

---

### 阶段 3: 开发脚本

#### shorten.py (7.7KB)

**功能**:
- URL 验证
- 短码生成（随机/自定义）
- SQLite 存储
- 批量处理

**关键技术点**:
```python
# uv inline script metadata (PEP 723)
# /// script
# requires-python = ">=3.11"
# dependencies = ["click", "rich", "sqlite-vec"]
# ///

# 数据库连接管理
def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    # 自动创建表...
```

**学到的**:
- ✅ 使用 uv 的 inline metadata 声明依赖
- ✅ 自动创建数据库和表
- ✅ 错误处理和用户反馈
- ✅ 支持多种使用模式（单个/批量/静默）

#### list.py (3.4KB)

**功能**:
- 列出所有链接
- 排序和分页
- JSON 输出

**学到的**:
- ✅ Rich 库格式化表格输出
- ✅ 支持程序化使用（--json）
- ✅ 参数验证

#### stats.py (3.4KB)

**功能**:
- 查看链接统计
- 详细点击记录
- JSON 输出

**学到的**:
- ✅ Panel 格式化关键信息
- ✅ 分级信息展示（基本/详细）

---

### 阶段 4: 编写参考文档

**api-reference.md (7.6KB)** 包含:

1. **脚本命令详解** - 所有参数和示例
2. **数据库 Schema** - 表结构和索引
3. **配置选项** - 环境变量和配置文件
4. **扩展开发指南** - 如何添加新功能

**学到的**:
- ✅ 参考文档按需加载，可以详细
- ✅ 包含实际代码示例
- ✅ 提供故障排除指南
- ✅ 在 SKILL.md 中引用参考文档

---

### 阶段 5: 清理和打包

```bash
# 删除示例文件
rm scripts/example.py references/api_reference.md

# 设置执行权限
chmod +x scripts/*.py

# 打包（使用 zip，因为验证脚本有 Python 版本兼容问题）
cd /home/admin/.openclaw/workspace/skills
zip -r url-shortener.skill url-shortener/
```

**输出**:
```
url-shortener.skill (11.9KB)
├── SKILL.md (4.4KB)
├── scripts/
│   ├── shorten.py (7.7KB)
│   ├── list.py (3.4KB)
│   └── stats.py (3.4KB)
└── references/
    └── api-reference.md (7.6KB)
```

**学到的**:
- ✅ 删除模板示例文件
- ✅ .skill 文件是标准 ZIP 格式
- ✅ 验证脚本可能有兼容性问题（Python 3.6 vs 3.9+）

---

## 📊 技能统计

| 指标 | 数值 |
|------|------|
| 总文件数 | 5 |
| 总代码量 | ~26KB |
| Python 脚本 | 3 个 |
| 文档页数 | ~20 页（估算） |
| 开发时间 | ~1 小时 |
| 依赖包 | click, rich, sqlite-vec |

---

## 🎯 设计决策

### 为什么选择 SQLite？
- ✅ 零配置
- ✅ 单文件
- ✅ 适合个人使用
- ✅ 易于备份

### 为什么使用 Rich 库？
- ✅ 美观的终端输出
- ✅ 表格、面板等组件
- ✅ 颜色支持
- ✅ 广泛使用

### 为什么支持 JSON 输出？
- ✅ 便于脚本集成
- ✅ 程序化使用
- ✅ 数据导出

---

## ⚠️ 遇到的问题和解决

### 问题 1: Python 版本兼容性

**现象**: 验证脚本使用 `dict[str, str]` 语法（Python 3.9+），但系统 Python 是 3.6.8

**解决**: 
- 手动验证结构
- 使用标准 zip 命令打包
- 建议升级验证脚本兼容性

### 问题 2: 依赖声明

**决策**: 使用 uv 的 inline script metadata (PEP 723)

**原因**:
- 现代化标准
- 自文档化
- uv 自动处理依赖

### 问题 3: 隐私保护

**实现**: IP 地址哈希存储

```python
import hashlib
ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
```

---

## 📚 学到的最佳实践

### SKILL.md 编写
1. description 包含触发场景
2. 提供具体使用示例
3. 结构清晰，使用标题分层
4. 引用参考文档避免臃肿

### 脚本开发
1. 使用 shebang 和 inline metadata
2. 提供 --help 和详细文档
3. 支持多种使用模式
4. 错误信息清晰有用

### 参考文档
1. 包含完整 API 参考
2. 提供故障排除指南
3. 给出扩展开发示例
4. 使用实际代码片段

### 项目结构
1. 遵循标准目录布局
2. 删除不必要的示例文件
3. 设置正确的文件权限
4. 保持简洁的依赖

---

## 🚀 下一步改进

### 功能增强
- [ ] 添加 QR 码生成
- [ ] 支持链接过期
- [ ] 添加用户认证
- [ ] HTTP API 服务

### 文档改进
- [ ] 添加视频教程
- [ ] 更多使用场景示例
- [ ] 性能优化指南

### 工具改进
- [ ] 修复验证脚本兼容性
- [ ] 添加单元测试
- [ ] CI/CD 集成

---

## 🎓 学习收获

### 理论知识
1. ✅ Skill 三层加载机制
2. ✅ 渐进式披露设计
3. ✅ 触发条件优化
4. ✅ 安全审查流程

### 实践技能
1. ✅ 使用 init_skill.py 初始化
2. ✅ 编写符合规范的 SKILL.md
3. ✅ 开发可执行脚本
4. ✅ 打包和分发技能

### 设计思维
1. ✅ 以用户为中心的设计
2. ✅ 模块化思维
3. ✅ 文档驱动开发
4. ✅ 隐私保护意识

---

## 📝 检查清单

开发新技能时的检查清单：

### 规划阶段
- [ ] 明确技能解决的问题
- [ ] 列出用户使用场景
- [ ] 确定需要的资源类型
- [ ] 选择合适的设计模式

### 开发阶段
- [ ] 编写详细的 description
- [ ] 创建清晰的目录结构
- [ ] 实现核心功能
- [ ] 添加错误处理
- [ ] 编写参考文档

### 测试阶段
- [ ] 验证 SKILL.md 格式
- [ ] 测试所有脚本功能
- [ ] 检查边界情况
- [ ] 验证输出格式

### 发布阶段
- [ ] 删除示例文件
- [ ] 设置文件权限
- [ ] 打包成 .skill 文件
- [ ] 编写发布说明

---

## 🔗 相关资源

- [Skill 开发完全指南](./skill-development-guide.md)
- [skill-creator SKILL.md](/opt/openclaw/skills/skill-creator/SKILL.md)
- [ClawHub](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

_持续学习，持续改进 🦀_
