# goEX 目录结构说明

**整理时间**: 2026-04-22 03:40  
**整理人**: Red Agent Team

---

## 目录结构

```
/home/admin/.openclaw/workspace/goEX/
├── src/                    # 源代码目录
│   ├── main.go            # 主程序入口
│   ├── go.mod             # Go 模块依赖
│   ├── go.sum             # 依赖校验
│   ├── core/              # 核心配置
│   ├── engine/            # 浏览器引擎
│   │   ├── rod/           # Rod 引擎
│   │   └── chromedp/      # ChromeDP 引擎
│   ├── api/               # HTTP API
│   │   └── handler/       # 请求处理
│   ├── service/           # 业务服务
│   └── plugin/            # 插件系统
│
├── build/                  # 编译输出
│   └── goEX               # Linux 二进制文件 (12MB)
│
├── docs/                   # 文档目录
│   ├── README.md          # 项目说明
│   ├── feishu-bot.md      # 飞书集成文档
│   ├── goEX-Phase1-Completion-Report.md
│   ├── goEX-最终评估报告.md
│   ├── goEX-50 遍推演报告.md
│   ├── goEX-AI 辅助版.md
│   ├── goEX-AI 辅助版 - 完整细节.md
│   ├── goEX-Phase1-5 遍推演.md
│   ├── OPTIMIZATION_EVALUATION.md
│   ├── OPTIMIZATION-REPORT.md
│   └── goex-batch-report-*.md
│
├── config/                 # 配置文件
│   ├── config.yaml        # 主配置
│   └── goex.service       # systemd 服务配置
│
├── logs/                   # 日志目录
│   └── goex.log           # 运行日志
│
├── data/                   # 运行时数据
│   └── (空，运行时生成)
│
└── test/                   # 测试目录
    └── (空，待补充)
```

---

## 文件统计

| 目录 | 文件数 | 说明 |
|------|--------|------|
| src/ | 7 | 源代码 |
| build/ | 1 | 编译二进制 |
| docs/ | 11 | 文档报告 |
| config/ | 2 | 配置文件 |
| logs/ | 1 | 日志 |
| data/ | 0 | 运行时数据 |
| test/ | 0 | 待补充 |
| **总计** | **22** | 所有文件 |

---

## 管理原则

1. ✅ 所有 goEX 文件都在 `/home/admin/.openclaw/workspace/goEX/` 内
2. ✅ 不自创目录，不分散存放
3. ✅ 自包含，易管理，易删除
4. ✅ 删除时只需 `rm -rf /home/admin/.openclaw/workspace/goEX/`

---

**状态**: ✅ 整理完成
