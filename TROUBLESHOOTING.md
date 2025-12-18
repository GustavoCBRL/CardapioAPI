# Troubleshooting - Erro 500 no Vercel

## Correções Aplicadas

### 1. ✅ DEBUG Habilitado Temporariamente
- Agora você verá a mensagem de erro completa no navegador
- Ajuda a identificar o problema exato

### 2. ✅ Banco de Dados Configurado para /tmp
- Vercel não permite escrita fora de /tmp
- O banco SQLite agora usa `/tmp/db.sqlite3`
- **IMPORTANTE**: Os dados são perdidos a cada deploy (natureza serverless)

### 3. ✅ Migrations Automáticas
- O `index.py` executa migrations automaticamente
- Cria as tabelas necessárias no /tmp a cada inicialização

## Próximos Passos para Resolver o Erro 500

### Verifique os Logs no Vercel

1. Acesse o dashboard do Vercel
2. Vá em **Deployments** → Último deploy
3. Clique em **Runtime Logs**
4. Procure pela mensagem de erro detalhada

### Problemas Comuns e Soluções

#### 1. Variável de Ambiente Faltando
**Erro**: `SECRET_KEY not set`

**Solução**: No Vercel, adicione:
```
DJANGO_SECRET_KEY=gere-uma-chave-secreta-forte-aqui
```

Gere uma chave:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 2. Imports Falhando
**Erro**: `ModuleNotFoundError: No module named 'cardapio'`

**Solução**: Já corrigido no `index.py` com ajustes no `sys.path`

#### 3. Static Files
**Erro relacionado a arquivos estáticos**

**Solução**: 
- Desabilite `STATICFILES_STORAGE` temporariamente
- Ou colete static files no build

#### 4. ALLOWED_HOSTS
**Erro**: `Invalid HTTP_HOST header`

**Solução**: Já configurado com `ALLOWED_HOSTS = ['*']`

## Comandos Úteis para Teste Local

### Testar localmente com configurações do Vercel:
```bash
export VERCEL=1
export DEBUG=True
cd cardapioAPIProject
python manage.py migrate
python manage.py runserver
```

### Testar o index.py:
```bash
export VERCEL=1
python -c "import index; print('OK')"
```

## Recomendações para Produção

### 1. Use PostgreSQL em vez de SQLite
**Por quê**: SQLite no Vercel é volátil (dados são perdidos)

**Opções gratuitas**:
- [Supabase](https://supabase.com) - PostgreSQL grátis
- [Neon](https://neon.tech) - PostgreSQL serverless
- [Railway](https://railway.app) - PostgreSQL + deploy

**Como configurar**:
1. Adicione ao `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   dj-database-url==2.1.0
   ```

2. Atualize `settings.py`:
   ```python
   import dj_database_url
   
   if os.environ.get('DATABASE_URL'):
       DATABASES = {
           'default': dj_database_url.config(
               conn_max_age=600,
               conn_health_checks=True,
           )
       }
   ```

3. Adicione no Vercel:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/db
   ```

### 2. Desabilite DEBUG em Produção
Após identificar o erro, configure:
```
DEBUG=False
```

### 3. Configure CORS Corretamente
```
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

## Se o Erro Persistir

### 1. Verifique o Runtime Log no Vercel
- Procure por stack traces completas
- Identifique a linha exata do erro

### 2. Teste com curl
```bash
curl -v https://seu-projeto.vercel.app/api/items/
```

### 3. Verifique as Dependências
Certifique-se que o `requirements.txt` tem todas as libs:
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
```

### 4. Force Redeploy
No dashboard do Vercel:
- Vá em **Deployments**
- Clique nos 3 pontos do último deploy
- Selecione **Redeploy**

## Contato para Suporte

Se o erro persistir, copie e cole:
1. O erro completo dos Runtime Logs
2. A URL do projeto no Vercel
3. As variáveis de ambiente configuradas (sem valores sensíveis)
