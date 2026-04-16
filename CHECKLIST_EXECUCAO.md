# ✅ CHECKLIST EXECUÇÃO - PUBLICAÇÃO SEGURA

**Use este documento como checklist prático durante a execução.**

Data de Início: _______________  
Data de Conclusão: _______________  
Preparado por: _______________

---

## 🔴 FASE 1: CRÍTICO (Bloqueia Publicação)

### PASSO 1: Sanitizar IRS_2026_9.xml

Tempo Estimado: ⏱️ 10 minutos

#### Verificação Prévia:
- [ ] Ficheiro `IRS_2026_9.xml` existe?
- [ ] Consegue abrir em editor de texto (VS Code, Notepad++)?
- [ ] Backup criado? (copiar ficheiro para outro local)

#### Sanitização (Use Find & Replace - Ctrl+H):

**Substituição 1: NIF Principal**
- [ ] Encontrar: `218448660`
- [ ] Substituir por: `000000000`
- [ ] Comentário adicionado? (para referência)

**Substituição 2: NIF Patronal**
- [ ] Encontrar: `505366215`
- [ ] Substituir por: `111111111`
- [ ] OK? (Pressione Replace All)

**Substituição 3: NIF Anexo G (Linha 1)**
- [ ] Encontrar: `980436613`
- [ ] Substituir por: `333333333`
- [ ] OK? (Pressione Replace All)

**Substituição 4: NIF Anexo A**
- [ ] Encontrar: `505335018`
- [ ] Substituir por: `222222222`
- [ ] OK? (Pressione Replace All)

**Substituição 5: IBAN**
- [ ] Encontrar: `PT50001000002541720000196`
- [ ] Substituir por: `PT50000000000000000000000`
- [ ] OK? (Pressione Replace All)

#### Adição de Avisos:
- [ ] Adicionar comentário XML no topo do ficheiro:
```xml
<!-- ⚠️ FICHEIRO DE TESTE - Dados fictícios para demonstração -->
<!-- Última atualização: [DATA] -->
```

#### Verificação Final:
```bash
Command: grep "218448660" IRS_2026_9.xml
Resultado Esperado: (sem resultados)
Resultado Obtido: _________________________________
☐ Nenhuma ocorrência encontrada? (✅ SIM)
```

#### Estado: ☐ COMPLETO

---

### PASSO 2: Verificar Modelo_G_J.xlsx

Tempo Estimado: ⏱️ 10 minutos

#### Abertura:
- [ ] Ficheiro `Modelo_G_J.xlsx` existe?
- [ ] Consegue abrir em Excel/LibreOffice?
- [ ] Ficheiro abre sem erros?

#### Verificação de PII (Marque o que encontrar):

**Procurar por:**
- [ ] Nomes de pessoas reais
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter (fictício)
  
- [ ] Números de telefone
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter
  
- [ ] Emails pessoais
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter
  
- [ ] Números de 9 dígitos (possíveis NIFs)
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter
  
- [ ] IBANs (PT + 24 números)
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter
  
- [ ] Valores monetários que pareçam rendimentos reais
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter
  
- [ ] Datas de nascimento
  - Se encontrou: ☐ Remover ☐ Anonimizar ☐ Manter

#### Ações Tomadas:

Se encontrou PII:
- [ ] Ação Escolhida: ☐ Remover ☐ Anonimizar ☐ Manter (fictício)
- [ ] Ficheiro salvo após mudanças?

Se não encontrou:
- [ ] OK - Ficheiro é fictício/teste ✅

#### Estado: ☐ COMPLETO

---

### PASSO 3: Revisar agent.md

Tempo Estimado: ⏱️ 5 minutos

#### Análise:
- [ ] Ficheiro `agent.md` existe?
- [ ] Contém contexto interno/pessoal?
- [ ] Pode comprometerSegurança?

#### Decisão:
- [ ] Opção A: Remover ficheiro completamente
  ```bash
  del agent.md
  git rm agent.md (se já commitido)
  ```
- [ ] Opção B: Reescrever como documento público
  - [ ] Removidas informações pessoais?
  - [ ] Removidas informações de case/contexto?
  - [ ] Reescrito em tom público/genérico?

#### Estado: ☐ COMPLETO

---

### PASSO 4: Verificar Histórico Git

Tempo Estimado: ⏱️ 5 minutos

**Objetivo**: Confirmar que dados sensíveis não estão em commits antigos

#### Comando 1: Procurar por NIFs em Git:
```bash
Command: git log --all -S "218448660" -- IRS_2026_9.xml
```

Resultado: _________________________________

- [ ] 0 commits encontrados (✅ Esperado)
- [ ] N commits encontrados (❌ Problema!)
  
**Se encontrou commits com dados reais:**
- [ ] Contactar especialista Git (rehistória é complexa)
- [ ] Ou: Criar novo repositório limpo (remover dados do histórico)

#### Comando 2: Verificar todos os commits do ficheiro:
```bash
Command: git log --oneline -- IRS_2026_9.xml
```

Resultado: 
```
_________________________________
_________________________________
_________________________________
```

- [ ] Revistos todos os commits?
- [ ] Confirmar que dados foram sanitizados em TODOS?

#### Estado: ☐ COMPLETO

---

## 🟡 FASE 2: VALIDAÇÃO (Antes de Push)

### PASSO 5: Validação Final - Comandos

Tempo Estimado: ⏱️ 10 minutos

#### Teste 1: Procurar por NIFs (9 dígitos):

```bash
Command: grep -r "[0-9]\{9\}" --include="*.xml" --include="*.md" .
```

Resultado (mostrar saída):
```
_________________________________
_________________________________
_________________________________
```

Análise:
- [ ] Apenas padrões fictícios (000000000, 111111111, etc)?
- [ ] OU nenhum resultado?
- ☐ PRONTO - Sem NIFs reais

#### Teste 2: Procurar por IBANs:

```bash
Command: grep -r "PT[0-9]\{24\}" --include="*.xml" .
```

Resultado (mostrar saída):
```
_________________________________
_________________________________
```

Análise:
- [ ] Apenas IBANS fictícios (PT50 0000...)?
- [ ] OU nenhum resultado?
- ☐ PRONTO - Sem IBANs reais

#### Teste 3: Procurar por Credenciais:

```bash
Command: grep -ri "password|secret|token|api_key|apikey" --include="*.py" --include="*.md" .
```

Resultado:
```
_________________________________
_________________________________
```

Análise:
- [ ] Nenhum resultado? ☐ SIM
- [ ] Apenas comentários/documentação?
- ☐ PRONTO - Sem credenciais

#### Teste 4: Verificar Git Status:

```bash
Command: git status --short
```

Resultado:
```
_________________________________
_________________________________
_________________________________
```

Análise:
- [ ] Ficheiros modificados Ok?
- [ ] Ficheiros staged Ok?
- [ ] Nenhum ficheiro sensível prestes a ser commitido?
- ☐ STATUS PRONTO

#### Estado Validação: ☐ COMPLETO

---

## 🟢 FASE 3: COMPLIANCE (Já Criado ✅)

Tempo Estimado: ⏱️ 2 minutos (apenas verificação)

- [x] LICENSE criado? ✅ 
- [x] SECURITY.md criado? ✅ 
- [x] CONTRIBUTING.md criado? ✅ 
- [x] .github/CODEOWNERS criado? ✅ 
- [x] requirements.txt criado? ✅ 
- [x] .python-version criado? ✅ 
- [x] .gitignore atualizado? ✅ 

**Nada a fazer nesta fase** - Já tudo criado automaticamente.

---

## ⚪ FASE 4: PRÉ-PUSH (Final - 5 min)

### Verificação Final Antes de Commit

- [ ] Leu [GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md)?
- [ ] Completou FASES 1-3 acima?
- [ ] Todos os testes PASSARAM (nenhum erro)?

### Prepare o Commit:

```bash
Command: git add .
```

- [ ] Arquivo estão stage (green)?

### Crie Commit com Mensagem Descritiva:

**Mensagem Recomendada:**
```
git commit -m "chore: sanitização de dados e compliance pré-publicação

- Sanitizar IRS_2026_9.xml: substituir NIFs e IBAN por fictícios
- Revisar Modelo_G_J.xlsx: confirmar dados são teste
- Remover contexto interno de agent.md
- Adicionar LICENSE (MIT)
- Adicionar SECURITY.md com política de divulgação
- Adicionar CONTRIBUTING.md
- Adicionar .github/CODEOWNERS para governança
- Criar requirements.txt com dependências pinned
- Criar .python-version
- Atualizar .gitignore com padrões mais específicos
- Criar EXEMPLO_IRS_SANITIZADO.xml como referência
- Criar documentação completa: relatório, guia, resumo

Satisfaz compliance LGPD/RGPD. Pronto para repositório público."
```

- [ ] Mensagem clara e descritiva?

### Push para Repositório:

```bash
Command: git push origin main
```

Resultado: _________________________________

- [ ] Push realizado com sucesso?
- [ ] Nenhum erro de autenticação?

---

## 🎉 FASE 5: PÓS-PUBLICAÇÃO (Verificação Final)

### No GitHub:

1. **Fazer Repositório Público**:
   - [ ] Ir a Settings
   - [ ] Selecionar "Public"
   - [ ] Confirmar

2. **Verificação Visual**:
   - [ ] Repositório aparece público?
   - [ ] LICENSE é visível?
   - [ ] README é visível?
   - [ ] Ficheiros sensíveis estão fora (não listados)?

3. **Validação de Segurança**:
   - [ ] Procurar no site GitHub: 218448660
   - [ ] Resultado esperado: ❌ Não encontrado
   - [ ] OK? ✅

---

## 📊 RESUMO FINAL

| Fase | Tarefa | Status | Notas |
|------|--------|--------|-------|
| 1 | IRS_2026_9.xml sanitizado | ☐ | ◼▪▪ |
| 1 | Modelo_G_J.xlsx verificado | ☐ | ◼▪▪ |
| 1 | agent.md revisado | ☐ | ◼▪▪ |
| 2 | Histórico Git verificado | ☐ | ◼▪▪ |
| 2 | Validação Final testada | ☐ | ◼▪▪ |
| 3 | Compliance files prontos | ✅ | ▪▪▪ |
| 4 | Commit realizado | ☐ | ◼▪▪ |
| 5 | Repositório público | ☐ | ◼▪▪ |

---

## ⚠️ TROUBLESHOOTING

**Se encontrou erro em:**

| Erro | Solução |
|------|---------|
| Não consegue abrir IRS_2026_9.xml | Use VS Code ou Notepad++ |
| Find & Replace não encontra texto | Copie o texto exato (sem espaços extra) |
| grep não funciona (Windows) | Use PowerShell ou Git Bash |
| Dados ainda aparecem em histórico Git | Ver GUIA_SANITIZACAO_DADOS.md > PASSO 4 |
| Push rejeitado | Verificar permissões GitHub / branch name |

---

## ✅ ASSINATURA

**Executado por**: ____________________  
**Data**: ____________________  
**Revisado por**: ____________________  
**Aprovado para Publicação**: ☐ SIM ☐ NÃO  

---

**Documento de Controlo**  
Versão: 1.0  
Última Atualização: 16 de Abril 2026

