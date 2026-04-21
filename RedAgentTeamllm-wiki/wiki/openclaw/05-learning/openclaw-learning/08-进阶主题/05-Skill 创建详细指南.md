---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: 05 Skill 创建详细指南
type: article
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
# OpenClaw Skill 创建详细指南

**学习时间**: 2026-03-12 11:46
**难度**: ⭐⭐⭐⭐ 进阶
**预计时间**: 60 分钟

---

## 📚 Skill 概述

### 什么是 Skill

Skill 是模块化的知识包，每个 Skill 以 `SKILL.md` 文件定义，Agent 根据用户请求自动匹配并加载对应 Skill 执行任务。

### Skill 用途

- 扩展 Agent 功能
- 封装特定领域知识
- 提供可复用的工具

---

## 📁 Skill 结构

### 标准目录结构

```
my-skill/
├── SKILL.md           # 技能说明（必需）
├── index.js           # 技能主逻辑（必需）
├── package.json       # 依赖配置（推荐）
├── config.json        # 技能配置（可选）
└── assets/            # 资源文件（可选）
    └── ...
```

---

## 📝 SKILL.md 模板

```markdown
# 技能名称

**描述**: 一句话说明技能功能
**作者**: 你的名字
**版本**: 1.0.0

## 功能

- 功能点 1
- 功能点 2
- 功能点 3

## 触发关键词

- 关键词 1
- 关键词 2
- 关键词 3

## 使用示例

```
指令示例 1
指令示例 2
```

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| apiKey | string | - | API 密钥 |
| timeout | number | 5000 | 超时时间 |

## 依赖

- Node.js v18+
- 外部 API: xxx
```

---

## 💻 index.js 模板

### 基础模板

```javascript
/**
 * 技能名称：my-skill
 * 描述：我的第一个 OpenClaw 技能
 */

module.exports = {
  // 技能元数据
  meta: {
    name: 'my-skill',
    version: '1.0.0',
    description: '我的第一个技能',
    author: 'Your Name'
  },

  // 技能配置
  config: {
    enabled: true,
    triggerPatterns: [
      /我的技能/,
      /测试命令/
    ],
    defaultParam: 'default'
  },

  // 技能执行函数
  async execute(context, params) {
    const { message, tools, config } = context;
    
    // 1. 解析用户输入
    const userInput = message.content;
    
    // 2. 调用工具（如需要）
    // const result = await tools.web_search({ query: 'xxx' });
    
    // 3. 处理逻辑
    const response = `收到你的消息：${userInput}`;
    
    // 4. 返回结果
    return {
      content: response,
      type: 'text'
    };
  },

  // 技能初始化（可选）
  async init(config) {
    console.log('[my-skill] 初始化完成');
  },

  // 技能清理（可选）
  async destroy() {
    console.log('[my-skill] 清理完成');
  }
};
```

---

## 🛠️ 完整示例：天气查询 Skill

### SKILL.md

```markdown
# Weather Skill

**描述**: 查询天气信息
**作者**: Your Name
**版本**: 1.0.0

## 功能

- 查询指定城市天气
- 提供天气建议

## 触发关键词

- 天气
- 下雨
- 温度
- 气候

## 使用示例

```
北京今天天气怎么样？
上海会下雨吗？
```

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| defaultCity | string | 北京 | 默认城市 |
| units | string | metric | 温度单位 |
```

---

### index.js

```javascript
/**
 * 技能名称：weather-skill
 * 描述：天气查询技能
 */

const https = require('https');

module.exports = {
  meta: {
    name: 'weather-skill',
    version: '1.0.0',
    description: '天气查询技能',
    author: 'Your Name'
  },

  config: {
    enabled: true,
    triggerPatterns: [
      /天气/,
      /下雨/,
      /温度/,
      /气候/
    ],
    defaultCity: '北京',
    units: 'metric'
  },

  async execute(context, params) {
    const { message, config } = context;
    
    // 1. 提取城市名
    const city = this.extractCity(message.content) || config.defaultCity;
    
    // 2. 获取天气数据
    const weather = await this.fetchWeather(city);
    
    // 3. 生成回复
    const reply = this.formatWeather(weather, city);
    
    return { content: reply };
  },

  // 提取城市名
  extractCity(text) {
    const cities = ['北京', '上海', '广州', '深圳', '杭州'];
    for (const city of cities) {
      if (text.includes(city)) return city;
    }
    return null;
  },

  // 获取天气数据
  async fetchWeather(city) {
    return new Promise((resolve, reject) => {
      const url = `https://wttr.in/${city}?format=j1`;
      https.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            resolve({
              temp: json.current_condition[0].temp_C,
              weather: json.current_condition[0].weatherDesc[0].value,
              humidity: json.current_condition[0].humidity
            });
          } catch (e) {
            reject(e);
          }
        });
      }).on('error', reject);
    });
  },

  // 格式化输出
  formatWeather(data, city) {
    return `🌤️ ${city}天气信息\n\n` +
           `温度：${data.temp}°C\n` +
           `天气：${data.weather}\n` +
           `湿度：${data.humidity}%`;
  },

  async init(config) {
    console.log('[weather-skill] 初始化完成');
  }
};
```

---

## 📦 package.json 模板

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "我的 OpenClaw 技能",
  "main": "index.js",
  "scripts": {
    "test": "node test.js"
  },
  "keywords": ["openclaw", "skill"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "node-fetch": "^3.3.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

---

## 🧪 测试 Skill

### 本地测试脚本

```javascript
// test.js
const skill = require('./index');

async function test() {
  // 模拟上下文
  const context = {
    message: { content: '北京天气怎么样？' },
    tools: {},
    config: { defaultCity: '北京' }
  };

  // 执行技能
  const result = await skill.execute(context);
  
  console.log('测试结果:', result);
}

test().catch(console.error);
```

### 在 OpenClaw 中测试

```bash
# 1. 复制 Skill 到技能目录
cp -r my-skill ~/.openclaw/workspace/skills/

# 2. 启用技能
openclaw skills enable my-skill

# 3. 测试
openclaw chat "测试我的技能"
```

---

## 🚀 发布到 ClawHub

### 步骤 1: 准备发布

```bash
# 确保目录结构正确
# 确保 SKILL.md 完整
# 确保代码无错误
```

### 步骤 2: 安装 clawhub CLI

```bash
npm install -g clawhub
```

### 步骤 3: 登录

```bash
clawhub login
```

### 步骤 4: 发布

```bash
clawhub publish ./my-skill
```

### 步骤 5: 验证

```bash
clawhub search my-skill
```

---

## ⚠️ 最佳实践

### 1. 错误处理

```javascript
async execute(context, params) {
  try {
    return await this.doSomething();
  } catch (error) {
    console.error('[my-skill] 错误:', error);
    return {
      content: `❌ 出错了：${error.message}`,
      type: 'error'
    };
  }
}
```

---

### 2. 超时控制

```javascript
async execute(context, params) {
  const timeout = 10000;
  
  const result = await Promise.race([
    this.doSomething(),
    new Promise((_, reject) => 
      setTimeout(() => reject(new Error('超时')), timeout)
    )
  ]);
  
  return result;
}
```

---

### 3. 配置验证

```javascript
async init(config) {
  if (!config.apiKey) {
    throw new Error('缺少 apiKey 配置');
  }
  if (config.timeout < 1000) {
    throw new Error('timeout 不能小于 1000ms');
  }
}
```

---

### 4. 文档完整

- SKILL.md 详细清晰
- 包含使用示例
- 说明配置项
- 列出依赖

---

## ✅ 验收清单

- [ ] SKILL.md 已创建
- [ ] index.js 已实现
- [ ] 错误处理完善
- [ ] 本地测试通过
- [ ] OpenClaw 中测试通过
- [ ] 文档完整

---

**学习状态**: ✅ 已完成
**下一步**: 更新索引和统计


## 相關文檔

- [[05-evomap_asset_safe_submit]]
- [[05-openclaw_gateway_forward]]
- [[19-skill_adapter_layer_openclaw_http_cli_docker]]
