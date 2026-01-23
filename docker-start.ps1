# =================================================
# Script para iniciar a aplicação com Docker
# =================================================

Write-Host "🚀 Iniciando Leitor de Notas Fiscais com Docker..." -ForegroundColor Cyan
Write-Host ""

# Verificar se o arquivo .env.docker existe
if (-not (Test-Path ".env.docker")) {
    Write-Host "❌ Arquivo .env.docker não encontrado!" -ForegroundColor Red
    Write-Host "📝 Criando .env.docker a partir do .env.docker.example..." -ForegroundColor Yellow
    Copy-Item ".env.docker.example" ".env.docker"
    Write-Host "⚠️  Por favor, edite o arquivo .env.docker com suas credenciais AWS" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Build e start dos containers
Write-Host "🔨 Construindo imagem Docker..." -ForegroundColor Green
docker-compose build

Write-Host ""
Write-Host "🚀 Iniciando containers..." -ForegroundColor Green
docker-compose up -d

Write-Host ""
Write-Host "✅ Aplicação iniciada com sucesso!" -ForegroundColor Green
Write-Host "📍 Acesse: http://localhost:5090" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Para ver os logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "🛑 Para parar: docker-compose down" -ForegroundColor Yellow
Write-Host ""
