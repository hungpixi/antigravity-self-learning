---
title: "workflow optimization rules"
name: Antigravity Workflow & Protocol Standards (Claude Code inspired)
description: Chuẩn hóa bộ workflow/prompts theo cấu trúc cực ngắn (5-Why/What/How) và protocol Context Isolation.
type: feedback
---

**Fact/Rule:** 
Khi biên soạn, audit hoặc refactor các file hệ thống workflow nội bộ cũng như prompt:
1. **Bám chặt vào cấu trúc 5-Why/What/How** một cách thô bạo dứt khoát.
2. **Kích thước lý tưởng**: Ép toàn bộ các module/file workflow dưới mức **6000 ký tự**.
3. Cài cắm các Protocol Agentic xịn của Claude Code như Context Isolation, Module hoá.

**Why:**
Bảo vệ context window. Workflow mà miên man thì AI sinh ra "ảo giác context". Càng giữ constraint khắt khe (Terminal-first, siêu ngắn, dứt khoát mảng khối) thì Agent và User càng thực thi đúng hướng (không flip-flop lật lọng). 

**How to apply:**
1. Workflow File `/plan`: Thiết kế Software Design Document (SDD) phải tách biệt Component, file nào sửa, file nào xoá, không viết mập mờ.
2. Từ chối thực thi các pattern rườm rà. Nắm đầu ra (Outcome) là quan trọng nhất (30% Effort - 80% Kết quả).
