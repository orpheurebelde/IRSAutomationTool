# 🔒 RELATÓRIO BANDIT - Análise de Segurança

**Data**: 16 de Abril de 2026  
**Analisador**: Bandit v1.7+  
**Ficheiro**: app.py  
**Linhas de Código**: 867  

---

## 📊 RESULTADO GERAL

| Métrica | Valor |
|---------|-------|
| Total de Vulnerabilidades | 2 |
| Severidade BAIXA | 1 |
| Severidade MÉDIA | 1 |
| Severidade ALTA | 0 |
| Linhas Skipped | 0 |

---

## 🔴 VULNERABILIDADES IDENTIFACADAS

### 1. [B405] Import xml.etree.ElementTree

**Severidade**: 🟡 BAIXA  
**Confiança**: ALTA  
**Localização**: app.py, linha 3  
**CWE**: CWE-20 (Improper Input Validation)

#### Problema
```python
import xml.etree.ElementTree as ET
```

O módulo `xml.etree.ElementTree` é vulnerável a ataques XML (XXE - XML External Entity Injection, Billion Laughs Attack, etc).

#### Recomendação
Substituir por `defusedxml`:

```python
from defusedxml import ElementTree as ET
```

#### Impacto
- **Alta**: Se o XML provém de fonte não confiável
- **Média**: Este projecto processa XMLs do utilizador (upload de ficheiro)

---

### 2. [B314] xml.etree.ElementTree.fromstring

**Severidade**: 🔴 MÉDIA  
**Confiança**: ALTA  
**Localização**: app.py, linha 675  
**CWE**: CWE-20 (Improper Input Validation)

#### Problema
```python
root = ET.fromstring(xml_string)
```

Usando `ET.fromstring()` para fazer parse de XML não validado/não confiável.

#### Recomendação
Substituir por `defusedxml`:

```python
from defusedxml.ElementTree import fromstring
root = fromstring(xml_string)
```

Ou se preferir manter `ET.`:

```python
from defusedxml.ElementTree import fromstring as defused_fromstring
root = defused_fromstring(xml_string)
```

#### Impacto
- **CRÍTICO**: Este método está no fluxo de upload de ficheiro XML
- **Risco Real**: Um utilizador poderia fazer upload de XML malicioso

---

## ✅ PLANO DE CORREÇÃO

### Passo 1: Instalar defusedxml
```bash
pip install defusedxml
```

Adicionar a `requirements.txt`:
```
defusedxml>=0.0.28
```

### Passo 2: Atualizar Imports (app.py linha 3)

**ANTES**:
```python
import xml.etree.ElementTree as ET
```

**DEPOIS**:
```python
from defusedxml.ElementTree import parse, fromstring
import xml.etree.ElementTree as ET  # Se necessário para compatibility
```

### Passo 3: Atualizar app.py linha 675

**ANTES**:
```python
root = ET.fromstring(xml_string)
```

**DEPOIS**:
```python
from defusedxml.ElementTree import fromstring
root = fromstring(xml_string)
```

### Passo 4: Verificação
```bash
python -m bandit app.py
# Resultado esperado: 0 vulnerabilidades
```

---

## 📈 CONTEXTO DO PROJECTO

Este projecto é uma aplicação **Streamlit** que:
- ✅ Aceita upload de ficheiros XML
- ✅ Faz parse e manipulação de XML
- ✅ Exporta XML modificado

**Risco**: Médio-Alto (utilizadores podem upload malicious XML)

---

## 🛡️ OUTRAS RECOMENDAÇÕES DE SEGURANÇA

1. **Validação de XML Schema**
   - Considerar validar XML contra schema (XSD) antes do parse

2. **Limite de Tamanho**
   - Implementar limite de tamanho de ficheiro XML

3. **Rate Limiting**
   - Adicionar proteção contra DoS

4. **Logging de Segurança**
   - Log de tentativas de upload suspeitos

---

## 🔍 REFERÊNCIAS

- [Bandit B405 Documentation](https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b405-import-xml-etree)
- [Bandit B314 Documentation](https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b313-b320-xml-bad-elementtree)
- [defusedxml Documentation](https://github.com/tiran/defusedxml)
- [OWASP XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

---

## 📝 PRÓXIMOS PASSOS

1. Instalar defusedxml
2. Atualizar app.py com imports seguro
3. Reexecutar Bandit para validar
4. Commit das mudanças
5. Manter verificação de segurança periódica

---

**Status**: 🟡 ATIVO - Requer Correção  
**Prioridade**: ALTA (para repositório público)  
**Gerado por**: Bandit Security Linter
