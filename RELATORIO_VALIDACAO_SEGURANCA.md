# 🔒 Relatório de Validação - Dados Confidenciais e Compliance
**Data**: 16 de Abril de 2026  
**Status**: ⚠️ REQUER AÇÕES ANTES DE PUBLICAÇÃO  
**Classificação**: CRÍTICO + ALTO

---

## 📋 RESUMO EXECUTIVO
O repositório contém **dados confidenciais que devem ser sanitizados** antes de tornar público. Identificadas **7 problemas críticos/altos** e **4 recomendações de compliance**.

| Severidade | Contagem | Status |
|-----------|----------|--------|
| 🔴 CRÍTICO | 3 | ⚠️ Ação Necessária |
| 🟠 ALTO | 4 | ⚠️ Ação Recomendada |
| 🟡 MÉDIO | 3 | ℹ️ Melhorar |
| 🟢 BAIXO | 2 | ✅ Opcional |

---

## 🔴 PROBLEMAS CRÍTICOS

### 1. **NIBS e Números de Identidade Fiscal Expostos** (CRÍTICO)
**Localização**: `IRS_2026_9.xml`  
**Risco**: Exposição de dados pessoais - violação RGPD/LGPD  

**Dados Identificados**:
```xml
<!-- Quadro03 - NIF Principal -->
<Q03C01>218448660</Q03C01>

<!-- Quadro11 - NIF da Entidade Patronal -->
<Q11C01>505366215</Q11C01>

<!-- AnexoA - NIF da Entidade -->
<NIF>505335018</NIF>

<!-- AnexoG - NIF Múltiplos -->
<NIF>980436613</NIF>
```

**Impacto**: Este é um ficheiro de teste/exemplo que será visto por qualquer pessoa que clone o repositório.

**Ação Recomendada**:
- ✅ Substituir NIFs por valores fictícios (ex: 000000000, 111111111)
- ✅ Usar NIFs de teste publicados por entidades oficiais, se disponíveis
- ✅ Ou remover este ficheiro e incluir um README com instruções de geração

**Prioridade**: 🔴 CRÍTICO - Fazer antes de push público

---

### 2. **IBAN Exposto no XML** (CRÍTICO)
**Localização**: `IRS_2026_9.xml` > `Quadro09`  
**Risco**: Exposição de conta bancária - violação RGPD/compliance

**Dado Identificado**:
```xml
<Q09C01>PT50001000002541720000196</Q09C01>
```

**Impacto**: IBAN válido em formato (PT50...) que pode ser utilizado para phishing ou engenharia social.

**Ação Recomendada**:
- ✅ Substituir por IBAN fictício: `PT50 0000 0000 0000 0000 0000`
- ✅ Adicionar comentário no ficheiro XML indicando que é exemplar

**Prioridade**: 🔴 CRÍTICO

---

### 3. **Ficheiro Excel com Dados Sensíveis Potenciais** (CRÍTICO)
**Localização**: `Modelo_G_J.xlsx`  
**Risco**: Arquivo binário - não conseguimos verificar conteúdo automaticamente

**O que verificar manualmente**:
- [ ] Abrir `Modelo_G_J.xlsx` em Excel
- [ ] Procurar por:
  - Nomes próprios
  - Números de telefone
  - Emails
  - NIFs/Números de identidade
  - Valores monetários reais
  - Qualquer PII (Personally Identifiable Information)

**Ação Recomendada**: Se contiver dados reais, remover ou substituir por dados fictícios.

**Prioridade**: 🔴 CRÍTICO

---

## 🟠 PROBLEMAS ALTOS

### 4. **agent.md - Contexto Interno Sensível** (ALTO)
**Localização**: `agent.md`  
**Risco**: Expõe contexto interno, requisitos e intenções

**Problema**:
```
Contexto: Sou um profissional de IT e quero criar uma ferramenta interna...
```

Este ficheiro revela:
- A profissão/departamento do criador
- Caso de uso específico (IRS)
- Stack tecnológica interna
- Estrutura de dados sensível (anexos, quadros)

**Ação Recomendada**:
1. **Opção A**: Remover ficheiro ou movê-lo para `.gitignore`
2. **Opção B**: Reescrito como documento público (sem informações pessoais/internas)
3. **Opção C**: Manter mas adicionar avisos de revisão antes de publicação

**Prioridade**: 🟠 ALTO

---

### 5. **Ausência de Ficheiro LICENSE** (ALTO)
**Localização**: Raiz do projeto  
**Risco**: Ambiguidade legal sobre direitos de uso/modificação

**Contexto**: Se é obra de Câmara Municipal, verificar:
- [ ] Qual a licença apropriada (LGPL, MIT, Apache 2.0, GPL)?
- [ ] Necessário aprovação jurídica da instituição?
- [ ] Contém código ou dados de propriedade?

**Ação Recomendada**:
- ✅ Adicionar ficheiro `LICENSE` na raiz (ex: LGPL 3.0, MIT)
- ✅ Adicionar clausula de copyright em `LICENSE`:
  ```
  Copyright (c) 2026 Câmara Municipal de Vila Nova de Gaia
  ```
- ✅ Adicionar referência em `README.md`

**Prioridade**: 🟠 ALTO

---

### 6. **Ausência de Ficheiro SECURITY.md** (ALTO)
**Localização**: Não existe  
**Risco**: Sem política de divulgação de vulnerabilidades

**Conteúdo Recomendado**:
```markdown
# Política de Segurança

## Reportar Vulnerabilidades

Se encontraste uma vulnerabilidade, **não abras uma issue pública**.
Contacta-nos em: **[email]**

Inclui:
- Descrição da vulnerabilidade
- Passos para reproduzir
- Impacto potencial

Responderemos no máximo em 5 dias úteis.
```

**Ação Recomendada**: Criar `SECURITY.md` na raiz

**Prioridade**: 🟠 ALTO

---

### 7. **Ausência de CODEOWNERS** (ALTO)
**Localização**: Não existe `.github/CODEOWNERS`  
**Risco**: Sem clareza sobre responsáveis e aprovadores

**Ação Recomendada**: Criar `.github/CODEOWNERS`:
```
# Proprietários padrão (toda a repo)
* @marco-owner-github-username

# Específico para ficheiros críticos
SECURITY.md @marco-owner-github-username
LICENSE @institutionalowner
```

**Prioridade**: 🟠 ALTO

---

## 🟡 PROBLEMAS MÉDIOS

### 8. **.gitignore Incompleto** (MÉDIO)
**Localização**: `.gitignore`  
**Problema**: Ignora `*.xml` mas deveria ser mais específico

**Config Atual**:
```
# Ficheiros de teste e Saidas
*.xml
*.log
```

**Problema**: Isto vai ignorar **todos** os XMLs, incluindo versões futuras legítimas.

**Ação Recomendada**: Ser mais específico:
```
# Ficheiros de teste e Saídas
test_data/
output/
IRS_*.xml
*.xml.bak
*.log

# Opcional - dados de rascunhos:
/data/
*.xlsx
```

**Prioridade**: 🟡 MÉDIO

---

### 9. **Falta requirements.txt com Versões Pinned** (MÉDIO)
**Localização**: Não existe  
**Risco**: Compatibilidade futura não garantida

**Ação Recomendada**: Criar `requirements.txt`:
```
streamlit==1.28.0
pandas==2.0.0
openpyxl==3.10.0
```

**Prioridade**: 🟡 MÉDIO

---

### 10. **Falta .python-version** (MÉDIO)
**Localização**: Não existe  
**Risco**: Ambiguidade sobre qual versão Python usar

**Ação Recomendada**: Criar `.python-version`:
```
3.10
```

**Prioridade**: 🟡 MÉDIO

---

## 🟢 RECOMENDAÇÕES ADICIONAIS (BAIXO)

### 11. **Adicionar CODIGO_CONDUTA.md** (BAIXO)
**Sugestão**: Incluir código de conduta para contribuidores (se pretendido)

---

### 12. **Adicionar CONTRIBUTING.md** (BAIXO)
**Sugestão**: Documentar processo de contribuição

---

## ✅ CHECKLIST PRÉ-PUBLICAÇÃO

### ANTES DE FAZER `git push` PARA REPOSITÓRIO PÚBLICO:

**CRÍTICO**:
- [ ] 1. Sanitizar IRS_2026_9.xml - NIFs e IBAN
- [ ] 2. Verificar Modelo_G_J.xlsx - PII
- [ ] 3. Revisar agent.md - contexto interno

**ALTO** (Recomendado):
- [ ] 4. Adicionar LICENSE
- [ ] 5. Criar SECURITY.md
- [ ] 6. Criar .github/CODEOWNERS
- [ ] 7. Atualizar .gitignore
- [ ] 8. Criar requirements.txt
- [ ] 9. Criar .python-version

**MÉDIO**:
- [ ] 10. Adicionar CODIGO_CONDUTA.md
- [ ] 11. Adicionar CONTRIBUTING.md
- [ ] 12. Verificar caminhos de ficheiros (nenhum path absoluto)
- [ ] 13. Fazer `git log --all --full-history -- <file>` para confirmar dados sensíveis não no histórico

---

## 🔍 VERIFICAÇÕES FINAIS

### Comandos para Validar Antes de Publicar:

```bash
# 1. Procurar por NIFs (padrão: 9 dígitos)
grep -r "[0-9]\{9\}" --include="*.xml" --include="*.md"

# 2. Procurar por IBANs (PT + 24 caracteres)
grep -r "PT[0-9]\{24\}" --include="*.xml"

# 3. Procurar por emails
grep -r "[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}" --include="*.md" --include="*.xml"

# 4. Verificar histórico Git
git log --all --oneline -- IRS_2026_9.xml

# 5. Procurar palavras-chave sensíveis
grep -ri "password\|secret\|token\|api_key\|private" --include="*.py" --include="*.md"
```

---

## 📊 RISCO FINAL ANTES DE PUBLICAÇÃO

| Item | Risco | Status | Ação |
|------|-------|--------|------|
| Dados PII (NIF, IBAN) | 🔴 CRÍTICO | ⚠️ Não | Sanitizar ficheiro XML |
| Dados Excel | 🔴 CRÍTICO | ⏳ Por verificar | Revisar manualmente |
| Context Interno | 🟠 ALTO | ⚠️ Não | Remover ou reescrever |
| Licensing | 🟠 ALTO | ❌ Não | Adicionar LICENSE |
| Security Policy | 🟠 ALTO | ❌ Não | Criar SECURITY.md |
| Governance | 🟠 ALTO | ❌ Não | Criar CODEOWNERS |
| Dependencies | 🟡 MÉDIO | ⚠️ Implícitas | Criar requirements.txt |

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

### Fase 1: CRÍTICO (Fazer Agora)
1. Sanitizar `IRS_2026_9.xml` - substituir NIFs e IBAN
2. Verificar `Modelo_G_J.xlsx`
3. Revisar `agent.md`

### Fase 2: ALTO (Fazer Antes de Push Público)
1. Criar `LICENSE`
2. Criar `SECURITY.md`
3. Criar `.github/CODEOWNERS`
4. Atualizar `.gitignore`

### Fase 3: MÉDIO (Recomendado)
1. Criar `requirements.txt`
2. Criar `.python-version`
3. Criar `CONTRIBUTING.md`

### Fase 4: VALIDAÇÃO FINAL
1. Executar comandos grep acima
2. Revisar histórico Git: `git log --oneline`
3. Revisar `README.md` para clareza
4. Testar clone + setup localmente

---

## 📞 Questões para Clarificar

1. **A Câmara Municipal autoriza publicação?**
   - Está autorizado publicar este código como open-source?
   - Qual a licença apropriada?

2. **O dados de exemplo são sensíveis?**
   - O NIF 218448660 é válido ou fictício?
   - A conta IBAN é teste?

3. **Confidencialidade de requisitos**:
   - Pode o `agent.md` com contexto estar público?
   - Há qualquer segredo comercial/municipal no código?

---

## ✨ Exemplo de Sanitização - IRS_2026_9.xml

### ANTES (❌ NÃO PUBLICAR):
```xml
<Q03C01>218448660</Q03C01>
<Q09C01>PT50001000002541720000196</Q09C01>
<Q11C01>505366215</Q11C01>
```

### DEPOIS (✅ PUBLICAR):
```xml
<!-- NIF de Teste - Fictício para demonstração -->
<Q03C01>000000000</Q03C01>
<!-- IBAN de Teste - Formato válido mas conta fictícia -->
<Q09C01>PT50 0000 0000 0000 0000 0000</Q09C01>
<!-- NIF de Teste - Fictício para demonstração -->
<Q11C01>111111111</Q11C01>
```

---

**Relatório Gerado**: 16 de Abril 2026  
**Próxima Revisão**: Após implementação de correções  
**Responsável**: Validação de Segurança Pre-Publicação
