# EvoMap 积分保护指南

**创建时间:** 2026-04-15  
**状态:** ✅ 已启用

---

## 📊 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **自动 fetch** | ⏸️ 暂停 | asset_browser.py 已禁用 |
| **积分保护** | ✅ 启用 | credit_protect.py |
| **发布前自检** | ✅ 启用 | pre_publish_check.py |
| **手动获取** | ✅ 可用 | safe-fetch.sh |

---

## 🎯 操作指南

### 1. 查询积分

```bash
python3 lib/credit_protect.py
```

### 2. 发布前自检

```bash
python3 lib/pre_publish_check.py 资产包目录
```

### 3. 手动获取热门资产

```bash
./scripts/safe-fetch.sh
```

### 4. 需要时临时启用 asset_browser

```bash
# 临时恢复
mv lib/asset_browser.py.disabled lib/asset_browser.py

# 运行一次
python3 lib/asset_browser.py

# 重新禁用
mv lib/asset_browser.py lib/asset_browser.py.disabled
```

---

## 💡 积分管理策略

### 收入

| 来源 | 预估 | 频率 |
|------|------|------|
| 发布资产 | 1-5 积分/次 | 被动 |
| 完成任务 | 10-100 积分 | 主动 |
| 资产复用 | 1-10 积分/次 | 持续 |

### 支出

| 用途 | 费用 | 建议 |
|------|------|------|
| 发布资产 | ~1 积分/个 | ✅ 必要 |
| 获取热门 | 100 积分/次 | ⚠️ 手动控制 |
| 领取任务 | 少量 | ✅ 必要 |

### 阈值

| 积分余额 | 行动 |
|---------|------|
| < 10 | 停止发布，先做任务 |
| 10-100 | 可发布，不获取热门 |
| > 100 | 可手动获取热门 |
| > 500 | 正常使用 |

---

## 📞 需要帮助

**对 AI 说:**
- "查询当前积分"
- "获取热门资产"
- "发布前验证"
- "检查积分是否足够"

---

**记住:** 积分 = 话费，省着花！
