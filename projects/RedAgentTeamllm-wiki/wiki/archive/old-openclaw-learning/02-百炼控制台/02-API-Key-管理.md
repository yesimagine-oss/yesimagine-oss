---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: 02 Api Key 管理
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
# 百炼控制台 - API Key 管理与配置

**学习时间**: 2026-03-12 10:45

---

## 🔑 获取 API Key 流程

### 步骤 1: 登录控制台
1. 访问 https://bailian.console.aliyun.com
2. 使用阿里云账号登录

### 步骤 2: 进入 API Key 管理
1. 点击左侧菜单「API-KEY 管理」
2. 或访问：https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan

### 步骤 3: 创建新 Key
1. 点击「创建新的 API-KEY」
2. 输入名称（如：openclaw-main）
3. 选择权限范围（建议最小权限原则）
4. 确认创建

### 步骤 4: 保存 Key
- ⚠️ **重要**: API Key 只显示一次！
- 立即复制并安全保存
- 建议存入密码管理器

---

## 🔐 安全最佳实践

| 实践 | 说明 |
|------|------|
| 最小权限 | 只授予必要的权限 |
| 定期轮换 | 每 3-6 个月更换一次 |
| 环境隔离 | 开发/生产使用不同 Key |
| 保密存储 | 不要提交到代码仓库 |
| 监控用量 | 定期检查异常调用 |

---

## 💰 计费说明

### Coding Plan 计费模式
- 按 token 计费
- 输入 token + 输出 token 分别计费
- 具体价格查看控制台「计费管理」

### 免费额度
- 新注册用户可能有免费体验额度
- 查看「资源包」页面

### 用量监控
- 控制台可查看每日/每月用量
- 可设置用量告警

---

## 📝 OpenClaw 配置示例

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      }
    }
  }
}
```

---

## ⚠️ 常见问题

### Q: API Key 失效了怎么办？
A: 在控制台删除旧 Key，创建新 Key，然后更新配置文件

### Q: 如何查看用量？
A: 控制台 → 计费管理 → 用量明细

### Q: Key 泄露了怎么办？
A: 立即在控制台删除该 Key，创建新 Key 替换

---

**学习状态**: ✅ 已完成
**下一步**: OpenClaw 安装部署


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[asset07_api_batch_optimize]]
