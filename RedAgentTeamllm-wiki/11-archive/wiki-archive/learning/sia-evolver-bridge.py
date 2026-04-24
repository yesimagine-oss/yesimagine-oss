#!/usr/bin/env python3
"""
双重进化引擎桥接脚本
连接 Self-Improving Agent 和 Capability Evolver
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

class DualEvolutionBridge:
    """双重进化引擎桥接器"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.expanduser()
        self.learnings_dir = self.workspace / ".learnings"
        self.sia_dir = self.learnings_dir / "sia"
        self.evolver_dir = self.learnings_dir / "evolver"
        
        # 确保目录存在
        self.sia_dir.mkdir(parents=True, exist_ok=True)
        (self.evolver_dir / "synced").mkdir(parents=True, exist_ok=True)
    
    def sync_sia_to_evolver(self):
        """同步 SIA 记录到 Evolver"""
        print("🔄 同步 SIA 记录到 Evolver...")
        
        synced_count = 0
        
        # 遍历 SIA 文件
        for sia_file in ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]:
            sia_path = self.sia_dir / sia_file
            
            if not sia_path.exists():
                continue
            
            # 读取 SIA 内容
            with open(sia_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析条目
            entries = self._parse_markdown_entries(content)
            
            # 同步每个条目
            for entry in entries:
                if self._should_sync(entry):
                    self._sync_entry(entry, sia_file)
                    synced_count += 1
        
        print(f"✅ 已同步 {synced_count} 条记录")
        return synced_count
    
    def _parse_markdown_entries(self, content: str) -> list:
        """解析 Markdown 条目"""
        entries = []
        current_entry = {}
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {
                    'title': line[3:].strip(),
                    'content': line + '\n'
                }
            elif current_entry:
                current_entry['content'] += line + '\n'
        
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def _should_sync(self, entry: dict) -> bool:
        """判断是否需要同步"""
        entry_id = entry.get('title', '').replace(' ', '_')[:50]
        sync_marker = self.evolver_dir / "synced" / f"{entry_id}.marker"
        return not sync_marker.exists()
    
    def _sync_entry(self, entry: dict, source_file: str):
        """同步单个条目"""
        entry_id = entry.get('title', '').replace(' ', '_')[:50]
        
        record = {
            'id': entry_id,
            'timestamp': datetime.now().isoformat(),
            'source': 'sia',
            'source_file': source_file,
            'text': entry.get('content', ''),
            'type': self._detect_type(source_file),
            'category': 'pending_analysis'
        }
        
        raw_dir = self.evolver_dir / "raw" / "auto-learnings"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = raw_dir / f"sia_{entry_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        synced_dir = self.evolver_dir / "synced"
        marker_path = synced_dir / f"{entry_id}.marker"
        with open(marker_path, 'w', encoding='utf-8') as f:
            f.write(f"Synced at {datetime.now().isoformat()}")
    
    def _detect_type(self, source_file: str) -> str:
        """检测记录类型"""
        type_map = {
            "LEARNINGS.md": "learning",
            "ERRORS.md": "error",
            "FEATURE_REQUESTS.md": "feature"
        }
        return type_map.get(source_file, "general")
    
    def trigger_evolution(self):
        """触发进化处理"""
        print("🧬 触发进化处理...")
        evolver_script = self.learnings_dir.parent / "evolver.py"
        
        if evolver_script.exists():
            os.system(f"python3 {evolver_script} --daily")
        else:
            print("⚠️ Evolver 脚本不存在")
    
    def run_full_cycle(self):
        """执行完整进化周期"""
        print("🧬 双重进化引擎 - 完整周期")
        print("=" * 60)
        
        print("\n📝 步骤 1: 同步 SIA 记录...")
        self.sync_sia_to_evolver()
        
        print("\n🧠 步骤 2: 触发进化处理...")
        self.trigger_evolution()
        
        print("\n" + "=" * 60)
        print("✅ 完整进化周期完成")


if __name__ == "__main__":
    bridge = DualEvolutionBridge()
    bridge.run_full_cycle()
