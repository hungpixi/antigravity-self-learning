---
name: mql5-trading-bot
description: Complete MQL5 trading bot development workflow for Antigravity IDE. Covers writing MQ5 code, compiling with MetaEditor, deploying to MT5, common errors and fixes.
---

# 🤖 MQL5 Trading Bot Development Skill

> Antigravity IDE skill cho phát triển Expert Advisor (EA) trên MetaTrader 5.  
> Từ viết code → compile → deploy → backtest → debug — tất cả trong IDE.

## 📋 Quick Reference

```
Write .mq5  →  Copy to MQL5/Experts  →  MetaEditor /compile  →  Read .log  →  Check .ex5
```

---

## 🔧 Environment

### Paths
| Item | Path |
|------|------|
| MT5 Install | `C:\Program Files\MetaTrader 5 EXNESS\` |
| MetaEditor | `C:\Program Files\MetaTrader 5 EXNESS\MetaEditor64.exe` |
| MQL5 Root | `%APPDATA%\MetaQuotes\Terminal\<TERMINAL_ID>\MQL5\` |
| Experts | `...MQL5\Experts\` |
| Include | `...MQL5\Include\` |
| Dev Workspace | `d:\Cá nhân\Trading\Bot trade bán tự động\` |

### Detect Terminal ID
```powershell
$terminalDir = Get-ChildItem "$env:APPDATA\MetaQuotes\Terminal\" -Directory |
    Where-Object { Test-Path "$($_.FullName)\MQL5" } | Select-Object -First 1
$mql5Path = "$($terminalDir.FullName)\MQL5"
Write-Host "MQL5 Path: $mql5Path"
```

### Known Terminal ID (ppnh1)
```
53785E099C927DB68A545C249CDBCE06
```

---

## 🔄 Workflow Steps

### Step 1: Write MQ5 Code
Write in dev workspace, then copy to MT5.

**Required boilerplate:**
```cpp
#property copyright "EA Name"
#property version   "1.00"
#property strict

#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>

CTrade g_trade;
CPositionInfo g_posInfo;
```

### Step 2: Auto-Detect Filling Type (CRITICAL)
```cpp
ENUM_ORDER_TYPE_FILLING GetFillingType()
{
   long fm = SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((fm & SYMBOL_FILLING_FOK) != 0) return ORDER_FILLING_FOK;
   if((fm & SYMBOL_FILLING_IOC) != 0) return ORDER_FILLING_IOC;
   return ORDER_FILLING_RETURN;
}

// In OnInit():
g_trade.SetTypeFilling(GetFillingType());
```

> ⚠️ **NEVER hardcode `ORDER_FILLING_IOC`!** Exness chỉ hỗ trợ FOK hoặc RETURN.

### Step 3: GetPipPoint (Multi-Symbol)
```cpp
double GetPipPoint()
{
   int d = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   if(d <= 3) return 0.1;       // XAUUSD, XAGUSD
   if(d == 5) return _Point*10; // Forex 5-digit
   return _Point;
}
```

### Step 4: Copy & Compile
```powershell
$mql5 = "C:\Users\ppnh1\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06\MQL5"
Copy-Item "d:\path\to\MyEA.mq5" "$mql5\Experts\MyEA.mq5" -Force
& "C:\Program Files\MetaTrader 5 EXNESS\MetaEditor64.exe" /compile:"$mql5\Experts\MyEA.mq5" /log
Start-Sleep -Seconds 8
```

### Step 5: Read Compile Log
```python
# Log file is UTF-16 encoded!
with open(r'...\MyEA.log', 'r', encoding='utf-16') as f:
    print(f.read()[-300:])
```

### Step 6: Verify EX5
```powershell
Get-ChildItem "$mql5\Experts\MyEA.ex5" | Format-Table Name, Length, LastWriteTime
```

### Step 7: Read .set Files
```python
# .set files are UTF-16-LE
with open('file.set', 'r', encoding='utf-16-le') as f:
    content = f.read()
```

---

## 🐛 Common Errors Database

### E001: Order Filling Type Not Supported
```
OrderSend error 10030 - Invalid fill type
```
- **Cause:** `ORDER_FILLING_IOC` hardcoded, broker requires FOK/RETURN
- **Fix:** Use `GetFillingType()` (see Step 2)
- **Frequency:** Every new EA on Exness

### E002: iBands Buffer Index Wrong
```
Signals inverted - buying at tops, selling at bottoms
```
**MT5 iBands buffer order (CORRECT):**

| Buffer | Content |
|--------|---------|
| **0** | **BASE** (middle line) |
| **1** | **UPPER** band |
| **2** | **LOWER** band |

> ⚠️ Many online examples show `0=UPPER` which is **WRONG!**

```cpp
// CORRECT:
CopyBuffer(hBB, 1, 0, 3, bbUpper);  // 1 = UPPER
CopyBuffer(hBB, 0, 0, 3, bbMiddle); // 0 = BASE
CopyBuffer(hBB, 2, 0, 3, bbLower);  // 2 = LOWER
```

### E003: Close Position Failed
```
PositionClose failed - error 10030
```
- **Fix:** Retry 3x with Sleep(500) between attempts
```cpp
for(int retry = 0; retry < 3; retry++) {
   int rem = 0;
   for(int i = PositionsTotal()-1; i >= 0; i--) {
      if(!g_posInfo.SelectByIndex(i)) continue;
      if(!g_trade.PositionClose(g_posInfo.Ticket())) rem++;
   }
   if(rem == 0) break;
   Sleep(500);
}
```

### E004: EMA Trend Filter + Mean Reversion = No Signals
- **Symptom:** 0 trades in backtest
- **Cause:** BB buy = price at LOWER band (LOW) + EMA filter requires price > EMA (HIGH) → contradiction
- **Fix:** Don't mix trend filter with mean reversion strategies

### E005: Undeclared Identifier (Declaration Order)
```
error 256: undeclared identifier 'INDI_RSI'
```
- **Cause:** MQL5 requires enum BEFORE input that uses it
- **Fix:** Declaration order: `enum` → `input` → `OnInit()`

### E006: Variable Name Conflicts
- **Cause:** Same array name in different functions at block scope
- **Fix:** Use unique suffixes: `lo1[]`, `lo2[]`

### E007: Strategy Tester Shows Old Inputs
- **Symptom:** Inputs panel shows only 5 inputs after adding 20+
- **Cause:** MT5 caches old EA version
- **Fix:** Close Strategy Tester → Re-select EA from dropdown, or restart MT5

---

## 📊 Indicator Buffer Reference

| Function | Indicator | Buffer 0 | Buffer 1 | Buffer 2 | Buffer 3 | Buffer 4 |
|----------|-----------|----------|----------|----------|----------|----------|
| `iBands` | Bollinger | BASE | **UPPER** | **LOWER** | - | - |
| `iIchimoku` | Ichimoku | Tenkan | Kijun | SpanA | SpanB | Chikou |
| `iMACD` | MACD | Main | Signal | - | - | - |
| `iStochastic` | Stochastic | %K | %D | - | - | - |
| `iRSI` | RSI | Value | - | - | - | - |
| `iCCI` | CCI | Value | - | - | - | - |
| `iATR` | ATR | Value | - | - | - | - |
| `iMA` | Moving Avg | Value | - | - | - | - |
| `iMomentum` | Momentum | Value | - | - | - | - |

---

## 🎯 MT5 Strategy Tester Tips

1. **Reload inputs:** Restart MT5 or re-select EA after recompiling
2. **Custom OnTester:**
```cpp
double OnTester() {
   double p = TesterStatistics(STAT_PROFIT);
   double d = TesterStatistics(STAT_EQUITY_DD_RELATIVE);
   double t = TesterStatistics(STAT_TRADES);
   if(t < 20) return -1000; // Penalize few trades
   return p * MathSqrt(t) / (1.0 + d);
}
```
3. **XAUUSD Max Spread:** Set to **40** (default Exness spread ~36)
4. **Timeframe in code:** Always use `PERIOD_M5` for M5, not `_Period`

---

## 🛡️ Anti-Detect (Prop Firm)

```cpp
// Random comment pool
string g_comments[] = {"manual trade","scalp entry","trend follow",
                        "breakout","pullback","retest","momentum"};

string GetRandomComment() {
   return g_comments[MathRand() % ArraySize(g_comments)];
}

// Random delay between orders
void SetRandomDelay(int minSec=3, int maxSec=15) {
   int delay = minSec + (MathRand() % (maxSec - minSec + 1));
   g_nextAllowed = TimeCurrent() + delay;
}
```

---

## 📁 Project Template

```
trading-bot/
├── MyEA.mq5              # Main EA code
├── ml_params.mqh          # Generated ML params (if applicable)
├── optimizer.py           # Python optimizer script
├── data/
│   └── XAUUSD_M5.csv     # Historical data (gitignored)
├── settings/
│   └── default.set        # Default settings (gitignored)
├── context.md             # ⚠️ NEVER upload (API keys, creds)
├── .gitignore
└── README.md
```

### .gitignore Template
```
context.md
*.set
*.csv
*.ex5
*.log
ml_params.mqh
.env*
__pycache__/
```
