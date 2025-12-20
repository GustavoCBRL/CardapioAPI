#!/bin/bash
# Oracle Cloud Infrastructure - Setup Script para CardapioAPI
# Autor: GustavoCBRL
# Uso: sudo ./oci-setup.sh

set -e

echo "================================================"
echo "  CardapioAPI - Setup Oracle Cloud (OCI)"
echo "================================================"
echo ""

# Detectar sistema operacional
if [ -f /etc/oracle-release ]; then
    OS="oracle"
    echo "✓ Detectado: Oracle Linux"
elif [ -f /etc/lsb-release ]; then
    OS="ubuntu"
    echo "✓ Detectado: Ubuntu"
else
    echo "❌ Sistema operacional não suportado"
    exit 1
fi

# Atualizar sistema
echo ""
echo "[1/8] Atualizando sistema..."
if [ "$OS" = "ubuntu" ]; then
    apt update && apt upgrade -y
else
    yum update -y
fi

# Instalar Python 3.11+
echo ""
echo "[2/8] Instalando Python 3.11..."
if [ "$OS" = "ubuntu" ]; then
    apt install -y python3.11 python3.11-venv python3-pip python3.11-dev
else
    yum install -y python3.11 python3.11-pip python3.11-devel
fi

# Instalar PostgreSQL
echo ""
echo "[3/8] Instalando PostgreSQL..."
if [ "$OS" = "ubuntu" ]; then
    apt install -y postgresql postgresql-contrib libpq-dev
else
    yum install -y postgresql postgresql-server postgresql-contrib postgresql-devel
    postgresql-setup --initdb
fi
systemctl start postgresql
systemctl enable postgresql

# Instalar Nginx
echo ""
echo "[4/8] Instalando Nginx..."
if [ "$OS" = "ubuntu" ]; then
    apt install -y nginx
else
    yum install -y nginx
fi
systemctl start nginx
systemctl enable nginx

# Instalar Git
echo ""
echo "[5/8] Instalando Git..."
if [ "$OS" = "ubuntu" ]; then
    apt install -y git
else
    yum install -y git
fi

# Instalar ferramentas adicionais
echo ""
echo "[6/8] Instalando ferramentas adicionais..."
if [ "$OS" = "ubuntu" ]; then
    apt install -y build-essential curl wget htop
else
    yum install -y gcc gcc-c++ make curl wget htop
fi

# Configurar firewall
echo ""
echo "[7/8] Configurando firewall..."
if [ "$OS" = "ubuntu" ]; then
    ufw allow 'Nginx Full'
    ufw allow OpenSSH
    echo "y" | ufw enable
else
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --permanent --add-service=ssh
    firewall-cmd --reload
fi

# Criar diretórios
echo ""
echo "[8/8] Criando estrutura de diretórios..."
mkdir -p /var/log/gunicorn
if [ "$OS" = "ubuntu" ]; then
    chown ubuntu:www-data /var/log/gunicorn
else
    chown opc:nginx /var/log/gunicorn
fi

echo ""
echo "================================================"
echo "  ✓ Setup Concluído!"
echo "================================================"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Configurar PostgreSQL:"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE cardapio_db;"
echo "   CREATE USER cardapio_user WITH PASSWORD 'sua_senha';"
echo "   GRANT ALL PRIVILEGES ON DATABASE cardapio_db TO cardapio_user;"
echo "   \q"
echo ""
echo "2. Clonar projeto:"
if [ "$OS" = "ubuntu" ]; then
    echo "   cd /home/ubuntu"
else
    echo "   cd /home/opc"
fi
echo "   git clone https://github.com/GustavoCBRL/CardapioAPI.git"
echo ""
echo "3. Seguir OCI_DEPLOY.md para configuração completa"
echo ""
