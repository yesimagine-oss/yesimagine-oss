# 🧬 双重进化引擎整合方案

**版本:** v1.0  
**创建时间:** 2026-03-15 15:03  
**整合:** Self-Improving Agent + Capability Evolver

---

## 🎯 整合目标

将 **Self-Improving Agent** (微观即时改进) 与 **Capability Evolver** (宏观持续进化) 完美整合，形成协同进化的双重引擎。

---

## 📊 双重引擎架构

```
┌─────────────────────────────────────────────────────────┐
│                  双重进化引擎                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  第一重：Self-Improving Agent                           │
│  ─────────────────────────────                          │
│  • 即时记录 (会话中)                                     │
│  • 手动触发 (用户纠正/任务失败)                           │
│  • 微观改进 (具体任务)                                   │
│  • 快速反馈 (立即生效)                                   │
│                                                         │
│  ↓ 数据流                                                │
│                                                         │
│  第二重：Capability Evolver                             │
│  ─────────────────────────────                          │
│  • 自动分析 (后台处理)                                   │
│  • 智能分类 (AI 驱动)                                    │
│  • 宏观进化 (能力体系)                                   │
│  • 持续优化 (每日处理)                                   │
│                                                         │
│  ↓ 晋升流                                                │
│                                                         │
│  核心文档：SOUL.md / AGENTS.md / TOOLS.md / MEMORY.md   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 整合配置

### 1. 统一目录结构

```
~/.openclaw/workspace/
├── .learnings/                       # 统一学习目录
│   ├── sia/                          # Self-Improving Agent
│   │   ├── LEARNINGS.md              # 即时学习记录
│   │   ├── ERRORS.md                 # 即时错误记录
│   │   └── FEATURE_REQUESTS.md       # 功能请求
│   ├── evolver/                      # Capability Evolver
│   │   ├── raw/                      # 原始记录
│   │   ├── processed/                # 处理结果
│   │   └── reports/                  # 进化报告
│   └── config/                       # 统一配置
│       ├── evolution-rules.yaml      # 进化规则
│       └── promotion-rules.yaml      # 晋升规则
├── SOUL.md                           # 行为准则 (晋升目标)
├── AGENTS.md                         # 工作流程 (晋升目标)
├── TOOLS.md                          # 工具技巧 (晋升目标)
└── MEMORY.md                         # 长期记忆 (晋升目标)
```

### 2. 数据流整合

```yaml
# 即时记录流 (Self-Improving Agent)
用户交互
    ↓
检测触发事件
    ↓
记录到 .learnings/sia/
    ↓
会话中立即应用

# 自动进化流 (Capability Evolver)
.learnings/sia/ 数据
    ↓
每日自动同步到 .learnings/evolver/
    ↓
智能分析 + 分类
    ↓
评估晋升条件
    ↓
晋升到核心文档
```

---

## ⚙️ 整合脚本

### sia-evolver-bridge.py

```python
#!/usr/bin/env python3
"""
双重进化引擎桥接脚本

功能:
- 同步 SIA 记录到 Evolver
- 触发自动进化处理
- 应用进化结果
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

class DualEvolutionBridge:
    """双重进化引擎桥接器"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.expanduser()
        self.learnings_dir = self.workspace / ".learnings"
        self.sia_dir = self.learnings_dir / "sia"
        self.evolver_dir = self.learnings_dir / "evolver"
        
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
            
            # 解析条目 (简单实现：按 ## 分割)
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
        # 检查是否已同步
        entry_id = entry.get('title', '')
        sync_marker = self.evolver_dir / "synced" / f"{entry_id}.marker"
        
        return not sync_marker.exists()
    
    def _sync_entry(self, entry: dict, source_file: str):
        """同步单个条目"""
        # 创建 Evolver 记录
        record = {
            'id': entry.get('title', ''),
            'timestamp': datetime.now().isoformat(),
            'source': 'sia',
            'source_file': source_file,
            'text': entry.get('content', ''),
            'type': self._detect_type(source_file),
            'category': 'pending_analysis'
        }
        
        # 保存到 Evolver raw 目录
        raw_dir = self.evolver_dir / "raw" / "auto-learnings"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = raw_dir / f"sia_{record['id']}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        # 创建同步标记
        synced_dir = self.evolver_dir / "synced"
        synced_dir.mkdir(parents=True, exist_ok=True)
        
        marker_path = synced_dir / f"{record['id']}.marker"
        with open(marker_path, 'w', encoding='utf-8') as f:
            f.write(f"Synced at {datetime.now().isoformat()}")
    
    def _detect_type(self, source_file: str) -> str:
        """检测记录类型"""
        if source_file == "LEARNINGS.md":
            return "learning"
        elif source_file == "ERRORS.md":
            return "error"
        elif source_file == "FEATURE_REQUESTS.md":
            return "feature"
        return "general"
    
    def trigger_evolution(self):
        """触发进化处理"""
        print("🧬 触发进化处理...")
        
        # 调用 Evolver 每日处理
        evolver_script = self.evolver_dir.parent / "evolver.py"
        
        if evolver_script.exists():
            os.system(f"python3 {evolver_script} --daily")
        else:
            print("⚠️ Evolver 脚本不存在")
    
    def apply_evolution_results(self):
        """应用进化结果"""
        print("📈 应用进化结果...")
        
        promoted_dir = self.evolver_dir / "processed" / "promoted"
        
        if not promoted_dir.exists():
            print("  暂无晋升记录")
            return
        
        # 遍历晋升记录
        for promo_file in promoted_dir.glob("*.md"):
            self._apply_promotion(promo_file)
    
    def _apply_promotion(self, promo_file: Path):
        """应用单个晋升"""
        # 读取晋升内容
        with open(promo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析目标文件
        target = self._extract_target(content)
        
        if target:
            target_path = self.workspace / target
            
            if target_path.exists():
                # 追加到目标文件
                with open(target_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n---\n\n## 进化更新 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
                    f.write(content)
                
                print(f"  ✅ 已晋升到 {target}")
            else:
                print(f"  ⚠️ 目标文件不存在：{target}")
    
    def _extract_target(self, content: str) -> str:
        """提取晋升目标"""
        # 简单实现：从内容中提取目标文件名
        if "SOUL.md" in content:
            return "SOUL.md"
        elif "AGENTS.md" in content:
            return "AGENTS.md"
        elif "TOOLS.md" in content:
            return "TOOLS.md"
        elif "MEMORY.md" in content:
            return "MEMORY.md"
        return None
    
    def run_full_cycle(self):
        """执行完整进化周期"""
        print("🧬 双重进化引擎 - 完整周期")
        print("=" * 60)
        
        # 1. 同步 SIA 记录
        print("\n📝 步骤 1: 同步 SIA 记录...")
        self.sync_sia_to_evolver()
        
        # 2. 触发进化处理
        print("\n🧠 步骤 2: 触发进化处理...")
        self.trigger_evolution()
        
        # 3. 应用进化结果
        print("\n📈 步骤 3: 应用进化结果...")
        self.apply_evolution_results()
        
        print("\n" + "=" * 60)
        print("✅ 完整进化周期完成")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="双重进化引擎桥接器")
    parser.add_argument("--sync", action="store_true", help="同步 SIA 记录")
    parser.add_argument("--evolve", action="store_true", help="触发进化")
    parser.add_argument("--apply", action="store_true", help="应用结果")
    parser.add_argument("--full", action="store_true", help="完整周期")
    
    args = parser.parse_args()
    
    bridge = DualEvolutionBridge()
    
    if args.sync:
        bridge.sync_sia_to_evolver()
    elif args.evolve:
        bridge.trigger_evolution()
    elif args.apply:
        bridge.apply_evolution_results()
    elif args.full:
        bridge.run_full_cycle()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## 📋 整合步骤

### 步骤 1: 创建统一目录

```bash
# 创建 SIA 目录
mkdir -p ~/.openclaw/workspace/.learnings/sia

# 复制现有文件
cp ~/.openclaw/workspace/skills/self-improving-agent/.learnings/*.md \
   ~/.openclaw/workspace/.learnings/sia/

# 创建 Evolver 目录结构
mkdir -p ~/.openclaw/workspace/.learnings/evolver/{raw,processed,reports,config}
```

### 步骤 2: 配置桥接脚本

```bash
# 保存桥接脚本
cp sia-evolver-bridge.py ~/.openclaw/workspace/.learnings/

# 设置权限
chmod +x ~/.openclaw/workspace/.learnings/sia-evolver-bridge.py
```

### 步骤 3: 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加双重进化任务 (每日凌晨 2 点)
0 2 * * * cd ~/.openclaw/workspace/.learnings && python3 sia-evolver-bridge.py --full >> dual-evolution.log 2>&1
```

---

## 🔄 工作流程

### 即时改进流程 (SIA)

```
用户交互
    ↓
检测触发事件 (纠正/失败/请求)
    ↓
记录到 .learnings/sia/LEARNINGS.md
    ↓
会话中立即应用改进
```

### 持续进化流程 (Evolver)

```
每日凌晨 2 点
    ↓
桥接器同步 SIA 记录
    ↓
Evolver 分析分类
    ↓
评估晋升条件
    ↓
晋升到核心文档
    ↓
下次会话自动应用
```

---

## 📊 整合效果

### 对比单一引擎

| 维度 | 单一 SIA | 单一 Evolver | 双重引擎 |
|------|---------|-------------|---------|
| **响应速度** | ⭐⭐⭐⭐⭐ 即时 | ⭐⭐⭐ 延迟 | ⭐⭐⭐⭐⭐ 即时 + 持续 |
| **自动化** | ⭐⭐ 手动 | ⭐⭐⭐⭐⭐ 自动 | ⭐⭐⭐⭐⭐ 混合 |
| **智能分析** | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ AI 驱动 | ⭐⭐⭐⭐⭐ AI 驱动 |
| **知识晋升** | ⭐⭐⭐ 手动 | ⭐⭐⭐⭐ 自动 | ⭐⭐⭐⭐⭐ 自动 + 审核 |
| **适用范围** | ⭐⭐⭐ 微观 | ⭐⭐⭐⭐ 宏观 | ⭐⭐⭐⭐⭐ 全场景 |

### 协同效应

```
即时改进 (SIA) + 持续进化 (Evolver) = 能力飞轮

1. SIA 快速记录 → 大量数据积累
2. Evolver 智能分析 → 发现模式
3. 晋升到核心文档 → 知识固化
4. 下次会话应用 → 能力提升了
5. 产生新的学习 → 回到步骤 1

(循环持续，能力不断提升)
```

---

## 📈 预期效果

| 时间 | SIA 贡献 | Evolver 贡献 | 综合效果 |
|------|---------|-------------|---------|
| **第 1 周** | 即时记录 50+ 条 | 分析 50+ 条 | 初步知识积累 |
| **第 1 月** | 即时记录 200+ 条 | 晋升 20+ 条 | 错误率下降 30% |
| **第 3 月** | 即时记录 600+ 条 | 晋升 60+ 条 | 效率提升 50%+ |

---

## 🎯 成功标准

| 指标 | 目标值 | 测量方式 |
|------|--------|---------|
| **SIA 记录速率** | >10 条/天 | 统计 LEARNINGS.md |
| **Evolver 处理速率** | 100% 自动 | 查看进化报告 |
| **知识晋升速率** | >5 条/周 | 统计核心文档更新 |
| **错误减少率** | >30%/月 | 对比 ERRORS.md |
| **用户满意度** | >4.5/5 | 用户反馈 |

---

**整合版本:** v1.0  
**创建时间:** 2026-03-15 15:03  
**状态:** 配置完成，等待启用
