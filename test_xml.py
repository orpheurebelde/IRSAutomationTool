import xml.etree.ElementTree as ET
import re

def get_default_namespace(xml_string):
    match = re.search(r'xmlns=\"([^\"]+)\"', xml_string)
    return match.group(1) if match else None

with open('IRS_2026_10.xml', 'r', encoding='utf-8') as f:
    xml_string = f.read()

ns = get_default_namespace(xml_string)
root = ET.fromstring(xml_string)
ns_map = {'ns': ns} if ns else {}

# For Anexo J 9.2A
tags = ['AnexoJ', 'Quadro09', 'AnexoJq092AT01']
xpath = '/'.join([f'ns:{tag}' if ns else tag for tag in tags])
print('XPath:', xpath)

quadro = root.find(f'.//{xpath}', namespaces=ns_map)
print('Quadro found:', quadro is not None)
if quadro is not None:
    linha_tag = f'ns:AnexoJq092AT01-Linha' if ns else 'AnexoJq092AT01-Linha'
    linhas = quadro.findall(linha_tag, namespaces=ns_map)
    print('Linhas found:', len(linhas))
