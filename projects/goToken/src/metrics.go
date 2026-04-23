package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"time"
)

// MetricsCollector 監控指標收集器
type MetricsCollector struct {
	sync.RWMutex
	stats MetricsStats
}

// MetricsStats 指標統計
type MetricsStats struct {
	TotalRequests   int64 `json:"total_requests"`   // 總請求數
	CacheHits       int64 `json:"cache_hits"`       // 緩存命中數
	CacheMisses     int64 `json:"cache_misses"`     // 緩存未命中數
	APICalls        int64 `json:"api_calls"`        // API 調用數
	TokensSaved     int64 `json:"tokens_saved"`     // 節省 Token 數
	TokensConsumed  int64 `json:"tokens_consumed"`  // 消耗 Token 數
	AvgResponseTime int64 `json:"avg_response_time"`// 平均響應時間 (ms)
	StartTime       time.Time `json:"start_time"`   // 啟動時間
}

// NewMetricsCollector 創建指標收集器
func NewMetricsCollector() *MetricsCollector {
	return &MetricsCollector{
		stats: MetricsStats{
			StartTime: time.Now(),
		},
	}
}

// RecordRequest 記錄請求
func (mc *MetricsCollector) RecordRequest(hit bool, responseTimeMs int64, tokens int) {
	mc.Lock()
	defer mc.Unlock()

	mc.stats.TotalRequests++

	if hit {
		mc.stats.CacheHits++
	} else {
		mc.stats.CacheMisses++
		mc.stats.APICalls++
		mc.stats.TokensConsumed += int64(tokens)
		mc.stats.TokensSaved += int64(tokens) // 緩存命中時節省的 Token
	}

	// 計算加權平均響應時間
	total := mc.stats.TotalRequests
	currentAvg := mc.stats.AvgResponseTime
	mc.stats.AvgResponseTime = (currentAvg*(total-1) + responseTimeMs) / total
}

// GetStats 獲取統計數據
func (mc *MetricsCollector) GetStats() MetricsStats {
	mc.RLock()
	defer mc.RUnlock()
	return mc.stats
}

// GetCacheHitRate 獲取緩存命中率
func (mc *MetricsCollector) GetCacheHitRate() float64 {
	mc.RLock()
	defer mc.RUnlock()

	if mc.stats.TotalRequests == 0 {
		return 0.0
	}

	return float64(mc.stats.CacheHits) / float64(mc.stats.TotalRequests) * 100
}

// GetTokenSaveRate 獲取 Token 節省率
func (mc *MetricsCollector) GetTokenSaveRate() float64 {
	mc.RLock()
	defer mc.RUnlock()

	totalExpected := mc.stats.TokensConsumed + mc.stats.TokensSaved
	if totalExpected == 0 {
		return 0.0
	}

	return float64(mc.stats.TokensSaved) / float64(totalExpected) * 100
}

// ExportJSON 導出為 JSON
func (mc *MetricsCollector) ExportJSON() (string, error) {
	mc.RLock()
	defer mc.RUnlock()

	stats := mc.stats
	stats.StartTime = mc.stats.StartTime

	data, err := json.MarshalIndent(stats, "", "  ")
	if err != nil {
		return "", err
	}

	return string(data), nil
}

// ExportPrometheus 導出為 Prometheus 格式
func (mc *MetricsCollector) ExportPrometheus() string {
	mc.RLock()
	defer mc.RUnlock()

	stats := mc.stats

	return fmt.Sprintf(`# HELP tokensaver_total_requests Total number of requests
# TYPE tokensaver_total_requests counter
tokensaver_total_requests %d

# HELP tokensaver_cache_hits Total number of cache hits
# TYPE tokensaver_cache_hits counter
tokensaver_cache_hits %d

# HELP tokensaver_cache_misses Total number of cache misses
# TYPE tokensaver_cache_misses counter
tokensaver_cache_misses %d

# HELP tokensaver_api_calls Total number of API calls
# TYPE tokensaver_api_calls counter
tokensaver_api_calls %d

# HELP tokensaver_tokens_saved Total tokens saved
# TYPE tokensaver_tokens_saved counter
tokensaver_tokens_saved %d

# HELP tokensaver_tokens_consumed Total tokens consumed
# TYPE tokensaver_tokens_consumed counter
tokensaver_tokens_consumed %d

# HELP tokensaver_cache_hit_rate Cache hit rate (percentage)
# TYPE tokensaver_cache_hit_rate gauge
tokensaver_cache_hit_rate %.2f

# HELP tokensaver_token_save_rate Token save rate (percentage)
# TYPE tokensaver_token_save_rate gauge
tokensaver_token_save_rate %.2f

# HELP tokensaver_avg_response_time Average response time in milliseconds
# TYPE tokensaver_avg_response_time gauge
tokensaver_avg_response_time %d
`,
		stats.TotalRequests,
		stats.CacheHits,
		stats.CacheMisses,
		stats.APICalls,
		stats.TokensSaved,
		stats.TokensConsumed,
		mc.getHitRate(),
		mc.getSaveRate(),
		stats.AvgResponseTime,
	)
}

func (mc *MetricsCollector) getHitRate() float64 {
	if mc.stats.TotalRequests == 0 {
		return 0.0
	}
	return float64(mc.stats.CacheHits) / float64(mc.stats.TotalRequests) * 100
}

func (mc *MetricsCollector) getSaveRate() float64 {
	totalExpected := mc.stats.TokensConsumed + mc.stats.TokensSaved
	if totalExpected == 0 {
		return 0.0
	}
	return float64(mc.stats.TokensSaved) / float64(totalExpected) * 100
}

// SaveToFile 保存到文件
func (mc *MetricsCollector) SaveToFile(filepath string) error {
	jsonData, err := mc.ExportJSON()
	if err != nil {
		return err
	}

	return os.WriteFile(filepath, []byte(jsonData), 0644)
}

// PrintReport 打印報告
func (mc *MetricsCollector) PrintReport() {
	stats := mc.GetStats()
	hitRate := mc.GetCacheHitRate()
	saveRate := mc.GetTokenSaveRate()

	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("📊 goToken 監控報告")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("總請求數：%d\n", stats.TotalRequests)
	fmt.Printf("緩存命中：%d\n", stats.CacheHits)
	fmt.Printf("緩存未命中：%d\n", stats.CacheMisses)
	fmt.Printf("API 調用：%d\n", stats.APICalls)
	fmt.Printf("緩存命中率：%.2f%%\n", hitRate)
	fmt.Printf("Token 節省：%.2f%% (%d tokens)\n", saveRate, stats.TokensSaved)
	fmt.Printf("平均響應時間：%dms\n", stats.AvgResponseTime)
	fmt.Printf("運行時長：%v\n", time.Since(stats.StartTime))
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
}
