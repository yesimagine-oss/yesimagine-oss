#!/usr/bin/env node
/**
 * 🧪 Content Collector 測試用例
 */

const { ContentCollector } = require('../index');

async function test() {
    console.log('🧪 開始測試 Content Collector...\n');
    
    // 測試 URL（微信文章）
    const testUrl = 'https://mp.weixin.qq.com/s/xxx';
    
    console.log('📎 測試 URL:', testUrl);
    console.log('⏳ 抓取中...\n');
    
    const collector = new ContentCollector({
        browser: {
            headless: true
        }
    });
    
    const result = await collector.collect(testUrl);
    
    if (result.success) {
        console.log('✅ 抓取成功！');
        console.log('📄 標題:', result.title);
        console.log('📁 位置:', result.file_path);
        console.log('🖼️  圖片:', result.images_count, '張');
        if (result.related_projects.length > 0) {
            console.log('🎯 關聯項目:', result.related_projects.join(', '));
        }
        console.log('\n📝 內容預覽:');
        console.log('（查看保存的文件）');
    } else {
        console.error('❌ 抓取失敗:', result.message);
    }
}

// 如果直接運行
if (require.main === module) {
    test().catch(console.error);
}

module.exports = { test };
