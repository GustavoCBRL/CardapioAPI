# Deploy no Render - Guia Completo

## 🚀 Vantagens do Render

- ✅ PostgreSQL **gratuito** (muito melhor que SQLite)
- ✅ Dados **persistentes** (não são perdidos)
- ✅ Deploy automático do GitHub
- ✅ HTTPS gratuito
- ✅ Mais fácil que Vercel para Django

## Pré-requisitos

- Conta no [Render](https://render.com)
- Projeto no GitHub (já configurado ✅)

## Passo a Passo

### 1. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em **Get Started for Free**
3. Conecte sua conta do GitHub

### 2. Deploy via Blueprint (Recomendado)

#### Opção A: Deploy Automático

1. No dashboard do Render, clique em **New** → **Blueprint**
2. Conecte seu repositório **CardapioAPI**
3. O Render detectará automaticamente o `render.yaml`
4. Clique em **Apply**
5. Aguarde a criação do banco de dados e do serviço web

**Pronto!** Tudo será configurado automaticamente:
- ✅ PostgreSQL criado
- ✅ Variáveis de ambiente configuradas
- ✅ Build executado
- ✅ Migrations aplicadas
- ✅ Superusuário criado

### 3. Deploy Manual (Alternativa)

Se preferir configurar manualmente:

#### 3.1 Criar Banco de Dados PostgreSQL

1. No dashboard, clique em **New** → **PostgreSQL**
2. Preencha:
   - **Name**: `cardapio-db`
   - **Database**: `cardapio`
   - **User**: `cardapio`
   - **Region**: escolha o mais próximo
   - **Plan**: **Free**
3. Clique em **Create Database**
4. Aguarde a criação (1-2 minutos)
5. **Copie** a **Internal Database URL** (começando com `postgresql://`)

#### 3.2 Criar Web Service

1. Clique em **New** → **Web Service**
2. Conecte o repositório **CardapioAPI**
3. Configure:
   - **Name**: `cardapio-api`
   - **Region**: mesma do banco de dados
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --chdir cardapioAPIProject cardapioAPI.wsgi:application`
   - **Plan**: **Free**

#### 3.3 Configurar Variáveis de Ambiente

Na seção **Environment Variables**, adicione:

```
PYTHON_VERSION=3.9.0
DEBUG=False
DJANGO_SECRET_KEY=<gere uma chave segura>
DATABASE_URL=<cole a Internal Database URL>
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=<escolha uma senha forte>
```

**Para gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. Clique em **Create Web Service**

### 4. Aguardar o Deploy

- O build leva 3-5 minutos na primeira vez
- Acompanhe os logs em tempo real
- Quando aparecer "Your service is live 🎉", está pronto!

## Acessar a API

Sua API estará disponível em:
```
https://cardapio-api.onrender.com
```

### Endpoints:

- `GET /api/items/` - Lista todos os itens
- `POST /api/items/` - Cria novo item
- `GET /api/items/{id}/` - Detalhes de um item
- `PUT /api/items/{id}/` - Atualiza item
- `DELETE /api/items/{id}/` - Remove item
- `POST /api/token/` - Obtém token JWT

### Admin:

```
https://cardapio-api.onrender.com/admin/
```

**Credenciais** (se configurou via blueprint):
- Username: `admin`
- Password: valor gerado automaticamente (veja nas Environment Variables)

**Credenciais** (se configurou manualmente):
- Username: valor de `ADMIN_USERNAME`
- Password: valor de `ADMIN_PASSWORD`

## Testar a API

```bash
# Listar itens
curl https://cardapio-api.onrender.com/api/items/

# Criar item (precisa autenticação)
curl -X POST https://cardapio-api.onrender.com/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Pizza", "descricao": "Pizza margherita", "preco": "35.00", "categoria": 1}'
```

## Atualizar o Deploy

Qualquer push para `main` no GitHub dispara automaticamente um novo deploy:

```bash
git add .
git commit -m "Suas alterações"
git push origin main
```

O Render detecta e faz redeploy automaticamente!

## Configurar CORS para React

No dashboard do Render, adicione/atualize a variável:

```
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app,http://localhost:3000
```

## Monitoramento

### Ver Logs em Tempo Real
1. No dashboard do Render
2. Clique no seu serviço
3. Aba **Logs**

### Métricas
- CPU e Memória disponíveis no dashboard
- Plano Free: 512 MB RAM

### Health Checks
O Render faz ping no seu serviço automaticamente
Se ficar 15 minutos inativo, "dorme" (cold start)

## Banco de Dados PostgreSQL

### Conectar ao Banco

Use a **External Database URL** para conectar de ferramentas locais:

```bash
psql <External Database URL>
```

Ou use ferramentas GUI:
- pgAdmin
- DBeaver
- TablePlus

### Backup

O plano Free do Render **não inclui backups automáticos**.

Para fazer backup manual:
```bash
pg_dump <External Database URL> > backup.sql
```

### Restore
```bash
psql <External Database URL> < backup.sql
```

## Limites do Plano Free

- ✅ 750 horas/mês de serviço web
- ✅ PostgreSQL com 256 MB de storage
- ⚠️ Serviço "dorme" após 15 min de inatividade (cold start ~30s)
- ⚠️ Sem backups automáticos

## Troubleshooting

### Build Falhou

**Erro**: `Permission denied: ./build.sh`

**Solução**: Tornar o arquivo executável:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push origin main
```

### Erro de Conexão com Banco

**Erro**: `could not connect to database`

**Solução**: 
- Verifique se a variável `DATABASE_URL` está correta
- Use a **Internal Database URL** (não a External)
- Certifique-se que o banco foi criado na mesma região

### Import Error

**Erro**: `ModuleNotFoundError`

**Solução**: Adicione o módulo faltando no `requirements.txt`

### Static Files não carregam

Os static files são servidos pelo WhiteNoise automaticamente.

Se ainda não funcionar:
```bash
python cardapioAPIProject/manage.py collectstatic --no-input
```

## Upgrade para Plano Pago (Opcional)

Se precisar de mais recursos:
- **Starter ($7/mês)**: Sem cold starts, 512 MB RAM
- **Standard ($25/mês)**: 2 GB RAM, backups automáticos

## Arquivos Configurados

- ✅ `render.yaml` - Configuração automática do Render
- ✅ `build.sh` - Script de build
- ✅ `requirements.txt` - Dependências (gunicorn, psycopg2)
- ✅ `settings.py` - Suporte a PostgreSQL com dj-database-url

## Comparação: Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| Banco de dados | PostgreSQL grátis | SQLite volátil |
| Persistência | ✅ Sim | ❌ Não |
| Django | ✅ Excelente | ⚠️ Limitado |
| Cold starts | ~30s (free) | ~5s |
| Setup | Mais fácil | Mais complexo |

**Recomendação**: Use **Render** para APIs Django com banco de dados!

## Próximos Passos

1. ✅ Deploy no Render
2. 🔐 Alterar senha do admin
3. 🗄️ Fazer backup do banco periodicamente
4. 🌐 Conectar com seu frontend React
5. 📊 Monitorar logs e performance

Seu projeto está pronto para produção! 🎉
