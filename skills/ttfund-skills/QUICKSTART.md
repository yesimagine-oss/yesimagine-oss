# 天天基金 Skills - 快速开始

## ✅ 安装完成

**安装位置**: `/home/admin/.openclaw/workspace/skills/ttfund-skills/`

**包含文件**:
- `ttfund-client.py` - Python 客户端库
- `README.md` - 完整文档
- `SKILL.md` - OpenClaw 技能定义

## 🚀 立即使用

### 方法 1: 命令行

```bash
# 加载环境变量
source ~/.bashrc

# 查询基金信息
python3 ~/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py info --fcode 000006

# 条件选基（筛选 4-5 星基金）
python3 ~/.openclaw/workspace/skills/ttfund-skills/ttfund-client.py select --params '{"fundLevel":"4,5","pageNum":10}'
```

### 方法 2: Python 代码

```python
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/skills/ttfund-skills')

from ttfund_client import query_fund_info, select_funds, format_fund_info, format_fund_select

# 查询单只基金
result = query_fund_info("000006")
print(format_fund_info(result))

# 条件选基
params = {
    "pageIndex": 1,
    "pageNum": 20,
    "fundLevel": "4,5",
    "riskLevel": "3,4",
    "orderField": "5_6_-1"  # 按近 1 年收益率倒序
}
result = select_funds(params)
print(format_fund_select(result))
```

### 方法 3: OpenClaw Agent

在 Agent 中直接使用:

```python
# 导入客户端
from ttfund_client import query_fund_info, select_funds

# 查询基金
fund = query_fund_info("000006")
```

## 📊 功能说明

### 1. 基金信息查询 (FUND_BASE_INFOS)

查询基金详细信息:
- 基本信息：代码、名称、公司、类型
- 净值：单位净值、累计净值
- 风险：风险等级、波动率、最大回撤
- 收益：近一周、近一年、成立以来收益
- 定投表现：普通/智能/目标止盈定投收益

**示例**:
```bash
python3 ttfund-client.py info --fcode 000006
```

### 2. 条件选基 (FUND_CONDITION_SELECT)

多维度筛选基金:
- 基金评级：1-5 星
- 风险等级：低/中低/中/中高/高
- 基金规模：小型/中型/大型
- 收益率：阶段收益、年化收益
- 排名：同类排名、年度排名
- 风险指标：波动率、最大回撤、夏普比率

**示例**:
```bash
# 筛选 4-5 星、中高风险基金，按近 1 年收益排序
python3 ttfund-client.py select --params '{
  "fundLevel": "4,5",
  "riskLevel": "3,4",
  "orderField": "5_6_-1",
  "pageNum": 20
}'
```

## 🔑 API Key 配置

**当前状态**: ✅ 已配置到 `~/.bashrc`

**手动配置**:
```bash
export TTFUND_APIKEY='ttf_sk_live_01KNDHQGMK89Q6BE15ECT949C4.qrY5GFmSGVDcdpX5hHdlmTPwhCzpiar1ykp_yKkDEPs'
```

**获取新 Key**:
1. 打开天天基金 App
2. 搜索 `skills`
3. 在 Skills 页面获取 apikey

## 📝 常用筛选参数

```json
{
  "pageIndex": 1,
  "pageNum": 20,
  "fundLevel": "4,5",
  "riskLevel": "3,4",
  "fundSize": "2,3",
  "establishPeriod": "2",
  "orderField": "5_6_-1",
  "stageSyl": "6_0_50",
  "sharpRanking": "6_0_20"
}
```

**参数说明**:
- `fundLevel`: 基金评级 ("4,5" = 4-5 星)
- `riskLevel`: 风险等级 ("3,4" = 中高风险)
- `fundSize`: 基金规模 ("2,3" = 中型/大型)
- `establishPeriod`: 成立年限 ("2" = 3-5 年)
- `orderField`: 排序字段 ("5_6_-1" = 近 1 年收益倒序)
- `stageSyl`: 阶段收益 ("6_0_50" = 近 1 年 0-50%)
- `sharpRanking`: 夏普比率排名 ("6_0_20" = 近 1 年前 20%)

## ⚠️ 注意事项

1. **API Key 安全**: 不要泄露给他人
2. **速率限制**: 避免短时间内大量请求
3. **数据用途**: 仅供参考，不构成投资建议
4. **网络环境**: 需要能访问 `skills.tiantianfunds.com`

## 🐛 故障排查

**问题 1: 缺少 TTFUND_APIKEY**
```bash
source ~/.bashrc
echo $TTFUND_APIKEY  # 检查是否设置
```

**问题 2: HTTP 401 错误**
- API Key 无效或过期
- 重新获取并更新环境变量

**问题 3: 请求超时**
- 检查网络连接
- 服务器可能暂时不可用

## 📚 完整文档

查看 `README.md` 获取详细 API 文档和参数说明。

---

**安装时间**: 2026-04-05  
**版本**: 1.0.0  
**状态**: ✅ 运行正常
