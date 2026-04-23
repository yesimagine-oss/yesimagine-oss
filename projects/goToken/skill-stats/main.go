package main

import (
	"encoding/json"
	"fmt"
	"os"
	"openclaw-gateway/skill"
	"strings"
)

func GoTokenStatsSkill(ctx *skill.Context) error {
	metricsFile := "/home/admin/.openclaw/workspace/goToken/logs/metrics.json"
	
	// 讀取指標文件
	data, err := os.ReadFile(metricsFile)
	if err != nil {
		return ctx.Reply("⚠️ 暫無統計數據\ngoToken 可能尚未運行")
	}
	
	var metrics struct {
		TotalRequests int64   `json:"total_requests"`
		CacheHits     int64   `json:"cache_hits"`
		CacheMisses   int64   `json:"cache_misses"`
		HitRate       float64 `json:"hit_rate"`
		Timestamp     string  `json:"timestamp"`
	}
	
	err = json.Unmarshal(data, &metrics)
	if err != nil {
		return ctx.Reply("❌ 讀取統計失敗")
	}
	
	// 計算 Token 節省
	expectedTokens := metrics.TotalRequests * 800
	actualTokens := metrics.CacheMisses * 800
	savedTokens := expectedTokens - actualTokens
	savedCost := float64(savedTokens) * 0.002 / 1000
	
	// 狀態標識
	status := "⚠️"
	if metrics.HitRate >= 85 {
		status = "🟢"
	} else if metrics.HitRate >= 75 {
		status = "🟡"
	}
	
	// 格式化回復
	reply := fmt.Sprintf(`📊 **goToken Token 節省看板** %s

**運行統計**
━━━━━━━━━━━━━━━━
總請求數：%d
緩存命中：%d ✅
緩存未命中：%d
命中率：**%.1f%%**

**Token 節省**
━━━━━━━━━━━━━━━━
預期消耗：%,d tokens
實際消耗：%,d tokens
節省 Token: **%,d tokens** ✅
節省比例：**%.1f%%**
節省金額：**¥%.2f**

**狀態**
━━━━━━━━━━━━━━━━
目標：≥75%
當前：%s %.1f%%`,
		status,
		metrics.TotalRequests,
		metrics.CacheHits,
		metrics.CacheMisses,
		metrics.HitRate,
		expectedTokens,
		actualTokens,
		savedTokens,
		metrics.HitRate,
		savedCost,
		status,
		metrics.HitRate)
	
	return ctx.Reply(reply)
}

func main() {
	skill.Register("gotoken_stats", GoTokenStatsSkill)
	skill.Run()
}
