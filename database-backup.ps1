# =================================================
# Script de Backup do Banco de Dados (PowerShell)
# FinanceAI
# =================================================

$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_DIR = ".\backups"
$BACKUP_FILE = "expenses_backup_$TIMESTAMP.db"

Write-Host "🔄 Iniciando backup do banco de dados..." -ForegroundColor Cyan

# Criar diretório de backups se não existir
if (!(Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}

# Fazer backup do banco de dados do container
Write-Host "📦 Criando backup..." -ForegroundColor Yellow
docker exec financeai-database sqlite3 /data/expenses.db ".backup /data/backup_temp.db"

# Copiar backup para o host
docker cp financeai-database:/data/backup_temp.db "$BACKUP_DIR\$BACKUP_FILE"

# Remover backup temporário do container
docker exec financeai-database rm /data/backup_temp.db

# Verificar se o backup foi criado
if (Test-Path "$BACKUP_DIR\$BACKUP_FILE") {
    $SIZE = (Get-Item "$BACKUP_DIR\$BACKUP_FILE").Length / 1KB
    Write-Host "✓ Backup criado com sucesso!" -ForegroundColor Green
    Write-Host "📁 Arquivo: $BACKUP_DIR\$BACKUP_FILE" -ForegroundColor White
    Write-Host "📊 Tamanho: $([math]::Round($SIZE, 2)) KB" -ForegroundColor White
    
    # Manter apenas os últimos 10 backups
    Get-ChildItem "$BACKUP_DIR\expenses_backup_*.db" | 
        Sort-Object LastWriteTime -Descending | 
        Select-Object -Skip 10 | 
        Remove-Item -Force
    
    Write-Host "🗑️  Backups antigos removidos (mantidos últimos 10)" -ForegroundColor Gray
} else {
    Write-Host "✗ Erro ao criar backup!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Backup concluído!" -ForegroundColor Green
