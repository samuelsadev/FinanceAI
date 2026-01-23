# =================================================
# Script para parar a aplicação Docker
# =================================================

Write-Host "🛑 Parando Leitor de Notas Fiscais..." -ForegroundColor Yellow
Write-Host ""

docker-compose down

Write-Host ""
Write-Host "✅ Aplicação parada com sucesso!" -ForegroundColor Green
Write-Host ""
