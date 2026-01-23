# =================================================
# Script para ver logs da aplicação Docker
# =================================================

Write-Host "📊 Exibindo logs da aplicação..." -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para sair" -ForegroundColor Yellow
Write-Host ""

docker-compose logs -f
