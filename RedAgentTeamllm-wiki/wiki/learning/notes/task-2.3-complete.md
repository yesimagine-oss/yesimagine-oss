---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 任务
- 学习笔记
- 修改并扩展
- url
- shortener
title: Task 2.3 Complete
type: general
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
# 📚 任务 2.2 学习笔记：修改并扩展 url-shortener 功能

**完成时间**: 2026-03-13 10:50 GMT+8  
**扩展内容**: 3 个新脚本 + 文档更新  
**开发时长**: ~5 分钟

---

## 🎯 扩展目标

实现 SKILL.md 中提到但未实现的功能：
1. ✅ delete.py - 删除链接
2. ✅ export.py - 导出数据
3. ✅ qr.py - 生成 QR 码

---

## 🛠️ 开发过程

### 1. delete.py (2.5KB)

**功能**: 删除短链接及其点击记录

**核心实现**:
```python
def delete_link(short_code: str, skip_confirm: bool = False):
    # 1. 检查链接是否存在
    link = conn.execute(
        "SELECT short_code, original_url, clicks FROM links WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    
    # 2. 显示链接信息
    console.print(Panel(...))  # 删除前确认信息
    
    # 3. 确认删除（除非 --confirm）
    if not skip_confirm:
        confirm = console.input("Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            return
    
    # 4. 先删除点击记录（外键约束）
    conn.execute("DELETE FROM clicks WHERE short_code = ?", (short_code,))
    
    # 5. 删除链接
    conn.execute("DELETE FROM links WHERE short_code = ?", (short_code,))
    conn.commit()
```

**CLI 参数**:
```python
parser.add_argument("short_code", help="Short code to delete")
parser.add_argument("--confirm", "-y", action="store_true", help="Skip confirmation")
```

**设计亮点**:
- ✅ 删除前显示链接信息
- ✅ 默认要求确认（安全）
- ✅ 支持 --confirm 跳过确认
- ✅ 正确处理外键约束（先删 clicks）

---

### 2. export.py (2.6KB)

**功能**: 导出链接数据为 JSON 或 CSV

**核心实现**:
```python
def export_links(format: str = "json", output_file: str = None):
    # 1. 查询所有链接
    rows = conn.execute("""
        SELECT short_code, original_url, created_at, clicks, last_clicked
        FROM links
        ORDER BY created_at DESC
    """).fetchall()
    
    # 2. 根据格式导出
    if format == "json":
        output = json.dumps(links, indent=2, default=str)
    elif format == "csv":
        output_buffer = io.StringIO()
        writer = csv.DictWriter(output_buffer, fieldnames=[...])
        writer.writeheader()
        writer.writerows(links)
        output = output_buffer.getvalue()
    
    # 3. 输出到文件或 stdout
    if output_file:
        Path(output_file).write_text(output)
    else:
        print(output)
```

**CLI 参数**:
```python
parser.add_argument("--format", "-f", default="json", choices=["json", "csv"])
parser.add_argument("--output", "-o", help="Output file path")
parser.add_argument("--stats", action="store_true", help="Include click statistics")
```

**设计亮点**:
- ✅ 支持 JSON 和 CSV 格式
- ✅ 可输出到文件或 stdout
- ✅ 使用 csv.DictWriter 规范格式
- ✅ 默认按创建时间倒序

---

### 3. qr.py (2.7KB)

**功能**: 为短链接生成 QR 码

**核心实现**:
```python
def generate_qr(short_code: str, output_file: str = None):
    # 1. 检查依赖
    try:
        import qrcode
    except ImportError:
        console.print("qrcode library not installed.")
        console.print("Install with: pip install qrcode[pil]")
        sys.exit(1)
    
    # 2. 获取链接信息
    link = conn.execute(
        "SELECT short_code, original_url FROM links WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    
    # 3. 生成短 URL
    domain = os.getenv("SHORTENER_DOMAIN", DEFAULT_DOMAIN)
    short_url = f"https://{domain}/{short_code}"
    
    # 4. 生成 QR 码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 5. 保存
    if output_file:
        img.save(output_file)
    else:
        img.save(f"{short_code}_qr.png")
```

**依赖声明**:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "qrcode"]
# ///
```

**设计亮点**:
- ✅ 优雅的依赖缺失处理
- ✅ 可自定义输出文件名
- ✅ 使用 qrcode 库（标准选择）
- ✅ 显示生成的 URL

---

## 📊 代码统计对比

### 扩展前
| 脚本 | 大小 |
|------|------|
| shorten.py | 7.7KB |
| list.py | 3.4KB |
| stats.py | 3.4KB |
| **总计** | **14.5KB** |

### 扩展后
| 脚本 | 大小 | 新增功能 |
|------|------|---------|
| shorten.py | 7.7KB | - |
| list.py | 3.4KB | - |
| stats.py | 3.4KB | - |
| delete.py | 2.5KB | ✅ 删除链接 |
| export.py | 2.6KB | ✅ 导出数据 |
| qr.py | 2.7KB | ✅ QR 码生成 |
| **总计** | **22.3KB** | **+54%** |

---

## 📝 文档更新

### SKILL.md 更新内容

#### 1. 添加 QR 码使用示例
```markdown
**生成 QR 码**:
```bash
uv run scripts/qr.py <短码>
uv run scripts/qr.py <短码> -o custom-qr.png
```
```

#### 2. 更新脚本说明表格
| 脚本 | 功能 | 示例 |
|------|------|------|
| `qr.py` | 生成 QR 码 | `uv run scripts/qr.py <code>` |

#### 3. 完善删除和导出示例
```markdown
**删除链接**:
```bash
uv run scripts/delete.py <短码>
uv run scripts/delete.py <短码> --confirm  # 跳过确认
```

**导出链接**:
```bash
uv run scripts/export.py --format json
uv run scripts/export.py --format csv -o links.csv
```
```

---

## 💡 开发收获

### 1. 一致性设计

所有新脚本遵循相同模式：
- ✅ uv inline metadata 声明依赖
- ✅ Rich 库彩色输出
- ✅ argparse CLI 参数
- ✅ 清晰的错误信息
- ✅ 设置执行权限

### 2. 安全设计

**delete.py**:
- 删除前显示信息
- 默认要求确认
- 正确处理外键约束

### 3. 用户体验

**export.py**:
- 支持 stdout 输出（便于管道）
- 支持文件输出
- 多种格式选择

**qr.py**:
- 自动默认文件名
- 依赖缺失友好提示
- 显示生成的 URL

### 4. 错误处理

所有脚本都包含：
- ✅ 数据库不存在检查
- ✅ 链接不存在检查
- ✅ 依赖缺失检查
- ✅ 清晰的错误信息

---

## 🔍 代码质量检查

| 指标 | delete.py | export.py | qr.py |
|------|-----------|-----------|-------|
| 依赖声明 | ✅ | ✅ | ✅ |
| shebang | ✅ | ✅ | ✅ |
| docstring | ✅ | ✅ | ✅ |
| 错误处理 | ✅ | ✅ | ✅ |
| CLI 参数 | ✅ | ✅ | ✅ |
| 执行权限 | ✅ | ✅ | ✅ |

---

## 🚀 测试建议

### delete.py 测试
```bash
# 测试删除（带确认）
uv run scripts/delete.py abc123

# 测试删除（跳过确认）
uv run scripts/delete.py abc123 --confirm

# 测试删除不存在的链接
uv run scripts/delete.py nonexistent
```

### export.py 测试
```bash
# JSON 导出到 stdout
uv run scripts/export.py --format json

# CSV 导出到文件
uv run scripts/export.py --format csv -o links.csv

# 查看导出文件
cat links.csv
```

### qr.py 测试
```bash
# 生成 QR 码（默认文件名）
uv run scripts/qr.py abc123

# 生成 QR 码（自定义文件名）
uv run scripts/qr.py abc123 -o custom.png

# 测试依赖缺失（未安装 qrcode 时）
uv run scripts/qr.py abc123
```

---

## 📦 打包更新

扩展后的技能结构：
```
url-shortener.skill (更新版)
├── SKILL.md (已更新)
├── scripts/
│   ├── shorten.py (7.7KB)
│   ├── list.py (3.4KB)
│   ├── stats.py (3.4KB)
│   ├── delete.py (2.5KB) ✨ 新增
│   ├── export.py (2.6KB) ✨ 新增
│   └── qr.py (2.7KB) ✨ 新增
└── references/
    └── api-reference.md (7.6KB)
```

**总大小**: ~30KB（原 26KB）

---

## ✅ 检查清单

- [x] 实现 delete.py 脚本 ✅
- [x] 实现 export.py 脚本 ✅
- [x] 实现 qr.py 脚本 ✅
- [x] 更新 SKILL.md 文档 ✅
- [x] 设置执行权限 ✅
- [x] 添加依赖声明 ✅
- [x] 错误处理完善 ✅

**自评**: 成功扩展 url-shortener 功能，代码质量与原有脚本保持一致

---

**下一步**: 阶段 3 - 实践开发（开发第一个原创技能）

## 參考

- [[Asset05 Task Solution Template]]


## 相關文檔

- [[evomap_task_template]]
- [[knowledge-files-complete-list]]
- [[task_solution_template]]
