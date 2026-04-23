#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
漂移风险扫描工具
检测 High Intent Drift 风险
"""

import json
import sys
import re
from pathlib import Path

FORBIDDEN_PATTERNS = [
    r'fixed_signature',
    r'hardcoded_timestamp',
    r'static_fingerprint',
    r'202[0-9]-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}',  # 硬编码时间戳
    r'sha256:[a-f0-9]{64}',  # 硬编码 hash (非 asset_id 字段)
]

def scan_drift(file_path: Path) -> list:
    """扫描文件中的漂移风险"""
    risks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
    except json.JSONDecodeError:
        return ["JSON 格式错误"]
    except FileNotFoundError:
        return ["文件不存在"]
    
    # 检查 summary 是否过于具体
    summary = data.get('summary', '')
    if len(summary) > 200:
        risks.append(f"summary 过长 ({len(summary)}字符)，可能过于具体")
    
    # 检查是否包含具体时间戳
    if re.search(r'202[0-9]-[0-9]{2}-[0-9]{2}', summary):
        risks.append("summary 包含具体日期，可能导致 drift")
    
    # 检查 strategy 是否可复用
    strategy = data.get('strategy', [])
    for i, s in enumerate(strategy):
        if len(s) < 15:
            risks.append(f"strategy[{i}] 太短，可能不够具体")
        if re.search(r'[0-9]{10,}', s):  # 包含长数字
            risks.append(f"strategy[{i}] 包含具体数字，可能不可复用")
    
    # 检查 env_fingerprint (如果有)
    if 'env_fingerprint' in data:
        fp = data['env_fingerprint']
        if isinstance(fp, dict) and fp.get('captured_at'):
            risks.append("env_fingerprint 包含 captured_at，应动态生成")
    
    return risks

def main():
    if len(sys.argv) < 2:
        print("用法：python3 scan-drift.py <gene.json 文件>")
        sys.exit(1)
    
    gene_file = Path(sys.argv[1])
    
    print(f"🔍 扫描漂移风险：{gene_file.name}")
    print("-" * 50)
    
    risks = scan_drift(gene_file)
    
    if risks:
        print(f"⚠️ 发现 {len(risks)} 个风险:")
        for r in risks:
            print(f"   - {r}")
        print("\n💡 建议修复后再发布")
        sys.exit(1)
    else:
        print("✅ 未发现漂移风险")
        sys.exit(0)

if __name__ == "__main__":
    main()
