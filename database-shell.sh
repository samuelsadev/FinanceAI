#!/bin/bash
# =================================================
# Script para Acessar o Shell do Banco de Dados
# FinanceAI
# =================================================

echo "🔧 Acessando shell do banco de dados SQLite..."
echo "📍 Banco: /data/expenses.db"
echo ""
echo "Comandos úteis:"
echo "  .tables          - Listar tabelas"
echo "  .schema          - Ver estrutura das tabelas"
echo "  .quit            - Sair"
echo ""
echo "Exemplo de consulta:"
echo "  SELECT COUNT(*) FROM analyses;"
echo ""
echo "─────────────────────────────────────────────────────────"
echo ""

# Verificar se o banco existe
if docker exec financeai-database test -f /data/expenses.db; then
    docker exec -it financeai-database sqlite3 /data/expenses.db
else
    echo "❌ Banco de dados não encontrado!"
    echo "💡 O banco será criado automaticamente quando você processar o primeiro documento."
    exit 1
fi
