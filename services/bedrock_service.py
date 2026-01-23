import json

class BedrockService:
    def __init__(self, bedrock_client):
        self.client = bedrock_client
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
    
    def analyze_expense(self, extracted_text):
        """Analisa texto extraído e classifica gastos usando AWS Bedrock"""
        try:
            prompt = f"""Analise o seguinte texto extraído de uma nota fiscal ou comprovante:

{extracted_text}

Por favor, forneça:
1. Valor total gasto (em R$, apenas números com ponto decimal, exemplo: 150.50)
2. Categoria do gasto (escolha UMA das opções: alimentacao, transporte, lazer, saude, educacao, moradia, transferencia, investimento, outros)
3. Data da transação (formato dd/mm/aaaa, se não encontrar use "N/A")
4. CNPJ ou identificação da empresa (se disponível, senão use "N/A")
5. Nome da instituição/comércio/empresa onde foi feito o pagamento ou transferência (extraia do texto, se não encontrar use "N/A")
6. Descrição resumida do gasto (máximo 100 caracteres)

IMPORTANTE sobre categorias:
- Use "transferencia" para: PIX, TED, DOC, transferências bancárias de qualquer tipo
- Use "investimento" para: aplicações financeiras, investimentos, aportes em fundos, ações, renda fixa, etc.

IMPORTANTE: Responda APENAS com um JSON válido, sem texto adicional antes ou depois:
{{
    "valor": "0.00",
    "categoria": "categoria",
    "data": "dd/mm/aaaa",
    "cnpj": "cnpj ou N/A",
    "instituicao": "nome da empresa/comércio",
    "descricao": "descrição breve"
}}"""

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            # Extrair JSON da resposta
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                analysis = json.loads(json_str)
                
                # Validar e normalizar dados
                return self._validate_analysis(analysis)
            
            return self._default_analysis()
            
        except Exception as e:
            print(f"Erro no Bedrock: {str(e)}")
            return self._default_analysis()
    
    def _validate_analysis(self, analysis):
        """Valida e normaliza os dados da análise"""
        try:
            # Garantir que valor seja float
            valor_str = str(analysis.get('valor', '0.00')).replace(',', '.')
            valor = float(valor_str)
            
            # Validar categoria
            categorias_validas = ['alimentacao', 'transporte', 'lazer', 'saude', 'educacao', 'moradia', 'transferencia', 'investimento', 'outros']
            categoria = analysis.get('categoria', 'outros').lower()
            if categoria not in categorias_validas:
                categoria = 'outros'
            
            return {
                'valor': f"{valor:.2f}",
                'categoria': categoria,
                'data': analysis.get('data', 'N/A'),
                'cnpj': analysis.get('cnpj', 'N/A'),
                'instituicao': analysis.get('instituicao', 'N/A'),
                'descricao': analysis.get('descricao', 'Sem descrição')[:100]
            }
        except Exception as e:
            print(f"Erro ao validar análise: {str(e)}")
            return self._default_analysis()
    
    def _default_analysis(self):
        """Retorna análise padrão em caso de erro"""
        return {
            "valor": "0.00",
            "categoria": "outros",
            "data": "N/A",
            "cnpj": "N/A",
            "instituicao": "N/A",
            "descricao": "Não foi possível analisar o documento"
        }
    
    def generate_summary(self, all_expenses):
        """Gera um resumo geral de todos os gastos"""
        try:
            total = sum(float(exp['analysis']['valor']) for exp in all_expenses if 'analysis' in exp)
            
            prompt = f"""Com base nos seguintes gastos totalizando R$ {total:.2f}, gere um resumo financeiro inteligente:

{json.dumps(all_expenses, indent=2, ensure_ascii=False)}

Forneça insights sobre:
1. Principais categorias de gasto
2. Recomendações de economia
3. Padrões identificados

Responda em português, de forma clara e objetiva (máximo 200 palavras)."""

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            summary = response_body['content'][0]['text']
            
            return summary
            
        except Exception as e:
            print(f"Erro ao gerar resumo: {str(e)}")
            return "Não foi possível gerar o resumo dos gastos."
