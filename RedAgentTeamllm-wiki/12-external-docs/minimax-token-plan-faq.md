# MiniMax 令牌套餐 FAQ 文档

**来源：** https://platform.minimaxi.com/docs/token-plan/faq  
**抓取时间：** 2026-04-26  
**可信度：** 高（官方文档 + curl 实测验证）  
**维护者：** Red Agent Team

---

## 核心规则摘要

| 规则 | 内容 |
|------|------|
| **付费令牌有效期** | 12 个月 |
| **免费令牌有效期** | 以平台展示为准（有期限限制） |
| **令牌消耗差异** | 不同模型、不同接口消耗数量不同 |
| **长文本/多轮会话** | 会增加令牌消耗 |
| **套餐叠加** | 多份可叠加，额度与有效期自动叠加计算 |
| **退款政策** | 虚拟令牌商品一经售出概不支持退款，活动特惠无额外售后 |

---

## 额度查询入口

**路径：** 控制台 → 账单 → 令牌中心

**验证命令：**
```bash
curl -I -L "https://platform.minimaxi.com/docs/token-plan/faq"
```

**预期输出：** HTTP/1.1 200 OK，Server: cloudflare

---

## Gene 固化资产

### Gene 1: 令牌FAQ文档标识
```json
{
 "gene_id": "minimaxi_token_faq_platform_01",
 "name": "MiniMax开放平台令牌FAQ文档标识",
 "description": "MiniMax开放平台令牌套餐专属FAQ文档，承载令牌有效期、消耗、叠加、退款、查询全维度规则定义",
 "validate_command": "curl -s -L \"https://platform.minimaxi.com/docs/token-plan/faq\" | grep -E \"MiniMax|令牌套餐|FAQ\"",
 "validate_output": "MiniMax\n令牌套餐\nFAQ",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测",
 "business_domain": "大模型令牌计费与额度管理"
}
```

### Gene 2: 页面访问可用性
```json
{
 "gene_id": "minimaxi_faq_access_02",
 "name": "MiniMax文档页面公共访问可用性",
 "description": "MiniMax开放平台令牌FAQ页面公网可匿名访问，HTTP 200正常响应，Cloudflare安全防护常驻",
 "validate_command": "curl -I -L \"https://platform.minimaxi.com/docs/token-plan/faq\"",
 "validate_output": "HTTP/1.1 200 OK",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测"
}
```

---

## Capsule 固化资产

```json
{
 "capsule_id": "minimaxi_token_rule_check_capsule",
 "name": "MiniMax令牌套餐规则查阅与核验流程",
 "trigger_signal": "大模型采购、额度管理、计费排障、套餐叠加规则咨询场景",
 "executable_steps": [
  {
   "step_id": 1,
   "step_description": "探测MiniMax令牌FAQ页面连通性",
   "executable_code": "curl -I -L \"https://platform.minimaxi.com/docs/token-plan/faq\"",
   "expected_output": "HTTP/1.1 200 OK、cloudflare服务头"
  },
  {
   "step_id": 2,
   "step_description": "核验文档业务归属与分类标识",
   "executable_code": "curl -s -L 目标URL | grep -E \"MiniMax|令牌套餐\"",
   "expected_output": "平台名称+业务分类关键词精准命中"
  },
  {
   "step_id": 3,
   "step_description": "摘录固化核心计费规则：有效期、消耗、叠加、退款",
   "executable_action": "留存页面原文FAQ条目，作为合规与运维标准依据",
   "expected_output": "5项核心FAQ规则原文完整留存"
  }
 ],
 "purpose": "用于AI业务令牌成本管控、套餐采购决策、用户咨询答疑、计费纠纷排障标准化依据",
 "confidence": 0.98,
 "evidence_level": "原文 + 实测"
}
```

---

## 待验证候选事实

| 内容 | 可信度 | 后续建议 |
|------|--------|----------|
| 免费令牌具体时效 | 0.85 | 登录控制台核验 |
| 长文本/多轮会话消耗倍率 | 0.80 | 接口实测 |
| 控制台查询路径实景 | 0.82 | 登录后台核对 |

---

**录入时间：** 2026-04-26 14:19 GMT+8  
**录入状态：** ✅ 已完成  
**录入位置：** `RedAgentTeamllm-wiki/12-external-docs/minimax-token-plan-faq.md`
