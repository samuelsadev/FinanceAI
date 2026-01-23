#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do banco de dados
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.database_service import DatabaseService

def test_database():
    """Testa as funcionalidades do banco de dados"""
    
    print("="*60)
    print("TESTE DO BANCO DE DADOS SQLITE")
    print("="*60)
    
    # Inicializar serviço
    print("\n1. Inicializando banco de dados...")
    db = DatabaseService('data/test_expenses.db')
    print("✓ Banco inicializado com sucesso!")
    
    # Criar dados de teste
    print("\n2. Criando dados de teste...")
    test_results = [
        {
            'success': True,
            'filename': 'nota_fiscal_1.pdf',
            'analysis': {
                'valor': 150.50,
                'categoria': 'Alimentação',
                'data': '15/01/2025',
                'cnpj': '12.345.678/0001-90',
                'empresa': 'Restaurante Bom Sabor'
            },
            'extracted_text': 'Texto extraído da nota fiscal...',
            'logos': [{'name': 'Logo1', 'confidence': 95.5}]
        },
        {
            'success': True,
            'filename': 'comprovante_uber.pdf',
            'analysis': {
                'valor': 45.80,
                'categoria': 'Transporte',
                'data': '16/01/2025',
                'cnpj': '98.765.432/0001-10',
                'empresa': 'Uber'
            },
            'extracted_text': 'Comprovante de viagem...',
            'logos': [{'name': 'Uber', 'confidence': 99.0}]
        },
        {
            'success': True,
            'filename': 'farmacia.pdf',
            'analysis': {
                'valor': 89.90,
                'categoria': 'Saúde',
                'data': '17/01/2025',
                'cnpj': '11.222.333/0001-44',
                'empresa': 'Farmácia Popular'
            },
            'extracted_text': 'Nota fiscal de medicamentos...',
            'logos': []
        }
    ]
    
    for result in test_results:
        record_id = db.save_analysis(result)
        print(f"✓ Registro salvo: ID {record_id} - {result['filename']}")
    
    # Buscar todas as análises
    print("\n3. Buscando todas as análises...")
    analyses = db.get_all_analyses()
    print(f"✓ Total de registros: {len(analyses)}")
    
    for analysis in analyses:
        print(f"  - {analysis['filename']}: R$ {analysis['valor']:.2f} ({analysis['categoria']})")
    
    # Calcular estatísticas
    print("\n4. Calculando estatísticas...")
    stats = db.get_statistics()
    print(f"✓ Total gasto: R$ {stats['total_gasto']:.2f}")
    print(f"✓ Total de arquivos: {stats['total_arquivos']}")
    print(f"✓ Categorias:")
    
    for categoria, dados in stats['categorias'].items():
        print(f"  - {categoria}: R$ {dados['valor']:.2f} ({dados['percentual']:.1f}%) - {dados['count']} registros")
    
    # Testar busca
    print("\n5. Testando busca...")
    search_term = "Uber"
    results = db.search_analyses(search_term)
    print(f"✓ Busca por '{search_term}': {len(results)} resultado(s)")
    
    for result in results:
        print(f"  - {result['empresa']}: R$ {result['valor']:.2f}")
    
    print("\n" + "="*60)
    print("TODOS OS TESTES PASSARAM COM SUCESSO! ✓")
    print("="*60)
    
    # Limpar banco de teste
    print("\n6. Limpando banco de teste...")
    if os.path.exists('data/test_expenses.db'):
        os.remove('data/test_expenses.db')
        print("✓ Banco de teste removido")

if __name__ == '__main__':
    try:
        test_database()
    except Exception as e:
        print(f"\n✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
