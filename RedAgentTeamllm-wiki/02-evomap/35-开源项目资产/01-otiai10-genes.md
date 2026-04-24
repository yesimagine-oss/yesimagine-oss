---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Otiai10 Genes
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
# otiai10 Genes - 验证核心

**来源:** otiai10 GitHub Profile (28 个仓库完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `otiai10_repo_metadata_parse` | otiai10 仓库元数据解析验证 | `pytest tests/test_otiai10_metadata.py` |
| 2 | `otiai10_go_build_validate` | Go 项目跨仓库构建验证 | `node tests/otiai10-go-build.test.js` |
| 3 | `otiai10_cgo_env_check` | CGO 环境验证 (Tesseract/Leptonica) | `pytest tests/test_otiai10_cgo.py` |
| 4 | `otiai10_dep_install_verify` | 跨平台依赖安装验证 | `node tests/otiai10-dep-install.test.js` |

---

## Gene 详细说明

### 1. otiai10_repo_metadata_parse

**用途:** 解析和验证 otiai10 GitHub 仓库元数据

**关键检查点:**
- 仓库基本信息 (名称/描述/语言)
- Star/Fork 数量统计
- 许可证信息
- 最后更新时间

**命令:**
```bash
gh api users/otiai10/repos --paginate | \
  jq '.[] | {name: .full_name, language: .language, stars: .stargazers_count}'
```

---

### 2. otiai10_go_build_validate

**用途:** 验证 otiai10 Go 项目构建

**检查项:**
- `go mod tidy` 执行成功
- `go build -v ./...` 编译通过
- `go test -v ./...` 测试通过
- 跨平台构建 (Linux/macOS/Windows)

**验证流程:**
```bash
cd {repo}
go mod tidy
go build -v ./...
go test -v ./...
```

---

### 3. otiai10_cgo_env_check

**用途:** 验证 CGO 环境配置 (Tesseract/Leptonica)

**检查项:**
- Tesseract OCR 安装
- Leptonica 库安装
- CGO_ENABLED 环境变量
- pkg-config 配置

**环境配置:**
```bash
# Ubuntu/Debian
apt install -y tesseract-ocr libtesseract-dev libleptonica-dev

# macOS
brew install tesseract leptonica

# 验证
pkg-config --cflags --libs leptonica
export CGO_ENABLED=1
```

---

### 4. otiai10_dep_install_verify

**用途:** 验证跨平台依赖安装

**检查项:**
- Linux (apt/yum)
- macOS (brew)
- Windows (choco/scoop)
- Docker 容器

**依赖列表:**
| 依赖 | 用途 | Linux | macOS |
|------|------|-------|-------|
| tesseract-ocr | OCR 引擎 | ✅ apt | ✅ brew |
| libtesseract-dev | Tesseract 开发库 | ✅ apt | ✅ brew |
| libleptonica-dev | Leptonica 图像库 | ✅ apt | ✅ brew |

---

**状态:** ✅ 已验证可复用
**适用场景:** Go + CGO 项目开发，特别是 OCR 相关项目

---

## 与 go-image-skill 项目的关联

| Gene | 直接应用 |
|------|----------|
| `otiai10_cgo_env_check` | go-image-skill OCR 功能必需 |
| `otiai10_go_build_validate` | go-image-skill 构建验证 |
| `otiai10_dep_install_verify` | go-image-skill 依赖安装 |

---

**特殊价值:** 此资产包为 go-image-skill 项目提供**直接的 CGO 和 OCR 集成支持**


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]
