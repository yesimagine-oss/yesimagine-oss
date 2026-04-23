package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/chromedp/chromedp"
)

// ClawBrowserCore Go 语言实现的浏览器自动化核心
type ClawBrowserCore struct {
	ctx       context.Context
	cancel    context.CancelFunc
	sessionID string
	allocated bool
}

// NewClawBrowserCore 创建新的浏览器实例
func NewClawBrowserCore(sessionID string) *ClawBrowserCore {
	return &ClawBrowserCore{
		sessionID: sessionID,
	}
}

// Start 启动浏览器
func (c *ClawBrowserCore) Start() error {
	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", true),
		chromedp.Flag("disable-gpu", true),
		chromedp.Flag("no-sandbox", true),
		chromedp.Flag("disable-dev-shm-usage", true),
		chromedp.WindowSize(1920, 1080),
	)

	allocCtx, _ := chromedp.NewExecAllocator(context.Background(), opts...)
	c.ctx, c.cancel = chromedp.NewContext(allocCtx)
	c.allocated = true

	return nil
}

// Close 关闭浏览器
func (c *ClawBrowserCore) Close() error {
	if c.cancel != nil {
		c.cancel()
	}
	c.allocated = false
	return nil
}

// Navigate 打开网页
func (c *ClawBrowserCore) Navigate(url string) error {
	if !c.allocated {
		return fmt.Errorf("browser not started")
	}

	return chromedp.Run(c.ctx, chromedp.Navigate(url))
}

// Screenshot 截图
func (c *ClawBrowserCore) Screenshot(path string) error {
	if !c.allocated {
		return fmt.Errorf("browser not started")
	}

	var buf []byte
	err := chromedp.Run(c.ctx, chromedp.FullScreenshot(&buf, 90))
	if err != nil {
		return err
	}

	return os.WriteFile(path, buf, 0644)
}

// Snapshot 获取页面快照（简化版）
func (c *ClawBrowserCore) Snapshot() (string, error) {
	if !c.allocated {
		return "", fmt.Errorf("browser not started")
	}

	var text string
	err := chromedp.Run(c.ctx, chromedp.Text("body", &text, chromedp.ByQuery))
	if err != nil {
		return "", err
	}

	return text, nil
}

// Click 点击元素（通过 CSS 选择器）
func (c *ClawBrowserCore) Click(selector string) error {
	if !c.allocated {
		return fmt.Errorf("browser not started")
	}

	return chromedp.Run(c.ctx, chromedp.Click(selector, chromedp.NodeVisible))
}

// Fill 填写输入框
func (c *ClawBrowserCore) Fill(selector, text string) error {
	if !c.allocated {
		return fmt.Errorf("browser not started")
	}

	return chromedp.Run(c.ctx, chromedp.SendKeys(selector, text))
}

// Wait 等待
func (c *ClawBrowserCore) Wait(seconds int) error {
	if !c.allocated {
		return fmt.Errorf("browser not started")
	}

	time.Sleep(time.Duration(seconds) * time.Second)
	return nil
}

// GetTitle 获取页面标题
func (c *ClawBrowserCore) GetTitle() (string, error) {
	if !c.allocated {
		return "", fmt.Errorf("browser not started")
	}

	var title string
	err := chromedp.Run(c.ctx, chromedp.Title(&title))
	return title, err
}

// GetURL 获取当前 URL
func (c *ClawBrowserCore) GetURL() (string, error) {
	if !c.allocated {
		return "", fmt.Errorf("browser not started")
	}

	var url string
	err := chromedp.Run(c.ctx, chromedp.Location(&url))
	return url, err
}

// Evaluate 执行 JavaScript
func (c *ClawBrowserCore) Evaluate(script string) (string, error) {
	if !c.allocated {
		return "", fmt.Errorf("browser not started")
	}

	var result string
	err := chromedp.Run(c.ctx, chromedp.Evaluate(script, &result))
	return result, err
}

// Extract 提取内容（通过 CSS 选择器）
func (c *ClawBrowserCore) Extract(selector string) ([]string, error) {
	if !c.allocated {
		return nil, fmt.Errorf("browser not started")
	}

	var text string
	err := chromedp.Run(c.ctx, chromedp.Text(selector, &text, chromedp.ByQuery))
	if err != nil {
		return nil, err
	}

	// 按行分割
	lines := strings.Split(text, "\n")
	var results []string
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" {
			results = append(results, line)
		}
	}
	return results, nil
}

// 命令行接口
func printUsage() {
	fmt.Println(`ClawBrowser Core - Go 语言浏览器自动化

用法:
  clawbrowser-core <command> [args]

命令:
  open <url>           打开网页
  screenshot <path>    截图
  snapshot             获取页面快照
  click <selector>     点击元素
  fill <selector> <text>  填写输入框
  wait <seconds>       等待
  title                获取页面标题
  url                  获取当前 URL
  eval <js>            执行 JavaScript
  extract <selector>   提取内容
  close                关闭浏览器

示例:
  clawbrowser-core open https://example.com
  clawbrowser-core screenshot page.png
  clawbrowser-core click "#submit-btn"
`)
}

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	browser := NewClawBrowserCore("default")
	if err := browser.Start(); err != nil {
		log.Fatalf("启动浏览器失败：%v", err)
	}
	defer browser.Close()

	command := os.Args[1]

	switch command {
	case "open":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core open <url>")
			os.Exit(1)
		}
		url := os.Args[2]
		if err := browser.Navigate(url); err != nil {
			log.Fatalf("打开网页失败：%v", err)
		}
		fmt.Printf("✅ 已打开：%s\n", url)

	case "screenshot":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core screenshot <path>")
			os.Exit(1)
		}
		path := os.Args[2]
		if err := browser.Screenshot(path); err != nil {
			log.Fatalf("截图失败：%v", err)
		}
		fmt.Printf("✅ 已截图：%s\n", path)

	case "snapshot":
		text, err := browser.Snapshot()
		if err != nil {
			log.Fatalf("获取快照失败：%v", err)
		}
		fmt.Println(text)

	case "click":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core click <selector>")
			os.Exit(1)
		}
		selector := os.Args[2]
		if err := browser.Click(selector); err != nil {
			log.Fatalf("点击失败：%v", err)
		}
		fmt.Printf("✅ 已点击：%s\n", selector)

	case "fill":
		if len(os.Args) < 4 {
			fmt.Println("用法：clawbrowser-core fill <selector> <text>")
			os.Exit(1)
		}
		selector := os.Args[2]
		text := os.Args[3]
		if err := browser.Fill(selector, text); err != nil {
			log.Fatalf("填写失败：%v", err)
		}
		fmt.Printf("✅ 已填写：%s\n", selector)

	case "wait":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core wait <seconds>")
			os.Exit(1)
		}
		seconds, err := strconv.Atoi(os.Args[2])
		if err != nil {
			log.Fatalf("无效的数字：%v", err)
		}
		if err := browser.Wait(seconds); err != nil {
			log.Fatalf("等待失败：%v", err)
		}
		fmt.Printf("✅ 已等待：%d 秒\n", seconds)

	case "title":
		title, err := browser.GetTitle()
		if err != nil {
			log.Fatalf("获取标题失败：%v", err)
		}
		fmt.Printf("📄 标题：%s\n", title)

	case "url":
		url, err := browser.GetURL()
		if err != nil {
			log.Fatalf("获取 URL 失败：%v", err)
		}
		fmt.Printf("🔗 URL: %s\n", url)

	case "eval":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core eval <javascript>")
			os.Exit(1)
		}
		script := os.Args[2]
		result, err := browser.Evaluate(script)
		if err != nil {
			log.Fatalf("执行 JS 失败：%v", err)
		}
		fmt.Printf("📝 结果：%s\n", result)

	case "extract":
		if len(os.Args) < 3 {
			fmt.Println("用法：clawbrowser-core extract <selector>")
			os.Exit(1)
		}
		selector := os.Args[2]
		texts, err := browser.Extract(selector)
		if err != nil {
			log.Fatalf("提取失败：%v", err)
		}
		for i, text := range texts {
			fmt.Printf("[%d] %s\n", i, text)
		}

	case "close":
		fmt.Println("✅ 已关闭")

	default:
		fmt.Printf("❌ 未知命令：%s\n", command)
		printUsage()
		os.Exit(1)
	}
}
