# =================================================
# Dockerfile - Leitor de Notas Fiscais
# Darede a Nuvem
# =================================================

FROM python:3.11-slim

# Metadados
LABEL maintainer="Darede a Nuvem"
LABEL description="Leitor de Notas Fiscais com IA - AWS Bedrock, Textract, Rekognition"
LABEL version="1.0"

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar apenas requirements primeiro (cache layer)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app.py .
COPY services/ ./services/
COPY templates/ ./templates/
COPY static/ ./static/

# Criar diretórios necessários
RUN mkdir -p uploads data && \
    chmod 755 uploads data

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta 5080
EXPOSE 5080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5080/health')" || exit 1

# Comando para executar a aplicação
CMD ["python", "app.py"]
