# 🚀 IRS Automator 2025 - Versão 2.0 (UI Refatorizada)

## 📖 Bem-vindo!

Esta é a aplicação **IRS Automator** - uma plataforma moderna para injetar e editar dados em ficheiros XML de declarações IRS.

**Versão**: 2.0 (UI Completamente Melhorada)  
**Data**: 16 de Abril de 2026  
**Status**: ✅ Pronto para Produção

---

## ⚠️ AVISO IMPORTANTE - Declaração de Responsabilidade

**Esta aplicação é uma FERRAMENTA DE APOIO** para edição de ficheiros XML de declarações IRS.

### Responsabilidades do Utilizador:

🔴 **CRÍTICO - Leia Antes de Usar:**

1. **Validação de Dados**: O utilizador é **inteiramente responsável** pela validação, correção e precisão de todos os dados inseridos antes de submeter a declaração aos órgãos competentes.

2. **Conformidade Fiscal**: O utilizador é responsável por garantir que todos os dados cumprem com a legislação fiscal portuguesa e as normas da Autoridade Tributária e Aduaneira (AT).

3. **Segurança de Ficheiros**: O utilizador é responsável por:
   - Manter cópias de segurança dos seus ficheiros XML
   - Proteger dados confidenciais e pessoais
   - Não partilhar ficheiros com dados sensíveis

4. **Acuidade Profissional**: Esta ferramenta **não substitui** aconselhamento fiscal profissional. Em caso de dúvidas, contacte um consultor fiscal qualificado.

5. **Teste Prévio**: O utilizador deve testar todas as alterações num ambiente seguro antes de utilizar em dados reais.

### Sem Garantias:

- Esta aplicação é fornecida "tal como está" **SEM GARANTIAS** de qualquer tipo
- Os criadores/desenvolvedores **não são responsáveis** por erros, omissões ou consequências da utilização
- O utilizador assume **todo o risco** associado ao uso desta ferramenta

### Conformidade Legal:

- A utilização desta aplicação implica a **aceitação integral** destas condições
- A responsabilidade legal recai **completamente no utilizador**
- Consulte a [SECURITY.md](SECURITY.md) para política de segurança

---

## ⚡ Início Rápido (3 Minutos)

### 1. Abrir Terminal
```bash
cd "seu/caminho/aqui/IRS"
```

### 2. Ativar Ambiente Virtual
```bash
.\.venv\Scripts\Activate.ps1
```

### 3. Executar Aplicação
```bash
streamlit run app.py
```

### 4. Usar no Browser
A página abre automaticamente em: http://localhost:8501

✅ Pronto! Vê a página Home. Carregue seu ficheiro XML e comece!

---

## 📚 Documentação Disponível

### Para Começar Imediatamente
📄 **[GUIA_RAPIDO_USUARIO.md](GUIA_RAPIDO_USUARIO.md)**  
- ⚡ Início em 5 minutos
- 🎯 Guia passo-a-passo
- 💡 Dicas profissionais
- 🆘 Resolução de problemas

### Para Entender a Aplicação
📄 **[DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md)**  
- 🏗️ Arquitetura completa
- 📋 Cada página detalhada
- 📊 Anexos suportados
- 🔄 Fluxos principais

### Para Detalhes Técnicos
📄 **[RESUMO_TECNICO_MELHORIAS.md](RESUMO_TECNICO_MELHORIAS.md)**  
- 🔧 10 Melhorias específicas
- 📈 Antes vs Depois
- 🎨 Detalhes de implementação
- 🚀 Roadmap futuro

### Para Validar Qualidade
📄 **[CHECKLIST_VALIDACAO.md](CHECKLIST_VALIDACAO.md)**  
- ✅ 139 pontos de verificação
- 🧪 Testes de funcionalidade
- 📱 Testes de responsividade
- 🔒 Validação de segurança

### Para Visão Geral
📄 **[SUMARIO_FINAL.md](SUMARIO_FINAL.md)**  
- 🎯 Resumo do que foi feito
- 📊 Estatísticas
- ✨ Alcançados vs Pedido
- 🏆 Conclusão

### Para Navegação
📄 **[INDICE_FICHEIROS.md](INDICE_FICHEIROS.md)**  
- 📇 Mapa de todos os ficheiros
- 🎓 Por que ficheiro consultar
- 👥 Recomendação por perfil
- 📈 Volume de documentação

### Para o Plano Original
📄 **[PLANO_MELHORIAS_UI.md](PLANO_MELHORIAS_UI.md)**  
- 🎯 Estratégia original
- 🏗️ Arquitetura proposta
- 📋 Anexos categorizados

---

## 🎯 Mapa Rápido de Páginas

A aplicação tem **5 páginas principais**:

### 1. 🏠 HOME
- Bem-vindo à aplicação
- Upload centralizado de ficheiro XML
- Métricas e estatísticas
- Instruções de início rápido

### 2. 📊 DASHBOARD
- Visualização de todos os anexos
- Pesquisa e filtro
- Cards com status de cada anexo
- Navegação direta para edição

### 3. 📝 WORKSPACE
- Edição de dados por anexo
- 4 Tabs:
  - **Dados Existentes**: Ver originais
  - **Novos Dados**: Colar do Excel
  - **Editor**: Edição manual
  - **Exportar**: Descarregar XML

### 4. ⚙️ CONFIGURAÇÕES
- Mapa de anexos
- Regras de validação
- Dicas de utilização
- Sobre a aplicação

### 5. 📖 DOCUMENTAÇÃO
- Guia de início rápido
- Estrutura de anexos
- Configuração técnica

---

## 📋 Anexos Suportados

| Anexo | Quadro | Descrição |
|-------|--------|-----------|
| **A** | 4 | Trabalho Dependente (Remuneração) |
| **G** | 9 | Mais Valias Realizadas |
| **J** | 8.A | Juros e Rendimentos de Capitais |
| **J** | 9.2A | Rendimentos Estrangeiros |
| **H** | 6 | Deduções à Coleta |

---

## 🎯 Fluxo Típico de Trabalho

```
1. HOME 🏠
   ↓
   Carreguue ficheiro XML
   ↓
2. DASHBOARD 📊
   ↓
   Vê todos os anexos disponíveis
   ↓
3. WORKSPACE 📝
   ├─ Tab 1: Ver dados originais (opcional)
   ├─ Tab 2: Colar novos dados do Excel
   ├─ Tab 3: Editar manualmente se necessário
   └─ Tab 4: Exportar (descarregar XML)
   ↓
✅ XML Pronto para a AT (Autoridade Tributária)
```

---

## 💡 Dicas Importantes

### Colar Dados do Excel
1. No Excel: Selecione colunas (Ctrl+C)
2. Na app: Vá a Workspace → Tab "Novos Dados"
3. Cole na textarea (Ctrl+V)
4. Marque se há cabeçalho
5. Clique "Adicionar à Tabela"

### Formato de Datas
- Excel: `10/03/2025` (formato português)
- App converte automaticamente para: `2025-03-10` ✅

### Valores Monetários
- Excel: `1.000,50` ou `1000.50`
- App normaliza para: `1000.50` (2 casas decimais) ✅

### Histórico Original
- Dados originais são **preservados**
- Novos dados são **adicionados**
- Se quer apagar histórico: Tab 1 → Clique "🗑️ Apagar"

---

## 🆘 Problemas Comuns

### ❌ "Erro ao carregar ficheiro"
**Solução**: Certifique-se que é um ficheiro XML válido

### ❌ "Erro ao colar dados"
**Solução**: Verificar separadores (vírgula ou ponto-e-vírgula)

### ❌ "Tabela desaparece"
**Solução**: Pressione F5 (refresh) e carregue novamente

Mais soluções em: [GUIA_RAPIDO_USUARIO.md](GUIA_RAPIDO_USUARIO.md#-problemas-comuns)

---

## 📞 Especificações Técnicas

- **Framework**: Streamlit (Python 3.8+)
- **Processamento XML**: ElementTree
- **Manipulação Dados**: Pandas
- **Validação**: Regex, tipo casting
- **Armazenamento**: Session State (Streamlit)

---

## ✨ Novidades da Versão 2.0

✅ **UI Refatorizada**
- Sidebar com navegação
- 5 páginas temáticas
- Dashboard interativo
- Workspace organizado em tabs

✅ **Melhorias Visuais**
- CSS customizado
- Emojis e ícones
- Cores consistentes
- Feedback visual rico

✅ **Documentação Completa**
- 7 ficheiros markdown (46 páginas)
- 2.300+ linhas de documentação
- Guias por perfil de utilizador
- Checklist de validação (139 pontos)

✅ **100% Compatível**
- Todos os dados processados de forma idêntica
- XML output 100% compatível
- Nenhuma função quebrada

---

## 🚀 Próximas Melhorias Planeadas

- [ ] Suportar mais anexos (B, C, D, E, F, I)
- [ ] Importação Excel direto (.xlsx)
- [ ] Modo escuro (dark mode)
- [ ] Validação XSD em tempo real
- [ ] Sistema de templates
- [ ] API REST para integração

Veja roadmap completo em: [RESUMO_TECNICO_MELHORIAS.md](RESUMO_TECNICO_MELHORIAS.md#-considerações-futuro)

---

## 👥 Suporte & Contacto

**Projeto**: IRS Automator 2025  
**Versão**: 2.0 (UI Refatorizada)  
**Entidade**: Câmara Municipal de Vila Nova de Gaia  
**Data**: 16 de Abril de 2026

---

## 📄 Ficheiros do Projeto

```
IRS\
├── app.py                        (✅ APLICAÇÃO PRINCIPAL)
├── GUIA_RAPIDO_USUARIO.md        (📚 Comece aqui!)
├── DOCUMENTACAO_COMPLETA.md      (📖 Referência completa)
├── RESUMO_TECNICO_MELHORIAS.md   (🔧 Detalhes técnicos)
├── CHECKLIST_VALIDACAO.md        (✅ Testes & QA)
├── SUMARIO_FINAL.md              (🎯 Executive summary)
├── INDICE_FICHEIROS.md           (📇 Navegação)
├── PLANO_MELHORIAS_UI.md         (🏗️ Plano original)
├── README.md                     (📖 Este ficheiro)
├── iniciar_app.bat               (🚀 Atalho para Windows)
├── Modelo_G_J.xlsx               (📊 Dados de exemplo)
├── IRS_2026_9.xml                (📄 XML de exemplo)
└── .venv/                        (🐍 Ambiente Python)
```

---

## 🎓 Leitura Recomendada

**Por Perfil de Utilizador:**

### 👤 Utilizador Final (Técnico IRS)
1. Este ficheiro (README) - 5 min
2. [GUIA_RAPIDO_USUARIO.md](GUIA_RAPIDO_USUARIO.md) - 15 min
3. Experimenta a app - 30 min

### 👨‍💼 Gestor/Stakeholder
1. [SUMARIO_FINAL.md](SUMARIO_FINAL.md) - 10 min
2. [PLANO_MELHORIAS_UI.md](PLANO_MELHORIAS_UI.md) - 5 min

### 👨‍💻 Programador
1. [RESUMO_TECNICO_MELHORIAS.md](RESUMO_TECNICO_MELHORIAS.md) - 20 min
2. [DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md) - 20 min
3. app.py (code review) - 30 min

### 🧪 QA/Tester
1. [CHECKLIST_VALIDACAO.md](CHECKLIST_VALIDACAO.md) - 30 min
2. Executar testes - 120 min

---

## 🔔 Próximos Passos

1. ✅ **Ativar ambiente virtual**
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

2. ✅ **Executar aplicação**
   ```bash
   streamlit run app.py
   ```

3. ✅ **Abrir em browser**
   ```
   http://localhost:8501
   ```

4. ✅ **Carregar ficheiro XML**
   - Vá a Home → Upload

5. ✅ **Explorar Dashboard**
   - Menu → Dashboard para ver anexos

6. ✅ **Editar dados**
   - Menu → Workspace para editar

7. ✅ **Exportar XML**
   - Workspace → Tab Exportar → Download

---

## 📝 Log de Versões

### v2.0 (16 Abril 2026) - ATUAL ✨
- ✅ UI Refatorizada (5 páginas)
- ✅ Sidebar com navegação
- ✅ Dashboard interativo
- ✅ Workspace em tabs
- ✅ Documentação completa (7 ficheiros)
- ✅ 100% compatível com v1.0

### v1.0 (Anterior)
- ✅ Funcionalidade base (3 passos)
- ✅ Upload e export
- ✅ Múltiplos anexos
- ✅ Validação de dados

---

**🎉 Bem-vindo ao IRS Automator 2025!**

**Versão 2.0 - Interface Melhorada e Documentação Completa**

**© Câmara Municipal de Vila Nova de Gaia**

---

## 🔗 Links Rápidos

- 📍 [Home page](http://localhost:8501)
- 📚 [Full Documentation](DOCUMENTACAO_COMPLETA.md)
- ⚡ [Quick Start](GUIA_RAPIDO_USUARIO.md)
- 🔧 [Technical Details](RESUMO_TECNICO_MELHORIAS.md)
- ✅ [Validation Checklist](CHECKLIST_VALIDACAO.md)
- 🎯 [Final Summary](SUMARIO_FINAL.md)
- 📇 [File Index](INDICE_FICHEIROS.md)

---

**Última atualização**: 16 de Abril de 2026
**Status**: ✅ Pronto para Produção
