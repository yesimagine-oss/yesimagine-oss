#!/usr/bin/env node
/**
 * 🔄 將 95 個 Gene 文件移動到正確位置
 * 源：/home/admin/llm-wiki/wiki/new/
 * 目標：/home/admin/.openclaw/workspace/
 */

const fs = require('fs');
const path = require('path');

const SOURCE_DIR = '/home/admin/llm-wiki/wiki/new';
const TARGET_DIR = '/home/admin/.openclaw/workspace';

// 統計
const stats = {
    total: 0,
    moved: 0,
    skipped: 0,
    errors: 0
};

// 安全移動文件
function safeMove(src, dest) {
    try {
        // 如果目標已存在，檢查是否相同
        if (fs.existsSync(dest)) {
            const srcContent = fs.readFileSync(src, 'utf8');
            const destContent = fs.readFileSync(dest, 'utf8');
            
            if (srcContent === destContent) {
                console.log(`   ⏭️  跳過（文件已存在且相同）：${path.basename(dest)}`);
                return { status: 'skipped', reason: 'identical' };
            } else {
                // 文件不同，創建新版本
                const baseName = path.basename(dest, '.json');
                const newDest = path.join(path.dirname(dest), `${baseName}_duplicate_${Date.now()}.json`);
                fs.copyFileSync(src, dest);
                console.log(`   ✅ 覆蓋並保存舊版本：${path.basename(dest)} → ${path.basename(newDest)}`);
                return { status: 'moved', path: dest, backup: newDest };
            }
        }
        
        // 直接移動
        fs.copyFileSync(src, dest);
        fs.unlinkSync(src);
        console.log(`   ✅ 移動：${path.basename(src)}`);
        return { status: 'moved', path: dest };
    } catch (e) {
        console.log(`   ❌ 錯誤：${e.message}`);
        return { status: 'error', error: e.message };
    }
}

// 主函數
function main() {
    console.log('='.repeat(70));
    console.log('🔄 移動 95 個 Gene 文件到正確位置');
    console.log('='.repeat(70));
    console.log(`\n源目錄：${SOURCE_DIR}`);
    console.log(`目標目錄：${TARGET_DIR}`);
    console.log('');
    
    // 確保源目錄存在
    if (!fs.existsSync(SOURCE_DIR)) {
        console.log(`❌ 源目錄不存在：${SOURCE_DIR}`);
        return;
    }
    
    // 確保目標目錄存在
    if (!fs.existsSync(TARGET_DIR)) {
        fs.mkdirSync(TARGET_DIR, { recursive: true });
        console.log(`📁 創建目標目錄：${TARGET_DIR}`);
    }
    
    // 獲取所有 JSON 文件
    const files = fs.readdirSync(SOURCE_DIR).filter(f => f.endsWith('.json'));
    stats.total = files.length;
    
    console.log(`📊 找到 ${stats.total} 個 Gene 文件\n`);
    console.log('🚀 開始移動...\n');
    
    // 移動文件
    for (const file of files) {
        const srcPath = path.join(SOURCE_DIR, file);
        const destPath = path.join(TARGET_DIR, file);
        
        const result = safeMove(srcPath, destPath);
        
        if (result.status === 'moved') {
            stats.moved++;
        } else if (result.status === 'skipped') {
            stats.skipped++;
        } else if (result.status === 'error') {
            stats.errors++;
        }
    }
    
    // 清理空目錄
    try {
        const remainingFiles = fs.readdirSync(SOURCE_DIR);
        if (remainingFiles.length === 0) {
            fs.rmdirSync(SOURCE_DIR);
            console.log(`\n🗑️  清理空目錄：${SOURCE_DIR}`);
        } else {
            console.log(`\n⚠️  源目錄還有 ${remainingFiles.length} 個文件`);
        }
    } catch (e) {
        console.log(`\n⚠️  無法清理源目錄：${e.message}`);
    }
    
    // 最終統計
    console.log('\n' + '='.repeat(70));
    console.log('📊 最終統計');
    console.log('='.repeat(70));
    console.log(`總文件數：${stats.total}`);
    console.log(`成功移動：${stats.moved}`);
    console.log(`跳過：${stats.skipped}`);
    console.log(`錯誤：${stats.errors}`);
    
    if (stats.errors === 0) {
        console.log('\n✅ 所有文件已成功移動！');
    } else {
        console.log('\n⚠️  有錯誤發生，請檢查');
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ 移動完成');
    console.log('='.repeat(70));
}

// 運行
if (require.main === module) {
    main();
}

module.exports = { main };
