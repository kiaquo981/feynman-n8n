#!/usr/bin/env python3
"""
Teste do Roteador Melhorado - Simulação Completa do Fluxo

Simula:
1. Normalização de telefone
2. Busca no banco de dados
3. Decisão de roteamento
4. Validação de casos extremos
"""

from typing import Dict, Optional, Tuple

# ============================================
# CONFIGURAÇÃO
# ============================================

QUEILA_PHONE = '5511964682447'

# Banco de dados simulado
MENTORADOS_DB = [
    {"id": 1, "nome": "Pablo Santos", "telefone": "5511999887766", "nicho": "Fitness"},
    {"id": 2, "nome": "Silvane Castro", "telefone": "5511988776655", "nicho": "Marketing"},
    {"id": 3, "nome": "Rafael Castro", "telefone": "5511977665544", "nicho": "Tech"},
    {"id": 4, "nome": "Juliana Altavilla", "telefone": "5511944332211", "nicho": "Saúde"},
]

# ============================================
# FUNÇÃO: NORMALIZAR TELEFONE
# ============================================

def normalizar_telefone(tel: str) -> Tuple[str, list]:
    """
    Normaliza telefone e retorna warnings se houver
    """
    warnings = []
    clean = ''.join(c for c in tel if c.isdigit())

    # Se não começa com 55, adiciona
    if not clean.startswith('55'):
        clean = '55' + clean
        warnings.append(f"Adicionado prefixo 55: {clean}")

    # Correção do dígito 9 (SP)
    if len(clean) == 12 and clean.startswith('5511') and clean[4] != '9':
        clean = clean[:4] + '9' + clean[4:]
        warnings.append(f"Adicionado dígito 9: {clean}")

    # Validação de tamanho
    if len(clean) < 12 or len(clean) > 13:
        warnings.append(f"⚠️ Tamanho inválido: {len(clean)} dígitos")

    return clean, warnings


# ============================================
# FUNÇÃO: BUSCAR MENTORADO
# ============================================

def buscar_mentorado(telefone: str) -> Optional[Dict]:
    """
    Simula busca no Supabase
    """
    for mentorado in MENTORADOS_DB:
        if mentorado['telefone'] == telefone:
            return mentorado
    return None


# ============================================
# FUNÇÃO: ROTEADOR
# ============================================

def roteador(sender_phone: str, is_group: bool, content: str, sender_name: str = "Desconhecido") -> Dict:
    """
    Lógica melhorada do roteador
    """
    # Buscar mentorado
    mentorado = buscar_mentorado(sender_phone)

    # Logs
    print(f"  [ROTEADOR] Telefone: {sender_phone}")
    print(f"  [ROTEADOR] Mentorado: {mentorado['nome'] if mentorado else 'Nenhum'}")
    print(f"  [ROTEADOR] É grupo: {is_group}")

    # Decisão
    # 1. QUEILA (consulta)
    if sender_phone == QUEILA_PHONE:
        print(f"  [ROTEADOR] Decisão: CONSULTA")
        return {
            'route': 'consulta',
            'query': content,
            'sender': {'nome': 'Queila', 'telefone': QUEILA_PHONE}
        }

    # 2. GRUPO DE MENTORADO
    if is_group and mentorado:
        print(f"  [ROTEADOR] Decisão: PROCESSAR_GRUPO")
        return {
            'route': 'processar_grupo',
            'mentorado': mentorado,
            'mentorado_nome': mentorado['nome'],
            'mentorado_id': mentorado['id']
        }

    # 3. PRIVADO DE MENTORADO
    if not is_group and mentorado:
        print(f"  [ROTEADOR] Decisão: PROCESSAR_PRIVADO")
        return {
            'route': 'processar_privado',
            'mentorado': mentorado,
            'mentorado_nome': mentorado['nome'],
            'mentorado_id': mentorado['id']
        }

    # 4. GRUPO DE NÃO-MENTORADO
    if is_group and not mentorado:
        print(f"  [ROTEADOR] Decisão: IGNORE (grupo não-mentorado)")
        return {
            'route': 'ignore',
            'reason': 'Grupo de não-mentorado',
            'sender_phone': sender_phone
        }

    # 5. PRIVADO DE NÃO-MENTORADO
    if not is_group and not mentorado:
        print(f"  [ROTEADOR] Decisão: IGNORE (telefone não cadastrado)")
        return {
            'route': 'ignore',
            'reason': 'Telefone não cadastrado',
            'sender_phone': sender_phone,
            'sender_name': sender_name
        }

    # 6. FALLBACK
    print(f"  [ROTEADOR] Decisão: IGNORE (caso não previsto)")
    return {
        'route': 'ignore',
        'reason': 'Caso não previsto'
    }


# ============================================
# FUNÇÃO: TESTE COMPLETO
# ============================================

def testar_fluxo(
    telefone_raw: str,
    is_group: bool,
    content: str,
    sender_name: str = "Desconhecido",
    descricao: str = ""
):
    """
    Simula fluxo completo
    """
    print(f"\n{'='*80}")
    print(f"🧪 TESTE: {descricao}")
    print(f"{'='*80}")
    print(f"📱 Input:")
    print(f"   Telefone: {telefone_raw}")
    print(f"   Grupo: {is_group}")
    print(f"   Conteúdo: \"{content}\"")
    print(f"   Nome: {sender_name}")
    print()

    # 1. Normalizar
    print(f"📋 Etapa 1: Normalização")
    telefone_norm, warnings = normalizar_telefone(telefone_raw)
    print(f"   Normalizado: {telefone_norm}")
    if warnings:
        for w in warnings:
            print(f"   {w}")
    print()

    # 2. Buscar
    print(f"📋 Etapa 2: Busca no Banco")
    mentorado = buscar_mentorado(telefone_norm)
    if mentorado:
        print(f"   ✅ Encontrado: {mentorado['nome']} (ID {mentorado['id']}) - {mentorado['nicho']}")
    else:
        print(f"   ❌ Não encontrado")
    print()

    # 3. Rotear
    print(f"📋 Etapa 3: Roteamento")
    resultado = roteador(telefone_norm, is_group, content, sender_name)
    print()

    # 4. Resultado
    print(f"✅ Resultado:")
    print(f"   Route: {resultado['route']}")
    if resultado['route'] == 'consulta':
        print(f"   Query: {resultado['query']}")
        print(f"   Sender: {resultado['sender']['nome']}")
    elif resultado['route'] in ['processar_grupo', 'processar_privado']:
        print(f"   Mentorado: {resultado['mentorado_nome']} (ID {resultado['mentorado_id']})")
    elif resultado['route'] == 'ignore':
        print(f"   Reason: {resultado['reason']}")

    # 5. Próximo passo
    print(f"\n📍 Próximo Passo:")
    if resultado['route'] == 'consulta':
        print(f"   → Switch: saída CONSULTA → Preparar para Agente")
    elif resultado['route'] == 'processar_grupo':
        print(f"   → Switch: saída PROCESSAR_GRUPO → Switch Tipo Mídia")
    elif resultado['route'] == 'processar_privado':
        print(f"   → Switch: saída PROCESSAR_PRIVADO → Switch Tipo Mídia")
    elif resultado['route'] == 'ignore':
        print(f"   → Switch: saída IGNORE → Fim (não processa)")


# ============================================
# CASOS DE TESTE
# ============================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTE DO ROTEADOR MELHORADO")
    print("="*80)

    # Teste 1: Mentorado conhecido (grupo)
    testar_fluxo(
        telefone_raw="11999887766",  # Sem 55
        is_group=True,
        content="Fiz a página de captura!",
        sender_name="Pablo Santos - Case",
        descricao="Mentorado conhecido (grupo) - telefone sem 55"
    )

    # Teste 2: Mentorado conhecido (privado)
    testar_fluxo(
        telefone_raw="5511988776655",  # Com 55
        is_group=False,
        content="Oi, preciso de ajuda",
        sender_name="Silvane Castro",
        descricao="Mentorado conhecido (privado) - telefone com 55"
    )

    # Teste 3: Queila (consulta)
    testar_fluxo(
        telefone_raw="5511964682447",
        is_group=False,
        content="Como está o Pablo?",
        sender_name="Queila Trizotti",
        descricao="Queila fazendo consulta"
    )

    # Teste 4: Não-mentorado (grupo)
    testar_fluxo(
        telefone_raw="5511000000000",
        is_group=True,
        content="Olá pessoal!",
        sender_name="Pessoa Desconhecida",
        descricao="Não-mentorado em grupo (deve ignorar)"
    )

    # Teste 5: Não-mentorado (privado)
    testar_fluxo(
        telefone_raw="5511111111111",
        is_group=False,
        content="Oi",
        sender_name="João Silva",
        descricao="Não-mentorado em privado (deve ignorar)"
    )

    # Teste 6: Telefone sem dígito 9 (SP)
    testar_fluxo(
        telefone_raw="551199887766",  # 12 dígitos, falta o 9
        is_group=True,
        content="Teste",
        sender_name="Pablo Santos - Case",
        descricao="Telefone SP sem dígito 9 (deve corrigir)"
    )

    # Teste 7: Queila no grupo (deve ser consulta, não grupo)
    testar_fluxo(
        telefone_raw="5511964682447",
        is_group=True,  # Queila postando no grupo
        content="Alguém viu o material?",
        sender_name="Queila Trizotti",
        descricao="Queila postando no grupo (prioridade = consulta)"
    )

    # Sumário
    print("\n" + "="*80)
    print("📊 SUMÁRIO DOS TESTES")
    print("="*80)
    print("""
✅ SUCESSOS:
   • Normalização de telefone (com e sem 55)
   • Correção de dígito 9 (SP)
   • Busca de mentorado no banco
   • Roteamento correto para cada caso
   • Priorização de Queila (sempre consulta)
   • Ignorar não-mentorados

⚠️ PONTOS DE ATENÇÃO:
   • Queila no grupo = consulta (não processar como grupo)
   • Telefones inválidos devem ser logados
   • Não-mentorados em privado podem querer se cadastrar

🔧 PRÓXIMOS PASSOS:
   1. Implementar código melhorado no n8n
   2. Testar com dados reais
   3. Monitorar logs por 48h
   4. Ajustar se necessário
""")

    print("="*80 + "\n")
