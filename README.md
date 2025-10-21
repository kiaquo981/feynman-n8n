# 🔌 Integração Webhook → Workflow n8n

Documentação completa para integrar o webhook de consulta no workflow principal do n8n.

## 📚 Arquivos Disponíveis

### 🎯 [RESUMO-VISUAL.md](RESUMO-VISUAL.md) ← **COMECE AQUI**
Visão geral rápida das mudanças (5 min de leitura)
- O que muda
- Antes vs Depois
- Comparação visual

### 📖 [GUIA-INTEGRACAO.md](GUIA-INTEGRACAO.md)
Guia completo passo a passo (20 min de leitura)
- Opção A: Modificação manual no n8n
- Opção B: Script Python automático
- Testes e troubleshooting
- Diagrama do fluxo final

### 📄 [workflow-integrado.md](workflow-integrado.md)
Documentação técnica das mudanças
- Código dos nós
- Configuração detalhada
- Estrutura JSON

### 🐍 [modificar-workflow.py](modificar-workflow.py)
Script Python para automação
- Lê workflow original
- Aplica mudanças automaticamente
- Gera workflow modificado

---

## 🚀 Início Rápido

### Opção 1: Manual (Recomendado para primeira vez)

1. Leia [RESUMO-VISUAL.md](RESUMO-VISUAL.md)
2. Siga [GUIA-INTEGRACAO.md](GUIA-INTEGRACAO.md) → Opção A
3. Teste!

### Opção 2: Automático (Para quem já conhece o fluxo)

```bash
# 1. Exporte o workflow atual do n8n
# 2. Salve como workflow-original.json nesta pasta
# 3. Execute:
python3 modificar-workflow.py
# 4. Importe workflow-modificado.json no n8n
```

---

## 📊 Resumo das Mudanças

### Antes: 2 Fluxos Separados
- Webhook Principal (processar mensagens)
- Webhook Separado (consultas) ← isolado

### Depois: 1 Fluxo Unificado
- Webhook Principal (processar mensagens + consultas) ← tudo integrado

### Redução de Complexidade
- **30+ nós** → **3 nós** para consulta
- **2 webhooks** → **1 webhook**
- **Manutenção difícil** → **Manutenção fácil**

---

## 🎯 O Que Você Vai Adicionar

### 2 Nós Novos:

1. **Preparar para Agente** (Code)
   - Adapta dados do Roteador para o Agente
   - 10 linhas de código JavaScript

2. **Enviar Resposta WhatsApp** (HTTP Request)
   - Envia resposta do agente para WhatsApp
   - Configuração simples de API

### 3 Conexões Novas:

```
Switch (CONSULTA) → Preparar para Agente → Agente Consulta → Enviar Resposta WhatsApp
```

---

## 🧪 Como Testar

Após implementar, envie via WhatsApp:

```
Como está o Pablo?
```

**Deve acontecer:**
1. ✅ Webhook recebe mensagem
2. ✅ Roteador detecta consulta
3. ✅ Agente busca dados
4. ✅ Resposta enviada no WhatsApp

---

## 📁 Estrutura de Arquivos

```
feynman-n8n/
├── README.md                      ← Você está aqui
├── RESUMO-VISUAL.md              ← Visão geral rápida
├── GUIA-INTEGRACAO.md            ← Guia passo a passo completo
├── workflow-integrado.md         ← Documentação técnica
├── modificar-workflow.py         ← Script de automação
├── workflow-original.json        ← (você cria) Workflow exportado
└── workflow-modificado.json      ← (script gera) Workflow modificado
```

---

## ⚠️ Importante

### Antes de Começar:
- ✅ Faça backup do workflow atual
- ✅ Teste em ambiente de desenvolvimento primeiro
- ✅ Leia pelo menos o RESUMO-VISUAL.md

### Durante:
- ✅ Siga os passos na ordem
- ✅ Verifique cada conexão
- ✅ Não delete nós antes de testar

### Depois:
- ✅ Teste com consultas reais
- ✅ Monitore logs de execução
- ✅ Verifique consumo de tokens GPT-4

---

## 🐛 Problemas Comuns

### "Agente não responde"
→ Verificar se conexões estão corretas
→ Ver logs de execução no n8n

### "Mensagem não chega no WhatsApp"
→ Verificar API key
→ Testar Evolution API manualmente

### "Mentorado não encontrado"
→ Verificar se nome está no banco
→ Testar query SQL diretamente

**Mais detalhes:** [GUIA-INTEGRACAO.md → Troubleshooting](GUIA-INTEGRACAO.md#-troubleshooting)

---

## 📞 Suporte

1. Leia os arquivos de documentação
2. Verifique logs do n8n
3. Teste nós individualmente
4. Compare com diagramas visuais

---

## ✅ Checklist de Implementação

- [ ] Li o RESUMO-VISUAL.md
- [ ] Fiz backup do workflow atual
- [ ] Escolhi método (Manual ou Automático)
- [ ] Adicionei nó "Preparar para Agente"
- [ ] Adicionei nó "Enviar Resposta WhatsApp"
- [ ] Conectei os 3 nós corretamente
- [ ] Desabilitei/deletei fluxo antigo
- [ ] Salvei e ativei workflow
- [ ] Testei com "Como está o Pablo?"
- [ ] Testei com "Quando foi última call?"
- [ ] Testei com "Quem precisa atenção?"

---

## 📈 Próximos Passos (Após Integração)

1. **Monitorar** - Acompanhar execuções por 1 semana
2. **Otimizar** - Ajustar prompts conforme feedback
3. **Expandir** - Adicionar novas tools se necessário
4. **Documentar** - Registrar padrões de uso

---

## 🎉 Resultado Final

Você terá:
- ✅ 1 workflow unificado e simples
- ✅ Consultas integradas no fluxo principal
- ✅ Agente reutilizado com todas as tools
- ✅ Menos nós, mais fácil de manter
- ✅ Melhor performance

---

**Boa implementação! 🚀**

Se tiver dúvidas, comece pelo [RESUMO-VISUAL.md](RESUMO-VISUAL.md) e depois vá para o [GUIA-INTEGRACAO.md](GUIA-INTEGRACAO.md).