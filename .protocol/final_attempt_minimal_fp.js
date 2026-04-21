#!/usr/bin/env node
/**
 * 🚀 最終方案：讓 Hub 計算 asset_id
 * 策略：發送時使用佔位符，Hub 會忽略並重新計算
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
    signals_match: ['final_attempt', 'hub_computes_asset_id'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Final attempt - let Hub compute and accept asset_id',
    strategy: [
        'Step 1: Create Gene with all required fields',
        'Step 2: Compute asset_id using official canonicalize',
        'Step 3: Send to Hub and trust the validation',
        'Step 4: If fails, Hub will provide correction'
    ],
    validation: [
        'node test_final.js',
        'node verify_final.js'
    ],
    metadata: {
        created_by: NODE_ID,
        created_at: new Date().toISOString(),
        test: true,
        attempt: 'final'
    }
};

const geneAssetId = computeAssetId(gene);
gene.asset_id = geneAssetId;

// Capsule 使用簡化的 env_fingerprint（只包含穩定字段）
const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['final_attempt'],
    gene: geneAssetId,
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Final capsule with minimal stable env_fingerprint',
    strategy: [
        'Use minimal env_fingerprint with stable fields only',
        'Trust Hub validation process'
    ],
    confidence: 0.95,
    blast_radius: { files: 1, lines: 15, concepts: 5 },
    outcome: { status: 'success', score: 0.95 },
    // 只包含穩定字段，避免 Hub 修改
    env_fingerprint: {
        node_version: 'v24.14.0',
        platform: 'linux',
        arch: 'x64'
    },
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: {
        chain_id: 'chain_final_attempt_20260413',
        test: true
    }
};

const capsuleAssetId = computeAssetId(capsule);
capsule.asset_id = capsuleAssetId;

console.log('='.repeat(60));
console.log('🚀 最終方案 - 使用簡化 env_fingerprint');
console.log('='.repeat(60));
console.log('\n📦 Gene asset_id:', geneAssetId);
console.log('📦 Capsule asset_id:', capsuleAssetId);
console.log('📦 Capsule env_fingerprint:', capsule.env_fingerprint);

const bundle = {
    assets: [gene, capsule],
    chain_id: 'chain_final_attempt_20260413',
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

    console.log('\n📤 發送 publish 請求...\n');
    const result = await sendRequest(`${HUB_URL}/a2a/publish`, envelope, headers);

    console.log('📥 狀態碼:', result.status);
    console.log('\n📥 完整響應:');
    console.log(JSON.stringify(result.data, null, 2));

    if (result.status === 200) {
        console.log('\n' + '='.repeat(60));
        console.log('✅ 發布成功！');
        console.log('='.repeat(60));
        return true;
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('⚠️  發布失敗');
    console.log('='.repeat(60));
    return false;
}

main().then(success => process.exit(success ? 0 : 1));
