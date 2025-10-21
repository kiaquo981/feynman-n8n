/**
 * Script de teste para extração de nomes de mensagens
 */

const { extractNames, extractNamesWithContext } = require('../functions/extractNames');

// Mensagens de teste
const testMessages = [
  {
    id: 1,
    message: "Preciso falar com Maria Silva sobre o projeto",
    expectedNames: ["Maria Silva"]
  },
  {
    id: 2,
    message: "Pode entregar o documento para João Pedro amanhã?",
    expectedNames: ["João Pedro"]
  },
  {
    id: 3,
    message: "Agendar reunião com Ana Carolina e Carlos Eduardo na segunda-feira",
    expectedNames: ["Ana Carolina", "Carlos Eduardo"]
  },
  {
    id: 4,
    message: "Enviar mensagem para @PauloRoberto sobre o orçamento",
    expectedNames: ["PauloRoberto"]
  },
  {
    id: 5,
    message: "Ligar para Dr. Fernando Santos e confirmar consulta",
    expectedNames: ["Fernando Santos"]
  },
  {
    id: 6,
    message: "Conversar com Beatriz sobre os resultados do mapa de identificação",
    expectedNames: ["Beatriz"]
  },
  {
    id: 7,
    message: "Preciso dos dados de Rodrigo Fernandes e Juliana Costa para o relatório",
    expectedNames: ["Rodrigo Fernandes", "Juliana Costa"]
  },
  {
    id: 8,
    message: "Oi, tudo bem? Preciso falar urgente!",
    expectedNames: []
  },
  {
    id: 9,
    message: "Contactar Rafael sobre a proposta comercial da Mentory",
    expectedNames: ["Rafael"]
  },
  {
    id: 10,
    message: "A Luciana Teixeira enviou o material. Precisa revisar com Pedro Henrique.",
    expectedNames: ["Luciana Teixeira", "Pedro Henrique"]
  },
  {
    id: 11,
    message: "Marcar apresentação com Camila Rodrigues e equipe de marketing",
    expectedNames: ["Camila Rodrigues"]
  },
  {
    id: 12,
    message: "Enviar proposta para gabriela.santos@empresa.com - Gabriela Santos",
    expectedNames: ["Gabriela Santos"]
  }
];

console.log('=== TESTE DE EXTRAÇÃO DE NOMES ===\n');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

testMessages.forEach(test => {
  totalTests++;
  console.log(`\n--- Teste #${test.id} ---`);
  console.log(`Mensagem: "${test.message}"`);

  const extractedNames = extractNames(test.message);
  console.log(`Nomes extraídos: [${extractedNames.join(', ')}]`);
  console.log(`Nomes esperados: [${test.expectedNames.join(', ')}]`);

  // Verificar se todos os nomes esperados foram encontrados
  const allFound = test.expectedNames.every(expectedName =>
    extractedNames.some(extracted =>
      extracted.toLowerCase().includes(expectedName.toLowerCase()) ||
      expectedName.toLowerCase().includes(extracted.toLowerCase())
    )
  );

  if (allFound && extractedNames.length >= test.expectedNames.length) {
    console.log('✓ PASSOU');
    passedTests++;
  } else {
    console.log('✗ FALHOU');
    failedTests++;
  }
});

console.log('\n\n=== TESTE COM CONTEXTO ===\n');

// Testar extração com contexto
const testMessage = "Preciso agendar reunião com Maria Silva e enviar documentos para João Pedro sobre o projeto Mentory";
console.log(`Mensagem: "${testMessage}"\n`);

const namesWithContext = extractNamesWithContext(testMessage);
namesWithContext.forEach(result => {
  console.log(`Nome: ${result.name}`);
  console.log(`Tipo de menção: ${result.mentionType}`);
  console.log(`Confiança: ${(result.confidence * 100).toFixed(0)}%`);
  console.log(`Contexto: "...${result.context}..."`);
  console.log('---');
});

console.log('\n\n=== RESUMO DOS TESTES ===');
console.log(`Total de testes: ${totalTests}`);
console.log(`Passou: ${passedTests} (${((passedTests/totalTests)*100).toFixed(1)}%)`);
console.log(`Falhou: ${failedTests} (${((failedTests/totalTests)*100).toFixed(1)}%)`);

if (passedTests === totalTests) {
  console.log('\n✓ TODOS OS TESTES PASSARAM! 🎉');
  process.exit(0);
} else {
  console.log('\n✗ Alguns testes falharam. Revise a implementação.');
  process.exit(1);
}
