# Deploy no Vercel - Guia Rápido

## Pré-requisitos
- Conta no [Vercel](https://vercel.com)
- Projeto no GitHub (já configurado ✅)

## Passo a Passo

### 1. Importar o Projeto no Vercel

1. Acesse [vercel.com/new](https://vercel.com/new)
2. Conecte sua conta do GitHub (se ainda não conectou)
3. Selecione o repositório **CardapioAPI**
4. Clique em **Import**

### 2. Configurar Variáveis de Ambiente

Na página de configuração do projeto, adicione estas variáveis de ambiente:

```
DJANGO_SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=.vercel.app
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

**Para gerar uma SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Deploy

1. Clique em **Deploy**
2. Aguarde o build finalizar (1-3 minutos)
3. Seu projeto estará disponível em: `https://seu-projeto.vercel.app`

## Endpoints da API

Após o deploy, sua API estará disponível em:

- `GET https://seu-projeto.vercel.app/api/items/` - Lista todos os itens
- `POST https://seu-projeto.vercel.app/api/items/` - Cria novo item
- `GET https://seu-projeto.vercel.app/api/items/{id}/` - Detalhes de um item
- `PUT https://seu-projeto.vercel.app/api/items/{id}/` - Atualiza item
- `DELETE https://seu-projeto.vercel.app/api/items/{id}/` - Remove item
- `POST https://seu-projeto.vercel.app/api/token/` - Obtém token JWT
- `POST https://seu-projeto.vercel.app/api/token/refresh/` - Atualiza token

## Testar a API

```bash
curl https://seu-projeto.vercel.app/api/items/
```

## Atualizar o Deploy

Qualquer push para a branch `main` no GitHub dispara automaticamente um novo deploy no Vercel.

```bash
git add .
git commit -m "Suas alterações"
git push origin main
```

## Solução de Problemas

### Erro 500
- Verifique se as variáveis de ambiente estão configuradas
- Confira os logs no painel do Vercel

### CORS Error
- Adicione a URL do seu frontend em `CORS_ALLOWED_ORIGINS`
- Exemplo: `https://meu-frontend.vercel.app,http://localhost:3000`

### Migrations não aplicadas
- O Vercel usa SQLite em memória (os dados são perdidos)
- Para produção, considere usar um banco PostgreSQL externo (ex: Supabase, Neon)

## Banco de Dados para Produção (Opcional)

Para persistência de dados, configure PostgreSQL:

1. Crie um banco no [Supabase](https://supabase.com) ou [Neon](https://neon.tech)
2. Adicione ao `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   dj-database-url==2.1.0
   ```
3. Configure em `settings.py`:
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```
4. Adicione a variável de ambiente `DATABASE_URL` no Vercel

## Arquivos de Configuração Criados

- ✅ `vercel.json` - Configuração do Vercel
- ✅ `build.sh` - Script de build (migrations e static files)
- ✅ `requirements.txt` - Dependências limpas e otimizadas
- ✅ `settings.py` - Configurado com whitenoise e variáveis de ambiente
- ✅ `.gitignore` - Atualizado para Vercel

## Próximos Passos

1. ⬆️ Fazer deploy no Vercel seguindo os passos acima
2. 🔐 Configurar SECRET_KEY segura
3. 🗄️ (Opcional) Configurar PostgreSQL para produção
4. 🌐 Conectar com seu frontend
5. 📊 Monitorar logs e performance no dashboard do Vercel
