with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'st.rerun()' in line:
        print(f'--- Line {i+1} ---')
        for j in range(max(0, i-5), i+1):
            print(f'{j+1}: {lines[j].encode("ascii", "ignore").decode("ascii").strip()}')
