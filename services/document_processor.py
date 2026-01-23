from services.textract_service import TextractService
from services.rekognition_service import RekognitionService
from services.bedrock_service import BedrockService

class DocumentProcessor:
    def __init__(self, aws_service):
        self.textract = TextractService(aws_service.textract_client)
        self.rekognition = RekognitionService(aws_service.rekognition_client)
        self.bedrock = BedrockService(aws_service.bedrock_client)
    
    def process_file(self, file_path, filename):
        """Processa um arquivo individual"""
        try:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            print(f"Processando arquivo: {filename}")
            
            # Extração de texto com Textract
            extracted_text = self.textract.extract_text(file_bytes)
            print(f"✓ Texto extraído: {len(extracted_text)} caracteres")
            
            # Detecção de logos com Rekognition
            logos = self.rekognition.detect_logos(file_bytes)
            print(f"✓ Logos detectados: {len(logos)}")
            
            # Análise com Bedrock
            analysis = self.bedrock.analyze_expense(extracted_text)
            print(f"✓ Análise concluída: R$ {analysis['valor']} - {analysis['categoria']}")
            
            return {
                "filename": filename,
                "extracted_text": extracted_text[:500],  # Primeiros 500 caracteres
                "logos": logos,  # Retornar objetos completos com name e confidence
                "analysis": analysis,
                "success": True
            }
        except Exception as e:
            print(f"✗ Erro ao processar {filename}: {str(e)}")
            return {
                "filename": filename,
                "error": str(e),
                "success": False
            }
    
    def process_multiple_files(self, file_paths_and_names):
        """Processa múltiplos arquivos"""
        results = []
        
        for file_path, filename in file_paths_and_names:
            result = self.process_file(file_path, filename)
            results.append(result)
        
        return results
    
    def calculate_statistics(self, results):
        """Calcula estatísticas dos gastos"""
        total_gasto = 0
        categorias = {}
        
        for result in results:
            if result.get('success') and 'analysis' in result:
                try:
                    valor = float(result['analysis']['valor'])
                    total_gasto += valor
                    
                    categoria = result['analysis']['categoria']
                    if categoria in categorias:
                        categorias[categoria] += valor
                    else:
                        categorias[categoria] = valor
                except Exception as e:
                    print(f"Erro ao calcular estatísticas: {str(e)}")
        
        # Calcular porcentagens
        categoria_percentual = {}
        if total_gasto > 0:
            for cat, val in categorias.items():
                categoria_percentual[cat] = {
                    "valor": round(val, 2),
                    "percentual": round((val / total_gasto) * 100, 2)
                }
        
        return {
            "total_gasto": round(total_gasto, 2),
            "categorias": categoria_percentual,
            "total_arquivos": len(results),
            "arquivos_processados": sum(1 for r in results if r.get('success'))
        }
