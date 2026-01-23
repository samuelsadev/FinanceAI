from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from services.aws_service import AWSService
from services.document_processor import DocumentProcessor
from services.database_service import DatabaseService
from services.ai_agent_service import AIAgentService

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

# Inicializar serviços
try:
    aws_service = AWSService()
    document_processor = DocumentProcessor(aws_service)
    database_service = DatabaseService()
    ai_agent = AIAgentService(aws_service.bedrock_client, database_service)
    print("✓ Aplicação inicializada com sucesso!")
except Exception as e:
    print(f"✗ Erro ao inicializar aplicação: {str(e)}")
    aws_service = None
    document_processor = None
    database_service = None
    ai_agent = None

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/history')
def history():
    """Página de histórico"""
    return render_template('history.html')

@app.route('/process', methods=['POST'])
def process_files():
    """Processa múltiplos arquivos enviados"""
    if not document_processor:
        return jsonify({
            "success": False,
            "error": "Serviços AWS não inicializados. Verifique as credenciais."
        }), 500
    
    if 'files[]' not in request.files:
        return jsonify({
            "success": False,
            "error": "Nenhum arquivo enviado"
        }), 400
    
    files = request.files.getlist('files[]')
    
    if not files:
        return jsonify({
            "success": False,
            "error": "Nenhum arquivo selecionado"
        }), 400
    
    # Salvar arquivos temporariamente
    file_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_paths.append((filepath, filename))
    
    if not file_paths:
        return jsonify({
            "success": False,
            "error": "Nenhum arquivo válido foi enviado"
        }), 400
    
    # Processar arquivos
    print(f"\n{'='*60}")
    print(f"Processando {len(file_paths)} arquivo(s)...")
    print(f"{'='*60}\n")
    
    results = document_processor.process_multiple_files(file_paths)
    
    # Salvar resultados no banco de dados
    if database_service:
        for result in results:
            if result.get('success'):
                database_service.save_analysis(result)
                print(f"✓ Análise salva no banco: {result['filename']}")
    
    # Remover arquivos temporários
    for filepath, _ in file_paths:
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao remover arquivo {filepath}: {str(e)}")
    
    # Calcular estatísticas
    statistics = document_processor.calculate_statistics(results)
    
    print(f"\n{'='*60}")
    print(f"Processamento concluído!")
    print(f"Total gasto: R$ {statistics['total_gasto']:.2f}")
    print(f"Arquivos processados: {statistics['arquivos_processados']}/{statistics['total_arquivos']}")
    print(f"{'='*60}\n")
    
    return jsonify({
        "success": True,
        "total_arquivos": statistics['total_arquivos'],
        "total_gasto": statistics['total_gasto'],
        "categorias": statistics['categorias'],
        "detalhes": results
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Verifica o status da aplicação"""
    return jsonify({
        "status": "ok",
        "aws_initialized": aws_service is not None,
        "processor_initialized": document_processor is not None,
        "database_initialized": database_service is not None
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Retorna histórico de análises"""
    if not database_service:
        return jsonify({"success": False, "error": "Banco de dados não inicializado"}), 500
    
    try:
        analyses = database_service.get_all_analyses()
        statistics = database_service.get_statistics()
        
        return jsonify({
            "success": True,
            "analyses": analyses,
            "statistics": statistics
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_analyses():
    """Busca análises por texto"""
    if not database_service:
        return jsonify({"success": False, "error": "Banco de dados não inicializado"}), 500
    
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"success": False, "error": "Query vazia"}), 400
    
    try:
        results = database_service.search_analyses(query)
        return jsonify({
            "success": True,
            "results": results,
            "count": len(results)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    """Processa consulta com agente de IA"""
    if not ai_agent:
        return jsonify({"success": False, "error": "Agente de IA não inicializado"}), 500
    
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"success": False, "error": "Query vazia"}), 400
    
    try:
        response = ai_agent.query(query)
        return jsonify({
            "success": True,
            "answer": response.get('answer', ''),
            "search_results": response.get('search_results', []),
            "statistics": response.get('statistics', {})
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Porta configurável via variável de ambiente
    port = int(os.getenv('PORT', 5080))
    
    print("\n" + "="*60)
    print("🚀 Iniciando servidor Flask...")
    print(f"📍 Acesse: http://localhost:{port}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
