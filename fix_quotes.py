import glob
files = glob.glob('vibescan/**/*.py', recursive=True) + glob.glob('tests/**/*.py', recursive=True) + glob.glob('*.py')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = file.read()
    if r'"""' in data:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(data.replace(r'"""', '"""'))
