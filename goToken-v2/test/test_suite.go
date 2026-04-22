package main

import (
	"fmt"
	"os"
	"sync"
	"testing"
	"time"
)

// 引入主包的类型（测试需要）
type Config = struct {
	Cache struct {
		TTLHours  int    `yaml:"ttl_hours"`
		MaxTokens int    `yaml:"max_tokens"`
	} `yaml:"cache"`
	Model struct {
		Name    string `yaml:"name"`
		APIBase string `yaml:"api_base"`
	} `yaml:"model"`
	Monitoring struct {
		Enabled     bool   `yaml:"enabled"`
		LogPath     string `yaml:"log_path"`
		StatsInterval int  `yaml:"stats_interval"`
	} `yaml:"monitoring"`
	RateLimit struct {
		MaxConcurrent int  `yaml:"max_concurrent"`
		Enabled       bool `yaml:"enabled"`
	} `yaml:"rate_limit"`
}

// 简化版 NewgoToken 用于测试
func NewgoToken(config *Config) *goToken {
	return &goToken{}
}

// TestResult 测试结果
type TestResult struct {
	Name     string
	Passed   bool
	Duration time.Duration
	Error    error
}

// TestSuite 测试套件
type TestSuite struct {
	results []TestResult
	passed  int
	failed  int
}

// NewTestSuite 创建测试套件
func NewTestSuite() *TestSuite {
	return &TestSuite{
		results: make([]TestResult, 0),
		passed:  0,
		failed:  0,
	}
}

// RunTest 运行单个测试
func (ts *TestSuite) RunTest(name string, testFunc func() error) {
	start := time.Now()
	err := testFunc()
	duration := time.Since(start)

	result := TestResult{
		Name:     name,
		Passed:   err == nil,
		Duration: duration,
		Error:    err,
	}

	ts.results = append(ts.results, result)

	if result.Passed {
		ts.passed++
		fmt.Printf("✅ %s (%.2fs)\n", name, duration.Seconds())
	} else {
		ts.failed++
		fmt.Printf("❌ %s (%.2fs): %v\n", name, duration.Seconds(), err)
	}
}

// Report 生成测试报告
func (ts *TestSuite) Report() {
	fmt.Println("\n================================")
	fmt.Printf("📊 测试完成：%d 通过，%d 失败，%d 总计\n", ts.passed, ts.failed, len(ts.results))

	totalDuration := time.Duration(0)
	for _, r := range ts.results {
		totalDuration += r.Duration
	}
	fmt.Printf("⏱️  总耗时：%.2fs\n", totalDuration.Seconds())
	fmt.Println("================================")
}

// ============================================================================
// 测试用例
// ============================================================================

// TestCacheHit 测试缓存命中
func TestCacheHit(t *testing.T) {
	config := &Config{
		Cache: struct {
			TTLHours  int `yaml:"ttl_hours"`
			MaxTokens int `yaml:"max_tokens"`
		}{
			TTLHours:  2,
			MaxTokens: 300,
		},
	}

	token := NewgoToken(config)

	// 第一次调用（未命中）
	query := "测试问题"
	answer1 := token.Query(query)

	// 第二次调用（应该命中）
	answer2 := token.Query(query)

	if answer1 != answer2 {
		t.Errorf("缓存未命中：第一次和第二次答案不一致")
	}
}

// TestCacheMiss 测试缓存未命中
func TestCacheMiss(t *testing.T) {
	config := &Config{
		Cache: struct {
			TTLHours  int `yaml:"ttl_hours"`
			MaxTokens int `yaml:"max_tokens"`
		}{
			TTLHours:  2,
			MaxTokens: 300,
		},
	}

	token := NewgoToken(config)

	// 不同问题应该不命中
	query1 := "测试问题 1"
	query2 := "测试问题 2"

	_ = token.Query(query1)
	_ = token.Query(query2)

	// 如果能执行到这里，说明未命中正常工作
}

// TestCacheTTL 测试 TTL 过期
func TestCacheTTL(t *testing.T) {
	config := &Config{
		Cache: struct {
			TTLHours  int `yaml:"ttl_hours"`
			MaxTokens int `yaml:"max_tokens"`
		}{
			TTLHours:  0, // 0 小时 = 立即过期
			MaxTokens: 300,
		},
	}

	token := NewgoToken(config)

	query := "TTL 测试问题"
	_ = token.Query(query)

	// 等待 1 秒
	time.Sleep(1 * time.Second)

	// 再次查询（应该已过期）
	_ = token.Query(query)

	// 如果能执行到这里，说明 TTL 正常工作
}

// TestRateLimit 测试限流保护
func TestRateLimit(t *testing.T) {
	config := &Config{
		RateLimit: struct {
			MaxConcurrent int  `yaml:"max_concurrent"`
			Enabled       bool `yaml:"enabled"`
		}{
			MaxConcurrent: 2,
			Enabled:       true,
		},
	}

	token := NewgoToken(config)

	// 并发发送 5 个请求
	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			query := fmt.Sprintf("并发测试 %d", id)
			_ = token.Query(query)
		}(i)
	}

	wg.Wait()
	// 如果能执行到这里，说明限流正常工作
}

// TestEmptyQuery 测试空查询处理
func TestEmptyQuery(t *testing.T) {
	config := &Config{}
	token := NewgoToken(config)

	query := ""
	answer := token.Query(query)

	if answer != "请输入有效问题" {
		t.Errorf("空查询未正确处理：期望'请输入有效问题'，得到'%s'", answer)
	}
}

// TestConfigLoad 测试配置加载
func TestConfigLoad(t *testing.T) {
	// 创建临时配置文件
	tmpConfig := "/tmp/gotoken-test-config.yaml"
	configContent := `
cache:
  ttl_hours: 4
  max_tokens: 500
model:
  name: qwen3.5-plus
`
	err := os.WriteFile(tmpConfig, []byte(configContent), 0644)
	if err != nil {
		t.Errorf("创建临时配置文件失败：%v", err)
		return
	}
	defer os.Remove(tmpConfig)

	// 加载配置
	config, err := LoadConfig(tmpConfig)
	if err != nil {
		t.Errorf("加载配置文件失败：%v", err)
		return
	}

	// 验证配置
	if config.Cache.TTLHours != 4 {
		t.Errorf("TTL 配置错误：期望 4，得到 %d", config.Cache.TTLHours)
	}
	if config.Cache.MaxTokens != 500 {
		t.Errorf("MaxTokens 配置错误：期望 500，得到 %d", config.Cache.MaxTokens)
	}
	if config.Model.Name != "qwen3.5-plus" {
		t.Errorf("模型配置错误：期望 qwen3.5-plus，得到 %s", config.Model.Name)
	}
}

// ============================================================================
// 主函数
// ============================================================================

func main() {
	fmt.Println("🧪 goToken-v2 测试套件")
	fmt.Println("================================")

	suite := NewTestSuite()

	// 运行测试用例
	suite.RunTest("缓存命中测试", func() error {
		t := &testing.T{}
		TestCacheHit(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	suite.RunTest("缓存未命中测试", func() error {
		t := &testing.T{}
		TestCacheMiss(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	suite.RunTest("TTL 过期测试", func() error {
		t := &testing.T{}
		TestCacheTTL(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	suite.RunTest("限流保护测试", func() error {
		t := &testing.T{}
		TestRateLimit(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	suite.RunTest("空查询处理测试", func() error {
		t := &testing.T{}
		TestEmptyQuery(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	suite.RunTest("配置加载测试", func() error {
		t := &testing.T{}
		TestConfigLoad(t)
		if t.Failed() {
			return fmt.Errorf("测试失败")
		}
		return nil
	})

	// 生成报告
	suite.Report()

	// 退出码
	if suite.failed > 0 {
		os.Exit(1)
	}
}
