#!/usr/bin/env node
/**
 * 🔍 分析缺失內容
 */

const fs = require('fs');
const path = require('path');

// 讀取 index.md 技能名稱
const indexContent = fs.readFileSync('/home/admin/llm-wiki/index.md', 'utf8');
const skillNames = indexContent.match(/^\s*-\s+([a-z0-9-]+)/gim) || [];
const names = skillNames.map(s => s.match(/-\s+([a-z0-9-]+)/i)[1].toLowerCase());

// 獲取 Skills 目錄
const skillsDir = '/home/admin/.openclaw/workspace/skills';
const skillDirs = fs.readdirSync(skillsDir).filter(d => 
    fs.existsSync(path.join(skillsDir, d, 'SKILL.md'))
).map(d => d.toLowerCase());

// 獲取 Gene 文件
const genesDir = '/home/admin/.openclaw/workspace';
const geneFiles = fs.readdirSync(genesDir)
    .filter(f => f.startsWith('gene_') && f.endsWith('.json'))
    .map(f => f.replace('gene_distilled_', '').replace('_v1.json', '').toLowerCase());

// 檢查缺失
const missing = {
    skills: [],
    genes: [],
    both: []
};

for (const name of names) {
    const hasSkill = skillDirs.some(d => d.includes(name) || name.includes(d));
    const hasGene = geneFiles.some(g => g.includes(name) || name.includes(g));
    
    if (!hasSkill && !hasGene) {
        missing.both.push(name);
    } else if (!hasSkill) {
        missing.genes.push(name);
    } else if (!hasGene) {
        missing.skills.push(name);
    }
}

// 輸出報告
console.log('='.repeat(70));
console.log('🔍 缺失內容分析');
console.log('='.repeat(70));
console.log('');
console.log('index.md 技能名稱總數:', names.length);
console.log('Skills 目錄:', skillDirs.length);
console.log('Genes 文件:', geneFiles.length);
console.log('');
console.log('缺失統計:');
console.log('  既無 Skill 也無 Gene:', missing.both.length);
console.log('  有 Skill 無 Gene:', missing.skills.length);
console.log('  有 Gene 無 Skill:', missing.genes.length);
console.log('');

console.log('❌ 完全缺失 (既無 Skill 也無 Gene):');
missing.both.slice(0, 50).forEach(name => console.log(`  - ${name}`));
if (missing.both.length > 50) {
    console.log(`  ... 還有 ${missing.both.length - 50} 個`);
}
console.log('');

console.log('⚠️  有 Skill 無 Gene:');
missing.skills.slice(0, 20).forEach(name => console.log(`  - ${name}`));
console.log('');

console.log('⚠️  有 Gene 無 Skill:');
missing.genes.slice(0, 20).forEach(name => console.log(`  - ${name}`));
console.log('');

// 保存報告
const report = {
    timestamp: new Date().toISOString(),
    indexSkillCount: names.length,
    skillsCount: skillDirs.length,
    genesCount: geneFiles.length,
    missing: {
        both: missing.both,
        hasSkillNoGene: missing.skills,
        hasGeneNoSkill: missing.genes
    }
};

fs.writeFileSync(
    '/home/admin/.openclaw/workspace/llm-wiki/missing-analysis-report.json',
    JSON.stringify(report, null, 2)
);
console.log('📄 報告已保存：/home/admin/.openclaw/workspace/llm-wiki/missing-analysis-report.json');
