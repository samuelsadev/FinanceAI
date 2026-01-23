# =================================================
# Script para Ver Estatísticas do Banco (PowerShell)
# FinanceAI
# =================================================

Write-Host "📊 Estatísticas do Banco de Dados" -ForegroundColor Cyan
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

# Verificar se o banco existe
$dbExists = docker exec financeai-database test -f /data/expenses.db
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Banco de dados não encontrado!" -ForegroundColor Red
    Write-Host "💡 O banco será criado automaticamente quando você processar o primeiro documento." -ForegroundColor Yellow
    exit 1
}

# Tamanho do banco
Write-Host "📁 Informações do Arquivo:" -ForegroundColor White
$SIZE = docker exec financeai-database du -h /data/expenses.db
$SIZE = ($SIZE -split '\s+')[0]
Write-Host "   Tamanho: $SIZE" -ForegroundColor Gray
Write-Host ""

# Estatísticas das tabelas
Write-Host "📋 Estatísticas das Tabelas:" -ForegroundColor White
Write-Host ""

# Total de registros
$TOTAL = docker exec financeai-database sqlite3 /data/expenses.db "SELECT COUNT(*) FROM analyses;"
Write-Host "   Total de análises: $TOTAL" -ForegroundColor Gray

# Total gasto
$TOTAL_GASTO = docker exec financeai-database sqlite3 /data/expenses.db "SELECT ROUND(SUM(valor), 2) FROM analyses;"
Write-Host "   Total gasto: R$ $TOTAL_GASTO" -ForegroundColor Gray

# Por categoria
Write-Host ""
Write-Host "📊 Gastos por Categoria:" -ForegroundColor White
docker exec financeai-database sqlite3 /data/expenses.db @"
SELECT 
    categoria, 
    COUNT(*) as quantidade,
    ROUND(SUM(valor), 2) as total,
    ROUND(AVG(valor), 2) as media
FROM analyses 
GROUP BY categoria 
ORDER BY total DESC;
"@ -header -column

# Últimos registros
Write-Host ""
Write-Host "📅 Últimos 5 Registros:" -ForegroundColor White
docker exec financeai-database sqlite3 /data/expenses.db @"
SELECT 
    datetime(created_at, 'localtime') as data,
    filename,
    empresa,
    categoria,
    'R$ ' || ROUND(valor, 2) as valor
FROM analyses 
ORDER BY created_at DESC 
LIMIT 5;
"@ -header -column

Write-Host ""
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Gray
