---
title: "ExportMate Codebase Security & Stacking Audit"
description: "Deep architectural audit of Express backend CORS policies, IP spoofing rate limiters, single-tenant mock auth, and overlay z-index stacking."
tags: ["security", "audit", "express", "backend", "css"]
---

# ExportMate Codebase Security & Stacking Audit

During a deep codebase and architectural audit of **ExportMate**, we identified crucial security risks in the Express backend and stacking bugs in the React frontend.

---

## Why (Context & Problem)

1.  **CORS Over-Permissiveness (CORS Wildcard)**
    In [server/index.ts:L179](file:///d:/code/exportmate/server/index.ts#L179), the backend applies `app.use(cors())` without parameters. This opens the server up to Cross-Origin Resource Sharing from any origin (`*`). Malicious external sites running in the user's browser could query sensitive agricultural data, shipment logs, or transaction credits.
2.  **IP Spoofing Rate Limit Bypass**
    The IP-based rate limiter in [server/index.ts:L188-L190](file:///d:/code/exportmate/server/index.ts#L188-L190) trusts the `x-forwarded-for` header blindly to fetch the client's IP. Because `app.set('trust proxy')` is not configured, any guest user can spoof their IP address by injecting custom `X-Forwarded-For` HTTP headers, completely bypassing the 5 calls/hour limit.
3.  **Single-Tenant Hardcoded Identity**
    The identity variable `const MOCK_USER_ID = 'test-user-id';` (Line 362) is utilized globally across database notifications, transaction deductions, and document kit queries. This blocks true multi-tenancy and session security.
4.  **Overlay Z-Index Stacking Bugs**
    Sticky header components (`AppHeader.tsx`) utilized extremely high z-indexes (`z-99999`), which sat *above* standard drawer modals (`z-[100]`), visually slicing the top of active workspace panels during scroll interactions.

---

## What (Solution & Design)

1.  **Strict CORS Origin Whitelisting**
    Restrict CORS origins in production by matching against an environment whitelist (`ALLOWED_ORIGINS`) while permitting wildcard routing exclusively in local development.
2.  **Secure Proxy-IP Fetching**
    Configure `app.set('trust proxy', 1)` when running behind trusted proxies (like Cloudflare or Nginx), or fallback to secure socket-level address tracking (`req.socket.remoteAddress`).
3.  **Dynamic Session Isolation**
    Integrate proper auth middleware (e.g., JWT token parser) to dynamically inject authenticated user contexts into requests rather than hardcoding `MOCK_USER_ID`.
4.  **Codified Stacking Order**
    Enforce a strict front-end z-index standard where all workspace backdrops sit at `z-[999998]` and foreground modals/drawers sit at `z-[999999]`.

---

## How (Implementation & Code Snippets)

### 1. Hardening CORS Whitelists
Replace `app.use(cors())` with a dynamically whitelisted resolver:
```typescript
const allowedOrigins = process.env.ALLOWED_ORIGINS 
  ? process.env.ALLOWED_ORIGINS.split(',') 
  : ['http://localhost:5173', 'http://localhost:5174'];

app.use(cors({
  origin: (origin, callback) => {
    // Allow server-to-server or local REST tools
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) !== -1 || process.env.NODE_ENV !== 'production') {
      return callback(null, true);
    }
    return callback(new Error('Blocked by secure CORS whitelisting'));
  },
  credentials: true
}));
```

### 2. Preventing IP Spoofing Rate Limit Bypasses
Explicitly configure Express to trust only the immediate upstream proxy and secure IP retrieval:
```typescript
// Enable trusting the first hop proxy
app.set('trust proxy', 1);

function getClientIp(req: express.Request): string {
  // If behind trusted proxy, express populates req.ip accurately
  return req.ip || req.socket.remoteAddress || 'unknown';
}
```

### 3. Transitioning to Authenticated Contexts
Deploy standard JWT validation middleware to resolve user scopes dynamically:
```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthenticatedRequest extends Request {
  userId?: string;
}

export function requireAuth(req: AuthenticatedRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback-secret-key') as { userId: string };
    req.userId = decoded.userId;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}
```

### 4. Resolving Stacking Orders (CSS Tailwind)
Enforce standard stacking order across all overlays in the project:
```tsx
// Backdrop Wrapper
<div className="fixed inset-0 bg-black/50 z-[999998] transition-opacity" onClick={onClose} />

// Foreground Container (Drawer / Modal)
<div className="fixed right-0 top-0 h-full w-[600px] bg-white shadow-xl z-[999999] flex flex-col">
  <div className="flex-none p-4 border-b">Header</div>
  <div className="flex-1 overflow-y-auto p-6">Content</div>
  <div className="flex-none p-4 border-t">Footer</div>
</div>
```
