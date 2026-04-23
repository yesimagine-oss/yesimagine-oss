package skill

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

// InputData 输入数据
type InputData struct {
	Text string
}

// Context 技能上下文
type Context struct {
	Input InputData
}

// Reply 回复
func (c *Context) Reply(text string) error {
	fmt.Println(text)
	return nil
}

// Response HTTP 响应包装器
type Response struct {
	body []byte
}

// Body 返回响应体
func (r *Response) Body() []byte {
	return r.body
}

// HTTPClient HTTP 客户端包装器
type HTTPClient struct {
	headers map[string]string
	client  *http.Client
}

// WithHeader 设置请求头
func (h *HTTPClient) WithHeader(key, value string) *HTTPClient {
	h.headers[key] = value
	return h
}

// Post 发送 POST 请求
func (h *HTTPClient) Post(url string, body []byte) (*Response, error) {
	req, err := http.NewRequest("POST", url, bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	for k, v := range h.headers {
		req.Header.Set(k, v)
	}
	resp, err := h.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	return &Response{body: respBody}, nil
}

// Log 日志输出
func Log(level, format string, args ...interface{}) {
	msg := fmt.Sprintf("[%s] "+format, append([]interface{}{level}, args...)...)
	log.Println(msg)
}

// Env 获取环境变量
func Env(key string) string {
	return os.Getenv(key)
}

// HTTP 返回 HTTP 客户端
func HTTP() *HTTPClient {
	return &HTTPClient{
		headers: make(map[string]string),
		client:  &http.Client{},
	}
}

// Register 注册技能
func Register(name string, handler func(*Context) error) {
	log.Printf("Registered skill: %s", name)
}

// Run 运行技能
func Run() {
	log.Println("Skill running")
}
