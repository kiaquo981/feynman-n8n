# Feynman N8N - Busca de Pessoas por Nome em Mensagens

Sistema automatizado para extrair nomes de pessoas de mensagens de texto e buscar informações na base de dados.

## 📋 Sobre o Projeto

Este projeto implementa uma solução completa para:
1. **Extrair nomes de pessoas** de mensagens em português usando padrões de linguagem natural
2. **Buscar automaticamente** essas pessoas em uma base de dados
3. **Retornar informações completas** sobre as pessoas encontradas

Baseado no conceito de "Mapa de Identificação" para comunicação estratégica.

## 🚀 Funcionalidades

### Extração Inteligente de Nomes
- Identifica nomes próprios em mensagens de texto
- Reconhece contextos como "falar com [Nome]", "entregar para [Nome]"
- Suporta nomes compostos (ex: Maria Silva, João Pedro)
- Filtra palavras comuns que não são nomes
- Suporta acentuação em português

### Busca no Banco de Dados
- Busca por nome completo ou primeiro nome
- Busca flexível (case-insensitive)
- Suporta múltiplos nomes em uma única mensagem
- Remove duplicatas automaticamente

## 📁 Estrutura do Projeto

```
feynman-n8n/
├── functions/
│   └── extractNames.js          # Funções de extração de nomes
├── workflows/
│   └── search-person-workflow.json  # Workflow do n8n
├── tests/
│   ├── test-extract-names.js    # Teste de extração
│   └── test-full-search.js      # Teste completo (extração + busca)
├── data/
│   └── sample-people-database.json  # Base de dados de exemplo
└── README.md
```

## 🔧 Como Usar

### 1. Configurar o n8n

1. Importe o workflow `workflows/search-person-workflow.json` no seu n8n
2. Configure a conexão com seu banco de dados (PostgreSQL, MySQL, MongoDB, etc.)
3. Ajuste a query SQL conforme sua estrutura de tabela

### 2. Estrutura da Tabela de Pessoas (Exemplo)

```sql
CREATE TABLE pessoas (
  id SERIAL PRIMARY KEY,
  nome_completo VARCHAR(255),
  primeiro_nome VARCHAR(100),
  email VARCHAR(255),
  telefone VARCHAR(20),
  empresa VARCHAR(255),
  cargo VARCHAR(100),
  data_cadastro DATE
);
```

### 3. Usar a API

Envie uma requisição POST para o webhook do n8n:

```bash
curl -X POST https://seu-n8n.com/webhook/search-person \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Preciso falar com Maria Silva sobre o projeto"
  }'
```

**Resposta:**
```json
{
  "success": true,
  "totalFound": 1,
  "pessoas": [
    {
      "id": 1,
      "nome": "Maria Silva Santos",
      "email": "maria.silva@email.com",
      "telefone": "+55 11 98765-4321",
      "empresa": "Mentory Consultoria",
      "cargo": "Gerente de Projetos"
    }
  ],
  "originalMessage": "Preciso falar com Maria Silva sobre o projeto"
}
```

## 🧪 Executar Testes

### Teste de Extração de Nomes

```bash
cd /home/user/feynman-n8n
node tests/test-extract-names.js
```

Este teste valida se a função está extraindo corretamente os nomes de diferentes tipos de mensagens.

### Teste Completo (Extração + Busca)

```bash
node tests/test-full-search.js
```

Este teste simula o fluxo completo:
1. Extrai nomes da mensagem
2. Busca no banco de dados de exemplo
3. Retorna as pessoas encontradas

## 📝 Exemplos de Uso

### Mensagens Suportadas

✅ **Com contexto:**
- "Preciso falar com Maria Silva sobre o projeto"
- "Entregar documento para João Pedro amanhã"
- "Agendar reunião com Ana Carolina"

✅ **Nome direto:**
- "A Luciana Teixeira enviou o material"
- "Rodrigo Fernandes está confirmado"

✅ **Múltiplos nomes:**
- "Reunião com Carlos Eduardo e Beatriz Almeida"
- "Enviar para Rafael e Juliana"

✅ **Menções:**
- "Falar com @PauloRoberto sobre o orçamento"

### Padrões Reconhecidos

A função reconhece os seguintes padrões:
- `falar com [Nome]`
- `entregar para [Nome]`
- `enviar para [Nome]`
- `contatar [Nome]`
- `ligar para [Nome]`
- `mensagem para [Nome]`
- `agendar com [Nome]`
- `reunião com [Nome]`
- `encontrar com [Nome]`
- `conversar com [Nome]`
- `@[Nome]`

## 🎯 Níveis de Confiança

O sistema atribui um score de confiança para cada nome extraído:

- **Alta confiança (≥80%)**: Nome completo + contexto claro
- **Média confiança (50-79%)**: Nome único ou contexto parcial
- **Baixa confiança (<50%)**: Palavra capitalizada sem contexto

## 🔌 Integrações

O workflow pode ser integrado com:
- **WhatsApp** (via API ou n8n-nodes-whatsapp)
- **Telegram**
- **Email**
- **Slack**
- **Microsoft Teams**
- Qualquer fonte de mensagens via webhook

## 🗄️ Bancos de Dados Suportados

- PostgreSQL
- MySQL / MariaDB
- MongoDB
- SQLite
- Microsoft SQL Server
- Oracle
- Qualquer banco compatível com n8n

## 📊 Casos de Uso

### 1. Atendimento ao Cliente
Identifica menções a clientes em mensagens e busca seu histórico automaticamente.

### 2. Gestão de Projetos
Extrai nomes de colaboradores mencionados em updates e notifica as pessoas certas.

### 3. CRM Automatizado
Captura menções a leads/prospects e atualiza o CRM automaticamente.

### 4. Triagem de Mensagens
Roteia mensagens para os responsáveis baseado em quem foi mencionado.

## ⚙️ Configurações Avançadas

### Ajustar Sensibilidade

Edite `functions/extractNames.js` para ajustar:
- Lista de stop words
- Padrões de regex
- Score de confiança mínimo

### Adicionar Novos Padrões

```javascript
const pattern = /novo padrão aqui/gi;
```

### Customizar Busca no Banco

Ajuste a query SQL no nó "Buscar no Banco de Dados" do workflow.

## 🐛 Troubleshooting

### Nomes não estão sendo extraídos
- Verifique se os nomes estão com a primeira letra maiúscula
- Adicione novos padrões de contexto em `extractNames.js`

### Muitos falsos positivos
- Adicione palavras à lista `STOP_WORDS`
- Aumente o score mínimo de confiança

### Pessoas não encontradas no banco
- Verifique a query SQL
- Confirme que os dados existem na tabela
- Teste busca por primeiro nome apenas

## 📄 Licença

Este projeto faz parte do sistema Mentory de identificação e mapeamento de comunicação estratégica.

## 👥 Autor

Desenvolvido para integração com o Mapa de Identificação Mentory (Queila Trizotti)

---

**Status do Projeto:** ✅ Pronto para testes

**Última atualização:** 2025-10-21
