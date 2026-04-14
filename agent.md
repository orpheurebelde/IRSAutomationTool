Contexto: Sou um profissional de IT e quero criar uma ferramenta interna para automatizar o preenchimento dos anexos G e J do IRS 2025 (Portugal). O objetivo é injetar linhas de transações financeiras num ficheiro XML exportado do Portal das Finanças.

Stack Tecnológica: Python 3.10+, Streamlit, Pandas e xml.etree.ElementTree.

Requisitos Funcionais:

Upload do XML: Permitir o upload do ficheiro XML original da declaração.

Input de Dados (Copy-Paste): Uma st.text_area onde eu possa colar dados tabulares (provenientes de Excel/CSV) com as colunas: Data de Realização, Valor de Realização, Data de Aquisição, Valor de Aquisição e País.

Lógica de Injeção (Anexo G - Quadro 9.1):

O script deve localizar a tag <ANEXOG>. Se não existir, deve criá-la com os namespaces corretos.

Deve inserir blocos <LINHA> dentro de <QUADRO09><QUADRO91>.

Mapear os campos: C91_COD (fixo em "G01"), C91_PAIS, C91_DATA_REALIZACAO, C91_VALOR_REALIZACAO, C91_DATA_AQUISICAO, C91_VALOR_AQUISICAO, e C91_DESPESAS (fixo em "0.00").

Lógica de Injeção (Anexo J - Quadro 9.2A): >    - Similar ao Anexo G, mas para a tag <ANEXOJ><QUADRO09><QUADRO92A>.

Exportação: Gerar um botão de download para o novo XML gerado.

Regras Técnicas Importantes:

Preservar a declaração XML e o encoding UTF-8.

Formatar datas como YYYY-MM-DD.

Garantir que valores numéricos usam o ponto . como separador decimal.

O script deve tratar o parsing do texto colado (separado por tabs ou vírgulas) usando Pandas.

Estrutura de Referência do XML (Exemplo para o Loop):
<LINHA><C91_COD>G01</C91_COD><C91_PAIS>276</C91_PAIS>...</LINHA>

Tarefa: Escreve o código completo para o ficheiro app.py.