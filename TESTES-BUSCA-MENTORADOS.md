# 🧪 Testes de Busca de Mentorados

Documentação completa dos testes de extração de nomes e busca no banco de dados.

## 📋 Resumo dos Testes

### ✅ O Que Funciona Bem

| Mensagem | Resultado | Status |
|----------|-----------|--------|
| "Como está o Pablo?" | Pablo Santos (ID 1) | ✅ Único |
| "Status da Silvane" | Silvane Castro (ID 2) | ✅ Único |
| "Juliana está ok?" | Juliana Altavilla (ID 4) | ✅ Único |
| "Última call da Dani" | Dani Silva (ID 5) | ✅ Único |
| "Como está a Juliana Altavilla?" | Juliana Altavilla (ID 4) | ✅ Nome completo |
| "Como está o Pablo e a Silvane?" | 2 mentorados | ✅ Múltiplos nomes |

### ⚠️ Requer Clarificação

| Mensagem | Resultado | Ação |
|----------|-----------|------|
| "Como está o Rafael?" | 3 Rafaéis Castro | ⚠️ Listar opções |
| "Status do Castro" | 4 pessoas Castro | ⚠️ Pedir clarificação |

### ❌ Não Identificado (Correto)

| Mensagem | Resultado | Motivo |
|----------|-----------|--------|
| "Quem precisa atenção?" | Nenhum nome | ✅ Consulta genérica |
| "Como está o João?" | Nenhum nome | ✅ Não cadastrado |

---

## 🎯 Melhorias Implementadas na V2

### 1. Filtro de Stopwords
Remove palavras comuns que não são nomes:
- Artigos: o, a, os, as
- Preposições: de, do, da, em, no
- Verbos: está, tá, como, foi
- Outros: ok, que, quando, onde

### 2. Validação contra Lista Conhecida
Só aceita nomes que estão na lista de primeiros nomes ou sobrenomes conhecidos:
```python
PRIMEIROS_NOMES = {'pablo', 'silvane', 'rafael', 'juliana', ...}
SOBRENOMES = {'santos', 'castro', 'altavilla', 'silva', ...}
```

### 3. Suporte para Nome Completo
- "Juliana Altavilla" → busca exata
- "Silvane Castro" → busca precisa
- Reduz ambiguidade

### 4. Detecção de Múltiplos Nomes
- "Pablo e Silvane" → processa ambos
- Identifica se algum tem ambiguidade
- Sugere ação correta

### 5. Identificação de Consultas Genéricas
- "Quem precisa atenção?" → usar `buscarTodasUrgencias()`
- Não tenta extrair nome

---

## 🔧 Integração com Banco Real

### Passo 1: Atualizar Lista de Nomes Conhecidos

Você precisa popular as listas com os nomes reais do banco:

```sql
-- Buscar todos os primeiros nomes
SELECT DISTINCT
  LOWER(SPLIT_PART(nome, ' ', 1)) as primeiro_nome
FROM mentorados
ORDER BY primeiro_nome;

-- Buscar todos os sobrenomes
SELECT DISTINCT
  LOWER(SPLIT_PART(nome, ' ', 2)) as sobrenome
FROM mentorados
WHERE SPLIT_PART(nome, ' ', 2) != ''
ORDER BY sobrenome;
```

### Passo 2: Adicionar Nomes no Script ou no Agente

**Opção A: Atualizar o script Python**
```python
PRIMEIROS_NOMES = {
    'pablo', 'silvane', 'rafael', 'juliana', 'dani',
    # ... adicionar todos os primeiros nomes do banco
}

SOBRENOMES = {
    'santos', 'castro', 'altavilla', 'silva',
    # ... adicionar todos os sobrenomes do banco
}
```

**Opção B: No Agente n8n (RECOMENDADO)**

O agente já faz a busca no banco com `LIKE`, então não precisa de lista fixa.
A validação acontece automaticamente quando a busca retorna resultados.

### Passo 3: Testar com Banco Real

```bash
# 1. Conectar ao banco Supabase
# 2. Executar teste manual:

# Teste 1: Nome único
curl -X POST https://seu-n8n.com/webhook/consulta-mentorado \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "data": {
        "key": {"id": "test1"},
        "message": {"conversation": "Como está o Pablo?"}
      }
    }
  }'

# Teste 2: Múltiplos resultados
curl -X POST https://seu-n8n.com/webhook/consulta-mentorado \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "data": {
        "key": {"id": "test2"},
        "message": {"conversation": "Como está o Rafael?"}
      }
    }
  }'
```

---

## 📊 Fluxo de Busca no Agente

```
Mensagem: "Como está o Rafael?"
         │
         ▼
┌─────────────────────┐
│  Agente Consulta    │
│  (extrai "Rafael")  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Tool: buscarMentorado("Rafael")    │
│                                     │
│  SQL:                               │
│  SELECT * FROM mentorados           │
│  WHERE nome LIKE '%Rafael%'         │
└──────────┬──────────────────────────┘
           │
           ▼
     ┌─────────┐
     │ 3 results│
     └────┬─────┘
          │
          ▼
┌────────────────────────────────────────┐
│  Agente analisa resultados:            │
│  - Múltiplos resultados encontrados    │
│  - System prompt instrui a listar      │
│  - Pedir clarificação                  │
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  Resposta para WhatsApp:               │
│                                        │
│  "Encontrei 3 mentorados com 'Rafael': │
│   1. Rafael Castro (ID 3) - Tech       │
│   2. Rafael Castro (ID 8) - Design     │
│   3. Rafael Castro (ID 15) - Vendas    │
│                                        │
│  Qual deles você quer?"                │
└────────────────────────────────────────┘
```

---

## 🎬 Casos de Uso Reais

### Caso 1: Consulta Única
```
User (WhatsApp): "Como está o Pablo?"

Agente:
1. Extrai: "Pablo"
2. Busca: buscarMentorado("Pablo")
3. Resultado: 1 mentorado
4. Prossegue: buscarCalls, buscarMensagens, etc.
5. Responde: Status completo do Pablo
```

### Caso 2: Múltiplos Resultados
```
User (WhatsApp): "Como está o Rafael?"

Agente:
1. Extrai: "Rafael"
2. Busca: buscarMentorado("Rafael")
3. Resultado: 3 mentorados
4. PARA e lista opções
5. Aguarda clarificação

User (WhatsApp): "O intermediário"

Agente:
1. Identifica: ID 8
2. Prossegue com consulta
3. Responde: Status do Rafael Castro (ID 8)
```

### Caso 3: Múltiplos Nomes
```
User (WhatsApp): "Como está o Pablo e a Silvane?"

Agente:
1. Extrai: ["Pablo", "Silvane"]
2. Busca ambos
3. Ambos únicos → processa separadamente
4. Responde:

   📊 PABLO SANTOS
   [status completo]

   📊 SILVANE CASTRO
   [status completo]
```

### Caso 4: Consulta Genérica
```
User (WhatsApp): "Quem precisa atenção?"

Agente:
1. Detecta: consulta genérica
2. Usa: buscarTodasUrgencias()
3. Retorna: lista de mentorados críticos
4. Responde:

   🔴 PRECISAM ATENÇÃO:
   • Rafael (3 eventos urgentes)
   • Silvane (call há 18 dias)
   ...
```

---

## 🐛 Troubleshooting

### Problema 1: "Agente não encontra mentorado conhecido"

**Diagnóstico:**
```sql
-- Verificar se nome está no banco
SELECT id, nome FROM mentorados WHERE nome LIKE '%Pablo%';
```

**Soluções:**
1. Verificar ortografia
2. Tentar nome completo
3. Tentar sobrenome
4. Verificar se está ativo

### Problema 2: "Muitos falsos positivos"

**Causa:** Palavras comuns sendo interpretadas como nomes

**Solução:** Atualizar STOPWORDS no script ou ajustar regex

### Problema 3: "Não detecta nome completo"

**Causa:** Regex não captura dois nomes

**Solução:** Usar padrões que capturam sobrenome:
```python
# Exemplo:
r'como\s+está\s+(?:o|a)\s+([a-z]+)(?:\s+([a-z]+))?'
```

### Problema 4: "Agente não pede clarificação"

**Causa:** System prompt não está configurado corretamente

**Solução:** Verificar seção do system prompt sobre buscarMentorado:
```
**Se retornar múltiplos:**
- Liste TODOS com ID
- Peça qual deles a Queila quer
- NÃO prossiga até confirmar
```

---

## ✅ Checklist de Validação

Antes de colocar em produção, teste:

### Testes Básicos
- [ ] Nome único retorna 1 resultado
- [ ] Nome duplicado lista opções
- [ ] Nome não cadastrado informa erro
- [ ] Nome completo funciona corretamente

### Testes de Múltiplos Nomes
- [ ] "Pablo e Silvane" processa ambos
- [ ] Se um for ambíguo, lista TODOS os ambíguos
- [ ] NÃO processa parcialmente

### Testes de Consultas Genéricas
- [ ] "Quem precisa atenção?" usa buscarTodasUrgencias
- [ ] "Alguém está travado?" responde adequadamente
- [ ] Não tenta extrair nome de consulta genérica

### Testes de Edge Cases
- [ ] Nome com acento (Érica)
- [ ] Nome com ç (Conceição)
- [ ] Nome curto (Ana, Léo)
- [ ] Sobrenome composto (Silva Santos)

### Testes de Performance
- [ ] Busca retorna em < 2s
- [ ] Múltiplas buscas paralelas funcionam
- [ ] Memória de contexto funciona (segunda pergunta)

---

## 📈 Métricas de Sucesso

Após implementar, monitore:

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Taxa de identificação correta | >90% | Logs do agente |
| Taxa de ambiguidade resolvida | >80% | Follow-up messages |
| Tempo médio de resposta | <3s | Logs do n8n |
| Satisfação do usuário | >4/5 | Feedback manual |

---

## 🚀 Próximos Passos

1. **Implementar no n8n** seguindo GUIA-INTEGRACAO.md
2. **Testar com banco real** usando casos de teste acima
3. **Monitorar primeiros dias** e ajustar regex se necessário
4. **Documentar casos específicos** que aparecerem
5. **Otimizar performance** se busca ficar lenta

---

## 📚 Arquivos Relacionados

- **test-extract-names.py** - Versão inicial (com falsos positivos)
- **test-extract-names-v2.py** - Versão melhorada (recomendada)
- **GUIA-INTEGRACAO.md** - Como integrar no workflow
- **README.md** - Visão geral do projeto

---

**Última atualização:** 2025-10-21
**Status:** ✅ Pronto para integração
