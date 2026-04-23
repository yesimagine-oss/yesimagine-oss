# 🛠️ OpenClaw 技能开发框架

**版本**: 1.0.0  
**创建时间**: 2026-03-22  
**状态**: 🚀 ready to use

---

## 🎯 核心理念

**标准化、模块化、可复用、易维护**

---

## 📁 标准目录结构

```
skill-name/
├── SKILL.md                 # 【必需】技能定义文件
├── README.md                # 【必需】使用说明
├── requirements.txt         # 【可选】Python 依赖
├── package.json            # 【可选】Node.js 依赖
├── scripts/
│   ├── main.py             # 【核心】主逻辑入口
│   ├── utils.py            # 【工具】工具函数
│   └── config.py           # 【配置】配置管理
├── tests/
│   ├── test_main.py        # 【测试】单元测试
│   └── fixtures/           # 【测试】测试数据
├── config/
│   └── default.yaml        # 【配置】默认配置
└── logs/                   # 【日志】日志目录
```

---

## 📝 SKILL.md 标准模板

```markdown
---
name: skill-name
version: 1.0.0
description: 技能的简短描述（50 字以内）
author: 作者名
keywords: [关键词 1, 关键词 2, 关键词 3]
triggers:
 - "触发词 1"
 - "触发词 2"
 - "触发词 3"
metadata: {
  "clawdbot": {
    "emoji": "🔧",
    "requires": {
      "bins": ["python3"],
      "env": {
        "API_KEY": {"description": "API 密钥", "required": false}
      }
    }
  }
}
---

# 技能名称

**一句话亮点** - 突出核心优势

---

## 🚀 快速开始

### 使用示例

```
用户：触发词 + 参数
执行：
1. 步骤 1
2. 步骤 2
3. 步骤 3
```

---

## 🎯 核心功能

1. **功能 1** - 描述
2. **功能 2** - 描述
3. **功能 3** - 描述

---

## 📁 文件结构

```
skill-name/
├── SKILL.md
├── README.md
└── scripts/
    └── main.py
```

---

## 🔧 安装说明

### 系统要求

- Python 3.8+
- Node.js 16+（可选）

### 安装步骤

```bash
# 1. 复制技能到工作区
cp -r skill-name ~/.openclaw/workspace/skills/

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量（可选）
export API_KEY="your-key"
```

---

## 📖 使用示例

### 示例 1: 基础使用

```bash
# 命令
python3 scripts/main.py "参数"

# 输出
结果
```

### 示例 2: 高级功能

```bash
# 命令
python3 scripts/main.py "参数" --option

# 输出
结果
```

---

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 成功率 | 95%+ | 测试环境 |
| 速度 | <5 秒 | 平均响应 |
| 并发 | 10 次/秒 | 最大并发 |

---

## ⚠️ 注意事项

1. **注意事项 1** - 说明
2. **注意事项 2** - 说明
3. **注意事项 3** - 说明

---

## 🔧 故障排查

### 问题 1: 问题描述

```bash
# 解决方案
解决命令
```

### 问题 2: 问题描述

```bash
# 解决方案
解决命令
```

---

## 📝 更新日志

### v1.0.0 (2026-03-22)

```
✅ 初始版本
✅ 核心功能
✅ 测试通过
```

---

**创建时间**: 2026-03-22  
**版本**: 1.0.0  
**状态**: 🚀 ready to use
```

---

## 🔧 核心组件库

### 组件 1: Fetcher（内容抓取）

```python
# scripts/fetcher.py
import requests
from typing import Dict, Optional

class Fetcher:
    """通用内容抓取器"""
    
    @staticmethod
    def fetch(url: str, method: str = "auto") -> Dict:
        """
        抓取内容
        
        Args:
            url: 目标 URL
            method: 抓取方法 (auto/jina/playwright)
        
        Returns:
            {
                "title": str,
                "markdown": str,
                "html": str,
                "source_url": str
            }
        """
        if method == "auto":
            # 自动选择最优方案
            return Fetcher._fetch_auto(url)
        elif method == "jina":
            return Fetcher._fetch_jina(url)
        elif method == "playwright":
            return Fetcher._fetch_playwright(url)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def _fetch_auto(url: str) -> Dict:
        """自动选择最优抓取方案"""
        # 优先级：jina > playwright
        try:
            return Fetcher._fetch_jina(url)
        except:
            return Fetcher._fetch_playwright(url)
    
    @staticmethod
    def _fetch_jina(url: str) -> Dict:
        """使用 Jina AI 抓取"""
        response = requests.get(f"https://r.jina.ai/{url}", timeout=30)
        response.raise_for_status()
        return {
            "title": "",  # Jina 不返回标题
            "markdown": response.text,
            "html": "",
            "source_url": url
        }
    
    @staticmethod
    def _fetch_playwright(url: str) -> Dict:
        """使用 Playwright 抓取（需要安装）"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            
            title = page.title()
            html = page.content()
            markdown = Fetcher._html_to_markdown(html)
            
            browser.close()
            
            return {
                "title": title,
                "markdown": markdown,
                "html": html,
                "source_url": url
            }
    
    @staticmethod
    def _html_to_markdown(html: str) -> str:
        """HTML 转 Markdown"""
        import html2text
        h = html2text.HTML2Text()
        return h.handle(html)
```

---

### 组件 2: Parser（内容解析）

```python
# scripts/parser.py
import re
from typing import Dict, List

class Parser:
    """通用内容解析器"""
    
    @staticmethod
    def parse(raw: Dict, format: str = "markdown") -> Dict:
        """
        解析内容
        
        Args:
            raw: 原始内容
            format: 输出格式 (markdown/html/json)
        
        Returns:
            {
                "title": str,
                "content": str,
                "metadata": Dict,
                "images": List[str]
            }
        """
        return {
            "title": raw.get("title", ""),
            "content": raw.get("markdown", raw.get("content", "")),
            "metadata": Parser._extract_metadata(raw),
            "images": Parser._extract_images(raw)
        }
    
    @staticmethod
    def _extract_metadata(raw: Dict) -> Dict:
        """提取元数据"""
        return {
            "source_url": raw.get("source_url", ""),
            "fetch_time": "",  # 当前时间
            "word_count": len(raw.get("markdown", ""))
        }
    
    @staticmethod
    def _extract_images(raw: Dict) -> List[str]:
        """提取图片 URL"""
        html = raw.get("html", "")
        markdown = raw.get("markdown", "")
        
        images = []
        
        # 从 HTML 提取
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        images.extend(re.findall(img_pattern, html))
        
        # 从 Markdown 提取
        md_pattern = r'!\[.*?\]\(([^)]+)\)'
        images.extend(re.findall(md_pattern, markdown))
        
        return list(set(images))  # 去重
```

---

### 组件 3: Classifier（智能分类）

```python
# scripts/classifier.py
from typing import Dict, List

class Classifier:
    """智能内容分类器"""
    
    # 8 大分类定义
    CATEGORIES = {
        "📖 技术教程": ["安装", "配置", "部署", "教程", "指南", "教学"],
        "🛠️ 实战案例": ["案例", "实战", "项目", "演示", "实践"],
        "📄 产品文档": ["安全", "公告", "版本", "功能", "更新"],
        "💡 学习笔记": ["学习", "成长", "笔记", "心得", "感悟"],
        "🔥 热点资讯": ["发布", "新功能", "热点", "新闻", "动态"],
        "🎨 设计技能": ["设计", "Prompt", "美学", "UI", "UX"],
        "🔧 工具推荐": ["工具", "CLI", "插件", "推荐", "软件"],
        "🎓 训练营": ["训练营", "课程", "教学", "培训", "学习"]
    }
    
    @staticmethod
    def classify(content: str, title: str = "") -> str:
        """
        智能分类
        
        Args:
            content: 内容文本
            title: 标题
        
        Returns:
            分类名称（含 Emoji）
        """
        # 合并标题和内容
        text = f"{title} {content}".lower()
        
        # 计算每个分类的匹配度
        scores = {}
        for category, keywords in Classifier.CATEGORIES.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score
        
        # 返回最高分的分类
        best_category = max(scores, key=scores.get)
        
        # 如果所有分类都得 0 分，返回"待分类"
        if scores[best_category] == 0:
            return "待分类"
        
        return best_category
```

---

### 组件 4: Uploader（文件上传）

```python
# scripts/uploader.py
import os
from typing import Dict, List

class Uploader:
    """通用文件上传器"""
    
    @staticmethod
    def upload_to_feishu(file_path: str, folder_id: str) -> str:
        """
        上传文件到飞书
        
        Args:
            file_path: 文件路径
            folder_id: 飞书文件夹 ID
        
        Returns:
            飞书文件 URL
        """
        # 这里需要飞书 API 集成
        # 示例代码：
        # token = get_feishu_token()
        # response = upload_file(token, file_path, folder_id)
        # return response["url"]
        pass
    
    @staticmethod
    def upload_images(images: List[str], target: str = "feishu") -> Dict[str, str]:
        """
        批量上传图片
        
        Args:
            images: 图片 URL 列表
            target: 上传目标 (feishu/local)
        
        Returns:
            {原 URL: 新 URL}
        """
        result = {}
        for img_url in images:
            # 下载图片
            local_path = Uploader._download_image(img_url)
            
            # 上传到目标
            if target == "feishu":
                new_url = Uploader.upload_to_feishu(local_path, "")
            else:
                new_url = local_path
            
            result[img_url] = new_url
        
        return result
    
    @staticmethod
    def _download_image(url: str) -> str:
        """下载图片到本地临时文件"""
        import requests
        import tempfile
        
        response = requests.get(url)
        response.raise_for_status()
        
        # 创建临时文件
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(response.content)
        tmp.close()
        
        return tmp.name
```

---

### 组件 5: Indexer（索引更新）

```python
# scripts/indexer.py
from typing import Dict

class Indexer:
    """索引更新器"""
    
    @staticmethod
    def update_bitable(app_token: str, table_id: str, fields: Dict) -> str:
        """
        更新飞书多维表格
        
        Args:
            app_token: 飞书应用 Token
            table_id: 表格 ID
            fields: 字段数据
        
        Returns:
            记录 ID
        """
        # 这里需要飞书 Bitable API 集成
        # 示例代码：
        # record_id = create_record(app_token, table_id, fields)
        # return record_id
        pass
    
    @staticmethod
    def update_index_doc(doc_id: str, category: str, title: str, url: str):
        """
        更新索引文档
        
        Args:
            doc_id: 索引文档 ID
            category: 分类
            title: 标题
            url: 文档 URL
        """
        # 这里需要飞书 Doc API 集成
        # 示例代码：
        # append_to_doc(doc_id, f"| {title} | {category} | {url} |")
        pass
```

---

## 🧪 测试框架

### 单元测试模板

```python
# tests/test_main.py
import unittest
from scripts.main import main_function

class TestMainFunction(unittest.TestCase):
    
    def test_success_case(self):
        """测试成功情况"""
        result = main_function("valid_input")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "success")
    
    def test_failure_case(self):
        """测试失败情况"""
        result = main_function("invalid_input")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "error")
    
    def test_edge_case(self):
        """测试边界情况"""
        result = main_function("")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
```

---

### 集成测试模板

```python
# tests/test_integration.py
import unittest
from scripts.main import full_workflow

class TestFullWorkflow(unittest.TestCase):
    
    def test_full_workflow(self):
        """测试完整工作流"""
        url = "https://mp.weixin.qq.com/s/xxx"
        result = full_workflow(url)
        
        # 验证所有步骤都完成
        self.assertIsNotNone(result["doc_url"])
        self.assertIsNotNone(result["category"])
        self.assertIsNotNone(result["record_id"])

if __name__ == "__main__":
    unittest.main()
```

---

## 📋 配置管理规范

### 默认配置文件

```yaml
# config/default.yaml
# 默认配置

# 飞书配置
feishu:
  app_token: ""
  table_id: ""
  space_id: ""

# 图片配置
image:
  max_count: 20
  max_size_mb: 10
  timeout_sec: 20
  allowed_types: ["jpg", "png", "gif", "webp"]

# 抓取配置
fetch:
  timeout_sec: 30
  retry_count: 3
  method: "auto"  # auto/jina/playwright
```

---

### 环境变量配置

```bash
# .env 文件
# 环境变量配置

# 飞书 API
FEISHU_APP_TOKEN=""
FEISHU_TABLE_ID=""
FEISHU_SPACE_ID=""

# 其他 API
API_KEY=""
```

---

## 🚀 快速开始新技能开发

### Step 1: 复制模板

```bash
# 复制技能模板
cp -r /opt/openclaw/skills/template ~/.openclaw/workspace/skills/my-new-skill
cd ~/.openclaw/workspace/skills/my-new-skill
```

### Step 2: 修改 SKILL.md

```bash
# 编辑 SKILL.md
vim SKILL.md
# 修改 name, description, keywords, triggers
```

### Step 3: 实现主逻辑

```bash
# 编辑主逻辑
vim scripts/main.py
# 使用组件库快速实现
```

### Step 4: 编写测试

```bash
# 编写测试
vim tests/test_main.py
# 运行测试
python3 -m pytest tests/
```

### Step 5: 测试验证

```bash
# 本地测试
python3 scripts/main.py "测试参数"

# 验证功能
# 确认所有功能正常
```

---

## 📊 技能开发检查清单

### 开发前

- [ ] 明确技能功能
- [ ] 确定触发词
- [ ] 准备测试数据

### 开发中

- [ ] 编写 SKILL.md
- [ ] 实现主逻辑
- [ ] 使用组件库
- [ ] 编写测试

### 开发后

- [ ] 运行测试
- [ ] 本地验证
- [ ] 编写 README
- [ ] 提交代码

---

**创建时间**: 2026-03-22  
**版本**: 1.0.0  
**状态**: 🚀 ready to use
