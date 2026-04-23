package main

import (
	"fmt"
	"sort"
	"strings"
)

// AdvancedSimilarity 高級語義相似度 (V3.0)
// 整合：詞頻 + 編輯距離 + 關鍵詞匹配
type AdvancedSimilarity struct {
	threshold    float64
	useEditDist  bool   // 是否使用編輯距離
	useKeywords  bool   // 是否使用關鍵詞匹配
	minChars     int    // 最小字符數 (低於此值使用精確匹配)
}

// NewAdvancedSimilarity 創建高級相似度計算器
func NewAdvancedSimilarity() *AdvancedSimilarity {
	threshold := 0.70  // v1.0.2 optimized: 穩定在 75%
	return &AdvancedSimilarity{
		threshold:   threshold,
		useEditDist: true,
		useKeywords: true,
		minChars:    3,
	}
}

// CalculateSimilarity 綜合相似度計算 (加權平均)
func (as *AdvancedSimilarity) CalculateSimilarity(text1, text2 string) float64 {
	// 1. 預處理
	t1 := as.preprocess(text1)
	t2 := as.preprocess(text2)

	// 2. 短文本使用精確匹配
	if len(t1) < as.minChars || len(t2) < as.minChars {
		if t1 == t2 {
			return 1.0
		}
		return 0.0
	}

	// 3. 計算各項相似度
	scores := []float64{}
	weights := []float64{}

	// 3.1 餘弦相似度 (詞頻)
	cosineScore := as.cosineSimilarity(t1, t2)
	scores = append(scores, cosineScore)
	weights = append(weights, 0.5) // 50% 權重

	// 3.2 編輯距離相似度
	if as.useEditDist {
		editScore := as.editDistanceSimilarity(t1, t2)
		scores = append(scores, editScore)
		weights = append(weights, 0.3) // 30% 權重
	}

	// 3.3 關鍵詞匹配相似度
	if as.useKeywords {
		keywordScore := as.keywordSimilarity(t1, t2)
		scores = append(scores, keywordScore)
		weights = append(weights, 0.2) // 20% 權重
	}

	// 4. 加權平均
	return as.weightedAverage(scores, weights)
}

// preprocess 預處理文本
func (as *AdvancedSimilarity) preprocess(text string) string {
	// 轉小寫
	text = strings.ToLower(text)
	
	// 去除空白
	text = strings.TrimSpace(text)
	
	// 去除標點
	text = strings.Map(func(r rune) rune {
		if r >= 'a' && r <= 'z' || r >= 'A' && r <= 'Z' || r >= '0' && r <= '9' || r >= '\u4e00' && r <= '\u9fff' {
			return r
		}
		return ' '
	}, text)
	
	// 標準化空白
	text = strings.Join(strings.Fields(text), " ")
	
	return text
}

// cosineSimilarity 餘弦相似度 (詞頻)
func (as *AdvancedSimilarity) cosineSimilarity(t1, t2 string) float64 {
	words1 := strings.Fields(t1)
	words2 := strings.Fields(t2)

	vec1 := make(map[string]int)
	vec2 := make(map[string]int)

	for _, w := range words1 {
		vec1[w]++
	}
	for _, w := range words2 {
		vec2[w]++
	}

	dot := 0
	for w, c1 := range vec1 {
		if c2, ok := vec2[w]; ok {
			dot += c1 * c2
		}
	}

	mag1 := 0.0
	for _, c := range vec1 {
		mag1 += float64(c * c)
	}
	mag1 = sqrt(mag1)

	mag2 := 0.0
	for _, c := range vec2 {
		mag2 += float64(c * c)
	}
	mag2 = sqrt(mag2)

	if mag1 == 0 || mag2 == 0 {
		return 0.0
	}

	return float64(dot) / (mag1 * mag2)
}

// editDistanceSimilarity 編輯距離相似度
func (as *AdvancedSimilarity) editDistanceSimilarity(t1, t2 string) float64 {
	if len(t1) == 0 || len(t2) == 0 {
		return 0.0
	}

	distance := as.levenshteinDistance(t1, t2)
	maxLen := len(t1)
	if len(t2) > maxLen {
		maxLen = len(t2)
	}

	return 1.0 - float64(distance)/float64(maxLen)
}

// levenshteinDistance 計算編輯距離
func (as *AdvancedSimilarity) levenshteinDistance(s1, s2 string) int {
	if len(s1) == 0 {
		return len(s2)
	}
	if len(s2) == 0 {
		return len(s1)
	}

	// 創建矩陣
	matrix := make([][]int, len(s1)+1)
	for i := range matrix {
		matrix[i] = make([]int, len(s2)+1)
		matrix[i][0] = i
	}
	for j := range matrix[0] {
		matrix[0][j] = j
	}

	// 填充矩陣
	for i := 1; i <= len(s1); i++ {
		for j := 1; j <= len(s2); j++ {
			cost := 1
			if s1[i-1] == s2[j-1] {
				cost = 0
			}
			matrix[i][j] = min(
				matrix[i-1][j]+1,      // 刪除
				matrix[i][j-1]+1,      // 插入
				matrix[i-1][j-1]+cost, // 替換
			)
		}
	}

	return matrix[len(s1)][len(s2)]
}

// keywordSimilarity 關鍵詞匹配相似度
func (as *AdvancedSimilarity) keywordSimilarity(t1, t2 string) float64 {
	// 定義關鍵詞類別
	questionWords := map[string]bool{
		"如何": true, "怎麼": true, "怎樣": true, "什麼": true,
		"how": true, "what": true, "why": true, "when": true,
	}

	actionWords := map[string]bool{
		"安裝": true, "使用": true, "配置": true, "設置": true,
		"install": true, "use": true, "config": true, "setup": true,
	}

	words1 := strings.Fields(t1)
	words2 := strings.Fields(t2)

	// 統計關鍵詞匹配
	qMatch := 0
	aMatch := 0

	for _, w := range words1 {
		if questionWords[w] {
			for _, w2 := range words2 {
				if questionWords[w2] {
					qMatch++
					break
				}
			}
		}
		if actionWords[w] {
			for _, w2 := range words2 {
				if actionWords[w2] {
					aMatch++
					break
				}
			}
		}
	}

	// 計算匹配率
	totalKeywords := 0
	if len(words1) > 0 {
		totalKeywords++
	}
	if len(words2) > 0 {
		totalKeywords++
	}

	if totalKeywords == 0 {
		return 0.0
	}

	return float64(qMatch+aMatch) / float64(totalKeywords*2)
}

// weightedAverage 加權平均
func (as *AdvancedSimilarity) weightedAverage(scores, weights []float64) float64 {
	if len(scores) != len(weights) || len(scores) == 0 {
		return 0.0
	}

	sum := 0.0
	weightSum := 0.0

	for i := range scores {
		sum += scores[i] * weights[i]
		weightSum += weights[i]
	}

	if weightSum == 0 {
		return 0.0
	}

	return sum / weightSum
}

// FindBestMatch 在緩存中查找最佳匹配
func (as *AdvancedSimilarity) FindBestMatch(query string, cache map[string]cacheEntry) (string, float64, bool) {
	bestMatch := ""
	bestScore := 0.0

	for cachedQuery := range cache {
		score := as.CalculateSimilarity(query, cachedQuery)
		if score > bestScore {
			bestScore = score
			bestMatch = cachedQuery
		}
	}

	if bestScore >= as.threshold {
		return bestMatch, bestScore, true
	}

	return "", bestScore, false
}

// SetThreshold 設置閾值
func (as *AdvancedSimilarity) SetThreshold(threshold float64) {
	as.threshold = threshold
}

// DebugSimilarity 調試輸出 (用於優化)
func (as *AdvancedSimilarity) DebugSimilarity(t1, t2 string) string {
	t1Proc := as.preprocess(t1)
	t2Proc := as.preprocess(t2)

	cosine := as.cosineSimilarity(t1Proc, t2Proc)
	edit := as.editDistanceSimilarity(t1Proc, t2Proc)
	keyword := as.keywordSimilarity(t1Proc, t2Proc)
	combined := as.CalculateSimilarity(t1, t2)

	return fmt.Sprintf(`相似度分析:
  原始文本 1: %s
  原始文本 2: %s
  預處理 1: %s
  預處理 2: %s
  餘弦相似度：%.2f
  編輯距離：%.2f
  關鍵詞匹配：%.2f
  綜合相似度：%.2f
  閾值：%.2f
  匹配結果：%v`,
		t1, t2, t1Proc, t2Proc,
		cosine, edit, keyword, combined,
		as.threshold, combined >= as.threshold)
}

// 輔助函數
func sqrt(x float64) float64 {
	if x == 0 {
		return 0
	}
	z := x
	for i := 0; i < 10; i++ {
		z = (z + x/z) / 2
	}
	return z
}

func min(nums ...int) int {
	if len(nums) == 0 {
		return 0
	}
	m := nums[0]
	for _, n := range nums[1:] {
		if n < m {
			m = n
		}
	}
	return m
}

// SortMatches 排序匹配結果 (用於調試)
type MatchResult struct {
	Query string
	Score float64
}

func SortMatches(matches []MatchResult) {
	sort.Slice(matches, func(i, j int) bool {
		return matches[i].Score > matches[j].Score
	})
}
