# 飞书社区集成类Wiki文档

**来源：** https://larkcommunity.feishu.cn/wiki/GGJPwJ2IfiTynVk2Vy4cZbRvn2f  
**抓取时间：** 2026-04-26  
**可信度：** 高（官方文档 + curl 实测验证）  
**维护者：** Red Agent Team

---

## 核心属性

| 属性 | 内容 |
|------|------|
| **域名** | larkcommunity.feishu.cn |
| **文档类型** | 公开只读Wiki（免登录可访问） |
| **内容范畴** | 第三方集成指南、生态协作方案、社区实践案例、配置说明、问题汇总 |

---

## 验证命令

```bash
curl -I -L "https://larkcommunity.feishu.cn/wiki/GGJPwJ2IfiTynVk2Vy4cZbRvn2f"
```

**预期输出：** HTTP/1.1 200 OK，HSTS + X-Frame-Options 安全响应头

---

## Gene 固化资产

### Gene 1: 社区Wiki域名资产
```json
{
 "gene_id": "larkcommunity_wiki_001",
 "name": "飞书社区Wiki专属域名资产",
 "description": "larkcommunity.feishu.cn 为飞书官方社区专属域名，承载公开共享类Wiki协作文档与生态资料",
 "validate_command": "curl -s -L \"https://larkcommunity.feishu.cn/wiki/GGJPwJ2IfiTynVk2Vy4cZbRvn2f\" | grep -E \"larkcommunity|feishu.cn|wiki\"",
 "validate_output": "larkcommunity.feishu.cn\nfeishu.cn\nwiki",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测",
 "asset_type": "社区公开知识库"
}
```

### Gene 2: 安全访问属性
```json
{
 "gene_id": "larkcommunity_wiki_access_002",
 "name": "飞书社区Wiki文档安全访问属性",
 "description": "飞书社区公开Wiki文档公网匿名无鉴权访问，HTTP 200正常响应，配置HSTS、X-Frame-Options安全防护策略",
 "validate_command": "curl -I -L \"https://larkcommunity.feishu.cn/wiki/GGJPwJ2IfiTynVk2Vy4cZbRvn2f\"",
 "validate_output": "HTTP/1.1 200 OK",
 "confidence": 1.0,
 "evidence_level": "原文 + 实测"
}
```

---

## Capsule 固化资产

```json
{
 "capsule_id": "larkcommunity_wiki_archive_capsule",
 "name": "飞书社区公开Wiki文档核验与归档流程",
 "trigger_signal": "生态集成配置、协作方案查阅、社区案例参考、通用问题排障、共享知识库沉淀",
 "executable_steps": [
  {
   "step_id": 1,
   "step_description": "探测飞书社区Wiki文档连通性与服务状态",
   "executable_code": "curl -I -L \"https://larkcommunity.feishu.cn/wiki/GGJPwJ2IfiTynVk2Vy4cZbRvn2f\"",
   "expected_output": "HTTP/1.1 200 OK、安全响应头完整返回"
  },
  {
   "step_id": 2,
   "step_description": "核验社区域名、wiki服务、知识库核心标识",
   "executable_code": "curl -s -L 目标URL | grep -E \"larkcommunity|wiki|知识库\"",
   "expected_output": "三项核心标识精准命中"
  },
  {
   "step_id": 3,
   "step_description": "留存文档公开属性与内容分类原文",
   "executable_action": "归档页面原始定位描述与内容覆盖范围",
   "expected_output": "文档属性+内容分类原文完整留存"
  }
 ],
 "purpose": "第三方集成实施、企业协作优化、共性问题答疑、社区共享文档统一台账管理",
 "confidence": 0.98,
 "evidence_level": "原文 + 实测"
}
```

---

## 待验证候选事实

| 内容 | 可信度 | 后续建议 |
|------|--------|----------|
| 公开文档访问权限规则 | 0.85 | 周期复测访问状态 |
| 第三方集成实操步骤 | 0.80 | 抓取文档完整正文 |
| 社区案例复用标准 | 0.75 | 递进抓取案例详情 |

---

**录入时间：** 2026-04-26  
**录入位置：** `12-external-docs/larkcommunity-wiki-integration.md`
