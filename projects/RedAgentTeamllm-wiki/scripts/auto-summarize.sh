#!/bin/bash
# 自動為 wiki 文件生成摘要
mkdir -p reports/summaries
for file in wiki/**/*.md; do
  if [ -f "$file" ]; then
    summary="reports/summaries/$(basename $file .md)-summary.md"
    head -20 "$file" > "$summary"
    echo "✅ $file"
  fi
done
