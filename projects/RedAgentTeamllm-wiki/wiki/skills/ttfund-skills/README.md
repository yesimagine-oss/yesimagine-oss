---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
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
# 天天基金 Skills

天天基金 API 集成技能，支持基金信息查询和条件选基。

## 安装

技能已位于：`~/.openclaw/workspace/skills/ttfund-skills/`

## 配置

### 1. 设置 API Key

```bash
# 临时设置（当前会话有效）
export TTFUND_APIKEY='ttf_sk_live_01KNDHQGMK89Q6BE15ECT949C4.qrY5GFmSGVDcdpX5hHdlmTPwhCzpiar1ykp_yKkDEPs'

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo "export TTFUND_APIKEY='ttf_sk_live_01KNDHQGMK89Q6BE15ECT949C4.qrY5GFmSGVDcdpX5hHdlmTPwhCzpiar1ykp_yKkDEPs'" >> ~/.bashrc
source ~/.bashrc
```

### 2. 获取 API Key（如需更新）

1. 打开天天基金 App
2. 搜索 `skills`
3. 在对应 Skills 页面获取 apikey

## 使用方法

### 方式一：命令行调用

```bash
# 查询基金信息
python3 ~/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py info --fcode 000006

# 条件选基
python3 ~/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py select --params '{"pageIndex":1,"pageNum":20}'
```

### 方式二：Python 导入

```python
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/skills/ttfund-skills')

from ttfund_client import query_fund_info, select_funds, format_fund_info

# 查询基金信息
result = query_fund_info("000006")
print(format_fund_info(result))

# 条件选基
params = {
    "pageIndex": 1,
    "pageNum": 20,
    "fundLevel": "4,5",
    "riskLevel": "3,4"
}
result = select_funds(params)
print(result)
```

### 方式三：OpenClaw Agent 调用

在 Agent 中直接导入使用：

```python
from ttfund_client import query_fund_info, select_funds
```

## API 说明

### 1. 天天基金信息 skill (FUND_BASE_INFOS)

查询基金基础信息，包括：
- 基金名称、代码、公司
- 单位净值、累计净值
- 风险等级、成立日期
- 阶段收益、波动率、最大回撤

**参数**:
- `fcode` (必填): 基金代码，例如 "000006"

**示例**:
```python
result = query_fund_info("000006")
```

### 2. 天天条件选基 skill (FUND_CONDITION_SELECT)

根据条件筛选基金，支持：
- 基金分类、风险等级
- 基金规模、费率
- 收益率、波动率、最大回撤
- 定投表现等

**参数** (常用):
- `pageIndex`: 页码 (默认 1)
- `pageNum`: 每页数量 (默认 20)
- `fundLevel`: 基金评级 ("4,5" 表示 4-5 星)
- `riskLevel`: 风险等级 ("3,4" 表示中高风险)
- `rsfType`: 基金分类一级
- `rsbType`: 基金分类二级
- `stageSyl`: 阶段收益率 ("6_0_50" 表示近 1 年 0-50%)

**示例**:
```python
# 筛选 4-5 星、中高风险的基金
params = {
    "pageIndex": 1,
    "pageNum": 20,
    "fundLevel": "4,5",
    "riskLevel": "3,4",
    "orderField": "5_6_-1"  # 按近 1 年收益率倒序
}
result = select_funds(params)
```

## 返回结果

### 基金信息接口

```json
{
  "success": true,
  "skill_id": "FUND_BASE_INFOS",
  "skill_name": "天天基金信息 skill",
  "data": {
    "errorCode": 0,
    "success": true,
    "totalCount": 1,
    "data": [{
      "FCODE": "000006",
      "SHORTNAME": "南方成长",
      "JJGS": "南方基金",
      "DWJZ": "1.2345",
      ...
    }]
  }
}
```

### 条件选基接口

```json
{
  "success": true,
  "skill_id": "FUND_CONDITION_SELECT",
  "skill_name": "天天条件选基 skill",
  "data": {
    "ErrCode": 0,
    "Succeed": true,
    "TotalCount": 156,
    "Data": [{
      "fundCode": "000006",
      "fundName": "南方成长",
      "company": "南方基金",
      "yearSyl": "15.6",
      ...
    }]
  }
}
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 缺少 TTFUND_APIKEY | 未配置环境变量 | 执行 `export TTFUND_APIKEY='...'` |
| HTTP 错误：401 | API Key 无效 | 检查 API Key 是否正确 |
| HTTP 错误：429 | 请求过于频繁 | 等待后重试 |
| 请求超时 | 网络问题 | 检查网络连接 |
| 业务错误 | 参数错误 | 检查基金代码或筛选条件 |

## 注意事项

1. **API Key 安全**: 不要将 API Key 提交到代码仓库
2. **速率限制**: 避免短时间内大量请求
3. **数据用途**: 返回数据仅供参考，不构成投资建议
4. **网络环境**: 服务器需要能访问 `skills.tiantianfunds.com`

## 文件结构

```
ttfund-skills/
├── ttfund-client.py    # 客户端库
├── README.md           # 本文档
└── SKILL.md            # OpenClaw 技能定义
```

## 版本

- 当前版本：1.0.0
- 最后更新：2026-04-05


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
