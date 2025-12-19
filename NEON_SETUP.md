# Deploy com Neon.tech - PostgreSQL Serverless

## 🚀 Por que Neon.tech?

- ✅ PostgreSQL serverless **gratuito**
- ✅ 10 GB de storage no plano free
- ✅ Mais rápido que SQLite
- ✅ Funciona perfeitamente com Vercel e Render
- ✅ Backups automáticos
- ✅ Escalável

## Passo a Passo

### 1. Criar conta e projeto no Neon

1. Acesse [neon.tech](https://neon.tech)
2. Clique em **Sign up** (pode usar conta GitHub)
3. Clique em **Create a project**
4. Configure:
   - **Project name**: `cardapio-db`
   - **Region**: escolha o mais próximo (US East recomendado)
   - **PostgreSQL version**: 16 (mais recente)
5. Clique em **Create project**

### 2. Copiar a Connection String

Após criar o projeto, você verá a **Connection String**:

```
postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Copie essa URL completa!**

### 3. Configurar no Vercel

1. Vá ao dashboard do Vercel
2. Selecione seu projeto CardapioAPI
3. Vá em **Settings** → **Environment Variables**
4. Adicione:
   ```
   DATABASE_URL=postgresql://user:password@ep-xxx...neon.tech/neondb?sslmode=require
   ```
5. Clique em **Save**
6. Faça **Redeploy**

### 4. Configurar no Render (se usar)

1. Dashboard do Render → seu serviço
2. **Environment**
3. Edite `DATABASE_URL` e cole a Connection String do Neon
4. Salve (redeploy automático)

### 5. Testar localmente

Adicione ao seu arquivo `.env` (crie se não existir):

```env
DATABASE_URL=postgresql://user:password@ep-xxx...neon.tech/neondb?sslmode=require
DJANGO_SECRET_KEY=sua-chave-local
DEBUG=True
```

Execute:
```bash
cd cardapioAPIProject
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configurações já preparadas ✅

Seu projeto já está configurado para usar Neon! O `settings.py` detecta automaticamente a variável `DATABASE_URL`:

```python
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
```

## Gerenciar o Banco de Dados

### Via Neon Console

1. Acesse [console.neon.tech](https://console.neon.tech)
2. Selecione seu projeto
3. Aba **Tables** - visualize suas tabelas
4. Aba **SQL Editor** - execute queries

### Via pgAdmin ou DBeaver

Use a **Connection String** para conectar qualquer ferramenta PostgreSQL.

### Via Terminal

```bash
psql "postgresql://user:password@ep-xxx...neon.tech/neondb?sslmode=require"
```

## Migrations

As migrations são executadas automaticamente no deploy (tanto Vercel quanto Render).

Para executar manualmente:
```bash
cd cardapioAPIProject
python manage.py migrate
```

## Criar Superusuário no Neon

### Opção 1: Automaticamente (já configurado)

O `build_render.sh` e `index.py` já criam o superusuário automaticamente usando:
- Username: valor de `ADMIN_USERNAME` (padrão: `admin`)
- Password: valor de `ADMIN_PASSWORD` (padrão: `admin123`)

### Opção 2: Manualmente

```bash
# Local
cd cardapioAPIProject
python manage.py createsuperuser

# Vercel (via Python snippet no index.py)
# Render (via Shell no dashboard)
```

## Backups

O Neon faz backups automáticos no plano free com:
- **Point-in-time restore**: últimos 7 dias
- **Branch**: crie branches do banco para teste

### Fazer backup manual:

```bash
pg_dump "postgresql://user:password@ep-xxx...neon.tech/neondb?sslmode=require" > backup.sql
```

### Restaurar:

```bash
psql "postgresql://user:password@ep-xxx...neon.tech/neondb?sslmode=require" < backup.sql
```

## Monitoramento

No [console.neon.tech](https://console.neon.tech):
- **Monitoring**: CPU, memória, conexões
- **Usage**: storage usado
- **Branches**: gerenciar branches do banco

## Limites do Plano Free

- ✅ 10 GB de storage
- ✅ 100 horas de compute por mês
- ✅ Autosuspend após inatividade (economiza recursos)
- ✅ 1 projeto ativo

## Vantagens sobre SQLite

| Feature | SQLite (Vercel) | Neon PostgreSQL |
|---------|----------------|-----------------|
| Persistência | ❌ Volátil | ✅ Permanente |
| Concurrent writes | ⚠️ Limitado | ✅ Excelente |
| Backups | ❌ Manual | ✅ Automático |
| Escalabilidade | ❌ Não | ✅ Sim |
| Produção | ❌ Não recomendado | ✅ Production-ready |

## Troubleshooting

### Erro de conexão

**Problema**: `could not connect to server`

**Solução**:
- Verifique se a Connection String está correta
- Certifique-se que inclui `?sslmode=require`
- Verifique se o projeto Neon não foi suspenso

### Migrations não aplicadas

**Problema**: Tabelas não existem

**Solução**:
```bash
python manage.py migrate --run-syncdb
```

### Too many connections

**Problema**: `FATAL: remaining connection slots reserved`

**Solução**: O Neon tem limite de conexões. Use `conn_max_age` (já configurado) para reusar conexões.

## Próximos Passos

1. ✅ Criar projeto no Neon
2. ✅ Copiar Connection String
3. ✅ Configurar `DATABASE_URL` no Vercel/Render
4. ✅ Fazer redeploy
5. ✅ Acessar `/admin` e fazer login
6. ✅ Testar API em `/api/items/`

Seu projeto agora tem um banco de dados PostgreSQL de produção! 🎉
