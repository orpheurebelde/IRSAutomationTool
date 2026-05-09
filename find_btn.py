with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'button' in line and 'Adicionar' in line:
        print(f'Line {i+1}: {line.encode("ascii", "ignore").decode("ascii").strip()}')
