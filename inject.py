import os

file_path = r'd:\Cá nhân\Trading\bot lái dca\mql5-algo-trading-portfolio\02_IchiDCA_Grinding\CCBSN_v3_PROMAX.mq5'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace ENUM
code = code.replace(
    "SIGNAL_MANUAL_ONLY             // 30. Manual Only (Dùng Panel)\n};",
    "SIGNAL_MANUAL_ONLY,            // 30. Manual Only (Dùng Panel)\n   SIGNAL_LOTTERY                 // 31. Chế độ Xổ số (Random / Ném đá dò đường)\n};"
)

# 2. Insert inputs after InpTpMoney
with open(r'C:\Users\ppnh1\.gemini\antigravity\formatted_inputs.txt', 'r', encoding='utf-8') as f:
    inputs = f.read()

target = "input double   InpTpMoney       = 5.0;          // Chốt lời chung TỔNG rổ lệnh ($)\n"
code = code.replace(target, target + "\n" + inputs + "\n")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Injected successfully!")
