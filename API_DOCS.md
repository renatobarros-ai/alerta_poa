# 🔌 API Documentation

## Sistema de Monitoramento de Alagamentos - Porto Alegre

Documentação completa das APIs REST e WebSocket do sistema.

---

## 📚 Índice

- [Visão Geral](#visão-geral)
- [Autenticação](#autenticação)
- [Endpoints REST](#endpoints-rest)
- [WebSocket API](#websocket-api)
- [Modelos de Dados](#modelos-de-dados)
- [Códigos de Erro](#códigos-de-erro)
- [Exemplos](#exemplos)

---

## 🎯 Visão Geral

### Base URL
```
http://localhost:8000/api/
```

### Formato de Resposta
Todas as respostas são em JSON:

```json
{
  "status": "success|error",
  "data": {},
  "message": "Mensagem opcional",
  "timestamp": "2025-06-02T14:30:00Z"
}
```

### Headers Recomendados
```http
Content-Type: application/json
Accept: application/json
X-CSRFToken: [token] (para POST/PUT/DELETE)
```

---

## 🔐 Autenticação

### APIs Públicas
A maioria das APIs são públicas para fins acadêmicos:
- ✅ Leitura de dados (GET)
- ✅ Consultas de status
- ✅ Dashboard e estatísticas

### APIs Protegidas
Algumas operações requerem CSRF token:
- 🔒 Cadastro de usuários (POST)
- 🔒 Simulação manual (POST)
- 🔒 Exclusão de dados (DELETE)

### Como obter CSRF Token
```javascript
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
```

---

## 🚀 Endpoints REST

### 🗺️ Regiões

#### Listar Regiões
```http
GET /api/regioes/
```

**Resposta:**
```json
[
  {
    "id": 1,
    "numero": 1,
    "nome": "Centro Histórico",
    "geojson": "{\"type\":\"Polygon\",...}",
    "created_at": "2025-06-02T10:00:00Z",
    "updated_at": "2025-06-02T10:00:00Z"
  }
]
```

#### Detalhes de uma Região
```http
GET /api/regioes/{id}/
```

**Parâmetros:**
- `id` (integer): ID da região

---

### 📊 Dashboard e Status

#### Situação Atual
```http
GET /api/situacao-atual/
```

**Resposta:**
```json
[
  {
    "id": 1,
    "numero": 1,
    "nome": "Centro Histórico",
    "status_atual": "Normal",
    "cor_atual": "Verde",
    "usuarios_cadastrados": 5,
    "ultima_medicao": "2025-06-02T14:30:00Z"
  }
]
```

#### Estatísticas do Dashboard
```http
GET /api/dashboard/
```

**Resposta:**
```json
{
  "total_regioes": 16,
  "regioes_normais": 12,
  "regioes_alerta": 3,
  "regioes_criticas": 1,
  "total_usuarios": 25,
  "usuarios_ativos": 20,
  "alertas_hoje": 8,
  "ultima_atualizacao": "2025-06-02T14:30:00Z"
}
```

#### Status em Tempo Real
```http
GET /api/status-regioes-tempo-real/
```

**Resposta:**
```json
[
  {
    "regiao_id": 1,
    "regiao_nome": "Centro Histórico",
    "status_nivel": 0,
    "status_cor": "Verde",
    "status_descricao": "Normal",
    "pessoas_detectadas": false,
    "nivel_agua": 1,
    "volume_chuva": 1,
    "confianca_ia": null,
    "timestamp": "2025-06-02T14:30:00Z"
  }
]
```

---

### 📈 Histórico e Medições

#### Histórico de Alertas
```http
GET /api/historico-alertas/
```

**Parâmetros Query:**
- `dias` (integer): Número de dias (default: 7)
- `regiao` (integer): ID da região (opcional)
- `tipo` (string): Tipo de alerta (opcional)
- `status` (string): Status de envio (opcional)

**Exemplo:**
```http
GET /api/historico-alertas/?dias=30&regiao=1&tipo=Crítico
```

**Resposta:**
```json
[
  {
    "id": 1,
    "data": "2025-06-02T14:30:00Z",
    "regiao": "Centro Histórico",
    "usuario": "João Silva",
    "telefone": "51999887766",
    "email": "joao@email.com",
    "tipo_alerta": "Crítico",
    "cor": "Vermelho",
    "envio_whats": true,
    "envio_email": true,
    "sucesso_whats": true,
    "sucesso_email": true,
    "confianca_ia": 0.856
  }
]
```

#### Medições Recentes
```http
GET /api/medicoes/
```

**Parâmetros Query:**
- `regiao` (integer): ID da região (opcional)

**Resposta:**
```json
[
  {
    "id": 1,
    "data": "2025-06-02T14:30:00Z",
    "regiao": 1,
    "regiao_nome": "Centro Histórico",
    "nivel_agua": 2,
    "nivel_agua_descricao": "Alerta",
    "volume_chuva": 2,
    "volume_chuva_descricao": "Moderada",
    "avaliar_risco": true,
    "created_at": "2025-06-02T14:30:00Z"
  }
]
```

#### Análises de Risco
```http
GET /api/riscos/
```

**Parâmetros Query:**
- `risco` (boolean): Filtrar por risco detectado

**Resposta:**
```json
[
  {
    "id": 1,
    "data": "2025-06-02T14:30:00Z",
    "medicao": {
      "id": 1,
      "regiao_nome": "Centro Histórico"
    },
    "imagem": "simulada_regiao_1_20250602_143000.jpg",
    "risco": true,
    "status": {
      "nivel": 2,
      "descricao": "Crítico",
      "cor": "Vermelho"
    },
    "processamento_tempo": 1.234,
    "confianca_ia": 0.856,
    "created_at": "2025-06-02T14:30:00Z"
  }
]
```

---

### 👥 Cadastros

#### Listar Cadastros
```http
GET /api/cadastros/
```

**Resposta:**
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "João Silva",
      "telefone": "51999887766",
      "email": "joao@email.com",
      "regiao": 1,
      "regiao_nome": "Centro Histórico",
      "situacao": "ATIVO",
      "created_at": "2025-06-02T10:00:00Z",
      "updated_at": "2025-06-02T10:00:00Z"
    }
  ]
}
```

#### Criar Cadastro
```http
POST /api/cadastros/
Content-Type: application/json
X-CSRFToken: [token]

{
  "nome": "Maria Santos",
  "telefone": "51988776655",
  "email": "maria@email.com",
  "regiao": 1,
  "situacao": "ATIVO"
}
```

**Resposta (201 Created):**
```json
{
  "id": 26,
  "nome": "Maria Santos",
  "telefone": "51988776655",
  "email": "maria@email.com",
  "regiao": 1,
  "regiao_nome": "Centro Histórico",
  "situacao": "ATIVO",
  "created_at": "2025-06-02T14:30:00Z",
  "updated_at": "2025-06-02T14:30:00Z"
}
```

#### Obter Cadastro
```http
GET /api/cadastros/{id}/
```

#### Atualizar Cadastro
```http
PUT /api/cadastros/{id}/
Content-Type: application/json
X-CSRFToken: [token]

{
  "nome": "Maria Santos Silva",
  "situacao": "INATIVO"
}
```

#### Deletar Cadastro
```http
DELETE /api/cadastros/{id}/
X-CSRFToken: [token]
```

---

### 🎮 Simulação

#### Executar Simulação
```http
POST /api/simulacao/executar/
X-CSRFToken: [token]
```

**Resposta:**
```json
{
  "sucesso": true,
  "resultado": {
    "medicoes_criadas": 16,
    "riscos_avaliados": 4,
    "alertas_gerados": 2,
    "timestamp": "2025-06-02T14:30:00Z"
  },
  "timestamp": "2025-06-02T14:30:00Z"
}
```

---

### 📋 Status e Configurações

#### Listar Status Possíveis
```http
GET /api/status/
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nivel": 0,
    "descricao": "Normal",
    "cor": "Verde",
    "tipo_alerta": "Nenhum",
    "cnn_ativa": false,
    "created_at": "2025-06-02T10:00:00Z"
  }
]
```

---

## 🔌 WebSocket API

### Conexão
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/alagamentos/');
```

### Eventos Recebidos

#### 1. Dados Iniciais
```json
{
  "type": "initial_data",
  "data": [...],
  "timestamp": "2025-06-02T14:30:00Z"
}
```

#### 2. Atualização de Status
```json
{
  "type": "status_update",
  "data": [
    {
      "regiao_id": 1,
      "regiao_nome": "Centro Histórico",
      "status_nivel": 2,
      "status_cor": "Vermelho",
      "pessoas_detectadas": true
    }
  ],
  "timestamp": "2025-06-02T14:30:00Z"
}
```

#### 3. Alerta de Região
```json
{
  "type": "region_alert",
  "region_id": 1,
  "alert_level": 2,
  "message": "Pessoas detectadas em área de risco crítico",
  "timestamp": "2025-06-02T14:30:00Z"
}
```

#### 4. Notificação do Sistema
```json
{
  "type": "system_notification",
  "message": "Simulação executada com sucesso",
  "level": "info",
  "timestamp": "2025-06-02T14:30:00Z"
}
```

### Eventos Enviados

#### Solicitar Atualização
```json
{
  "type": "request_update"
}
```

#### Inscrever-se em Região
```json
{
  "type": "subscribe_region",
  "region_id": 1
}
```

---

## 📝 Modelos de Dados

### Região
```json
{
  "id": "integer",
  "numero": "integer (1-16)",
  "nome": "string",
  "geojson": "string (JSON)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Status
```json
{
  "id": "integer",
  "nivel": "integer (0-2)",
  "descricao": "string",
  "cor": "string",
  "tipo_alerta": "string",
  "cnn_ativa": "boolean"
}
```

### Medição
```json
{
  "id": "integer",
  "data": "datetime",
  "regiao": "integer (FK)",
  "nivel_agua": "integer (1-3)",
  "volume_chuva": "integer (1-3)",
  "avaliar_risco": "boolean"
}
```

### Risco Humano
```json
{
  "id": "integer",
  "data": "datetime",
  "medicao": "integer (FK)",
  "imagem": "string (path)",
  "risco": "boolean",
  "status": "integer (FK)",
  "processamento_tempo": "decimal",
  "confianca_ia": "decimal (0-1)"
}
```

### Cadastro
```json
{
  "id": "integer",
  "nome": "string",
  "telefone": "string",
  "email": "string (unique)",
  "regiao": "integer (FK)",
  "situacao": "enum (ATIVO|INATIVO|BLOQUEADO)"
}
```

---

## ❌ Códigos de Erro

### HTTP Status Codes

| Code | Descrição |
|------|-----------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Não autorizado |
| 403 | Forbidden - CSRF token inválido |
| 404 | Not Found - Recurso não encontrado |
| 405 | Method Not Allowed - Método não permitido |
| 500 | Internal Server Error - Erro interno |

### Erros Comuns

#### Erro de Validação (400)
```json
{
  "email": ["Este email já está cadastrado."],
  "telefone": ["Este campo é obrigatório."]
}
```

#### Erro CSRF (403)
```json
{
  "detail": "CSRF Failed: CSRF token missing or incorrect."
}
```

#### Recurso não encontrado (404)
```json
{
  "detail": "Not found."
}
```

---

## 💡 Exemplos de Uso

### JavaScript/AJAX

```javascript
// Buscar situação atual
fetch('/api/situacao-atual/')
  .then(response => response.json())
  .then(data => {
    console.log('Situação atual:', data);
  });

// Criar cadastro
fetch('/api/cadastros/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken()
  },
  body: JSON.stringify({
    nome: 'João Silva',
    email: 'joao@email.com',
    telefone: '51999887766',
    regiao: 1
  })
})
.then(response => response.json())
.then(data => {
  console.log('Cadastro criado:', data);
});

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/alagamentos/');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  if (data.type === 'status_update') {
    updateMap(data.data);
  }
};

// Solicitar atualização
ws.send(JSON.stringify({
  type: 'request_update'
}));
```

### Python/Requests

```python
import requests

# Buscar regiões
response = requests.get('http://localhost:8000/api/regioes/')
regioes = response.json()

# Executar simulação
response = requests.post(
    'http://localhost:8000/api/simulacao/executar/',
    headers={'X-CSRFToken': 'token'}
)
resultado = response.json()

# WebSocket com websockets
import asyncio
import websockets
import json

async def listen_updates():
    uri = "ws://localhost:8000/ws/alagamentos/"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            data = json.loads(message)
            print(f"Atualização: {data}")

asyncio.run(listen_updates())
```

### cURL

```bash
# Buscar dashboard
curl http://localhost:8000/api/dashboard/

# Criar cadastro
curl -X POST http://localhost:8000/api/cadastros/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: token" \
  -d '{"nome":"João Silva","email":"joao@email.com","telefone":"51999887766","regiao":1}'

# Executar simulação
curl -X POST http://localhost:8000/api/simulacao/executar/ \
  -H "X-CSRFToken: token"

# Histórico com filtros
curl "http://localhost:8000/api/historico-alertas/?dias=7&regiao=1"
```

---

## 📋 Rate Limiting

Para uso acadêmico, não há rate limiting implementado. Em produção, recomenda-se:

- **APIs GET:** 100 requests/minuto
- **APIs POST:** 20 requests/minuto
- **WebSocket:** 1 conexão por IP

---

## 🔄 Versionamento

Atualmente na versão **v1.0**. Futuras versões manterão compatibilidade:

- `v1.x` - Atualizações compatíveis
- `v2.x` - Mudanças que quebram compatibilidade

---

**API Documentation v1.0**  
*Sistema de Monitoramento de Alagamentos - Porto Alegre*