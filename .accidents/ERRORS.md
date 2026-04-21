## [ERR-20260317-001] Web UI 下载失败

**Logged**: 2026-03-17T20:30:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
无法下载 Yacd Web UI 文件，服务器无法访问 GitHub/CDN

### Error
```
curl: (28) Operation timed out after 60001 milliseconds
HTTP Error 404: Not Found
```

### Context
- 尝试下载源：GitHub, jsDelivr, gcore.jsdelivr.net
- 服务器位置：阿里云轻量应用服务器（中国大陆）
- 网络限制：无法直接访问 GitHub 和部分 CDN

### Suggested Fix
1. ✅ 已尝试 5 种下载方法
2. ⏳ 需要用户在本地下载后上传
3. ⏳ 或配置代理后下载

### Metadata
- Reproducible: yes
- Related Files: ~/.config/clash/ui/
- Tags: network, download, github-blocked

---

## [ERR-20260315-001] Playwright 安装失败

**Logged**: 2026-03-15T12:05:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
无法安装 Playwright，Python 版本过低

### Error
```
Playwright requires Python 3.8+
System Python: 3.6.8
```

### Context
- 系统 Python 版本：3.6.8
- Playwright 最低要求：Python 3.8+
- 影响：Day 1 学习任务无法继续

### Suggested Fix
1. ✅ 已记录多种解决方案
2. ⏳ 需要升级 Python 或安装 Node.js
3. ⏳ 或使用 Docker 方案

### Metadata
- Reproducible: yes
- Tags: python-version, dependency, playwright

---
