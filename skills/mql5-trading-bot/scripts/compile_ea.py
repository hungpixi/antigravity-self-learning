# Compile MQL5 EA from Antigravity IDE
# Usage: python compile_ea.py MyEA.mq5

import subprocess, sys, os, time

def find_mt5():
    """Find MetaTrader 5 installation"""
    paths = [
        r"C:\Program Files\MetaTrader 5 EXNESS\MetaEditor64.exe",
        r"C:\Program Files\MetaTrader 5\MetaEditor64.exe",
        r"C:\Program Files (x86)\MetaTrader 5\MetaEditor64.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def find_mql5():
    """Find MQL5 experts folder"""
    appdata = os.environ.get('APPDATA', '')
    terminal_dir = os.path.join(appdata, 'MetaQuotes', 'Terminal')
    if not os.path.exists(terminal_dir):
        return None
    for d in os.listdir(terminal_dir):
        mql5 = os.path.join(terminal_dir, d, 'MQL5')
        if os.path.isdir(mql5):
            return mql5
    return None

def compile_ea(source_file):
    editor = find_mt5()
    if not editor:
        print("ERROR: MetaEditor64.exe not found!")
        return False
    
    mql5 = find_mql5()
    if not mql5:
        print("ERROR: MQL5 folder not found!")
        return False
    
    experts = os.path.join(mql5, 'Experts')
    basename = os.path.basename(source_file)
    target = os.path.join(experts, basename)
    
    # Copy
    import shutil
    shutil.copy2(source_file, target)
    print(f"Copied: {source_file} -> {target}")
    
    # Compile
    print(f"Compiling with: {editor}")
    subprocess.Popen([editor, f'/compile:{target}', '/log'])
    time.sleep(8)
    
    # Read log
    log_file = target.replace('.mq5', '.log')
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-16') as f:
            log = f.read()
        
        # Extract errors/warnings
        for line in log.split('\n'):
            line = line.strip()
            if 'error' in line.lower() and '.mq5(' in line:
                print(f"  ❌ {line}")
            elif 'warning' in line.lower() and '.mq5(' in line:
                print(f"  ⚠️ {line}")
        
        # Result
        for line in log.split('\n'):
            if 'Result' in line:
                print(f"\n{line.strip()}")
                if '0 error' in line:
                    print("✅ Compilation successful!")
                    return True
                else:
                    print("❌ Compilation failed!")
                    return False
    
    # Check EX5
    ex5 = target.replace('.mq5', '.ex5')
    if os.path.exists(ex5):
        size = os.path.getsize(ex5)
        print(f"✅ EX5 created: {ex5} ({size} bytes)")
        return True
    
    print("❌ No EX5 file generated")
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compile_ea.py <file.mq5>")
        sys.exit(1)
    
    success = compile_ea(sys.argv[1])
    sys.exit(0 if success else 1)
