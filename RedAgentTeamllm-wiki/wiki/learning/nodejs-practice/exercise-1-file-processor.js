#!/usr/bin/env node
/**
 * 練習 1: 文件批處理工具
 * 功能：批量處理指定目錄下的文件
 */

const fs = require('fs').promises;
const path = require('path');

class FileProcessor {
  constructor(directory) {
    this.directory = directory;
  }
  
  // 獲取所有文件
  async getFiles(extension = null) {
    try {
      const files = await fs.readdir(this.directory);
      
      if (extension) {
        return files.filter(f => f.endsWith(extension));
      }
      
      return files;
    } catch (err) {
      console.error(`讀取目錄失敗：${err.message}`);
      throw err;
    }
  }
  
  // 批量讀取
  async readAll(extension = null) {
    const files = await this.getFiles(extension);
    
    const results = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        try {
          const content = await fs.readFile(filePath, 'utf8');
          return { file, content };
        } catch (err) {
          console.error(`讀取文件 ${file} 失敗：${err.message}`);
          return { file, error: err.message };
        }
      })
    );
    
    return results;
  }
  
  // 批量統計
  async getStats(extension = null) {
    const files = await this.getFiles(extension);
    
    const stats = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        try {
          const fileStats = await fs.stat(filePath);
          const content = await fs.readFile(filePath, 'utf8');
          
          return {
            file,
            size: fileStats.size,
            lines: content.split('\n').length,
            words: content.split(/\s+/).length,
            created: fileStats.birthtime,
            modified: fileStats.mtime
          };
        } catch (err) {
          console.error(`統計文件 ${file} 失敗：${err.message}`);
          return { file, error: err.message };
        }
      })
    );
    
    return stats;
  }
  
  // 批量替換
  async replaceAll(searchStr, replaceStr, extension = null) {
    const files = await this.getFiles(extension);
    
    const results = await Promise.all(
      files.map(async (file) => {
        const filePath = path.join(this.directory, file);
        try {
          let content = await fs.readFile(filePath, 'utf8');
          const originalLength = content.length;
          content = content.replace(new RegExp(searchStr, 'g'), replaceStr);
          
          if (originalLength !== content.length) {
            await fs.writeFile(filePath, content, 'utf8');
            return { file, changed: true };
          }
          
          return { file, changed: false };
        } catch (err) {
          console.error(`處理文件 ${file} 失敗：${err.message}`);
          return { file, error: err.message };
        }
      })
    );
    
    const changedCount = results.filter(r => r.changed).length;
    console.log(`✅ 修改了 ${changedCount} 個文件`);
    
    return results;
  }
  
  // 生成報告
  async generateReport(extension = null) {
    const stats = await this.getStats(extension);
    
    const validStats = stats.filter(s => !s.error);
    
    if (validStats.length === 0) {
      console.log('⚠️  沒有找到有效的文件');
      return null;
    }
    
    const totalSize = validStats.reduce((sum, s) => sum + s.size, 0);
    const totalLines = validStats.reduce((sum, s) => sum + s.lines, 0);
    const totalWords = validStats.reduce((sum, s) => sum + s.words, 0);
    
    const report = `
╔════════════════════════════════════════╗
║        文件統計報告                     ║
╠════════════════════════════════════════╣
║ 文件總數：${String(validStats.length).padEnd(28)}║
║ 總大小：${(totalSize / 1024).toFixed(2).padStart(7)} KB                  ║
║ 總行數：${String(totalLines).padEnd(28)}║
║ 總字數：${String(totalWords).padEnd(28)}║
╠════════════════════════════════════════╣
║ 文件詳情：                             ║
╚════════════════════════════════════════╝

${validStats.map(s => 
  `📄 ${s.file}`.padEnd(50) + 
  `${s.size} 字節`.padStart(10) + 
  ` | ${s.lines} 行`.padStart(8) + 
  ` | ${s.words} 字`.padStart(8)
).join('\n')}
`.trim();
    
    const reportPath = path.join(this.directory, 'report.txt');
    await fs.writeFile(reportPath, report, 'utf8');
    
    console.log(report);
    console.log(`\n📊 報告已保存到：${reportPath}`);
    
    return report;
  }
}

// CLI 界面
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
╔════════════════════════════════════════╗
║     文件批處理工具 v1.0                ║
╠════════════════════════════════════════╣
║ 用法：                                 ║
║   node exercise-1.js <命令> [選項]      ║
╠════════════════════════════════════════╣
║ 命令：                                 ║
║   list [ext]     - 列出文件             ║
║   stats [ext]    - 統計信息             ║
║   report [ext]   - 生成報告             ║
║   replace <old> <new> [ext] - 批量替換  ║
╚════════════════════════════════════════╝
    `);
    return;
  }
  
  const processor = new FileProcessor(process.cwd());
  
  try {
    switch (command) {
      case 'list':
        const files = await processor.getFiles(args[1]);
        console.log(`📁 找到 ${files.length} 個文件:`);
        files.forEach(f => console.log(`  - ${f}`));
        break;
        
      case 'stats':
        const stats = await processor.getStats(args[1]);
        console.log('📊 文件統計:');
        stats.forEach(s => {
          if (s.error) {
            console.log(`  ❌ ${s.file}: ${s.error}`);
          } else {
            console.log(`  📄 ${s.file}: ${s.size} 字節，${s.lines} 行，${s.words} 字`);
          }
        });
        break;
        
      case 'report':
        await processor.generateReport(args[1]);
        break;
        
      case 'replace':
        if (args.length < 4) {
          console.log('❌ 用法：node exercise-1.js replace <舊文本> <新文本> [擴展名]');
          return;
        }
        await processor.replaceAll(args[1], args[2], args[3]);
        break;
        
      default:
        console.log(`❌ 未知命令：${command}`);
    }
  } catch (err) {
    console.error(`❌ 錯誤：${err.message}`);
    process.exit(1);
  }
}

// 如果直接運行則執行 main
if (require.main === module) {
  main();
}

module.exports = FileProcessor;
