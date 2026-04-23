package queue

import (
	"sync"
	"time"

	"github.com/openclaw/go-image-skill/internal/image"
)

// AnalysisTask 分析任务
type AnalysisTask struct {
	ID        string
	ImagePath string
	Query     string
	Priority  int
	CreatedAt time.Time
}

// AnalysisResult 分析结果
type AnalysisResult struct {
	TaskID string
	Result *image.AnalysisResult
	Error  error
}

// TaskQueue 任务队列
type TaskQueue struct {
	tasks     chan *AnalysisTask
	results   chan *AnalysisResult
	workers   int
	wg        sync.WaitGroup
	running   bool
	mu        sync.Mutex
}

// NewTaskQueue 创建任务队列
func NewTaskQueue(workers int) *TaskQueue {
	q := &TaskQueue{
		tasks:   make(chan *AnalysisTask, 100),
		results: make(chan *AnalysisResult, 100),
		workers: workers,
	}
	return q
}

// Start 启动队列
func (q *TaskQueue) Start(analyzer *image.ImageAnalyzer) {
	q.mu.Lock()
	defer q.mu.Unlock()

	if q.running {
		return
	}

	q.running = true

	for i := 0; i < q.workers; i++ {
		q.wg.Add(1)
		go q.worker(analyzer)
	}
}

// Stop 停止队列
func (q *TaskQueue) Stop() {
	q.mu.Lock()
	defer q.mu.Unlock()

	if !q.running {
		return
	}

	q.running = false
	close(q.tasks)
	q.wg.Wait()
	close(q.results)
}

// Submit 提交任务
func (q *TaskQueue) Submit(task *AnalysisTask) {
	q.tasks <- task
}

// Results 获取结果通道
func (q *TaskQueue) Results() <-chan *AnalysisResult {
	return q.results
}

// worker 工作协程
func (q *TaskQueue) worker(analyzer *image.ImageAnalyzer) {
	defer q.wg.Done()

	for task := range q.tasks {
		result, err := analyzer.Analyze(task.ImagePath)

		q.results <- &AnalysisResult{
			TaskID: task.ID,
			Result: result,
			Error:  err,
		}
	}
}

// BatchSubmit 批量提交任务
func (q *TaskQueue) BatchSubmit(imagePaths []string, query string) []string {
	taskIDs := make([]string, len(imagePaths))

	for i, path := range imagePaths {
		taskID := generateTaskID()
		taskIDs[i] = taskID

		q.Submit(&AnalysisTask{
			ID:        taskID,
			ImagePath: path,
			Query:     query,
			Priority:  0,
			CreatedAt: time.Now(),
		})
	}

	return taskIDs
}

// generateTaskID 生成任务 ID
func generateTaskID() string {
	return time.Now().Format("20060102150405") + "-" + randomString(8)
}

// randomString 生成随机字符串
func randomString(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyz0123456789"
	b := make([]byte, n)
	for i := range b {
		b[i] = letters[time.Now().UnixNano()%int64(len(letters))]
	}
	return string(b)
}
