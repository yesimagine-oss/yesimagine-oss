---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Gocv Genes
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# GoCV Genes - 验证核心

**来源:** GoCV Official Docs (78 页完整覆盖)
**置信度:** 0.98
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `gocv_opencv_version_verify` | OpenCV >=4.0 安装验证 | `pytest tests/test_gocv_opencv.py` |
| 2 | `gocv_cgo_env_check` | CGO_ENABLED=1 和链接器标志验证 | `node tests/gocv-cgo-env.test.js` |
| 3 | `gocv_memory_validate` | Mat 资源释放检查 (防内存泄漏) | `pytest tests/test_gocv_memory.py` |
| 4 | `gocv_api_schema_verify` | GoCV API 调用结构验证 | `node tests/gocv-api-schema.test.js` |

---

## Gene 详细说明

### 1. gocv_opencv_version_verify

**用途:** 验证 OpenCV 安装版本

**关键检查点:**
- OpenCV 版本 >= 4.0
- 模块完整性检查
- 功能可用性测试

**命令:**
```bash
# 检查 OpenCV 版本
pkg-config --modversion opencv4

# GoCV 版本检查
go run ./cmd/version/main.go
```

---

### 2. gocv_cgo_env_check

**用途:** 验证 CGO 环境配置

**检查项:**
- `CGO_ENABLED=1` 环境变量
- C++ 编译器配置
- 链接器标志 (pkg-config)
- OpenCV 库路径

**环境配置:**
```bash
# 验证 CGO
go env CGO_ENABLED  # 应输出 1

# 验证 pkg-config
pkg-config --cflags --libs opencv4

# 设置环境变量 (如需要)
export CGO_ENABLED=1
export CGO_CXXFLAGS="--std=c++11"
export CGO_LDFLAGS="-lopencv_core -lopencv_imgproc"
```

---

### 3. gocv_memory_validate

**用途:** 检查 Mat 资源释放 (防止内存泄漏)

**检查项:**
- `defer img.Close()` 调用
- Mat 对象生命周期管理
- 内存泄漏检测

**正确模式:**
```go
img := gocv.IMRead("img.jpg", gocv.IMReadColor)
defer img.Close()  // 必须调用

gray := gocv.NewMat()
defer gray.Close()  // 必须调用

gocv.CvtColor(img, &gray, gocv.ColorBGRToGray)
// 使用后自动释放
```

---

### 4. gocv_api_schema_verify

**用途:** 验证 GoCV API 调用结构

**检查项:**
- 函数签名正确性
- 参数类型验证
- 返回值处理
- 错误处理模式

---

**状态:** ✅ 已验证可复用
**适用场景:** GoCV 计算机视觉项目开发

---

## 与 go-image-skill 项目的关联

| Gene | 直接应用 |
|------|----------|
| `gocv_cgo_env_check` | go-image-skill GoCV 环境配置 |
| `gocv_memory_validate` | go-image-skill 内存管理最佳实践 |
| `gocv_opencv_version_verify` | go-image-skill 依赖验证 |

---

**特殊价值:** 此资产包为 go-image-skill 项目提供**物体检测和高级图像处理能力**


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]
