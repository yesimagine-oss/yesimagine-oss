#!/usr/bin/env node

/**
 * 腾讯企业邮监控脚本
 * 使用 IMAP 检查新邮件
 */

import Imap from 'imap';
import { simpleParser } from 'mailparser';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_PATH = path.join(__dirname, 'mail-state.json');
const CONFIG_PATH = path.join(__dirname, 'config.json');

// 邮件配置
const IMAP_CONFIG = {
  user: 'red@unvw.com',
  password: 'Red73951',
  host: 'imap.exmail.qq.com',
  port: 993,
  tls: true,
  tlsOptions: { servername: 'imap.exmail.qq.com' },
};

// 加载已处理邮件 ID
function loadState() {
  try {
    if (fs.existsSync(STATE_PATH)) {
      return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
    }
  } catch (e) {
    console.error('加载状态失败:', e.message);
  }
  return { processedIds: [], lastCheck: null };
}

// 保存状态
function saveState(state) {
  try {
    fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
  } catch (e) {
    console.error('保存状态失败:', e.message);
  }
}

// 检查邮件是否是新的（未处理过）
function isNewMail(uid, state) {
  return !state.processedIds.includes(uid);
}

// 标记邮件为已处理
function markAsProcessed(uid, state, maxKeep = 100) {
  if (!state.processedIds.includes(uid)) {
    state.processedIds.push(uid);
    // 保持列表大小
    if (state.processedIds.length > maxKeep) {
      state.processedIds = state.processedIds.slice(-maxKeep);
    }
  }
  state.lastCheck = new Date().toISOString();
}

// 解析邮件地址
function parseAddress(addr) {
  if (!addr) return '未知';
  if (Array.isArray(addr)) {
    return addr.map(a => a.address).join(', ');
  }
  return addr.address || addr.name || '未知';
}

// 检查邮件是否重要
function isImportant(mail) {
  const subject = mail.subject?.toLowerCase() || '';
  const from = mail.from?.value?.[0]?.address?.toLowerCase() || '';
  
  // 重要关键词
  const importantKeywords = [
    '紧急', 'urgent', '重要', 'important', '必须', 'required',
    '付款', 'payment', '合同', 'contract', '发票', 'invoice',
    '会议', 'meeting', '截止', 'deadline', '提醒', 'reminder'
  ];
  
  // 检查主题
  for (const keyword of importantKeywords) {
    if (subject.includes(keyword)) {
      return true;
    }
  }
  
  // 检查发件人（可以添加重要联系人）
  const importantSenders = [];
  for (const sender of importantSenders) {
    if (from.includes(sender)) {
      return true;
    }
  }
  
  return false;
}

// 检查邮件
async function checkMail() {
  console.log(`📧 [${new Date().toLocaleString('zh-CN')}] 开始检查邮件...\n`);
  
  const state = loadState();
  const config = loadConfig();
  
  return new Promise((resolve, reject) => {
    const imap = new Imap(IMAP_CONFIG);
    
    imap.on('error', (err) => {
      console.error('❌ IMAP 连接错误:', err.message);
      reject(err);
    });
    
    imap.on('ready', () => {
      console.log('✅ IMAP 连接成功\n');
      
      imap.openBox('INBOX', false, (err, box) => {
        if (err) {
          console.error('❌ 打开收件箱失败:', err.message);
          imap.end();
          reject(err);
          return;
        }
        
        console.log(`📥 收件箱共有 ${box.messages.total} 封邮件\n`);
        
        // 获取最近的邮件（最多 20 封）
        const searchRange = [];
        const start = Math.max(1, box.messages.total - 19);
        for (let i = start; i <= box.messages.total; i++) {
          searchRange.push(i);
        }
        
        if (searchRange.length === 0) {
          console.log('📭 收件箱为空');
          imap.end();
          resolve({ newMails: 0, importantMails: 0 });
          return;
        }
        
        const fetch = imap.fetch(searchRange, { bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)', struct: true });
        
        let newMailCount = 0;
        let importantMailCount = 0;
        const newMails = [];
        
        fetch.on('message', (msg, seqno) => {
          const attributes = [];
          
          msg.on('body', (stream, info) => {
            let buffer = '';
            stream.on('data', (chunk) => {
              buffer += chunk.toString('utf8');
            });
            stream.on('end', () => {
              const parsed = simpleParser(buffer);
              attributes.push(parsed);
            });
          });
          
          msg.on('attributes', (attrs) => {
            const uid = attrs.uid;
            const flags = attrs.flags;
            
            Promise.all(attributes).then(async (parsedMails) => {
              const mail = parsedMails[0];
              
              if (isNewMail(uid, state)) {
                newMailCount++;
                markAsProcessed(uid, state);
                
                const important = isImportant(mail);
                if (important) {
                  importantMailCount++;
                }
                
                const mailInfo = {
                  uid,
                  from: parseAddress(mail.from),
                  subject: mail.subject || '(无主题)',
                  date: mail.date?.toLocaleString('zh-CN') || '未知时间',
                  important,
                  unread: !flags.includes('\\Seen')
                };
                
                newMails.push(mailInfo);
                
                console.log(`📬 新邮件 #${newMailCount}`);
                console.log(`   发件人：${mailInfo.from}`);
                console.log(`   主题：${mailInfo.subject}`);
                console.log(`   时间：${mailInfo.date}`);
                console.log(`   状态：${mailInfo.unread ? '未读' : '已读'} ${important ? '⚠️ 重要' : ''}`);
                console.log();
              }
            });
          });
        });
        
        fetch.on('error', (err) => {
          console.error('❌ 获取邮件失败:', err.message);
        });
        
        fetch.on('end', () => {
          console.log('─────────────────────────────────────');
          console.log(`本次检查：发现 ${newMailCount} 封新邮件，${importantMailCount} 封重要邮件`);
          
          if (newMailCount === 0) {
            console.log('✅ 没有新邮件');
          }
          
          saveState(state);
          imap.end();
          
          resolve({
            newMails: newMailCount,
            importantMails: importantMailCount,
            mails: newMails
          });
        });
      });
    });
    
    imap.connect();
  });
}

// 加载配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (e) {
    console.error('加载配置失败:', e.message);
  }
  return {
    notifyOnImportant: true,
    notifyOnAny: false,
    checkIntervalMinutes: 5
  };
}

// 主函数
async function main() {
  try {
    const result = await checkMail();
    
    const config = loadConfig();
    
    // 是否需要通知
    if (config.notifyOnImportant && result.importantMails > 0) {
      console.log('\n⚠️  发现重要邮件，需要通知用户！');
      // 这里可以集成通知功能（飞书消息、邮件等）
    } else if (config.notifyOnAny && result.newMails > 0) {
      console.log('\n📬 发现新邮件，需要通知用户！');
    }
    
    process.exit(0);
  } catch (e) {
    console.error('\n❌ 检查邮件失败:', e.message);
    process.exit(1);
  }
}

// 如果是直接运行
if (process.argv[1]?.includes('check-mail.js')) {
  main();
}

export { checkMail, loadConfig, loadState };
