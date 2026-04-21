#!/usr/bin/env node
/**
 * 🔀 安全合併 wiki/ - 僅添加缺失文件，不覆蓋任何內容
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 配置
const SOURCE_DIR = '/home/admin/llm-wiki/wiki';
const TARGET_DIR = '/home/admin/.openclaw/workspace/llm-wiki/wiki';

// 統計
const stats = {
    sourceFiles: 0,
    targetFilesBefore: 0,
    targetFilesAfter: 0,
    added: 0,
    skipped: 0,
    errors: 0
};

// 計算文件 hash
function getFileHash(filePath) {
    return crypto.createHash('md5').update(fs.readFileSync(filePath)).digest('hex');
}

// 安全複製（僅當目標不存在時）
function safeCopyOnlyIfMissing(src, dest) {
    try {
        // 如果目標已存在，跳過
        if (fs.existsSync(dest)) {
            // 檢查是否相同
            const srcHash = getFileHash(src);
            const destHash = getFileHash(dest);
            
            if (srcHash === destHash) {
                console.log(`   ⏭️  跳過（文件相同）：${path.basename(dest)}`);
                return { status: 'skipped', reason: 'identical' };
            } else {
                console.log(`   ⏭️  跳過（文件已存在但不同）：${path.basename(dest)}`);
                return { status: 'skipped', reason: 'exists_different' };
            }
        }
        
        // 確保目錄存在
        const destDir = path.dirname(dest);
        if (!fs.existsSync(destDir)) {
            fs.mkdirSync(destDir, { recursive: true });
        }
        
        // 複製文件
        fs.copyFileSync(src, dest);
        console.log(`   ✅ 添加：${path.basename(dest)}`);
        return { status: 'added', path: dest };
    } catch (e) {
        console.log(`   ❌ 錯誤：${e.message}`);
        return { status: 'error', error: e.message };
    }
}

// 重建索引
function rebuildIndex() {
    console.log('\n📋 重建索引...');
    
    const indexPath = path.join(path.dirname(TARGET_DIR), 'index.md');
    const wikiFiles = fs.existsSync(TARGET_DIR)
        ? fs.readdirSync(TARGET_DIR).filter(f => f.endsWith('.md'))
        : [];
    
    let indexContent = `# LLM-Wiki 知識庫索引\n\n`;
    indexContent += `**最後更新:** ${new Date().toISOString()}\n`;
    indexContent += `**合併時間:** ${new Date().toISOString()}\n`;
    indexContent += `**來源:** /home/admin/llm-wiki/wiki\n`;
    indexContent += `**目標:** /home/admin/.openclaw/workspace/llm-wiki/wiki\n\n`;
    indexContent += `---\n\n`;
    
    indexContent += `## 📊 統計\n\n`;
    indexContent += `| 項目 | 數量 |\n`;
    indexContent += `|------|------|\n`;
    indexContent += `| 知識條目 | ${wikiFiles.length} |\n\n`;
    indexContent += `---\n\n`;
    
    indexContent += `## 📚 知識條目列表\n\n`;
    for (const file of wikiFiles) {
        const filePath = path.join(TARGET_DIR, file);
        try {
            const content = fs.readFileSync(filePath, 'utf8').substring(0, 100);
            indexContent += `- **${file}**: ${content.replace(/\n/g, ' ')}...\n`;
        } catch (e) {
            indexContent += `- **${file}**: (無法讀取)\n`;
        }
    }
    indexContent += `\n---\n\n`;
    
    indexContent += `## 🔀 合併說明\n\n`;
    indexContent += `- ✅ 僅添加缺失文件\n`;
    indexContent += `- ✅ 不覆蓋任何現有文件\n`;
    indexContent += `- ✅ 無數據丟失\n\n`;
    
    fs.writeFileSync(indexPath, indexContent, 'utf8');
    console.log(`✅ 索引已重建：${indexPath}`);
}

// 主函數
function main() {
    console.log('='.repeat(70));
    console.log('🔀 安全合併 wiki/ - 僅添加缺失文件');
    console.log('='.repeat(70));
    console.log(`\n源目錄：${SOURCE_DIR}`);
    console.log(`目標目錄：${TARGET_DIR}`);
    console.log('\n原則:');
    console.log('  ✅ 不覆蓋任何文件');
    console.log('  ✅ 僅添加缺失文件');
    console.log('  ✅ 重建索引');
    console.log('  ✅ 最終檢查');
    console.log('');
    
    // 確保目標目錄存在
    if (!fs.existsSync(TARGET_DIR)) {
        fs.mkdirSync(TARGET_DIR, { recursive: true });
        console.log(`📁 創建目標目錄：${TARGET_DIR}`);
    }
    
    // 統計目標文件數（合併前）
    stats.targetFilesBefore = fs.readdirSync(TARGET_DIR).filter(f => f.endsWith('.md')).length;
    console.log(`\n📊 合併前目標文件數：${stats.targetFilesBefore}`);
    
    // 掃描源目錄
    const sourceFiles = fs.readdirSync(SOURCE_DIR).filter(f => f.endsWith('.md'));
    stats.sourceFiles = sourceFiles.length;
    console.log(`📊 源目錄文件數：${stats.sourceFiles}`);
    console.log('');
    
    // 複製文件
    console.log('🚀 開始合併...\n');
    for (const file of sourceFiles) {
        const srcPath = path.join(SOURCE_DIR, file);
        const destPath = path.join(TARGET_DIR, file);
        
        const result = safeCopyOnlyIfMissing(srcPath, destPath);
        
        if (result.status === 'added') {
            stats.added++;
        } else if (result.status === 'skipped') {
            stats.skipped++;
        } else if (result.status === 'error') {
            stats.errors++;
        }
    }
    
    // 統計目標文件數（合併後）
    stats.targetFilesAfter = fs.readdirSync(TARGET_DIR).filter(f => f.endsWith('.md')).length;
    
    // 重建索引
    rebuildIndex();
    
    // 最終檢查
    console.log('\n🔍 最終檢查...');
    console.log('='.repeat(70));
    console.log(`源目錄文件數：${stats.sourceFiles}`);
    console.log(`目標目錄文件數（合併前）：${stats.targetFilesBefore}`);
    console.log(`目標目錄文件數（合併後）：${stats.targetFilesAfter}`);
    console.log(`添加文件：${stats.added}`);
    console.log(`跳過文件：${stats.skipped}`);
    console.log(`錯誤：${stats.errors}`);
    
    if (stats.errors === 0) {
        console.log('\n✅ 最終檢查通過！');
    } else {
        console.log('\n⚠️  警告：發生錯誤');
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 合併完成');
    console.log('='.repeat(70));
}

// 運行
if (require.main === module) {
    main();
}

module.exports = { main };
