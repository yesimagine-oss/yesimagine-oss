// Package wiki_ingest implements the wiki ingestion plugin
package wiki_ingest

import (
	"context"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/chromedp/chromedp"
	"gitlab.com/openclaw/goex/plugin"
)

func init() {
	plugin.Register("wiki-ingest", &WikiIngestPlugin{})
}

// WikiIngestPlugin handles wiki content ingestion
type WikiIngestPlugin struct {
	config WikiConfig
}

// WikiConfig holds plugin configuration
type WikiConfig struct {
	BasePath    string `json:"base_path"`
	AutoIngest  bool   `json:"auto_ingest"`
	MaxRetries  int    `json:"max_retries"`
	TimeoutSec  int    `json:"timeout_sec"`
}

// Name returns the plugin name
func (p *WikiIngestPlugin) Name() string {
	return "wiki-ingest"
}

// Init initializes the plugin with configuration
func (p *WikiIngestPlugin) Init(config map[string]interface{}) error {
	// Set defaults
	p.config = WikiConfig{
		BasePath:   "/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/raw/",
		AutoIngest: true,
		MaxRetries: 3,
		TimeoutSec: 45,
	}
	
	// Apply overrides from config
	if basePath, ok := config["base_path"].(string); ok {
		p.config.BasePath = basePath
	}
	if maxRetries, ok := config["max_retries"].(int); ok {
		p.config.MaxRetries = maxRetries
	}
	if timeoutSec, ok := config["timeout_sec"].(int); ok {
		p.config.TimeoutSec = timeoutSec
	}
	
	fmt.Printf("📚 Wiki-Ingest 插件已初始化: %s\n", p.config.BasePath)
	return nil
}

// Execute executes the wiki ingestion
func (p *WikiIngestPlugin) Execute(params map[string]interface{}) (map[string]interface{}, error) {
	url, ok := params["url"].(string)
	if !ok || url == "" {
		return nil, fmt.Errorf("url parameter is required")
	}
	
	ctx, ok := params["context"].(context.Context)
	if !ok {
		ctx = context.Background()
	}
	
	fmt.Printf("🌐 开始抓取：%s\n", url)
	
	// Execute scraping
	result, err := p.scrapeToWiki(ctx, url)
	if err != nil {
		return nil, err
	}
	
	return map[string]interface{}{
		"success":   true,
		"url":       url,
		"file":      result.FilePath,
		"category":  result.Category,
		"title":     result.Title,
		"timestamp": time.Now().Format(time.RFC3339),
	}, nil
}

// ScrapedResult holds the result of a scrape operation
type ScrapedResult struct {
	FilePath  string
	Category  string
	Title     string
	WordCount int
}

// scrapeToWiki scrapes a URL and saves to wiki
func (p *WikiIngestPlugin) scrapeToWiki(ctx context.Context, url string) (*ScrapedResult, error) {
	var lastErr error
	
	for attempt := 1; attempt <= p.config.MaxRetries; attempt++ {
		if attempt > 1 {
			fmt.Printf("🔄 第 %d 次重试...\n", attempt)
			time.Sleep(3 * time.Second)
		}
		
		// Create browser context
		browserCtx, cancel := chromedp.NewContext(ctx)
		timeout := time.Duration(p.config.TimeoutSec) * time.Second
		browserCtx, timeoutCancel := context.WithTimeout(browserCtx, timeout)
		
		var html, title string
		
		err := chromedp.Run(browserCtx,
			chromedp.Navigate(url),
			chromedp.Sleep(2*time.Second),
			chromedp.OuterHTML("html", &html),
			chromedp.Title(&title),
		)
		
		timeoutCancel()
		cancel()
		
		if err == nil {
			fmt.Printf("✅ 抓取成功：%s\n", title)
			
			// Convert to markdown
			markdown := p.htmlToMarkdown(html, title, url)
			
			// Categorize
			category := p.categorizeURL(url)
			
			// Save
			rawDir := p.config.BasePath + category
			filename := p.urlToFilename(url)
			filePath := rawDir + "/" + filename + ".md"
			
			os.MkdirAll(rawDir, 0755)
			err = os.WriteFile(filePath, []byte(markdown), 0644)
			if err != nil {
				return nil, fmt.Errorf("保存失败：%v", err)
			}
			
			fmt.Printf("✅ 已保存到：%s\n", filePath)
			
			return &ScrapedResult{
				FilePath:  filePath,
				Category:  category,
				Title:     title,
				WordCount: len(markdown),
			}, nil
		}
		
		lastErr = err
		fmt.Printf("⚠️  尝试 %d 失败：%v\n", attempt, err)
	}
	
	return nil, fmt.Errorf("抓取失败（已重试 %d 次）: %v", p.config.MaxRetries, lastErr)
}

// htmlToMarkdown converts HTML to markdown
func (p *WikiIngestPlugin) htmlToMarkdown(html, title, url string) string {
	timestamp := time.Now().Format(time.RFC3339)
	
	// Extract text content
	textContent := p.extractTextContent(html)
	
	// Extract links
	links := p.extractLinks(html)
	
	md := "# " + title + "\n\n"
	md += "**来源**: " + url + "\n"
	md += "**抓取时间**: " + timestamp + "\n"
	md += "**分类**: 自动抓取\n\n"
	md += "---\n\n"
	md += "## 内容摘要\n\n"
	md += textContent + "\n\n"
	
	if len(links) > 0 {
		md += "## 关键链接\n\n"
		for _, link := range links {
			md += "- " + link + "\n"
		}
		md += "\n"
	}
	
	md += "---\n\n"
	md += "> 注意：此文件为自动抓取，将由 auto-ingest.py 编译为知识库条目\n"
	
	return md
}

// extractTextContent extracts plain text from HTML
func (p *WikiIngestPlugin) extractTextContent(html string) string {
	text := html
	text = strings.ReplaceAll(text, "<script", "<!--<script")
	text = strings.ReplaceAll(text, "</script>", "</script>-->")
	text = strings.ReplaceAll(text, "<style", "<!--<style")
	text = strings.ReplaceAll(text, "</style>", "</style>-->")
	
	if len(text) > 5000 {
		text = text[:5000] + "...\n\n[内容过长，已截断]"
	}
	
	return text
}

// extractLinks extracts links from HTML
func (p *WikiIngestPlugin) extractLinks(html string) []string {
	links := []string{}
	lines := strings.Split(html, "\n")
	
	for _, line := range lines {
		if strings.Contains(line, "href=") && strings.Contains(line, "http") {
			start := strings.Index(line, "http")
			if start != -1 {
				end := strings.Index(line[start:], "\"")
				if end != -1 {
					url := line[start : start+end]
					if !strings.Contains(url, "static") && !strings.Contains(url, "chunk") {
						links = append(links, url)
					}
				}
			}
		}
		if len(links) >= 10 {
			break
		}
	}
	return links
}

// categorizeURL categorizes a URL
func (p *WikiIngestPlugin) categorizeURL(url string) string {
	if strings.Contains(url, "wiki") || strings.Contains(url, "doc") {
		return "wiki"
	} else if strings.Contains(url, "api") || strings.Contains(url, "swagger") {
		return "api"
	} else if strings.Contains(url, "blog") || strings.Contains(url, "news") {
		return "blog"
	} else if strings.Contains(url, "github") || strings.Contains(url, "gitee") {
		return "code"
	}
	return "general"
}

// urlToFilename converts URL to filename
func (p *WikiIngestPlugin) urlToFilename(url string) string {
	filename := strings.ReplaceAll(url, "https://", "")
	filename = strings.ReplaceAll(filename, "http://", "")
	filename = strings.ReplaceAll(filename, "/", "_")
	filename = strings.ReplaceAll(filename, ".", "_")
	filename = strings.ReplaceAll(filename, "?", "_")
	filename = strings.ReplaceAll(filename, "=", "_")
	
	if len(filename) > 100 {
		filename = filename[:100]
	}
	
	return filename
}

// Shutdown cleans up plugin resources
func (p *WikiIngestPlugin) Shutdown() error {
	fmt.Println("📚 Wiki-Ingest 插件已关闭")
	return nil
}
