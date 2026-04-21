#!/usr/bin/env node
/**
 * 🔍 檢查 index.md 中的技能名稱與實際文件
 */

const fs = require('fs');
const path = require('path');

const INDEX_PATH = '/home/admin/llm-wiki/index.md';
const SKILLS_DIR = '/home/admin/.openclaw/workspace/skills';
const GENES_DIR = '/home/admin/.openclaw/workspace';

// 解析 index.md 中的技能名稱
function parseSkillNames(content) {
    const skills = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
        // 匹配 - skill-name 格式
        const match = line.match(/^\s*-\s+([a-z0-9-]+)/i);
        if (match) {
            skills.push(match[1].toLowerCase());
        }
    }
    
    return skills;
}

// 檢查 Skills 目錄
function checkSkillsDir(skillNames) {
    const results = {
        found: [],
        missing: []
    };
    
    if (!fs.existsSync(SKILLS_DIR)) {
        console.log(`⚠️  Skills 目錄不存在：${SKILLS_DIR}`);
        return results;
    }
    
    const skillDirs = fs.readdirSync(SKILLS_DIR);
    
    for (const skill of skillNames) {
        // 檢查是否有匹配的目錄
        const match = skillDirs.find(dir => 
            dir.toLowerCase().includes(skill) || 
            skill.includes(dir.toLowerCase())
        );
        
        if (match) {
            results.found.push({
                skill,
                path: path.join(SKILLS_DIR, match),
                hasSkillMd: fs.existsSync(path.join(SKILLS_DIR, match, 'SKILL.md'))
            });
        } else {
            results.missing.push(skill);
        }
    }
    
    return results;
}

// 檢查 Gene 文件
function checkGeneFiles(skillNames) {
    const results = {
        found: [],
        missing: []
    };
    
    const geneFiles = fs.readdirSync(GENES_DIR)
        .filter(f => f.startsWith('gene_') && f.endsWith('.json'));
    
    for (const skill of skillNames) {
        const match = geneFiles.find(f => 
            f.toLowerCase().includes(skill)
        );
        
        if (match) {
            results.found.push({
                skill,
                path: path.join(GENES_DIR, match)
            });
        }
    }
    
    return results;
}

// 主函數
function main() {
    console.log('='.repeat(70));
    console.log('🔍 檢查 index.md 技能名稱與實際文件');
    console.log('='.repeat(70));
    
    // 讀取 index.md
    const content = fs.readFileSync(INDEX_PATH, 'utf8');
    const skillNames = parseSkillNames(content);
    
    console.log(`\n📋 從 index.md 解析出 ${skillNames.length} 個技能名稱`);
    console.log('');
    
    // 檢查 Skills 目錄
    console.log('📂 檢查 Skills 目錄...');
    const skillsResults = checkSkillsDir(skillNames);
    console.log(`   找到：${skillsResults.found.length}`);
    console.log(`   缺失：${skillsResults.missing.length}`);
    
    // 檢查 Gene 文件
    console.log('\n📂 檢查 Gene 文件...');
    const geneResults = checkGeneFiles(skillNames);
    console.log(`   找到：${geneResults.found.length}`);
    
    // 打印找到的技能
    console.log('\n✅ 找到的技能 (Skills 目錄):');
    skillsResults.found.slice(0, 20).forEach(item => {
        console.log(`   - ${item.skill} → ${path.basename(item.path)} ${item.hasSkillMd ? '✅' : '⚠️'}`);
    });
    
    // 打印缺失的技能
    console.log('\n❌ 缺失的技能 (不在 Skills 目錄):');
    skillsResults.missing.slice(0, 50).forEach(skill => {
        console.log(`   - ${skill}`);
    });
    
    if (skillsResults.missing.length > 50) {
        console.log(`   ... 還有 ${skillsResults.missing.length - 50} 個`);
    }
    
    // 總結
    console.log('\n' + '='.repeat(70));
    console.log('📊 總結');
    console.log('='.repeat(70));
    console.log(`index.md 技能名稱總數：${skillNames.length}`);
    console.log(`Skills 目錄中找到：${skillsResults.found.length} (${Math.round(skillsResults.found.length / skillNames.length * 100)}%)`);
    console.log(`Skills 目錄中缺失：${skillsResults.missing.length} (${Math.round(skillsResults.missing.length / skillNames.length * 100)}%)`);
    console.log(`Gene 文件中找到：${geneResults.found.length}`);
    
    // 生成報告
    const report = {
        timestamp: new Date().toISOString(),
        indexSkillCount: skillNames.length,
        skillsFound: skillsResults.found.length,
        skillsMissing: skillsResults.missing.length,
        genesFound: geneResults.found.length,
        missingSkills: skillsResults.missing
    };
    
    const reportPath = '/home/admin/.openclaw/workspace/llm-wiki/skill-existence-report.json';
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\n📄 報告已保存：${reportPath}`);
}

main();
