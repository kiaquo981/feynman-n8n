#!/usr/bin/env python3
"""
Script de teste MELHORADO para extração de nomes de mentorados

Melhorias:
- Filtro de stopwords
- Validação de nomes contra lista conhecida
- Melhor detecção de múltiplos nomes
"""

import re
from typing import List, Dict, Tuple

# ============================================
# BASE DE DADOS SIMULADA
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
# STOPWORDS (palavras que NÃO são nomes)
# ============================================

STOPWORDS = {
    # Artigos
    'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
    # Preposições
    'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
    'por', 'para', 'com', 'sem', 'sob', 'sobre', 'e',
    # Verbos comuns
    'está', 'tá', 'estão', 'como', 'que', 'foi', 'tem', 'teve',
    # Interrogativos
    'quando', 'onde', 'quem', 'qual', 'quais',
    # Outros
    'ok', 'está ok', 'precisa', 'atenção'
}

# ============================================
# PRIMEIROS NOMES CONHECIDOS
# ============================================

PRIMEIROS_NOMES = {'pablo', 'silvane', 'rafael', 'juliana', 'dani', 'flávia', 'flavia', 'érica', 'erica'}
SOBRENOMES = {'santos', 'castro', 'altavilla', 'silva', 'costa', 'almeida'}

# ============================================
# FUNÇÃO MELHORADA: EXTRAIR NOMES
# ============================================

def extrair_nomes_v2(mensagem: str) -> List[str]:
    """
    Extração melhorada de nomes com filtros
    """
    mensagem_lower = mensagem.lower()
    nomes_candidatos = []

    # Padrão 1: "Como está o/a NOME [SOBRENOME]?"
    match = re.search(
        r'como\s+(?:está|tá)\s+(?:o|a)\s+([a-záàâãéêíóôõúç]+)(?:\s+([a-záàâãéêíóôõúç]+))?',
        mensagem_lower
    )
    if match:
        nome = match.group(1)
        sobrenome = match.group(2)
        if nome not in STOPWORDS:
            if sobrenome and sobrenome not in STOPWORDS:
                nomes_candidatos.append(f"{nome} {sobrenome}")
            else:
                nomes_candidatos.append(nome)

    # Padrão 2: "Status do/da NOME [SOBRENOME]"
    match = re.search(
        r'status\s+d[oa]\s+([a-záàâãéêíóôõúç]+)(?:\s+([a-záàâãéêíóôõúç]+))?',
        mensagem_lower
    )
    if match:
        nome = match.group(1)
        sobrenome = match.group(2)
        if nome not in STOPWORDS:
            if sobrenome and sobrenome not in STOPWORDS:
                nomes_candidatos.append(f"{nome} {sobrenome}")
            else:
                nomes_candidatos.append(nome)

    # Padrão 3: "NOME [SOBRENOME] está/tá"
    match = re.search(
        r'^([a-záàâãéêíóôõúç]+)(?:\s+([a-záàâãéêíóôõúç]+))?\s+(?:está|tá)',
        mensagem_lower
    )
    if match:
        nome = match.group(1)
        sobrenome = match.group(2)
        if nome not in STOPWORDS:
            if sobrenome and sobrenome not in STOPWORDS:
                nomes_candidatos.append(f"{nome} {sobrenome}")
            else:
                nomes_candidatos.append(nome)

    # Padrão 4: "Última call do/da NOME [SOBRENOME]"
    match = re.search(
        r'(?:última|ultima)\s+call\s+d[oa]\s+([a-záàâãéêíóôõúç]+)(?:\s+([a-záàâãéêíóôõúç]+))?',
        mensagem_lower
    )
    if match:
        nome = match.group(1)
        sobrenome = match.group(2)
        if nome not in STOPWORDS:
            if sobrenome and sobrenome not in STOPWORDS:
                nomes_candidatos.append(f"{nome} {sobrenome}")
            else:
                nomes_candidatos.append(nome)

    # Padrão 5: "NOME e NOME" (múltiplos nomes)
    if ' e ' in mensagem_lower:
        # Detectar padrão: "Pablo e Silvane", "Pablo e a Silvane"
        match = re.search(
            r'(?:o|a)?\s*([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)\s+e\s+(?:o|a)?\s*([a-záàâãéêíóôõúç]+(?:\s+[a-záàâãéêíóôõúç]+)?)',
            mensagem_lower
        )
        if match:
            nome1 = match.group(1).strip()
            nome2 = match.group(2).strip()
            if nome1 not in STOPWORDS:
                nomes_candidatos.append(nome1)
            if nome2 not in STOPWORDS:
                nomes_candidatos.append(nome2)

    # Filtrar apenas nomes conhecidos ou válidos
    nomes_validos = []
    for candidato in nomes_candidatos:
        # Verificar se primeira palavra é nome conhecido
        primeira_palavra = candidato.split()[0]
        if primeira_palavra in PRIMEIROS_NOMES or primeira_palavra in SOBRENOMES:
            nomes_validos.append(candidato)

    return list(set(nomes_validos))  # Remover duplicatas


# ============================================
# FUNÇÃO: BUSCAR NO BANCO
# ============================================

def buscar_mentorado(nome: str) -> List[Dict]:
    """Busca no banco de dados"""
    resultados = []
    for mentorado in MENTORADOS_DB:
        if nome.lower() in mentorado['nome'].lower():
            resultados.append(mentorado)
    return resultados


# ============================================
# FUNÇÃO: VALIDAR RESULTADO
# ============================================

def validar_resultado(mensagem: str, resultados: List[Dict]) -> Tuple[str, str]:
    """Valida e retorna status"""
    if len(resultados) == 0:
        return 'nao_encontrado', f'❌ Mentorado "{mensagem}" não encontrado.'

    elif len(resultados) == 1:
        m = resultados[0]
        return 'unico', f'✅ {m["nome"]} (ID {m["id"]}) - {m["estagio"]}, {m["nicho"]}'

    else:
        nomes = '\n'.join([
            f'   {i+1}. {r["nome"]} (ID {r["id"]}) - {r["nicho"]}, {r["estagio"]}'
            for i, r in enumerate(resultados)
        ])
        return 'multiplos', f'⚠️ Múltiplos resultados:\n{nomes}\n\n   💬 Resposta para WhatsApp:\n   "Encontrei {len(resultados)} mentorados. Qual deles você quer?"'


# ============================================
# FUNÇÃO: TESTE COMPLETO V2
# ============================================

def testar_mensagem_v2(mensagem: str):
    """Teste completo melhorado"""
    print(f"\n{'='*80}")
    print(f"📱 MENSAGEM: \"{mensagem}\"")
    print(f"{'='*80}\n")

    # Extrair nomes
    nomes = extrair_nomes_v2(mensagem)

    if not nomes:
        # Verificar se é consulta genérica
        if any(palavra in mensagem.lower() for palavra in ['quem precisa', 'urgente', 'atenção']):
            print("🔍 Consulta genérica detectada (não é busca por nome)")
            print("→ Usar buscarTodasUrgencias() ou similar\n")
        else:
            print("❌ Nenhum nome identificado.")
            print("💡 Possíveis causas:")
            print("   • Nome não está na lista conhecida")
            print("   • Padrão de mensagem não reconhecido\n")
        return

    print(f"🔍 Nomes extraídos: {nomes}\n")

    # Buscar cada nome
    todos_resultados = {}
    for nome in nomes:
        print(f"📊 Buscando '{nome}'...")
        resultados = buscar_mentorado(nome)
        todos_resultados[nome] = resultados

        status, acao = validar_resultado(nome, resultados)
        print(f"{acao}\n")

    # Análise final para múltiplos nomes
    if len(nomes) > 1:
        print("="*80)
        print("📌 ANÁLISE: Múltiplos nomes detectados")
        print("="*80)

        tem_ambiguidade = any(len(r) > 1 for r in todos_resultados.values())

        if tem_ambiguidade:
            print("\n⚠️ ATENÇÃO: Pelo menos 1 nome tem múltiplos resultados.")
            print("📋 AÇÃO RECOMENDADA:")
            print("   1. Listar TODAS as ambiguidades de uma vez")
            print("   2. Pedir usuário clarificar TODOS os nomes ambíguos")
            print("   3. NÃO processar até confirmar\n")

            # Mostrar exemplo de resposta
            print("💬 Exemplo de resposta para WhatsApp:")
            print("   ─────────────────────────────────────")
            for nome, resultados in todos_resultados.items():
                if len(resultados) > 1:
                    print(f"   Encontrei {len(resultados)} mentorados com '{nome}':")
                    for i, r in enumerate(resultados, 1):
                        print(f"     {i}. {r['nome']} - {r['nicho']}, {r['estagio']}")
            print("   ")
            print("   Qual deles você quer? (responda com o número ou estágio)")
            print("   ─────────────────────────────────────")
        else:
            print("\n✅ Todos os nomes têm resultado único.")
            print("📋 AÇÃO: Processar cada mentorado separadamente")

            # Mostrar exemplo
            print("\n💬 Exemplo de resposta para WhatsApp:")
            print("   ─────────────────────────────────────")
            for nome, resultados in todos_resultados.items():
                if resultados:
                    m = resultados[0]
                    print(f"   📊 {m['nome']}:")
                    print(f"   • Status: [buscar dados...]")
            print("   ─────────────────────────────────────")


# ============================================
# CASOS DE TESTE V2
# ============================================

CASOS_TESTE_V2 = [
    # Casos básicos
    "Como está o Pablo?",
    "Status da Silvane",
    "Juliana está ok?",
    "Última call da Dani",

    # Múltiplos resultados
    "Como está o Rafael?",
    "Status do Castro",

    # Nome completo
    "Como está a Juliana Altavilla?",
    "Status da Silvane Castro",

    # Sobrenome apenas
    "Como está o Santos?",

    # Múltiplos nomes
    "Como está o Pablo e a Silvane?",
    "Status do Rafael e da Juliana",

    # Consultas genéricas
    "Quem precisa atenção?",
    "Alguém está travado?",

    # Casos sem resultado
    "Como está o João?",

    # Casos complexos
    "Pablo e Rafael estão ok?",
]


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTE DE EXTRAÇÃO V2 - VERSÃO MELHORADA")
    print("="*80)

    for mensagem in CASOS_TESTE_V2:
        testar_mensagem_v2(mensagem)

    print("\n" + "="*80)
    print("📊 MELHORIAS IMPLEMENTADAS")
    print("="*80)
    print("""
✅ Filtro de stopwords
   • Remove "como", "está", "o", "a", etc.

✅ Validação contra lista conhecida
   • Só aceita nomes da lista de primeiros nomes/sobrenomes
   • Evita falsos positivos

✅ Suporte para nome completo
   • "Juliana Altavilla" detectado corretamente
   • Busca mais precisa

✅ Detecção de múltiplos nomes
   • "Pablo e Silvane" → processa ambos
   • Identifica ambiguidades
   • Sugere ação correta

✅ Identificação de consultas genéricas
   • "Quem precisa atenção?" não tenta extrair nome
   • Sugere usar buscarTodasUrgencias()
""")

    print("\n" + "="*80)
    print("🎯 INTEGRAÇÃO COM AGENTE N8N")
    print("="*80)
    print("""
O Agente Consulta no workflow já está preparado para:

1. **Tool buscarMentorado(nome):**
   - Faz busca LIKE no banco
   - Retorna TODOS os resultados

2. **System Prompt:**
   - Instrui agente a listar múltiplos resultados
   - Pede clarificação antes de prosseguir
   - NÃO processa se houver ambiguidade

3. **Detecção de padrões:**
   - Identifica consulta genérica vs busca por nome
   - Usa tool apropriada (buscarTodasUrgencias vs buscarMentorado)

**PRÓXIMO PASSO:**
Testar no n8n enviando mensagens reais pelo WhatsApp e validar comportamento.
""")

    print("="*80 + "\n")
