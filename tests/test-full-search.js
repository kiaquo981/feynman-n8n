/**
 * Teste completo: Extração de nomes + Busca no banco de dados simulado
 */

const fs = require('fs');
const path = require('path');
const { extractNames, extractNamesWithContext } = require('../functions/extractNames');

// Carregar banco de dados de exemplo
const dbPath = path.join(__dirname, '../data/sample-people-database.json');
const peopleDatabase = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

/**
 * Simula busca no banco de dados
 */
function searchPeopleInDatabase(names) {
  const results = [];

  names.forEach(searchName => {
    const nameLower = searchName.toLowerCase();

    // Buscar pessoas que correspondem ao nome
    const matches = peopleDatabase.filter(person => {
      const nomeCompleto = person.nome_completo.toLowerCase();
      const primeiroNome = person.primeiro_nome.toLowerCase();

      return nomeCompleto.includes(nameLower) ||
             nameLower.includes(primeiroNome) ||
             primeiroNome.includes(nameLower);
    });

    matches.forEach(match => {
      results.push({
        searchedName: searchName,
        ...match
      });
    });
  });

  // Remover duplicatas por ID
  const uniqueResults = {};
  results.forEach(result => {
    if (!uniqueResults[result.id]) {
      uniqueResults[result.id] = result;
    }
  });

  return Object.values(uniqueResults);
}

/**
 * Processa mensagem completa: extrai nomes e busca no banco
 */
function processMessage(message) {
  console.log('\n' + '='.repeat(80));
  console.log(`MENSAGEM: "${message}"`);
  console.log('='.repeat(80));

  // Etapa 1: Extrair nomes
  console.log('\n[1] Extraindo nomes da mensagem...');
  const extractedNames = extractNamesWithContext(message);

  if (extractedNames.length === 0) {
    console.log('   ✗ Nenhum nome encontrado na mensagem');
    return {
      success: false,
      message: 'Nenhum nome encontrado',
      extractedNames: [],
      peopleFound: []
    };
  }

  console.log(`   ✓ ${extractedNames.length} nome(s) encontrado(s):`);
  extractedNames.forEach(item => {
    console.log(`      - ${item.name} (${item.mentionType}, confiança: ${(item.confidence * 100).toFixed(0)}%)`);
  });

  // Etapa 2: Buscar no banco de dados
  console.log('\n[2] Buscando pessoas no banco de dados...');
  const names = extractedNames.map(n => n.name);
  const peopleFound = searchPeopleInDatabase(names);

  if (peopleFound.length === 0) {
    console.log('   ✗ Nenhuma pessoa encontrada no banco de dados');
    return {
      success: false,
      message: 'Nenhuma pessoa encontrada no banco',
      extractedNames: names,
      peopleFound: []
    };
  }

  console.log(`   ✓ ${peopleFound.length} pessoa(s) encontrada(s) no banco:`);
  peopleFound.forEach(person => {
    console.log(`\n      Nome: ${person.nome_completo}`);
    console.log(`      Email: ${person.email}`);
    console.log(`      Telefone: ${person.telefone}`);
    console.log(`      Empresa: ${person.empresa}`);
    console.log(`      Cargo: ${person.cargo}`);
    console.log(`      (Buscado por: "${person.searchedName}")`);
  });

  return {
    success: true,
    message: 'Pessoas encontradas com sucesso',
    extractedNames: names,
    peopleFound: peopleFound
  };
}

// ============================================================================
// EXECUTAR TESTES
// ============================================================================

console.log('\n\n');
console.log('╔════════════════════════════════════════════════════════════════════════════╗');
console.log('║           TESTE COMPLETO: EXTRAÇÃO + BUSCA NO BANCO DE DADOS              ║');
console.log('╚════════════════════════════════════════════════════════════════════════════╝');

const testCases = [
  "Preciso falar com Maria Silva sobre o projeto Mentory",
  "Agendar reunião com Ana Carolina e Carlos Eduardo na segunda",
  "Enviar proposta para Rafael e confirmar com Beatriz",
  "Ligar para Dr. Fernando Santos",
  "Preciso dos contatos de Rodrigo Fernandes e Juliana Costa",
  "Conversar com Queila Trizotti sobre o mapa de identificação",
  "Mensagem urgente sem nome de pessoa específica",
  "A Luciana Teixeira enviou material. Revisar com Pedro Henrique."
];

const results = [];

testCases.forEach((message, index) => {
  const result = processMessage(message);
  results.push(result);

  if (index < testCases.length - 1) {
    console.log('\n');
  }
});

// Resumo final
console.log('\n\n');
console.log('╔════════════════════════════════════════════════════════════════════════════╗');
console.log('║                           RESUMO DOS TESTES                                ║');
console.log('╚════════════════════════════════════════════════════════════════════════════╝');

const totalTests = results.length;
const successfulTests = results.filter(r => r.success && r.peopleFound.length > 0).length;
const testsWithExtraction = results.filter(r => r.extractedNames.length > 0).length;
const testsWithPeople = results.filter(r => r.peopleFound.length > 0).length;

console.log(`\nTotal de mensagens testadas: ${totalTests}`);
console.log(`Mensagens com nomes extraídos: ${testsWithExtraction} (${((testsWithExtraction/totalTests)*100).toFixed(1)}%)`);
console.log(`Mensagens com pessoas encontradas: ${testsWithPeople} (${((testsWithPeople/totalTests)*100).toFixed(1)}%)`);
console.log(`Taxa de sucesso completo: ${((successfulTests/totalTests)*100).toFixed(1)}%`);

console.log('\n✓ Teste completo finalizado!\n');
