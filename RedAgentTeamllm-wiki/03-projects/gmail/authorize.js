#!/usr/bin/env node

/**
 * Gmail API OAuth2 授权脚本
 * 运行后会打开浏览器，让你登录 Google 账号并授权
 */

import { authenticate } from '@google-cloud/local-auth';
import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');
const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];

async function authorize() {
  console.log('🔐 Gmail API 授权工具\n');
  
  // 检查凭据文件
  if (!fs.existsSync(CREDENTIALS_PATH)) {
    console.error('❌ 错误：找不到 credentials.json');
    console.error('请确保此文件与脚本在同一目录');
    process.exit(1);
  }
  
  // 检查现有 token
  if (fs.existsSync(TOKEN_PATH)) {
    console.log('⚠️  发现已有的 token.json');
    console.log('是否要重新授权？(y/N): ');
    
    const answer = await new Promise(resolve => {
      process.stdin.once('data', data => {
        resolve(data.toString().trim().toLowerCase());
      });
    });
    
    if (answer === 'y' || answer === 'yes') {
      fs.unlinkSync(TOKEN_PATH);
      console.log('🗑️  已删除旧 token\n');
    } else {
      console.log('✅ 使用现有 token');
      console.log(`📍 Token 位置：${TOKEN_PATH}`);
      process.exit(0);
    }
  }
  
  console.log('📝 即将打开浏览器进行授权...');
  console.log('🔑 请求的权限：读取 Gmail 邮件（只读）\n');
  
  try {
    // 执行授权
    const oauth2Client = await authenticate({
      keyfilePath: CREDENTIALS_PATH,
      scopes: SCOPES,
    });
    
    // 保存 token
    const tokens = oauth2Client.credentials;
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    
    console.log('\n✅ 授权成功！');
    console.log(`📍 Token 已保存到：${TOKEN_PATH}`);
    console.log('\n⚠️  重要提示：');
    console.log('   - token.json 包含敏感信息，不要分享给他人');
    console.log('   - Token 过期后会自动刷新，无需重新授权');
    console.log('   - 如需撤销授权，访问：https://myaccount.google.com/permissions\n');
    
  } catch (error) {
    console.error('\n❌ 授权失败:', error.message);
    console.error('\n可能的原因：');
    console.error('   1. 浏览器未成功打开');
    console.error('   2. 授权流程被中断');
    console.error('   3. Google 账号登录问题');
    console.error('\n请重试，或手动访问授权 URL 完成授权。');
    process.exit(1);
  }
}

authorize();
