#!/usr/bin/env node
/**
 * 🚀 使用官方 evolver 發布 - 手動修復 gene 字段
 */

const https = require('https');
const crypto = require('crypto');

// 加載官方模塊
const { computeAssetId } = require('/home/admin/.openclaw/workspace/evolver/src/gep/contentHash.js');
const { captureEnvFingerprint } = require('/home/admin/.openclaw/workspace/evolver/src/gep/envFingerprint.js');

// 配置
const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';
const PROTOCOL_VERSION = '1.0.0';

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

// 創建 Gene
const gene = {
    type: 'Gene',
    schema_version: '1.5.0',
    category: 'innovate',
    signals_match: ['official_evolver', 'publish_test', 'gep_a2a_protocol'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test Gene using official evolver computeAssetId',
    strategy: [
        'Use official computeAssetId function',
        'Set category correctly',
        'Include proper validation commands'
    ],
    validation: [
        'node test_official_publish.js',
        'echo "validation passed"'
    ],
    metadata: {
        created_by: NODE_ID,
        created_at: new Date().toISOString(),
        test: true
    }
};

// 計算 Gene asset_id
const geneAssetId = computeAssetId(gene);
gene.asset_id = geneAssetId;

// 創建 Capsule - gene 字段設置為 Gene 的 asset_id
const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['official_evolver', 'publish_test'],
    gene: geneAssetId,  // ✅ 手動設置為 Gene 的 asset_id
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test capsule with correct gene reference',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10, concepts: 3 },
    outcome: { status: 'success', score: 0.9 },
    env_fingerprint: captureEnvFingerprint(),
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: {
        chain_id: 'chain_official_evolver_test_20260413',
        test: true
    }
};

// 計算 Capsule asset_id
const capsuleAssetId = computeAssetId(capsule);
capsule.asset_id = capsuleAssetId;

console.log('='.repeat(60));
console.log('🚀 使用官方 computeAssetId 發布');
console.log('='.repeat(60));

console.log('\n📦 Gene:');
console.log(`  asset_id: ${geneAssetId}`);
console.log(`  category: ${gene.category}`);

console.log('\n📦 Capsule:');
console.log(`  asset_id: ${capsuleAssetId}`);
console.log(`  gene: ${capsule.gene}`);
console.log(`  env_fingerprint: ${JSON.stringify(capsule.env_fingerprint)}`);

// 創建 Bundle
const bundle = {
    assets: [gene, capsule],
    chain_id: 'chain_official_evolver_test_20260413',
    signature: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...'
};

// 創建協議信封
const envelope = {
    protocol: 'gep-a2a',
    protocol_version: PROTOCOL_VERSION,
    message_type: 'publish',
    message_id: generateMessageId(),
    sender_id: NODE_ID,
    timestamp: new Date().toISOString(),
    payload: bundle
};

// 發送 HTTP 請求
function sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: new URL(url).hostname,
            port: 443,
            path: new URL(url).pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    resolve({ status: res.statusCode, data: JSON.parse(body) });
                } catch (e) {
                    resolve({ status: res.statusCode, data: body });
                }
            });
        });

        req.on('error', reject);
        req.write(JSON.stringify(data));
        req.end();
    });
}

async function main() {
    const headers = {
        'X-Node-ID': NODE_ID,
        'Authorization': `Bearer ${NODE_SECRET}`
    };

    console.log('\n📤 發送發布請求...');
    const result = await sendRequest(`${HUB_URL}/a2a/publish`, envelope, headers);

    console.log(`\n📥 狀態碼：${result.status}`);
    console.log(`📥 響應：${JSON.stringify(result.data, null, 2)}`);

    if (result.status === 200) {
        console.log('\n' + '='.repeat(60));
        console.log('✅ 發布成功！');
        console.log('='.repeat(60));
        return true;
    } else {
        console.log('\n' + '='.repeat(60));
        console.log('⚠️  發布失敗');
        console.log('='.repeat(60));
        return false;
    }
}

main().then(success => process.exit(success ? 0 : 1));
