#!/bin/bash
# =================================================
# Script para Ver Estatísticas do Banco de Dados
# FinanceAI
# =================================================

echo "📊 Estatísticas do Banco de Dados"
echo "═════════════════════════════════════════════════════════"
echo ""

# Verificar se o banco existe
if ! docker exec financeai-database test -f /data/expenses.db; then
    echo "❌ Banco de dados não encontrado!"
    echo "💡 O banco será criado automaticamente quando você processar o primeiro documento."
    exit 1
fi

# Tamanho do banco
echo "📁 Informações do Arquivo:"
SIZE=$(docker exec financeai-database du -h /data/expenses.db | cut -f1)
echo "   Tamanho: ${SIZE}"
echo ""

# Estatísticas das tabelas
echo "📋 Estatísticas das Tabelas:"
echo ""

# Total de registros
TOTAL=$(docker exec financeai-database sqlite3 /data/expenses.db "SELECT COUNT(*) FROM analyses;")
echo "   Total de análises: ${TOTAL}"

# Total gasto
TOTAL_GASTO=$(docker exec financeai-database sqlite3 /data/expenses.db "SELECT ROUND(SUM(valor), 2) FROM analyses;")
echo "   Total gasto: R$ ${TOTAL_GASTO}"

# Por categoria
echo ""
echo "📊 Gastos por Categoria:"
docker exec financeai-database sqlite3 /data/expenses.db \
    "SELECT 
        categoria, 
        COUNT(*) as quantidade,
        ROUND(SUM(valor), 2) as total,
        ROUND(AVG(valor), 2) as media
     FROM analyses 
     GROUP BY categoria 
     ORDER BY total DESC;" \
    -header -column

# Últimos registros
echo ""
echo "📅 Últimos 5 Registros:"
docker exec financeai-database sqlite3 /data/expenses.db \
    "SELECT 
        datetime(created_at, 'localtime') as data,
        filename,
        empresa,
        categoria,
        'R$ ' || ROUND(valor, 2) as valor
     FROM analyses 
     ORDER BY created_at DESC 
     LIMIT 5;" \
    -header -column

echo ""
echo "═════════════════════════════════════════════════════════"
