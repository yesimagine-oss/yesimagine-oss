#!/usr/bin/env node
/**
 * 🔧 LLM-Wiki 維護腳本 - 備份、清理、完整性檢查
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

const WIKI_ROOT = '/home/admin/llm-wiki';
const BACKUP_DIR = '/home/admin/llm-wiki-backups';
const GENES_DIR = '/home/admin/.openclaw/workspace';

// 1. 備份知識庫
function backup(options = {}) {
    const { timestamp = Date.now(), compress = true } = options;
    const backupPath = path.join(BACKUP_DIR, `llm-wiki-${timestamp}`);
    
    console.log(`📦 備份到：${backupPath}`);
    
    // 創建備份目錄
    if (!fs.existsSync(BACKUP_DIR)) {
        fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
    
    // 複製整個 wiki 目錄
    execSync(`cp -r ${WIKI_ROOT} ${backupPath}`);
    
    // 可選壓縮
    if (compress) {
        execSync(`tar -czf ${backupPath}.tar.gz -C ${path.dirname(backupPath)} ${path.basename(backupPath)}`);
        execSync(`rm -rf ${backupPath}`);
        console.log(`✅ 壓縮備份：${backupPath}.tar.gz`);
        return `${backupPath}.tar.gz`;
    }
    
    console.log(`✅ 備份完成：${backupPath}`);
    return backupPath;
}

// 2. 清理舊備份（保留最近 N 個）
function cleanupBackups(keepCount = 5) {
    console.log(`🧹 清理舊備份（保留最近 ${keepCount} 個）`);
    
    if (!fs.existsSync(BACKUP_DIR)) {
        console.log('⚠️  備份目錄不存在');
        return;
    }
    
    const backups = fs.readdirSync(BACKUP_DIR)
        .filter(f => f.startsWith('llm-wiki-'))
        .sort()
        .reverse();
    
    if (backups.length > keepCount) {
        const toDelete = backups.slice(keepCount);
        for (const file of toDelete) {
            const fullPath = path.join(BACKUP_DIR, file);
            execSync(`rm -rf ${fullPath}`);
            console.log(`   🗑️  刪除：${file}`);
        }
    }
    
    console.log(`✅ 保留 ${Math.min(backups.length, keepCount)} 個備份`);
}

// 3. 檢查知識完整性
function checkIntegrity() {
    console.log('🔍 檢查知識完整性');
    console.log('='.repeat(60));
    
    const report = {
        raw_files: [],
        wiki_files: [],
        genes: [],
        issues: []
    };
    
    // 檢查 raw 目錄
    if (fs.existsSync(path.join(WIKI_ROOT, 'raw'))) {
        report.raw_files = fs.readdirSync(path.join(WIKI_ROOT, 'raw'))
            .filter(f => f.endsWith('.md'));
        console.log(`\n📁 raw/: ${report.raw_files.length} 個文件`);
    }
    
    // 檢查 wiki 目錄
    if (fs.existsSync(path.join(WIKI_ROOT, 'wiki'))) {
        report.wiki_files = fs.readdirSync(path.join(WIKI_ROOT, 'wiki'))
            .filter(f => f.endsWith('.md'));
        console.log(`📁 wiki/: ${report.wiki_files.length} 個文件`);
    }
    
    // 檢查 Gene 文件
    const geneFiles = fs.readdirSync(GENES_DIR)
        .filter(f => f.startsWith('gene_') && f.endsWith('.json'));
    report.genes = geneFiles;
    console.log(`📁 genes: ${geneFiles.length} 個文件`);
    
    // 檢查問題
    if (report.raw_files.length === 0) {
        report.issues.push('⚠️  raw 目錄為空');
    }
    if (report.wiki_files.length === 0) {
        report.issues.push('⚠️  wiki 目錄為空');
    }
    
    // 檢查 index.md
    const indexPath = path.join(WIKI_ROOT, 'index.md');
    if (!fs.existsSync(indexPath)) {
        report.issues.push('⚠️  index.md 不存在');
    }
    
    console.log('\n📋 問題報告:');
    if (report.issues.length === 0) {
        console.log('   ✅ 無問題');
    } else {
        report.issues.forEach(issue => console.log(`   ${issue}`));
    }
    
    return report;
}

// 4. 避免知識衰變 - 定期刷新
function refreshKnowledge() {
    console.log('🔄 刷新知識（避免衰變）');
    console.log('='.repeat(60));
    
    // 讀取 log.md
    const logPath = path.join(WIKI_ROOT, 'log.md');
    let logContent = '';
    if (fs.existsSync(logPath)) {
        logContent = fs.readFileSync(logPath, 'utf8');
    }
    
    // 添加刷新記錄
    const newEntry = `\n## ${new Date().toISOString()}\n- 定期知識刷新\n- 檢查完整性\n- 備份知識庫\n`;
    
    fs.appendFileSync(logPath, newEntry);
    console.log('✅ 更新 log.md');
    
    // 觸發完整性檢查
    checkIntegrity();
    
    // 觸發備份
    backup({ compress: false });
}

// 主函數
function main() {
    const command = process.argv[2] || 'status';
    
    switch (command) {
        case 'backup':
            backup();
            break;
        case 'cleanup':
            cleanupBackups(5);
            break;
        case 'check':
            checkIntegrity();
            break;
        case 'refresh':
            refreshKnowledge();
            break;
        case 'all':
            console.log('🚀 執行完整維護流程\n');
            checkIntegrity();
            console.log('');
            backup();
            console.log('');
            cleanupBackups(5);
            console.log('');
            refreshKnowledge();
            break;
        default:
            console.log('LLM-Wiki 維護腳本');
            console.log('用法：node wiki-maintenance.js <command>');
            console.log('\n命令:');
            console.log('  backup   - 備份知識庫');
            console.log('  cleanup  - 清理舊備份');
            console.log('  check    - 檢查完整性');
            console.log('  refresh  - 刷新知識');
            console.log('  all      - 執行完整流程');
    }
}

main();
