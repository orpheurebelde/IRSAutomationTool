# 🎯 Guia Rápido - IRS Automator 2025

## ⚡ Início em 5 Minutos

### 1️⃣ Abrir Aplicação
```
PowerShell
> cd "caminho\do\projeto"
> .\.venv\Scripts\Activate.ps1
> streamlit run app.py
```
✅ Abre no browser em `http://localhost:8501`

---

### 2️⃣ Página HOME 🏠

**O que vê:**
```
┌──────────────────────────────────────┐
│  IRS Automator 2025                  │
│  [Descrição + Como Começar]          │
│                    [📥 Upload]       │
│  Métricas (4 cards):                 │
│  ├─ Anexos Disponíveis: 6            │
│  ├─ Quadros Suportados: 6            │
│  ├─ Total Colunas: 43                │
│  └─ Status: Pronto                   │
└──────────────────────────────────────┘
```

**Ação:**
```
1. Clique em [📥 Upload do ficheiro]
2. Selecione seu XML originalde IRS
3. Espere validação (2-3s)
4. Vê "✅ Ficheiro processado"
5. Aplicação vai para Dashboard (automático)
```

---

### 3️⃣ Página DASHBOARD 📊

**O que vê:**
```
┌────────────────────────────┐
│ 🔍 Procurar anexo:   |__|  │
│ Ordenar por: [Nome ▼]      │
│                            │
│ 📦 TRABALHO DEPENDENTE     │
│ ┌─────────────────────┐    │
│ │ Anexo A - Quadro 4  │    │
│ │ Colunas: 7          │    │
│ │ Registos: 5 🟢      │    │
│ │ [✏️ Editar]         │    │
│ └─────────────────────┘    │
│                            │
│ 💰 MAIS VALIAS             │
│ ┌─────────────────────┐    │
│ │ Anexo G - Quadro 9  │    │
│ │ Colunas: 10         │    │
│ │ Registos: 3 🟢      │    │
│ │ [✏️ Editar]         │    │
│ └─────────────────────┘    │
└────────────────────────────┘
```

**Ações:**
- 🔍 Pesquisar: escrever "Juros" filtra anexos
- 📊 Ordenar: por Nome, Quadro, ou Estado
- ✏️ Editar: clica card → vai para Workspace

---

### 4️⃣ Página WORKSPACE 📝

**Seletor no Topo:**
```
Selecione o Anexo: [Anexo G - Quadro 9 ▼]
```

**4 Tabs:**

#### 📁 ABA 1: Dados Existentes
```
Tabela:
┌─────────┬──────┬─────────────┐
│ Titular │ NIF  │ Valor (€)   │
├─────────┼──────┼─────────────┤
│ A       │ 1234 │ 1.500,50    │
│ A       │ 5678 │ 2.000,00    │
└─────────┴──────┴─────────────┘

Botão: [🗑️ Apagar Histórico Original]
```
✅ Vê o que já existe no XML

#### ➕ ABA 2: Novos Dados
```
[COLA AQUI O CONTEÚDO DO EXCEL]
└─ Escrever ou colar dados

☑️ Incluir cabeçalho na 1ª linha?

[✅ Adicionar à Tabela]
[🗑️ Limpar Tabela]
```
✅ Cole dados do Excel/Google Sheets

#### 📝 ABA 3: Editor
```
Tabela editável:
┌──────┬──────┬──────────────┐
│ Titu │ NIF  │ Valor (€)    │
├──────┼──────┼──────────────┤
│   A  │ 1234 │ 1.500,50  ✏️ │  (duplo clique para editar)
│   A  │ 5678 │ 2.000,00  ✏️ │
│  [+] │ novo │ vazio     [+] │  (nova linha)
└──────┴──────┴──────────────┘

[💾 Guardar Alterações] [🗑️ Limpar]
```
✅ Edite manualmente células

#### 📤 ABA 4: Exportar
```
ℹ️ Aplique as mudanças ao ficheiro

[🔁 Aplicar Anexo G]
  ↓ Se sucesso:
[📥 Descarregar]  [💾 Guardar Local]
```
✅ Faça download ou guarde no PC

---

### 5️⃣ Atalhos Teclado

| Atalho | Função |
|--------|--------|
| `Tab` | Próxima célula (editor) |
| `Shift+Tab` | Célula anterior |
| `Enter` | Nova linha (editor) |
| `Delete` | Eliminar linha selecionada |
| `Esc` | Cancelar edição |
| `Ctrl+C` | Copiar (do Excel) |
| `Ctrl+V` | Colar (na app) |

---

## 📋 Mapa Mental das Páginas

```
┌─── HOME 🏠
│    ├─ Upload XML
│    ├─ Statisticas
│    └─ → Dashboard
│
├─── DASHBOARD 📊
│    ├─ Visualizar Anexos (cards)
│    ├─ Filtro + Pesquisa
│    └─ → Workspace
│
├─── WORKSPACE 📝
│    ├─ Tab 1: Ver originais
│    ├─ Tab 2: Colar dados
│    ├─ Tab 3: Editar manual
│    ├─ Tab 4: Exportar
│    └─ ↔ Dashboard
│
├─── CONFIGURAÇÕES ⚙️
│    ├─ Mapa de Anexos
│    ├─ Regras de Validação
│    ├─ Dicas & Truques
│    └─ Sobre a App
│
└─── DOCUMENTAÇÃO 📖
     ├─ Guia Rápido
     ├─ Anexos (Descrição)
     └─ Config Técnica
```

---

## 🎨 Cores de Feedback

| Cor | Significado | Exemplo |
|-----|-------------|---------|
| 🟢 Verde | Sucesso | ✅ Ficheiro processado |
| 🔴 Vermelho | Erro | ❌ Erro ao gravar |
| 🟡 Amarelo | Aviso | ⚠️ Nenhum ficheiro |
| 🔵 Azul | Informação | ℹ️ Colunas esperadas |

---

## 📊 Fluxo Ideal de Trabalho

```
INÍCIO
  ↓
HOME 🏠
  ├─ Upload XML ✅
  └─ Clique automático → Dashboard
  ↓
DASHBOARD 📊
  ├─ Vê todos anexos
  ├─ Pesquisa "Mais Valias"
  └─ Clica "Editar" no card
  ↓
WORKSPACE 📝
  ├─ TAB 1: Verifica dados (já existem? ou vazio?)
  ├─ TAB 2: Cola novos dados (do Excel)
  ├─ TAB 3: Revisa linhas no editor
  ├─ TAB 4: Aplica e descarrega
  └─ Download XML ✅
  ↓
FIM - XML Pronto para AT
```

---

## 💡 Dicas Profissionais

### Excel → Copiar Dados
```
1. Abrir Excel
2. Selecionar coluna C até E (Código, Data, Valor)
3. Ctrl+C
4. Ir app → Tab 2: "Novos Dados"
5. Cola no textarea: Ctrl+V
6. Marcar "Incluir cabeçalho?" se 1ª linha for títulos
7. Clica "✅ Adicionar à Tabela"
```

### Datas - Automática Conversão
```
Excel: 10/03/2025
Cole: 10/03/2025
App converte: 2025-03-10 ✅ (automático)
```

### Valores Monetários
```
Excel: 1.000,50  (formato português)
Cole: 1.000,50
App converte: 1000.50 ✅ (normalizado)
```

### Histórico Original
```
XML Original: 3 linhas de dados
Cole nova: 2 linhas
Resultado: 5 linhas (originalem + novas)
Quer apagar original? Tab 1: [🗑️ Apagar]
```

---

## 🆘 Problemas Comuns

### ❌ "Erro ao ler os dados colados"
**Causa**: Formato incorreto ou separadores errados
**Solução**:
- Verificar se separador é `;` ou `,`
- Testar com Excel (File → Import)
- Usar Tab como separador

### ❌ "Ficheiro não carregado"
**Causa**: Ficheiro não é XML válido
**Solução**:
- Confirmar extensão `.xml`
- Validar XML (site: xmlvalidation.com)
- Tentar upload novamente

### ❌ "Tabela desaparece ao mudar de aba"
**Causa**: Bug de UI/Streamlit cache
**Solução**:
- Clique F5 (refresh browser)
- Carregue XML novamente
- Contacte suporte técnico

### ❌ "Descarregamento não funciona"
**Causa**: Bloqueador de popup ou browser
**Solução**:
- Clique [💾 Guardar Local] em vez
- Escolha pasta onde guardar
- Ficheiro aparece nessa pasta

---

## 🔢 Referência Anexos

| Anexo | Quadro | Tema | Colunas |
|-------|--------|------|---------|
| **A** | 4 | Trabalho Dependente | 7 |
| **G** | 9 | Mais Valias | 10 |
| **J** | 8.A | Juros/Capitais | 5 |
| **J** | 9.2A | Rendimento Estrangeiro | 10 |
| **H** | 6 | Deduções | 3 |

---

## 📞 Precisa Ajuda?

**Para Dentro da App:**
1. Clique ⚙️ CONFIGURAÇÕES → Dicas
2. Clique 📖 DOCUMENTAÇÃO → Guia Rápido
3. Leia RESUMO_TECNICO_MELHORIAS.md (GitHub)

**Suporte Técnico:**
- Email: 
- Versão App: 2.0 (UI Refatorizada)
- Data: 16 Abril 2026

---

## ✨ Atalhos URL (Bookmarks)

Guardar estes links no browser:

```
📌 Home:       http://localhost:8501
📌 Dashboard:  http://localhost:8501 → Menu 📊
📌 Workspace:  http://localhost:8501 → Menu 📝
📌 Config:     http://localhost:8501 → Menu ⚙️
📌 Docs:       http://localhost:8501 → Menu 📖
```

---

**🚀 Bem-vindo ao IRS Automator!**
**Versão 2.0 - Interface Melhorada**
**© 2026 Câmara Municipal de Vila Nova de Gaia**
