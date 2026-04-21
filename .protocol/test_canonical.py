#!/usr/bin/env python3
import json
import hashlib

# Load gene
with open('/home/admin/.openclaw/workspace/gene_distilled_evomap_publish_success_v1.json', 'r') as f:
    gene = json.load(f)

# Remove asset_id
gene.pop('asset_id', None)

# Method 1: json.dumps with sort_keys
canonical1 = json.dumps(gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
hash1 = hashlib.sha256(canonical1.encode()).hexdigest()

# Method 2: Custom recursive sort
def sort_keys_recursive(obj):
    if isinstance(obj, dict):
        return {k: sort_keys_recursive(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_keys_recursive(item) for item in obj]
    else:
        return obj

sorted_gene = sort_keys_recursive(gene)
canonical2 = json.dumps(sorted_gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
hash2 = hashlib.sha256(canonical2.encode()).hexdigest()

print(f"Method 1 hash: sha256:{hash1}")
print(f"Method 2 hash: sha256:{hash2}")
print(f"\nCanonical JSON (first 200 chars):")
print(canonical1[:200])
