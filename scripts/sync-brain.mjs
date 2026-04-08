import fs from 'fs/promises';
import path from 'path';
import os from 'os';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

const HOME_DIR = os.homedir();
const SOURCE_MEMORY = path.join(HOME_DIR, '.gemini/antigravity/memory');
const SOURCE_SKILLS = path.join(HOME_DIR, '.gemini/antigravity/skills');

const DEST_MEMORY = path.resolve('./src/content/docs/memory');
const DEST_SKILLS = path.resolve('./src/content/docs/skills');

async function copyDir(src, dest) {
    try {
        await fs.access(src);
    } catch (err) {
        console.warn(`Source folder does not exist: ${src}`);
        return;
    }

    await fs.mkdir(dest, { recursive: true });
    const entries = await fs.readdir(src, { withFileTypes: true });

    for (let entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            await copyDir(srcPath, destPath);
        } else {
            // [UPDATE] STRICT ZERO-TRUST BLACKLIST (Rule #2)
            const isSecret = /credential|secret|key|password|token|env|auth|ftp|ssh/i.test(entry.name);

            if (isSecret) {
                console.log(`🛡️ [Zero-Trust Guard] Blocked sensitive file from public syncing: ${entry.name}`);
            } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
                let content = await fs.readFile(srcPath, 'utf8');
                const fallbackTitle = entry.name.replace('.mdx', '').replace('.md', '').replaceAll('_', ' ');

                if (!content.trimStart().startsWith('---')) {
                    content = `---\ntitle: "${fallbackTitle}"\n---\n\n` + content;
                } else if (!content.includes('title:')) {
                    // Chèn title vào dưới --- đầu tiên
                    content = content.replace('---', `---\ntitle: "${fallbackTitle}"`);
                }

                await fs.writeFile(destPath, content, 'utf8');
            } else {
                await fs.copyFile(srcPath, destPath);
            }
        }
    }
}

async function main() {
    console.log('🔄 Syncing Antigravity Core (Memory & Skills)...');

    // WIPE legacy stale files to prevent old secret leaks and Astro schema collisions
    await fs.rm(DEST_MEMORY, { recursive: true, force: true });
    await fs.rm(DEST_SKILLS, { recursive: true, force: true });

    // Create destination folders explicitly in case the copy method misses root
    await fs.mkdir(DEST_MEMORY, { recursive: true });
    await fs.mkdir(DEST_SKILLS, { recursive: true });

    // Doing actual deep copy
    console.log(`Copying source: ${SOURCE_MEMORY}`);
    await copyDir(SOURCE_MEMORY, DEST_MEMORY);

    console.log(`Copying source: ${SOURCE_SKILLS}`);
    await copyDir(SOURCE_SKILLS, DEST_SKILLS);

    console.log('📦 Committing Synced Knowledge to Git...');
    try {
        await execAsync('git add src/content/docs/memory src/content/docs/skills');
        await execAsync('git commit -m "chore: auto-sync antigravity brain"');

        console.log('🚀 Pushing to Github branch...');
        await execAsync('git push');

        console.log('✅ Setup success: Synchronized Brain memory with repository!');
    } catch (err) {
        if (err.stdout && /nothing to commit/i.test(err.stdout)) {
            console.log('🤖 Brain is already strictly up to date. Nothing to commit.');
        } else {
            console.error('⚠️ Git operation skipped/failed:', err.message);
        }
    }
}

main();
