import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class AWSService:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.textract_client = None
        self.rekognition_client = None
        self.bedrock_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializa os clientes AWS"""
        try:
            self.textract_client = boto3.client('textract', region_name=self.region)
            self.rekognition_client = boto3.client('rekognition', region_name=self.region)
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=self.region)
            print(f"✓ Clientes AWS inicializados com sucesso na região {self.region}")
        except Exception as e:
            print(f"✗ Erro ao inicializar clientes AWS: {str(e)}")
            raise
