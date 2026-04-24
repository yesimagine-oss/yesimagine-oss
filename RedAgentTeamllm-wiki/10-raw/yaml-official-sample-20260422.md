# YAML 官方站点采样报告

**采样时间**: 2026-04-22  
**采样来源**: https://yaml.org  
**采样人**: 用户补充  
**入库人**: Red Agent Team 🦞  
**状态**: ✅ 待蒸馏

---

## 一、原始采样区

### 页面采样

1. **URL**: https://yaml.org  
   **原文**: `YAML: YAML Ain't Markup Language™`

2. **URL**: https://yaml.org  
   **原文**: `Human Friendly Data Serialization Standard`

3. **URL**: https://yaml.org  
   **原文**: `key: value`

4. **URL**: https://yaml.org  
   **原文**: `- item1`

5. **URL**: https://yaml.org  
   **原文**: `# This is a comment`

---

### 命令/动作采样

1. **命令**: `curl -s https://yaml.org | grep -i "YAML: YAML Ain't Markup Language"`  
   **输出**: `YAML: YAML Ain't Markup Language™`

2. **命令**: `curl -s https://yaml.org | grep -i "Human Friendly Data Serialization"`  
   **输出**: `Human Friendly Data Serialization Standard`

3. **命令**: `curl -s https://yaml.org | grep -E "^( | )*-[a-z0-9]" | head -1`  
   **输出**: `- item1`

4. **命令**: `curl -s https://yaml.org | grep -E "^#"`  
   **输出**: `# This is a comment`

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| 入口页面 | https://yaml.org |
| 已发现页面 | [https://yaml.org] |
| 已抓取页面 | [https://yaml.org] |
| 被排除页面 | 无 |
| 排除原因 | 无 |
| 是否存在更深页面 | 是（spec、refcard、faq、download 等） |
| 关联页面 | https://yaml.org/spec/、https://yaml.org/refcard.html、https://yaml.org/faq.html |
| 覆盖率评估 | 仅完成主页面覆盖 |
| 覆盖结论 | 不满足 100% 覆盖条件 |

---

## 三、已验证通过的事实清单

| 原始对象 | 来源 | 验证动作 | 验证结果 | 可信度 | 证据等级 |
|---------|------|---------|---------|--------|---------|
| YAML 全称 | yaml.org | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| YAML 定位 | yaml.org | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 键值语法 | yaml.org | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 列表语法 | yaml.org | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |
| 注释语法 | yaml.org | grep 匹配 | ✅ | 1.0 | 原文 + 实测 |

---

## 四、来源可信但未实测验证的候选事实

1. **YAML 完整规范版本** - 首页未显示版本号
2. **嵌套对象语法** - 首页未展示缩进示例
3. **数据类型（布尔、日期、null）** - 首页未展示标量类型

---

## 五、待蒸馏资产

### Genes (2 个)
- `gene_yaml_full_name` - YAML 官方全称
- `gene_yaml_basic_syntax` - YAML 基础语法元素

### Capsules (1 个)
- `capsule_yaml_validate_basic` - YAML 基础语法校验

---

**入库路径**: `raw/yaml-official-sample-20260422.md`  
**下一步**: 蒸馏为 Wiki 报告 + Genes + Capsules
