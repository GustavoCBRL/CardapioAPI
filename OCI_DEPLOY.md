# Deploy no Oracle Cloud Infrastructure (OCI) - Guia Completo

## 🚀 Por que Oracle Cloud?

- ✅ **Always Free Tier** - 2 VMs ARM (4 CPUs, 24GB RAM total) ou 2 VMs AMD (1 CPU, 1GB RAM cada)
- ✅ **200GB Block Storage grátis**
- ✅ **PostgreSQL ou MySQL grátis** (Autonomous Database)
- ✅ **10TB de tráfego de saída por mês**
- ✅ **IP público grátis**
- ✅ **100% gratuito para sempre** (não expira!)

## Passo a Passo

### 1. Criar Conta no Oracle Cloud

1. Acesse [cloud.oracle.com](https://cloud.oracle.com)
2. Clique em **Start for free**
3. Preencha o formulário (precisa de cartão, mas **não cobra**)
4. Confirme email e faça login

### 2. Criar Compute Instance (VM)

1. No console OCI, vá em **Compute** → **Instances**
2. Clique em **Create Instance**

#### Configuração Recomendada:

- **Name**: `cardapio-api`
- **Compartment**: (deixe padrão)
- **Availability Domain**: (escolha qualquer)
- **Image**: `Oracle Linux 8` ou `Ubuntu 22.04`
- **Shape**: 
  - **Always Free**: `VM.Standard.A1.Flex` (ARM - 4 OCPUs, 24GB RAM)
  - OU: `VM.Standard.E2.1.Micro` (AMD - 1 OCPU, 1GB RAM)
- **Networking**:
  - Create new VCN: `cardapio-vcn`
  - Assign public IP: ✅ **Yes**
- **SSH Keys**: 
  - Clique em **Generate SSH Key Pair**
  - Baixe a chave privada (`ssh-key-*.key`)
  - **IMPORTANTE**: Guarde bem essa chave!

3. Clique em **Create**
4. Aguarde a VM ficar em **Running** (2-3 minutos)
5. Anote o **Public IP Address**

### 3. Configurar Firewall (Security List)

1. Na página da instância, clique no link da **Subnet**
2. Vá em **Security Lists** → Clique na security list padrão
3. Clique em **Add Ingress Rules**

Adicione as seguintes regras:

#### Regra 1 - HTTP
- **Source CIDR**: `0.0.0.0/0`
- **IP Protocol**: `TCP`
- **Destination Port Range**: `80`
- **Description**: `HTTP`

#### Regra 2 - HTTPS
- **Source CIDR**: `0.0.0.0/0`
- **IP Protocol**: `TCP`
- **Destination Port Range**: `443`
- **Description**: `HTTPS`

### 4. Conectar via SSH

#### Linux/Mac:
```bash
chmod 400 ~/Downloads/ssh-key-*.key
ssh -i ~/Downloads/ssh-key-*.key ubuntu@SEU_IP_PUBLICO
# OU para Oracle Linux:
ssh -i ~/Downloads/ssh-key-*.key opc@SEU_IP_PUBLICO
```

#### Windows (PowerShell):
```powershell
ssh -i C:\Users\SeuNome\Downloads\ssh-key-*.key ubuntu@SEU_IP_PUBLICO
```

### 5. Setup Inicial no Servidor

Quando conectado via SSH, execute:

```bash
# Baixar script de setup
curl -O https://raw.githubusercontent.com/GustavoCBRL/CardapioAPI/main/oci-setup.sh
chmod +x oci-setup.sh
sudo ./oci-setup.sh
```

**OU** faça manualmente:

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y  # Ubuntu
# OU
sudo yum update -y  # Oracle Linux

# Instalar Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip -y  # Ubuntu
# OU
sudo yum install python3.11 python3.11-pip -y  # Oracle Linux

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y  # Ubuntu
# OU
sudo yum install postgresql postgresql-server postgresql-contrib -y  # Oracle Linux
sudo postgresql-setup --initdb  # Oracle Linux only
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Instalar Nginx
sudo apt install nginx -y  # Ubuntu
# OU
sudo yum install nginx -y  # Oracle Linux
sudo systemctl start nginx
sudo systemctl enable nginx

# Instalar Git
sudo apt install git -y  # Ubuntu
# OU
sudo yum install git -y  # Oracle Linux

# Abrir firewall interno
sudo firewall-cmd --permanent --add-service=http  # Oracle Linux
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
# OU
sudo ufw allow 'Nginx Full'  # Ubuntu
```

### 6. Configurar PostgreSQL

```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE cardapio_db;
CREATE USER cardapio_user WITH PASSWORD 'sua_senha_segura_aqui';
ALTER ROLE cardapio_user SET client_encoding TO 'utf8';
ALTER ROLE cardapio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cardapio_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE cardapio_db TO cardapio_user;
\q
```

### 7. Clonar e Configurar Projeto

```bash
# Criar diretório
cd /home/ubuntu  # ou /home/opc para Oracle Linux
git clone https://github.com/GustavoCBRL/CardapioAPI.git
cd CardapioAPI

# Criar virtualenv
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
nano .env
```

Cole no `.env`:
```env
DJANGO_SECRET_KEY=gere-uma-chave-super-segura-aqui
DEBUG=False
DATABASE_URL=postgresql://cardapio_user:sua_senha_segura_aqui@localhost:5432/cardapio_db
ALLOWED_HOSTS=seu-ip-publico.com,localhost,127.0.0.1
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=senha-admin-segura
```

Salve: `Ctrl+X` → `Y` → `Enter`

```bash
# Executar migrations
cd cardapioAPIProject
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

### 8. Configurar Gunicorn (Systemd Service)

```bash
sudo nano /etc/systemd/system/cardapio.service
```

Cole:
```ini
[Unit]
Description=Cardapio API Gunicorn daemon
After=network.target

[Service]
Type=notify
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/CardapioAPI/cardapioAPIProject
Environment="PATH=/home/ubuntu/CardapioAPI/venv/bin"
EnvironmentFile=/home/ubuntu/CardapioAPI/.env
ExecStart=/home/ubuntu/CardapioAPI/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/CardapioAPI/gunicorn.sock \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          cardapioAPI.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Para Oracle Linux**, mude `User=opc` e os caminhos para `/home/opc/`.

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn  # ou opc:www-data

# Iniciar serviço
sudo systemctl start cardapio
sudo systemctl enable cardapio
sudo systemctl status cardapio
```

### 9. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/cardapio
```

Cole:
```nginx
server {
    listen 80;
    server_name SEU_IP_PUBLICO;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/CardapioAPI/cardapioAPIProject/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/CardapioAPI/cardapioAPIProject/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/CardapioAPI/gunicorn.sock;
    }
}
```

```bash
# Habilitar site
sudo ln -s /etc/nginx/sites-available/cardapio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Para Oracle Linux** (não tem sites-available):
```bash
sudo nano /etc/nginx/conf.d/cardapio.conf
# Cole a configuração acima
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Testar API

Acesse no navegador:
```
http://SEU_IP_PUBLICO/api/items/
http://SEU_IP_PUBLICO/admin/
http://SEU_IP_PUBLICO/health/
```

## 🔒 Configurar HTTPS (Opcional - Recomendado)

### Opção 1: Usar Domínio Próprio + Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y  # Ubuntu
# OU
sudo yum install certbot python3-certbot-nginx -y  # Oracle Linux

# Obter certificado (substitua seu-dominio.com)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática já configurada!
```

### Opção 2: Usar NoIP ou DuckDNS (DNS Dinâmico Grátis)

1. Cadastre-se em [noip.com](https://www.noip.com) ou [duckdns.org](https://www.duckdns.org)
2. Crie um hostname: `cardapio-api.ddns.net`
3. Aponte para seu IP público do OCI
4. Use Certbot com esse domínio

## Monitoramento e Logs

### Ver logs da aplicação
```bash
sudo journalctl -u cardapio -f
```

### Ver logs do Nginx
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Ver logs do Gunicorn
```bash
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log
```

### Reiniciar serviços
```bash
sudo systemctl restart cardapio
sudo systemctl restart nginx
sudo systemctl restart postgresql
```

## Atualizar Código

```bash
cd /home/ubuntu/CardapioAPI
git pull
source venv/bin/activate
cd cardapioAPIProject
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart cardapio
```

## Backup Automático do Banco

```bash
# Criar script de backup
sudo nano /usr/local/bin/backup-cardapio.sh
```

Cole:
```bash
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
PGPASSWORD="sua_senha" pg_dump -U cardapio_user -h localhost cardapio_db > $BACKUP_DIR/cardapio_$TIMESTAMP.sql

# Manter apenas últimos 7 backups
find $BACKUP_DIR -name "cardapio_*.sql" -mtime +7 -delete
```

```bash
chmod +x /usr/local/bin/backup-cardapio.sh

# Agendar backup diário (3h da manhã)
crontab -e
# Adicione:
0 3 * * * /usr/local/bin/backup-cardapio.sh
```

## Segurança Extra

### Configurar fail2ban (proteção contra brute force)
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Desabilitar login root via SSH
```bash
sudo nano /etc/ssh/sshd_config
# Mude: PermitRootLogin no
sudo systemctl restart sshd
```

### Configurar firewall adicional
```bash
# Ubuntu
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Oracle Linux (já tem firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Custos Always Free

### Recursos Gratuitos para Sempre:

- **Compute**: 2x VM.Standard.E2.1.Micro (AMD) ou 4 OCPUs ARM + 24GB RAM
- **Block Volume**: 200 GB total
- **Object Storage**: 10 GB
- **Archive Storage**: 10 GB
- **Load Balancer**: 1 instance
- **Database**: Autonomous Database (20GB storage)
- **Network**: 10 TB/mês de saída

### Seu Projeto Cardapio API:

- ✅ **VM**: ARM Ampere (4 CPUs, 24GB RAM) - **GRÁTIS**
- ✅ **Storage**: 50GB - **GRÁTIS**
- ✅ **PostgreSQL**: Auto no servidor - **GRÁTIS**
- ✅ **Nginx + Gunicorn**: - **GRÁTIS**
- ✅ **Tráfego**: Até 10TB/mês - **GRÁTIS**

**Custo total: R$ 0,00 para sempre!** 🎉

## Troubleshooting

### Erro 502 Bad Gateway
```bash
# Verificar status do gunicorn
sudo systemctl status cardapio
# Verificar logs
sudo journalctl -u cardapio -n 50
# Verificar socket
ls -la /home/ubuntu/CardapioAPI/gunicorn.sock
```

### Erro de permissão
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/CardapioAPI
sudo chmod -R 755 /home/ubuntu/CardapioAPI
```

### PostgreSQL não conecta
```bash
# Editar pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Adicione: local all cardapio_user md5
sudo systemctl restart postgresql
```

## Próximos Passos

1. ✅ Criar conta no Oracle Cloud
2. ✅ Criar Compute Instance (VM ARM)
3. ✅ Configurar firewall (portas 80, 443)
4. ✅ Conectar via SSH
5. ✅ Instalar dependências (Python, PostgreSQL, Nginx)
6. ✅ Configurar PostgreSQL
7. ✅ Clonar e configurar projeto
8. ✅ Configurar Gunicorn como serviço
9. ✅ Configurar Nginx como proxy reverso
10. ✅ Testar API
11. 🔒 Configurar HTTPS (Let's Encrypt)
12. 🌐 Conectar frontend

Seu projeto está rodando em infraestrutura profissional, GRÁTIS para sempre! 🚀
