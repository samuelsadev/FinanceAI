import sqlite3
import json
from datetime import datetime
import os

class DatabaseService:
    """Serviço para gerenciar o banco de dados SQLite"""
    
    def __init__(self, db_path='data/expenses.db'):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Garante que o diretório do banco existe"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def _init_database(self):
        """Inicializa o banco de dados e cria tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de análises de documentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                data_documento TEXT,
                cnpj TEXT,
                empresa TEXT,
                extracted_text TEXT,
                logos TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Banco de dados inicializado: {self.db_path}")
    
    def save_analysis(self, result):
        """
        Salva uma análise no banco de dados
        
        Args:
            result: Dicionário com os dados da análise
        
        Returns:
            int: ID do registro inserido
        """
        if not result.get('success'):
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = result.get('analysis', {})
        logos = result.get('logos', [])
        
        cursor.execute('''
            INSERT INTO analyses 
            (filename, valor, categoria, data_documento, cnpj, empresa, extracted_text, logos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.get('filename'),
            float(analysis.get('valor', 0)),
            analysis.get('categoria', 'Outros'),
            analysis.get('data', 'N/A'),
            analysis.get('cnpj', 'N/A'),
            analysis.get('empresa', 'N/A'),
            result.get('extracted_text', ''),
            json.dumps(logos)
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    def get_all_analyses(self):
        """
        Retorna todas as análises armazenadas
        
        Returns:
            list: Lista de dicionários com as análises
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analyses 
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in rows:
            analyses.append({
                'id': row['id'],
                'filename': row['filename'],
                'valor': row['valor'],
                'categoria': row['categoria'],
                'data_documento': row['data_documento'],
                'cnpj': row['cnpj'],
                'empresa': row['empresa'],
                'extracted_text': row['extracted_text'],
                'logos': json.loads(row['logos']) if row['logos'] else [],
                'created_at': row['created_at']
            })
        
        return analyses
    
    def get_statistics(self):
        """
        Calcula estatísticas gerais dos dados armazenados
        
        Returns:
            dict: Estatísticas com total gasto, categorias, etc.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total gasto
        cursor.execute('SELECT SUM(valor) as total FROM analyses')
        total_gasto = cursor.fetchone()[0] or 0
        
        # Total de arquivos
        cursor.execute('SELECT COUNT(*) as count FROM analyses')
        total_arquivos = cursor.fetchone()[0] or 0
        
        # Gastos por categoria
        cursor.execute('''
            SELECT categoria, SUM(valor) as total, COUNT(*) as count
            FROM analyses
            GROUP BY categoria
            ORDER BY total DESC
        ''')
        
        categorias = {}
        for row in cursor.fetchall():
            categoria, total, count = row
            categorias[categoria] = {
                'valor': round(total, 2),
                'percentual': round((total / total_gasto * 100) if total_gasto > 0 else 0, 2),
                'count': count
            }
        
        conn.close()
        
        return {
            'total_gasto': round(total_gasto, 2),
            'total_arquivos': total_arquivos,
            'categorias': categorias
        }
    
    def search_analyses(self, query):
        """
        Busca análises por texto (empresa, categoria, CNPJ, etc.)
        
        Args:
            query: Texto de busca
        
        Returns:
            list: Lista de análises que correspondem à busca
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f'%{query}%'
        
        cursor.execute('''
            SELECT * FROM analyses 
            WHERE 
                empresa LIKE ? OR
                categoria LIKE ? OR
                cnpj LIKE ? OR
                filename LIKE ? OR
                extracted_text LIKE ?
            ORDER BY created_at DESC
        ''', (search_term, search_term, search_term, search_term, search_term))
        
        rows = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in rows:
            analyses.append({
                'id': row['id'],
                'filename': row['filename'],
                'valor': row['valor'],
                'categoria': row['categoria'],
                'data_documento': row['data_documento'],
                'cnpj': row['cnpj'],
                'empresa': row['empresa'],
                'extracted_text': row['extracted_text'][:200],
                'logos': json.loads(row['logos']) if row['logos'] else [],
                'created_at': row['created_at']
            })
        
        return analyses
