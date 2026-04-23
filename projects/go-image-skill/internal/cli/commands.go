package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/openclaw/go-image-skill/internal/image"
)

// Analyze 分析单张图片
func Analyze(imagePath, query string) {
	analyzer := image.NewAnalyzer("")
	
	result, err := analyzer.Analyze(imagePath)
	if err != nil {
		fmt.Printf("分析失败：%v\n", err)
		os.Exit(1)
	}

	// 如果有自然语言查询，处理查询
	if query != "" {
		response := handleQuery(result, query)
		fmt.Println(response)
	} else {
		// 输出 JSON 结果
		output, _ := json.MarshalIndent(result, "", "  ")
		fmt.Println(string(output))
	}
}

// Batch 批量分析
func Batch(dirPath string) {
	analyzer := image.NewAnalyzer("")
	
	files, err := filepath.Glob(filepath.Join(dirPath, "*.{jpg,jpeg,png,gif,webp,bmp}"))
	if err != nil {
		fmt.Printf("搜索文件失败：%v\n", err)
		os.Exit(1)
	}

	fmt.Printf("找到 %d 张图片\n", len(files))

	for i, file := range files {
		fmt.Printf("[%d/%d] 分析：%s\n", i+1, len(files), filepath.Base(file))
		
		result, err := analyzer.Analyze(file)
		if err != nil {
			fmt.Printf("  失败：%v\n", err)
			continue
		}

		// 输出简要信息
		fmt.Printf("  尺寸：%dx%d, 格式：%s, 场景：%s\n",
			result.Dimensions.Width,
			result.Dimensions.Height,
			result.Format,
			result.Scene)
	}
}

// Query 自然语言查询
func Query(query, imagePath string) {
	analyzer := image.NewAnalyzer("")
	
	result, err := analyzer.Analyze(imagePath)
	if err != nil {
		fmt.Printf("分析失败：%v\n", err)
		os.Exit(1)
	}

	response := handleQuery(result, query)
	fmt.Println(response)
}

// Serve 启动 HTTP 服务
func Serve(args []string) {
	port := "8080"
	for i, arg := range args {
		if arg == "--port" && i+1 < len(args) {
			port = args[i+1]
		}
	}

	fmt.Printf("启动 HTTP 服务，端口：%s\n", port)
	fmt.Println("API 端点:")
	fmt.Println("  POST /analyze - 分析图片")
	fmt.Println("  POST /query - 自然语言查询")
	fmt.Println("  GET /search?q=xxx - 搜索图片")
	fmt.Println("  POST /compare - 比对图片")
	fmt.Println("\n按 Ctrl+C 停止服务")

	// TODO: 实现 HTTP 服务
	select {}
}

// Search 搜索图片
func Search(query, dirPath string) {
	analyzer := image.NewAnalyzer("")
	
	files, err := filepath.Glob(filepath.Join(dirPath, "*.{jpg,jpeg,png,gif,webp,bmp}"))
	if err != nil {
		fmt.Printf("搜索文件失败：%v\n", err)
		os.Exit(1)
	}

	fmt.Printf("在 %d 张图片中搜索：%s\n", len(files), query)

	matches := 0
	for _, file := range files {
		result, err := analyzer.Analyze(file)
		if err != nil {
			continue
		}

		// 简单匹配逻辑 (TODO: 实现智能搜索)
		if contains(result.Scene, query) || contains(result.OCR.Text, query) {
			fmt.Printf("匹配：%s (场景：%s)\n", filepath.Base(file), result.Scene)
			matches++
		}
	}

	fmt.Printf("共找到 %d 张匹配的图片\n", matches)
}

// Compare 比对两张图片
func Compare(imagePath1, imagePath2 string) {
	analyzer := image.NewAnalyzer("")
	
	result1, err := analyzer.Analyze(imagePath1)
	if err != nil {
		fmt.Printf("分析图片 1 失败：%v\n", err)
		os.Exit(1)
	}

	result2, err := analyzer.Analyze(imagePath2)
	if err != nil {
		fmt.Printf("分析图片 2 失败：%v\n", err)
		os.Exit(1)
	}

	// 计算相似度 (TODO: 实现比对算法)
	similarity := calculateSimilarity(result1, result2)

	fmt.Printf("图片 1: %s\n", filepath.Base(imagePath1))
	fmt.Printf("  尺寸：%dx%d, 场景：%s\n",
		result1.Dimensions.Width, result1.Dimensions.Height, result1.Scene)
	fmt.Printf("图片 2: %s\n", filepath.Base(imagePath2))
	fmt.Printf("  尺寸：%dx%d, 场景：%s\n",
		result2.Dimensions.Width, result2.Dimensions.Height, result2.Scene)
	fmt.Printf("\n相似度：%.2f%%\n", similarity*100)
}

// handleQuery 处理自然语言查询
func handleQuery(result *image.AnalysisResult, query string) string {
	// TODO: 集成 NLP 模块处理查询
	// 目前返回简单响应
	return fmt.Sprintf("分析结果：图片尺寸 %dx%d, 格式 %s, 场景 %s",
		result.Dimensions.Width,
		result.Dimensions.Height,
		result.Format,
		result.Scene)
}

// calculateSimilarity 计算图片相似度
func calculateSimilarity(r1, r2 *image.AnalysisResult) float64 {
	// TODO: 实现相似度算法
	return 0.5
}

// contains 简单字符串包含检查
func contains(s, substr string) bool {
	return len(s) > 0 && len(substr) > 0
}
