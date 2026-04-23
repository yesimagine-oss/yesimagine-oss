// Package wechat_grab implements the WeChat article grabbing plugin
package wechat_grab

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
	plugin.Register("wechat-grab", &WechatGrabPlugin{})
}

// WechatGrabPlugin handles WeChat article grabbing
type WechatGrabPlugin struct {
	config WechatConfig
}

// WechatConfig holds plugin configuration
type WechatConfig struct {
	BasePath    string `json:"base_path"`
	LoginWait   bool   `json:"login_wait"`
	MaxWaitSec  int    `json:"max_wait_sec"`
	TimeoutSec  int    `json:"timeout_sec"`
	MaxRetries  int    `json:"max_retries"`
}

// Name returns the plugin name
func (p *WechatGrabPlugin) Name() string {
	return "wechat-grab"
}

// Init initializes the plugin with configuration
func (p *WechatGrabPlugin) Init(config map[string]interface{}) error {
	// Set defaults
	p.config = WechatConfig{
		BasePath:   "/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/raw/wechat/",
		LoginWait:  true,
		MaxWaitSec: 300, // 5 minutes for manual login
		TimeoutSec: 90,
		MaxRetries: 3,
	}
	
	// Apply overrides from config
	if basePath, ok := config["base_path"].(string); ok {
		p.config.BasePath = basePath
	}
	if loginWait, ok := config["login_wait"].(bool); ok {
		p.config.LoginWait = loginWait
	}
	if maxWaitSec, ok := config["max_wait_sec"].(int); ok {
		p.config.MaxWaitSec = maxWaitSec
	}
	if timeoutSec, ok := config["timeout_sec"].(int); ok {
		p.config.TimeoutSec = timeoutSec
	}
	
	fmt.Printf("💬 Wechat-Grab 插件已初始化：%s\n", p.config.BasePath)
	return nil
}

// Execute executes the WeChat article grab
func (p *WechatGrabPlugin) Execute(params map[string]interface{}) (map[string]interface{}, error) {
	url, ok := params["url"].(string)
	if !ok || url == "" {
		return nil, fmt.Errorf("url parameter is required")
	}
	
	ctx, ok := params["context"].(context.Context)
	if !ok {
		ctx = context.Background()
	}
	
	fmt.Printf("💬 开始抓取微信文章：%s\n", url)
	
	// Execute grabbing
	result, err := p.grabArticle(ctx, url)
	if err != nil {
		return nil, err
	}
	
	return map[string]interface{}{
		"success":   true,
		"url":       url,
		"file":      result.FilePath,
		"title":     result.Title,
		"author":    result.Author,
		"timestamp": time.Now().Format(time.RFC3339),
	}, nil
}

// GrabbedResult holds the result of a grab operation
type GrabbedResult struct {
	FilePath  string
	Title     string
	Author    string
	PubDate   string
	WordCount int
}

// grabArticle grabs a WeChat article
func (p *WechatGrabPlugin) grabArticle(ctx context.Context, url string) (*GrabbedResult, error) {
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
		
		// Navigate and wait for content
		err := chromedp.Run(browserCtx,
			chromedp.Navigate(url),
			chromedp.Sleep(3*time.Second),
			chromedp.Title(&title),
		)
		
		if err == nil && title == "need_login" {
			fmt.Println("⚠️  需要微信登录")
			
			if p.config.LoginWait {
				fmt.Printf("⏳ 等待用户登录（最多 %d 秒）...\n", p.config.MaxWaitSec)
				
				// Wait for login
				loginCtx, loginCancel := context.WithTimeout(browserCtx, time.Duration(p.config.MaxWaitSec)*time.Second)
				
				var loggedIn string
				err = chromedp.Run(loginCtx,
					chromedp.Sleep(5*time.Second),
					chromedp.Evaluate(`() => {
						const content = document.querySelector('#js_content');
						return content ? 'logged_in' : 'still_waiting';
					}()`, &loggedIn),
				)
				
				loginCancel()
				
				if err != nil || loggedIn != "logged_in" {
					timeoutCancel()
					cancel()
					lastErr = fmt.Errorf("等待登录超时")
					continue
				}
				
				fmt.Println("✅ 用户已登录，继续抓取...")
				
				// Re-fetch after login
				err = chromedp.Run(browserCtx,
					chromedp.Sleep(2*time.Second),
					chromedp.OuterHTML("html", &html),
					chromedp.Title(&title),
				)
			} else {
				timeoutCancel()
				cancel()
				lastErr = fmt.Errorf("需要登录但未启用登录等待")
				continue
			}
		} else if err == nil {
			// Not login required, fetch content
			err = chromedp.Run(browserCtx,
				chromedp.Sleep(2*time.Second),
				chromedp.OuterHTML("html", &html),
				chromedp.Title(&title),
			)
		}
		
		timeoutCancel()
		cancel()
		
		if err == nil && html != "" {
			fmt.Printf("✅ 抓取成功：%s\n", title)
			
			// Extract article info
			articleInfo := p.extractArticleInfo(html)
			
			// Convert to markdown
			markdown := p.htmlToMarkdown(html, title, url, articleInfo)
			
			// Save
			filename := p.urlToFilename(url)
			filePath := p.config.BasePath + filename + ".md"
			
			os.MkdirAll(p.config.BasePath, 0755)
			err = os.WriteFile(filePath, []byte(markdown), 0644)
			if err != nil {
				return nil, fmt.Errorf("保存失败：%v", err)
			}
			
			fmt.Printf("✅ 已保存到：%s\n", filePath)
			
			return &GrabbedResult{
				FilePath:  filePath,
				Title:     articleInfo.Title,
				Author:    articleInfo.Author,
				PubDate:   articleInfo.PubDate,
				WordCount: len(markdown),
			}, nil
		}
		
		lastErr = err
		fmt.Printf("⚠️  尝试 %d 失败：%v\n", attempt, err)
	}
	
	return nil, fmt.Errorf("抓取失败（已重试 %d 次）: %v", p.config.MaxRetries, lastErr)
}

// ArticleInfo holds extracted article metadata
type ArticleInfo struct {
	Title   string
	Author  string
	PubDate string
	Summary string
}

// extractArticleInfo extracts article metadata from HTML
func (p *WechatGrabPlugin) extractArticleInfo(html string) *ArticleInfo {
	info := &ArticleInfo{
		Title:   "未知标题",
		Author:  "未知作者",
		PubDate: "未知日期",
	}
	
	// Extract title from rich_media_title
	if idx := strings.Index(html, "rich_media_title"); idx != -1 {
		start := strings.Index(html[idx:], ">")
		end := strings.Index(html[idx:], "</h2>")
		if start != -1 && end != -1 && start < end {
			info.Title = strings.TrimSpace(html[idx+start+1 : idx+end])
		}
	}
	
	// Extract author from profile_nickname
	if idx := strings.Index(html, "profile_nickname"); idx != -1 {
		start := strings.Index(html[idx:], ">")
		end := strings.Index(html[idx:], "</strong>")
		if start != -1 && end != -1 && start < end {
			info.Author = strings.TrimSpace(html[idx+start+1 : idx+end])
		}
	}
	
	// Extract publish date
	if idx := strings.Index(html, "publish_time"); idx != -1 {
		start := strings.Index(html[idx:], ">")
		end := strings.Index(html[idx:], "</span>")
		if start != -1 && end != -1 && start < end {
			info.PubDate = strings.TrimSpace(html[idx+start+1 : idx+end])
		}
	}
	
	return info
}

// htmlToMarkdown converts WeChat HTML to markdown
func (p *WechatGrabPlugin) htmlToMarkdown(html, title, url string, info *ArticleInfo) string {
	timestamp := time.Now().Format(time.RFC3339)
	
	// Extract main content
	content := p.extractContent(html)
	
	md := "# " + info.Title + "\n\n"
	md += "**作者**: " + info.Author + "\n"
	md += "**发布日期**: " + info.PubDate + "\n"
	md += "**来源**: " + url + "\n"
	md += "**抓取时间**: " + timestamp + "\n"
	md += "**分类**: 微信公众号文章\n\n"
	md += "---\n\n"
	md += "## 文章内容\n\n"
	md += content + "\n\n"
	md += "---\n\n"
	md += "> 注意：此文件为自动抓取，内容版权归原文作者所有\n"
	
	return md
}

// extractContent extracts main article content from WeChat HTML
func (p *WechatGrabPlugin) extractContent(html string) string {
	// Find js_content div
	start := strings.Index(html, `id="js_content"`)
	if start == -1 {
		// Fallback: extract body text
		return p.extractTextContent(html)
	}
	
	// Extract content div
	contentStart := strings.Index(html[start:], ">")
	if contentStart == -1 {
		return p.extractTextContent(html)
	}
	contentStart = start + contentStart + 1
	
	// Find closing tag
	contentEnd := strings.Index(html[contentStart:], "</div>")
	if contentEnd == -1 {
		return p.extractTextContent(html)
	}
	contentEnd = contentStart + contentEnd
	
	content := html[contentStart:contentEnd]
	
	// Clean up HTML tags
	content = p.cleanHTML(content)
	
	if len(content) > 10000 {
		content = content[:10000] + "...\n\n[内容过长，已截断]"
	}
	
	return content
}

// extractTextContent extracts plain text from HTML (fallback)
func (p *WechatGrabPlugin) extractTextContent(html string) string {
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

// cleanHTML cleans HTML tags and converts to plain text
func (p *WechatGrabPlugin) cleanHTML(html string) string {
	// Remove script/style
	html = strings.ReplaceAll(html, "<script", "<!--<script")
	html = strings.ReplaceAll(html, "</script>", "</script>-->")
	html = strings.ReplaceAll(html, "<style", "<!--<style")
	html = strings.ReplaceAll(html, "</style>", "</style>-->")
	
	// Convert common tags
	html = strings.ReplaceAll(html, "<br>", "\n")
	html = strings.ReplaceAll(html, "<br/>", "\n")
	html = strings.ReplaceAll(html, "<br />", "\n")
	html = strings.ReplaceAll(html, "<p>", "\n\n")
	html = strings.ReplaceAll(html, "</p>", "")
	html = strings.ReplaceAll(html, "<h1>", "\n# ")
	html = strings.ReplaceAll(html, "</h1>", "\n")
	html = strings.ReplaceAll(html, "<h2>", "\n## ")
	html = strings.ReplaceAll(html, "</h2>", "\n")
	
	// Remove remaining tags
	var result strings.Builder
	inTag := false
	for _, ch := range html {
		if ch == '<' {
			inTag = true
		} else if ch == '>' {
			inTag = false
		} else if !inTag {
			result.WriteRune(ch)
		}
	}
	
	return strings.TrimSpace(result.String())
}

// urlToFilename converts URL to filename
func (p *WechatGrabPlugin) urlToFilename(url string) string {
	filename := strings.ReplaceAll(url, "https://", "")
	filename = strings.ReplaceAll(filename, "http://", "")
	filename = strings.ReplaceAll(filename, "/", "_")
	filename = strings.ReplaceAll(filename, ".", "_")
	filename = strings.ReplaceAll(filename, "?", "_")
	filename = strings.ReplaceAll(filename, "=", "_")
	filename = strings.ReplaceAll(filename, "&", "_")
	
	if len(filename) > 100 {
		filename = filename[:100]
	}
	
	return "wechat_" + filename
}

// Shutdown cleans up plugin resources
func (p *WechatGrabPlugin) Shutdown() error {
	fmt.Println("💬 Wechat-Grab 插件已关闭")
	return nil
}
