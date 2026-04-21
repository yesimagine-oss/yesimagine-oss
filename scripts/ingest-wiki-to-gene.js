#!/usr/bin/env node
/**
 * 📥 LLM-Wiki 文件攝入為 Gene 的標準流程
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置
const RAW_DIR = '/home/admin/llm-wiki/raw';
const WIKI_DIR = '/home/admin/llm-wiki/wiki';
const GENES_DIR = '/home/admin/.openclaw/workspace';

// 從文件內容計算 asset_id
function computeAssetId(content, metadata) {
    const obj = { content, ...metadata };
    delete obj.asset_id;
    const canonical = JSON.stringify(obj, Object.keys(obj).sort());
    const hash = crypto.createHash('sha256').update(canonical, 'utf8').digest('hex');
    return `sha256:${hash}`;
}

// 從 raw 文件創建 Gene
function createGeneFromRaw(rawFile) {
    const content = fs.readFileSync(rawFile, 'utf8');
    const fileName = path.basename(rawFile, '.md');
    
    // 提取元數據（從文件名或內容）
    const metadata = {
        source: 'llm-wiki/raw',
        ingested_at: new Date().toISOString(),
        original_file: fileName
    };
    
    // 創建 Gene 對象
    const gene = {
        type: 'Gene',
        schema_version: '1.5.0',
        category: 'innovate',
        signals_match: [fileName.replace(/_/g, '-').replace('asset', '').replace(/\d+$/, '')],
        summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Knowledge from LLM-Wiki: ' + fileName,
        strategy: [
            'Read raw asset from llm-wiki/raw',
            'Extract knowledge content',
            'Convert to Gene format',
            'Compute asset_id',
            'Store in workspace'
        ],
        validation: [
            'node verify_gene.js',
            'node validate_format.js'
        ],
        metadata: metadata,
        content: content.substring(0, 500) // 截斷內容
    };
    
    gene.asset_id = computeAssetId(gene.content, metadata);
    
    return gene;
}

// 攝入所有 raw 文件
function ingestAll() {
    console.log('='.repeat(60));
    console.log('📥 LLM-Wiki 文件攝入為 Gene');
    console.log('='.repeat(60));
    
    const rawFiles = fs.readdirSync(RAW_DIR).filter(f => f.endsWith('.md'));
    console.log(`\n找到 ${rawFiles.length} 個原始資產`);
    
    const genes = [];
    for (const file of rawFiles) {
        console.log(`\n📄 處理：${file}`);
        const gene = createGeneFromRaw(path.join(RAW_DIR, file));
        genes.push(gene);
        console.log(`   asset_id: ${gene.asset_id}`);
    }
    
    console.log(`\n✅ 完成：${genes.length} 個 Gene`);
    return genes;
}

if (process.argv[2] === '--run') {
    ingestAll();
} else {
    console.log('Usage: node ingest-wiki-to-gene.js --run');
}

module.exports = { createGeneFromRaw, ingestAll };
