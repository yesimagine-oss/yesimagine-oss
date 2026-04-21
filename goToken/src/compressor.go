package main

import (
	"os"
	"strings"
)

// PromptCompressor 動態 Prompt 壓縮器
type PromptCompressor struct {
	maxTokens int
	scene     string // 場景：coding/chat/analysis
}

// Scene 場景常量
const (
	SceneCoding    = "coding"    // 代碼場景：保留更多上下文
	SceneChat      = "chat"      // 聊天場景：精簡為主
	SceneAnalysis  = "analysis"  // 分析場景：需要完整信息
	SceneDefault   = "default"   // 默認場景
)

// NewPromptCompressor 創建壓縮器
func NewPromptCompressor() *PromptCompressor {
	scene := os.Getenv("PROMPT_SCENE")
	if scene == "" {
		scene = SceneDefault
	}

	return &PromptCompressor{
		maxTokens: 300, // 默认值
		scene:     scene,
	}
}

// Compress 動態壓縮 Prompt (按場景自適應)
func (pc *PromptCompressor) Compress(query string) string {
	// 1. 去除多餘空白
	compressed := strings.Join(strings.Fields(query), " ")

	// 2. 按場景設置最大長度
	maxLen := pc.getMaxLenByScene()

	// 3. 截斷
	if len(compressed) > maxLen {
		compressed = compressed[:maxLen] + "..."
	}

	return compressed
}

// getMaxLenByScene 按場景獲取最大長度
func (pc *PromptCompressor) getMaxLenByScene() int {
	// 場景配置 (字符數)
	sceneConfig := map[string]int{
		SceneCoding:    500,  // 代碼需要更多上下文
		SceneChat:      150,  // 聊天精簡為主
		SceneAnalysis:  1000, // 分析需要完整信息
		SceneDefault:   300,  // 默認
	}

	if maxLen, exists := sceneConfig[pc.scene]; exists {
		return maxLen
	}

	return sceneConfig[SceneDefault]
}

// SetScene 設置場景
func (pc *PromptCompressor) SetScene(scene string) {
	pc.scene = scene
}

// SetMaxTokens 設置最大 Token 數
func (pc *PromptCompressor) SetMaxTokens(tokens int) {
	pc.maxTokens = tokens
}

// GetScene 獲取當前場景
func (pc *PromptCompressor) GetScene() string {
	return pc.scene
}

// AutoDetectScene 自動檢測場景 (簡化實現)
func (pc *PromptCompressor) AutoDetectScene(query string) string {
	query = strings.ToLower(query)

	// 關鍵詞檢測
	codingKeywords := []string{"代碼", "code", "function", "func", "var", "import", "package"}
	analysisKeywords := []string{"分析", "analyze", "compare", "evaluate", "評估"}

	// 檢測代碼場景
	for _, keyword := range codingKeywords {
		if strings.Contains(query, keyword) {
			return SceneCoding
		}
	}

	// 檢測分析場景
	for _, keyword := range analysisKeywords {
		if strings.Contains(query, keyword) {
			return SceneAnalysis
		}
	}

	// 默认聊天場景
	return SceneChat
}
