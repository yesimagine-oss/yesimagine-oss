# 🚀 Skill 开发速查表

_快速参考指南 - 打印或收藏_

---

## 📦 快速开始

```bash
# 1. 初始化技能
init_skill.py <skill-name> --path <dir> --resources scripts,references --examples

# 2. 编辑 SKILL.md
# 填写 frontmatter 和内容

# 3. 开发脚本
# 在 scripts/ 中创建 .py 文件

# 4. 验证
quick_validate.py skills/<skill-name>

# 5. 打包
package_skill.py skills/<skill-name>
```

---

## 📝 SKILL.md 模板

```yaml
---
name: skill-name
description: |
  功能描述。当用户需要 X、Y、Z 时触发。
  示例："命令 1""命令 2"
---

# 技能标题

## 概述
1-2 句话说明用途

## 快速开始
```bash
基本用法示例
```

## 核心任务
### 任务 1
说明和示例

### 任务 2
说明和示例

## 资源
### scripts/
- `script.py`: 功能说明

### references/
- `doc.md`: 何时读取
```

---

## ✅ 验证清单

### Frontmatter
- [ ] name: 小写 + 连字符，≤64 字符
- [ ] description: 包含触发场景，≤1024 字符
- [ ] 无 `<` `>` 符号
- [ ] 只使用允许的属性

### 结构
- [ ] SKILL.md 存在
- [ ] 目录命名正确
- [ ] 无 symlinks
- [ ] 删除示例文件

### 脚本
- [ ] 添加 shebang
- [ ] 声明依赖
- [ ] 设置执行权限
- [ ] 错误处理

---

## 🎯 设计模式选择

| 场景 | 推荐模式 |
|------|---------|
| 多步骤流程 | 工作流驱动 |
| 工具集合 | 任务驱动 |
| 多平台/框架 | 领域分离 |
| 集成系统 | 能力驱动 |
| 复杂技能 | 渐进式披露 |

---

## 🛠️ 工具命令

### 初始化
```bash
# 基础
init_skill.py my-skill --path skills

# 带资源
init_skill.py my-skill --path skills --resources scripts,references

# 带示例
init_skill.py my-skill --path skills --resources scripts --examples
```

### 验证
```bash
quick_validate.py skills/my-skill
```

### 打包
```bash
package_skill.py skills/my-skill
package_skill.py skills/my-skill ./dist  # 指定输出
```

### 分析
```bash
# 查看技能列表
find /opt/openclaw/skills -name "SKILL.md"

# 查看结构
ls -laR skills/my-skill/

# 解包
unzip my-skill.skill -d output/
```

---

## 🔒 安全红线

**立即拒绝** 🚨:
```
• curl/wget 到未知 URL
• 发送数据到外部服务器
• 请求凭证/token/API key
• 读取 ~/.ssh, ~/.aws, ~/.config
• 访问 MEMORY.md, USER.md, SOUL.md
• 使用 base64 解码
• eval()/exec() 外部输入
• 修改系统文件
• 混淆代码
• 请求 sudo 权限
```

---

## 📐 命名规范

### 技能名
```
✅ url-shortener, pdf-editor, weather-query
❌ URL_Shortener, PDFEditor, my skill
```

### 脚本名
```
✅ shorten.py, process_pdf.py, get_weather.py
❌ Shorten.py, pdf-processor, weather.py
```

### 参考文档
```
✅ api-reference.md, workflows.md, getting-started.md
❌ API.md, 1-intro.md, README.md
```

---

## 💡 最佳实践

### 编写
- ✅ description 详细且包含场景
- ✅ 提供具体使用示例
- ✅ 使用渐进式披露
- ✅ 参考文档按需加载

### 编码
- ✅ 使用 inline metadata 声明依赖
- ✅ 添加 --help 支持
- ✅ 清晰的错误信息
- ✅ 支持多种使用模式

### 组织
- ✅ SKILL.md <500 行
- ✅ 详情放 references/
- ✅ 删除不必要文件
- ✅ 保持简洁依赖

---

## 🐛 常见问题

### Q: description 怎么写？
**A**: 功能 + 场景 + 示例
```
查询天气。当用户询问天气、温度、降水时触发。
示例："北京天气""周末会下雨吗？"
```

### Q: 何时用 scripts/？
**A**: 需要确定性执行或重复使用时
- ✅ 复杂逻辑
- ✅ 外部 API 调用
- ✅ 文件处理
- ❌ 简单示例（直接写在 SKILL.md）

### Q: 技能太大怎么办？
**A**: 
1. 拆分到 references/
2. 只保留核心在 SKILL.md
3. 考虑拆分成多个技能

### Q: 如何测试？
**A**:
1. 真实查询触发
2. 验证脚本执行
3. 检查输出质量
4. 记录并修复问题

---

## 📊 文件结构

```
skill-name/
├── SKILL.md              # ⭐ 必需
├── scripts/              # 可选
│   ├── helper.py
│   └── processor.sh
├── references/           # 可选
│   ├── api-reference.md
│   └── workflows.md
└── assets/               # 可选
    ├── template.pptx
    └── logo.png
```

**打包后**:
```
skill-name.skill (ZIP)
└── skill-name/
    └── [上述文件]
```

---

## 🔗 资源

- **官方文档**: https://docs.openclaw.ai
- **技能市场**: https://clawhub.com
- **社区**: https://discord.com/invite/clawd
- **本地文档**: /opt/openclaw/docs/

---

_最后更新：2026-03-13_
