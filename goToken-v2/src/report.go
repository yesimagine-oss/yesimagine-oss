package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// TokenReport Token 使用报告
type TokenReport struct {
	Period       string  `json:"period"`        // 统计周期
	TotalReqs    int64   `json:"total_requests"`
	CacheHits    int64   `json:"cache_hits"`
	CacheMisses  int64   `json:"cache_misses"`
	HitRate      float64 `json:"hit_rate"`
	TokensSaved  int64   `json:"tokens_saved"`
	CostSaved    float64 `json:"cost_saved"` // 节省金额（元）
	Timestamp    string  `json:"timestamp"`
}

// SaveReport 保存报告
func SaveReport(report *TokenReport, path string) error {
	data, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		return fmt.Errorf("JSON 序列化失败：%v", err)
	}

	err = os.WriteFile(path, data, 0644)
	if err != nil {
		return fmt.Errorf("保存文件失败：%v", err)
	}

	fmt.Printf("📄 报告已保存：%s\n", path)
	return nil
}

// GenerateReport 生成报告
func GenerateReport(metricsPath string, reportPath string) error {
	// 读取监控数据
	data, err := os.ReadFile(metricsPath)
	if err != nil {
		return fmt.Errorf("读取监控数据失败：%v", err)
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
		return fmt.Errorf("解析监控数据失败：%v", err)
	}

	// 计算节省
	avgTokensPerReq := int64(800) // 假设每次 800 Token
	tokensPerYuan := int64(500000) // ¥1 = 50 万 Token（参考定价）

	tokensSaved := metrics.CacheHits * avgTokensPerReq
	costSaved := float64(tokensSaved) / float64(tokensPerYuan)

	// 创建报告
	report := &TokenReport{
		Period:      "自启动至今",
		TotalReqs:   metrics.TotalRequests,
		CacheHits:   metrics.CacheHits,
		CacheMisses: metrics.CacheMisses,
		HitRate:     metrics.HitRate,
		TokensSaved: tokensSaved,
		CostSaved:   costSaved,
		Timestamp:   time.Now().Format(time.RFC3339),
	}

	// 保存报告
	err = SaveReport(report, reportPath)
	if err != nil {
		return err
	}

	// 打印摘要
	fmt.Println("\n📊 goToken 统计报告")
	fmt.Println("================================")
	fmt.Printf("统计周期：%s\n", report.Period)
	fmt.Printf("总请求数：%d\n", report.TotalReqs)
	fmt.Printf("缓存命中：%d ✅\n", report.CacheHits)
	fmt.Printf("缓存未命中：%d\n", report.CacheMisses)
	fmt.Printf("命中率：%.1f%%\n", report.HitRate)
	fmt.Printf("节省 Token: %,d\n", report.TokensSaved)
	fmt.Printf("节省金额：¥%.2f\n", report.CostSaved)
	fmt.Println("================================")

	return nil
}

// GenerateCSVReport 生成 CSV 报告
func GenerateCSVReport(report *TokenReport, path string) error {
	csv := "指标，数值，说明\n"
	csv += fmt.Sprintf("总请求数，%d,统计周期内总请求\n", report.TotalReqs)
	csv += fmt.Sprintf("缓存命中，%d,从缓存返回的请求\n", report.CacheHits)
	csv += fmt.Sprintf("缓存未命中，%d,调用 API 的请求\n", report.CacheMisses)
	csv += fmt.Sprintf("命中率，%.1f%%,命中/总请求\n", report.HitRate)
	csv += fmt.Sprintf("节省 Token,%d,缓存命中节省的 Token\n", report.TokensSaved)
	csv += fmt.Sprintf("节省金额，¥%.2f,按¥1=50 万 Token 计算\n", report.CostSaved)
	csv += fmt.Sprintf("统计周期，%s,%s\n", report.Period, report.Timestamp)

	err := os.WriteFile(path, []byte(csv), 0644)
	if err != nil {
		return fmt.Errorf("保存 CSV 失败：%v", err)
	}

	fmt.Printf("📄 CSV 报告已保存：%s\n", path)
	return nil
}
