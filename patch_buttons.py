import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add time.sleep before rerun to show balloons
content = re.sub(
    r'st\.success\([^)]+\)\s*st\.balloons\(\)\s*st\.session_state\.current_page = "dashboard"\s*st\.rerun\(\)',
    'st.success("✅ Ficheiro processado com sucesso!")\n        st.balloons()\n        import time\n        time.sleep(2)\n        st.session_state.current_page = "dashboard"\n        st.rerun()',
    content
)

# Fix 2: Fix Adicionar à Tabela
target2 = '''            if st.button("✅ Adicionar à Tabela", width="stretch", type="primary"):
                if pasted_data.strip():
                    new_df = parse_pasted_data(pasted_data, paste_cols, global_vals, has_header)
                    if not new_df.empty:
                        new_df = align_to_config_columns(new_df, config)
                        combined_df = pd.concat([st.session_state[state_key], new_df], ignore_index=True)
                        st.session_state[state_key] = combined_df
                        refresh_editor(selected_anexo)
                        st.success("✅ Dados adicionados!")
                        st.rerun()
                else:
                    st.warning("Cole alguns dados primeiro")'''

replacement2 = '''            if st.button("✅ Adicionar à Tabela", width="stretch", type="primary", key=f"btn_add_{selected_anexo}"):
                if pasted_data.strip():
                    new_df = parse_pasted_data(pasted_data, paste_cols, global_vals, has_header)
                    if not new_df.empty:
                        new_df = align_to_config_columns(new_df, config)
                        combined_df = pd.concat([st.session_state[state_key], new_df], ignore_index=True)
                        st.session_state[state_key] = combined_df
                        refresh_editor(selected_anexo)
                        st.success("✅ Dados adicionados! Verifique o separador '📝 Editor'.")
                    else:
                        st.error("Nenhum dado válido encontrado para adicionar.")
                else:
                    st.warning("Cole alguns dados primeiro")'''

content = content.replace(target2, replacement2)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done patching')
