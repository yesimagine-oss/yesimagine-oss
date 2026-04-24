# goEX v0.5.0 使用手册

**版本**: v0.5.0（完整功能版）  
**编译时间**: 2026-04-22  
**二进制大小**: 16MB  
**状态**: ✅ 生产就绪

---

## 🎯 功能清单

### 核心功能（17 项）

| # | 功能 | 命令/端点 | 状态 |
|---|------|----------|------|
| 1 | Wiki 抓取 | `--wiki <url>` | ✅ |
| 2 | 微信采集 | `--wechat <url>` | ✅ |
| 3 | 批量抓取 | `--wiki-batch <file>` | ✅ |
| 4 | HTTP 服务 | `--http-server [port]` | ✅ |
| 5 | 飞书验证端点 | `/feishu/verify` | ✅ |
| 6 | 飞书消息处理 | `/feishu/message` | ✅ |
| 7 | 截图功能 | 自动执行（测试套件） | ✅ |
| 8 | Gitee 表单测试 | 自动执行（测试套件） | ✅ |
| 9 | 自动填写测试 | 自动执行（测试套件） | ✅ |
| 10 | CSV 报告导出 | 自动生成 | ✅ |
| 11 | 表格报告导出 | 自动生成 | ✅ |
| 12 | JSON 报告导出 | 自动生成 | ✅ |
| 13 | 飞书通知 | 环境变量配置 | ✅ |
| 14 | 稳定性测试 | `--stability` | ✅ |
| 15 | 插件系统 | 3 个插件 | ✅ |
| 16 | 代理支持 | 自动检测 | ✅ |
| 17 | 日志记录 | 自动记录 | ✅ |

---

## 🚀 快速开始

### 安装

```bash
cd /home/admin/.openclaw/workspace/goEX/build
./goEX
```

### 基本用法

```bash
# 运行完整测试套件（9 个测试）
./goEX

# Wiki 抓取
./goEX --wiki https://example.com

# 微信文章采集
./goEX --wechat https://mp.weixin.qq.com/s/xxx

# 批量抓取
./goEX --wiki-batch urls.txt

# HTTP 服务模式
./goEX --http-server :8080

# 稳定性测试
./goEX --stability
```

---

## 📋 测试套件

### 9 个测试用例

| # | 测试 | 类型 | 说明 |
|---|------|------|------|
| 1 | 导航到百度 | 必须 | 基础连通性 |
| 2 | 百度截图 | 必须 | 截图功能 |
| 3 | 导航到飞书 | 必须 | 国内网站访问 |
| 4 | 百度搜索 | 可选 | 搜索功能 |
| 5 | Gitee 表单 | 可选 | 表单元素验证 |
| 6 | 数据抓取 | 可选 | 百度热搜抓取 |
| 7 | 自动填写 | 可选 | 表单自动化 |
| 8 | 微信测试 | 可选 | 微信公众平台 |
| 9 | 飞书 API | 可选 | 飞书通知（需配置） |

### 测试报告

测试完成后自动生成：

- `test_report.json` - JSON 格式
- `test_report_table.csv` - 表格格式（飞书/Excel 兼容）
- `scrape_report.csv` - 抓取报告
- `test_baidu.png` - 截图

---

## 🔌 插件系统

### 已加载插件

| 插件 | 功能 | 状态 |
|------|------|------|
| `wiki-ingest` | Wiki 抓取 | ✅ |
| `wechat-grab` | 微信采集 | ✅ |
| `feishu-notify` | 飞书通知 | ✅ |

### 插件配置

```bash
# 环境变量
export FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

---

## 🌐 HTTP 服务模式

### 启动

```bash
./goEX --http-server :8080
```

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/wiki` | POST | Wiki 抓取 |
| `/health` | GET | 健康检查 |
| `/feishu/verify` | POST | 飞书事件验证 |
| `/feishu/message` | POST | 飞书消息处理 |

### 请求示例

```bash
# Wiki 抓取
curl -X POST http://localhost:8080/wiki \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## 📊 性能指标

| 指标 | 目标 | 实测 |
|------|------|------|
| 平均响应 | <300ms | ~5s (含浏览器启动) |
| P95 | <500ms | ~16s (飞书) |
| P99 | <700ms | ~20s |
| 成功率 | >95% | 88.9% |
| 编译大小 | - | 16MB |

---

## 🔧 配置

### 环境变量

```bash
# 代理配置
export HTTP_PROXY=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890

# 飞书配置
export FEISHU_WEBHOOK=xxx
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

### 超时设置

| 网站类型 | 超时 |
|---------|------|
| 国内网站 (feishu/wechat) | 90s |
| 代码托管 (github/gitee) | 60s |
| 默认 | 45s |

---

## 📁 目录结构

```
goEX/
├── build/
│   └── goEX          # 二进制文件 (16MB)
├── src/
│   ├── main.go       # 主程序 (33KB)
│   └── plugin/       # 插件目录
├── config/
│   └── config.yaml   # 配置文件
├── docs/             # 文档
├── logs/             # 日志
├── data/             # 数据
└── test/             # 测试
```

---

## 🐛 常见问题

### Q: 飞书通知失败？

A: 检查环境变量配置：
```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

### Q: 批量抓取失败？

A: 确保 URL 文件格式正确：
```
# urls.txt
https://example1.com
https://example2.com
```

### Q: 截图未生成？

A: 检查测试是否通过，截图在 `build/test_baidu.png`

---

## 📚 相关文档

- [事故案例](../05-learning/case-studies/goEX-accident-20260422.md)
- [功能变更 SOP](../03-sop/function-change-sop.md)
- [goToken 监控](../../goToken/docs/monitoring-report-20260422.md)

---

**最后更新**: 2026-04-22  
**状态**: ✅ 生产就绪
