import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import re
import io

st.set_page_config(page_title="IRS Automator - Injeção de Anexos", layout="wide")

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
        "columns": ["Código", "País", "Rendimento Bruto", "Imp. Pago País Fonte", "País Pagador", "Imp. Retido"],
        "xml_mapping": {
            "Código": "CodRendimento",
            "País": "CodPais",
            "Rendimento Bruto": "RendimentoBruto",
            "Imp. Pago País Fonte": "ImpostoPagoEstrangeiroPaisFonte",
            "País Pagador": "ImpostoPagoEstrangeiroCodPaisPagador",
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
        "tags": ["AnexoJ", "Quadro09", "AnexoJq09T01A"], 
        "linha_tag": "AnexoJq09T01A-Linha",
        "has_linha_attr": True,
        "base_nlinha": 9000,
        "columns": ["Código", "País", "Data Realização", "Valor Realização", "Data Aquisição", "Valor Aquisição", "Despesas"],
        "global_paste_fields": ["Código", "País"],
        "defaults": {"Código": "G01"},
        "xml_mapping": {
            "Código": "CodRendimentos",
            "País": "Pais",
            "Data Realização": "data_split_Realizacao",
            "Valor Realização": "ValorRealizacao",
            "Data Aquisição": "data_split_Aquisicao",
            "Valor Aquisição": "ValorAquisicao",
            "Despesas": "Despesas"
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

def inject_data_to_xml(root, anexo_name, ns, df):
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
    for linha in quadro.findall(linha_search, namespaces=ns_map):
        quadro.remove(linha)
        
    row_count = 1
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
                    soma_el.text = f"{val_sum:.2f}"
                    
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

# UI Rendering
st.title("📄 IRS Automator 2025")
st.markdown("Plataforma Dinâmica de Injeção de Anexos no formato XML da AT.")

if "xml_content_str" not in st.session_state:
    st.session_state["xml_content_str"] = None

with st.expander("🛠️ Passo 1: Carregar Ficheiro Original", expanded=True):
    uploaded_file = st.file_uploader("Upload do Ficheiro XML", type=['xml'])

if uploaded_file is not None:
    xml_string = uploaded_file.getvalue().decode("utf-8")
    
    try:
        root = ET.fromstring(xml_string)
        ns = get_default_namespace(xml_string)
        if ns: ET.register_namespace('', ns)
        
        st.success("Ficheiro processado. Siga para as áreas de trabalho abaixo.")
        
        st.divider()
        st.subheader("🛠️ Passo 2: Workspace de Anexos")
        
        selected_anexo = st.selectbox("Selecione o Anexo a Configurar", list(ANEXOS_CONFIG.keys()))
        config = ANEXOS_CONFIG[selected_anexo]
        state_key = f"df_{selected_anexo}"
        
        if state_key not in st.session_state:
            initial_df = extract_data_from_xml(root, selected_anexo, ns)
            if initial_df.empty:
                initial_df = pd.DataFrame(columns=config["columns"])
            st.session_state[state_key] = initial_df
            
        with st.expander(f"🧩 Gestor de Dados: {selected_anexo}", expanded=True):
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                st.markdown("##### 📝 Tabela Final (editável)")
                st.info("Pode alterar valores duplo clique. Apagar linhas usando tecla Delete.")
                edited_df = st.data_editor(
                    st.session_state[state_key], 
                    num_rows="dynamic",
                    key=f"editor_{selected_anexo}",
                    hide_index=True,
                    use_container_width=True
                )
                
            with col2:
                st.markdown("##### 📥 Colar Novos Dados")
                
                global_fields = config.get("global_paste_fields", [])
                paste_cols = [c for c in config["columns"] if c not in global_fields]
                
                st.caption(f"No texto colado, devem estar APENAS as colunas:\n`{', '.join(paste_cols)}`")
                
                pasted_data = st.text_area("Cole aqui (a partir do Excel/CSV, sem Titular/NIF/Cod)", height=150)
                has_header = st.checkbox("Os dados colados incluem cabeçalho na primeira linha?", value=False)
                
                if st.button("Adicionar à Tabela", use_container_width=True):
                    if pasted_data.strip():
                        if config.get("global_paste_fields"):
                            # Dispara janela popup (modal dialog) se tiver perguntas
                            dialog_ask_globals(config, pasted_data, paste_cols, has_header, edited_df, state_key)
                        else:
                            # Bypass do dialog se o quadro não exigir perguntas extra (Anexo J Quadro 8)
                            new_df = parse_pasted_data(pasted_data, paste_cols, {}, has_header)
                            if not new_df.empty:
                                new_df = new_df[config["columns"]]
                                combined_df = pd.concat([edited_df, new_df], ignore_index=True)
                                st.session_state[state_key] = combined_df
                                st.rerun()
                    else:
                        st.warning("Tem de colar alguns dados primeiro!")

                if st.button("Limpar todos os dados atuais", type="secondary", use_container_width=True):
                    st.session_state[state_key] = pd.DataFrame(columns=config["columns"])
                    st.rerun()

        st.divider()
        st.subheader("🛠️ Passo 3: Fechar Arquivo XML")
        
        col_export_1, col_export_2 = st.columns([1, 2])
        with col_export_1:
            if st.button(f"Aplicar {selected_anexo} no Ficheiro", type="primary", use_container_width=True):
                inject_data_to_xml(root, selected_anexo, ns, edited_df)
                
                out_stream = io.BytesIO()
                tree = ET.ElementTree(root)
                tree.write(out_stream, encoding="UTF-8", xml_declaration=True)
                
                st.session_state['ready_xml'] = out_stream.getvalue()
                
        with col_export_2:
            if 'ready_xml' in st.session_state:
                col_btn_1, col_btn_2 = st.columns(2)
                with col_btn_1:
                    st.download_button(
                        label="📥 Descarregar (Pelo Navegador)",
                        data=st.session_state['ready_xml'],
                        file_name=f"IRS_{selected_anexo.split(' ')[1]}.xml",
                        mime="application/xml",
                        type="primary",
                        use_container_width=True
                    )
                with col_btn_2:
                    if st.button("📁 Salvar Como... (No Computador)", use_container_width=True):
                        import tkinter as tk
                        from tkinter import filedialog
                        
                        root_tk = tk.Tk()
                        root_tk.withdraw()
                        root_tk.attributes("-topmost", True)
                        save_path = filedialog.asksaveasfilename(
                            defaultextension=".xml",
                            initialfile=f"IRS_{selected_anexo.split(' ')[1]}.xml",
                            title="Onde pretende guardar o ficheiro XML da AT?",
                            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
                        )
                        root_tk.destroy()
                        
                        if save_path:
                            try:
                                with open(save_path, "wb") as f:
                                    f.write(st.session_state['ready_xml'])
                                st.success(f"Ficheiro guardado com sucesso em:\n`{save_path}`")
                            except Exception as e:
                                st.error(f"Erro ao gravar ficheiro: {e}")

    except Exception as e:
        st.error(f"Falha de Validação: {e}")

