# Go Image Skill 使用文档

---

## CLI 命令

### analyze - 分析单张图片

```bash
# 基本用法
image-skill analyze photo.jpg

# 带自然语言查询
image-skill analyze photo.jpg "照片里有几个人？"

# 输出 JSON
image-skill analyze photo.jpg | jq .
```

### batch - 批量分析

```bash
# 分析目录下所有图片
image-skill batch ./photos/

# 分析递归子目录
image-skill batch ./photos/ --recursive

# 限制并发数
image-skill batch ./photos/ --workers 4
```

### query - 自然语言查询

```bash
# 查询单张图片
image-skill query "这张照片是在哪里拍的？" photo.jpg

# 查询多张图片
image-skill query "有猫的照片" ./photos/
```

### search - 搜索图片

```bash
# 搜索关键词
image-skill search "海边" ./photos/

# 搜索带过滤
image-skill search "人物" ./photos/ --date-from 2026-01-01
```

### compare - 比对图片

```bash
# 比对两张图片
image-skill compare photo1.jpg photo2.jpg

# 比对多张图片 (找出最相似的)
image-skill compare photo1.jpg photo2.jpg photo3.jpg
```

### serve - 启动 HTTP 服务

```bash
# 默认端口 8080
image-skill serve

# 指定端口
image-skill serve --port 8081

# 指定配置
image-skill serve --config configs/config.local.yaml
```

### version - 显示版本

```bash
image-skill version
```

### help - 显示帮助

```bash
image-skill help
image-skill analyze --help
```

---

## 使用场景

### 场景 1: Agent 图像分析

```
用户 (飞书) → 发送图片 + "这张图里有什么？"
    ↓
Agent → 调用 /analyze API
    ↓
图像分析 → 返回分析结果
    ↓
Agent → 生成自然语言回复
    ↓
用户 ← 收到回复
```

### 场景 2: 批量整理照片

```bash
# 分析所有照片
image-skill batch ./vacation_photos/

# 按场景分类
image-skill search "beach" ./vacation_photos/ > beach_photos.txt
image-skill search "mountain" ./vacation_photos/ > mountain_photos.txt

# 找出重复照片
image-skill batch ./vacation_photos/ --find-duplicates
```

### 场景 3: 隐私保护

```bash
# 自动模糊人脸
image-skill batch ./public_photos/ --blur-faces

# 自动模糊车牌
image-skill batch ./public_photos/ --blur-license-plates
```

### 场景 4: 照片搜索

```bash
# 找出去年的海边照片
image-skill search "海边" ./photos/ --date-from 2025-01-01 --date-to 2025-12-31

# 找出有特定人物的照片
image-skill search "张三" ./photos/
```

---

## 输出格式

### JSON 输出 (默认)

```json
{
  "file_path": "photo.jpg",
  "dimensions": {"width": 1920, "height": 1080},
  "scene": "beach",
  "objects": [{"name": "person", "confidence": 0.95}],
  "exif": {"date_time": "2026-04-15 10:30:00"}
}
```

### 文本输出

```bash
image-skill analyze photo.jpg --format text
```

```
文件：photo.jpg
尺寸：1920x1080
格式：jpeg
场景：beach
物体：person (95%)
拍摄时间：2026-04-15 10:30:00
```

### 飞书卡片输出

```bash
image-skill analyze photo.jpg --format feishu
```

---

## 高级用法

### 使用缓存

```bash
# 启用缓存 (默认开启)
image-skill analyze photo.jpg --cache

# 清空缓存
image-skill cache clear

# 查看缓存统计
image-skill cache stats
```

### 批量处理队列

```bash
# 提交批量任务
image-skill batch ./photos/ --queue

# 查看队列状态
image-skill queue status

# 取消任务
image-skill queue cancel <task_id>
```

### 自定义配置

```bash
# 使用自定义配置
image-skill serve --config my-config.yaml

# 环境变量覆盖
export IMAGE_SKILL_PORT=9090
image-skill serve
```

---

## 最佳实践

### 性能优化

1. **启用缓存** - 重复分析的图片直接从缓存读取
2. **调整并发数** - 根据服务器性能调整 workers 数量
3. **限制图片大小** - 避免处理超大图片

### 安全建议

1. **限制上传大小** - 防止 DoS 攻击
2. **验证文件格式** - 只接受图片格式
3. **隔离运行环境** - 使用 Docker 容器

### 监控建议

1. **启用健康检查** - 定期检查服务状态
2. **收集指标** - 监控请求量、响应时间
3. **设置告警** - 异常时及时通知

---

## 常见问题

### Q: 如何处理大量图片？

A: 使用批量处理 + 队列：
```bash
image-skill batch ./large_folder/ --queue --workers 8
```

### Q: 如何提高 OCR 准确率？

A: 确保图片清晰，文字区域明显：
```bash
image-skill analyze photo.jpg --ocr-enhance
```

### Q: 如何集成到现有系统？

A: 使用 HTTP API：
```bash
curl -X POST http://localhost:8080/analyze -F "file=@photo.jpg"
```
