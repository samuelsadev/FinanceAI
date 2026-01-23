#!/bin/bash
# =================================================
# Script de Restauração do Banco de Dados
# FinanceAI
# =================================================

if [ -z "$1" ]; then
    echo "❌ Uso: ./database-restore.sh <arquivo_backup.db>"
    echo ""
    echo "Backups disponíveis:"
    ls -lh ./backups/expenses_backup_*.db 2>/dev/null || echo "  Nenhum backup encontrado"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "❌ Arquivo de backup não encontrado: ${BACKUP_FILE}"
    exit 1
fi

echo "⚠️  ATENÇÃO: Esta operação irá substituir o banco de dados atual!"
echo "📁 Backup: ${BACKUP_FILE}"
echo ""
read -p "Deseja continuar? (s/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Operação cancelada"
    exit 0
fi

echo "🔄 Restaurando banco de dados..."

# Parar a aplicação
echo "⏸️  Parando aplicação..."
docker-compose stop app

# Copiar backup para o container
docker cp ${BACKUP_FILE} financeai-database:/data/restore_temp.db

# Substituir banco de dados
docker exec financeai-database sh -c "mv /data/expenses.db /data/expenses.db.old 2>/dev/null; mv /data/restore_temp.db /data/expenses.db"

# Verificar restauração
if docker exec financeai-database test -f /data/expenses.db; then
    SIZE=$(docker exec financeai-database du -h /data/expenses.db | cut -f1)
    echo "✓ Banco de dados restaurado com sucesso!"
    echo "📊 Tamanho: ${SIZE}"
    
    # Remover backup antigo
    docker exec financeai-database rm /data/expenses.db.old 2>/dev/null
else
    echo "✗ Erro ao restaurar banco de dados!"
    echo "🔄 Tentando reverter..."
    docker exec financeai-database mv /data/expenses.db.old /data/expenses.db 2>/dev/null
    exit 1
fi

# Reiniciar aplicação
echo "▶️  Reiniciando aplicação..."
docker-compose start app

echo "✓ Restauração concluída!"
