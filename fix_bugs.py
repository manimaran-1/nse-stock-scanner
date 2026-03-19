import os
import glob

# 1. Fix NameError in Arbitrage Scanner
arb_path = "dmi_scanner/pages/3_Arbitrage_Scanner.py"
if os.path.exists(arb_path):
    with open(arb_path, 'r') as f:
        content = f.read()
    
    # Replace the incorrect variable name
    content = content.replace("active_timeframe", "selected_timeframe")
    
    with open(arb_path, 'w') as f:
        f.write(content)
    print(f"Fixed {arb_path}")

# 2. Fix UnhashableParamError in fetch_bulk_data calls
# We need to find all .py files in dmi_scanner/ and dmi_scanner/pages/
# that call fetch_bulk_data(..., progress_callback=...) and change to _progress_callback=
# Note: we only want to change it where it's being passed as an argument.

def fix_progress_callback(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Split into lines to do safer replacement
                lines = content.split('\n')
                new_lines = []
                changed = false = False
                for line in lines:
                    if 'fetch_bulk_data' in line and 'progress_callback=' in line and '_progress_callback=' not in line:
                        line = line.replace('progress_callback=', '_progress_callback=')
                        changed = True
                    new_lines.append(line)
                
                if changed:
                    with open(filepath, 'w') as f:
                        f.write('\n'.join(new_lines))
                    print(f"Patched {filepath}")
                    count += 1
    return count

count = fix_progress_callback("dmi_scanner")
print(f"Replaced progress_callback in {count} files.")
