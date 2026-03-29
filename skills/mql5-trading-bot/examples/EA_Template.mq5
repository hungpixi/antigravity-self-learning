//+------------------------------------------------------------------+
//|                                              EA_Template.mq5      |
//|      Starter template for new Expert Advisors                     |
//|      Includes: auto-fill type, pip calc, order management         |
//+------------------------------------------------------------------+
#property copyright "EA Template - Comarai.com"
#property version   "1.00"
#property strict

#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>

// === INPUTS ===
input int      InpMagicID     = 12345;      // Magic Number
input double   InpLots        = 0.01;       // Lot Size
input double   InpTPPips      = 30.0;       // Take Profit (pips)
input double   InpSLPips      = 20.0;       // Stop Loss (pips)
input double   InpMaxSpread   = 40.0;       // Max Spread (pips)

// === GLOBALS ===
CTrade         g_trade;
CPositionInfo  g_posInfo;
datetime       g_lastBar = 0;

//+------------------------------------------------------------------+
//| Auto-detect broker filling type                                   |
//+------------------------------------------------------------------+
ENUM_ORDER_TYPE_FILLING GetFillingType()
{
   long fm = SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((fm & SYMBOL_FILLING_FOK) != 0) return ORDER_FILLING_FOK;
   if((fm & SYMBOL_FILLING_IOC) != 0) return ORDER_FILLING_IOC;
   return ORDER_FILLING_RETURN;
}

//+------------------------------------------------------------------+
//| Get pip value for any symbol                                      |
//+------------------------------------------------------------------+
double GetPipPoint()
{
   int d = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   if(d <= 3) return 0.1;       // Metals (XAUUSD)
   if(d == 5) return _Point*10; // Forex 5-digit
   return _Point;
}

//+------------------------------------------------------------------+
//| Normalize lot size                                                |
//+------------------------------------------------------------------+
double NormLots(double lots)
{
   double mn = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double mx = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double st = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   lots = MathMax(lots, mn);
   lots = MathMin(lots, mx);
   lots = MathRound(lots / st) * st;
   return NormalizeDouble(lots, 2);
}

//+------------------------------------------------------------------+
int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicID);
   g_trade.SetDeviationInPoints(10);
   g_trade.SetTypeFilling(GetFillingType()); // CRITICAL!
   
   // TODO: Initialize indicators here
   // g_hRSI = iRSI(_Symbol, PERIOD_M5, 14, PRICE_CLOSE);
   
   Print("EA initialized on ", _Symbol);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   // TODO: Release indicators
   // if(g_hRSI != INVALID_HANDLE) IndicatorRelease(g_hRSI);
}

//+------------------------------------------------------------------+
//| Count our positions                                               |
//+------------------------------------------------------------------+
int CountPos(ENUM_POSITION_TYPE type)
{
   int c = 0;
   for(int i = PositionsTotal()-1; i >= 0; i--)
   {
      if(g_posInfo.SelectByIndex(i) && g_posInfo.Symbol()==_Symbol &&
         g_posInfo.Magic()==InpMagicID && g_posInfo.PositionType()==type)
         c++;
   }
   return c;
}

//+------------------------------------------------------------------+
//| Close positions with retry                                        |
//+------------------------------------------------------------------+
void CloseType(ENUM_POSITION_TYPE type)
{
   for(int r = 0; r < 3; r++)
   {
      int rem = 0;
      for(int i = PositionsTotal()-1; i >= 0; i--)
      {
         if(!g_posInfo.SelectByIndex(i)) continue;
         if(g_posInfo.Symbol()!=_Symbol || g_posInfo.Magic()!=InpMagicID ||
            g_posInfo.PositionType()!=type) continue;
         if(!g_trade.PositionClose(g_posInfo.Ticket())) rem++;
      }
      if(rem == 0) break;
      Sleep(500);
   }
}

//+------------------------------------------------------------------+
//| YOUR SIGNAL LOGIC HERE                                            |
//| Returns: +1 = BUY, -1 = SELL, 0 = no signal                     |
//+------------------------------------------------------------------+
int GetSignal()
{
   // TODO: Implement your signal logic
   // Example: RSI oversold/overbought
   return 0;
}

//+------------------------------------------------------------------+
void OnTick()
{
   // New bar only
   datetime bt = iTime(_Symbol, PERIOD_M5, 0);
   if(bt == 0 || bt == g_lastBar) return;
   g_lastBar = bt;
   
   // Spread check
   double spread = (SymbolInfoDouble(_Symbol, SYMBOL_ASK) -
                    SymbolInfoDouble(_Symbol, SYMBOL_BID)) / GetPipPoint();
   if(spread > InpMaxSpread) return;
   
   int sig = GetSignal();
   if(sig == 0) return;
   
   double pip = GetPipPoint();
   
   // Close opposite
   if(sig == 1 && CountPos(POSITION_TYPE_SELL) > 0) CloseType(POSITION_TYPE_SELL);
   if(sig == -1 && CountPos(POSITION_TYPE_BUY) > 0) CloseType(POSITION_TYPE_BUY);
   
   // Open new
   if(sig == 1 && CountPos(POSITION_TYPE_BUY) == 0)
   {
      double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      double tp = (InpTPPips > 0) ? ask + InpTPPips * pip : 0;
      double sl = (InpSLPips > 0) ? ask - InpSLPips * pip : 0;
      g_trade.Buy(NormLots(InpLots), _Symbol, ask, sl, tp, "EA");
   }
   else if(sig == -1 && CountPos(POSITION_TYPE_SELL) == 0)
   {
      double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      double tp = (InpTPPips > 0) ? bid - InpTPPips * pip : 0;
      double sl = (InpSLPips > 0) ? bid + InpSLPips * pip : 0;
      g_trade.Sell(NormLots(InpLots), _Symbol, bid, sl, tp, "EA");
   }
}

//+------------------------------------------------------------------+
double OnTester()
{
   double p = TesterStatistics(STAT_PROFIT);
   double d = TesterStatistics(STAT_EQUITY_DD_RELATIVE);
   double t = TesterStatistics(STAT_TRADES);
   double pf = TesterStatistics(STAT_PROFIT_FACTOR);
   if(t < 20) return -1000;
   return p * MathSqrt(t) * pf / (1.0 + d);
}
