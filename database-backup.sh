#!/bin/bash
# =================================================
# Script de Backup do Banco de Dados
# FinanceAI
# =================================================

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
BACKUP_FILE="expenses_backup_${TIMESTAMP}.db"

echo "🔄 Iniciando backup do banco de dados..."

# Criar diretório de backups se não existir
mkdir -p ${BACKUP_DIR}

# Fazer backup do banco de dados do container
docker exec financeai-database sqlite3 /data/expenses.db ".backup /data/backup_temp.db"

# Copiar backup para o host
docker cp financeai-database:/data/backup_temp.db ${BACKUP_DIR}/${BACKUP_FILE}

# Remover backup temporário do container
docker exec financeai-database rm /data/backup_temp.db

# Verificar se o backup foi criado
if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo "✓ Backup criado com sucesso!"
    echo "📁 Arquivo: ${BACKUP_DIR}/${BACKUP_FILE}"
    echo "📊 Tamanho: ${SIZE}"
    
    # Manter apenas os últimos 10 backups
    cd ${BACKUP_DIR}
    ls -t expenses_backup_*.db | tail -n +11 | xargs -r rm
    echo "🗑️  Backups antigos removidos (mantidos últimos 10)"
else
    echo "✗ Erro ao criar backup!"
    exit 1
fi

echo "✓ Backup concluído!"
