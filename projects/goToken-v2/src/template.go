package main

import (
	"regexp"
	"strings"
)

// TemplateRecognizer 模板識別器
type TemplateRecognizer struct {
	templates map[string]*regexp.Regexp
}

// NewTemplateRecognizer 創建模板識別器
func NewTemplateRecognizer() *TemplateRecognizer {
	tr := &TemplateRecognizer{
		templates: make(map[string]*regexp.Regexp),
	}
	
	// 註冊常見模板
	tr.registerDefaultTemplates()
	
	return tr
}

// registerDefaultTemplates 註冊默認模板 (v1.0.2 optimized: 10 大類)
func (tr *TemplateRecognizer) registerDefaultTemplates() {
	// 安裝類
	tr.templates["install"] = regexp.MustCompile(`(?i)(如何 | 怎麼 | 怎樣 | 方法).*(安裝 |install|setup| 部署)` )
	
	// 使用類
	tr.templates["usage"] = regexp.MustCompile(`(?i)(如何 | 怎麼 | 怎樣 | 方法).*(使用 |use|usage| 用 | 操作)` )
	
	// 配置類
	tr.templates["config"] = regexp.MustCompile(`(?i)(如何 | 怎麼 | 怎樣 | 方法).*(配置 |config|setup| 設置 | 設定)` )
	
	// 錯誤類
	tr.templates["error"] = regexp.MustCompile(`(?i)(錯誤 |error|fail| 失敗 | 報錯 | 出錯 | 異常 |exception)` )
	
	// 性能類
	tr.templates["performance"] = regexp.MustCompile(`(?i)(性能 | 速度 | 優化 |optimize|performance| 提升 | 加速)` )
	
	// 比較類
	tr.templates["compare"] = regexp.MustCompile(`(?i)(比較 |compare|vs| 哪個好 | 區別 | 差異 | 對比)` )
	
	// 排查類
	tr.templates["troubleshoot"] = regexp.MustCompile(`(?i)(排查 | 診斷 |debug| 檢查 | 查看 | 為什麼 |why)` )
	
	// 最佳實踐類
	tr.templates["bestpractice"] = regexp.MustCompile(`(?i)(最佳實踐 |best practice| 推薦 | 建議 | 應該)` )
	
	// 集成類
	tr.templates["integration"] = regexp.MustCompile(`(?i)(集成 | 整合 | 對接 |integrate| 接入 | 接入)` )
	
	// 部署類
	tr.templates["deployment"] = regexp.MustCompile(`(?i)(部署 | 發布 | 上線 |deploy| 安裝 | 配置)` )
}

// ExtractTemplatePattern 提取模板模式
func (tr *TemplateRecognizer) ExtractTemplatePattern(query string) string {
	// 1. 轉換為小寫
	query = strings.ToLower(query)
	
	// 2. 移除具體名詞 (保留動詞和疑問詞)
	query = tr.removeNouns(query)
	
	// 3. 標準化疑問詞
	query = tr.normalizeQuestionWords(query)
	
	// 4. 移除空白
	query = strings.Join(strings.Fields(query), " ")
	
	return query
}

// removeNouns 移除具體名詞 (簡化實現)
func (tr *TemplateRecognizer) removeNouns(query string) string {
	// 常見產品名詞 (應替換為 <PRODUCT>)
	products := []string{
		"openclaw", "tokensaver", "evomap", "evolver",
		"go", "python", "javascript", "typescript",
		"linux", "windows", "macos",
	}
	
	result := query
	for _, product := range products {
		result = strings.ReplaceAll(result, product, "<PRODUCT>")
	}
	
	return result
}

// normalizeQuestionWords 標準化疑問詞
func (tr *TemplateRecognizer) normalizeQuestionWords(query string) string {
	// 標準化疑問詞
	replacements := map[string]string{
		"怎麼": "如何",
		"怎樣": "如何",
		"用":    "使用",
		"設置": "配置",
		"設定": "配置",
	}
	
	result := query
	for old, new := range replacements {
		result = strings.ReplaceAll(result, old, new)
	}
	
	return result
}

// GetTemplateType 獲取模板類型
func (tr *TemplateRecognizer) GetTemplateType(query string) string {
	for templateType, pattern := range tr.templates {
		if pattern.MatchString(query) {
			return templateType
		}
	}
	
	return "unknown"
}

// IsTemplateQuery 判斷是否為模板化查詢
func (tr *TemplateRecognizer) IsTemplateQuery(query string) bool {
	templateType := tr.GetTemplateType(query)
	return templateType != "unknown"
}

// GenerateCacheKey 生成緩存 Key (結合模板 + 語義)
func (tr *TemplateRecognizer) GenerateCacheKey(query string) string {
	// 1. 提取模板模式
	pattern := tr.ExtractTemplatePattern(query)
	
	// 2. 獲取模板類型
	templateType := tr.GetTemplateType(query)
	
	// 3. 組合 Key
	if templateType != "unknown" {
		return templateType + ":" + pattern
	}
	
	return "exact:" + pattern
}
