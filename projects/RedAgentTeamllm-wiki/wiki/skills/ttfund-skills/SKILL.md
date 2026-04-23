---
category: llm
created_at: '2026-04-14'
tags:
- llm
- skill
- md
- 天天基金
- skills
title: Skill
type: general
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
# SKILL.md - 天天基金 Skills

## 技能信息

- **名称**: 天天基金 Skills
- **版本**: 1.0.0
- **类型**: 基金查询与筛选
- **状态**: ✅ 已安装

## 功能

### 1. 基金基础信息查询 (FUND_BASE_INFOS)

通过基金代码查询基金详细信息：

**支持查询**:
- 基金基本信息（代码、名称、公司、类型）
- 净值信息（单位净值、累计净值、净值日期）
- 风险指标（风险等级、波动率、最大回撤）
- 收益表现（近一周、近一年、成立以来收益）
- 费率信息（申购费率、赎回费率）
- 定投表现（普通定投、智能定投、目标止盈定投等）

**使用示例**:
```python
from ttfund_client import query_fund_info, format_fund_info

result = query_fund_info("000006")
print(format_fund_info(result))
```

### 2. 条件选基 (FUND_CONDITION_SELECT)

根据多维度条件筛选基金：

**支持筛选条件**:
- 基金分类（一级、二级分类）
- 基金评级（1-5 星）
- 风险等级（低、中低、中、中高、高）
- 基金规模（小型、中型、大型）
- 成立年限
- 收益率（阶段收益、年化收益、逐年收益）
- 排名（同类排名、年度排名）
- 风险指标（波动率、最大回撤、夏普比率）
- 定投表现
- 持仓特征（行业、股票集中度、换手率）
- 费率（申购费、管理费、赎回费）

**使用示例**:
```python
from ttfund_client import select_funds, format_fund_select

params = {
    "pageIndex": 1,
    "pageNum": 20,
    "fundLevel": "4,5",        # 4-5 星基金
    "riskLevel": "3,4",        # 中高风险
    "orderField": "5_6_-1"     # 按近 1 年收益率倒序
}
result = select_funds(params)
print(format_fund_select(result))
```

## 配置要求

### 环境变量

必须设置 `TTFUND_APIKEY`:

```bash
export TTFUND_APIKEY='ttf_sk_live_01KNDHQGMK89Q6BE15ECT949C4.qrY5GFmSGVDcdpX5hHdlmTPwhCzpiar1ykp_yKkDEPs'
```

### API Key 获取

1. 打开天天基金 App
2. 搜索 `skills`
3. 在对应 Skills 页面获取 apikey

### 系统要求

- Python 3.7+
- requests 库
- 能访问 `https://skills.tiantianfunds.com`

## 调用规范

### 1. API Key 检查

每次调用前必须检查 `TTFUND_APIKEY` 环境变量：

```python
import os

api_key = os.environ.get("TTFUND_APIKEY")
if not api_key:
    raise ValueError("未配置 TTFUND_APIKEY 环境变量")
```

### 2. 请求格式

所有请求必须包含:
- `skill_id`: 技能标识
- `_skill_version`: 技能版本 (固定为 "1.0.0")

### 3. 错误处理

- HTTP 错误：提示网络问题
- 业务错误 (errorCode/ErrCode != 0): 提示具体错误信息
- 数据为空：提示检查参数

## 输出规范

### 基金信息输出

优先展示核心字段:
- 基金代码、名称、公司
- 单位净值、累计净值
- 风险等级
- 近一周/近一年收益
- 最大回撤、波动率

### 条件选基输出

优先展示:
- 符合条件的基金总数
- 前 10 只基金的核心信息
- 每只基金：代码、名称、公司、类型、收益、评级

## 安全与边界

- ✅ 返回的是公开基金信息，不涉及用户隐私
- ✅ 仅用于基金查询、对比和辅助分析
- ❌ 不作为收益承诺或投资建议
- ❌ 不伪造结果或输出未验证内容

## 文件位置

- 客户端库：`/home/admin/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py`
- 文档：`/home/admin/.openclaw/workspace/skills/ttfund-skills/README.md`

## 测试命令

```bash
# 设置环境变量
export TTFUND_APIKEY='ttf_sk_live_01KNDHQGMK89Q6BE15ECT949C4.qrY5GFmSGVDcdpX5hHdlmTPwhCzpiar1ykp_yKkDEPs'

# 测试基金查询
python3 /home/admin/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py info --fcode 000006

# 测试条件选基
python3 /home/admin/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py select --params '{"pageIndex":1,"pageNum":5}'
```

## 版本历史

- **v1.0.0** (2026-04-05): 初始版本
  - 支持基金基础信息查询
  - 支持条件选基
  - 完整的错误处理和格式化输出

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]
