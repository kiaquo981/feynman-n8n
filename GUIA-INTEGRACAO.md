# 🔧 Guia de Integração - Webhook no Workflow Principal

## 📋 Visão Geral

Você tem 2 opções para fazer a integração:

### Opção A: Modificação Manual no n8n (Recomendado)
Mais visual, você vê o que está fazendo passo a passo.

### Opção B: Script Python Automático
Mais rápido, mas precisa reimportar o workflow.

---

## 🎯 Opção A: Modificação Manual (Passo a Passo)

### Passo 1: Adicionar Nó "Preparar para Agente"

1. **Clique no canvas** próximo ao nó "Switch"
2. **Adicione um nó "Code"**
3. **Renomeie** para "Preparar para Agente"
4. **Cole este código:**

```javascript
const roteador = $('Roteador').first().json;

// Formato esperado pelo Agente
return [{
  json: {
    sessionId: roteador.message?.message_id || `${Date.now()}`,
    pergunta: roteador.query,
    from: roteador.message?.chat_id || roteador.sender?.telefone,
    sender_phone: roteador.sender?.telefone || '5511964682447',
    // Dados extras para contexto
    sender_name: roteador.sender?.nome || 'Queila',
    is_group: roteador.message?.is_group || false
  }
}];
```

### Passo 2: Adicionar Nó "Enviar Resposta WhatsApp"

1. **Adicione um nó "HTTP Request"**
2. **Renomeie** para "Enviar Resposta WhatsApp"
3. **Configure:**

**Authentication:** None

**Method:** POST

**URL:**
```
https://evolution.manager01.feynmanproject.com/message/sendText/produ02
```

**Send Headers:** Ativado
- Name: `apikey`
- Value: `BAD515E8A35F-438C-AF16-77FCDC7D2DAC`

**Send Body:** Ativado
- Parameter 1:
  - Name: `number`
  - Value: `={{ $('Preparar para Agente').first().json.sender_phone }}`
- Parameter 2:
  - Name: `text`
  - Value: `={{ $json.output }}`

### Passo 3: Conectar os Nós

**Conexão 1:** Switch (saída CONSULTA) → Preparar para Agente
1. Clique no nó "Switch"
2. Arraste da **saída "CONSULTA"** (terceira saída)
3. Conecte ao nó "Preparar para Agente"

**Conexão 2:** Preparar para Agente → Agente Consulta
1. Arraste da saída do "Preparar para Agente"
2. Conecte ao nó "Agente Consulta"

**Conexão 3:** Agente Consulta → Enviar Resposta WhatsApp
1. Arraste da saída do "Agente Consulta"
2. Conecte ao nó "Enviar Resposta WhatsApp"

### Passo 4: Desabilitar Fluxo Antigo (Opcional)

Para manter o workflow limpo, você pode:

**Opção 1:** Deletar os nós antigos da consulta
**Opção 2:** Desabilitar clicando em cada nó e marcando "Disabled"

Nós para desabilitar/deletar:
- Preparar Consulta
- Analisar Consulta (GPT-4)
- Parse Intent
- Switch1
- Buscar Mentorado por Nome
- Validar Mentorado
- Query Inteligente
- Code in JavaScript1 até Code in JavaScript6
- Buscar Calls Dinâmico
- Buscar Interações
- Buscar Direcionamentos
- Buscar Diagnóstico
- Buscar Compromissos
- Buscar Métricas
- Construir Contexto Inteligente
- Prompt Conversacional Focado
- Construir Contexto Denso
- Gerar Resposta
- Enviar Resposta (o antigo)
- Análise Global
- Buscar Todos Mentorados
- Buscar Todas Interações

### Passo 5: Desabilitar Webhook Separado (Opcional)

Você pode manter o webhook separado para testes, ou desabilitar:
- Webhook Entrada
- Normalizar Entrada
- Responder (do webhook)

### Passo 6: Salvar e Ativar

1. **Clique em "Save"**
2. **Ative o workflow** (toggle no canto superior direito)

---

## 🚀 Opção B: Script Python Automático

### Pré-requisitos

```bash
python3 --version  # Verificar se tem Python 3
```

### Passos

1. **Exporte o workflow atual do n8n:**
   - Abra o workflow no n8n
   - Menu → Download
   - Salve como `workflow-original.json`

2. **Coloque os arquivos juntos:**
```
/home/user/feynman-n8n/
├── workflow-original.json       (exportado do n8n)
└── modificar-workflow.py        (script criado)
```

3. **Execute o script:**
```bash
cd /home/user/feynman-n8n/
python3 modificar-workflow.py
```

4. **Importe o workflow modificado:**
   - n8n → Workflows → Import from File
   - Selecione `workflow-modificado.json`

---

## 🧪 Testando a Integração

### Teste 1: Consulta Simples

Envie via WhatsApp (do número da Queila):
```
Como está o Pablo?
```

**Fluxo esperado:**
1. ✅ Webhook recebe mensagem
2. ✅ Roteador detecta `route: "consulta"`
3. ✅ Switch direciona para CONSULTA
4. ✅ Preparar para Agente formata dados
5. ✅ Agente Consulta processa
6. ✅ Resposta enviada para WhatsApp

### Teste 2: Consulta com Contexto

```
Quando foi a última call da Silvane?
```

**Deve buscar:**
- buscarMentorado("Silvane")
- buscarCalls(mentorado_id, limit=1)
- Retornar data e resumo

### Teste 3: Urgências

```
Quem precisa atenção?
```

**Deve buscar:**
- buscarTodasUrgencias()
- Listar mentorados com eventos urgentes

---

## 🐛 Troubleshooting

### Problema: "Agente não encontra mentorado"

**Causa:** Banco de dados não tem o mentorado ou nome está diferente

**Solução:**
```sql
SELECT id, nome FROM mentorados WHERE nome LIKE '%Pablo%';
```

### Problema: "Resposta não chega no WhatsApp"

**Verificar:**
1. API key está correta
2. Número do telefone está no formato certo (5511...)
3. Evolution API está ativa

**Debug:**
```bash
# Testar manualmente a API
curl -X POST https://evolution.manager01.feynmanproject.com/message/sendText/produ02 \
  -H "apikey: BAD515E8A35F-438C-AF16-77FCDC7D2DAC" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511964682447",
    "text": "Teste de integração"
  }'
```

### Problema: "Agente não tem memória"

**Causa:** Session ID não está sendo passado corretamente

**Verificar:**
- No nó "Preparar para Agente", verificar se `sessionId` está sendo gerado
- No nó "Memory", verificar se `sessionKey` usa o session ID correto

---

## 📊 Diagrama do Fluxo Final

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBHOOK EVOLUTION API                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
           ┌─────────────────────┐
           │  Responder Webhook  │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │ Normalizar Webhook  │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │   Filtrar Válidos   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  Buscar Mentorado   │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │      Roteador       │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │       Switch        │
           └─┬──────┬──────────┬─┘
             │      │          │
    ┌────────┘      │          └──────────┐
    │               │                     │
    ▼               ▼                     ▼
PROCESSAR     PROCESSAR              CONSULTA ✨
PRIVADO        GRUPO                     │
    │               │                     ▼
    │               │          ┌─────────────────────┐
    │               │          │ Preparar p/ Agente  │ ← NOVO
    │               │          └──────────┬──────────┘
    │               │                     │
    │               │                     ▼
    │               │          ┌─────────────────────┐
    │               │          │   Agente Consulta   │
    │               │          │  ┌─────────────┐    │
    │               │          │  │ buscarMent. │    │
    │               │          │  │ buscarCalls │    │
    │               │          │  │ buscarMsgs  │    │
    │               │          │  │ buscarVendas│    │
    │               │          │  │ etc...      │    │
    │               │          │  └─────────────┘    │
    │               │          └──────────┬──────────┘
    │               │                     │
    ▼               ▼                     ▼
 Switch Tipo    Switch Tipo    ┌─────────────────────┐
   Mídia          Mídia        │ Enviar Resposta WA  │ ← NOVO
    │               │          └─────────────────────┘
    ▼               ▼                     │
  (Análise      (Análise                 ▼
   áudio,        áudio,              📱 WhatsApp
   imagem,       imagem,
   etc...)       etc...)
    │               │
    ▼               ▼
  Salvar        Salvar
  etc...        etc...
```

---

## ✅ Checklist Final

Após implementar, verifique:

- [ ] Nó "Preparar para Agente" criado e configurado
- [ ] Nó "Enviar Resposta WhatsApp" criado e configurado
- [ ] Switch (CONSULTA) conectado a "Preparar para Agente"
- [ ] "Preparar para Agente" conectado a "Agente Consulta"
- [ ] "Agente Consulta" conectado a "Enviar Resposta WhatsApp"
- [ ] Fluxo antigo desabilitado ou deletado
- [ ] Workflow salvo e ativado
- [ ] Teste 1 realizado com sucesso
- [ ] Teste 2 realizado com sucesso
- [ ] Teste 3 realizado com sucesso

---

## 📚 Próximos Passos

Após integração funcionando:

1. **Monitorar logs** - Ver se as consultas estão sendo processadas corretamente
2. **Ajustar prompts** - Melhorar respostas do agente conforme feedback
3. **Adicionar mais tools** - Se precisar de novos tipos de busca
4. **Otimizar performance** - Cache de consultas frequentes

---

## 💡 Dicas

- Mantenha o webhook separado desabilitado como backup
- Use o webhook separado para testar mudanças antes de aplicar no fluxo principal
- Monitore o uso de tokens do GPT-4 (está no nó "GPT-4o")
- Acompanhe as execuções no painel do n8n

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs de execução no n8n
2. Teste cada nó individualmente
3. Confira as conexões no diagrama visual
4. Valide os dados que estão sendo passados entre nós
