#!/usr/bin/env python3
"""
ClawBrowser - OpenClaw 無頭瀏覽器自動化工具

基於 agent-browser 的 Python 集成層
支持 CDP 協議、ARIA 快照、自然語言交互
"""

import subprocess
import shlex
import json
from pathlib import Path
from typing import Optional, List


class ClawBrowser:
    """ClawBrowser 瀏覽器自動化工具類"""
    
    def __init__(self, session_name: str = "default", cdp_port: int = 18800):
        """
        初始化 ClawBrowser
        
        Args:
            session_name: 會話名稱
            cdp_port: CDP 端口
        """
        self.session_name = session_name
        self.cdp_port = cdp_port
        self.session_active = False
    
    def _run_command(self, command: str, check: bool = True) -> subprocess.CompletedProcess:
        """
        執行 agent-browser 命令
        
        Args:
            command: 命令字符串
            check: 是否檢查錯誤
            
        Returns:
            執行結果
        """
        full_command = f"agent-browser {command}"
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ 命令執行失敗：{e}")
            raise
    
    def open(self, url: str) -> bool:
        """
        打開網頁
        
        Args:
            url: 網址
            
        Returns:
            是否成功
        """
        result = self._run_command(f"open {url} --cdp-port {self.cdp_port}")
        self.session_active = True
        return result.returncode == 0
    
    def snapshot(self, interactive: bool = True, refs: str = "aria") -> str:
        """
        獲取頁面快照
        
        Args:
            interactive: 交互式輸出
            refs: 引用類型 (aria/role)
            
        Returns:
            快照內容
        """
        flags = "-i" if interactive else ""
        result = self._run_command(f"snapshot {flags} --refs {refs} --cdp-port {self.cdp_port}")
        return result.stdout
    
    def click(self, ref: str) -> bool:
        """
        點擊元素
        
        Args:
            ref: 元素引用 (如 @e1)
            
        Returns:
            是否成功
        """
        result = self._run_command(f"click {ref} --cdp-port {self.cdp_port}")
        return result.returncode == 0
    
    def fill(self, ref: str, text: str) -> bool:
        """
        填寫輸入框
        
        Args:
            ref: 元素引用
            text: 填寫內容
            
        Returns:
            是否成功
        """
        result = self._run_command(f"fill {ref} {shlex.quote(text)} --cdp-port {self.cdp_port}")
        return result.returncode == 0
    
    def screenshot(self, output_path: str) -> bool:
        """
        截圖
        
        Args:
            output_path: 輸出路徑
            
        Returns:
            是否成功
        """
        result = self._run_command(f"screenshot {output_path} --cdp-port {self.cdp_port}")
        return result.returncode == 0
    
    def wait(self, load_state: str = "networkidle", timeout: int = 30000) -> bool:
        """
        等待條件
        
        Args:
            load_state: 加載狀態 (networkidle/domcontentloaded)
            timeout: 超時時間 (ms)
            
        Returns:
            是否成功
        """
        result = self._run_command(
            f"wait --load {load_state} --timeout {timeout} --cdp-port {self.cdp_port}"
        )
        return result.returncode == 0
    
    def extract(self, selector: str) -> List[str]:
        """
        提取內容
        
        Args:
            selector: CSS 選擇器
            
        Returns:
            提取的內容列表
        """
        result = self._run_command(f"extract {shlex.quote(selector)} --cdp-port {self.cdp_port}")
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
        return []
    
    def close(self) -> bool:
        """
        關閉頁面
        
        Returns:
            是否成功
        """
        result = self._run_command(f"close --cdp-port {self.cdp_port}")
        self.session_active = False
        return result.returncode == 0
    
    def natural_language_command(self, command: str) -> str:
        """
        自然語言指令
        
        Args:
            command: 自然語言指令 (如 "打開 github.com")
            
        Returns:
            執行結果
        """
        # 簡單的指令解析
        command = command.lower().strip()
        
        if command.startswith("打開") or command.startswith("open"):
            url = command.replace("打開", "").replace("open", "").strip()
            if not url.startswith("http"):
                url = f"https://{url}"
            success = self.open(url)
            return f"✅ 已打開 {url}" if success else f"❌ 打開失敗 {url}"
        
        elif command.startswith("點擊") or command.startswith("click"):
            ref = command.replace("點擊", "").replace("click", "").strip()
            success = self.click(ref)
            return f"✅ 已點擊 {ref}" if success else f"❌ 點擊失敗 {ref}"
        
        elif command.startswith("填寫") or command.startswith("fill"):
            # 解析：填寫 @e1 "text"
            parts = command.replace("填寫", "").replace("fill", "").strip().split('"')
            if len(parts) >= 2:
                ref = parts[0].strip()
                text = parts[1]
                success = self.fill(ref, text)
                return f"✅ 已填寫 {ref}" if success else f"❌ 填寫失敗 {ref}"
        
        elif command.startswith("截圖") or command.startswith("screenshot"):
            filename = command.replace("截圖", "").replace("screenshot", "").strip() or "screenshot.png"
            success = self.screenshot(filename)
            return f"✅ 已截圖 {filename}" if success else f"❌ 截圖失敗"
        
        elif command.startswith("快照") or command.startswith("snapshot"):
            snapshot = self.snapshot()
            return snapshot
        
        return f"⚠️ 未知指令：{command}"


# 便捷函數
def open_browser(url: str, session: str = "default") -> ClawBrowser:
    """快速打開瀏覽器"""
    browser = ClawBrowser(session_name=session)
    browser.open(url)
    return browser


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 browser_tool.py <command> [args]")
        print("命令：open, snapshot, click, fill, screenshot, wait, extract, close")
        sys.exit(1)
    
    browser = ClawBrowser()
    command = sys.argv[1]
    
    if command == "open" and len(sys.argv) > 2:
        browser.open(sys.argv[2])
        print(f"✅ 已打開 {sys.argv[2]}")
    
    elif command == "snapshot":
        print(browser.snapshot())
    
    elif command == "screenshot" and len(sys.argv) > 2:
        browser.screenshot(sys.argv[2])
        print(f"✅ 已截圖 {sys.argv[2]}")
    
    elif command == "close":
        browser.close()
        print("✅ 已關閉")
    
    else:
        print(f"⚠️ 未知命令：{command}")
