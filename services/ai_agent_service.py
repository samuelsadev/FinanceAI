import json
from services.bedrock_service import BedrockService

class AIAgentService:
    """Agente de IA para buscar e analisar dados armazenados"""
    
    def __init__(self, bedrock_client, database_service):
        self.bedrock = BedrockService(bedrock_client)
        self.database = database_service
    
    def query(self, user_query):
        """
        Processa uma consulta do usuário e retorna resultados relevantes
        
        Args:
            user_query: Pergunta ou busca do usuário
        
        Returns:
            dict: Resposta do agente com dados encontrados
        """
        # Buscar dados relevantes no banco
        all_analyses = self.database.get_all_analyses()
        statistics = self.database.get_statistics()
        
        # Preparar contexto para o agente
        context = self._prepare_context(all_analyses, statistics)
        
        # Criar prompt para o Claude
        prompt = self._create_agent_prompt(user_query, context)
        
        # Obter resposta do Claude
        response = self._get_claude_response(prompt)
        
        # Buscar dados específicos se necessário
        search_results = self.database.search_analyses(user_query)
        
        return {
            'answer': response,
            'search_results': search_results[:10],  # Limitar a 10 resultados
            'statistics': statistics,
            'query': user_query
        }
    
    def _prepare_context(self, analyses, statistics):
        """Prepara contexto resumido dos dados"""
        from datetime import datetime
        from collections import defaultdict
        
        # Agrupar gastos por ano
        gastos_por_ano = defaultdict(lambda: {'total': 0, 'count': 0, 'categorias': defaultdict(float)})
        
        for analysis in analyses:
            try:
                # Extrair ano da data do documento
                data_parts = analysis['data_documento'].split('/')
                if len(data_parts) == 3:
                    ano = data_parts[2]
                    valor = analysis['valor']
                    categoria = analysis['categoria']
                    
                    gastos_por_ano[ano]['total'] += valor
                    gastos_por_ano[ano]['count'] += 1
                    gastos_por_ano[ano]['categorias'][categoria] += valor
            except:
                pass
        
        context = {
            'total_gasto': statistics['total_gasto'],
            'total_arquivos': statistics['total_arquivos'],
            'categorias': statistics['categorias'],
            'gastos_por_ano': dict(gastos_por_ano),
            'ultimos_registros': []
        }
        
        # Adicionar últimos 50 registros (aumentado de 20)
        for analysis in analyses[:50]:
            context['ultimos_registros'].append({
                'empresa': analysis['empresa'],
                'valor': analysis['valor'],
                'categoria': analysis['categoria'],
                'data': analysis['data_documento']
            })
        
        return context
    
    def _create_agent_prompt(self, user_query, context):
        """Cria prompt para o agente de IA"""
        prompt = f"""Você é um assistente financeiro inteligente que ajuda usuários a analisar seus gastos.

DADOS DISPONÍVEIS:
- Total gasto (todos os períodos): R$ {context['total_gasto']:.2f}
- Total de arquivos: {context['total_arquivos']}
- Categorias: {', '.join(context['categorias'].keys())}

GASTOS POR ANO:
"""
        # Adicionar informações por ano
        for ano, dados in sorted(context['gastos_por_ano'].items(), reverse=True):
            prompt += f"\n📅 Ano {ano}:\n"
            prompt += f"   Total: R$ {dados['total']:.2f}\n"
            prompt += f"   Documentos: {dados['count']}\n"
            if dados['categorias']:
                prompt += f"   Categorias:\n"
                for cat, valor in sorted(dados['categorias'].items(), key=lambda x: x[1], reverse=True):
                    prompt += f"      - {cat}: R$ {valor:.2f}\n"
        
        prompt += f"""
GASTOS POR CATEGORIA (GERAL):
"""
        for cat, data in context['categorias'].items():
            prompt += f"- {cat}: R$ {data['valor']:.2f} ({data['percentual']:.1f}%) - {data['count']} registros\n"
        
        prompt += f"""
ÚLTIMOS REGISTROS (com datas):
"""
        for i, reg in enumerate(context['ultimos_registros'][:20], 1):
            prompt += f"{i}. {reg['data']} - {reg['empresa']} - {reg['categoria']} - R$ {reg['valor']:.2f}\n"
        
        prompt += f"""

PERGUNTA DO USUÁRIO: {user_query}

INSTRUÇÕES:
1. Analise a pergunta do usuário cuidadosamente
2. Use os dados fornecidos acima para responder
3. Se a pergunta mencionar um ano específico (como 2025, 2024, etc), use os dados de "GASTOS POR ANO"
4. Seja específico e objetivo com números exatos
5. Se a pergunta for sobre valores, forneça números exatos com R$
6. Se a pergunta for sobre categorias, liste as relevantes
7. Responda em português brasileiro
8. Use formatação clara e organizada
9. IMPORTANTE: Os dados incluem informações de diferentes anos - verifique o ano mencionado na pergunta

RESPOSTA:"""
        
        return prompt
    
    def _get_claude_response(self, prompt):
        """Obtém resposta do Claude via Bedrock"""
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.bedrock.client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return f"Desculpe, não consegui processar sua pergunta. Erro: {str(e)}"
