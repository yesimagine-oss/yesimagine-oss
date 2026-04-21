package main

import (
	"math"
	"strings"
)

// SemanticSimilarity 語義相似度計算器
type SemanticSimilarity struct {
	threshold float64 // 相似度閾值，默认 0.85
}

// NewSemanticSimilarity 創建相似度計算器
func NewSemanticSimilarity() *SemanticSimilarity {
	return &SemanticSimilarity{
		threshold: 0.85, // 85% 相似度即視為相同
	}
}

// CosineSimilarity 計算兩個文本的餘弦相似度
// 簡化實現：基於詞頻向量
func (ss *SemanticSimilarity) CosineSimilarity(text1, text2 string) float64 {
	// 分詞 (中文按字符，英文按單詞)
	words1 := ss.tokenize(text1)
	words2 := ss.tokenize(text2)

	// 構建詞頻向量
	vector1 := ss.buildVector(words1)
	vector2 := ss.buildVector(words2)

	// 計算餘弦相似度
	return ss.cosine(vector1, vector2)
}

// tokenize 分詞 (簡化實現)
func (ss *SemanticSimilarity) tokenize(text string) []string {
	// 去除空白
	text = strings.TrimSpace(text)
	
	// 簡化分詞：按字符分割 (中文)
	// 生產環境應使用專業分詞庫 (如 jieba)
	chars := strings.Split(text, "")
	
	// 過濾空白字符
	result := []string{}
	for _, char := range chars {
		if strings.TrimSpace(char) != "" {
			result = append(result, char)
		}
	}
	
	return result
}

// buildVector 構建詞頻向量
func (ss *SemanticSimilarity) buildVector(words []string) map[string]int {
	vector := make(map[string]int)
	for _, word := range words {
		vector[word]++
	}
	return vector
}

// cosine 計算餘弦相似度
func (ss *SemanticSimilarity) cosine(vec1, vec2 map[string]int) float64 {
	// 計算點積
	dotProduct := 0
	for word, count1 := range vec1 {
		if count2, exists := vec2[word]; exists {
			dotProduct += count1 * count2
		}
	}

	// 計算模長
	magnitude1 := 0.0
	for _, count := range vec1 {
		magnitude1 += float64(count * count)
	}
	magnitude1 = math.Sqrt(magnitude1)

	magnitude2 := 0.0
	for _, count := range vec2 {
		magnitude2 += float64(count * count)
	}
	magnitude2 = math.Sqrt(magnitude2)

	// 避免除零
	if magnitude1 == 0 || magnitude2 == 0 {
		return 0.0
	}

	// 餘弦相似度
	return float64(dotProduct) / (magnitude1 * magnitude2)
}

// IsSimilar 判斷兩個文本是否相似
func (ss *SemanticSimilarity) IsSimilar(text1, text2 string) bool {
	similarity := ss.CosineSimilarity(text1, text2)
	return similarity >= ss.threshold
}

// FindSimilarQuery 在緩存中查找相似查詢
func (ss *SemanticSimilarity) FindSimilarQuery(query string, cache map[string]cacheEntry) (string, bool) {
	bestMatch := ""
	bestScore := 0.0

	for cachedQuery := range cache {
		score := ss.CosineSimilarity(query, cachedQuery)
		if score > bestScore && score >= ss.threshold {
			bestScore = score
			bestMatch = cachedQuery
		}
	}

	if bestMatch != "" {
		return bestMatch, true
	}

	return "", false
}
