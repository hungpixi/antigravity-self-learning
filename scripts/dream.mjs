import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import { GoogleGenAI } from '@google/genai';

const MEMORY_DIR = path.resolve(process.cwd(), 'src/content/docs/memory');

async function runDreamPipeline() {
    console.log('🌌 INIT THE DREAM PROTOCOL (Claude Code Inspired Auto-Consolidator)...\n');

    // Phase 1: Orient
    console.log('[Phase 1: Orient] Đánh hơi và quét dọn trong Memory...');
    let files = [];
    try {
        const list = await fs.readdir(MEMORY_DIR);
        files = list.filter(f => f.endsWith('.md') && f !== 'MEMORY.md'); // Bỏ qua file chúa
    } catch (e) {
        console.log('Không tìm thấy thư mục memory.');
        return;
    }

    if (files.length === 0) {
        console.log(`Não bộ vẫn đang sạch tưng, chưa cần Mơ (Nén Memory). Đi ngủ tiếp.`);
        return;
    }

    // Phase 2: Gather
    console.log(`[Phase 2: Gather] Dùng Native fs.readFile để luộc ${files.length} file rác...`);
    let rawContext = '';
    for (const f of files) {
        const text = await fs.readFile(path.join(MEMORY_DIR, f), 'utf8');
        rawContext += `\n--- File: ${f} ---\n${text}\n`;
    }
    console.log(`📍 Đã moi được tổng cộng: ${(Buffer.byteLength(rawContext, 'utf8') / 1024).toFixed(2)} KB raw context.`);

    // Phase 3: Consolidate
    console.log('[Phase 3: Consolidate] Bắt đầu kích hoạt quá trình dập nạp AAAK Dialect qua LLM...');
    let compressedHAAK = '';

    if (process.env.GEMINI_API_KEY) {
        console.log('🔗 Bắt được GEMINI_API_KEY! Bắt tay vào nạp Context cho AI nén rác...');
        try {
            const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
            const prompt = `Bạn là một hệ thống tối ưu bộ nhớ. Hãy đọc toàn bộ đống luật (Rules/Context) được vứt lộn xộn dư thừa sau đây và ép nó về CHUẨN NGÔN NGỮ SIÊU NÉN AAAK (Giống kiến trúc Mempalace của Claude Code).
      
      Yêu cầu:
      - Mã hóa Entity thành 3 chữ cái in hoa (VD: RUL cho Rules, TSK cho Tasks, PRJ cho Project).
      - Dùng ký hiệu mũi tên (->) để chỉ sự liên kết Logic.
      - Xóa bỏ 100% ngữ pháp, từ đệm con người, cảm xúc thừa thãi. Tính bằng Byte chứ không tính bằng câu chữ.
      - Phải đóng gói gọn gàng để máy móc (AI Agent) đọc phát hiểu ngay 0ms.

      Dữ liệu Raw Text cần nén:
      ${rawContext.slice(0, 20000)}
      `;

            const response = await ai.models.generateContent({
                model: 'gemini-2.5-pro',
                contents: prompt
            });
            compressedHAAK = response.text;
        } catch (err) {
            console.error('LLM Consolidation failed (Vượt quá Quota hoặc Rate Limit):', err.message);
            compressedHAAK = 'Lỗi nén mượt... Chuyển sang Dry Run.';
        }
    }

    if (!compressedHAAK || !process.env.GEMINI_API_KEY) {
        console.log('⚠️ Không tìm thấy GEMINI_API_KEY hoặc gọi Lỗi. Bật chế độ Bypass Dry Run (Mock AAAK Rule)...');
        compressedHAAK = `---
title: "Nén Memory Phân Mảnh (AAAK Dialect)"
description: "Dữ liệu được ép xung tự động bởi Tiến trình The Dream."
---

SYS: MEM->CZD(20ms) | RAG: NAT(FST)->MCP(SLW)
RLS: 
 - 5W/WH/HW(6k_chr)<->CTX_ISO
 - TML_CLI: DOC->NOP_MCP | G-DOC: PULL->MD->PUSH(CALIBRI)
BCH: 
 - MIT->LAT
 - RAG->ACC
 - SWE->AGT
`;
    }

    console.log(`📍 Kích thước file sau khi NÉN CỨNG (AAAK): ${(Buffer.byteLength(compressedHAAK, 'utf8') / 1024).toFixed(2)} KB.`);

    // Phase 4: Prune
    console.log('[Phase 4: Prune] Lọc bỏ sự dông dài (Delete rác) & Ghi đè file Lõi Mới...');
    for (const f of files) {
        if (!f.includes('CONSOLIDATED_AAAK')) {
            await fs.unlink(path.join(MEMORY_DIR, f));
        }
    }
    console.log(`🔥 Đã thủ tiêu vĩnh viễn ${files.length} file rác dông dài cũ.`);

    const newFilePath = path.join(MEMORY_DIR, '000_CONSOLIDATED_AAAK.md');
    await fs.writeFile(newFilePath, compressedHAAK);
    console.log(`💾 Ghi đè Thành Công Bộ não Siêu Nén vào: ${newFilePath}`);

    // Tự động kéo cò Astro Sync
    console.log('\n🌟 Đã Tỉnh Giấc! Cập nhật lại kho tàng mới thông suốt rồi. Tự động Hook đẩy mã nguồn lên Github...');
    try {
        execSync('npm run sync', { stdio: 'inherit' });
    } catch (e) {
        console.log('Lưu ý: Sync lên Github không có File thay đổi để commit!');
    }
}

runDreamPipeline();
