# Go Image Skill API 文档

---

## 基础信息

- **Base URL:** `http://localhost:8080`
- **Content-Type:** `multipart/form-data` 或 `application/json`
- **认证:** 暂无 (生产环境建议添加)

---

## 端点列表

### 1. 分析图片

**POST** `/analyze`

分析单张图片并返回详细结果。

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 图片文件 (最大 50MB) |
| query | String | 否 | 自然语言查询 |

**响应示例:**

```json
{
  "success": true,
  "data": {
    "file_path": "/tmp/image-123.jpg",
    "file_name": "photo.jpg",
    "file_size": 1024000,
    "dimensions": {"width": 1920, "height": 1080},
    "format": "jpeg",
    "color_analysis": {
      "dominant_colors": [
        {"hex": "#FF5733", "rgb": [255,87,51], "percent": 45.2}
      ],
      "brightness": 0.65,
      "contrast": 0.72
    },
    "scene": "outdoor",
    "objects": [
      {"name": "person", "confidence": 0.95, "box": {"x": 100, "y": 200, "width": 300, "height": 500}}
    ],
    "exif": {
      "date_time": "2026-04-15 10:30:00",
      "camera_model": "iPhone 15"
    },
    "confidence": 0.96
  }
}
```

**curl 示例:**

```bash
curl -X POST http://localhost:8080/analyze \
  -F "file=@photo.jpg" \
  -F "query=照片里有几个人？"
```

---

### 2. 自然语言查询

**POST** `/query`

对图片进行自然语言问答。

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | String | 是 | 自然语言问题 |
| image_id | String | 否 | 图片 ID (已分析过的) |
| file | File | 否 | 新图片文件 |

**响应示例:**

```json
{
  "success": true,
  "answer": "照片里有 3 个人，分别是 2 个成年人和 1 个小孩。他们站在海边，背景是夕阳。"
}
```

**curl 示例:**

```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "照片里有几个人？", "image_id": "abc123"}'
```

---

### 3. 搜索图片

**GET** `/search`

在图片库中搜索匹配的图片。

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | String | 是 | 搜索关键词 |
| dir | String | 否 | 搜索目录 (默认：/data) |
| limit | Integer | 否 | 返回数量限制 (默认：20) |

**响应示例:**

```json
{
  "success": true,
  "query": "海边",
  "total": 15,
  "results": [
    {
      "file_path": "/data/beach_001.jpg",
      "scene": "beach",
      "date_time": "2026-04-10",
      "confidence": 0.92
    }
  ]
}
```

**curl 示例:**

```bash
curl "http://localhost:8080/search?q=海边&limit=10"
```

---

### 4. 比对图片

**POST** `/compare`

比对两张图片的相似度。

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file1 | File | 是 | 第一张图片 |
| file2 | File | 是 | 第二张图片 |

**响应示例:**

```json
{
  "success": true,
  "similarity": 0.85,
  "details": {
    "color_similarity": 0.88,
    "structure_similarity": 0.82,
    "object_similarity": 0.85
  },
  "conclusion": "两张图片高度相似，可能是同一场景的不同角度拍摄。"
}
```

**curl 示例:**

```bash
curl -X POST http://localhost:8080/compare \
  -F "file1=@photo1.jpg" \
  -F "file2=@photo2.jpg"
```

---

### 5. 健康检查

**GET** `/health`

检查服务健康状态。

**响应示例:**

```json
{
  "status": "healthy",
  "uptime": "2h30m",
  "cache_size": 156,
  "queue_size": 3
}
```

**curl 示例:**

```bash
curl http://localhost:8080/health
```

---

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源未找到 |
| 413 | 文件过大 |
| 415 | 不支持的文件格式 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

**错误响应示例:**

```json
{
  "success": false,
  "error": "文件过大，最大支持 50MB"
}
```

---

## 限流说明

- 默认限流：100 请求/分钟
- 批量分析：10 图片/批次
- 超时时间：300 秒

---

## 认证 (未来版本)

计划支持 API Key 认证：

```bash
curl -X POST http://localhost:8080/analyze \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@photo.jpg"
```
