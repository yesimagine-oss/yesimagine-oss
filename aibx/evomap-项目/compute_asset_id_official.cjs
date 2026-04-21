#!/usr/bin/env node
/**
 * EvoMap Asset ID 计算器（官方版）
 * 使用官方 contentHash.js 的 canonicalize 算法
 * 
 * 使用方式:
 *   node compute_asset_id_official.cjs '{"type":"Gene",...}'
 */

const crypto = require('crypto');

// 官方 canonicalize 函数（来自 contentHash.js）
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

// CLI 入口
function main() {
  let inputData;
  
  if (process.argv.includes('--stdin')) {
    const fs = require('fs');
    inputData = fs.readFileSync(0, 'utf-8').trim();
  } else if (process.argv.length > 2) {
    inputData = process.argv[2];
  } else {
    console.error('Usage:');
    console.error('  node compute_asset_id_official.cjs \'{"type":"Gene",...}\'');
    console.error('  echo \'{"type":"Gene",...}\' | node compute_asset_id_official.cjs --stdin');
    process.exit(1);
  }
  
  try {
    const data = JSON.parse(inputData);
    const assetId = computeAssetId(data);
    console.log(assetId);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
