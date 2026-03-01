import glob
import re

files = glob.glob('vibescan/**/*.py', recursive=True) + glob.glob('tests/**/*.py', recursive=True) + glob.glob('*.py')
for f in files:
    if 'fix_quotes.py' in f:
        continue
    with open(f, 'r', encoding='utf-8') as file:
        data = file.read()
    # Replace escaped quotes
    modified = data.replace(r'\"', '"')
    if modified != data:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(modified)
        print(f"Fixed: {f}")