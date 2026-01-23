#!/bin/sh
# =================================================
# Script de Inicialização do Banco de Dados
# FinanceAI
# =================================================

echo "🔧 Inicializando banco de dados..."

# Criar diretório se não existir
mkdir -p /data

# Verificar se o banco já existe
if [ -f "/data/expenses.db" ]; then
    echo "✓ Banco de dados já existe: /data/expenses.db"
    echo "📊 Tamanho: $(du -h /data/expenses.db | cut -f1)"
else
    echo "📝 Banco de dados será criado na primeira execução da aplicação"
fi

# Definir permissões
chmod 755 /data
if [ -f "/data/expenses.db" ]; then
    chmod 644 /data/expenses.db
fi

echo "✓ Inicialização concluída!"
echo "📍 Banco de dados: /data/expenses.db"

# Manter container rodando
tail -f /dev/null
