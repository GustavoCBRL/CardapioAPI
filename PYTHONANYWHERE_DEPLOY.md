# Deploy no PythonAnywhere - Guia Completo

## 🚀 Por que PythonAnywhere?

- ✅ **Grátis** com domínio personalizado
- ✅ PostgreSQL/MySQL **incluído** (persistente)
- ✅ Perfeito para Django
- ✅ Sem problemas de psycopg2
- ✅ Console e bash integrados
- ✅ Fácil de configurar

## Passo a Passo

### 1. Criar Conta

1. Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
2. Clique em **Pricing & signup**
3. Escolha **Create a Beginner account** (grátis)
4. Preencha o formulário e crie sua conta

### 2. Clonar o Repositório

1. No dashboard, clique em **Consoles** → **Bash**
2. Execute:

```bash
git clone https://github.com/GustavoCBRL/CardapioAPI.git
cd CardapioAPI
```

### 3. Criar Ambiente Virtual

```bash
mkvirtualenv --python=/usr/bin/python3.10 cardapio-env
workon cardapio-env
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie o arquivo `.env`:

```bash
cd ~/CardapioAPI
nano .env
```

Cole:
```
DJANGO_SECRET_KEY=gere-uma-chave-segura-aqui
DEBUG=False
DATABASE_URL=postgresql://neondb_owner:npg_t8ojG1lbsqkO@ep-raspy-king-adiyprq4-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=sua-senha-aqui
```

Salve: `Ctrl+X` → `Y` → `Enter`

**Ou use o MySQL do PythonAnywhere (recomendado):**

1. No dashboard, vá em **Databases**
2. Configure uma senha para MySQL
3. Anote: `username_databasename`
4. No `.env`:
```
DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere-services.com/username$cardapio
```

### 5. Executar Migrations

```bash
cd ~/CardapioAPI/cardapioAPIProject
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

### 6. Configurar Web App

1. No dashboard, clique em **Web**
2. Clique em **Add a new web app**
3. Escolha **Manual configuration**
4. Selecione **Python 3.10**

#### 6.1 Configurar Code Section

- **Source code**: `/home/seuusername/CardapioAPI/cardapioAPIProject`
- **Working directory**: `/home/seuusername/CardapioAPI/cardapioAPIProject`

#### 6.2 Configurar Virtualenv

- **Virtualenv**: `/home/seuusername/.virtualenvs/cardapio-env`

#### 6.3 Configurar WSGI

Clique no link do arquivo WSGI e substitua todo o conteúdo por:

```python
import os
import sys

# Adicionar projeto ao path
path = '/home/seuusername/CardapioAPI/cardapioAPIProject'
if path not in sys.path:
    sys.path.insert(0, path)

# Carregar variáveis de ambiente do .env
from pathlib import Path
env_file = Path('/home/seuusername/CardapioAPI/.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardapioAPI.settings')

# Carregar aplicação Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Substitua `seuusername` pelo seu username do PythonAnywhere!**

#### 6.4 Configurar Static Files

Na seção **Static files**, adicione:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/seuusername/CardapioAPI/cardapioAPIProject/staticfiles` |

### 7. Reload Web App

1. Volte para o topo da página **Web**
2. Clique no botão verde **Reload yourusername.pythonanywhere.com**

## Acessar a API

Sua API estará em:
```
https://seuusername.pythonanywhere.com/api/items/
https://seuusername.pythonanywhere.com/admin/
```

## Configurar CORS

O CORS já está configurado no `settings.py`. Adicione o domínio do PythonAnywhere:

```bash
cd ~/CardapioAPI/cardapioAPIProject/cardapioAPI
nano settings.py
```

Atualize:
```python
CORS_ALLOWED_ORIGINS = [
    'https://restaurante-chi-two.vercel.app',
    'https://seuusername.pythonanywhere.com',
    'http://localhost:3000',
]
```

Depois:
```bash
cd ~/CardapioAPI
git add .
git commit -m "Add PythonAnywhere domain to CORS"
git push
```

E faça **Reload** no Web App.

## Atualizar o Código

Quando fizer mudanças no GitHub:

```bash
cd ~/CardapioAPI
git pull
cd cardapioAPIProject
python manage.py migrate
python manage.py collectstatic --no-input
```

Depois clique em **Reload** no Web App.

## Banco de Dados

### Opção 1: Neon PostgreSQL (Atual)

Já está configurado com a `DATABASE_URL` do Neon no `.env`.

### Opção 2: MySQL do PythonAnywhere (Recomendado)

1. Dashboard → **Databases**
2. Configure senha do MySQL
3. Clique em **Initialize database**
4. Anote: `username_databasename`

Atualize o `.env`:
```
DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere-services.com/username$cardapio
```

Adicione ao `requirements.txt`:
```
mysqlclient==2.2.0
```

Execute:
```bash
workon cardapio-env
pip install mysqlclient
cd ~/CardapioAPI/cardapioAPIProject
python manage.py migrate
```

## Logs e Debug

### Ver Logs de Erro

Dashboard → **Web** → **Log files**:
- **Error log**: Erros do servidor
- **Server log**: Requisições HTTP
- **WSGI error log**: Erros do Django

### Bash Console

Para executar comandos Django:
```bash
workon cardapio-env
cd ~/CardapioAPI/cardapioAPIProject
python manage.py shell
```

### Django Shell

```python
from cardapio.models import Item
print(Item.objects.all())
```

## Limites do Plano Grátis

- ✅ 1 web app
- ✅ 512 MB de storage
- ✅ 100 segundos de CPU/dia
- ✅ Acesso SSH/console
- ⚠️ Domínio: `username.pythonanywhere.com`

## Troubleshooting

### ImportError ou ModuleNotFoundError

```bash
workon cardapio-env
cd ~/CardapioAPI
pip install -r requirements.txt
```

### Static files não carregam

```bash
cd ~/CardapioAPI/cardapioAPIProject
python manage.py collectstatic --no-input
```

E verifique se o path em **Static files** está correto.

### Error 500

Verifique:
1. **Error log** na seção Web
2. Variáveis de ambiente no `.env`
3. `DJANGO_SECRET_KEY` configurada
4. Migrations executadas

### CORS Error

Adicione seu domínio frontend em `CORS_ALLOWED_ORIGINS` no `settings.py`.

## Comandos Úteis

```bash
# Ativar ambiente virtual
workon cardapio-env

# Ver ambiente virtual ativo
which python

# Atualizar código
cd ~/CardapioAPI && git pull

# Migrations
cd ~/CardapioAPI/cardapioAPIProject
python manage.py makemigrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Collectstatic
python manage.py collectstatic --no-input

# Shell Django
python manage.py shell
```

## Upgrade para Plano Pago (Opcional)

Se precisar de mais recursos:
- **Hacker ($5/mês)**: 
  - 2 GB storage
  - Domínio personalizado
  - Postgres incluído
  - Sempre online

## Próximos Passos

1. ✅ Criar conta no PythonAnywhere
2. ✅ Clonar repositório
3. ✅ Criar virtualenv e instalar dependências
4. ✅ Configurar `.env`
5. ✅ Executar migrations
6. ✅ Configurar Web App
7. ✅ Testar API
8. 🌐 Conectar com frontend

Seu projeto está pronto para produção no PythonAnywhere! 🎉
