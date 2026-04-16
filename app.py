import streamlit as st
import pandas as pd
from defusedxml.ElementTree import fromstring as safe_fromstring, parse as safe_parse
import xml.etree.ElementTree as ET  # nosec B405 - Used only for namespace registration, parsing done via defusedxml
import re
import io

st.set_page_config(
    page_title="IRS Automator 2025",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "IRS Automator 2025 - Plataforma de Injeção de Anexos XML"
    }
)

# CSS Customização
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
    }
    [data-testid="stSidebar"] {
        width: 280px;
    }
    [data-testid="stMainBlockContainer"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .anexo-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .somas-container {
        background: transparent;
        padding: 0;
        border: none;
        box-shadow: none;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 12px;
        margin-top: 20px;
        width: fit-content;
        margin-left: auto;
    }
    .somas-title {
        font-size: 14px;
        color: #667eea;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .somas-boxes {
        display: flex;
        gap: 12px;
        flex-wrap: nowrap;
        justify-content: flex-end;
        width: fit-content;
    }
    .soma-box {
        background: linear-gradient(135deg, #f0f4ff 0%, #f5f0ff 100%);
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #667eea;
        border-left: 4px solid #2ca02c;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.12);
        white-space: nowrap;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: fit-content;
        width: auto;
        flex-shrink: 0;
    }
    .soma-label {
        font-size: 10px;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .soma-valor {
        font-size: 16px;
        color: #2ca02c;
        font-weight: 700;
        font-family: 'Courier New', monospace;
    }
    .soma-valor.negativo {
        color: #d32f2f;
    }
    /* Estilos para Tabelas */
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.12);
    }
    [data-testid="stDataFrame"] > iframe {
        border-radius: 10px !important;
        border: 1px solid #e8e8f0 !important;
    }
    /* Cabeçalho da tabela */
    [role="presentation"] > table thead {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    [role="presentation"] > table thead th {
        color: white;
        font-weight: 600;
        padding: 12px 16px !important;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #667eea !important;
    }
    /* Linhas da tabela */
    [role="presentation"] > table tbody tr {
        border-bottom: 1px solid #f0f0f5;
    }
    [role="presentation"] > table tbody tr:hover {
        background-color: #f8f9ff !important;
    }
    [role="presentation"] > table tbody td {
        padding: 12px 16px !important;
        color: #333;
        font-size: 14px;
    }
    /* Alternância de cores nas linhas */
    [role="presentation"] > table tbody tr:nth-child(even) {
        background-color: #f8f9ff;
    }
    [role="presentation"] > table tbody tr:nth-child(odd) {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração dinâmica
ANEXOS_CONFIG = {
    "Anexo G - Quadro 9 (Mais Valias)": {
        "tags": ["AnexoG", "Quadro09", "AnexoGq09T01"],
        "linha_tag": "AnexoGq09T01-Linha",
        "has_linha_attr": True, 
        "base_nlinha": 9000, 
        "columns": ["Titular", "NIF", "Código", "Data Realização", "Valor Realização", "Data Aquisição", "Valor Aquisição", "Despesas", "País Contraparte", "Valores Mobiliários"],
        "global_paste_fields": ["Titular", "NIF", "Código", "País Contraparte", "Valores Mobiliários"],
        "defaults": {"Titular": "A", "Código": "G01", "País Contraparte": "620", "Valores Mobiliários": "S"},
        "xml_mapping": {
            "Titular": "Titular",
            "NIF": "NIF",
            "Código": "CodEncargos",
            "Data Realização": "data_split_Realizacao", 
            "Valor Realização": "ValorRealizacao",
            "Data Aquisição": "data_split_Aquisicao",
            "Valor Aquisição": "ValorAquisicao",
            "Despesas": "Despesas",
            "País Contraparte": "PaisContraparte",
            "Valores Mobiliários": "RespeitaValoresMobiliarios"
        },
        "sums": {
            "Valor Realização": "SomaC01",
            "Valor Aquisição": "SomaC02",
            "Despesas": "SomaC03"
        }
    },
    "Anexo J - Quadro 8.A (Juros e Rend. Capitais)": {
        "tags": ["AnexoJ", "Quadro08", "AnexoJq08AT01"],
        "linha_tag": "AnexoJq08AT01-Linha",
        "has_linha_attr": True,
        "base_nlinha": 800,
        "columns": ["Código", "País", "Rendimento Bruto", "Imp. Pago País Fonte", "Imp. Retido"],
        "xml_mapping": {
            "Código": "CodRendimento",
            "País": "CodPais",
            "Rendimento Bruto": "RendimentoBruto",
            "Imp. Pago País Fonte": "ImpostoPagoEstrangeiroPaisFonte",
            "Imp. Retido": "ImpostoPagoEstrangeiroImpostoRetido"
        },
        "sums": {
            "Rendimento Bruto": "SomaC01",
            "Imp. Pago País Fonte": "SomaC02",
            "Imp. Retido": "SomaC03"
        },
        "fixed_sums": {
            "SomaC04": "0.00"
        }
    },
    "Anexo J - Quadro 9.2A (Rend. Estrangeiro)": {
        "tags": ["AnexoJ", "Quadro09", "AnexoJq092AT01"], 
        "linha_tag": "AnexoJq092AT01-Linha",
        "has_linha_attr": True,
        "base_nlinha": 950,
        "columns": ["País Fonte", "Código", "Data Realização", "Valor Realização", "Data Aquisição", "Valor Aquisição", "Despesas Encargos", "Imposto Pago Estrangeiro", "País Contraparte", "Títulos Mobiliários"],
        "xml_mapping": {
            "País Fonte": "CodPais",
            "Código": "Codigo",
            "Data Realização": "data_split_Realizacao",
            "Valor Realização": "ValorRealizacao",
            "Data Aquisição": "data_split_Aquisicao",
            "Valor Aquisição": "ValorAquisicao",
            "Despesas Encargos": "DespesasEncargos",
            "Imposto Pago Estrangeiro": "ImpostoPagoNoEstrangeiro",
            "País Contraparte": "CodPaisContraparte",
            "Títulos Mobiliários": "RespeitaValoresMobiliarios"
        },
        "sums": {
            "Valor Realização": "SomaC01",
            "Valor Aquisição": "SomaC02",
            "Despesas Encargos": "SomaC03",
            "Imposto Pago Estrangeiro": "SomaC04"
        }
    },
    "Anexo A - Quadro 4 (Trabalho Dependente) - EXEMPLO": {
        "tags": ["AnexoA", "Quadro04", "AnexoAq04AT01"],
        "linha_tag": "AnexoAq04AT01-Linha",
        "has_linha_attr": True,
        "columns": ["Titular", "NIF Entidade", "Código", "Rendimentos", "Retenções", "Contribuições", "Quotizações"],
        "global_paste_fields": ["Titular"],
        "defaults": {"Titular": "A"},
        "xml_mapping": {
            "Titular": "Titular",
            "NIF Entidade": "NIF",
            "Código": "CodRendimentos",
            "Rendimentos": "Rendimentos",
            "Retenções": "Retencoes",
            "Contribuições": "Contribuicoes",
            "Quotizações": "Quotizacoes"
        },
        "sums": {
            "Rendimentos": "SomaC01",
            "Retenções": "SomaC02",
            "Contribuições": "SomaC03"
        }
    },
    "Anexo H - Quadro 6 (Deduções à Coleta) - EXEMPLO": {
        "tags": ["AnexoH", "Quadro06", "AnexoHq06AT01"],
        "linha_tag": "AnexoHq06AT01-Linha",
        "has_linha_attr": True,
        "columns": ["Titular", "NIF Entidade", "Valor (Euros)"],
        "global_paste_fields": ["Titular"],
        "defaults": {"Titular": "A"},
        "xml_mapping": {
            "Titular": "SujeitoPassivo",
            "NIF Entidade": "NifBeneficiario",
            "Valor (Euros)": "ValorPensao"
        },
        "sums": {
            "Valor (Euros)": "SomaC01"
        }
    }
}

def get_default_namespace(xml_string):
    match = re.search(r'xmlns="([^"]+)"', xml_string)
    return match.group(1) if match else ""

def build_xpath(tags, has_ns):
    if has_ns:
        return "/".join([f"ns:{tag}" for tag in tags])
    return "/".join(tags)

def extract_sums_from_xml(root, anexo_name, ns):
    """Extrai os valores de soma/checksum do XML para um anexo"""
    config = ANEXOS_CONFIG[anexo_name]
    ns_map = {'ns': ns} if ns else {}
    sums = {}
    
    if "sums" in config:
        for val_col, soma_tag in config["sums"].items():
            tag_path = f".//ns:{config['tags'][-1]}{soma_tag}" if ns else f".//{config['tags'][-1]}{soma_tag}"
            soma_el = root.find(tag_path, namespaces=ns_map)
            if soma_el is not None and soma_el.text:
                sums[val_col] = soma_el.text
    
    if "fixed_sums" in config:
        for soma_tag, fixed_val in config["fixed_sums"].items():
            tag_path = f".//ns:{config['tags'][-1]}{soma_tag}" if ns else f".//{config['tags'][-1]}{soma_tag}"
            soma_el = root.find(tag_path, namespaces=ns_map)
            if soma_el is not None and soma_el.text:
                # Extrai o nome do campo se conseguir (simples)
                sums[soma_tag] = soma_el.text
    
    return sums

def display_sums_box(sums_dict, anexo_config=None, anexo_name=None):
    """Renderiza as somas em caixas arredondadas, uma linha à direita.
    Para Anexo G (Quadro 9), calcula Mais-Valia e Imposto.
    Para Anexo J Quadro 8A, calcula Imposto = (Rendimento Bruto * 28%) - Imp. Pago País Fonte.
    Para Anexo J Quadro 9.2A, calcula Mais-Valia e Imposto como no Anexo G.
    """
    if not sums_dict:
        return
    
    # Criar dicionário com os somatórios
    display_dict = dict(sums_dict)
    
    # Cálculos extras para Anexo G (Mais Valias) ou Anexo J Quadro 9.2A
    if anexo_name and ("Mais Valias" in anexo_name or "9.2A" in anexo_name) and anexo_config:
        try:
            # Extrair valores de Realização e Aquisição
            val_realiz = float(sums_dict.get("Valor Realização", 0).replace(",", ".")) if "Valor Realização" in sums_dict else 0
            val_aquisic = float(sums_dict.get("Valor Aquisição", 0).replace(",", ".")) if "Valor Aquisição" in sums_dict else 0
            
            # Calcular Mais-Valia/Menos-Valia
            mais_valia = val_realiz - val_aquisic
            display_dict["Mais/Menos-Valia"] = f"{mais_valia:.2f}"
            
            # Calcular Imposto (28% se positivo)
            imposto = max(0, mais_valia) * 0.28
            display_dict["Imposto (28%)"] = f"{imposto:.2f}"
        except (ValueError, TypeError):
            pass  # Se houver erro na conversão, ignora os cálculos
    
    # Cálculos extras para Anexo J Quadro 8.A (Juros e Rend. Capitais)
    elif anexo_name and "Quadro 8.A" in anexo_name and anexo_config:
        try:
            # Extrair valores de Rendimento Bruto e Imposto Pago País Fonte
            rend_bruto = float(sums_dict.get("Rendimento Bruto", 0).replace(",", ".")) if "Rendimento Bruto" in sums_dict else 0
            imp_pago = float(sums_dict.get("Imp. Pago País Fonte", 0).replace(",", ".")) if "Imp. Pago País Fonte" in sums_dict else 0
            
            # Calcular Imposto = (Rendimento Bruto * 28%) - Imp. Pago País Fonte
            imposto = (rend_bruto * 0.28) - imp_pago
            display_dict["Imposto a Pagar"] = f"{imposto:.2f}"
        except (ValueError, TypeError):
            pass  # Se houver erro na conversão, ignora os cálculos
    
    # Constrói todo o HTML de uma vez para o flexbox funcionar
    html_boxes = "".join([
        f"""<div class="soma-box">
            <div class="soma-label">{label}</div>
            <div class="soma-valor {'negativo' if str(valor).strip().startswith('-') else ''}">{valor}</div>
        </div>"""
        for label, valor in display_dict.items()
    ])
    
    st.markdown(f"""
    <div class="somas-container">
        <h5 class="somas-title">📊 Somatórios</h5>
        <div class="somas-boxes">
            {html_boxes}
        </div>
    </div>
    """, unsafe_allow_html=True)


def clean_pt_float(val):
    if pd.isna(val): return 0.0
    v_str = str(val).strip()
    if not v_str: return 0.0
    v_str = v_str.replace(' ', '').replace('\xa0', '')
    if '.' in v_str and ',' in v_str:
        v_str = v_str.replace('.', '').replace(',', '.')
    elif ',' in v_str:
        v_str = v_str.replace(',', '.')
    try:
        return float(v_str)
    except ValueError:
        return 0.0

def reconstruct_date(ano, mes, dia):
    if ano and mes and dia:
        return f"{ano}-{str(mes).zfill(2)}-{str(dia).zfill(2)}"
    return ""

def split_date(date_str):
    if not date_str:
        return "", "", ""
    parts = str(date_str).split("-")
    if len(parts) == 3:
        return parts[0], str(int(parts[1])), str(int(parts[2]))
    return "", "", ""

def extract_data_from_xml(root, anexo_name, ns):
    config = ANEXOS_CONFIG[anexo_name]
    ns_map = {'ns': ns} if ns else {}
    xpath = build_xpath(config["tags"], bool(ns))
    quadro = root.find(f".//{xpath}", namespaces=ns_map)
    data = []
    
    if quadro is not None:
        linha_tag = f"ns:{config['linha_tag']}" if ns else config['linha_tag']
        for linha in quadro.findall(linha_tag, namespaces=ns_map):
            row = {}
            for col_name, mapping in config["xml_mapping"].items():
                if mapping.startswith("data_split_"):
                    suffix = mapping.split("_")[2]
                    ano_el = linha.find(f"ns:Ano{suffix}" if ns else f"Ano{suffix}", namespaces=ns_map)
                    mes_el = linha.find(f"ns:Mes{suffix}" if ns else f"Mes{suffix}", namespaces=ns_map)
                    dia_el = linha.find(f"ns:Dia{suffix}" if ns else f"Dia{suffix}", namespaces=ns_map)
                    
                    ano = ano_el.text if ano_el is not None else ""
                    mes = mes_el.text if mes_el is not None else ""
                    dia = dia_el.text if dia_el is not None else ""
                    row[col_name] = reconstruct_date(ano, mes, dia)
                else:
                    el = linha.find(f"ns:{mapping}" if ns else mapping, namespaces=ns_map)
                    row[col_name] = el.text if el is not None else ""
            data.append(row)
            
    return pd.DataFrame(data, columns=config["columns"])

def inject_data_to_xml(root, anexo_name, ns, df, clear_existing=False):
    config = ANEXOS_CONFIG[anexo_name]
    ns_map = {'ns': ns} if ns else {}
    xpath = build_xpath(config["tags"], bool(ns))
    
    current = root
    for i, tag in enumerate(config["tags"]):
        tag_search = f"ns:{tag}" if ns else tag
        found = current.find(tag_search, namespaces=ns_map)
        
        if found is None:
            if i == 0:
                found = root.find(f".//ns:{tag}", namespaces=ns_map) if ns else root.find(f".//{tag}")
            
            if found is None:
                new_tag_name = f"{{{ns}}}{tag}" if ns else tag
                new_elem = ET.SubElement(current, new_tag_name)
                if "Anexo" in tag and "id" not in new_elem.attrib:
                    q03 = root.find(".//ns:Quadro03/ns:Q03C01" if ns else ".//Quadro03/Q03C01", namespaces=ns_map)
                    if q03 is not None and q03.text:
                        new_elem.set("id", q03.text)
                current = new_elem
            else:
                current = found
        else:
            current = found
            
    quadro = current
    
    linha_search = f"ns:{config['linha_tag']}" if ns else config['linha_tag']
    existing_lines = quadro.findall(linha_search, namespaces=ns_map)
        
    if clear_existing:
        for linha in existing_lines:
            quadro.remove(linha)
        existing_lines = []
        
    row_count = len(existing_lines) + 1
    for _, row in df.iterrows():
        if row.astype(str).str.strip().eq("").all():
            continue

        linha_tag_name = f"{{{ns}}}{config['linha_tag']}" if ns else config['linha_tag']
        linha_elem = ET.SubElement(quadro, linha_tag_name)
        if config.get("has_linha_attr"):
            linha_elem.set("numero", str(row_count))
            
        if "base_nlinha" in config:
            nlinha_tag = f"{{{ns}}}NLinha" if ns else "NLinha"
            ET.SubElement(linha_elem, nlinha_tag).text = str(config["base_nlinha"] + row_count)
            
        for col_name, mapping in config["xml_mapping"].items():
            field_val = str(row.get(col_name, "")).strip()
            
            # Formatar para 2 casas decimais colunas financeiras
            if any(key in col_name for key in ["Valor", "Despesas", "Rendimento", "Imp."]):
                numeric_val = clean_pt_float(field_val)
                field_val = "0.00" if numeric_val == 0 else f"{numeric_val:.2f}"

            if mapping.startswith("data_split_"):
                suffix = mapping.split("_")[2]
                ano, mes, dia = split_date(field_val)
                if ano: ET.SubElement(linha_elem, f"{{{ns}}}Ano{suffix}" if ns else f"Ano{suffix}").text = ano
                if mes: ET.SubElement(linha_elem, f"{{{ns}}}Mes{suffix}" if ns else f"Mes{suffix}").text = mes
                if dia: ET.SubElement(linha_elem, f"{{{ns}}}Dia{suffix}" if ns else f"Dia{suffix}").text = dia
            else:
                if field_val:
                    field_tag = f"{{{ns}}}{mapping}" if ns else mapping
                    ET.SubElement(linha_elem, field_tag).text = field_val
                
        row_count += 1

    if "sums" in config:
        for val_col, soma_suffix in config["sums"].items():
            if val_col in df.columns:
                # Summing parsing the float correctly per row (crucial for AT checksum matching)
                parsed_col = df[val_col].apply(clean_pt_float)
                val_sum = parsed_col.round(2).sum()
                
                soma_tag = f"{{{ns}}}{config['tags'][-1]}{soma_suffix}" if ns else f"{config['tags'][-1]}{soma_suffix}"
                
                soma_el = root.find(f".//ns:{config['tags'][-1]}{soma_suffix}" if ns else f".//{config['tags'][-1]}{soma_suffix}", namespaces=ns_map)
                if soma_el is None:
                    # Append it to Quadro09 basically
                    parent_quadro = root.find(f".//ns:{config['tags'][0]}//ns:{config['tags'][1]}" if ns else f".//{config['tags'][0]}//{config['tags'][1]}", namespaces=ns_map)
                    if parent_quadro is not None:
                        ET.SubElement(parent_quadro, soma_tag).text = f"{val_sum:.2f}"
                else:
                    existing_sum = clean_pt_float(soma_el.text) if not clear_existing else 0.0
                    total_sum = existing_sum + val_sum
                    soma_el.text = f"{total_sum:.2f}"
                    
    if "fixed_sums" in config:
        for soma_suffix, fixed_val in config["fixed_sums"].items():
            soma_tag = f"{{{ns}}}{config['tags'][-1]}{soma_suffix}" if ns else f"{config['tags'][-1]}{soma_suffix}"
            soma_el = root.find(f".//ns:{config['tags'][-1]}{soma_suffix}" if ns else f".//{config['tags'][-1]}{soma_suffix}", namespaces=ns_map)
            if soma_el is None:
                parent_quadro = root.find(f".//ns:{config['tags'][0]}//ns:{config['tags'][1]}" if ns else f".//{config['tags'][0]}//{config['tags'][1]}", namespaces=ns_map)
                if parent_quadro is not None:
                    ET.SubElement(parent_quadro, soma_tag).text = fixed_val
            else:
                soma_el.text = fixed_val


def normalize_date(date_str):
    if not date_str or pd.isna(date_str) or str(date_str).strip() == "":
        return ""
    try:
        # pd.to_datetime can parse formats like '10/03/2025' reliably if dayfirst=True
        parsed = pd.to_datetime(str(date_str).strip(), dayfirst=True)
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        # Se não conseguir fazer parse, mantém para não destruir o sistema
        return str(date_str).strip()

def parse_pasted_data(pasted_text, paste_cols, global_vals, has_header):
    try:
        header_val = 0 if has_header else None
        
        if '\t' in pasted_text:
            df = pd.read_csv(io.StringIO(pasted_text), sep='\t', dtype=str, header=header_val)
        else:
            df = pd.read_csv(io.StringIO(pasted_text), sep=',', dtype=str, header=header_val)
            
        taken_cols = min(len(df.columns), len(paste_cols))
        new_df = pd.DataFrame(columns=paste_cols)
        for i in range(taken_cols):
            new_df[paste_cols[i]] = df.iloc[:, i]
            
        new_df = new_df.fillna("")
        
        # Merge global fixed values
        for field, val in global_vals.items():
            new_df[field] = val
            
        # Converter as datas p/ formato AT
        date_columns = [col for col in new_df.columns if "Data" in col]
        for date_col in date_columns:
            new_df[date_col] = new_df[date_col].apply(normalize_date)
            
        # Formatar colunas financeiras coladas p/ dar feedback visual garantido das 2 casas decimais
        val_columns = [col for col in new_df.columns if any(key in col for key in ["Valor", "Despesas", "Rendimento", "Imp."])]
        for v_col in val_columns:
            new_df[v_col] = new_df[v_col].apply(
                lambda x: f"{clean_pt_float(x):.2f}".replace('.', ',') if str(x).strip() else ""
            )
            
        # Reordenar para o order oficial 
        # as the DataFrame structure requires exactly what config["columns"] has
        return new_df
    except Exception as e:
        st.error(f"Erro ao ler os dados colados: {e}")
        return pd.DataFrame()


@st.dialog("📋 Dados Adicionais Necessários")
def dialog_ask_globals(config, pasted_text, paste_cols, has_header, current_edited_df, state_key):
    global_fields = config.get("global_paste_fields", [])
    st.markdown("Preencha os dados abaixo. Estes valores serão aplicados de forma uniforme **a todas as linhas** que acabou de colar. Se os ignorar e gravar no XML a autoridade tributária poderá dar erro.")
    
    global_vals = {}
    for g_field in global_fields:
        default_val = config.get("defaults", {}).get(g_field, "")
        if g_field == "Titular":
            index_start = ["A", "B", "C", "F"].index(default_val) if default_val in ["A", "B", "C", "F"] else 0
            global_vals[g_field] = st.selectbox(f"Titular", ["A", "B", "C", "F"], index=index_start)
        else:
            global_vals[g_field] = st.text_input(f"{g_field}", value=default_val)
            
    if st.button("Confirmar e Adicionar Tabela Final", type="primary", use_container_width=True):
        new_df = parse_pasted_data(pasted_text, paste_cols, global_vals, has_header)
        if not new_df.empty:
            new_df = new_df[config["columns"]]
            combined_df = pd.concat([current_edited_df, new_df], ignore_index=True)
            st.session_state[state_key] = combined_df
            st.rerun()

@st.dialog("⚠️ Confirmar Eliminação")
def dialog_clear_existing(anexo_name):
    st.warning(f"Tem a certeza que deseja APAGAR TODOS os dados originais preenchidos no ficheiro para o {anexo_name}? Apenas as novas linhas que escrever vão ser incluídas.")
    if st.button("Sim, apagar histórico", type="primary"):
        st.session_state[f"clear_existing_{anexo_name}"] = True
        st.rerun()

# ==================== SISTEMA DE NAVEGAÇÃO ====================
def init_session_state():
    """Inicializa variáveis de sessão"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "xml_content_str" not in st.session_state:
        st.session_state.xml_content_str = None
    if "xml_root" not in st.session_state:
        st.session_state.xml_root = None
    if "xml_ns" not in st.session_state:
        st.session_state.xml_ns = None
    if "xml_filename" not in st.session_state:
        st.session_state.xml_filename = None

init_session_state()

# ==================== SIDEBAR - MENU LATERAL ====================
with st.sidebar:
    st.title("📘 Menu")
    st.markdown("---")
    
    pages = {
        "🏠 Home": "home",
        "📊 Dashboard de Anexos": "dashboard",
        "📝 Workspace": "workspace",
        "⚙️ Configurações": "config",
        "📖 Documentação": "docs"
    }
    
    for page_name, page_id in pages.items():
        if st.button(page_name, use_container_width=True, 
                     key=f"btn_{page_id}",
                     type="primary" if st.session_state.current_page == page_id else "secondary"):
            st.session_state.current_page = page_id
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.xml_root is not None:
        st.success(f"✅ Ficheiro Carregado:\n`{st.session_state.xml_filename}`")
        if st.button("🔄 Descarregar Ficheiro", use_container_width=True, type="secondary"):
            st.session_state.xml_root = None
            st.session_state.xml_ns = None
            st.session_state.xml_filename = None
            st.rerun()
    else:
        st.warning("⚠️ Nenhum ficheiro carregado")

# ==================== PÁGINA: HOME ====================
def page_home():
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.title("🏠 Bem-vindo ao IRS Automator 2025")
        st.markdown("""
        ### 📋 Plataforma Dinâmica de Injeção de Anexos XML
        
        Esta aplicação permite-lhe **carregar e modificar ficheiros XML** de declarações IRS,
        facilitando a injeção de dados em **múltiplos anexos** de forma integrada e validada.
        
        ---
        
        #### 🚀 Como Começar:
        1. **Carregue** um ficheiro XML original (à direita)
        2. **Aceda** ao Dashboard de Anexos para ver os quadros disponíveis
        3. **Edite** os dados no Workspace
        4. **Exporte** o ficheiro modificado
        """)
    
    with col2:
        st.subheader("📥 Carregar Ficheiro")
        uploaded_file = st.file_uploader("Selecione ficheiro XML:", type=['xml'], key="home_upload")
        
        if uploaded_file is not None:
            try:
                xml_string = uploaded_file.getvalue().decode("utf-8")
                root = safe_fromstring(xml_string)  # Security: Use defusedxml to prevent XXE attacks
                ns = get_default_namespace(xml_string)
                if ns:
                    ET.register_namespace('', ns)
                
                st.session_state.xml_root = root
                st.session_state.xml_ns = ns
                st.session_state.xml_filename = uploaded_file.name
                
                st.success("✅ Ficheiro processado com sucesso!")
                st.balloons()
                st.session_state.current_page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao processar ficheiro: {e}")
    
    st.markdown("---")
    
    # Estatísticas
    st.subheader("📊 Informações Gerais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Anexos Disponíveis", len(ANEXOS_CONFIG))
    with col2:
        st.metric("🔧 Quadros Suportados", len(ANEXOS_CONFIG))
    with col3:
        st.metric("📈 Colunas Totais", sum(len(config["columns"]) for config in ANEXOS_CONFIG.values()))
    with col4:
        st.metric("✅ Status", "Pronto" if st.session_state.xml_root is None else "Ficheiro Carregado")

# ==================== PÁGINA: DASHBOARD ====================
def page_dashboard():
    if st.session_state.xml_root is None:
        st.warning("⚠️ Por favor, carregue um ficheiro XML primeiro (página Home)")
        return
    
    st.title("📊 Dashboard de Anexos")
    st.markdown("Visualize e gerencie todos os anexos disponíveis")
    
    # Filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Procurar anexo:", placeholder="ex: Mais Valias, Juros...")
    with col2:
        sort_by = st.selectbox("Ordenar por:", ["Nome", "Quadro", "Estado"])
    
    # Agrupar anexos por categoria
    anexos_by_category = {
        "📦 Trabalho Dependente": [],
        "💰 Mais Valias": [],
        "🏦 Rendimentos Capitais": [],
        "💵 Rendimento Estrangeiro": [],
        "🎁 Deduções": [],
        "📋 Outros": []
    }
    
    for anexo_name in ANEXOS_CONFIG.keys():
        if search_term.lower() in anexo_name.lower():
            if "Trabalho" in anexo_name:
                anexos_by_category["📦 Trabalho Dependente"].append(anexo_name)
            elif "Mais Valias" in anexo_name:
                anexos_by_category["💰 Mais Valias"].append(anexo_name)
            elif "Juros" in anexo_name or "Capitais" in anexo_name:
                anexos_by_category["🏦 Rendimentos Capitais"].append(anexo_name)
            elif "Estrangeiro" in anexo_name:
                anexos_by_category["💵 Rendimento Estrangeiro"].append(anexo_name)
            elif "Deduções" in anexo_name:
                anexos_by_category["🎁 Deduções"].append(anexo_name)
            else:
                anexos_by_category["📋 Outros"].append(anexo_name)
    
    # Renderizar cards por categoria
    for category, anexos in anexos_by_category.items():
        if anexos:
            st.subheader(category)
            cols = st.columns(min(3, len(anexos)))
            
            for idx, anexo_name in enumerate(anexos):
                with cols[idx % len(cols)]:
                    config = ANEXOS_CONFIG[anexo_name]
                    
                    # Extrair dados existentes
                    existing_df = extract_data_from_xml(st.session_state.xml_root, anexo_name, st.session_state.xml_ns)
                    num_rows = len(existing_df)
                    
                    # Card
                    st.markdown(f"""
                    <div class="anexo-card">
                        <h4>{anexo_name}</h4>
                        <p><strong>Colunas:</strong> {len(config['columns'])}</p>
                        <p><strong>Registos:</strong> <span style="color: {'green' if num_rows > 0 else 'gray'}">{num_rows}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"✏️ Editar {anexo_name.split('-')[0]}", use_container_width=True, key=f"edit_{anexo_name}"):
                        st.session_state.selected_anexo = anexo_name
                        st.session_state.current_page = "workspace"
                        st.rerun()

# ==================== PÁGINA: WORKSPACE ====================
def page_workspace():
    if st.session_state.xml_root is None:
        st.warning("⚠️ Por favor, carregue um ficheiro XML primeiro")
        return
    
    st.title("📝 Workspace - Editar Anexos")
    
    # Seletor de Anexo
    if "selected_anexo" not in st.session_state:
        st.session_state.selected_anexo = list(ANEXOS_CONFIG.keys())[0]
    
    selected_anexo = st.selectbox(
        "Selecione o Anexo:",
        list(ANEXOS_CONFIG.keys()),
        index=list(ANEXOS_CONFIG.keys()).index(st.session_state.selected_anexo),
        key="workspace_selector"
    )
    st.session_state.selected_anexo = selected_anexo
    
    config = ANEXOS_CONFIG[selected_anexo]
    state_key = f"df_{selected_anexo}"
    
    # Inicializar dados
    if f"clear_existing_{selected_anexo}" not in st.session_state:
        st.session_state[f"clear_existing_{selected_anexo}"] = False
    
    if state_key not in st.session_state:
        initial_df = extract_data_from_xml(st.session_state.xml_root, selected_anexo, st.session_state.xml_ns)
        st.session_state[f"existing_{state_key}"] = initial_df
        st.session_state[state_key] = pd.DataFrame(columns=config["columns"])
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Dados Existentes", "➕ Novos Dados", "📝 Editor", "📤 Exportar"])
    
    with tab1:
        st.subheader("Dados Já Presentes no Ficheiro")
        if not st.session_state[f"existing_{state_key}"].empty and not st.session_state[f"clear_existing_{selected_anexo}"]:
            st.dataframe(st.session_state[f"existing_{state_key}"], use_container_width=True, hide_index=True)
            
            # Mostrar somatórios se existirem
            sums = extract_sums_from_xml(st.session_state.xml_root, selected_anexo, st.session_state.xml_ns)
            if sums:
                display_sums_box(sums, config, selected_anexo)
            
            if st.button("🗑️ Apagar Histórico Original", type="primary"):
                dialog_clear_existing(selected_anexo)
        else:
            st.info("Sem dados existentes ou dados foram apagados")
    
    with tab2:
        st.subheader("Colar Novos Dados")
        
        global_fields = config.get("global_paste_fields", [])
        paste_cols = [c for c in config["columns"] if c not in global_fields]
        
        st.info(f"**Colunas esperadas**: {', '.join(paste_cols)}")
        
        col1, col2 = st.columns(2)
        with col1:
            pasted_data = st.text_area("Cole aqui os dados (Excel/CSV):", height=200, key=f"paste_{selected_anexo}")
        with col2:
            has_header = st.checkbox("Incluir cabeçalho?", value=False)
            
            if st.button("✅ Adicionar à Tabela", use_container_width=True, type="primary"):
                if pasted_data.strip():
                    if config.get("global_paste_fields"):
                        dialog_ask_globals(config, pasted_data, paste_cols, has_header, st.session_state[state_key], state_key)
                    else:
                        new_df = parse_pasted_data(pasted_data, paste_cols, {}, has_header)
                        if not new_df.empty:
                            new_df = new_df[config["columns"]]
                            combined_df = pd.concat([st.session_state[state_key], new_df], ignore_index=True)
                            st.session_state[state_key] = combined_df
                            st.success("✅ Dados adicionados!")
                            st.rerun()
                else:
                    st.warning("Cole alguns dados primeiro")
    
    with tab3:
        st.subheader("Editor de Tabela")
        
        edited_df = st.data_editor(
            st.session_state[state_key],
            num_rows="dynamic",
            key=f"editor_{selected_anexo}",
            hide_index=True,
            use_container_width=True
        )
        
        # Mostrar somatórios se existirem
        sums = extract_sums_from_xml(st.session_state.xml_root, selected_anexo, st.session_state.xml_ns)
        if sums:
            display_sums_box(sums)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar Alterações", use_container_width=True):
                st.session_state[state_key] = edited_df
                st.success("✅ Alterações guardadas!")
        
        with col2:
            if st.button("🗑️ Limpar Tabela", type="secondary", use_container_width=True):
                st.session_state[state_key] = pd.DataFrame(columns=config["columns"])
                st.rerun()
    
    with tab4:
        st.subheader("Exportar Dados")
        
        st.info("Aplique as mudanças ao ficheiro XML e exporte-o")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"🔁 Aplicar {selected_anexo}", type="primary", use_container_width=True):
                inject_data_to_xml(st.session_state.xml_root, selected_anexo, st.session_state.xml_ns, 
                                 edited_df if 'edited_df' in locals() else st.session_state[state_key], 
                                 st.session_state[f"clear_existing_{selected_anexo}"])
                
                out_stream = io.BytesIO()
                tree = ET.ElementTree(st.session_state.xml_root)
                tree.write(out_stream, encoding="UTF-8", xml_declaration=True)
                
                st.session_state['ready_xml'] = out_stream.getvalue()
                st.success("✅ Dados aplicados ao XML!")
        
        with col2:
            if 'ready_xml' in st.session_state:
                st.download_button(
                    label="📥 Descarregar XML",
                    data=st.session_state['ready_xml'],
                    file_name=f"IRS_Modificado.xml",
                    mime="application/xml",
                    type="primary",
                    use_container_width=True
                )
        
        with col3:
            if 'ready_xml' in st.session_state and st.button("💾 Guardar Localmente", use_container_width=True):
                import tkinter as tk
                from tkinter import filedialog
                
                root_tk = tk.Tk()
                root_tk.withdraw()
                root_tk.attributes("-topmost", True)
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".xml",
                    initialfile="IRS_Modificado.xml",
                    title="Guardar ficheiro XML",
                    filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
                )
                root_tk.destroy()
                
                if save_path:
                    try:
                        with open(save_path, "wb") as f:
                            f.write(st.session_state['ready_xml'])
                        st.success(f"✅ Ficheiro guardado em:\n`{save_path}`")
                    except Exception as e:
                        st.error(f"❌ Erro ao guardar: {e}")

# ==================== PÁGINA: CONFIGURAÇÕES ====================
def page_config():
    st.title("⚙️ Configurações")
    
    tabs = st.tabs(["📚 Anexos", "🔍 Validação", "💡 Dicas", "ℹ️ Sobre"])
    
    with tabs[0]:
        st.subheader("Mapa de Anexos Disponíveis")
        
        for anexo_name, config in ANEXOS_CONFIG.items():
            with st.expander(f"📋 {anexo_name}", expanded=False):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**Tags XML:**")
                    for tag in config.get("tags", []):
                        st.code(tag)
                
                with col2:
                    st.markdown("**Colunas:**")
                    for col in config.get("columns", []):
                        st.write(f"• {col}")
    
    with tabs[1]:
        st.subheader("Regras de Validação")
        st.markdown("""
        #### 📅 Datas
        - Formato: YYYY-MM-DD (ex: 2025-12-31)
        - Entrada aceita: dd/mm/yyyy ou formato português
        
        #### 💰 Valores Monetários
        - Sempre com 2 casas decimais
        - Separador: ponto (.) ou vírgula (,)
        - Exemplo: 1.000,50 ou 1000.50
        
        #### 🔢 Códigos
        - NIF: 9 dígitos
        - Código País: 3 dígitos (ISO)
        - Código Rendimento: conforme anexo
        """)
    
    with tabs[2]:
        st.subheader("💡 Dicas de Utilização")
        st.markdown("""
        1. **Colar Dados**: Use Excel/CSV com Ctrl+C e Ctrl+V
        2. **Editar Tabela**: Duplo clique para editar célula
        3. **Eliminar Linha**: Selecione e pressione Delete
        4. **Datas**: Se colar datas em PT (dd/mm/yyyy), serão convertidas
        5. **Valores**: Limpeza automática de formatação de moeda
        """)
    
    with tabs[3]:
        st.markdown("""
        ## ℹ️ IRS Automator 2025
        
        **Versão**: 2.0 Melhorada (UI Refatorizada)
        **Autor**: Câmara Municipal Vila Nova de Gaia
        **Data**: 16 de Abril de 2026
        
        ### Funcionalidades:
        - ✅ Suporta múltiplos anexos IRS
        - ✅ Edição em tempo real
        - ✅ Validação automática
        - ✅ Interface intuitiva
        - ✅ Exportação XML segura
        """)

# ==================== PÁGINA: DOCUMENTAÇÃO ====================
def page_docs():
    st.title("📖 Documentação")
    
    with st.expander("🚀 Guia de Início Rápido", expanded=True):
        st.markdown("""
        ### 1️⃣ Carregue o Ficheiro XML
        - Aceda à página Home
        - Clique em "Carregar Ficheiro"
        - Selecione o seu ficheiro IRS original
        
        ### 2️⃣ Aceda ao Dashboard
        - Visualize todos os anexos disponíveis
        - Veja o número de registos em cada anexo
        - Clique em "Editar" para modificar um anexo
        
        ### 3️⃣ Edite os Dados
        - Na página Workspace, selecione o anexo desejado
        - Use a aba "Novos Dados" para colar dados
        - Ou use a aba "Editor" para editar manualmente
        
        ### 4️⃣ Exporte o Ficheiro
        - Na aba "Exportar", clique "Aplicar Anexo"
        - Descarregue o ficheiro modificado
        - Ou guarde localmente no seu computador
        """)
    
    with st.expander("📋 Estrutura de Anexos"):
        st.markdown("""
        #### Anexo A - Trabalho Dependente
        - Quadro 4: Rendimentos do trabalho dependente
        
        #### Anexo G - Mais Valias
        - Quadro 9: Mais valias realizadas
        
        #### Anexo J - Rendimentos Estrangeiros
        - Quadro 8.A: Juros e rendimentos de capitais
        - Quadro 9.2A: Rendimentos estrangeiros
        
        #### Anexo H - Deduções à Coleta
        - Quadro 6: Deduções fiscais
        """)
    
    with st.expander("⚙️ Configuração Técnica"):
        st.markdown("""
        - **Framework**: Streamlit
        - **Processamento XML**: ElementTree
        - **Manipulação de Dados**: Pandas
        - **Suporte**: Python 3.8+
        """)

# ==================== RENDERIZAÇÃO PRINCIPAL ====================
if st.session_state.current_page == "home":
    page_home()
elif st.session_state.current_page == "dashboard":
    page_dashboard()
elif st.session_state.current_page == "workspace":
    page_workspace()
elif st.session_state.current_page == "config":
    page_config()
elif st.session_state.current_page == "docs":
    page_docs()
else:
    page_home()

