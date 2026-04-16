# 🗺️ MAPA DE NAVEGAÇÃO - Validação de Segurança

**Bem-vindo!** Este mapa ajuda você a navegar nos documentos criados para publicação segura.

---

## 🎯 ONDE COMEÇAR?

### 👤 Se você é o DESENVOLVEDOR (Marco):

```
1️⃣  Comece AQUI:
    └─ [RESUMO_EXECUTIVO_VALIDACAO.md](RESUMO_EXECUTIVO_VALIDACAO.md)
       (2 min - Visão geral do que fazer)

2️⃣  Depois SIGA:
    └─ [GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md)
       (30 min - Passo a passo da sanitização)

3️⃣  Para referência COMPLETA:
    └─ [RELATORIO_VALIDACAO_SEGURANCA.md](RELATORIO_VALIDACAO_SEGURANCA.md)
       (10 min leitura - Contexto técnico completo)
```

### 👨‍⚖️ Se você é RESPONSÁVEL DE CONFORMIDADE:

```
1️⃣  Revise PRIMEIRO:
    └─ [LICENSE](LICENSE)
       (Meta-verificação: Copyright está correto?)

2️⃣  Depois VALIDE:
    └─ [SECURITY.md](SECURITY.md)
       (Política de segurança OK?)

3️⃣  E CONFIRME:
    └─ [CONTRIBUTING.md](CONTRIBUTING.md)
       (Diretrizes de contribuição apropriadas?)

4️⃣  Para GOVERNANÇA:
    └─ [.github/CODEOWNERS](.github/CODEOWNERS)
       (Responsáveis de código definidos?)
```

### 👨‍💼 Se você é GESTOR/SUPERVISOR:

```
1️⃣  Leia APENAS:
    └─ [RESUMO_EXECUTIVO_VALIDACAO.md](RESUMO_EXECUTIVO_VALIDACAO.md)
       (Status executivo - O que foi feito?)

2️⃣  Questões importantes:
    └─ "Estão os dados sensíveis identificados?" ✅ SIM
    └─ "Há um plano para sanitizar?" ✅ SIM
    └─ "Compliance foi criado?" ✅ SIM
    └─ "Quando fica pronto?" ⏳ Depende de PASSO 4 abaixo
```

---

## 📋 ESTRUTURA DOS DOCUMENTOS

```
📁 IRS/ (Repositório)
│
├─ 📄 RESUMO_EXECUTIVO_VALIDACAO.md ⭐ (COMECE AQUI)
│  └─ Visão geral executiva
│  └─ Checklist copy-paste
│  └─ Próximos passos rápidos
│
├─ 📄 RELATORIO_VALIDACAO_SEGURANCA.md
│  └─ Análise completa e detalhada
│  └─ Todos os problemas explicados
│  └─ Referência técnica completa
│
├─ 📄 GUIA_SANITIZACAO_DADOS.md 🔑 (FAZER ISTO AGORA)
│  └─ Instruções passo-a-passo
│  └─ Comandos para executar
│  └─ Verificações de conclusão
│
├─ 📄 LICENSE ✅
│  └─ MIT (Copyright Câmara)
│  └─ Pronto para publicação
│
├─ 📄 SECURITY.md ✅
│  └─ Política de divulgação de vul.
│  └─ Pronto para publicação
│
├─ 📄 CONTRIBUTING.md ✅
│  └─ Guia de contribuição
│  └─ Pronto para publicação
│
├─ 📄 EXEMPLO_IRS_SANITIZADO.xml
│  └─ Ficheiro XML com dados fictícios
│  └─ Pode usar como referência
│
├─ 📁 .github/
│  └─ 📄 CODEOWNERS ✅
│     └─ Governança de código
│     └─ Pronto para publicação
│
├─ 📄 requirements.txt ✅
│  └─ Dependências pinned
│  └─ Pronto para publicação
│
├─ 📄 .python-version ✅
│  └─ Versão Python
│  └─ Pronto para publicação
│
└─ 📄 .gitignore ✅
   └─ Padrões atualizados
   └─ Pronto para publicação
```

---

## 🎯 FLUXO DE TRABALHO

### Passo por Passo:

```
┌─────────────────────────────────────────────┐
│  1. LER                                      │
│  [RESUMO_EXECUTIVO_VALIDACAO.md] ⭐ (2 min) │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  2. EXECUTAR                                 │
│  [GUIA_SANITIZACAO_DADOS.md] 🔑 (30 min)    │
│  └─ PASSO 1: IRS_2026_9.xml                │
│  └─ PASSO 2: Modelo_G_J.xlsx               │
│  └─ PASSO 3: agent.md                      │
│  └─ PASSO 4: Histórico Git                 │
│  └─ PASSO 5: Validação Final               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  3. RESOLVER DÚVIDAS                         │
│  [RELATORIO_VALIDACAO_SEGURANCA.md] (ref)   │
│  │  └─ Se não sabe por que fazer algo      │
│  │  └─ Se encontrar erros                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  4. PUBLICAR                                 │
│  git push origin main (após sanitização)    │
│  Git hub: Settings > Make Public            │
└─────────────────────────────────────────────┘
```

---

## 🔍 RÁPIDA VERIFICAÇÃO: O QUE ESTÁ PRONTO?

| Item | Status | Ficheiro |
|------|--------|----------|
| 🔴 NIFs e IBAN em XML | ⏳ TODO | Sanitizar [GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md) |
| 🔴 PII em Modelo_G_J.xlsx | ⏳ TODO | Verificar manualmente |
| 🔴 Context em agent.md | ⏳ TODO | Remover ou reescrever |
| 🟢 LICENSE | ✅ PRONTO | [LICENSE](LICENSE) |
| 🟢 SECURITY.md | ✅ PRONTO | [SECURITY.md](SECURITY.md) |
| 🟢 CONTRIBUTING.md | ✅ PRONTO | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 🟢 CODEOWNERS | ✅ PRONTO | [.github/CODEOWNERS](.github/CODEOWNERS) |
| 🟢 requirements.txt | ✅ PRONTO | [requirements.txt](requirements.txt) |
| 🟢 .python-version | ✅ PRONTO | [.python-version](.python-version) |
| 🟢 .gitignore | ✅ ATUALIZADO | [.gitignore](.gitignore) |

---

## 💡 DICAS RÁPIDAS

### Se está com pressa:
```
Execute APENAS:
1. Abra GUIA_SANITIZACAO_DADOS.md
2. Siga PASSO 1-5 (30 min)
3. Done! Pronto para push
```

### Se quer entender tudo:
```
Ordem de leitura:
1. RESUMO_EXECUTIVO_VALIDACAO.md (visão geral)
2. RELATORIO_VALIDACAO_SEGURANCA.md (detalhe técnico)
3. GUIA_SANITIZACAO_DADOS.md (ação prática)
4. Ficheiros de compliance (LICENSE, SECURITY.md, etc)
```

### Se tiver um erro específico:
```
Procure no índice de [RELATORIO_VALIDACAO_SEGURANCA.md]:
- Problema 1: NIFs -> Solução em GUIA > PASSO 1
- Problema 2: IBAN -> Solução em GUIA > PASSO 1
- Problema 3: Excel -> Solução em GUIA > PASSO 2
- Problema 4: agent.md -> Solução em GUIA > PASSO 3
- Problema 5: Git History -> Solução em GUIA > PASSO 4
```

---

## 📞 PERGUNTAS E RESPOSTAS

**P: Por onde começo?**  
A: [RESUMO_EXECUTIVO_VALIDACAO.md](RESUMO_EXECUTIVO_VALIDACAO.md) (2 min)

**P: Como sanitizo os dados?**  
A: [GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md) (30 min)

**P: Por que preciso fazer isto?**  
A: [RELATORIO_VALIDACAO_SEGURANCA.md](RELATORIO_VALIDACAO_SEGURANCA.md) (contexto completo)

**P: E as licenças e compliance?**  
A: Já está criado! [LICENSE](LICENSE), [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md)

**P: Quanto tempo leva tudo?**  
A: ~45 minutos (leitura + sanitização + teste)

**P: Posso fazer isto depois?**  
⚠️ Não. Fazer antes de push público é CRÍTICO.

---

## ✅ CHECKLIST VISUAL

```
SEGURANÇA PRÉ-PUBLICAÇÃO:

Dados Confidenciais:
  ☐ IRS_2026_9.xml - NIFs sanitizados
  ☐ IRS_2026_9.xml - IBAN sanitizado
  ☐ Modelo_G_J.xlsx - PII verificado
  ☐ agent.md - Revisado/Removido

Compliance (Já Criado):
  ✅ LICENSE
  ✅ SECURITY.md
  ✅ CONTRIBUTING.md
  ✅ .github/CODEOWNERS
  ✅ requirements.txt
  ✅ .python-version
  ✅ .gitignore

Documentação (Já Criada):
  ✅ RESUMO_EXECUTIVO_VALIDACAO.md
  ✅ RELATORIO_VALIDACAO_SEGURANCA.md
  ✅ GUIA_SANITIZACAO_DADOS.md
  ✅ EXEMPLO_IRS_SANITIZADO.xml

PRÓXIMO: 
  → Abra GUIA_SANITIZACAO_DADOS.md
  → Siga PASSO 1-5
  → Execute checklist
  → Push para público
```

---

## 🚀 ATALHOS RÁPIDOS

**Para o desenvolvedor:**
- 📖 Resumo Quick: [RESUMO_EXECUTIVO_VALIDACAO.md](RESUMO_EXECUTIVO_VALIDACAO.md)
- 🔧 Como fazer: [GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md)
- 🔍 Entender tudo: [RELATORIO_VALIDACAO_SEGURANCA.md](RELATORIO_VALIDACAO_SEGURANCA.md)

**Para review de compliance:**
- ⚖️ Licença: [LICENSE](LICENSE)
- 🔒 Segurança: [SECURITY.md](SECURITY.md)
- 🤝 Contribuições: [CONTRIBUTING.md](CONTRIBUTING.md)

**Para verificações técnicas:**
- 📋 Governança: [.github/CODEOWNERS](.github/CODEOWNERS)
- 📦 Deps: [requirements.txt](requirements.txt)
- 🐍 Python: [.python-version](.python-version)
- .ignore: [.gitignore](.gitignore)

---

**Versão**: 1.0  
**Data**: 16 de Abril 2026  
**Status**: 🟢 Pronto para usar

---

# ⭐ COMECE AQUI:

→ **[RESUMO_EXECUTIVO_VALIDACAO.md](RESUMO_EXECUTIVO_VALIDACAO.md)** (2 min)  
→ **[GUIA_SANITIZACAO_DADOS.md](GUIA_SANITIZACAO_DADOS.md)** (30 min)  
→ **git push** (quando pronto!)
