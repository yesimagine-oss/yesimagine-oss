package main

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

// Config 配置结构
type Config struct {
	Cache struct {
		TTLHours  int `yaml:"ttl_hours"`
		MaxTokens int `yaml:"max_tokens"`
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

// LoadConfig 从文件加载配置
func LoadConfig(path string) (*Config, error) {
	// 默认配置
	config := &Config{
		Cache: struct {
			TTLHours  int `yaml:"ttl_hours"`
			MaxTokens int `yaml:"max_tokens"`
		}{
			TTLHours:  2,
			MaxTokens: 300,
		},
		Model: struct {
			Name    string `yaml:"name"`
			APIBase string `yaml:"api_base"`
		}{
			Name:    "qwen-coding-lite",
			APIBase: "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
		},
		Monitoring: struct {
			Enabled     bool   `yaml:"enabled"`
			LogPath     string `yaml:"log_path"`
			StatsInterval int  `yaml:"stats_interval"`
		}{
			Enabled:     true,
			LogPath:     "/home/admin/.openclaw/workspace/goToken-v2/logs/metrics.json",
			StatsInterval: 60,
		},
		RateLimit: struct {
			MaxConcurrent int  `yaml:"max_concurrent"`
			Enabled       bool `yaml:"enabled"`
		}{
			MaxConcurrent: 2,
			Enabled:       true,
		},
	}

	// 检查配置文件是否存在
	if _, err := os.Stat(path); os.IsNotExist(err) {
		fmt.Printf("⚠️  配置文件不存在：%s，使用默认配置\n", path)
		return config, nil
	}

	// 读取配置文件
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("读取配置文件失败：%v", err)
	}

	// 解析 YAML
	err = yaml.Unmarshal(data, config)
	if err != nil {
		return nil, fmt.Errorf("解析配置文件失败：%v", err)
	}

	fmt.Printf("✅ 配置文件已加载：%s\n", path)
	fmt.Printf("   缓存 TTL: %d 小时\n", config.Cache.TTLHours)
	fmt.Printf("   最大 Token: %d\n", config.Cache.MaxTokens)
	fmt.Printf("   模型：%s\n", config.Model.Name)

	return config, nil
}
