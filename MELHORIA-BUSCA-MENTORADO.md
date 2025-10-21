# 🔄 Melhoria: Buscar Mentorado ANTES do Switch

## 📋 Análise do Fluxo Atual

### Fluxo Existente:
```
Webhook Evolution API
  ↓
Responder Webhook
  ↓
Normalizar Webhook (extrai sender_phone)
  ↓
Filtrar Válidos
  ↓
Buscar Mentorado (busca por telefone) ← JÁ EXISTE
  ↓
Roteador (decide fluxo)
  ↓
Switch
```

### ✅ O Que Já Funciona:
- Nó "Buscar Mentorado" já busca pelo telefone
- Configuração Supabase correta
- Filtro por telefone normalizado

### ⚠️ O Que Precisa Melhorar:

1. **Roteador não usa dados do mentorado corretamente**
   - Precisa extrair nome do mentorado
   - Precisa detectar se é Queila ou mentorado

2. **Tratamento quando não encontra mentorado**
   - Se não encontrar, precisa decidir o que fazer
   - Grupo de não-mentorado deve ser ignorado

3. **Extração do nome para consultas**
   - Quando Queila pergunta "Como está o Pablo?"
   - Precisa ter o nome disponível

---

## 🛠️ Melhorias Propostas

### 1. Melhorar Nó "Roteador"

**ANTES** (código atual):
```javascript
const msg = $('Filtrar Válidos').first().json;
const mentorado = $('Buscar Mentorado').first()?.json;
const QUEILA_PHONE = '5511964682447';

if (!mentorado && msg.is_group) {
  return [{json: {route: 'ignore', reason: 'Grupo de não-mentorado'}}];
}

if (!msg.is_group && msg.sender_phone === QUEILA_PHONE) {
  return [{json: {route: 'consulta', query: msg.content, sender: {nome: 'Queila', telefone: QUEILA_PHONE}}}];
}

if (msg.is_group && mentorado) {
  return [{json: {route: 'processar_grupo', mentorado: mentorado, message: msg}}];
}

if (!msg.is_group && mentorado) {
  return [{json: {route: 'processar_privado', mentorado: mentorado, message: msg}}];
}

return [{json: {route: 'ignore', reason: 'Não identificado'}}];
```

**DEPOIS** (código melhorado):
```javascript
const msg = $('Filtrar Válidos').first().json;
const busca = $('Buscar Mentorado').all();
const QUEILA_PHONE = '5511964682447';

// ========================================
// EXTRAIR MENTORADO (se encontrado)
// ========================================

let mentorado = null;

if (busca.length > 0 && busca[0].json) {
  // Supabase retorna array vazio se não encontrar
  // Ou array com 1 objeto se encontrar
  mentorado = busca[0].json;
}

// ========================================
// LOGS PARA DEBUG
// ========================================

console.log('[ROTEADOR] Telefone:', msg.sender_phone);
console.log('[ROTEADOR] Mentorado encontrado:', mentorado ? mentorado.nome : 'Nenhum');
console.log('[ROTEADOR] É grupo:', msg.is_group);

// ========================================
// DECISÃO DE ROTEAMENTO
// ========================================

// 1. MENSAGEM DA QUEILA (consulta)
if (msg.sender_phone === QUEILA_PHONE) {
  return [{
    json: {
      route: 'consulta',
      query: msg.content,
      sender: {
        nome: 'Queila',
        telefone: QUEILA_PHONE
      },
      message: msg
    }
  }];
}

// 2. GRUPO DE MENTORADO
if (msg.is_group && mentorado) {
  return [{
    json: {
      route: 'processar_grupo',
      mentorado: mentorado,
      mentorado_nome: mentorado.nome,
      mentorado_id: mentorado.id,
      message: msg
    }
  }];
}

// 3. PRIVADO DE MENTORADO
if (!msg.is_group && mentorado) {
  return [{
    json: {
      route: 'processar_privado',
      mentorado: mentorado,
      mentorado_nome: mentorado.nome,
      mentorado_id: mentorado.id,
      message: msg
    }
  }];
}

// 4. GRUPO DE NÃO-MENTORADO (ignorar)
if (msg.is_group && !mentorado) {
  return [{
    json: {
      route: 'ignore',
      reason: 'Grupo de não-mentorado',
      sender_phone: msg.sender_phone
    }
  }];
}

// 5. PRIVADO DE NÃO-MENTORADO (ignorar ou alertar)
if (!msg.is_group && !mentorado) {
  return [{
    json: {
      route: 'ignore',
      reason: 'Telefone não cadastrado',
      sender_phone: msg.sender_phone,
      sender_name: msg.sender_name
    }
  }];
}

// 6. FALLBACK
return [{
  json: {
    route: 'ignore',
    reason: 'Caso não previsto',
    debug: {
      is_group: msg.is_group,
      has_mentorado: !!mentorado,
      sender_phone: msg.sender_phone
    }
  }
}];
```

---

### 2. Adicionar Nó "Log Mentorado Encontrado" (Opcional)

Para facilitar debug, adicionar um nó Code após "Buscar Mentorado":

```javascript
const busca = $('Buscar Mentorado').all();
const msg = $('Filtrar Válidos').first().json;

let mentorado = null;
let status = 'nao_encontrado';

if (busca.length > 0 && busca[0].json && busca[0].json.id) {
  mentorado = busca[0].json;
  status = 'encontrado';
}

console.log('='.repeat(80));
console.log('[BUSCA MENTORADO] Status:', status);
console.log('[BUSCA MENTORADO] Telefone buscado:', msg.sender_phone);
if (mentorado) {
  console.log('[BUSCA MENTORADO] Encontrado:', mentorado.nome, '(ID:', mentorado.id, ')');
} else {
  console.log('[BUSCA MENTORADO] Nenhum mentorado com este telefone');
}
console.log('='.repeat(80));

// Passar dados adiante
return [{
  json: {
    ...msg,
    mentorado_encontrado: status === 'encontrado',
    mentorado: mentorado
  }
}];
```

---

### 3. Melhorar Nó "Normalizar Webhook"

Adicionar validação extra do telefone:

```javascript
// ... (código existente)

// ========================================
// NORMALIZAR TELEFONE
// ========================================

function normalizarTelefone(tel) {
  let clean = tel.replace(/\D/g, '');

  // Se não começa com 55, adiciona
  if (!clean.startsWith('55')) {
    clean = '55' + clean;
  }

  // Correção do dígito 9 (SP)
  if (clean.length === 12 && clean.startsWith('5511') && clean.charAt(4) !== '9') {
    clean = clean.substring(0, 4) + '9' + clean.substring(4);
  }

  // ========================================
  // VALIDAÇÃO ADICIONAL
  // ========================================

  // Telefone brasileiro deve ter 13 dígitos (55 + DDD + número)
  if (clean.length < 12 || clean.length > 13) {
    console.warn('[NORMALIZAR] Telefone com tamanho inválido:', clean);
  }

  console.log('[NORMALIZAR] Telefone normalizado:', clean);

  return clean;
}

senderPhone = normalizarTelefone(senderPhone);

// ... (restante do código)
```

---

## 📊 Fluxo Melhorado

```
Webhook Evolution API
  ↓
Responder Webhook
  ↓
Normalizar Webhook
  ├─ Extrai: sender_phone normalizado
  ├─ Extrai: sender_name
  └─ Log: telefone normalizado
  ↓
Filtrar Válidos
  ↓
Buscar Mentorado (Supabase)
  ├─ Busca: WHERE telefone = sender_phone
  ├─ Retorna: {id, nome, telefone, nicho, estagio} ou null
  └─ Log: mentorado encontrado ou não
  ↓
[OPCIONAL] Log Mentorado Encontrado
  └─ Debug: status da busca
  ↓
Roteador (MELHORADO)
  ├─ Extrai mentorado dos dados
  ├─ Detecta: Queila, Mentorado, Não-cadastrado
  ├─ Log: decisão de roteamento
  └─ Retorna: route + dados completos
  ↓
Switch
  ├─ CONSULTA → Preparar para Agente
  ├─ PROCESSAR_GRUPO → Switch Tipo Mídia
  ├─ PROCESSAR_PRIVADO → Switch Tipo Mídia
  └─ IGNORE → (fim)
```

---

## 🧪 Casos de Teste

### Teste 1: Mentorado Conhecido (Grupo)
```
Input:
  sender_phone: "5511999887766" (Pablo Santos)
  is_group: true
  content: "Fiz a página de captura"

Esperado:
  route: "processar_grupo"
  mentorado_nome: "Pablo Santos"
  mentorado_id: 1
```

### Teste 2: Queila (Consulta)
```
Input:
  sender_phone: "5511964682447" (Queila)
  is_group: false
  content: "Como está o Pablo?"

Esperado:
  route: "consulta"
  query: "Como está o Pablo?"
  sender.nome: "Queila"
```

### Teste 3: Não-Mentorado (Grupo)
```
Input:
  sender_phone: "5511000000000" (desconhecido)
  is_group: true
  content: "Oi pessoal"

Esperado:
  route: "ignore"
  reason: "Grupo de não-mentorado"
```

### Teste 4: Não-Mentorado (Privado)
```
Input:
  sender_phone: "5511000000000" (desconhecido)
  is_group: false
  content: "Oi"

Esperado:
  route: "ignore"
  reason: "Telefone não cadastrado"
```

---

## 🔧 Implementação no n8n

### Passo 1: Atualizar Nó "Roteador"

1. Abra o nó "Roteador" no n8n
2. Substitua o código JavaScript pelo código melhorado acima
3. Salve

### Passo 2: (Opcional) Adicionar Nó de Log

1. Adicione nó "Code" entre "Buscar Mentorado" e "Roteador"
2. Renomeie para "Log Mentorado Encontrado"
3. Cole o código de log
4. Conecte: Buscar Mentorado → Log Mentorado → Roteador

### Passo 3: Atualizar Nó "Normalizar Webhook"

1. Abra o nó "Normalizar Webhook"
2. Adicione a validação extra do telefone
3. Salve

### Passo 4: Testar

Execute o workflow com diferentes cenários de teste listados acima.

---

## 📋 Checklist

- [ ] Código do Roteador atualizado
- [ ] Logs adicionados para debug
- [ ] Normalização de telefone validada
- [ ] Teste com mentorado conhecido (grupo)
- [ ] Teste com mentorado conhecido (privado)
- [ ] Teste com Queila (consulta)
- [ ] Teste com não-mentorado (grupo)
- [ ] Teste com não-mentorado (privado)
- [ ] Logs do n8n verificados
- [ ] Workflow salvo e ativado

---

## 🐛 Troubleshooting

### Problema: "Mentorado não encontrado mesmo estando cadastrado"

**Diagnóstico:**
```sql
-- Verificar telefone no banco
SELECT id, nome, telefone FROM mentorados
WHERE telefone = '5511999887766';

-- Verificar formato
SELECT telefone, LENGTH(telefone) FROM mentorados;
```

**Soluções:**
1. Verificar se telefone está normalizado (com 55)
2. Verificar se tem espaços ou caracteres especiais
3. Atualizar telefones no banco se necessário

### Problema: "Roteador sempre retorna 'ignore'"

**Diagnóstico:**
- Ver logs do console.log no n8n
- Verificar output do "Buscar Mentorado"
- Verificar se `busca[0].json` está correto

**Solução:**
Adicionar nó de log para ver estrutura exata dos dados.

---

## 📝 Exemplo de Log Esperado

```
================================================================================
[NORMALIZAR] Telefone normalizado: 5511999887766
================================================================================
[BUSCA MENTORADO] Status: encontrado
[BUSCA MENTORADO] Telefone buscado: 5511999887766
[BUSCA MENTORADO] Encontrado: Pablo Santos (ID: 1)
================================================================================
[ROTEADOR] Telefone: 5511999887766
[ROTEADOR] Mentorado encontrado: Pablo Santos
[ROTEADOR] É grupo: true
[ROTEADOR] Decisão: processar_grupo
================================================================================
```

---

**Próximo passo:** Implementar mudanças no n8n e testar
