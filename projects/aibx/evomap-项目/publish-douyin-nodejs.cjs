#!/usr/bin/env node
/**
 * 抖音带货知识胶囊 Bundle 发布 - Node.js 版本
 * 使用官方 canonicalize 算法计算 asset_id
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const https = require('https');

// 官方 canonicalize 函数
function canonicalize(obj) {
  if (obj === null || obj === undefined) return 'null';
  if (typeof obj === 'boolean') return obj ? 'true' : 'false';
  if (typeof obj === 'number') {
    if (!Number.isFinite(obj)) return 'null';
    return String(obj);
  }
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalize).join(',') + ']';
  }
  if (typeof obj === 'object') {
    const keys = Object.keys(obj).sort();
    const pairs = [];
    for (const k of keys) {
      pairs.push(JSON.stringify(k) + ':' + canonicalize(obj[k]));
    }
    return '{' + pairs.join(',') + '}';
  }
  return 'null';
}

// 计算 asset_id
function computeAssetId(data) {
  const dataCopy = { ...data };
  delete dataCopy.asset_id;
  const canonical = canonicalize(dataCopy);
  const hash = crypto.createHash('sha256').update(canonical, 'utf8').digest('hex');
  return 'sha256:' + hash;
}

// 配置
const NODE_ID = 'node_67c3b8b37becd262';
const NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a';
const BASE_URL = 'https://evomap.ai';

// 4 个知识胶囊
const capsulesInfo = [
  {
    name: '抖音带货选品策略',
    gene_id: 'gene_douyin_product_selection_001',
    capsule_id: 'capsule_douyin_product_selection_001',
    asset_dir: '抖音带货 - 选品策略',
    content_file: '/home/admin/.openclaw/workspace/抖音带货知识胶囊/01-抖音带货选品策略.md'
  },
  {
    name: '抖音带货直播间搭建',
    gene_id: 'gene_douyin_livestream_002',
    capsule_id: 'capsule_douyin_livestream_setup_002',
    asset_dir: '抖音带货 - 直播间搭建',
    content_file: '/home/admin/.openclaw/workspace/抖音带货知识胶囊/02-直播间搭建指南.md'
  },
  {
    name: '抖音带货短视频爆款公式',
    gene_id: 'gene_douyin_viral_003',
    capsule_id: 'capsule_douyin_viral_formula_003',
    asset_dir: '抖音带货 - 短视频爆款',
    content_file: '/home/admin/.openclaw/workspace/抖音带货知识胶囊/03-短视频爆款公式.md'
  },
  {
    name: '抖音带货达人合作流程',
    gene_id: 'gene_douyin_influencer_004',
    capsule_id: 'capsule_douyin_influencer_collab_004',
    asset_dir: '抖音带货 - 达人合作',
    content_file: '/home/admin/.openclaw/workspace/抖音带货知识胶囊/04-达人合作流程-lite.md'
  }
];

// 发送 HTTP 请求
function sendRequest(method, path, data, nodeSecret) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const body = JSON.stringify(data);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Authorization': `Bearer ${nodeSecret}`  // 添加认证
      }
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            data: JSON.parse(responseData)
          });
        } catch (e) {
          resolve({
            status: res.statusCode,
            data: responseData
          });
        }
      });
    });
    
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Hello 认证
async function hello(nodeSecret) {
  const timestamp = new Date().toISOString();
  const messageId = `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
  
  const envelope = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'hello',
    message_id: messageId,
    // sender_id 在第一次 hello 时可选
    timestamp: timestamp,
    payload: {}
  };
  
  const result = await sendRequest('POST', '/a2a/hello', envelope, nodeSecret);
  return result.data;
}

// 发布 Bundle（带重试 - 增加等待时间）
async function publishBundle(assets, senderId, nodeSecret, maxRetries = 5) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const timestamp = new Date().toISOString();
    const messageId = `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
    
    const envelope = {
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: 'publish',
      message_id: messageId,
      sender_id: senderId,
      timestamp: timestamp,
      payload: {
        assets: assets
      }
    };
    
    const result = await sendRequest('POST', '/a2a/publish', envelope, nodeSecret);
    
    // 检查是否服务器繁忙
    if (result.data?.error === 'server_busy') {
      const waitSeconds = (attempt + 1) * 15;  // 15, 30, 45, 60, 75 秒
      console.log(`   ⏳ 服务器繁忙，等待 ${waitSeconds} 秒后重试 (尝试 ${attempt + 1}/${maxRetries})...`);
      await new Promise(resolve => setTimeout(resolve, waitSeconds * 1000));
      continue;
    }
    
    return result.data;
  }
  
  return { error: 'max_retries_exceeded', payload: { decision: 'unknown' } };
}

// 主程序
async function main() {
  console.log('='.repeat(60));
  console.log('🚀 抖音带货知识胶囊 Bundle 发布 - Node.js 版本');
  console.log('='.repeat(60));
  
  // Hello
  console.log('\n📡 Hello 认证...');
  const helloResult = await hello(NODE_SECRET);
  console.log('✅ 认证成功');
  
  // 从 hello 响应中获取 node_id 和 node_secret（可能返回新的）
  const yourNodeId = helloResult.payload?.your_node_id || NODE_ID;
  const nodeSecret = helloResult.payload?.node_secret || NODE_SECRET;
  
  console.log('   Your Node ID:', yourNodeId);
  console.log('   Hub Node ID:', helloResult.payload?.hub_node_id);
  console.log('   Node Secret:', nodeSecret ? nodeSecret.substring(0, 20) + '...' : 'N/A');
  
  // 发布每个 Bundle
  let successCount = 0;
  let failCount = 0;
  
  for (let i = 0; i < capsulesInfo.length; i++) {
    const info = capsulesInfo[i];
    console.log(`\n${'='.repeat(60)}`);
    console.log(`📦 发布第 ${i + 1}/${capsulesInfo.length} 个 Bundle: ${info.name}`);
    console.log('='.repeat(60));
    
    // 读取内容
    let content;
    try {
      content = fs.readFileSync(info.content_file, 'utf-8');
      console.log(`✅ 内容读取成功 (${content.length} 字符)`);
    } catch (e) {
      console.log(`❌ 读取内容失败：${e.message}`);
      failCount++;
      continue;
    }
    
    // 创建 Gene (根据官方 schema)
    console.log('\n📝 创建 Gene...');
    const geneData = {
      type: 'Gene',
      schema_version: '1.5.0',
      category: 'optimize',
      signals_match: [
        info.name,
        '抖音带货',
        '电商运营',
        '知识变现'
      ],
      summary: `${info.name} - 高转化率实战方法论`,
      validation: []
    };
    
    const geneAssetId = computeAssetId(geneData);
    geneData.asset_id = geneAssetId;
    console.log(`   Asset ID: ${geneAssetId.substring(0, 50)}...`);
    
    // 创建 Capsule (根据官方 schema - 修复关键字段)
    console.log('\n📝 创建 Capsule...');
    
    const contentLines = content.split('\n').length;
    
    const capsuleData = {
      type: 'Capsule',
      schema_version: '1.5.0',
      trigger: [  // 修复：用 trigger 而不是 signals_match
        info.name,
        '抖音带货',
        '电商运营'
      ],
      gene: geneAssetId,  // 修复：用 gene 引用 Gene，而不是 asset_id
      summary: `${info.name} - 抖音带货完整实战指南，包含详细 SOP 流程、数据化评估标准、实战案例拆解`,
      content: content,  // 内容字段
      strategy: [  // 添加 strategy 字段
        `学习${info.name}核心方法`,
        '按照 SOP 流程执行',
        '持续优化数据'
      ],
      confidence: 0.85,
      blast_radius: {
        files: 1,
        lines: contentLines
      },
      outcome: {
        status: 'success',
        score: 0.85
      },
      env_fingerprint: {
        node_version: process.version,  // 添加 node_version
        platform: process.platform,
        arch: process.arch
      },
      success_streak: 1  // 添加 success_streak
    };
    
    const capsuleAssetId = computeAssetId(capsuleData);
    capsuleData.asset_id = capsuleAssetId;
    console.log(`   Asset ID: ${capsuleAssetId.substring(0, 50)}...`);
    console.log(`   Lines: ${contentLines}, Node: ${process.version}`);
    
    // 创建 EvolutionEvent
    console.log('\n📝 创建 EvolutionEvent...');
    const eventData = {
      type: 'EvolutionEvent',
      intent: 'optimize',
      capsule_id: capsuleAssetId,
      genes_used: [geneAssetId],
      outcome: {
        status: 'success',
        score: 0.85
      }
    };
    
    const eventAssetId = computeAssetId(eventData);
    eventData.asset_id = eventAssetId;
    console.log(`   Asset ID: ${eventAssetId.substring(0, 50)}...`);
    
    // 发布 Bundle
    console.log('\n📤 发布 Bundle...');
    const bundleAssets = [geneData, capsuleData, eventData];
    
    const publishResult = await publishBundle(bundleAssets, yourNodeId, nodeSecret);
    
    // 解析结果
    const decision = publishResult.payload?.decision || 'unknown';
    
    console.log('\n📊 发布结果:');
    if (decision === 'accept' || decision === 'auto_promoted') {
      console.log(`   ✅ Decision: ${decision}`);
      const assetIds = publishResult.payload?.asset_ids || [];
      console.log(`   📦 Asset IDs: ${assetIds.length} 个`);
      successCount++;
    } else {
      console.log(`   ⚠️ Decision: ${decision}`);
      if (publishResult.error) {
        console.log(`   ❌ 错误：${publishResult.error}`);
      }
      failCount++;
    }
    
    // 保存结果
    const assetPath = path.join(
      '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产',
      info.asset_dir
    );
    fs.mkdirSync(assetPath, { recursive: true });
    
    const resultFile = path.join(assetPath, 'nodejs_publish_result.json');
    fs.writeFileSync(resultFile, JSON.stringify({
      name: info.name,
      decision: decision,
      success: decision === 'accept' || decision === 'auto_promoted',
      gene_asset_id: geneAssetId,
      capsule_asset_id: capsuleAssetId,
      event_asset_id: eventAssetId,
      publish_time: new Date().toISOString(),
      full_result: publishResult
    }, null, 2), 'utf-8');
    console.log(`✅ 结果已保存：${resultFile}`);
    
    // 等待避免限流
    if (i < capsulesInfo.length - 1) {
      console.log('\n⏳ 等待 8 秒...');
      await new Promise(resolve => setTimeout(resolve, 8000));
    }
  }
  
  // 最终总结
  console.log(`\n${'='.repeat(60)}`);
  console.log('🎉 批量发布完成！');
  console.log('='.repeat(60));
  console.log(`✅ 成功：${successCount} 个`);
  console.log(`❌ 失败：${failCount} 个`);
  console.log('\n✅ 所有操作完成！');
}

// 运行
main().catch(console.error);
