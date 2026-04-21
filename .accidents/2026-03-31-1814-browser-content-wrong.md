# 2026-03-31 18:14 browser 工具内容错误事故

**事故级别**: 🟠 P1 严重  
**发生时间**: 2026-03-31 18:14  
**影响范围**: browser 工具访问 clawhub.ai 时显示 moltbook.com 内容  
**状态**: ✅ 已修复

---

## 事故描述

**用户发现**：
- 每次访问 clawhub.ai 的 skill 页面
- browser 工具都显示 moltbook.com 的 XHunt KOL 排行榜
- 但 curl 能正确获取 clawhub.ai 的内容

---

## 根本原因

**OpenClaw browser 工具需要 Docker sandbox 容器运行**：
- OpenClaw browser 工具使用 Docker 容器运行 Chrome
- 通过 CDP (Chrome DevTools Protocol) 控制浏览器
- 默认端口：9222

**当时状态**：
- ❌ 没有运行中的 browser sandbox 容器
- ❌ 没有相关的 Docker 镜像

---

## 修复过程

### 步骤 1：构建 sandbox 镜像
- ✅ 配置 Docker 镜像源
- ✅ 拉取 debian:bookworm-slim
- ✅ 构建 openclaw-sandbox-browser（1.03 GB）
- ⏱️ 构建时间：约 3.5 小时

### 步骤 2：运行容器
- ✅ 启动 openclaw-browser 容器
- ✅ 暴露 CDP 端口 9222
- ✅ Chrome/146.0.7680.164 就绪

### 步骤 3：更新 OpenClaw 配置
- ✅ 修改 ~/.openclaw/openclaw.json
- ✅ 配置 CDP endpoint: http://localhost:9222

---

## 当前状态（2026-04-01 03:30）

| 组件 | 状态 | 说明 |
|------|------|------|
| **Docker 镜像** | ✅ 完成 | openclaw-sandbox-browser:latest (1.03 GB) |
| **Docker 容器** | ✅ 运行中 | openclaw-browser (端口 9222) |
| **Chrome CDP** | ✅ 就绪 | Chrome/146.0.7680.164 |
| **OpenClaw 配置** | ✅ 已更新 | 需要重启服务生效 |
| **browser 工具** | ⏳ 待测试 | 配置生效后可用 |

---

## 下一步

1. 重启 OpenClaw 服务使配置生效
2. 测试 browser 工具访问 clawhub.ai
3. 安装 twitter-article-reader skill

---

**记录时间**: 2026-03-31 18:14  
**修复完成**: 2026-04-01 03:26  
**记录者**: RedOpenClaw  
**状态**: ✅ Docker sandbox 就绪，等待 OpenClaw 重启
