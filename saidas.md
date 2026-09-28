## P0
### Setup e leitura do corpus

**Evidência da Parte 0:** Tabela com doc_id, status e número de palavras de cada documento.

| doc_id | status | num_palavras |
|---|---|---|
| POL-001 | vigente | 164 |
| POL-002 | vigente | 136 |
| POL-003 | vigente | 128 |
| POL-004 | revogada | 90 |
| POL-005 | vigente | 119 |
| POL-006 | vigente | 117 |
| POL-007 | vigente | 114 |
| POL-008 | vigente | 119 |
| POL-009 | vigente | 142 |
| POL-010 | vigente | 92 |
| POL-011 | vigente | 102 |
| FAQ-001 | vigente | 145 |

---

## P1
### Chunking por seção

**Número total de chunks:** 46

**Número de chunks por documento:**
- FAQ-001: 6 chunks
- POL-002: 4 chunks
- POL-003: 4 chunks
- POL-006: 4 chunks
- POL-007: 4 chunks
- POL-008: 4 chunks
- POL-009: 4 chunks
- POL-011: 4 chunks
- POL-001: 3 chunks
- POL-004: 3 chunks
- POL-005: 3 chunks
- POL-010: 3 chunks

**Exemplo de Chunk Completo:**
- **doc_id:** POL-001
- **titulo:** Política de Onboarding
- **secao:** Objetivo
- **status:** vigente
- **texto:** Esta política define as etapas dos primeiros 30 dias de um novo colaborador na Horizonte Tech.

---

## P2
### Indexação com TF-IDF

**Forma da matriz:** 46 linhas por 328 colunas.

**Decisão de pré-processamento:** Optei remover acentos (strip_accents='unicode') e excluir uma lista customizada de stopwords em português (incluindo termos como 'qual', 'posso', 'quantos') para reduzir o ruído e focar nas palavras com maior peso, evitando falsos positivos na recuperação.

---

## P3
### Recuperação top-k com regra de vigência

**P01 - Pergunta:** Com quantos dias de antecedência devo solicitar minhas férias?

| Posição | doc_id | seção | score |
|---|---|---|---|
| 1 | POL-002 | Como solicitar | 0.41 |
| 2 | POL-002 | Venda de dias | 0.34 |
| 3 | POL-002 | Direito a férias | 0.23 |

**P02 - Pergunta:** Quantos dias por semana posso trabalhar de forma remota?

| Posição | doc_id | seção | score |
|---|---|---|---|
| 1 | POL-005 | Regra de trabalho remoto | 0.53 |
| 2 | FAQ-001 | Posso trabalhar remoto todos os dias? | 0.15 |
| 3 | FAQ-001 | Quem é o meu buddy? | 0.10 |

**P10 - Pergunta:** Qual é a política de estacionamento da empresa?

| Posição | doc_id | seção | score |
|---|---|---|---|
| 1 | POL-001 | Objetivo | 0.21 |
| 2 | POL-008 | Aviso | 0.20 |
| 3 | POL-003 | Auxílio para trabalho remoto | 0.20 |

---

