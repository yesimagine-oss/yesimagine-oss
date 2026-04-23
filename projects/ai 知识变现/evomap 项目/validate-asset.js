#!/usr/bin/env node
/**
 * 使用 /a2a/validate 验证 asset_id
 */

const crypto = require('crypto');
const https = require('https');

const NODE_ID = 'node_67c3b8b37becd262';
const NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a';
const BASE_URL = 'https://evomap.ai';

function canonicalStringify(obj) {
    if (obj === null || obj === undefined) return 'null';
    if (typeof obj === 'boolean') return obj ? 'true' : 'false';
    if (typeof obj === 'number') return String(obj);
    if (typeof obj === 'string') return JSON.stringify(obj);
    if (Array.isArray(obj)) {
        return '[' + obj.map(v => canonicalStringify(v)).join(',') + ']';
    }
    if (typeof obj === 'object') {
        const keys = Object.keys(obj).sort();
        return '{' + keys.map(k => `"${k}":${canonicalStringify(obj[k])}`).join(',') + '}';
    }
    return JSON.stringify(obj);
}

function computeAssetId(asset) {
    const { asset_id, ...clean } = asset;
    const canonical = canonicalStringify(clean);
    const hash = crypto.createHash('sha256').update(canonical).digest('hex');
    return `sha256:${hash}`;
}

function post(url, data, headers = {}) {
    return new Promise((resolve, reject) => {
        const req = https.request(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...headers },
            timeout: 60000
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => resolve({ status: res.statusCode, data: JSON.parse(body || '{}') }));
        });
        req.on('error', reject);
        req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
        req.write(JSON.stringify(data));
        req.end();
    });
}

async function validate() {
    console.log('🔍 验证 asset_id\n');
    
    const gene = {
        type: 'Gene',
        schema_version: '1.5.0',
        category: 'optimize',
        summary: '抖音带货选品策略 - 高转化率商品选择方法论，包含佣金率销量增长评分退货率四维评估模型',
        signals_match: ['抖音带货', '选品策略', '电商运营', '转化率优化', '爆款选品'],
        strategy: ['选择佣金率 20%+ 的商品', '优先选择 7 天内销量增长>100%', '选择评分 4.8+ 且差评率<3%', '聚焦垂直领域建立专业人设', '使用蝉妈妈飞瓜数据监控热度', '选择退货率<15% 的商品'],
        confidence: 0.90,
        blast_radius: { files: 1, lines: 200 },
        domain: 'marketing',
        env_fingerprint: { arch: 'x64', platform: 'linux', node_version: 'v24.14.0' }
    };
    
    const geneId = computeAssetId(gene);
    console.log(`我们计算的 Gene asset_id: ${geneId}`);
    console.log(`\nGene canonical JSON:\n${canonicalStringify(gene)}\n`);
    
    // 使用 validate 端点验证
    const validatePayload = {
        protocol: 'gep-a2a',
        protocol_version: '1.0.0',
        message_type: 'validate',
        message_id: `msg_${Date.now()}`,
        sender_id: NODE_ID,
        timestamp: new Date().toISOString(),
        payload: {
            assets: [{
                type: 'Gene',
                schema_version: '1.5.0',
                asset_id: geneId
            }]
        }
    };
    
    console.log('📤 发送验证请求...');
    const headers = { 'Authorization': `Bearer ${NODE_SECRET}` };
    
    try {
        const result = await post(`${BASE_URL}/a2a/validate`, validatePayload, headers);
        console.log(`\n状态：${result.status}`);
        console.log(`响应：${JSON.stringify(result.data, null, 2)}`);
    } catch (e) {
        console.log(`错误：${e.message}`);
    }
}

validate();
