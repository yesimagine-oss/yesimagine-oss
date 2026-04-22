// Package feishu_notify implements the Feishu notification plugin
package feishu_notify

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"gitlab.com/openclaw/goex/plugin"
)

func init() {
	plugin.Register("feishu-notify", &FeishuNotifyPlugin{})
}

// FeishuNotifyPlugin handles Feishu notifications
type FeishuNotifyPlugin struct {
	config FeishuConfig
	client *http.Client
}

// FeishuConfig holds plugin configuration
type FeishuConfig struct {
	Mode      string `json:"mode"` // "webhook" or "api"
	Webhook   string `json:"webhook"`
	AppID     string `json:"app_id"`
	AppSecret string `json:"app_secret"`
	UserID    string `json:"user_id"`
	TimeoutSec int   `json:"timeout_sec"`
}

// Name returns the plugin name
func (p *FeishuNotifyPlugin) Name() string {
	return "feishu-notify"
}

// Init initializes the plugin with configuration
func (p *FeishuNotifyPlugin) Init(config map[string]interface{}) error {
	// Set defaults
	p.config = FeishuConfig{
		Mode:       "webhook",
		TimeoutSec: 10,
		UserID:     "ou_f4919832188bcc630f8f257497fa93a4",
	}
	
	// Apply overrides from config or environment
	if mode, ok := config["mode"].(string); ok {
		p.config.Mode = mode
	}
	if webhook, ok := config["webhook"].(string); ok {
		p.config.Webhook = webhook
	}
	if appID, ok := config["app_id"].(string); ok {
		p.config.AppID = appID
	}
	if appSecret, ok := config["app_secret"].(string); ok {
		p.config.AppSecret = appSecret
	}
	
	// Environment variable overrides
	if envWebhook := os.Getenv("FEISHU_WEBHOOK"); envWebhook != "" {
		p.config.Webhook = envWebhook
		p.config.Mode = "webhook"
	}
	if envAppID := os.Getenv("FEISHU_APP_ID"); envAppID != "" {
		p.config.AppID = envAppID
		p.config.Mode = "api"
	}
	if envAppSecret := os.Getenv("FEISHU_APP_SECRET"); envAppSecret != "" {
		p.config.AppSecret = envAppSecret
		p.config.Mode = "api"
	}
	
	p.client = &http.Client{
		Timeout: time.Duration(p.config.TimeoutSec) * time.Second,
	}
	
	fmt.Printf("📬 Feishu-Notify 插件已初始化 (模式：%s)\n", p.config.Mode)
	return nil
}

// Execute sends a Feishu notification
func (p *FeishuNotifyPlugin) Execute(params map[string]interface{}) (map[string]interface{}, error) {
	title, _ := params["title"].(string)
	content, _ := params["content"].(string)
	msgType, _ := params["msg_type"].(string)
	
	if title == "" {
		title = "goEX 通知"
	}
	if msgType == "" {
		msgType = "text"
	}
	
	fmt.Printf("📬 发送飞书通知：%s\n", title)
	
	var err error
	if p.config.Mode == "webhook" {
		err = p.sendViaWebhook(title, content)
	} else {
		err = p.sendViaAPI(title, content, msgType)
	}
	
	if err != nil {
		return nil, err
	}
	
	return map[string]interface{}{
		"success":   true,
		"title":     title,
		"mode":      p.config.Mode,
		"timestamp": time.Now().Format(time.RFC3339),
	}, nil
}

// sendViaWebhook sends notification via webhook
func (p *FeishuNotifyPlugin) sendViaWebhook(title, content string) error {
	if p.config.Webhook == "" {
		return fmt.Errorf("webhook URL 未配置")
	}
	
	msg := fmt.Sprintf("## %s\n%s", title, content)
	
	payload := map[string]interface{}{
		"msg_type": "post",
		"content": map[string]interface{}{
			"post": map[string]interface{}{
				"zh_cn": map[string]interface{}{
					"title": title,
					"content": [][]map[string]interface{}{
						{
							{"tag": "text", "text": msg},
						},
					},
				},
			},
		},
	}
	
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("JSON 编码失败：%v", err)
	}
	
	resp, err := p.client.Post(p.config.Webhook, "application/json", bytes.NewReader(jsonData))
	if err != nil {
		return fmt.Errorf("发送失败：%v", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("HTTP 状态码：%d - %s", resp.StatusCode, string(body))
	}
	
	fmt.Println("   ✅ 飞书通知已发送（Webhook 模式）")
	return nil
}

// sendViaAPI sends notification via Feishu API
func (p *FeishuNotifyPlugin) sendViaAPI(title, content, msgType string) error {
	if p.config.AppID == "" || p.config.AppSecret == "" {
		return fmt.Errorf("AppID 或 AppSecret 未配置")
	}
	
	// Get access token
	token, err := p.getAccessToken()
	if err != nil {
		return fmt.Errorf("获取 Token 失败：%v", err)
	}
	
	// Send message
	err = p.sendMessage(token, title, content, msgType)
	if err != nil {
		return fmt.Errorf("发送消息失败：%v", err)
	}
	
	fmt.Println("   ✅ 飞书通知已发送（API 模式）")
	return nil
}

// getAccessToken gets Feishu access token
func (p *FeishuNotifyPlugin) getAccessToken() (string, error) {
	tokenURL := "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
	
	payload := map[string]string{
		"app_id":     p.config.AppID,
		"app_secret": p.config.AppSecret,
	}
	
	jsonData, _ := json.Marshal(payload)
	resp, err := p.client.Post(tokenURL, "application/json", bytes.NewReader(jsonData))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	
	var result struct {
		Code              int    `json:"code"`
		Msg               string `json:"msg"`
		TenantAccessToken string `json:"tenant_access_token"`
	}
	
	json.NewDecoder(resp.Body).Decode(&result)
	
	if result.Code != 0 {
		return "", fmt.Errorf("Token 请求失败：%s", result.Msg)
	}
	
	return result.TenantAccessToken, nil
}

// sendMessage sends a message via Feishu API
func (p *FeishuNotifyPlugin) sendMessage(token, title, content, msgType string) error {
	msgURL := "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
	
	var msgContent string
	if msgType == "text" {
		msgContent = fmt.Sprintf(`{"text":"📬 %s\n%s"}`, title, content)
	} else if msgType == "post" {
		msgContent = fmt.Sprintf(`{"post":{"zh_cn":{"title":"%s","content":[[{"tag":"text","text":"%s"}]]}}}`, title, content)
	}
	
	payload := map[string]string{
		"receive_id": p.config.UserID,
		"msg_type":   msgType,
		"content":    msgContent,
	}
	
	jsonData, _ := json.Marshal(payload)
	
	req, _ := http.NewRequest("POST", msgURL, bytes.NewReader(jsonData))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)
	
	resp, err := p.client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	
	var result struct {
		Code int    `json:"code"`
		Msg  string `json:"msg"`
	}
	
	json.NewDecoder(resp.Body).Decode(&result)
	
	if result.Code != 0 {
		return fmt.Errorf("消息发送失败：%s", result.Msg)
	}
	
	return nil
}

// SendTest sends a test notification
func (p *FeishuNotifyPlugin) SendTest() error {
	title := "goEX 测试通知"
	content := fmt.Sprintf("- **测试**: 飞书通知连通性\n- **状态**: ✅ 成功\n- **时间**: %s", time.Now().Format("2006-01-02 15:04:05"))
	
	_, err := p.Execute(map[string]interface{}{
		"title":   title,
		"content": content,
	})
	
	return err
}

// Shutdown cleans up plugin resources
func (p *FeishuNotifyPlugin) Shutdown() error {
	fmt.Println("📬 Feishu-Notify 插件已关闭")
	return nil
}

// Helper functions for backward compatibility

// TestFeishuWebhook tests webhook connectivity
func TestFeishuWebhook(webhook string) error {
	msg := fmt.Sprintf("## goEX 测试通知\n- **测试**: 飞书 Webhook 连通性\n- **状态**: ✅ 成功\n- **时间**: %s", time.Now().Format("2006-01-02 15:04:05"))
	
	payload := fmt.Sprintf(`{"msg_type": "post", "content": {"post": {"zh_cn": {"title": "goEX 测试通知", "content": [[{"tag": "text", "text": "%s"}]]}}}}`, msg)
	
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Post(webhook, "application/json", strings.NewReader(payload))
	if err != nil {
		return fmt.Errorf("发送失败：%v", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != 200 {
		return fmt.Errorf("HTTP 状态码：%d", resp.StatusCode)
	}
	
	fmt.Println("   ✅ 飞书 Webhook 测试成功")
	return nil
}
