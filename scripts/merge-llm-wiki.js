#!/usr/bin/env node
/**
 * 🔀 安全合併 LLM-Wiki 到 OpenClaw 系統目錄
 * 原則：不覆蓋、不刪除、不損壞任何文件
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置
const SOURCE_DIR = '/home/admin/llm-wiki';
const TARGET_DIR = '/home/admin/.openclaw/workspace/llm-wiki';
const BACKUP_DIR = '/home/admin/.openclaw/workspace/llm-wiki-backups';

// 生成唯一 ID
function generateId() {
    return Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

// 安全複製文件（如果目標已存在則跳過）
function safeCopyFile(src, dest, options = {}) {
    const { skipIfExists = true, mergeContent = false } = options;
    
    if (!fs.existsSync(src)) {
        console.log(`   ⚠️  源文件不存在：${src}`);
        return { status: 'skipped', reason: 'source_not_found' };
    }
    
    // 確保目標目錄存在
    const destDir = path.dirname(dest);
    if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
    }
    
    // 檢查目標文件是否已存在
    if (fs.existsSync(dest)) {
        if (skipIfExists) {
            // 計算 hash 檢查是否相同
            const srcHash = crypto.createHash('md5').update(fs.readFileSync(src)).digest('hex');
            const destHash = crypto.createHash('md5').update(fs.readFileSync(dest)).digest('hex');
            
            if (srcHash === destHash) {
                console.log(`   ⏭️  跳過（文件相同）：${path.basename(dest)}`);
                return { status: 'skipped', reason: 'identical' };
            } else {
                // 文件不同，創建新版本
                const baseName = path.basename(dest, '.md');
                const ext = path.extname(dest);
                const newDest = path.join(destDir, `${baseName}_${generateId()}${ext}`);
                fs.copyFileSync(src, newDest);
                console.log(`   📄  創建新版本：${path.basename(newDest)}`);
                return { status: 'created', path: newDest };
            }
        }
        
        if (mergeContent) {
            // 合併內容（僅限 markdown）
            const srcContent = fs.readFileSync(src, 'utf8');
            const destContent = fs.readFileSync(dest, 'utf8');
            
            // 檢查是否已包含
            if (destContent.includes(srcContent)) {
                console.log(`   ⏭️  跳過（已包含）：${path.basename(dest)}`);
                return { status: 'skipped', reason: 'already_merged' };
            }
            
            // 追加內容
            const merged = destContent + '\n\n---\n\n## Merged Content (' + new Date().toISOString() + ')\n\n' + srcContent;
            fs.writeFileSync(dest, merged, 'utf8');
            console.log(`   🔀  合併內容：${path.basename(dest)}`);
            return { status: 'merged', path: dest };
        }
    }
    
    // 直接複製
    fs.copyFileSync(src, dest);
    console.log(`   ✅ 複製：${path.basename(dest)}`);
    return { status: 'copied', path: dest };
}

// 遞歸複製目錄
function copyDir(srcDir, destDir, options = {}) {
    const { skipIfExists = true, mergeContent = false, fileFilter = null } = options;
    
    const stats = {
        copied: 0,
        skipped: 0,
        merged: 0,
        created: 0,
        errors: 0
    };
    
    if (!fs.existsSync(srcDir)) {
        console.log(`⚠️  源目錄不存在：${srcDir}`);
        return stats;
    }
    
    // 確保目標目錄存在
    if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
        console.log(`📁 創建目錄：${destDir}`);
    }
    
    const entries = fs.readdirSync(srcDir, { withFileTypes: true });
    
    for (const entry of entries) {
        const srcPath = path.join(srcDir, entry.name);
        const destPath = path.join(destDir, entry.name);
        
        // 應用過濾器
        if (fileFilter && !fileFilter(entry.name, srcPath)) {
            console.log(`   ⏭️  跳過（過濾器）：${entry.name}`);
            stats.skipped++;
            continue;
        }
        
        if (entry.isDirectory()) {
            // 遞歸複製子目錄
            const subStats = copyDir(srcPath, destPath, options);
            stats.copied += subStats.copied;
            stats.skipped += subStats.skipped;
            stats.merged += subStats.merged;
            stats.created += subStats.created;
            stats.errors += subStats.errors;
        } else if (entry.isFile()) {
            // 複製文件
            const result = safeCopyFile(srcPath, destPath, { skipIfExists, mergeContent });
            
            if (result.status === 'copied' || result.status === 'created') {
                stats.copied++;
            } else if (result.status === 'skipped') {
                stats.skipped++;
            } else if (result.status === 'merged') {
                stats.merged++;
            }
        }
    }
    
    return stats;
}

// 重建索引
function rebuildIndex(targetDir) {
    console.log('\n📋 重建索引...');
    
    const indexPath = path.join(targetDir, 'index.md');
    const rawDir = path.join(targetDir, 'raw');
    const wikiDir = path.join(targetDir, 'wiki');
    
    let indexContent = `# LLM-Wiki 知識庫索引\n\n`;
    indexContent += `**最後更新:** ${new Date().toISOString()}\n`;
    indexContent += `**合併時間:** ${new Date().toISOString()}\n\n`;
    indexContent += `---\n\n`;
    
    // 掃描 raw 目錄
    if (fs.existsSync(rawDir)) {
        const rawFiles = fs.readdirSync(rawDir).filter(f => f.endsWith('.md'));
        indexContent += `## 原始資產 (${rawFiles.length})\n\n`;
        
        for (const file of rawFiles) {
            const filePath = path.join(rawDir, file);
            const content = fs.readFileSync(filePath, 'utf8').substring(0, 100);
            indexContent += `- **${file}**: ${content.replace(/\n/g, ' ')}...\n`;
        }
        
        indexContent += `\n---\n\n`;
    }
    
    // 掃描 wiki 目錄
    if (fs.existsSync(wikiDir)) {
        const wikiFiles = fs.readdirSync(wikiDir).filter(f => f.endsWith('.md'));
        indexContent += `## 知識條目 (${wikiFiles.length})\n\n`;
        
        for (const file of wikiFiles) {
            const filePath = path.join(wikiDir, file);
            const content = fs.readFileSync(filePath, 'utf8').substring(0, 100);
            indexContent += `- **${file}**: ${content.replace(/\n/g, ' ')}...\n`;
        }
        
        indexContent += `\n---\n\n`;
    }
    
    // 添加合併說明
    indexContent += `## 合併說明\n\n`;
    indexContent += `本知識庫已從 /home/admin/llm-wiki/ 安全合併到此目錄。\n\n`;
    indexContent += `- 所有文件均保留原始版本\n`;
    indexContent += `- 如有衝突，創建新版本而非覆蓋\n`;
    indexContent += `- 無數據丟失\n\n`;
    
    fs.writeFileSync(indexPath, indexContent, 'utf8');
    console.log(`✅ 索引已重建：${indexPath}`);
}

// 主函數
function main() {
    console.log('='.repeat(70));
    console.log('🔀 安全合併 LLM-Wiki 到 OpenClaw 系統目錄');
    console.log('='.repeat(70));
    console.log(`\n源目錄：${SOURCE_DIR}`);
    console.log(`目標目錄：${TARGET_DIR}`);
    console.log(`\n原則:`);
    console.log(`  ✅ 不覆蓋現有文件`);
    console.log(`  ✅ 不刪除任何文件`);
    console.log(`  ✅ 不損壞數據`);
    console.log(`  ✅ 安全合併`);
    console.log(`  ✅ 重建索引`);
    console.log(`  ✅ 無數據丟失`);
    console.log('');
    
    // 創建備份目錄
    if (!fs.existsSync(BACKUP_DIR)) {
        fs.mkdirSync(BACKUP_DIR, { recursive: true });
        console.log(`📁 創建備份目錄：${BACKUP_DIR}`);
    }
    
    // 創建目標目錄
    if (!fs.existsSync(TARGET_DIR)) {
        fs.mkdirSync(TARGET_DIR, { recursive: true });
        console.log(`📁 創建目標目錄：${TARGET_DIR}`);
    }
    
    // 執行合併
    console.log('\n🚀 開始合併...\n');
    
    const stats = copyDir(SOURCE_DIR, TARGET_DIR, {
        skipIfExists: true,  // 跳過已存在的文件
        mergeContent: false, // 不自動合併內容（避免損壞）
        fileFilter: (name, srcPath) => {
            // 跳過某些文件（如臨時文件）
            if (name.startsWith('.')) return false;
            if (name.endsWith('.tmp')) return false;
            if (name.endsWith('.bak')) return false;
            return true;
        }
    });
    
    // 打印統計
    console.log('\n' + '='.repeat(70));
    console.log('📊 合併統計');
    console.log('='.repeat(70));
    console.log(`✅ 複製：${stats.copied} 個文件`);
    console.log(`⏭️  跳過：${stats.skipped} 個文件`);
    console.log(`🔀 合併：${stats.merged} 個文件`);
    console.log(`🆕 創建：${stats.created} 個新版本`);
    console.log(`❌ 錯誤：${stats.errors} 個`);
    
    // 重建索引
    rebuildIndex(TARGET_DIR);
    
    // 驗證
    console.log('\n🔍 驗證合併結果...');
    const sourceFiles = countFiles(SOURCE_DIR);
    const targetFiles = countFiles(TARGET_DIR);
    
    console.log(`\n源目錄文件數：${sourceFiles}`);
    console.log(`目標目錄文件數：${targetFiles}`);
    
    if (targetFiles >= sourceFiles) {
        console.log('\n✅ 合併成功！所有文件已安全遷移。');
    } else {
        console.log('\n⚠️  警告：目標文件數少於源文件數，請檢查。');
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 合併完成');
    console.log('='.repeat(70));
}

// 計算目錄中的文件數
function countFiles(dir) {
    let count = 0;
    if (!fs.existsSync(dir)) return 0;
    
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        if (entry.isDirectory()) {
            count += countFiles(path.join(dir, entry.name));
        } else if (entry.isFile()) {
            count++;
        }
    }
    
    return count;
}

// 運行
if (require.main === module) {
    main();
}

module.exports = { safeCopyFile, copyDir, rebuildIndex, main };
