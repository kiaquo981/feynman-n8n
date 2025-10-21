/**
 * Função para extrair nomes de pessoas de mensagens em português
 * Utiliza padrões comuns e lista de pronomes para identificação
 */

// Lista de palavras comuns que não são nomes
const STOP_WORDS = [
  'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
  'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
  'para', 'com', 'por', 'sobre', 'entre', 'sem', 'sob',
  'este', 'esse', 'aquele', 'esta', 'essa', 'aquela',
  'meu', 'teu', 'seu', 'nosso', 'vosso', 'minha', 'tua', 'sua', 'nossa', 'vossa',
  'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
  'me', 'te', 'se', 'lhe', 'nos', 'vos', 'lhes',
  'mim', 'ti', 'si',
  'senhor', 'senhora', 'dr', 'dra', 'doutor', 'doutora',
  'whatsapp', 'email', 'telefone', 'celular',
  'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo',
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
];

// Prefixos de tratamento
const TITLE_PREFIXES = [
  'sr', 'sra', 'srta', 'dr', 'dra', 'prof', 'profa',
  'eng', 'arq', 'adv', 'senhor', 'senhora'
];

/**
 * Extrai nomes próprios de uma mensagem
 * @param {string} message - Mensagem para extrair nomes
 * @returns {Array} Array de nomes encontrados
 */
function extractNames(message) {
  if (!message || typeof message !== 'string') {
    return [];
  }

  const names = [];

  // Padrão 1: "falar com [Nome]" ou "entregar para [Nome]"
  const pattern1 = /(?:falar com|entregar para|enviar para|contatar|ligar para|mensagem para|agendar com|reunião com|encontrar com)\s+([A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]+(?:\s+[A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]+)*)/gi;
  let matches = message.match(pattern1);
  if (matches) {
    matches.forEach(match => {
      const name = match.replace(/.+\s+/, '').trim();
      if (name && !STOP_WORDS.includes(name.toLowerCase())) {
        names.push(name);
      }
    });
  }

  // Padrão 2: Nome próprio (palavras iniciadas com maiúscula, mínimo 2 caracteres)
  const pattern2 = /\b([A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]{1,}(?:\s+(?:da|de|do|das|dos|e)\s+)?(?:[A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]+)*)\b/g;
  matches = message.match(pattern2);
  if (matches) {
    matches.forEach(match => {
      const name = match.trim();
      const nameLower = name.toLowerCase();

      // Filtrar stop words e nomes muito curtos
      if (name.length >= 3 && !STOP_WORDS.includes(nameLower)) {
        // Verificar se não é uma palavra comum no início de frase
        const words = name.split(/\s+/);
        if (words.length >= 2 || !isCommonSentenceStarter(name)) {
          names.push(name);
        }
      }
    });
  }

  // Padrão 3: "@Nome" ou "#Nome" (menções)
  const pattern3 = /[@#]([A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]+(?:\s+[A-ZÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇ][a-zàáâãäåçèéêëìíîïñòóôõöùúûüý]+)*)/g;
  matches = message.match(pattern3);
  if (matches) {
    matches.forEach(match => {
      const name = match.substring(1).trim();
      if (name && !STOP_WORDS.includes(name.toLowerCase())) {
        names.push(name);
      }
    });
  }

  // Remover duplicatas e retornar
  return [...new Set(names)];
}

/**
 * Verifica se é uma palavra comum que inicia frases
 */
function isCommonSentenceStarter(word) {
  const commonStarters = [
    'Olá', 'Oi', 'Bom', 'Boa', 'Prezado', 'Prezada',
    'Caro', 'Cara', 'Obrigado', 'Obrigada', 'Sim', 'Não',
    'Por', 'Favor', 'Desculpe', 'Com', 'Então', 'Assim',
    'Quando', 'Como', 'Onde', 'Porque', 'Qual', 'Quais',
    'Gostaria', 'Preciso', 'Quero', 'Pode', 'Poderia',
    'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'
  ];
  return commonStarters.includes(word);
}

/**
 * Extrai nomes e informações contextuais adicionais
 * @param {string} message - Mensagem para extrair nomes
 * @returns {Array} Array de objetos com nome e contexto
 */
function extractNamesWithContext(message) {
  const names = extractNames(message);

  return names.map(name => {
    // Encontrar o contexto ao redor do nome
    const nameIndex = message.indexOf(name);
    const contextStart = Math.max(0, nameIndex - 50);
    const contextEnd = Math.min(message.length, nameIndex + name.length + 50);
    const context = message.substring(contextStart, contextEnd).trim();

    // Tentar identificar o tipo de menção
    let mentionType = 'general';
    if (message.match(new RegExp(`(?:falar com|contatar|ligar para)\\s+${name}`, 'i'))) {
      mentionType = 'contact';
    } else if (message.match(new RegExp(`(?:entregar para|enviar para)\\s+${name}`, 'i'))) {
      mentionType = 'delivery';
    } else if (message.match(new RegExp(`(?:agendar com|reunião com|encontrar com)\\s+${name}`, 'i'))) {
      mentionType = 'meeting';
    }

    return {
      name: name,
      context: context,
      mentionType: mentionType,
      confidence: calculateConfidence(name, message)
    };
  });
}

/**
 * Calcula um score de confiança de que a palavra é realmente um nome
 */
function calculateConfidence(name, message) {
  let confidence = 0.5; // Base

  // Aumentar confiança se tem mais de uma palavra (nome completo)
  if (name.split(/\s+/).length >= 2) {
    confidence += 0.2;
  }

  // Aumentar confiança se está em contexto de ação com pessoa
  if (message.match(new RegExp(`(?:falar com|contatar|ligar para|entregar para|enviar para|agendar com)\\s+${name}`, 'i'))) {
    confidence += 0.2;
  }

  // Aumentar confiança se começa com @
  if (message.includes('@' + name)) {
    confidence += 0.1;
  }

  return Math.min(1.0, confidence);
}

// Exportar funções
module.exports = {
  extractNames,
  extractNamesWithContext
};

// Para uso em n8n (ambiente sem module.exports)
if (typeof module === 'undefined') {
  // Funções disponíveis globalmente no n8n
}
