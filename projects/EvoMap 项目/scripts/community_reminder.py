#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 社區提醒腳本
每天 20:00 執行，提醒用戶參與社區互動
"""

import requests
import logging
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
EVO_API = "https://evomap.ai"

# 日誌配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "cron_community.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_node_stats():
    """獲取節點統計"""
    try:
        response = requests.get(
            f"{EVO_API}/a2a/nodes/{NODE_ID}",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"獲取統計失敗：{e}")
    return None

def send_reminder():
    """发送社區提醒"""
    logger.info("🌐 開始執行社區提醒...")
    
    stats = get_node_stats()
    
    message = f"""
## 🌐 EvoMap 社區互動提醒 — {datetime.now().strftime('%Y-%m-%d %H:%M')}

### 🎯 社區互動任務

1. **查看資產狀態**（優先級：🔴 高）
   - 檢查已提交資產的審核狀態
   - 回應社區反饋和評論
   - 參與相關討論

2. **Claim 新任務**（優先級：🟡 中）
   - 瀏覽開放任務列表
   - Claim 1-2 個匹配技能的任務
   - 目標：增加積分和聲譽

3. **社區參與**（優先級：🟡 中）
   - 回覆其他節點的問題
   - 分享經驗和最佳實踐
   - 建立社區影響力

### 📊 當前進度

| 項目 | 狀態 | 積分 |
|------|------|------|
| 發布 Capsule | ✅ 完成 | +20（待確認） |
| 提交任務 | ✅ 已提交 | +10-20（審核中） |
| 社區互動 | ⏳ 待執行 | +5-10 |

### ⏰ 今日時間安排

| 時間 | 任務 | 狀態 |
|------|------|------|
| 07:30 | 晨間檢查 | ✅ 已完成 |
| 17:25 | 任務提醒 | ✅ 已完成 |
| 17:30 | 自動 Claim | ✅ 已完成 |
| 18:10 | 創作提醒 | ✅ 已完成 |
| 20:00 | 社區互動 | 🔄 執行中 |
| 22:00 | 每日汇总 | ⏳ 等待中 |

**需要協助執行哪個任務？請回復任務編號。**
"""
    
    logger.info("✅ 社區提醒已發送")
    print(message)
    return message

if __name__ == "__main__":
    send_reminder()
