class TextractService:
    def __init__(self, textract_client):
        self.client = textract_client
    
    def extract_text(self, file_bytes):
        """Extrai texto de documentos usando AWS Textract"""
        try:
            response = self.client.detect_document_text(
                Document={'Bytes': file_bytes}
            )
            
            text = ""
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    text += block['Text'] + "\n"
            
            return text
        except Exception as e:
            print(f"Erro no Textract: {str(e)}")
            return ""
    
    def extract_structured_data(self, file_bytes):
        """Extrai dados estruturados como tabelas e formulários"""
        try:
            response = self.client.analyze_document(
                Document={'Bytes': file_bytes},
                FeatureTypes=['TABLES', 'FORMS']
            )
            
            # Extrair key-value pairs
            key_values = {}
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'KEY_VALUE_SET':
                    if 'KEY' in block.get('EntityTypes', []):
                        key_text = self._get_text_from_block(block, response['Blocks'])
                        value_text = self._get_value_from_key(block, response['Blocks'])
                        if key_text and value_text:
                            key_values[key_text] = value_text
            
            return key_values
        except Exception as e:
            print(f"Erro ao extrair dados estruturados: {str(e)}")
            return {}
    
    def _get_text_from_block(self, block, all_blocks):
        """Extrai texto de um bloco"""
        text = ""
        if 'Relationships' in block:
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next((b for b in all_blocks if b['Id'] == child_id), None)
                        if child_block and child_block['BlockType'] == 'WORD':
                            text += child_block['Text'] + " "
        return text.strip()
    
    def _get_value_from_key(self, key_block, all_blocks):
        """Obtém o valor associado a uma chave"""
        if 'Relationships' in key_block:
            for relationship in key_block['Relationships']:
                if relationship['Type'] == 'VALUE':
                    for value_id in relationship['Ids']:
                        value_block = next((b for b in all_blocks if b['Id'] == value_id), None)
                        if value_block:
                            return self._get_text_from_block(value_block, all_blocks)
        return ""
