#!/usr/bin/env node
/**
 * 🚀 使用 Node.js 計算 asset_id 並發布
 * 目標：確保與 Hub 的計算方法完全一致
 */

const fs = require('fs');
const crypto = require('crypto');
const https = require('https');

// 配置
const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

// 遞歸排序對象鍵
function sortObjectKeys(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    if (Array.isArray(obj)) {
        return obj.map(sortObjectKeys);
    }
    const sortedObj = {};
    Object.keys(obj).sort().forEach(key => {
        sortedObj[key] = sortObjectKeys(obj[key]);
    });
    return sortedObj;
}

// 計算 asset_id
function computeAssetId(asset) {
    const assetCopy = { ...asset };
    delete assetCopy.asset_id;
    const sorted = sortObjectKeys(assetCopy);
    const canonicalJson = JSON.stringify(sorted);
    const hash = crypto.createHash('sha256').update(canonicalJson).digest('hex');
    return `sha256:${hash}`;
}

// 發送 HTTP POST 請求
function postRequest(url, data, headers) {
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
    console.log('='.repeat(60));
    console.log('🚀 使用 Node.js 計算 asset_id 並發布');
    console.log('='.repeat(60));

    // 讀取成功的模板
    const template = JSON.parse(fs.readFileSync('/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json', 'utf8'));

    console.log('\n📦 成功模板中的 Gene:');
    console.log(`  asset_id: ${template.assets[0].asset_id}`);

    // 計算 Gene 的 asset_id
    const geneAssetId = computeAssetId(template.assets[0]);
    console.log(`\n🔍 Node.js 計算的 Gene asset_id: ${geneAssetId}`);
    console.log(`🔍 模板中的 Gene asset_id: ${template.assets[0].asset_id}`);
    console.log(`🔍 匹配：${geneAssetId === template.assets[0].asset_id}`);

    // 計算 Capsule 的 asset_id
    const capsuleAssetId = computeAssetId(template.assets[1]);
    console.log(`\n🔍 Node.js 計算的 Capsule asset_id: ${capsuleAssetId}`);
    console.log(`🔍 模板中的 Capsule asset_id: ${template.assets[1].asset_id}`);
    console.log(`🔍 匹配：${capsuleAssetId === template.assets[1].asset_id}`);

    // 如果匹配，直接發布模板
    if (geneAssetId === template.assets[0].asset_id && capsuleAssetId === template.assets[1].asset_id) {
        console.log('\n✅ Hash 計算方法正確！直接發布模板...');

        const envelope = {
            protocol: 'gep-a2a',
            protocol_version: '1.0.0',
            message_type: 'publish',
            message_id: `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`,
            sender_id: NODE_ID,
            timestamp: new Date().toISOString(),
            payload: template
        };

        const headers = {
            'X-Node-ID': NODE_ID,
            'Authorization': `Bearer ${NODE_SECRET}`
        };

        const result = await postRequest(`${HUB_URL}/a2a/publish`, envelope, headers);

        console.log(`\n📥 狀態碼：${result.status}`);
        console.log(`📥 響應：${JSON.stringify(result.data, null, 2)}`);

        if (result.status === 200) {
            console.log('\n' + '='.repeat(60));
            console.log('✅ 發布成功！');
            console.log('='.repeat(60));
            return true;
        }
    }

    console.log('\n' + '='.repeat(60));
    console.log('⚠️  Hash 計算方法與模板不匹配');
    console.log('='.repeat(60));
    return false;
}

main().then(success => process.exit(success ? 0 : 1));
