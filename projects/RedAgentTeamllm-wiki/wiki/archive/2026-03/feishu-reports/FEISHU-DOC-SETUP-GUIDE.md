---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 飞书云文档配置指南
- guide
- setup
title: Feishu Doc Setup Guide
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
# 📄 飞书云文档配置指南

**创建时间**: 2026-03-19 20:10  
**状态**: ⏳ 需要配置权限

---

## 📊 当前权限状态

### 已有权限

| 权限 | 状态 |
|------|------|
| `docs:document:import` | ✅ 已有 |
| `docs:document.content:read` | ✅ 已有 |
| `aily:file:write` | ✅ 已有 |
| `wiki:wiki:readonly` | ✅ 已有（只读） |

### 缺少的权限/配置

| 项目 | 状态 | 说明 |
|------|------|------|
| 飞书应用文档创建权限 | ⏳ 待确认 | 需要在开放平台配置 |
| 知识库空间访问 | ❌ 无权限 | 需要添加机器人到空间 |
| 云盘访问 | ⏳ 待测试 | 可能需要额外权限 |

---

## 🎯 配置方案

### 方案 A: 飞书应用添加文档权限 ⭐⭐⭐⭐⭐

**步骤：**

1. **登录飞书开放平台**
   - 访问：https://open.feishu.cn
   - 登录管理员账号

2. **进入企业自建应用**
   - 选择你的应用
   - 点击"权限管理"

3. **添加文档权限**
   - 搜索 "docs"
   - 添加以下权限：
     - `docs:document` - 文档基础权限
     - `docs:document:write` - 文档写入权限
     - `docs:document:create` - 文档创建权限

4. **发布应用**
   - 点击"发布"
   - 等待审核（通常自动通过）

5. **重新授权**
   - 在飞书中移除应用
   - 重新添加应用
   - 授予新权限

---

### 方案 B: 知识库空间授权 ⭐⭐⭐⭐

**步骤：**

1. **打开飞书知识库**
   - 访问：https://xxx.feishu.cn/wiki/
   - 选择要授权的知识空间

2. **添加机器人为成员**
   - 点击空间设置
   - 选择"成员与权限"
   - 添加机器人应用
   - 授予编辑权限

3. **获取空间 Token**
   - 在空间设置中复制空间 ID
   - 用于 API 调用

---

### 方案 C: 使用现有权限创建 ⭐⭐⭐

**尝试使用已有权限：**

1. **使用 `docs:document:import`**
   - 这个权限可能包含创建能力
   - 需要测试

2. **使用 `aily:file:write`**
   - 上传文件到飞书
   - 然后转换为文档

---

## 🔧 测试命令

### 测试 1: 创建文档

```bash
# 使用 feishu_doc 工具
feishu_doc action=create title="测试文档" owner_open_id="ou_f4919832188bcc630f8f257497fa93a4"
```

**预期结果：**
- ✅ 成功：返回 doc_token
- ❌ 失败：错误信息

---

### 测试 2: 列出知识库空间

```bash
feishu_wiki action=spaces
```

**预期结果：**
- ✅ 成功：返回空间列表
- ❌ 失败：需要授权

---

### 测试 3: 列出云盘文件

```bash
feishu_drive action=list
```

**预期结果：**
- ✅ 成功：返回文件列表
- ❌ 失败：权限不足

---

## 📝 临时解决方案

### 方案 1: 手动创建文档

1. 在飞书手动创建文档
2. 复制 doc_token
3. 用 API 写入内容

**示例：**
```bash
# 写入内容到现有文档
feishu_doc action=write doc_token="ABC123def" content="# 内容"
```

---

### 方案 2: 使用邮件发送文档内容

1. 生成文档内容
2. 通过邮件发送给自己
3. 手动复制到飞书

---

### 方案 3: 使用飞书消息发送文档

1. 生成文档内容
2. 通过飞书机器人发送
3. 用户手动保存为文档

**示例：**
```
📄 新文档已生成

标题：测试文档
内容：
# 标题

正文内容...

---
💡 提示：点击"收藏"保存为云文档
```

---

## 🐛 故障排查

### 问题 1: 创建文档返回 400

**原因：**
- 缺少 owner_open_id
- 权限不足
- API 参数错误

**解决：**
1. 确保传递 owner_open_id
2. 检查应用权限
3. 查看 API 文档

---

### 问题 2: 知识库返回空列表

**原因：**
- 机器人未添加到空间
- 权限不足

**解决：**
1. 在知识库空间添加机器人
2. 授予编辑权限

---

### 问题 3: 云盘访问失败

**原因：**
- 缺少云盘权限
- API 配置错误

**解决：**
1. 在开放平台添加云盘权限
2. 重新授权应用

---

## 📖 API 参考

### 创建文档

```json
{
  "action": "create",
  "title": "文档标题",
  "owner_open_id": "ou_xxx",
  "folder_token": "fldcnXXX"  // 可选
}
```

### 写入文档内容

```json
{
  "action": "write",
  "doc_token": "ABC123def",
  "content": "# Markdown 内容"
}
```

### 上传文件

```json
{
  "action": "upload_file",
  "file_path": "/path/to/file.pdf",
  "parent_folder_token": "fldcnXXX"
}
```

---

## 🎯 下一步

### 立即执行

1. **检查飞书应用权限**
   - 登录开放平台
   - 查看已开通权限
   - 添加文档相关权限

2. **测试创建文档**
   - 使用 feishu_doc 工具
   - 传递 owner_open_id
   - 查看返回结果

3. **配置知识库空间**
   - 添加机器人到空间
   - 获取空间 token
   - 测试创建 Wiki 节点

---

## 📞 需要帮助？

### 提供以下信息

1. **飞书应用 ID**
   ```bash
   # 查看配置
   cat ~/.openclaw/config/feishu.json | grep app_id
   ```

2. **错误信息**
   ```bash
   # 完整错误输出
   feishu_doc action=create title="测试" 2>&1
   ```

3. **权限列表**
   ```bash
   feishu_app_scopes
   ```

---

**最后更新**: 2026-03-19  
**维护者**: 麻小 🦐

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[feishu-evolution-20260413]]
- [[21-user_guide_image_analysis_skill]]
