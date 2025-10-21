# 🚀 Guia de Implementação: Roteador Melhorado

## 📋 Resumo

Atualização do nó "Roteador" para:
- ✅ Buscar mentorado ANTES do Switch (já está funcionando)
- ✅ Melhorar lógica de decisão
- ✅ Adicionar logs para debug
- ✅ Tratar todos os casos possíveis

---

## ⚡ Implementação Rápida (5 minutos)

### Passo 1: Abrir n8n

1. Acesse seu n8n
2. Abra o workflow "Fluxo Whatsapp | Mentorados | Case"

### Passo 2: Atualizar Nó "Roteador"

1. Clique no nó **"Roteador"**
2. Substitua TODO o código JavaScript pelo conteúdo do arquivo `codigo-roteador-melhorado.js`
3. Clique em **"Execute Node"** para testar
4. Clique em **"Save"**

### Passo 3: Testar

Execute o workflow e envie uma mensagem de teste pelo WhatsApp.

### Passo 4: Verificar Logs

No n8n, vá em "Executions" e veja os logs do console:

```
================================================================================
[ROTEADOR] Telefone: 5511999887766
[ROTEADOR] Nome sender: Pablo Santos - Case
[ROTEADOR] Mentorado encontrado: Pablo Santos
[ROTEADOR] É grupo: true
[ROTEADOR] Decisão: PROCESSAR_GRUPO
[ROTEADOR] Mentorado: Pablo Santos (ID: 1)
================================================================================
```

---

## 📊 Mudanças Implementadas

### ANTES:
```javascript
const mentorado = $('Buscar Mentorado').first()?.json;

if (!mentorado && msg.is_group) {
  return [{json: {route: 'ignore'}}];
}
```

**Problema:** Não validava se `json` era um objeto válido

### DEPOIS:
```javascript
let mentorado = null;

if (busca.length > 0 && busca[0].json) {
  const resultado = busca[0].json;

  if (resultado && typeof resultado === 'object' && resultado.id) {
    mentorado = resultado;
  }
}
```

**Vantagem:** Validação robusta + logs detalhados

---

## 🧪 Casos de Teste

### Teste 1: Mentorado em Grupo
```
Enviar mensagem no grupo do Pablo Santos
```

**Esperado:**
- Route: `processar_grupo`
- Mentorado: `Pablo Santos (ID 1)`
- Log: `[ROTEADOR] Decisão: PROCESSAR_GRUPO`

### Teste 2: Queila Fazendo Consulta
```
Queila envia: "Como está o Pablo?"
```

**Esperado:**
- Route: `consulta`
- Query: `Como está o Pablo?`
- Log: `[ROTEADOR] Decisão: CONSULTA (Queila)`

### Teste 3: Não-Mentorado
```
Pessoa não cadastrada envia mensagem no grupo
```

**Esperado:**
- Route: `ignore`
- Reason: `Grupo de não-mentorado`
- Log: `[ROTEADOR] Decisão: IGNORE`

---

## 🔍 Como Ver os Logs

### No n8n:

1. Execute o workflow
2. Clique em "Executions" (barra lateral)
3. Clique na execução mais recente
4. Clique no nó "Roteador"
5. Vá em "Code" → "Console"
6. Veja os logs

### Exemplo de Log Bom:
```
================================================================================
[ROTEADOR] Telefone: 5511964682447
[ROTEADOR] Nome sender: Queila Trizotti
[ROTEADOR] Mentorado encontrado: Nenhum
[ROTEADOR] É grupo: false
[ROTEADOR] Decisão: CONSULTA (Queila)
================================================================================
```

### Exemplo de Log com Problema:
```
================================================================================
[ROTEADOR] Telefone: 5511999887766
[ROTEADOR] Nome sender: Pablo Santos - Case
[ROTEADOR] Mentorado encontrado: Nenhum  ← PROBLEMA
[ROTEADOR] É grupo: true
[ROTEADOR] Decisão: IGNORE (grupo de não-mentorado)
================================================================================
```

**Se isso acontecer:** O mentorado deveria ter sido encontrado. Verificar:
1. Telefone está no banco?
2. Formato do telefone está correto?
3. Nó "Buscar Mentorado" está conectado?

---

## 🐛 Troubleshooting

### Problema 1: "Mentorado não encontrado" (mas está no banco)

**Diagnóstico:**
```sql
-- Verificar telefone no banco
SELECT id, nome, telefone
FROM mentorados
WHERE telefone = '5511999887766';
```

**Soluções:**
1. Verificar se telefone no banco está com 55
2. Verificar se não tem espaços ou caracteres especiais
3. Re-salvar o nó "Buscar Mentorado"

### Problema 2: "Logs não aparecem"

**Solução:**
1. Executar workflow em modo "Execute Workflow"
2. Ver execuções passadas em "Executions"
3. Logs ficam em "Code" → "Console" do nó

### Problema 3: "Erro ao executar nó"

**Solução:**
1. Verificar se código JavaScript está correto
2. Verificar se nó "Buscar Mentorado" está antes
3. Verificar se nó "Filtrar Válidos" está antes

---

## ✅ Checklist de Implementação

- [ ] Backup do workflow atual criado
- [ ] Código do Roteador atualizado
- [ ] Workflow salvo
- [ ] Teste 1: Mentorado em grupo (passou)
- [ ] Teste 2: Queila consulta (passou)
- [ ] Teste 3: Não-mentorado (passou)
- [ ] Logs verificados no console
- [ ] Workflow ativado em produção

---

## 📁 Arquivos de Referência

- **MELHORIA-BUSCA-MENTORADO.md** - Documentação completa
- **codigo-roteador-melhorado.js** - Código pronto para copiar
- **test-roteador-melhorado.py** - Script de teste em Python
- **IMPLEMENTAR-ROTEADOR.md** - Este arquivo (guia rápido)

---

## 🎯 Resultado Esperado

### Fluxo Completo Funcionando:

```
WhatsApp: "Fiz a página de captura!"
  ↓
Webhook Evolution API
  ↓
Normalizar Webhook (telefone: 5511999887766)
  ↓
Filtrar Válidos
  ↓
Buscar Mentorado (encontra: Pablo Santos)
  ↓
Roteador (decide: processar_grupo)
  ↓
Switch (saída: PROCESSAR_GRUPO)
  ↓
Switch Tipo Mídia
  ↓
... (processamento de mídia)
  ↓
Salvar Interação
```

---

## 🚀 Após Implementação

### Monitorar por 48h:
- Verificar se todos os mentorados são encontrados
- Verificar se não-mentorados são ignorados
- Verificar se consultas da Queila funcionam

### Métricas de Sucesso:
- Taxa de reconhecimento de mentorados: >95%
- Falsos positivos (não-mentorado como mentorado): 0%
- Consultas da Queila funcionando: 100%

---

**Tempo estimado:** 5 minutos
**Dificuldade:** Baixa
**Impacto:** Alto

Boa implementação! 🎉
