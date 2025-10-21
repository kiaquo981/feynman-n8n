#!/usr/bin/env python3
"""
Script para modificar o workflow n8n e integrar o webhook no fluxo principal
"""

import json
import sys

# Ler o workflow original (você deve colar o JSON no arquivo workflow-original.json)
with open('workflow-original.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# ============================================
# NOVOS NÓS
# ============================================

# 1. Preparar para Agente (adapta dados do Roteador para o Agente)
preparar_agente = {
    "parameters": {
        "jsCode": """const roteador = $('Roteador').first().json;

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
}];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [-480, 944],
    "id": "preparar-agente-001",
    "name": "Preparar para Agente"
}

# 2. Enviar Resposta WhatsApp (envia resposta do agente para WhatsApp)
enviar_whatsapp = {
    "parameters": {
        "method": "POST",
        "url": "https://evolution.manager01.feynmanproject.com/message/sendText/produ02",
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                {
                    "name": "apikey",
                    "value": "BAD515E8A35F-438C-AF16-77FCDC7D2DAC"
                }
            ]
        },
        "sendBody": True,
        "bodyParameters": {
            "parameters": [
                {
                    "name": "number",
                    "value": "={{ $('Preparar para Agente').first().json.sender_phone }}"
                },
                {
                    "name": "text",
                    "value": "={{ $json.output }}"
                }
            ]
        },
        "options": {}
    },
    "id": "enviar-whatsapp-001",
    "name": "Enviar Resposta WhatsApp",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [4256, 1920]
}

# Adicionar os novos nós ao workflow
workflow['nodes'].append(preparar_agente)
workflow['nodes'].append(enviar_whatsapp)

# ============================================
# MODIFICAR CONEXÕES
# ============================================

# Adicionar conexão: Switch (saída CONSULTA) → Preparar para Agente
if 'Switch' not in workflow['connections']:
    workflow['connections']['Switch'] = {}

if 'main' not in workflow['connections']['Switch']:
    workflow['connections']['Switch']['main'] = [[], [], []]

# A saída CONSULTA é a terceira (índice 2)
workflow['connections']['Switch']['main'][2] = [
    {
        "node": "Preparar para Agente",
        "type": "main",
        "index": 0
    }
]

# Adicionar conexão: Preparar para Agente → Agente Consulta
workflow['connections']['Preparar para Agente'] = {
    "main": [
        [
            {
                "node": "Agente Consulta",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Modificar conexão: Agente Consulta → Enviar Resposta WhatsApp
workflow['connections']['Agente Consulta'] = {
    "main": [
        [
            {
                "node": "Enviar Resposta WhatsApp",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# ============================================
# DESABILITAR FLUXO ANTIGO (opcional)
# ============================================

# Marcar nós do fluxo antigo como disabled
nos_antigos = [
    'Preparar Consulta',
    'Analisar Consulta (GPT-4)',
    'Parse Intent',
    'Switch1',
    'Buscar Mentorado por Nome',
    'Validar Mentorado',
    'Query Inteligente',
    'Code in JavaScript1',
    'Code in JavaScript2',
    'Code in JavaScript3',
    'Code in JavaScript4',
    'Code in JavaScript5',
    'Code in JavaScript6',
    'Buscar Calls Dinâmico',
    'Buscar Interações',
    'Buscar Direcionamentos',
    'Buscar Diagnóstico',
    'Buscar Compromissos',
    'Buscar Métricas',
    'Construir Contexto Inteligente',
    'Prompt Conversacional Focado',
    'Construir Contexto Denso',
    'Gerar Resposta',
    'Enviar Resposta',
    'Análise Global',
    'Buscar Todos Mentorados',
    'Buscar Todas Interações',
    'Webhook Entrada',
    'Normalizar Entrada',
    'Responder'
]

for node in workflow['nodes']:
    if node['name'] in nos_antigos:
        node['disabled'] = True
        print(f"✓ Desabilitado: {node['name']}")

# ============================================
# SALVAR WORKFLOW MODIFICADO
# ============================================

with open('workflow-modificado.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print("\n✅ Workflow modificado salvo em 'workflow-modificado.json'")
print("\n📋 Mudanças aplicadas:")
print("  1. Adicionado nó 'Preparar para Agente'")
print("  2. Adicionado nó 'Enviar Resposta WhatsApp'")
print("  3. Conectado Switch (CONSULTA) → Preparar para Agente → Agente Consulta → Enviar Resposta WhatsApp")
print("  4. Desabilitados nós do fluxo antigo de consulta")
print("\n🚀 Próximos passos:")
print("  1. Importe o arquivo 'workflow-modificado.json' no n8n")
print("  2. Verifique as posições dos nós no canvas")
print("  3. Teste enviando uma consulta para o WhatsApp")
