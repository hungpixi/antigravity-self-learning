import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import Database from 'better-sqlite3';
import { run, bench, group } from 'mitata';
import fsSync from 'fs';

console.log('🚀 Cấu hình môi trường Benchmark THỰC TẾ (Python STDIO MCP Server)...');

// 1. Phá DB cũ nếu có, dựng DB SQLite MỚI lưu cứng trên Ổ đĩa (Kiến trúc Mempalace thật)
if (fsSync.existsSync('mempalace_mock.db')) fsSync.unlinkSync('mempalace_mock.db');
const db = new Database('mempalace_mock.db');
db.exec('CREATE TABLE memory (id INTEGER PRIMARY KEY, content TEXT, timestamp DATETIME)');
const insert = db.prepare('INSERT INTO memory (content, timestamp) VALUES (?, ?)');

// 2. Locate File .md
const MEMORY_DIR = path.resolve(process.cwd(), 'src/content/docs/memory');
let filesList = [];

try {
    const allFiles = await fs.readdir(MEMORY_DIR);
    filesList = allFiles.filter(f => f.endsWith('.md') || f.endsWith('.mdx')).slice(0, 20);

    // Bơm dữ liệu thật vào ổ cứng cho công bằng 
    for (const f of filesList) {
        const data = await fs.readFile(path.join(MEMORY_DIR, f), 'utf8');
        insert.run(data, new Date().toISOString());
    }
} catch (e) {
    console.log('Warn: Vui lòng chạy `npm run sync` để kéo memory về repo.');
}
// Chốt Database ghi xuống đĩa
db.close();

console.log('✅ SQLite Database Created! Bắt đầu chèn ép phần cứng...\n');

group('AI Memory Latency (Khớp lệnh RAG 20 files Context)', () => {
    bench('Native Markdown RAG (Đọc OS fs.readFile thuần)', async () => {
        let bytes = 0;
        for (const f of filesList) {
            const data = await fs.readFile(path.join(MEMORY_DIR, f), 'utf8');
            bytes += data.length;
        }
    });

    bench('Chuẩn Thực Tế MCP Server (Python Script -> STDIO -> SQLite -> Decode JSON)', () => {
        // Gọi tệp Python qua STDIO chuẩn giao thức của MCP Servers (như Claude Code kết nối Zep/Mempalace)
        const rawOutput = execSync('python benchmarks/mcp_server_mock.py', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
        const mcpPacket = JSON.parse(rawOutput);
        if (!mcpPacket) throw new Error("Thất bại");
    });
});

await run();

// Dọn dẹp
if (fsSync.existsSync('mempalace_mock.db')) fsSync.unlinkSync('mempalace_mock.db');
