# Integração do Webhook no Workflow Principal

## Resumo das Mudanças

### Novos Nós Criados

#### 1. **Preparar para Agente** (Code)
**Posição:** Entre Switch (saída CONSULTA) e Agente Consulta
**Função:** Adaptar dados do Roteador para formato do Agente

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

#### 2. **Enviar Resposta WhatsApp** (HTTP Request)
**Posição:** Após Agente Consulta
**Função:** Enviar resposta do agente para WhatsApp

**Configuração:**
- **Method:** POST
- **URL:** `https://evolution.manager01.feynmanproject.com/message/sendText/produ02`
- **Headers:**
  - `apikey`: `BAD515E8A35F-438C-AF16-77FCDC7D2DAC`
- **Body:**
```json
{
  "number": "={{ $('Preparar para Agente').first().json.sender_phone }}",
  "text": "={{ $json.output }}"
}
```

### Conexões Modificadas

**ANTES:**
```
Switch (CONSULTA) → Preparar Consulta → ... (fluxo antigo)
```

**DEPOIS:**
```
Switch (CONSULTA) → Preparar para Agente → Agente Consulta → Enviar Resposta WhatsApp
```

## Passos para Implementar

### No Editor n8n:

1. **Deletar o fluxo antigo de consulta** (opcional - pode manter desabilitado):
   - Preparar Consulta
   - Analisar Consulta (GPT-4)
   - Parse Intent
   - Switch1
   - Buscar Mentorado por Nome
   - Validar Mentorado
   - Query Inteligente
   - Code in JavaScript1
   - Todos os nós de busca (Calls, Interações, etc.)
   - Construir Contexto Inteligente
   - Prompt Conversacional Focado
   - Construir Contexto Denso
   - Gerar Resposta

2. **Adicionar nó "Preparar para Agente":**
   - Tipo: Code
   - Código: (ver acima)
   - Posição: Logo após o Switch

3. **Adicionar nó "Enviar Resposta WhatsApp":**
   - Tipo: HTTP Request
   - Configuração: (ver acima)
   - Posição: Logo após Agente Consulta

4. **Modificar conexões:**
   - Switch saída "CONSULTA" → Preparar para Agente
   - Preparar para Agente → Agente Consulta
   - Agente Consulta → Enviar Resposta WhatsApp

5. **Remover/desabilitar webhook separado** (opcional):
   - Webhook Entrada
   - Normalizar Entrada
   - Responder (do webhook)

## Benefícios

✅ **Fluxo unificado** - Tudo em um único workflow
✅ **Reutiliza agente configurado** - Todas as tools já estão prontas
✅ **Mantém contexto** - Session ID preservado para memória
✅ **Mais simples** - Menos nós, mais fácil de manter

## Fluxo Final Completo

```
Webhook Evolution API
  ↓
Responder Webhook
  ↓
Normalizar Webhook
  ↓
Filtrar Válidos
  ↓
Buscar Mentorado
  ↓
Roteador
  ↓
Switch ━━━━━━━━━━━━━━━━━┳━━━ PROCESSAR_PRIVADO → Switch Tipo Mídia → ...
                         ┃
                         ┣━━━ PROCESSAR_GRUPO → Switch Tipo Mídia → ...
                         ┃
                         ┗━━━ CONSULTA → Preparar para Agente
                                           ↓
                                        Agente Consulta
                                           ↓
                                    Enviar Resposta WhatsApp
```

## Teste

Para testar, envie uma mensagem para o WhatsApp do número da Queila:
```
"Como está o Pablo?"
```

O fluxo deve:
1. Detectar que é consulta (Roteador)
2. Rotear para Agente (Switch)
3. Processar com agente (buscar dados)
4. Responder no WhatsApp
