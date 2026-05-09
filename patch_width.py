import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'use_container_width\s*=\s*True', 'width="stretch"', content)
content = re.sub(r'use_container_width\s*=\s*False', 'width="content"', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Replaced width attributes')
