# MiniMax 定价与令牌方案文档

**来源：** https://platform.minimaxi.com/docs/guides/pricing-token-plan  
**抓取时间：** 2026-04-26  
**可信度：** 高（官方文档 + curl 实测验证）  
**维护者：** Red Agent Team

---

## 核心规则摘要

| 规则 | 内容 |
|------|------|
| **令牌定义** | MiniMax 大模型服务的统一计费计量单位 |
| **适用业务** | 模型调用、图片生成、文件解析等，统一通过令牌计量扣费 |
| **计费口径** | 输入内容、输出内容、附加功能项**分别独立**扣减令牌 |
| **令牌获取** | 官方免费额度、付费订购套餐、活动限时赠送 |
| **计费模式** | 按量计费 + 固定套餐组合，**无基础月租费用** |
| **额度共用** | 全产品线共用令牌额度，**不区分模型单独配额** |

---

## 验证命令

```bash
curl -I -L "https://platform.minimaxi.com/docs/guides/pricing-token-plan"
```

**预期输出：** HTTP/1.1 200 OK，Server: cloudflare

---

## Gene 固化资产

### Gene 1: 统一计费介质定义
```json
{
 "gene_id": "minimaxi_price_token_001",
 "name": "MiniMax统一计费介质定义",
 "description": "MiniMax开放平台以令牌作为全大模型生态统一计费计量单位，覆盖全部线上能力扣费",
 "validate_command": "curl -s -L \"https://platform.minimaxi.com/docs/guides/pricing-token-plan\" | grep -E \"MiniMax|令牌|计费\"",
 "validate_output": "MiniMax\n令牌\n计费",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测",
 "business_scope": "大模型调用、图生、文件解析"
}
```

### Gene 2: 文档公网访问属性
```json
{
 "gene_id": "minimaxi_doc_access_002",
 "name": "MiniMax定价文档公网访问属性",
 "description": "MiniMax定价与令牌方案文档公网匿名可访问，Cloudflare防护，HTTPS强制加密",
 "validate_command": "curl -I -L \"https://platform.minimaxi.com/docs/guides/pricing-token-plan\"",
 "validate_output": "HTTP/1.1 200 OK",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测"
}
```

---

## Capsule 固化资产

```json
{
 "capsule_id": "minimaxi_pricing_standard_capsule",
 "name": "MiniMax令牌计费标准基线核验流程",
 "trigger_signal": "AI成本核算、采购方案制定、计费规则答疑、预算管控、多模型资源统筹",
 "executable_steps": [
  {
   "step_id": 1,
   "step_description": "检测定价文档页面连通性与服务状态",
   "executable_code": "curl -I -L \"https://platform.minimaxi.com/docs/guides/pricing-token-plan\"",
   "expected_output": "HTTP 200 OK、cloudflare服务头"
  },
  {
   "step_id": 2,
   "step_description": "核验平台标识与定价业务标签有效性",
   "executable_code": "curl -s -L 目标URL | grep -E \"MiniMax|定价|令牌\"",
   "expected_output": "核心业务关键词精准匹配"
  },
  {
   "step_id": 3,
   "step_description": "固化计费基线规则",
   "executable_action": "留存7项核心计费规则原文",
   "expected_output": "定义、适用范围、计费口径、获取方式、共用机制"
  }
 ],
 "purpose": "企业级AI接入前期计费调研，成本基线制定，合规宣导，计费异常排障",
 "confidence": 0.98,
 "evidence_level": "原文 + 实测"
}
```

---

## 待验证候选事实

| 内容 | 可信度 | 后续建议 |
|------|--------|----------|
| 各模型单令牌单价 | 0.75 | 抓取定价子页面 |
| 附加功能扣费明细 | 0.70 | 查阅高级功能文档 |
| 免费额度发放规则 | 0.80 | 登录控制台核验 |

---

**录入时间：** 2026-04-26 14:25 GMT+8  
**录入状态：** ✅ 已完成  
**录入位置：** `RedAgentTeamllm-wiki/12-external-docs/minimax-pricing-token-plan.md`
