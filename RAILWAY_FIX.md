# 🚂 Railway - Como Forçar Rebuild Limpo

## Problema
Railway está usando cache antigo e ainda tentando instalar `mysqlclient` que não existe mais no `requirements.txt`.

## ✅ Solução Rápida (Dashboard Railway)

### Opção 1: Limpar Cache pelo Dashboard
1. Acesse seu projeto no [Railway Dashboard](https://railway.app/)
2. Clique no seu serviço (CardapioAPI)
3. Vá em **Settings** (Configurações)
4. Role até encontrar **"Danger Zone"**
5. Clique em **"Clear Build Cache"** ou **"Redeploy"**
6. Confirme a ação

### Opção 2: Trigger Manual
1. No Railway Dashboard, vá até a aba **Deployments**
2. Clique nos 3 pontinhos (...) do último deploy
3. Selecione **"Redeploy"**
4. Aguarde o novo build

### Opção 3: Criar Deploy Vazio (mais garantido)
```bash
git commit --allow-empty -m "Force Railway clean rebuild"
git push origin main
```

## 🔍 Verificar se Funcionou

Depois do deploy, acesse no Railway Dashboard:
- **Build Logs**: Verifique se `mysqlclient` não aparece mais
- **Deploy Logs**: Deve ver apenas os pacotes corretos sendo instalados

## 📋 Configuração Atual (Correta)

### requirements.txt ✅
```
asgiref==3.10.0
Django==5.2.7
django-cors-headers==4.9.0
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
Markdown==3.10
PyJWT==2.10.1
sqlparse==0.5.3
whitenoise==6.7.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### Procfile ✅
```
web: cd cardapioAPIProject && python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT cardapioAPI.wsgi:application
```

### railway.json ✅
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "healthcheckPath": "/health/",
    "healthcheckTimeout": 300
  }
}
```

### nixpacks.toml ✅
```toml
[phases.setup]
nixPkgs = ['python312', 'postgresql']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = ['python cardapioAPIProject/manage.py collectstatic --noinput']
```

## 🔧 Variáveis de Ambiente Necessárias

No Railway Dashboard > Settings > Variables:

```bash
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui-min-50-caracteres
DEBUG=False

# Database (Railway provisiona automaticamente)
DATABASE_URL=postgresql://... (gerado automaticamente pelo Railway)

# Hosts
ALLOWED_HOSTS=.up.railway.app,.vercel.app

# CORS
CORS_ALLOWED_ORIGINS=https://restaurante-chi-two.vercel.app
```

## 🎯 Próximos Passos

1. **Adicionar PostgreSQL** (se ainda não tiver):
   - No Railway Dashboard, clique em **"+ New"**
   - Selecione **"Database" > "PostgreSQL"**
   - Railway automaticamente cria a variável `DATABASE_URL`

2. **Verificar Health Check**:
   ```bash
   curl https://seu-projeto.up.railway.app/health/
   ```
   Deve retornar: `{"status": "healthy"}`

3. **Testar API**:
   ```bash
   curl https://seu-projeto.up.railway.app/api/items/
   ```

4. **Acessar Admin**:
   ```
   https://seu-projeto.up.railway.app/admin/
   ```

## 🐛 Troubleshooting

### Ainda aparece mysqlclient nos logs?
1. Delete completamente o serviço no Railway
2. Crie um novo serviço conectando ao mesmo repositório GitHub
3. Railway vai fazer build do zero

### Health check falha?
- Verifique se o endpoint `/health/` existe em `cardapioAPI/urls.py`
- Teste localmente: `python manage.py runserver` e acesse `http://localhost:8000/health/`

### Migrations não rodam?
- Railway executa automaticamente via Procfile
- Verifique os logs de deploy para ver se há erros de banco de dados

### Porta incorreta?
- Railway define automaticamente a variável `$PORT`
- O Procfile já usa: `--bind 0.0.0.0:$PORT`

## 📚 Documentação

- [Railway Docs](https://docs.railway.app/)
- [Nixpacks Python](https://nixpacks.com/docs/providers/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
