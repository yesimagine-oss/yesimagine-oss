#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 創作提醒腳本
每天 18:10 執行，提醒用戶進行內容創作
"""

import requests
import logging
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"

# 日誌配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "cron_content.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def send_reminder():
    """发送創作提醒"""
    logger.info("📝 開始執行創作提醒...")
    
    message = f"""
## 📋 EvoMap 創作提醒 — {datetime.now().strftime('%Y-%m-%d %H:%M')}

### 🎯 今日創作任務

1. **發布 Capsule**（優先級：🔴 高）
   - 狀態：✅ 已完成第一個 Capsule
   - Bundle ID: `bundle_e027d9fdcbff3948`
   - 下一步：提交到相關任務

2. **內容創作**（優先級：🟡 中）
   - 選題建議：
     - 《EvoMap 新手入門完整指南》
     - 《GEP-A2A 協議實戰解析》
     - 《如何用 EvoMap 實現知識變現》
   - 目標：建立個人品牌，吸引複用流量

3. **Bounty 任務**（優先級：🟡 中）
   - 當前狀態：已提交 1 個任務（審核中）
   - 今日目標：Claim 1-2 個新任務

### 📊 當前進度

| 項目 | 狀態 | 積分 |
|------|------|------|
| 發布 Capsule | ✅ 完成 | +20（待確認） |
| 提交任務 | ✅ 已提交 | +10-20（審核中） |
| Claim 新任務 | ⏳ 待執行 | - |

### ⏰ 今日時間安排

| 時間 | 任務 | 狀態 |
|------|------|------|
| 18:10 | 創作提醒 | ✅ 已執行 |
| 20:00 | 社區互動 | ⏳ 等待中 |
| 22:00 | 每日汇总 | ⏳ 等待中 |

**需要協助執行哪個任務？請回復任務編號。**
"""
    
    logger.info("✅ 創作提醒已發送")
    print(message)
    return message

if __name__ == "__main__":
    send_reminder()
