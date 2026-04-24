#!/bin/bash
# EvoMap 資產批量發布腳本
# 日期：2026-04-24

set -e

ASSET_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/assets/batch-publish-2026-04-24"
GENES_DIR="$ASSET_DIR/genes"
CAPSULES_DIR="$ASSET_DIR/capsules"
OUTPUT_DIR="$ASSET_DIR/gepx"

mkdir -p "$OUTPUT_DIR"

echo "=== EvoMap 資產批量發布 ==="
echo "日期：$(date)"
echo ""

# 處理 Gene 資產
echo "📦 處理 Gene 資產..."
for gene_file in "$GENES_DIR"/*.gene.md; do
    if [ -f "$gene_file" ]; then
        gene_name=$(basename "$gene_file" .gene.md)
        echo "  ✓ $gene_name"
        # 提取 JSON 內容
        sed -n '/^```json/,/^```/p' "$gene_file" | sed '1d;$d' > "$OUTPUT_DIR/$gene_name.gene.json"
    fi
done

# 處理 Capsule 資產
echo "📦 處理 Capsule 資產..."
for capsule_file in "$CAPSULES_DIR"/*.capsule.md; do
    if [ -f "$capsule_file" ]; then
        capsule_name=$(basename "$capsule_file" .capsule.md)
        echo "  ✓ $capsule_name"
        # 提取 JSON 內容
        sed -n '/^```json/,/^```/p' "$capsule_file" | sed '1d;$d' > "$OUTPUT_DIR/$capsule_name.capsule.json"
    fi
done

echo ""
echo "✅ 資產提取完成"
echo "📁 輸出目錄：$OUTPUT_DIR"
echo ""

# 統計
gene_count=$(ls "$OUTPUT_DIR"/*.gene.json 2>/dev/null | wc -l)
capsule_count=$(ls "$OUTPUT_DIR"/*.capsule.json 2>/dev/null | wc -l)

echo "📊 統計:"
echo "  Genes: $gene_count"
echo "  Capsules: $capsule_count"
echo "  總計: $((gene_count + capsule_count))"
echo ""

# 創建發布清單
cat > "$OUTPUT_DIR/PUBLISH_MANIFEST.md" << EOF
# 發布清單

**日期:** $(date -Iseconds)
**批次:** batch-publish-2026-04-24

## 資產列表

### Genes ($gene_count)
$(ls "$GENES_DIR"/*.gene.md | xargs -n1 basename | sed 's/.gene.md$//')

### Capsules ($capsule_count)
$(ls "$CAPSULES_DIR"/*.capsule.md | xargs -n1 basename | sed 's/.capsule.md$//')

## 預計價值

| 類型 | 數量 | 單價 | 總計 |
|------|------|------|------|
| Genes | $gene_count | \$20-50 | \$140-350 |
| Capsules | $capsule_count | \$30-100 | \$90-300 |
| **總計** | $((gene_count + capsule_count)) | - | **\$230-650** |

## 被動收入預估

| 時間 | 預估收入 |
|------|----------|
| 日 | \$5-20 |
| 週 | \$35-140 |
| 月 | \$150-600 |

---

**狀態:** 待發布
**發布方式:** evolver / Hub API
EOF

echo "📋 發布清單已創建：$OUTPUT_DIR/PUBLISH_MANIFEST.md"
echo ""
echo "=== 完成 ==="
