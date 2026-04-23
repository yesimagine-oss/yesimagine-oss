package api

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"

	"github.com/openclaw/go-image-skill/internal/image"
)

// Server HTTP API 服务器
type Server struct {
	analyzer *image.ImageAnalyzer
	port     string
}

// NewServer 创建服务器
func NewServer(port string) *Server {
	return &Server{
		analyzer: image.NewAnalyzer(""),
		port:     port,
	}
}

// Start 启动服务器
func (s *Server) Start() error {
	http.HandleFunc("/analyze", s.handleAnalyze)
	http.HandleFunc("/query", s.handleQuery)
	http.HandleFunc("/search", s.handleSearch)
	http.HandleFunc("/compare", s.handleCompare)
	http.HandleFunc("/health", s.handleHealth)

	fmt.Printf("HTTP 服务启动在端口 %s\n", s.port)
	return http.ListenAndServe(":"+s.port, nil)
}

// AnalyzeRequest 分析请求
type AnalyzeRequest struct {
	Query string `json:"query,omitempty"`
}

// AnalyzeResponse 分析响应
type AnalyzeResponse struct {
	Success bool                `json:"success"`
	Data    *image.AnalysisResult `json:"data,omitempty"`
	Error   string              `json:"error,omitempty"`
}

// QueryRequest 查询请求
type QueryRequest struct {
	Query   string `json:"query"`
	ImageID string `json:"image_id,omitempty"`
}

// QueryResponse 查询响应
type QueryResponse struct {
	Success bool   `json:"success"`
	Answer  string `json:"answer"`
}

// handleAnalyze 处理分析请求
func (s *Server) handleAnalyze(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// 解析 multipart 表单
	err := r.ParseMultipartForm(50 << 20) // 50MB limit
	if err != nil {
		s.sendError(w, "解析表单失败："+err.Error(), http.StatusBadRequest)
		return
	}

	// 获取上传的文件
	file, header, err := r.FormFile("file")
	if err != nil {
		s.sendError(w, "获取文件失败："+err.Error(), http.StatusBadRequest)
		return
	}
	defer file.Close()

	// 保存到临时文件
	tmpFile, err := os.CreateTemp("", "image-*"+filepath.Ext(header.Filename))
	if err != nil {
		s.sendError(w, "创建临时文件失败："+err.Error(), http.StatusInternalServerError)
		return
	}
	defer os.Remove(tmpFile.Name())

	if _, err := io.Copy(tmpFile, file); err != nil {
		s.sendError(w, "保存文件失败："+err.Error(), http.StatusInternalServerError)
		return
	}
	tmpFile.Close()

	// 分析图片
	result, err := s.analyzer.Analyze(tmpFile.Name())
	if err != nil {
		s.sendError(w, "分析失败："+err.Error(), http.StatusInternalServerError)
		return
	}

	// 获取查询参数 (可选)
	query := r.FormValue("query")
	if query != "" {
		// TODO: 调用 NLP 模块处理查询
	}

	response := AnalyzeResponse{
		Success: true,
		Data:    result,
	}

	s.sendJSON(w, response, http.StatusOK)
}

// handleQuery 处理自然语言查询
func (s *Server) handleQuery(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req QueryRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		s.sendError(w, "解析请求失败："+err.Error(), http.StatusBadRequest)
		return
	}

	if req.Query == "" {
		s.sendError(w, "查询不能为空", http.StatusBadRequest)
		return
	}

	// TODO: 实现查询逻辑
	response := QueryResponse{
		Success: true,
		Answer:  "查询处理中...",
	}

	s.sendJSON(w, response, http.StatusOK)
}

// handleSearch 处理搜索请求
func (s *Server) handleSearch(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	query := r.URL.Query().Get("q")
	if query == "" {
		s.sendError(w, "查询参数 q 不能为空", http.StatusBadRequest)
		return
	}

	// TODO: 实现搜索逻辑
	s.sendJSON(w, map[string]interface{}{
		"success": true,
		"results": []string{},
	}, http.StatusOK)
}

// handleCompare 处理比对请求
func (s *Server) handleCompare(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// TODO: 实现比对逻辑
	s.sendJSON(w, map[string]interface{}{
		"success":    true,
		"similarity": 0.5,
	}, http.StatusOK)
}

// handleHealth 健康检查
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	s.sendJSON(w, map[string]string{
		"status": "healthy",
	}, http.StatusOK)
}

// sendJSON 发送 JSON 响应
func (s *Server) sendJSON(w http.ResponseWriter, data interface{}, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// sendError 发送错误响应
func (s *Server) sendError(w http.ResponseWriter, message string, status int) {
	s.sendJSON(w, map[string]string{
		"success": "false",
		"error":   message,
	}, status)
}
