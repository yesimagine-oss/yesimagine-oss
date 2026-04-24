---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 飞书云文档配置
- 当前状态
title: Feishu Doc Status
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
# ✅ 飞书云文档配置 - 当前状态

**创建时间**: 2026-03-19 20:10  
**状态**: ⏳ 需要飞书开放平台配置

---

## 📊 当前权限

### 已有权限 ✅

| 权限 | 说明 |
|------|------|
| `docs:document:import` | 可以导入文档 |
| `docs:document.content:read` | 可以读取文档内容 |
| `aily:file:write` | 可以上传文件 |

### 可能需要的权限 ⏳

| 权限 | 说明 |
|------|------|
| `docs:document` | 文档基础权限 |
| `docs:document:write` | 文档写入权限 |
| `docs:document:create` | 文档创建权限 |

---

## 🎯 测试结果

### 测试 1: 创建文档 ❌

**命令：**
```bash
feishu_doc action=create title="测试文档" owner_open_id="ou_f4919832188bcc630f8f257497fa93a4"
```

**结果：** 返回 400 错误

**可能原因：**
1. 缺少创建权限
2. API 调用方式不对
3. 需要额外参数

---

### 测试 2: 知识库空间 ❌

**命令：**
```bash
feishu_wiki action=spaces
```

**结果：** 返回空列表，提示需要授权

**原因：** 机器人未添加到知识库空间

---

### 测试 3: 云盘访问 ❌

**命令：**
```bash
feishu_drive action=list
```

**结果：** 返回 400 错误

**原因：** 可能缺少云盘权限

---

## 📋 配置步骤

### 步骤 1: 飞书开放平台配置 ⭐⭐⭐⭐⭐

1. **登录开放平台**
   - https://open.feishu.cn

2. **进入应用管理**
   - 选择你的企业自建应用

3. **添加权限**
   - 权限管理 → 添加权限
   - 搜索 "docs"
   - 添加：
     - `docs:document` - 文档管理
     - `docs:document:write` - 文档写入
     - `docs:document:create` - 文档创建

4. **发布应用**
   - 点击"发布"
   - 等待审核（通常自动通过）

5. **重新授权**
   - 在飞书中移除应用
   - 重新添加应用
   - 授予所有权限

---

### 步骤 2: 知识库空间授权（可选）⭐⭐⭐⭐

如果需要操作知识库：

1. **打开知识库空间**
   - 飞书 → 知识库
   - 选择要授权的空间

2. **添加机器人**
   - 空间设置 → 成员与权限
   - 添加机器人应用
   - 授予编辑权限

3. **获取空间 Token**
   - 空间设置 → 复制空间 ID

---

### 步骤 3: 测试配置 ⭐⭐⭐⭐⭐

配置完成后测试：

```bash
# 测试创建文档
feishu_doc action=create title="测试文档" owner_open_id="ou_f4919832188bcc630f8f257497fa93a4"

# 测试列出空间
feishu_wiki action=spaces

# 测试云盘
feishu_drive action=list
```

---

## 📖 使用示例

### 示例 1: 创建文档

```bash
feishu_doc action=create \
  title="邮件发送记录" \
  owner_open_id="ou_f4919832188bcc630f8f257497fa93a4"
```

**返回：**
```json
{
  "doc_token": "ABC123def",
  "title": "邮件发送记录"
}
```

---

### 示例 2: 写入文档内容

```bash
feishu_doc action=write \
  doc_token="ABC123def" \
  content="# 邮件发送记录\n\n2026-03-19: 发送测试邮件成功"
```

---

### 示例 3: 上传文件

```bash
feishu_doc action=upload_file \
  file_path="/path/to/file.pdf" \
  parent_folder_token="fldcnXXX"
```

---

## 🐛 故障排查

### 问题 1: 创建文档返回 400

**检查：**
1. 是否有 `owner_open_id` 参数
2. 应用是否有创建权限
3. 用户是否有权限创建文档

**解决：**
```bash
# 确保传递 owner_open_id
feishu_doc action=create title="测试" owner_open_id="ou_xxx"
```

---

### 问题 2: 权限不足

**检查：**
```bash
feishu_app_scopes
```

**解决：**
1. 开放平台添加权限
2. 重新发布应用
3. 重新授权

---

### 问题 3: 知识库空列表

**原因：** 机器人未添加到空间

**解决：**
1. 在知识库空间添加机器人
2. 授予编辑权限

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `FEISHU-DOC-SETUP-GUIDE.md` | 详细配置指南 |
| `tools/test-feishu-doc.py` | 测试脚本 |
| `tools/test-feishu-doc.sh` | Bash 测试脚本 |

---

## 🎯 下一步

### 立即执行

1. **登录飞书开放平台**
   - 添加文档相关权限
   - 发布应用

2. **重新授权应用**
   - 飞书中移除应用
   - 重新添加

3. **测试创建文档**
   - 使用 feishu_doc 工具
   - 传递 owner_open_id

---

### 备选方案

如果 API 创建不可用：

1. **手动创建文档**
   - 飞书手动创建
   - 复制 doc_token
   - API 写入内容

2. **使用飞书消息**
   - 生成内容
   - 机器人发送
   - 用户手动保存

---

## 📞 需要帮助？

提供以下信息：

1. **飞书应用 ID**
2. **权限列表** (`feishu_app_scopes`)
3. **错误信息**（完整输出）

---

**最后更新**: 2026-03-19 20:10  
**维护者**: 麻小 🦐

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[feishu-evolution-20260413]]
- [[feishu-merged-learning-report]]
- [[04-feishu_docs_block_parse]]
