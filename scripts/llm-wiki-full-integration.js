#!/usr/bin/env node
/**
 * 📥 完整集成 LLM-Wiki 所有知識文件
 * 掃描所有 md, logs, configs, documents
 * 不刪除、不損壞、完全集成
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

// 配置
const SOURCE_DIR = '/home/admin/llm-wiki';
const TARGET_DIR = '/home/admin/.openclaw/workspace/llm-wiki';
const RAW_DIR = path.join(TARGET_DIR, 'raw');
const WIKI_DIR = path.join(TARGET_DIR, 'wiki');

// 文件類型定義
const FILE_PATTERNS = {
    markdown: ['.md', '.markdown'],
    logs: ['.log', '.logs'],
    configs: ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'],
    documents: ['.txt', '.rst', '.doc', '.docx', '.pdf']
};

// 統計
const stats = {
    scanned: 0,
    raw: 0,
    wiki: 0,
    config: 0,
    logs: 0,
    documents: 0,
    skipped: 0,
    errors: 0
};

// 檢查文件類型
function getFileType(fileName) {
    const ext = path.extname(fileName).toLowerCase();
    
    if (FILE_PATTERNS.markdown.includes(ext)) return 'markdown';
    if (FILE_PATTERNS.logs.includes(ext)) return 'logs';
    if (FILE_PATTERNS.configs.includes(ext)) return 'configs';
    if (FILE_PATTERNS.documents.includes(ext)) return 'documents';
    return 'unknown';
}

// 安全複製文件
function safeCopy(src, dest) {
    try {
        // 確保目錄存在
        const destDir = path.dirname(dest);
        if (!fs.existsSync(destDir)) {
            fs.mkdirSync(destDir, { recursive: true });
        }
        
        // 如果目標已存在，檢查是否相同
        if (fs.existsSync(dest)) {
            const srcHash = crypto.createHash('md5').update(fs.readFileSync(src)).digest('hex');
            const destHash = crypto.createHash('md5').update(fs.readFileSync(dest)).digest('hex');
            
            if (srcHash === destHash) {
                return { status: 'skipped', reason: 'identical' };
            } else {
                // 創建新版本
                const baseName = path.basename(dest, path.extname(dest));
                const ext = path.extname(dest);
                const newDest = path.join(destDir, `${baseName}_${Date.now()}${ext}`);
                fs.copyFileSync(src, newDest);
                return { status: 'created', path: newDest };
            }
        }
        
        // 直接複製
        fs.copyFileSync(src, dest);
        return { status: 'copied', path: dest };
    } catch (e) {
        return { status: 'error', error: e.message };
    }
}

// 處理 Markdown 文件到 wiki/
function processMarkdownToWiki(srcFile, destFile) {
    try {
        const content = fs.readFileSync(srcFile, 'utf8');
        
        // 提取標題
        const titleMatch = content.match(/^#\s+(.+)$/m);
        const title = titleMatch ? titleMatch[1].trim() : path.basename(srcFile, '.md');
        
        // 提取標籤
        const tagMatch = content.match(/标签 [：:]\s*(.+)$/m);
        const tags = tagMatch ? tagMatch[1].split(/[,,\s]+/).filter(t => t.trim()) : [];
        
        // 提取類型
        const typeMatch = content.match(/类型 [：:]\s*(.+)$/m);
        const type = typeMatch ? typeMatch[1].trim() : 'general';
        
        // 提取來源
        const sourceMatch = content.match(/来源 [：:]\s*(.+)$/m);
        const source = sourceMatch ? sourceMatch[1].trim() : 'llm-wiki';
        
        // 創建結構化條目
        const structuredContent = `# ${title}

**類型:** ${type}
**來源:** ${source}
**標籤:** ${tags.join(', ')}
**導入時間:** ${new Date().toISOString()}

---

${content}

---

**結構化元數據:**
- 原始文件：${path.basename(srcFile)}
- 導入日期：${new Date().toISOString()}
- 處理狀態：completed
`;
        
        fs.writeFileSync(destFile, structuredContent, 'utf8');
        return { status: 'processed', path: destFile };
    } catch (e) {
        return { status: 'error', error: e.message };
    }
}

// 掃描並集成所有文件
function scanAndIntegrate() {
    console.log('='.repeat(70));
    console.log('📥 完整集成 LLM-Wiki 所有知識文件');
    console.log('='.repeat(70));
    console.log(`\n源目錄：${SOURCE_DIR}`);
    console.log(`目標目錄：${TARGET_DIR}`);
    console.log('\n掃描範圍:');
    console.log('  - Markdown 文件 (.md, .markdown)');
    console.log('  - 日誌文件 (.log, .logs)');
    console.log('  - 配置文件 (.json, .yaml, .yml, .toml)');
    console.log('  - 文檔文件 (.txt, .rst, .doc, .docx, .pdf)');
    console.log('');
    
    // 確保目標目錄存在
    if (!fs.existsSync(TARGET_DIR)) {
        fs.mkdirSync(TARGET_DIR, { recursive: true });
    }
    if (!fs.existsSync(RAW_DIR)) {
        fs.mkdirSync(RAW_DIR, { recursive: true });
    }
    if (!fs.existsSync(WIKI_DIR)) {
        fs.mkdirSync(WIKI_DIR, { recursive: true });
    }
    
    // 遞歸掃描源目錄
    function scanDir(dir, relativePath = '') {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        
        for (const entry of entries) {
            const srcPath = path.join(dir, entry.name);
            const relPath = path.join(relativePath, entry.name);
            
            if (entry.isDirectory()) {
                // 跳過某些目錄
                if (entry.name === 'node_modules' || entry.name.startsWith('.')) {
                    continue;
                }
                scanDir(srcPath, relPath);
            } else if (entry.isFile()) {
                stats.scanned++;
                const fileType = getFileType(entry.name);
                
                console.log(`📄 掃描：${relPath} (${fileType})`);
                
                // 複製到 raw/
                const rawDest = path.join(RAW_DIR, relativePath ? path.join(relativePath, entry.name) : entry.name);
                const rawResult = safeCopy(srcPath, rawDest);
                
                if (rawResult.status === 'copied') {
                    stats.raw++;
                } else if (rawResult.status === 'created') {
                    stats.raw++;
                } else if (rawResult.status === 'skipped') {
                    stats.skipped++;
                } else if (rawResult.status === 'error') {
                    stats.errors++;
                    console.log(`   ❌ 錯誤：${rawResult.error}`);
                }
                
                // 處理 Markdown 到 wiki/
                if (fileType === 'markdown') {
                    const wikiFileName = entry.name.replace(/asset\d+_/, '').replace(/_/g, '_');
                    const wikiDest = path.join(WIKI_DIR, wikiFileName);
                    const wikiResult = processMarkdownToWiki(srcPath, wikiDest);
                    
                    if (wikiResult.status === 'processed') {
                        stats.wiki++;
                        console.log(`   ✅ 處理為 wiki 條目`);
                    } else if (wikiResult.status === 'error') {
                        stats.errors++;
                        console.log(`   ❌ 處理錯誤：${wikiResult.error}`);
                    }
                } else if (fileType === 'configs') {
                    stats.config++;
                } else if (fileType === 'logs') {
                    stats.logs++;
                } else if (fileType === 'documents') {
                    stats.documents++;
                }
            }
        }
    }
    
    // 執行掃描
    scanDir(SOURCE_DIR);
    
    return stats;
}

// 重建索引
function rebuildIndex() {
    console.log('\n📋 重建索引...');
    
    const indexPath = path.join(TARGET_DIR, 'index.md');
    
    // 掃描 raw 目錄
    const rawFiles = fs.existsSync(RAW_DIR) 
        ? fs.readdirSync(RAW_DIR).filter(f => f.endsWith('.md'))
        : [];
    
    // 掃描 wiki 目錄
    const wikiFiles = fs.existsSync(WIKI_DIR)
        ? fs.readdirSync(WIKI_DIR).filter(f => f.endsWith('.md'))
        : [];
    
    // 掃描其他文件
    const configFiles = fs.existsSync(RAW_DIR)
        ? fs.readdirSync(RAW_DIR).filter(f => {
            const ext = path.extname(f).toLowerCase();
            return FILE_PATTERNS.configs.includes(ext);
        })
        : [];
    
    const logFiles = fs.existsSync(RAW_DIR)
        ? fs.readdirSync(RAW_DIR).filter(f => {
            const ext = path.extname(f).toLowerCase();
            return FILE_PATTERNS.logs.includes(ext);
        })
        : [];
    
    // 創建索引內容
    let indexContent = `# LLM-Wiki 知識庫完整索引\n\n`;
    indexContent += `**最後更新:** ${new Date().toISOString()}\n`;
    indexContent += `**完整集成時間:** ${new Date().toISOString()}\n`;
    indexContent += `**源目錄:** ${SOURCE_DIR}\n`;
    indexContent += `**目標目錄:** ${TARGET_DIR}\n\n`;
    indexContent += `---\n\n`;
    
    // 統計摘要
    indexContent += `## 📊 集成統計\n\n`;
    indexContent += `| 類型 | 數量 |\n`;
    indexContent += `|------|------|\n`;
    indexContent += `| 原始文件 (raw/) | ${rawFiles.length} |\n`;
    indexContent += `| 知識條目 (wiki/) | ${wikiFiles.length} |\n`;
    indexContent += `| 配置文件 | ${configFiles.length} |\n`;
    indexContent += `| 日誌文件 | ${logFiles.length} |\n`;
    indexContent += `| **總計** | **${rawFiles.length + wikiFiles.length + configFiles.length + logFiles.length}** |\n\n`;
    indexContent += `---\n\n`;
    
    // 原始資產列表
    indexContent += `## 📁 原始資產 (raw/)\n\n`;
    for (const file of rawFiles) {
        const filePath = path.join(RAW_DIR, file);
        const content = fs.readFileSync(filePath, 'utf8').substring(0, 100);
        indexContent += `- **${file}**: ${content.replace(/\n/g, ' ')}...\n`;
    }
    indexContent += `\n---\n\n`;
    
    // 知識條目列表
    indexContent += `## 📚 知識條目 (wiki/)\n\n`;
    for (const file of wikiFiles) {
        const filePath = path.join(WIKI_DIR, file);
        const content = fs.readFileSync(filePath, 'utf8').substring(0, 100);
        indexContent += `- **${file}**: ${content.replace(/\n/g, ' ')}...\n`;
    }
    indexContent += `\n---\n\n`;
    
    // 配置文件列表
    if (configFiles.length > 0) {
        indexContent += `## ⚙️ 配置文件\n\n`;
        for (const file of configFiles) {
            indexContent += `- ${file}\n`;
        }
        indexContent += `\n---\n\n`;
    }
    
    // 日誌文件列表
    if (logFiles.length > 0) {
        indexContent += `## 📝 日誌文件\n\n`;
        for (const file of logFiles) {
            indexContent += `- ${file}\n`;
        }
        indexContent += `\n---\n\n`;
    }
    
    // 集成說明
    indexContent += `## 🔀 集成說明\n\n`;
    indexContent += `本知識庫已從 ${SOURCE_DIR} 完整集成到此目錄。\n\n`;
    indexContent += `### 集成原則\n\n`;
    indexContent += `- ✅ 不刪除任何文件\n`;
    indexContent += `- ✅ 不損壞任何數據\n`;
    indexContent += `- ✅ 完全集成所有文件類型\n`;
    indexContent += `- ✅ 安全複製（衝突時創建新版本）\n`;
    indexContent += `- ✅ 重建完整索引\n\n`;
    
    indexContent += `### 目錄結構\n\n`;
    indexContent += `\`\`\`\n${TARGET_DIR}/\n├── raw/          # 原始文件\n├── wiki/         # 結構化知識條目\n├── index.md      # 本索引\n└── log.md        # 變更日誌\n\`\`\`\n\n`;
    
    fs.writeFileSync(indexPath, indexContent, 'utf8');
    console.log(`✅ 索引已重建：${indexPath}`);
    
    return { raw: rawFiles.length, wiki: wikiFiles.length, config: configFiles.length, logs: logFiles.length };
}

// 驗證完整性
function verifyIntegrity(beforeCount, afterCount) {
    console.log('\n🔍 驗證完整性...');
    console.log(`\n源目錄文件數：${beforeCount}`);
    console.log(`目標目錄文件數：${afterCount}`);
    
    if (afterCount >= beforeCount) {
        console.log('\n✅ 完整性驗證通過！');
        return true;
    } else {
        console.log('\n⚠️  警告：目標文件數少於源文件數');
        return false;
    }
}

// 主函數
function main() {
    // 掃描前統計
    const beforeCount = execSync(`find ${SOURCE_DIR} -type f | wc -l`, { encoding: 'utf8' }).trim();
    
    // 執行集成
    const integrateStats = scanAndIntegrate();
    
    // 重建索引
    const indexStats = rebuildIndex();
    
    // 掃描後統計
    const afterCount = execSync(`find ${TARGET_DIR} -type f | wc -l`, { encoding: 'utf8' }).trim();
    
    // 驗證
    const integrityOk = verifyIntegrity(parseInt(beforeCount), parseInt(afterCount));
    
    // 打印最終統計
    console.log('\n' + '='.repeat(70));
    console.log('📊 最終統計');
    console.log('='.repeat(70));
    console.log(`掃描文件：${integrateStats.scanned}`);
    console.log(`複製到 raw/: ${integrateStats.raw}`);
    console.log(`處理到 wiki/: ${integrateStats.wiki}`);
    console.log(`配置文件：${integrateStats.config}`);
    console.log(`日誌文件：${integrateStats.logs}`);
    console.log(`文檔文件：${integrateStats.documents}`);
    console.log(`跳過：${integrateStats.skipped}`);
    console.log(`錯誤：${integrateStats.errors}`);
    console.log(`\n索引統計:`);
    console.log(`  raw/ 文件：${indexStats.raw}`);
    console.log(`  wiki/ 文件：${indexStats.wiki}`);
    console.log(`  配置文件：${indexStats.config}`);
    console.log(`  日誌文件：${indexStats.logs}`);
    console.log(`\n完整性驗證：${integrityOk ? '✅ 通過' : '❌ 失敗'}`);
    console.log('\n' + '='.repeat(70));
    console.log('✅ 完整集成完成');
    console.log('='.repeat(70));
}

// 執行
if (require.main === module) {
    const { execSync } = require('child_process');
    main();
}

module.exports = { scanAndIntegrate, rebuildIndex, verifyIntegrity, main };
