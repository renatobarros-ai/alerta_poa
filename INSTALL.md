# 🚀 Guia de Instalação Rápida

## Sistema de Monitoramento de Alagamentos - Porto Alegre

Este guia fornece instruções passo a passo para instalar e executar o sistema.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter:

- ✅ **Python 3.11+** instalado
- ✅ **MariaDB/MySQL 8.0+** instalado e rodando
- ✅ **Git** instalado
- ✅ **pip** atualizado

---

## ⚡ Instalação Rápida (5 minutos)

### 1. Clone e Configure o Ambiente

```bash
# Clone o repositório
git clone <seu-repositorio>
cd sistema

# Crie ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure o Banco de Dados

**Opção A: Usar script SQL pronto (Recomendado)**
```bash
# Execute o script no MariaDB
mysql -u root -p < doc_dev/script_sql.txt
```

**Opção B: Criar banco manualmente**
```bash
mysql -u root -p -e "CREATE DATABASE alagamentos_poa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Configure as Variáveis de Ambiente

Edite o arquivo `.env` com suas credenciais:

```env
# Substitua pelos seus dados
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql

# Mantenha o resto como está para teste
DB_ENGINE=django.db.backends.mysql
DB_NAME=alagamentos_poa
DB_HOST=localhost
DB_PORT=3306
```

### 4. Configure o Django

```bash
# Se usou o script SQL
python manage.py migrate --fake-initial

# Se criou banco vazio
python manage.py makemigrations
python manage.py migrate

# Popule dados iniciais
python manage.py populate_initial_data

# Crie superusuário
python manage.py createsuperuser
```

### 5. Execute o Sistema

```bash
# Terminal 1 - Servidor Django
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Simulação (em paralelo)
python manage.py simulate_data --continuous --interval 15
```

### 6. Acesse o Sistema

Abra seu navegador e acesse:

- 🏠 **Dashboard:** http://localhost:8000/
- 👥 **Cadastro:** http://localhost:8000/cadastro/
- 📊 **Histórico:** http://localhost:8000/historico/
- ⚙️ **Admin:** http://localhost:8000/admin/

---

## 🔧 Resolução de Problemas Comuns

### Erro: "That port is already in use"

```bash
# Encontre o processo usando a porta
ps aux | grep runserver

# Mate o processo (substitua XXXX pelo PID)
kill XXXX

# Ou use outra porta
python manage.py runserver 8001
```

### Erro: "Table already exists"

```bash
# Marque migrações como aplicadas
python manage.py migrate --fake-initial
```

### Erro: "No module named 'MySQLdb'"

```bash
# Instale o driver MySQL
pip install PyMySQL

# Ou reinstale requirements
pip install -r requirements.txt
```

### Erro: "Access denied for user"

Verifique suas credenciais no arquivo `.env`:
```env
DB_USER=seu_usuario_correto
DB_PASSWORD=sua_senha_correta
```

### Erro: "static files not found"

```bash
# Colete arquivos estáticos
python manage.py collectstatic --noinput
```

---

## 🎯 Verificação da Instalação

### 1. Teste o Sistema

```bash
# Execute uma simulação de teste
python manage.py simulate_data --rounds 3
```

### 2. Verifique as URLs

- ✅ Dashboard carregando com mapa
- ✅ Cadastro funcionando
- ✅ Histórico exibindo dados
- ✅ Admin acessível

### 3. Teste o WebSocket

1. Abra o dashboard
2. Execute simulação em outro terminal
3. Observe as mudanças automáticas no mapa

---

## 📝 Configurações Opcionais

### Email (Para notificações reais)

```env
# Gmail (recomendado)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=senha_de_aplicativo
DEFAULT_FROM_EMAIL=noreply@alagamentos-poa.com
```

### WhatsApp Business API

```env
WHATSAPP_TOKEN=seu_token_aqui
WHATSAPP_PHONE_ID=seu_phone_id_aqui
```

---

## 🐳 Instalação com Docker (Alternativa)

Se preferir usar Docker:

```bash
# Build da imagem
docker build -t alagamentos-poa .

# Execute com docker-compose
docker-compose up -d
```

---

## 💡 Dicas de Uso

### Para Desenvolvimento

```bash
# Monitore logs em tempo real
python manage.py runserver --verbosity=2

# Execute com debug ativo
DEBUG=True python manage.py runserver

# Limpe dados e recomece
python manage.py flush
python manage.py populate_initial_data
```

### Para Demonstração

```bash
# Simulação mais visual (intervalos menores)
python manage.py simulate_data --continuous --interval 5

# Mais regiões em alerta
python manage.py simulate_data --continuous --interval 10
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Consulte a documentação completa:** `README.md`
2. **Verifique logs de erro** nos terminais
3. **Teste com dados limpos:** `python manage.py flush`
4. **Reinstale dependências:** `pip install -r requirements.txt --force-reinstall`

---

## ✅ Checklist de Instalação

- [ ] Python 3.11+ instalado
- [ ] MariaDB/MySQL rodando
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Arquivo .env configurado
- [ ] Migrações executadas
- [ ] Dados iniciais populados
- [ ] Superusuário criado
- [ ] Servidor Django funcionando
- [ ] Simulação executando
- [ ] Dashboard acessível

**🎉 Se todos os itens estão marcados, sua instalação foi bem-sucedida!**

---

**Sistema de Monitoramento de Alagamentos - Porto Alegre**  
*Guia de Instalação v1.0*