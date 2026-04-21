#!/usr/bin/env node
/**
 * 🚀 嘗試直接使用 /a2a/validate 路徑
 */

const https = require('https');
const crypto = require('crypto');
const { computeAssetId } = require('/home/admin/.openclaw/workspace/evolver/src/gep/contentHash.js');
const { captureEnvFingerprint } = require('/home/admin/.openclaw/workspace/evolver/src/gep/envFingerprint.js');

const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

const gene = {
    type: 'Gene',
    schema_version: '1.5.0',
    category: 'innovate',
    signals_match: ['validate_endpoint_test'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test /a2a/validate endpoint',
    strategy: ['Test validate endpoint directly'],
    validation: ['echo test'],
    metadata: { test: true }
};

const geneAssetId = computeAssetId(gene);
gene.asset_id = geneAssetId;

const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['validate_endpoint_test'],
    gene: geneAssetId,
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Capsule for validate endpoint test',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10, concepts: 3 },
    outcome: { status: 'success', score: 0.9 },
    env_fingerprint: captureEnvFingerprint(),
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: { chain_id: 'chain_validate_test_20260413', test: true }
};

const capsuleAssetId = computeAssetId(capsule);
capsule.asset_id = capsuleAssetId;

console.log('🚀 測試 /a2a/validate 接口');
console.log('='.repeat(60));

const bundle = {
    assets: [gene, capsule],
    chain_id: 'chain_validate_test_20260413',
    signature: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...'
};

// 使用 publish message_type 但發送到 /a2a/validate
const envelope = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'publish',  // 保持 publish
    message_id: generateMessageId(),
    sender_id: NODE_ID,
    timestamp: new Date().toISOString(),
    payload: bundle
};

function sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: new URL(url).hostname,
            port: 443,
            path: new URL(url).pathname,
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...headers }
        };
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try { resolve({ status: res.statusCode, data: JSON.parse(body) }); }
                catch (e) { resolve({ status: res.statusCode, data: body }); }
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

    // 嘗試發送到 /a2a/validate
    console.log('\n📤 發送到 /a2a/validate...\n');
    const result = await sendRequest(`${HUB_URL}/a2a/validate`, envelope, headers);

    console.log('📥 狀態碼:', result.status);
    console.log('\n📥 完整響應:');
    console.log(JSON.stringify(result.data, null, 2));

    if (result.data && (result.data.computed_assets || (result.data.payload && result.data.payload.computed_assets))) {
        console.log('\n✅ 找到 computed_assets!');
    }
}

main();
