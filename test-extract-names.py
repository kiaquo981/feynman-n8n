#!/usr/bin/env python3
"""
Script de teste para extração de nomes de mentorados em mensagens

Simula o processo de:
1. Receber mensagem do WhatsApp
2. Extrair nomes mencionados
3. Buscar no banco de dados
4. Validar resultados
"""

import re
from typing import List, Dict, Tuple

# ============================================
# NOMES DE EXEMPLO (base de dados simulada)
# ============================================

MENTORADOS_DB = [
    {"id": 1, "nome": "Pablo Santos", "telefone": "5511999887766", "nicho": "Fitness", "estagio": "intermediario"},
    {"id": 2, "nome": "Silvane Castro", "telefone": "5511988776655", "nicho": "Marketing", "estagio": "avancado"},
    {"id": 3, "nome": "Rafael Castro", "telefone": "5511977665544", "nicho": "Tech", "estagio": "iniciante"},
    {"id": 8, "nome": "Rafael Castro", "telefone": "5511966554433", "nicho": "Design", "estagio": "intermediario"},
    {"id": 15, "nome": "Rafael Castro", "telefone": "5511955443322", "nicho": "Vendas", "estagio": "iniciante"},
    {"id": 4, "nome": "Juliana Altavilla", "telefone": "5511944332211", "nicho": "Saúde", "estagio": "avancado"},
    {"id": 5, "nome": "Dani Silva", "telefone": "5511933221100", "nicho": "Educação", "estagio": "intermediario"},
    {"id": 6, "nome": "Flávia Costa", "telefone": "5511922110099", "nicho": "Beleza", "estagio": "iniciante"},
    {"id": 7, "nome": "Érica Almeida", "telefone": "5511911009988", "nicho": "Nutrição", "estagio": "avancado"},
]

# ============================================
# PADRÕES DE NOMES COMUNS
# ============================================

NOMES_CONHECIDOS = [
    "pablo", "silvane", "rafael", "juliana", "dani",
    "flávia", "flavia", "érica", "erica", "castro"
]

# ============================================
# FUNÇÃO: EXTRAIR NOMES DE MENSAGEM
# ============================================

def extrair_nomes(mensagem: str) -> List[str]:
    """
    Extrai possíveis nomes de mentorados da mensagem

    Padrões detectados:
    - "Como está o/a [Nome]?"
    - "Status do/da [Nome]"
    - "[Nome] está ok?"
    - "Última call do/da [Nome]"
    - "O que fazer com o/a [Nome]"
    """
    mensagem_lower = mensagem.lower()
    nomes_encontrados = []

    # Padrão 1: "Como está o/a X?"
    match = re.search(r'como\s+está\s+(?:o|a)\s+([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)', mensagem_lower)
    if match:
        nomes_encontrados.append(match.group(1))

    # Padrão 2: "Status do/da X"
    match = re.search(r'status\s+d[oa]\s+([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)', mensagem_lower)
    if match:
        nomes_encontrados.append(match.group(1))

    # Padrão 3: "X está ok?"
    match = re.search(r'^([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)\s+(?:está|tá)', mensagem_lower)
    if match:
        nomes_encontrados.append(match.group(1))

    # Padrão 4: "Última call do/da X"
    match = re.search(r'(?:última|ultima)\s+call\s+d[oa]\s+([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)', mensagem_lower)
    if match:
        nomes_encontrados.append(match.group(1))

    # Padrão 5: Procurar nomes conhecidos
    for nome in NOMES_CONHECIDOS:
        if nome in mensagem_lower and nome not in [n.lower() for n in nomes_encontrados]:
            nomes_encontrados.append(nome)

    return list(set(nomes_encontrados))  # Remover duplicatas


# ============================================
# FUNÇÃO: BUSCAR NO BANCO
# ============================================

def buscar_mentorado(nome: str) -> List[Dict]:
    """
    Simula busca no banco de dados (como o nó buscarMentorado)

    SQL equivalente:
    SELECT * FROM mentorados WHERE nome LIKE '%{nome}%'
    """
    resultados = []

    for mentorado in MENTORADOS_DB:
        if nome.lower() in mentorado['nome'].lower():
            resultados.append(mentorado)

    return resultados


# ============================================
# FUNÇÃO: VALIDAR RESULTADO
# ============================================

def validar_resultado(mensagem: str, resultados: List[Dict]) -> Tuple[str, str]:
    """
    Valida o resultado da busca e retorna status + ação sugerida

    Returns:
        (status, acao)
        status: 'unico', 'multiplos', 'nao_encontrado'
        acao: descrição do que fazer
    """
    if len(resultados) == 0:
        return 'nao_encontrado', f'❌ Nenhum mentorado encontrado. Verificar ortografia ou cadastro.'

    elif len(resultados) == 1:
        return 'unico', f'✅ Encontrado: {resultados[0]["nome"]} (ID {resultados[0]["id"]}) - Pode prosseguir com consulta.'

    else:
        nomes = '\n'.join([f'   {i+1}. {r["nome"]} (ID {r["id"]}) - {r["estagio"]}' for i, r in enumerate(resultados)])
        return 'multiplos', f'⚠️ Múltiplos resultados encontrados:\n{nomes}\n   → Pedir clarificação: "Qual deles você quer?"'


# ============================================
# FUNÇÃO: TESTE COMPLETO
# ============================================

def testar_mensagem(mensagem: str, verbose: bool = True):
    """
    Testa o fluxo completo de extração e busca
    """
    print(f"\n{'='*80}")
    print(f"📱 MENSAGEM: \"{mensagem}\"")
    print(f"{'='*80}\n")

    # 1. Extrair nomes
    nomes = extrair_nomes(mensagem)

    if not nomes:
        print("❌ Nenhum nome identificado na mensagem.")
        print("\n💡 Sugestão: Refinar padrões de regex ou pedir clarificação ao usuário.\n")
        return

    print(f"🔍 Nomes extraídos: {nomes}\n")

    # 2. Buscar cada nome
    for nome in nomes:
        print(f"📊 Buscando '{nome}'...")
        resultados = buscar_mentorado(nome)

        # 3. Validar resultado
        status, acao = validar_resultado(mensagem, resultados)

        print(f"\n{acao}\n")

        if verbose and resultados:
            print(f"📋 Detalhes dos resultados:")
            for r in resultados:
                print(f"   • {r['nome']} - {r['nicho']} ({r['estagio']})")
            print()


# ============================================
# CASOS DE TESTE
# ============================================

CASOS_TESTE = [
    # Casos com 1 resultado
    "Como está o Pablo?",
    "Status da Silvane",
    "Juliana está ok?",
    "Última call da Dani",

    # Casos com múltiplos resultados (nome duplicado)
    "Como está o Rafael?",
    "Status do Castro",

    # Casos sem resultado
    "Como está o João?",
    "Status da Maria",

    # Casos com nome completo
    "Como está a Juliana Altavilla?",

    # Casos com sobrenome
    "Status do Santos",

    # Casos complexos
    "Quem precisa atenção?",  # Não deve extrair nome
    "Como está o Pablo e a Silvane?",  # Múltiplos nomes
]


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTE DE EXTRAÇÃO DE NOMES E BUSCA NO BANCO")
    print("="*80)

    # Executar todos os casos de teste
    for mensagem in CASOS_TESTE:
        testar_mensagem(mensagem, verbose=False)

    print("\n" + "="*80)
    print("📊 RESUMO")
    print("="*80)
    print("\n✅ Funciona bem:")
    print("   • Nomes únicos (Pablo, Silvane, Juliana, Dani)")
    print("   • Padrões comuns de consulta")
    print("\n⚠️ Requer clarificação:")
    print("   • Nomes duplicados (Rafael, Castro)")
    print("   • Sistema deve listar opções e pedir escolha")
    print("\n❌ Não identifica:")
    print("   • Nomes não cadastrados")
    print("   • Consultas sem nome específico (genéricas)")

    print("\n" + "="*80)
    print("💡 RECOMENDAÇÕES")
    print("="*80)
    print("""
1. **Para múltiplos resultados:**
   - Listar TODOS com ID e informação distintiva (estágio/nicho)
   - Pedir usuário escolher: "Qual deles você quer?"
   - NÃO prosseguir até confirmar

2. **Para nomes não encontrados:**
   - Informar "Mentorado não encontrado"
   - Sugerir verificar ortografia
   - Listar nomes similares se houver

3. **Para consultas genéricas:**
   - Identificar padrão (ex: "Quem precisa atenção?")
   - Usar função específica (ex: buscarTodasUrgencias)
   - NÃO tentar extrair nome

4. **Para múltiplos nomes na mesma mensagem:**
   - Exemplo: "Como está o Pablo e a Silvane?"
   - Processar CADA nome separadamente
   - Se houver ambiguidade em algum, parar e listar TODOS os ambíguos
""")

    print("\n" + "="*80)
    print("🔧 INTEGRAÇÃO COM N8N")
    print("="*80)
    print("""
No workflow n8n, o fluxo seria:

1. **Webhook recebe mensagem**
   └─ "Como está o Rafael?"

2. **Roteador detecta consulta**
   └─ route: "consulta", query: "Como está o Rafael?"

3. **Preparar para Agente**
   └─ Formata dados para o Agente

4. **Agente Consulta**
   ├─ Tool: buscarMentorado("Rafael")
   ├─ Retorna: 3 resultados (IDs 3, 8, 15)
   └─ Agente DEVE listar opções e pedir clarificação

5. **Enviar Resposta WhatsApp**
   └─ "Encontrei 3 mentorados com 'Rafael': ..."

**IMPORTANTE:** O agente está configurado para fazer isso automaticamente
através do system prompt. Verifique a seção sobre buscarMentorado.
""")

    print("="*80 + "\n")
