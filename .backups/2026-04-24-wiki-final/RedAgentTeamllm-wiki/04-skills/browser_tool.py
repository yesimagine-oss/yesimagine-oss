#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Browser Tool - Agent Browser 集成
使用 agent-browser CLI 實現瀏覽器自動化，支持自然語言指令、ARIA ref 定位、網頁抓取

核心設計原則：
1. 完全無頭模式 - 只保留 DOM 渲染 + 無障礙樹快照
2. ref-based 元素定位 - 使用 ARIA ref (@e1, @e2) 替代 CSS 選擇器
3. 自然語言指令 - 直接接收 AI 的自然語言操作指令

使用示例：
```python
from browser_tool import BrowserTool

browser = BrowserTool()

# 導航 + 快照
browser.open("https://example.com")
snapshot = browser.snapshot()

# 使用 ref 交互
browser.click("@e2")
browser.fill("@e3", "test@example.com")

# 網頁抓取
content = browser.extract_content()
browser.save_to_feishu(content, "頁面標題")
```
"""

import subprocess
import json
import os
import tempfile
from typing import Optional, Dict, Any, List
from datetime import datetime


class BrowserTool:
    """Agent Browser 集成工具類"""
    
    def __init__(self, session_name: str = "default", headed: bool = False):
        """
        初始化瀏覽器工具
        
        Args:
            session_name: 會話名稱（隔離不同任務）
            headed: 是否顯示瀏覽器窗口（調試用）
        """
        self.session_name = session_name
        self.headed = headed
        self.current_snapshot = None
        self.current_refs = {}
        # 使用工作区编译的 agent-browser（如果存在），否则使用系统版本
        self.browser_cli = "/home/admin/.openclaw/workspace/agent-browser-study/agent-browser/bin/agent-browser-linux-x64"
        if not os.path.exists(self.browser_cli):
            self.browser_cli = "agent-browser"  # 回退到系统版本
        # 使用 auto-connect 自动发现 OpenClaw 自有的 Chromium 实例
        self.auto_connect = False  # 暂时禁用，让 agent-browser 自己启动浏览器
        
    def _run_command(self, cmd: List[str], json_mode: bool = True) -> Dict[str, Any]:
        """執行 agent-browser 命令"""
        base_cmd = [self.browser_cli]
        
        # 使用 auto-connect 自动发现 OpenClaw 自有的 Chromium 实例
        if self.auto_connect:
            base_cmd.append("--auto-connect")
        
        # 添加會話參數
        if self.session_name:
            base_cmd.extend(["--session", self.session_name])
        
        # 添加 headed 模式
        if self.headed:
            base_cmd.append("--headed")
        
        # 添加 json 模式
        if json_mode:
            base_cmd.append("--json")
        
        # 執行命令
        full_cmd = base_cmd + cmd
        try:
            result = subprocess.run(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            if json_mode:
                try:
                    return json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": f"Failed to parse JSON: {result.stdout}",
                        "stderr": result.stderr
                    }
            else:
                return {
                    "success": result.returncode == 0,
                    "data": result.stdout,
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timeout after 60s: {' '.join(cmd)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def open(self, url: str, wait_load: bool = True) -> Dict[str, Any]:
        """
        打開網頁
        
        Args:
            url: 網址
            wait_load: 是否等待頁面加載完成
            
        Returns:
            執行結果
        """
        # 自動添加 https:// 如果沒有協議
        if not url.startswith(("http://", "https://", "file://", "chrome://")):
            url = f"https://{url}"
        
        result = self._run_command(["open", url])
        
        if result.get("success") and wait_load:
            # 等待網絡空閒
            self._run_command(["wait", "--load", "networkidle"])
        
        return result
    
    def snapshot(self, interactive: bool = True, compact: bool = True) -> Dict[str, Any]:
        """
        獲取無障礙樹快照（包含 refs）
        
        Args:
            interactive: 只獲取可交互元素
            compact: 緊湊模式（移除空元素）
            
        Returns:
            快照數據（包含 refs）
        """
        cmd = ["snapshot"]
        
        if interactive:
            cmd.append("-i")
        if compact:
            cmd.append("-c")
        
        result = self._run_command(cmd)
        
        if result.get("success") and "data" in result:
            self.current_snapshot = result["data"]
            # 解析 refs
            if "refs" in result["data"]:
                self.current_refs = result["data"]["refs"]
        
        return result
    
    def click(self, selector: str, new_tab: bool = False) -> Dict[str, Any]:
        """
        點擊元素
        
        Args:
            selector: 元素選擇器（@e1 或 CSS）
            new_tab: 是否在新標籤頁打開
            
        Returns:
            執行結果
        """
        cmd = ["click", selector]
        if new_tab:
            cmd.append("--new-tab")
        
        result = self._run_command(cmd)
        
        # 點擊後可能需要重新快照
        if result.get("success"):
            self.current_snapshot = None  # 標記快照已失效
        
        return result
    
    def fill(self, selector: str, text: str) -> Dict[str, Any]:
        """
        填寫輸入框
        
        Args:
            selector: 元素選擇器
            text: 要填寫的文本
            
        Returns:
            執行結果
        """
        return self._run_command(["fill", selector, text])
    
    def type(self, selector: str, text: str) -> Dict[str, Any]:
        """
        輸入文本（不清空原有內容）
        
        Args:
            selector: 元素選擇器
            text: 要輸入的文本
            
        Returns:
            執行結果
        """
        return self._run_command(["type", selector, text])
    
    def get_text(self, selector: str) -> Dict[str, Any]:
        """
        獲取元素文本
        
        Args:
            selector: 元素選擇器
            
        Returns:
            執行結果（包含 text 字段）
        """
        return self._run_command(["get", "text", selector])
    
    def get_url(self) -> Dict[str, Any]:
        """獲取當前 URL"""
        return self._run_command(["get", "url"])
    
    def get_title(self) -> Dict[str, Any]:
        """獲取頁面標題"""
        return self._run_command(["get", "title"])
    
    def wait(self, selector: Optional[str] = None, timeout: Optional[int] = None, 
             text: Optional[str] = None, load_state: Optional[str] = None) -> Dict[str, Any]:
        """
        等待
        
        Args:
            selector: 等待元素出現
            timeout: 等待毫秒數
            text: 等待文本出現
            load_state: 等待加載狀態（load/domcontentloaded/networkidle）
            
        Returns:
            執行結果
        """
        cmd = ["wait"]
        
        if selector:
            cmd.append(selector)
        elif timeout:
            cmd.append(str(timeout))
        elif text:
            cmd.extend(["--text", text])
        elif load_state:
            cmd.extend(["--load", load_state])
        
        return self._run_command(cmd)
    
    def screenshot(self, path: Optional[str] = None, full_page: bool = False, 
                   annotate: bool = False) -> Dict[str, Any]:
        """
        截圖
        
        Args:
            path: 保存路徑（可選，默認臨時目錄）
            full_page: 是否完整頁面
            annotate: 是否標註元素（vision mode）
            
        Returns:
            執行結果（包含 screenshot_path）
        """
        cmd = ["screenshot"]
        
        if path:
            cmd.append(path)
        if full_page:
            cmd.append("--full")
        if annotate:
            cmd.append("--annotate")
        
        return self._run_command(cmd)
    
    def extract_content(self, selector: Optional[str] = None) -> str:
        """
        提取頁面內容（網頁抓取核心功能）
        
        Args:
            selector: 可選，只提取特定區域
            
        Returns:
            頁面文本內容
        """
        if selector:
            result = self.get_text(selector)
        else:
            result = self.get_text("body")
        
        if result.get("success"):
            return result.get("data", "")
        return ""
    
    def extract_links(self) -> List[Dict[str, str]]:
        """
        提取頁面所有鏈接
        
        Returns:
            鏈接列表 [{"text": "...", "href": "..."}, ...]
        """
        js_code = """
        Array.from(document.querySelectorAll('a[href]')).map(a => ({
            text: a.textContent.trim().substring(0, 100),
            href: a.href
        })).filter(link => link.text && link.href)
        """
        
        result = self._run_command(["eval", js_code])
        
        if result.get("success") and "data" in result:
            try:
                return json.loads(result["data"])
            except:
                return []
        return []
    
    def extract_images(self) -> List[Dict[str, str]]:
        """
        提取頁面所有圖片
        
        Returns:
            圖片列表 [{"src": "...", "alt": "..."}, ...]
        """
        js_code = """
        Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src,
            alt: img.alt || '',
            width: img.naturalWidth,
            height: img.naturalHeight
        })).filter(img => img.src)
        """
        
        result = self._run_command(["eval", js_code])
        
        if result.get("success") and "data" in result:
            try:
                return json.loads(result["data"])
            except:
                return []
        return []
    
    def save_to_feishu(self, content: str, title: str, doc_token: Optional[str] = None) -> Dict[str, Any]:
        """
        保存抓取的內容到飛書文檔
        
        Args:
            content: 內容
            title: 文檔標題
            doc_token: 可選，現有文檔 token
            
        Returns:
            執行結果
        """
        # 使用 feishu_doc 工具
        from feishu_doc import feishu_doc
        
        if doc_token:
            # 更新現有文檔
            return feishu_doc(action="write", doc_token=doc_token, content=content)
        else:
            # 創建新文檔
            return feishu_doc(action="create", title=title, content=content)
    
    def close(self) -> Dict[str, Any]:
        """關閉瀏覽器會話"""
        result = self._run_command(["close"])
        self.current_snapshot = None
        self.current_refs = {}
        return result
    
    def natural_language_command(self, instruction: str) -> Dict[str, Any]:
        """
        自然語言指令執行（AI 友好接口）
        
        Args:
            instruction: 自然語言指令，如：
                - "打開 example.com"
                - "點擊提交按鈕"
                - "填寫郵箱為 test@example.com"
                - "抓取頁面內容"
                - "截圖保存為 page.png"
            
        Returns:
            執行結果
        """
        # 簡單的指令解析（實際應該用 LLM）
        instruction = instruction.lower().strip()
        
        if instruction.startswith("打開") or instruction.startswith("open"):
            url = instruction.replace("打開", "").replace("open", "").strip()
            return self.open(url)
        
        elif instruction.startswith("點擊") or instruction.startswith("click"):
            # 從快照中查找匹配的元素
            selector = self._find_ref_by_text(instruction.replace("點擊", "").replace("click", "").strip())
            if selector:
                return self.click(selector)
            return {"success": False, "error": "未找到匹配的元素"}
        
        elif instruction.startswith("填寫") or instruction.startswith("fill"):
            # 解析：填寫 [元素] 為 [內容]
            parts = instruction.replace("填寫", "").replace("fill", "").split("為")
            if len(parts) == 2:
                element = parts[0].strip()
                text = parts[1].strip()
                selector = self._find_ref_by_text(element)
                if selector:
                    return self.fill(selector, text)
            return {"success": False, "error": "指令格式錯誤"}
        
        elif instruction.startswith("抓取") or instruction.startswith("extract"):
            content = self.extract_content()
            return {"success": True, "data": {"content": content}}
        
        elif instruction.startswith("截圖") or instruction.startswith("screenshot"):
            parts = instruction.replace("截圖", "").replace("screenshot", "").split("保存為")
            path = parts[1].strip() if len(parts) > 1 else None
            return self.screenshot(path=path)
        
        else:
            return {"success": False, "error": f"無法解析的指令：{instruction}"}
    
    def _find_ref_by_text(self, text: str) -> Optional[str]:
        """根據文本查找 ref"""
        if not self.current_refs:
            return None
        
        for ref_id, ref_data in self.current_refs.items():
            name = ref_data.get("name", "").lower()
            role = ref_data.get("role", "").lower()
            
            if text in name or text in role:
                return f"@{ref_id}"
        
        return None


# 命令行接口
if __name__ == "__main__":
    import sys
    
    browser = BrowserTool(session_name="cli")
    
    if len(sys.argv) < 2:
        print("使用方式：python3 browser_tool.py <指令> [參數]")
        print("示例:")
        print("  python3 browser_tool.py open https://example.com")
        print("  python3 browser_tool.py snapshot")
        print("  python3 browser_tool.py click @e1")
        print("  python3 browser_tool.py extract")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "open" and len(sys.argv) > 2:
        result = browser.open(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "snapshot":
        result = browser.snapshot()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "click" and len(sys.argv) > 2:
        result = browser.click(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "extract":
        content = browser.extract_content()
        print(f"提取內容 ({len(content)} 字符):")
        print(content[:500])
    
    elif command == "close":
        result = browser.close()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)

# ============================================================
# 作者：RedOpenClaw
# 完成日期：2026.04.02
# 說明：ClawBrowser 瀏覽器自動化工具
# ============================================================
