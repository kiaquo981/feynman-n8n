// ============================================
// CÓDIGO JAVASCRIPT PARA NÓ "ROTEADOR"
// Copie e cole este código no nó "Roteador" do n8n
// ============================================

const msg = $('Filtrar Válidos').first().json;
const busca = $('Buscar Mentorado').all();
const QUEILA_PHONE = '5511964682447';

// ========================================
// EXTRAIR MENTORADO (se encontrado)
// ========================================

let mentorado = null;

if (busca.length > 0 && busca[0].json) {
  // Supabase pode retornar array vazio [] ou null
  // Verificar se tem dados reais
  const resultado = busca[0].json;

  // Checar se é um objeto válido com id
  if (resultado && typeof resultado === 'object' && resultado.id) {
    mentorado = resultado;
  }
}

// ========================================
// LOGS PARA DEBUG
// ========================================

console.log('='.repeat(80));
console.log('[ROTEADOR] Telefone:', msg.sender_phone);
console.log('[ROTEADOR] Nome sender:', msg.sender_name);
console.log('[ROTEADOR] Mentorado encontrado:', mentorado ? mentorado.nome : 'Nenhum');
console.log('[ROTEADOR] É grupo:', msg.is_group);

// ========================================
// DECISÃO DE ROTEAMENTO
// ========================================

// 1. MENSAGEM DA QUEILA (sempre consulta, independente de grupo ou não)
if (msg.sender_phone === QUEILA_PHONE) {
  console.log('[ROTEADOR] Decisão: CONSULTA (Queila)');
  console.log('='.repeat(80));

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
  console.log('[ROTEADOR] Decisão: PROCESSAR_GRUPO');
  console.log('[ROTEADOR] Mentorado:', mentorado.nome, '(ID:', mentorado.id, ')');
  console.log('='.repeat(80));

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
  console.log('[ROTEADOR] Decisão: PROCESSAR_PRIVADO');
  console.log('[ROTEADOR] Mentorado:', mentorado.nome, '(ID:', mentorado.id, ')');
  console.log('='.repeat(80));

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
  console.log('[ROTEADOR] Decisão: IGNORE (grupo de não-mentorado)');
  console.log('[ROTEADOR] Telefone não cadastrado:', msg.sender_phone);
  console.log('='.repeat(80));

  return [{
    json: {
      route: 'ignore',
      reason: 'Grupo de não-mentorado',
      sender_phone: msg.sender_phone,
      sender_name: msg.sender_name
    }
  }];
}

// 5. PRIVADO DE NÃO-MENTORADO (ignorar com alerta)
if (!msg.is_group && !mentorado) {
  console.log('[ROTEADOR] Decisão: IGNORE (telefone não cadastrado)');
  console.log('[ROTEADOR] Telefone:', msg.sender_phone);
  console.log('[ROTEADOR] Nome:', msg.sender_name);
  console.log('[ROTEADOR] ⚠️ Possível novo interessado?');
  console.log('='.repeat(80));

  return [{
    json: {
      route: 'ignore',
      reason: 'Telefone não cadastrado',
      sender_phone: msg.sender_phone,
      sender_name: msg.sender_name,
      alert: 'Possível novo interessado'
    }
  }];
}

// 6. FALLBACK (não deveria chegar aqui)
console.log('[ROTEADOR] Decisão: IGNORE (caso não previsto)');
console.log('[ROTEADOR] Debug:', {
  is_group: msg.is_group,
  has_mentorado: !!mentorado,
  sender_phone: msg.sender_phone
});
console.log('='.repeat(80));

return [{
  json: {
    route: 'ignore',
    reason: 'Caso não previsto',
    debug: {
      is_group: msg.is_group,
      has_mentorado: !!mentorado,
      sender_phone: msg.sender_phone,
      sender_name: msg.sender_name
    }
  }
}];
