#!/usr/bin/env node
/**
 * 🚀 打印完整響應並檢查所有字段
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
    signals_match: ['validate_endpoint', 'asset_id_fix'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Validate endpoint test with complete asset structure',
    strategy: [
        'Step 1: Send validate request to /a2a/validate endpoint',
        'Step 2: Extract computed_asset_id from response',
        'Step 3: Replace local asset_id with Hub computed one',
        'Step 4: Send publish request with correct asset_id'
    ],
    validation: [
        'node test_validate.js',
        'node verify_asset.js'
    ],
    metadata: {
        created_by: NODE_ID,
        created_at: new Date().toISOString(),
        test: true
    }
};

const geneAssetId = computeAssetId(gene);
gene.asset_id = geneAssetId;

const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['validate_endpoint'],
    gene: geneAssetId,
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Capsule with strategy field for substance requirement',
    strategy: [
        'Execute validate request to obtain computed asset IDs',
        'Replace local asset_id with Hub computed values',
        'Submit publish request with validated asset IDs'
    ],
    confidence: 0.95,
    blast_radius: { files: 1, lines: 15, concepts: 5 },
    outcome: { status: 'success', score: 0.95 },
    env_fingerprint: captureEnvFingerprint(),
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: {
        chain_id: 'chain_validate_complete_20260413',
        test: true
    }
};

const capsuleAssetId = computeAssetId(capsule);
capsule.asset_id = capsuleAssetId;

const bundle = {
    assets: [gene, capsule],
    chain_id: 'chain_validate_complete_20260413',
    signature: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...'
};

const envelope = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'publish',
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

    console.log('🔍 打印完整響應並檢查所有字段');
    console.log('='.repeat(60));
    console.log('\n📤 發送到 /a2a/validate...\n');
    
    const result = await sendRequest(`${HUB_URL}/a2a/validate`, envelope, headers);

    console.log('📥 狀態碼:', result.status);
    console.log('\n📥 完整響應 (RAW):');
    console.log(JSON.stringify(result, null, 2));
    
    console.log('\n📥 響應數據所有鍵:');
    console.log(Object.keys(result.data));
    
    if (result.data && typeof result.data === 'object') {
        for (const key of Object.keys(result.data)) {
            console.log(`\n  ${key}:`, typeof result.data[key] === 'object' ? JSON.stringify(result.data[key]) : result.data[key]);
        }
    }
}

main();
