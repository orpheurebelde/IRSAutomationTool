import xml.etree.ElementTree as ET
import re

def get_default_namespace(xml_string):
    match = re.search(r'xmlns="([^"]+)"', xml_string)
    return match.group(1) if match else None

with open('IRS_2026_10.xml', 'r', encoding='utf-8') as f:
    xml_string = f.read()

ns = get_default_namespace(xml_string)
root = ET.fromstring(xml_string)
ns_map = {'ns': ns} if ns else {}

tags = ['AnexoJ', 'Quadro08', 'AnexoJq08AT01']
xpath = '/'.join([f'ns:{tag}' if ns else tag for tag in tags])

quadro = root.find(f'.//{xpath}', namespaces=ns_map)
if quadro is not None:
    linha_tag = f'ns:AnexoJq08AT01-Linha' if ns else 'AnexoJq08AT01-Linha'
    for i, linha in enumerate(quadro.findall(linha_tag, namespaces=ns_map)):
        cod = linha.find('ns:CodRendimento' if ns else 'CodRendimento', namespaces=ns_map).text
        pais = linha.find('ns:CodPais' if ns else 'CodPais', namespaces=ns_map).text
        print(f'Line {i+1}: {cod} - {pais}')
