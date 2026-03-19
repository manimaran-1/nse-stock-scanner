import os

base_dir = "/home/mohan/.gemini/antigravity/scratch"
count = 0

target_str = '.stDeployButton {display:none;}'
replacement_str = '.stDeployButton {display:none;}'

for root, dirs, files in os.walk(base_dir):
    # Ignore virtualenvs to save time
    if 'venv' in root or '.venv' in root or '__pycache__' in root:
        continue
    
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if target_str in content:
                    new_content = content.replace(target_str, replacement_str)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Patched {filepath}")
                    count += 1
            except Exception as e:
                print(f"Failed to read/write {filepath}: {e}")

print(f"\\nSuccessfully patched {count} files across all projects.")
