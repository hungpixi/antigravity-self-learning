import sys

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith(';'):
            title = line[1:].strip()
            out.append(f'sinput string sep_{len(out)} = "{title}";')
        else:
            if '=' in line:
                var_name = line.split('=')[0]
                rhs = line.split('=')[1]
                val = rhs.split('||')[0]
                
                # Determine type
                if val == 'false' or val == 'true':
                    t = 'bool'
                elif '.' in val:
                    t = 'double'
                elif ':' in val or 'Nhập' in val:
                    t = 'string'
                    val = f'"{val}"'
                else:
                    try:
                        int(val)
                        t = 'int'
                    except:
                        t = 'string'
                        val = f'"{val}"'
                
                out.append(f'input {t} {var_name} = {val}; // ')
                
    with open('mql5_inputs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print("DONE! Wrote to mql5_inputs.txt")

if __name__ == "__main__":
    parse_txt(r'd:\Cá nhân\Trading\bot lái dca\tmp_antoan.txt')
