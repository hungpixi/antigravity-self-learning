---
title: "ExportMate Codebase Completeness & Architecture Audit"
description: "Deep architectural audit of the frontend React pages, DDD patterns, API routing inconsistencies, SQLite database locks, and interactive UI enhancements."
tags: ["architecture", "completeness", "audit", "react", "backend"]
---

# ExportMate Codebase Completeness & Architecture Audit

We conducted a deep codebase quality, architectural, and visual-UX audit of **ExportMate** across both its frontend React SPA and backend Express services.

---

## Why (Context & Problem)

1.  **API Routing Inconsistencies**
    In the frontend, API integration is decentralized. Pages like `ExportCenterPage.tsx` use a configurable `${API_BASE}` prefix (`import.meta.env.VITE_API_URL || ""`), while others (`AITeamPage.tsx`, `BuyerMatchPage.tsx`, `WalletPage.tsx`) hardcode absolute `/api/...` fetch calls.
    - *Risk*: When deployed separately, static frontend hosts (like Netlify) will route `/api` queries to their own hosts instead of the backend VPS, breaking the features instantly.
2.  **SQLite Database Locking Risk**
    The backend uses **SQLite** via Prisma. While perfect for lightweight local developer work and zero-latency testing, SQLite lacks multi-user concurrent write support. Under simultaneous document uploads, the database will fail with `sqlite busy / database is locked` errors.
3.  **UI Code Bloat & Lack of Global Stores**
    The React SPA manages state in isolated custom hooks and local `useState` hooks. Pages like `WalletPage.tsx` contain over 580 lines of code including keyframe animations, VietQR modals, and confetti simulation state inside a single monolithic component.
4.  **DDD Architecture Completion Rate**
    The `src` folder structure is beautifully planned with Domain-Driven Design (DDD) subfolders (`src/domain`, `src/application`, `src/infrastructure`). However, most current page-level logic bypasses this layer and queries API endpoints directly.

---

## What (Solution & Design)

1.  **Unified API Fetch Client Layer**
    Standardize all HTTP requests into a single centralized API client module using an Axios instance or a unified `apiFetch` wrapper that handles global header injection (JWT), base URL resolution, and centralized error catching.
2.  **PostgreSQL Migration Pipeline**
    Prepare the Prisma configuration for a fast migration to PostgreSQL when scaling.
3.  **Interactive UX Preservation**
    Ensure custom interactive widgets—like the VietQR dynamic laser scanner (`laserScan` animation) and simulated confetti celebrate layer (`confettiFall`)—are modularized into reusable presentation components.
4.  **DDD Infrastructure Alignment**
    Gradually refactor transactional logic from component states into domain services (`src/domain/wallet/`) and repositories inside `src/infrastructure/`.

---

## How (Implementation & Code Snippets)

### 1. Designing a Unified API Client (`src/infrastructure/api/client.ts`)
Create a single, secure gateway for all API calls to resolve routing inconsistencies:
```typescript
const API_BASE = import.meta.env.VITE_API_URL || "";

export async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;
  
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
  }
  
  return response.json() as Promise<T>;
}
```

### 2. Upgrading Prisma for PostgreSQL Compatibility
Modify `schema.prisma` to scale securely without locking:
```prisma
// server/prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Implement connection pooling in server/index.ts
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});
```

### 3. Modularizing VietQR & Celebration UI
Move the complex animated VietQR laser modal from `WalletPage.tsx` into a reusable shared component (`src/components/Payment/VietQrModal.tsx`):
```tsx
import React, { useEffect } from 'react';

interface VietQrModalProps {
  show: boolean;
  onClose: () => void;
  vndAmount: number;
  credits: number;
  txnCode: string;
}

export const VietQrModal: React.FC<VietQrModalProps> = ({ show, onClose, vndAmount, credits, txnCode }) => {
  useEffect(() => {
    if (!show) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [show]);

  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-black/75 z-[999999] flex items-center justify-center p-4">
      {/* Dynamic Laser Line Scanning Container */}
      <div className="bg-white dark:bg-gray-900 rounded-3xl p-6 max-w-md w-full relative">
        <div className="relative mx-auto w-48 h-48 bg-white p-3 rounded-2xl">
          <img src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=txn=${txnCode}&amount=${vndAmount}`} />
          {/* Laser Scanning Animation */}
          <div className="absolute left-0 right-0 h-0.5 bg-emerald-500 animate-[laserScan_2s_linear_infinite]" />
        </div>
      </div>
    </div>
  );
};
```
