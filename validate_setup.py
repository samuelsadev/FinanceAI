#!/usr/bin/env python3
"""
Script de validação da configuração do projeto
Verifica se todos os arquivos e configurações estão corretos
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Verifica se um arquivo existe"""
    exists = Path(filepath).exists()
    status = "✓" if exists else ("✗" if required else "⚠")
    color = "\033[92m" if exists else ("\033[91m" if required else "\033[93m")
    reset = "\033[0m"
    print(f"{color}{status}{reset} {filepath}")
    return exists

def check_env_file(filepath):
    """Verifica se o arquivo .env tem as variáveis necessárias"""
    if not Path(filepath).exists():
        return False
    
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        missing_vars = []
        for var in required_vars:
            if f"{var}=" not in content:
                missing_vars.append(var)
        
        if missing_vars:
            for var in missing_vars:
                print(f"  ⚠ Variável {var} não encontrada em {filepath}")
            return False
    return True

def main():
    print("\n" + "="*60)
    print("🔍 VALIDAÇÃO DA CONFIGURAÇÃO DO PROJETO")
    print("="*60 + "\n")
    
    # Verificar arquivos principais
    print("📁 Arquivos Principais:")
    check_file_exists("app.py")
    check_file_exists("requirements.txt")
    check_file_exists("Dockerfile")
    check_file_exists("docker-compose.yml")
    check_file_exists("README.md")
    check_file_exists("CHANGELOG.md")
    
    print("\n📁 Arquivos de Configuração:")
    env_exists = check_file_exists(".env", required=False)
    env_docker_exists = check_file_exists(".env.docker", required=False)
    check_file_exists(".env.example")
    check_file_exists(".env.docker.example")
    check_file_exists(".gitignore")
    check_file_exists(".dockerignore")
    
    print("\n📁 Scripts PowerShell:")
    check_file_exists("start_server.ps1", required=False)
    check_file_exists("docker-start.ps1", required=False)
    check_file_exists("docker-stop.ps1", required=False)
    check_file_exists("docker-logs.ps1", required=False)
    
    print("\n📁 Diretórios:")
    check_file_exists("services/")
    check_file_exists("templates/")
    check_file_exists("static/")
    check_file_exists("static/css/")
    check_file_exists("static/js/")
    check_file_exists("uploads/")
    
    print("\n📁 Arquivos de Serviços:")
    check_file_exists("services/__init__.py")
    check_file_exists("services/aws_service.py")
    check_file_exists("services/textract_service.py")
    check_file_exists("services/rekognition_service.py")
    check_file_exists("services/bedrock_service.py")
    check_file_exists("services/document_processor.py")
    
    print("\n📁 Arquivos Frontend:")
    check_file_exists("templates/index.html")
    check_file_exists("static/css/styles.css")
    check_file_exists("static/js/config.js")
    check_file_exists("static/js/app.js")
    check_file_exists("static/js/charts.js")
    check_file_exists("static/js/fileUpload.js")
    check_file_exists("static/README.md")
    
    # Validar arquivos .env
    print("\n🔐 Validação de Credenciais:")
    if env_exists:
        if check_env_file(".env"):
            print("  ✓ Arquivo .env configurado corretamente")
        else:
            print("  ✗ Arquivo .env incompleto")
    else:
        print("  ⚠ Arquivo .env não encontrado (necessário para execução local)")
    
    if env_docker_exists:
        if check_env_file(".env.docker"):
            print("  ✓ Arquivo .env.docker configurado corretamente")
        else:
            print("  ✗ Arquivo .env.docker incompleto")
    else:
        print("  ⚠ Arquivo .env.docker não encontrado (necessário para Docker)")
    
    # Verificar dependências Python
    print("\n📦 Dependências Python:")
    try:
        import flask
        print(f"  ✓ Flask {flask.__version__}")
    except ImportError:
        print("  ✗ Flask não instalado")
    
    try:
        import boto3
        print(f"  ✓ boto3 {boto3.__version__}")
    except ImportError:
        print("  ✗ boto3 não instalado")
    
    try:
        import dotenv
        print("  ✓ python-dotenv instalado")
    except ImportError:
        print("  ✗ python-dotenv não instalado")
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    if env_exists and env_docker_exists:
        print("✅ Projeto configurado corretamente!")
        print("\n🚀 Próximos passos:")
        print("   1. Verifique as credenciais AWS nos arquivos .env")
        print("   2. Execute: docker-compose up --build")
        print("   3. Acesse: http://localhost:5090")
    else:
        print("⚠️  Configuração incompleta!")
        print("\n📝 Ações necessárias:")
        if not env_exists:
            print("   1. Copie .env.example para .env")
            print("   2. Adicione suas credenciais AWS no .env")
        if not env_docker_exists:
            print("   3. Copie .env.docker.example para .env.docker")
            print("   4. Adicione suas credenciais AWS no .env.docker")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
