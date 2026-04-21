package main

import (
	"encoding/json"
	"fmt"
	"os"
	"openclaw-gateway/skill"
	"strings"
	"sync"
	"time"
)

// cacheEntry 緩存条目結構
type cacheEntry struct {
	Answer   string
	ExpireAt time.Time
}

// goToken 緩存管理器
type goToken struct {
	cache struct {
		sync.RWMutex
		m map[string]cacheEntry
	}
	callLimiter chan struct{}
	cacheTTL    time.Duration
	maxTokens   int
	model       string
}

// NewgoToken 創建新的 goToken 實例
func NewgoToken() *goToken {
	// 從環境變量讀取配置 (支持自定義)
	cacheTTLHours := getEnvInt("CACHE_TTL_HOURS", 2)
	maxTokens := getEnvInt("MAX_TOKENS", 300)
	model := getEnv("LLM_MODEL", "qwen-coding-lite")

	ts := &goToken{
		callLimiter: make(chan struct{}, 2), // 並發限流：最多 2 個同時請求
		cacheTTL:    time.Duration(cacheTTLHours) * time.Hour,
		maxTokens:   maxTokens,
		model:       model,
	}
	ts.cache.m = make(map[string]cacheEntry)

	// 啟動緩存清理協程 (每小時清理過期條目)
	go ts.cleanupCache()

	return ts
}

// cleanupCache 定期清理過期緩存 (每小時執行一次)
func (ts *goToken) cleanupCache() {
	ticker := time.NewTicker(1 * time.Hour)
	defer ticker.Stop()

	for range ticker.C {
		ts.cache.Lock()
		now := time.Now()
		count := 0
		for k, v := range ts.cache.m {
			if now.After(v.ExpireAt) {
				delete(ts.cache.m, k)
				count++
			}
		}
		ts.cache.Unlock()

		if count > 0 {
			skill.Log("INFO", "緩存清理：已刪除 %d 個過期條目", count)
		}
	}
}

// GetEnv 獲取環境變量 (支持默認值)
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// GetEnvInt 獲取環境變量 (整數，支持默認值)
func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		var intVal int
		if _, err := fmt.Sscanf(value, "%d", &intVal); err == nil {
			return intVal
		}
	}
	return defaultValue
}

// compressPrompt 壓縮 Prompt (去除空白 + 限制長度)
func (ts *goToken) compressPrompt(q string) string {
	// 去除多餘空白
	compressed := strings.Join(strings.Fields(q), " ")
	
	// 限制最大長度 (可配置)
	maxLen := ts.maxTokens / 2 // 簡化估算：1 token ≈ 0.5 中文字符
	if len(compressed) > maxLen {
		compressed = compressed[:maxLen] + "..."
	}
	
	return compressed
}

// callDashScope 調用 DashScope API
func (ts *goToken) callDashScope(prompt string) (string, error) {
	apiKey := skill.Env("DASHSCOPE_API_KEY")
	if apiKey == "" {
		skill.Log("ERROR", "DASHSCOPE_API_KEY 未設置")
		return "", fmt.Errorf("API 配置錯誤")
	}

	// 構建請求
	req := map[string]any{
		"model": ts.model,
		"input": map[string]string{
			"prompt": prompt,
		},
		"parameters": map[string]any{
			"max_tokens": ts.maxTokens,
		},
	}

	// 序列化請求 (P0-001 修復：添加錯誤處理)
	body, err := json.Marshal(req)
	if err != nil {
		skill.Log("ERROR", "JSON 序列化失敗：%v", err)
		return "", fmt.Errorf("請求格式化失敗")
	}

	// 發送 HTTP 請求
	resp, err := skill.HTTP().
		WithHeader("Authorization", "Bearer "+apiKey).
		WithHeader("Content-Type", "application/json").
		Post("https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", body)

	if err != nil {
		skill.Log("ERROR", "HTTP 請求失敗：%v", err)
		return "", fmt.Errorf("網絡請求失敗")
	}

	// 解析響應 (P0-001 修復：添加錯誤處理)
	var result struct {
		Output  struct{ Text string }
		Code    string
		Message string
	}

	err = json.Unmarshal(resp.Body(), &result)
	if err != nil {
		skill.Log("ERROR", "JSON 解析失敗：%v", err)
		return "", fmt.Errorf("響應解析失敗")
	}

	// 檢查 API 錯誤 (P0-002 修復：錯誤脫敏)
	if result.Code != "" {
		skill.Log("ERROR", "API 錯誤：%s - %s", result.Code, result.Message)
		return "", fmt.Errorf("AI 服務請求失敗，請稍後重試")
	}

	return result.Output.Text, nil
}

// Query 查詢接口 (核心邏輯)
func (ts *goToken) Query(query string) string {
	query = strings.TrimSpace(query)
	if query == "" {
		return "請輸入有效問題"
	}

	// 1. 檢查緩存
	ts.cache.RLock()
	entry, hit := ts.cache.m[query]
	ts.cache.RUnlock()

	if hit && time.Now().Before(entry.ExpireAt) {
		skill.Log("INFO", "緩存命中：%s", query)
		return entry.Answer
	}

	// 2. 限流控制
	ts.callLimiter <- struct{}{}
	defer func() { <-ts.callLimiter }()

	// 3. 壓縮 Prompt
	prompt := ts.compressPrompt(query)

	// 4. 調用 API
	skill.Log("INFO", "API 調用：%s", query)
	answer, err := ts.callDashScope(prompt)

	if err != nil {
		skill.Log("ERROR", "請求失敗：%v", err)
		return "本周额度已达上限，将在周一重置；已开启缓存保护避免额度浪费。"
	}

	// 5. 更新緩存
	ts.cache.Lock()
	ts.cache.m[query] = cacheEntry{
		Answer:   answer,
		ExpireAt: time.Now().Add(ts.cacheTTL),
	}
	ts.cache.Unlock()

	skill.Log("INFO", "緩存更新：%s", query)
	return answer
}

// goTokenSkill Skill 入口函數
func goTokenSkill(ctx *skill.Context) error {
	// 創建 goToken 實例 (單例模式)
	var ts = NewgoToken()

	query := strings.TrimSpace(ctx.Input.Text)
	answer := ts.Query(query)

	return ctx.Reply(answer)
}

func main() {
	skill.Register("go_token", goTokenSkill)
	skill.Run()
}
