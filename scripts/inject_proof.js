const { execSync } = require('child_process');
const fs = require('fs');

try {
    console.log('Running benchmarks to capture raw log proof...');
    const output = execSync('npm run benchmark', { cwd: 'd:/code/antigravity-self-learning', encoding: 'utf8' });

    // Strip ANSI color codes
    const cleanOutput = output.replace(/\x1B\[[0-9;]*[a-zA-Z]/g, '');

    const readmePath = 'd:/code/antigravity-self-learning/README.md';
    let readme = fs.readFileSync(readmePath, 'utf8');

    if (!readme.includes('### 🖥️ Raw Terminal Benchmark Output')) {
        const proofText = `\n### 🖥️ Raw Terminal Benchmark Output (Proof)\n\`\`\`console\n$ npm run benchmark\n\n${cleanOutput.trim()}\n\`\`\`\n`;
        readme = readme.replace('## 🤝 Contribution & License', proofText + '\n## 🤝 Contribution & License');
        fs.writeFileSync(readmePath, readme);
        console.log('Successfully injected terminal proof to README.md');
    } else {
        console.log('Proof already exists in README');
    }
} catch (e) {
    console.error('Failed:', e.message);
}
