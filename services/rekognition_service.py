class RekognitionService:
    def __init__(self, rekognition_client):
        self.client = rekognition_client
    
    def detect_logos(self, file_bytes):
        """Detecta logos e marcas em imagens usando AWS Rekognition"""
        try:
            response = self.client.detect_labels(
                Image={'Bytes': file_bytes},
                MaxLabels=20,
                MinConfidence=60
            )
            
            logos = []
            brands = []
            
            # Procurar por logos e marcas
            for label in response['Labels']:
                label_name = label['Name']
                confidence = round(label['Confidence'], 2)
                
                # Detectar logos, marcas, texto, símbolos
                if any(keyword in label_name.lower() for keyword in ['logo', 'brand', 'text', 'symbol', 'trademark']):
                    logos.append({
                        'name': label_name,
                        'confidence': confidence
                    })
                # Também capturar categorias que podem indicar a empresa
                elif any(keyword in label_name.lower() for keyword in ['company', 'business', 'store', 'shop']):
                    brands.append({
                        'name': label_name,
                        'confidence': confidence
                    })
            
            # Se encontrou logos específicos, retornar
            if logos:
                return logos
            
            # Se não encontrou logos mas encontrou marcas, retornar marcas
            if brands:
                return brands
            
            # Tentar detectar texto que pode conter nome da empresa
            text_response = self.detect_text(file_bytes)
            if text_response:
                # Pegar as primeiras linhas de texto (geralmente contém o nome da empresa)
                top_texts = text_response[:3]
                if top_texts:
                    return [{
                        'name': f"Texto detectado: {text['text'][:30]}...",
                        'confidence': text['confidence']
                    } for text in top_texts]
            
            # Se nada foi encontrado
            return [{"name": "Nenhuma logo ou marca detectada", "confidence": 0}]
            
        except Exception as e:
            print(f"Erro no Rekognition: {str(e)}")
            return [{"name": f"Erro ao detectar: {str(e)}", "confidence": 0}]
    
    def detect_text(self, file_bytes):
        """Detecta texto em imagens"""
        try:
            response = self.client.detect_text(
                Image={'Bytes': file_bytes}
            )
            
            detected_text = []
            for text_detection in response['TextDetections']:
                if text_detection['Type'] == 'LINE':
                    detected_text.append({
                        'text': text_detection['DetectedText'],
                        'confidence': round(text_detection['Confidence'], 2)
                    })
            
            return detected_text
        except Exception as e:
            print(f"Erro ao detectar texto: {str(e)}")
            return []
    
    def analyze_document(self, file_bytes):
        """Análise completa do documento"""
        try:
            logos = self.detect_logos(file_bytes)
            text = self.detect_text(file_bytes)
            
            return {
                'logos': logos,
                'text': text
            }
        except Exception as e:
            print(f"Erro na análise do documento: {str(e)}")
            return {
                'logos': [],
                'text': []
            }
