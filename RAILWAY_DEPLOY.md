# Deploy no Railway - Guia Completo

## 🚀 Por que Railway?

- ✅ **$5 de crédito grátis todo mês**
- ✅ PostgreSQL **nativo e automático**
- ✅ Deploy via GitHub (CI/CD automático)
- ✅ Domínio HTTPS gratuito
- ✅ Variáveis de ambiente seguras
- ✅ Logs em tempo real
- ✅ Escalável e rápido

## Passo a Passo

### 1. Preparar o Projeto

O projeto já está configurado! Verifique se tem:

- ✅ `Procfile` → Define como rodar (gunicorn)
- ✅ `requirements.txt` → Dependências Python
- ✅ `settings.py` → Configurado para DATABASE_URL

### 2. Criar Conta no Railway

1. Acesse [railway.app](https://railway.app)
2. Clique em **Login** ou **Start a New Project**
3. Faça login com **GitHub**
4. Autorize o Railway a acessar seus repositórios

### 3. Criar Novo Projeto

1. No dashboard do Railway, clique em **New Project**
2. Escolha **Deploy from GitHub repo**
3. Selecione o repositório: **GustavoCBRL/CardapioAPI**
4. Railway vai detectar automaticamente que é Python/Django

### 4. Adicionar PostgreSQL

1. No seu projeto Railway, clique em **New**
2. Selecione **Database** → **Add PostgreSQL**
3. Railway cria automaticamente um banco PostgreSQL
4. A variável `DATABASE_URL` é configurada automaticamente! ✨

### 5. Configurar Variáveis de Ambiente

1. Clique no serviço **CardapioAPI** (não no PostgreSQL)
2. Vá na aba **Variables**
3. Adicione as seguintes variáveis:

```bash
DJANGO_SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=sua-senha-admin
RAILWAY_ENVIRONMENT=production
```

**Gerar uma SECRET_KEY segura:**
```python
# No terminal local Python:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**Importante:** `DATABASE_URL` já é criada automaticamente pelo Railway quando você adiciona PostgreSQL!

### 6. Configurar Settings

O Railway vai usar estas configurações automaticamente:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `cd cardapioAPIProject && gunicorn cardapioAPI.wsgi:application`

Não precisa alterar nada, o `Procfile` já define isso!

### 7. Deploy Automático

1. Railway vai fazer o **primeiro deploy automaticamente**
2. Acompanhe os logs em tempo real
3. Aguarde até ver: ✅ **Deploy successful**

### 8. Obter a URL do Projeto

1. No dashboard do Railway, clique no serviço **CardapioAPI**
2. Vá na aba **Settings** → **Domains**
3. Clique em **Generate Domain**
4. Copie a URL: `https://seu-projeto.up.railway.app`

### 9. Configurar ALLOWED_HOSTS

1. **Volte ao seu código local** (VS Code)
2. Adicione o domínio Railway ao `settings.py`:

```python
ALLOWED_HOSTS = [
    'seu-projeto.up.railway.app',  # Adicione aqui
    'gustavocbrl.pythonanywhere.com',
    'cardapioapi-xiz8.onrender.com',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
]
```

3. Commit e push:

```bash
git add cardapioAPIProject/cardapioAPI/settings.py
git commit -m "Add Railway domain to ALLOWED_HOSTS"
git push origin main
```

4. **Railway faz redeploy automático!** 🚀

### 10. Executar Migrations

Railway **não roda migrations automaticamente**. Você precisa fazer manualmente:

1. No dashboard Railway, clique no serviço **CardapioAPI**
2. Vá na aba **Deployments**
3. Clique no deployment ativo → **View Logs**
4. No canto superior direito, clique em **⋮** → **Connect to Service**
5. Abre um terminal! Execute:

```bash
cd cardapioAPIProject
python manage.py migrate
python manage.py createsuperuser
```

**OU** adicione no `Procfile` (recomendado):

```
web: cd cardapioAPIProject && python manage.py migrate && gunicorn cardapioAPI.wsgi:application
```

Isso roda migrations automaticamente em cada deploy! ✨

### 11. Configurar CORS

Adicione o domínio Railway ao CORS:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    'https://restaurante-chi-two.vercel.app',  # Frontend
    'https://seu-projeto.up.railway.app',       # Railway
    'http://localhost:3000',
]
```

Commit e push:

```bash
git add cardapioAPIProject/cardapioAPI/settings.py
git commit -m "Add Railway domain to CORS"
git push origin main
```

## Acessar a API

Sua API estará em:

```
https://seu-projeto.up.railway.app/api/items/
https://seu-projeto.up.railway.app/admin/
```

## Logs e Monitoramento

### Ver Logs em Tempo Real

1. Dashboard Railway → Seu serviço
2. Aba **Deployments** → Clique no deploy ativo
3. **View Logs** → Logs em tempo real! 📊

### Métricas

- CPU, RAM, Network
- Tempo de resposta
- Erros e crashes

Tudo disponível no dashboard!

## Banco de Dados PostgreSQL

### Conectar ao PostgreSQL

1. Railway → PostgreSQL service
2. Aba **Connect**
3. Copie as credenciais:

```bash
Host: containers-us-west-xxx.railway.app
Port: 7432
User: postgres
Password: xxxxxxxxxx
Database: railway
```

### Usar DBeaver, pgAdmin, etc.

Use as credenciais acima para conectar com qualquer cliente PostgreSQL!

### Backup do Banco

```bash
# No terminal Railway (Connect to Service):
pg_dump $DATABASE_URL > backup.sql
```

## CI/CD Automático

Railway monitora seu repositório GitHub:

- **Push to main** → Deploy automático
- **Pull Request** → Preview deployment (opcional)
- **Rollback** → Um clique para voltar versões anteriores

## Variáveis de Ambiente Importantes

```bash
# Obrigatórias
DJANGO_SECRET_KEY=sua-chave-segura
DEBUG=False
DATABASE_URL=postgresql://...  # Automático!

# Opcionais
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=sua-senha
RAILWAY_ENVIRONMENT=production
```

## Comandos Úteis

### Conectar ao Terminal Railway

1. Dashboard → Service → Deployments
2. Clique em **⋮** → **Connect to Service**

```bash
# Ver logs Django
cd cardapioAPIProject
python manage.py shell

# Migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Ver itens no banco
python manage.py shell
>>> from cardapio.models import Item
>>> Item.objects.all()
```

## Troubleshooting

### Error 500 - Verificar

1. **Logs**: Dashboard → View Logs
2. **DATABASE_URL**: Deve estar configurada automaticamente
3. **DJANGO_SECRET_KEY**: Precisa estar nas variáveis
4. **ALLOWED_HOSTS**: Adicione `seu-projeto.up.railway.app`
5. **Migrations**: Execute `python manage.py migrate`

### Build Failed

- Verifique `requirements.txt`
- Confirme que Python 3.10+ está instalado
- Veja logs completos no Railway

### CORS Error

- Adicione domínio Railway ao `CORS_ALLOWED_ORIGINS`
- Commit e push para redeploy

### Static Files 404

Railway serve static files via WhiteNoise (já configurado):

```bash
python manage.py collectstatic --no-input
```

## Custos (Plano Hobby)

- **$5 de crédito grátis por mês**
- **$0.000231/GB-hora** (RAM)
- **$0.000463/vCPU-hora** (CPU)

**Estimativa**: Projeto pequeno/médio = $3-5/mês (dentro do crédito grátis!)

## Escalar Aplicação

Railway escala automaticamente, mas você pode configurar:

1. Service → Settings → **Resources**
2. Ajuste **CPU** e **RAM**
3. Habilite **Autoscaling** (planos pagos)

## Custom Domain (Opcional)

1. Service → Settings → **Domains**
2. Clique em **Custom Domain**
3. Adicione seu domínio: `api.seusite.com`
4. Configure DNS:
   - CNAME → seu-projeto.up.railway.app
5. HTTPS automático via Let's Encrypt! 🔒

## Comparação Railway vs Outros

| Feature | Railway | Render | PythonAnywhere |
|---------|---------|--------|----------------|
| PostgreSQL | ✅ Nativo | ✅ Pago | ❌ Pago |
| Deploy GitHub | ✅ Auto | ✅ Auto | ❌ Manual |
| Free Tier | $5/mês | 750h/mês | Limitado |
| Domínio HTTPS | ✅ Grátis | ✅ Grátis | ❌ Pago |
| Escalabilidade | ✅ Fácil | ✅ Fácil | ⚠️ Limitada |

## Atualizar Código

Railway faz deploy automático quando você faz push:

```bash
# Local
git add .
git commit -m "Sua mensagem"
git push origin main

# Railway detecta e faz redeploy automático! 🚀
```

## Rollback

Se algo der errado:

1. Dashboard → Deployments
2. Clique no deploy anterior que funcionava
3. **Redeploy** → Volta para versão anterior! ✨

## Próximos Passos

1. ✅ Criar conta no Railway
2. ✅ Conectar repositório GitHub
3. ✅ Adicionar PostgreSQL
4. ✅ Configurar variáveis de ambiente
5. ✅ Deploy automático
6. ✅ Executar migrations
7. ✅ Testar API
8. 🌐 Conectar com frontend

Seu projeto está rodando no Railway com PostgreSQL persistente! 🎉

## Links Úteis

- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)
