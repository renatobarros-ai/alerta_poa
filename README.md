# Sistema de Monitoramento de Alagamentos - Porto Alegre

Sistema acadêmico de monitoramento em tempo real de alagamentos na cidade de Porto Alegre, integrando dados simulados de sensores meteorológicos com análise de imagens por inteligência artificial para identificar pessoas em situação de risco.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [API](#api)
- [Desenvolvimento](#desenvolvimento)
- [Testes](#testes)
- [Deploy](#deploy)
- [Contribuição](#contribuição)

## 🎯 Visão Geral

Este sistema simula o monitoramento em tempo real de alagamentos nas 16 regiões administrativas de Porto Alegre, utilizando:

- **Sensores simulados** para medir nível de água e volume de chuva
- **CNN (Rede Neural Convolucional)** para detecção de pessoas em risco
- **Sistema de alertas** em 3 níveis: Normal (Verde), Alerta (Amarelo), Crítico (Vermelho)
- **Interface web** com mapa interativo
- **Notificações automáticas** via email e WhatsApp
- **Atualizações em tempo real** via WebSocket

## ⚡ Funcionalidades

### Core Features
- 🗺️ **Mapa Interativo**: Visualização das 16 regiões de POA com status em tempo real
- 🤖 **IA para Detecção**: CNN que identifica pessoas em situação de risco
- 📊 **Dashboard**: Estatísticas em tempo real com contadores por status
- 🚨 **Sistema de Alertas**: 3 níveis de alerta com lógica inteligente
- 📱 **Notificações**: Email e WhatsApp automáticos para usuários cadastrados
- ⚡ **Tempo Real**: WebSocket para atualizações instantâneas
- 📈 **Histórico**: Relatórios com filtros e exportação

### Funcionalidades Específicas
- **Simulação de Dados**: Gera dados realísticos a cada 30 segundos
- **Ativação Condicional da CNN**: Só processa quando água/chuva ≥ nível 2
- **Cadastro de Usuários**: Interface para registro de interessados por região
- **APIs REST**: Endpoints completos para integração
- **Admin Interface**: Painel administrativo Django

## 🏗️ Arquitetura

### Stack Tecnológico

**Backend:**
- **Django 5.2+** - Framework web principal
- **Django REST Framework** - APIs REST
- **Django Channels** - WebSocket para tempo real
- **PyTorch** - CNN para detecção de pessoas
- **MariaDB/MySQL** - Banco de dados principal

**Frontend:**
- **Bootstrap 5** - Framework CSS responsivo
- **Leaflet.js** - Mapa interativo
- **Chart.js** - Gráficos e visualizações
- **JavaScript ES6+** - Lógica do frontend
- **WebSocket API** - Comunicação tempo real

### Estrutura do Projeto

```
alagamentos_poa/
├── alagamentos_poa/           # Configurações Django
│   ├── settings.py           # Configurações principais
│   ├── urls.py              # URLs principais
│   ├── asgi.py              # Configuração WebSocket
│   └── wsgi.py              # Configuração WSGI
├── core/                      # App principal
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views web
│   ├── admin.py             # Admin interface
│   ├── routing.py           # WebSocket routing
│   ├── consumers.py         # WebSocket consumers
│   └── management/commands/ # Comandos customizados
├── api/                       # App APIs REST
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   └── urls.py              # URLs da API
├── ia/                        # App CNN/IA
│   ├── detector.py          # Detector de pessoas
│   ├── models/              # Modelos PyTorch
│   │   └── detector.pth     # Modelo treinado
│   └── utils.py             # Funções auxiliares
├── simulator/                 # App simulação
│   ├── generator.py         # Gerador de dados
│   └── management/commands/ # Comandos de simulação
├── notifications/             # App notificações
│   ├── email.py             # Sistema de email
│   └── whatsapp.py          # API WhatsApp
├── static/                    # Arquivos estáticos
│   ├── css/                 # Estilos customizados
│   ├── js/                  # JavaScript
│   └── data/                # Dados GeoJSON
├── templates/                 # Templates HTML
│   ├── base.html            # Template base
│   ├── dashboard.html       # Dashboard principal
│   ├── historico.html       # Histórico
│   └── cadastro.html        # Cadastro usuários
└── requirements.txt           # Dependências Python
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- MariaDB/MySQL 8.0+
- Git

### 1. Clone o Repositório

```bash
git clone <seu-repositorio>
cd sistema
```

### 2. Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Banco de Dados

**Opção A: Usar script SQL fornecido**
```bash
# Execute o script SQL no MariaDB
mysql -u usuario -p < doc_dev/script_sql.txt
```

**Opção B: Criar banco vazio**
```bash
# Crie um banco chamado 'alagamentos_poa'
mysql -u usuario -p -e "CREATE DATABASE alagamentos_poa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## ⚙️ Configuração

### 1. Arquivo .env

Crie/edite o arquivo `.env` na raiz do projeto:

```env
# Django Settings
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Database (MariaDB/MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=alagamentos_poa
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app
DEFAULT_FROM_EMAIL=noreply@alagamentos-poa.com

# WhatsApp Business API (opcional)
WHATSAPP_TOKEN=seu_token_whatsapp
WHATSAPP_PHONE_ID=seu_phone_id
```

### 2. Migrações Django

**Se usou o script SQL:**
```bash
python manage.py migrate --fake-initial
```

**Se criou banco vazio:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Dados Iniciais

```bash
# Popula tabelas obrigatórias
python manage.py populate_initial_data

# Criar superusuário
python manage.py createsuperuser
```

### 4. Arquivos Estáticos

```bash
python manage.py collectstatic
```

## 🎮 Uso

### 1. Iniciar o Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

### 2. Acessar o Sistema

- **Dashboard:** http://localhost:8000/
- **Cadastro:** http://localhost:8000/cadastro/
- **Histórico:** http://localhost:8000/historico/
- **Admin:** http://localhost:8000/admin/

### 3. Executar Simulação

**Terminal separado:**

```bash
# Simulação única (5 rodadas)
python manage.py simulate_data --rounds 5

# Simulação contínua (recomendado)
python manage.py simulate_data --continuous --interval 15

# Com mais opções
python manage.py simulate_data --continuous --interval 30 --rounds 100
```

### 4. Fluxo de Uso

1. **Acesse o Dashboard** para ver o mapa de Porto Alegre
2. **Execute a simulação** para gerar dados
3. **Observe as mudanças** nas cores das regiões
4. **Cadastre usuários** na página de cadastro
5. **Veja o histórico** de alertas gerados
6. **Use o admin** para gerenciar dados

## 🔌 API

### Endpoints Principais

```bash
# Listar regiões
GET /api/regioes/

# Situação atual de todas as regiões
GET /api/situacao-atual/

# Estatísticas do dashboard
GET /api/dashboard/

# Histórico de alertas
GET /api/historico-alertas/?dias=7&regiao=1

# Gerenciar cadastros
GET/POST /api/cadastros/
GET/PUT/DELETE /api/cadastros/{id}/

# Executar simulação
POST /api/simulacao/executar/

# Medições recentes
GET /api/medicoes/?regiao=1

# Análises de risco
GET /api/riscos/?risco=true
```

### WebSocket

```javascript
// Conectar ao WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/alagamentos/');

// Mensagens recebidas
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'status_update':
            // Atualizar mapa com novos dados
            break;
        case 'region_alert':
            // Mostrar alerta específico
            break;
        case 'system_notification':
            // Notificação do sistema
            break;
    }
};

// Solicitar atualização
ws.send(JSON.stringify({
    type: 'request_update'
}));
```

## 🛠️ Desenvolvimento

### Comandos Úteis

```bash
# Executar testes
python manage.py test

# Verificar modelos
python manage.py check

# Shell Django
python manage.py shell

# Ver migrações
python manage.py showmigrations

# Resetar simulação
python manage.py populate_initial_data --force

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

### Estrutura da CNN

O modelo de detecção de pessoas está em `ia/detector.py`:

```python
from ia.detector import get_detector, detect_people_in_region

# Usar o detector
detector = get_detector()
result = detector.detect_people(image_path="path/to/image.jpg")

# Ou usar a função simplificada
result = detect_people_in_region(region_id=1, simulate=True)
```

### Lógica de Alertas

```python
# Status baseado em:
# Normal (0): água=1 E chuva=1
# Alerta (1): (água>=2 OU chuva>=2) E pessoas=False
# Crítico (2): (água>=2 OU chuva>=2) E pessoas=True

def calculate_alert_status(nivel_agua, volume_chuva, pessoas_detectadas):
    if nivel_agua == 1 and volume_chuva == 1:
        return 0  # Normal
    elif nivel_agua >= 2 or volume_chuva >= 2:
        return 2 if pessoas_detectadas else 1  # Crítico ou Alerta
    return 0
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test core.tests
python manage.py test api.tests
python manage.py test simulator.tests
```

### Teste Manual

1. **Teste de Simulação:**
   ```bash
   python manage.py simulate_data --rounds 1
   ```

2. **Teste de API:**
   ```bash
   curl http://localhost:8000/api/dashboard/
   ```

3. **Teste de WebSocket:**
   - Abra o dashboard
   - Execute simulação
   - Observe atualizações automáticas

## 🚀 Deploy

### Configuração de Produção

1. **Configurar .env para produção:**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
   SECRET_KEY=chave-secreta-forte
   ```

2. **Configurar banco de dados:**
   ```env
   DB_HOST=seu-servidor-db
   DB_USER=usuario-producao
   DB_PASSWORD=senha-forte
   ```

3. **Configurar servidor web:**
   - Nginx + Gunicorn (recomendado)
   - Apache + mod_wsgi
   - Docker (ver Dockerfile de exemplo)

### Exemplo com Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn alagamentos_poa.wsgi:application --bind 0.0.0.0:8000
```

### Variáveis de Ambiente Importantes

```env
# Produção
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Segurança
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Email real
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=seu-email-real
EMAIL_HOST_PASSWORD=senha-app-gmail

# WhatsApp real
WHATSAPP_TOKEN=token-real-do-whatsapp-business
WHATSAPP_PHONE_ID=phone-id-real
```

## 🤝 Contribuição

### Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch:** `git checkout -b feature/nova-funcionalidade`
3. **Commit suas mudanças:** `git commit -m 'Adiciona nova funcionalidade'`
4. **Push para a branch:** `git push origin feature/nova-funcionalidade`
5. **Abra um Pull Request**

### Padrões de Código

- **Python:** Siga PEP 8
- **JavaScript:** ES6+ com comentários
- **CSS:** Organize por componentes
- **Commits:** Mensagens claras e descritivas

### Estrutura de Branch

- `main` - Branch principal (produção)
- `develop` - Branch de desenvolvimento
- `feature/*` - Novas funcionalidades
- `bugfix/*` - Correções de bugs
- `hotfix/*` - Correções urgentes

## 📄 Licença

Este projeto é acadêmico e foi desenvolvido para fins educacionais.

## 📞 Contato

Para dúvidas ou sugestões sobre este sistema acadêmico:

- **Documentação:** Veja os arquivos em `doc_dev/`
- **Issues:** Use o sistema de issues do repositório
- **Email:** [Seu email de contato]

---

## 📚 Documentação Técnica Adicional

### Banco de Dados

O sistema utiliza 8 tabelas principais:

1. **regiao** - 16 regiões administrativas de POA
2. **nivel_agua** - 3 níveis (Normal, Alerta, Crítico)
3. **volume_chuva** - 3 volumes (Baixa, Moderada, Intensa)
4. **status** - 3 status de alerta (Verde, Amarelo, Vermelho)
5. **medicao** - Dados dos sensores por região
6. **risco_humano** - Análises da CNN
7. **cadastro** - Usuários cadastrados
8. **envio_alerta** - Histórico de notificações

### Performance

- **CNN:** Processa apenas quando necessário (água/chuva ≥ 2)
- **WebSocket:** Conexões otimizadas com reconexão automática
- **Cache:** Uso de cache para dados estáticos
- **Índices:** Banco otimizado com índices nas consultas principais

### Segurança

- **CSRF Protection:** Todos os formulários protegidos
- **SQL Injection:** Uso de ORM Django
- **XSS Protection:** Templates escapados automaticamente
- **Autenticação:** Sistema Django padrão para admin

---

**Sistema de Monitoramento de Alagamentos - Porto Alegre v1.0**  
*Projeto Acadêmico - 2025*