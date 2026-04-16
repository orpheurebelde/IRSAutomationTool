# 🛡️ Guia Prático: Sanitização de Dados Confidenciais

**Objetivo**: Remover todas as informações pessoais antes de tornar o repositório público.

---

## 📋 CHECKLIST EXECUTIVO

Execute **exatamente** nesta ordem:

1. ✅ [Sanitizar IRS_2026_9.xml](#sanitizar-irs_2026_9xml)
2. ✅ [Verificar Modelo_G_J.xlsx](#verificar-modelo_gj_xlsx)
3. ✅ [Revisar agent.md](#revisar-agentmd)
4. ✅ [Verificar Histórico Git](#verificar-histórico-git)
5. ✅ [Validação Final](#validação-final)

---

## 🔴 PASSO 1: Sanitizar IRS_2026_9.xml

### Problema Identificado:
```xml
<!-- ANTES - NÃO PUBLICAR ❌ -->
<Q03C01>218448660</Q03C01>           <!-- NIF REAL -->
<Q09C01>PT50001000002541720000196</Q09C01>  <!-- IBAN REAL -->
<Q11C01>505366215</Q11C01>           <!-- NIF REAL -->
<NIF>980436613</NIF>                 <!-- NIF REAL -->
```

### Solução:

**Opção A: Usar o Ficheiro de Exemplo Sanitizado (RECOMENDADO ✅)**

```bash
# O ficheiro EXEMPLO_IRS_SANITIZADO.xml já contém dados fictícios
# Simplesmente remova o ficheiro original e use apenas o exemplo
del IRS_2026_9.xml
# OU renomeie
ren IRS_2026_9.xml IRS_2026_9.xml.backup

# O ficheiro de exemplo está pronto para usar/publicar
```

**Opção B: Sanitizar Manualmente**

1. Abra `IRS_2026_9.xml` em editor de texto (VS Code)

2. Use Find & Replace (Ctrl+H):

| Encontrar | Substituir | Motivo |
|-----------|-----------|---------|
| `218448660` | `000000000` | NIF Principal |
| `505366215` | `111111111` | NIF Patronal |
| `980436613` | `333333333` | NIF Anexo G |
| `505335018` | `222222222` | NIF Anexo A |
| `PT50001000002541720000196` | `PT50000000000000000000000` | IBAN |

3. Salve o ficheiro

4. **Importante**: Adicione avisos como comentários XML:
```xml
<!-- ⚠️ FICHEIRO DE TESTE - Dados fictícios para demonstração -->
<!-- NIF: 000000000 (Fictício) -->
<!-- IBAN: PT50000000000000000000000 (Fictício) -->
```

### Verificação:
```bash
# No PowerShell, procure pelos NIFs antigos:
grep "218448660" IRS_2026_9.xml
# Resultado esperado: ❌ Nada encontrado
```

---

## 🔴 PASSO 2: Verificar Modelo_G_J.xlsx

### Problema Identificado:
Ficheiro binário (Excel) - não conseguimos ver conteúdo automaticamente.

### O Que Fazer:

1. **Abra o ficheiro em Excel**:
   ```bash
   start Modelo_G_J.xlsx
   ```

2. **Procure por**:
   - [ ] Nomes de pessoas reais
   - [ ] Números de telefone
   - [ ] Emails pessoais
   - [ ] Datas de nascimento
   - [ ] NIFs ou Números de Identidade
   - [ ] Valores monetários reais (que pareçam rendimentos reais)
   - [ ] Qualquer PII (Personally Identifiable Information)

3. **Se encontrou dados sensíveis**:
   - **Opção A**: Remova o ficheiro (se for só de teste)
   - **Opção B**: Substitua por dados fictícios
   - **Opção C**: Indique que o ficheiro é de exemplo no README

### Se Tiver Dados Fictícios, Está OK ✅
Se o ficheiro contém já dados de teste (como valores de exemplo), pode manter.

---

## 🟠 PASSO 3: Revisar agent.md

### Problema Identificado:
Ficheiro contém contexto interno que pode ser sensível.

### Conteúdo Problemático:
```
Contexto: Sou um profissional de IT e quero criar uma ferramenta interna...
Stack Tecnológica: Python 3.10+, Streamlit, Pandas...
Requisitos Funcionais: [detalhes de implementação]
```

### O Que Fazer:

**Opção A: Remover Ficheiro (RECOMENDADO ✅)**
```bash
del agent.md
git rm agent.md  # Se já está no Git
```

**Opção B: Reescrever como Documento Público**

Se quer manter, reescreva como:
```markdown
# Instruções para o Copilot (Versão Pública)

Esta aplicação destina-se a:
- Processar ficheiros XML do IRS
- Injetar dados em anexos específicos
- Exportar ficheiros processados

Stack: Python 3.10+, Streamlit, Pandas
```

---

## 🟢 PASSO 4: Verificar Histórico Git

### Problema Possível:
Se os ficheiros já foram commitidos com dados reais, eles continuam no histórico.

### Verificação:

```bash
# Ver todos os commits que tocaram no ficheiro XML
git log --all --oneline -- IRS_2026_9.xml

# Ver conteúdo de commits anteriores
git log -p -- IRS_2026_9.xml | grep "218448660"
# Resultado esperado: Encontra dados reais nos commits antigos
```

### Se Encontrou Dados nos Commits Antigos:

⚠️ **Isto é CRÍTICO!** Mesmo que remova o ficheiro agora, os dados sensíveis continuam no histórico.

**Solução (Nuclear - Use com cuidado)**:

```bash
# OPÇÃO 1: Reescrever histórico (para um repositório público novo)
# ⚠️ Isto muda todos os SHAs de commit - só fazer se ainda não é público!

# Remover ficheiro do histórico completamente:
git filter-branch --tree-filter 'rm -f IRS_2026_9.xml' HEAD -f

# Ou usar a ferramenta moderna:
git filter-repo --path IRS_2026_9.xml --invert-paths

# OPÇÃO 2: Criar novo repositório limpo (MAIS RECOMENDADO)
# Se for tornar público agora mesmo:
mkdir IRS_PUBLICO
cd IRS_PUBLICO
git init
git remote add origin https://github.com/SEU_USERNAME/IRS.git
# Copiar apenas ficheiros sanitizados
```

### Verificação Pós-Limpeza:

```bash
# Procurar por dados sensíveis em TODOS os commits
git log --all -S "218448660" -- IRS_2026_9.xml
# Resultado esperado: ❌ Nenhum commit encontrado
```

---

## ✅ PASSO 5: Validação Final

Antes de fazer push para repositório público, execute estes comandos:

### 5.1 Procurar por NIFs (padrão: 9 dígitos)
```bash
grep -r "[0-9]\{9\}" --include="*.xml" --include="*.md" .
# Resultado esperado: Apenas comentários de teste (000000000, etc)
```

### 5.2 Procurar por IBANs
```bash
grep -r "PT[0-9]\{24\}" --include="*.xml" .
# Resultado esperado: Apenas IBANs fictícios (PT50000000000000...)
```

### 5.3 Procurar por Credenciais
```bash
grep -ri "password\|secret\|token\|api_key\|private\|apikey" --include="*.py" --include="*.md" .
# Resultado esperado: ❌ Nada encontrado ou apenas comentários
```

### 5.4 Verificar .gitignore
```bash
# Confirmar que ficheiros sensíveis estão ignorados:
cat .gitignore | grep -E "\.xml|\.xlsx|\.env"
# Resultado esperado: Deve ignorar IRS_*.xml, Modelo_*.xlsx, .env
```

### 5.5 Listar Ficheiros que Vão ser Commitidos
```bash
git status --short
# Revise a lista - não deve incluir dados sensíveis

git diff --cached --name-status
# Revise ficheiros que estão staged
```

---

## 📋 CHECKLIST PRÉ-PUSH PARA REPOSITÓRIO PÚBLICO

```
ANTES DE FAZER git push:

CRÍTICO:
□ IRS_2026_9.xml: NIFs sanitizados? (000000000, 111111111, etc)
□ IRS_2026_9.xml: IBAN sanitizado? (PT50000000000000000000000)
□ Modelo_G_J.xlsx: Verificado manualmente?
□ agent.md: Remover ou reescrever?
□ Histórico Git: Limpo de dados sensíveis?

ALTO (Compliance):
□ LICENSE adicionado? (✅ Já feito)
□ SECURITY.md adicionado? (✅ Já feito)
□ CONTRIBUTING.md adicionado? (✅ Já feito)
□ .github/CODEOWNERS adicionado? (✅ Já feito)
□ requirements.txt adicionado? (✅ Já feito)
□ .python-version adicionado? (✅ Já feito)

MÉDIO:
□ .gitignore atualizado? (✅ Já feito)
□ README.md atualizado com referência a LICENSE?
□ README.md menciona que ficheiros de teste são fictícios?

VERIFICAÇÃO FINAL:
□ Teste local: git status | sem problemas?
□ Teste local: grep confirmou - sem dados reais?
□ README está pronto e referencia GUIA_RAPIDO_USUARIO.md?
□ Todas as branches pronto?
```

---

## 🚀 APÓS SANITIZAÇÃO - PRÓXIMOS PASSOS

### 1. Atualize o README.md:

Adicione esta secção no topo:

```markdown
⚠️ **AVISO IMPORTANTE**

Este repositório contém uma aplicação de exemplo para processar ficheiros XML.

- ✅ **Ficheiros de Teste**: Todos os dados de exemplo são **fictícios**
- ⚠️ **Dados Reais**: Nunca commitir dados reais, NIFs, IBANs ou informações pessoais
- 🔒 **Segurança**: Veja [SECURITY.md](SECURITY.md) para reportar vulnerabilidades
- 📋 **Compliance**: Licença MIT - Veja [LICENSE](LICENSE)
- 🤝 **Contribuições**: Veja [CONTRIBUTING.md](CONTRIBUTING.md)

[Resto do README...]
```

### 2. Commit e Push Final:

```bash
git add .
git commit -m "chore: sanitização de dados e compliance pré-publicação

- Remover dados sensíveis de IRS_2026_9.xml
- Adicionar LICENSE (MIT)
- Adicionar SECURITY.md
- Adicionar CONTRIBUTING.md
- Adicionar CODEOWNERS
- Atualizar .gitignore com padrões específicos
- Adicionar requirements.txt e .python-version
- Criar EXEMPLO_IRS_SANITIZADO.xml para referência"

git push origin main
```

### 3. Configurar no GitHub:

- [ ] Ir a Settings > General
- [ ] Marcar "Public" repositório
- [ ] Adicionar descrição clara
- [ ] Adicionar tópicos (tags): `irs`, `portugal`, `python`, `streamlit`

---

## 🆘 CHECKLIST SE DER PROBLEMAS

**P: Commitei dados sensíveis por acidente!**

A: Ver Passo 4 - Como limpar histórico Git

**P: Não sei que dados remover?**

A: Remova QUALQUER coisa que seja:
- Número de 9 dígitos (pode ser NIF)
- Código IBAN (PT + 24 números)
- Email ou nome pessoal
- Endereço ou morada
- Número de telefone

**P: Qual é o formato fictício correto?**

A: Use os padrões:
- NIF fictício: `000000000`, `111111111`, `222222222`
- IBAN fictício: `PT50 0000 0000 0000 0000 0000`
- Email fictício: `example@example.com`
- Data fictícia: `1910-01-01`

**P: E para Modelo_G_J.xlsx?**

A: Se é Excel com dados reais:
1. Abra em Excel
2. Selecione-tudo e delete o conteúdo
3. Adicione dados fictícios ou remova
4. Salve como `Modelo_G_J_EXEMPLO.xlsx`

---

## ✨ Concluído! ✅

Após estes passos, o repositório está pronto para publicação pública com segurança.

**Próximo**: Ver [RELATORIO_VALIDACAO_SEGURANCA.md](RELATORIO_VALIDACAO_SEGURANCA.md) para checklist completo.

---

**Versão**: 1.0  
**Data**: 16 de Abril 2026  
**Approver**: Validação de Segurança Pre-Publicação
