# 📊 FinanceAI - Análise Inteligente de Gastos

> Plataforma completa para análise automatizada de notas fiscais e comprovantes usando AWS AI Services, com banco de dados persistente, histórico detalhado e assistente financeiro inteligente.

## ✨ Funcionalidades Principais

### 📤 Processamento de Documentos
- **Upload Múltiplo**: Processe vários documentos simultaneamente (PDF, JPG, PNG, DOC, DOCX)
- **Extração Inteligente**: AWS Textract extrai valores, CNPJ e datas automaticamente
- **Detecção de Logos**: AWS Rekognition identifica logos de empresas nos documentos
- **Classificação com IA**: AWS Bedrock (Claude 3 Haiku) classifica gastos por categoria
- **Dashboard Visual**: Gráfico interativo com distribuição de gastos por categoria

### 💾 Banco de Dados e Persistência
- **SQLite Persistente**: Armazena todas as análises com dados completos
- **Arquitetura Multi-Container**: Banco de dados isolado em container separado
- **Volume Docker**: Dados persistem mesmo após reinicialização dos containers
- **Scripts de Gerenciamento**: Backup, restauração e estatísticas do banco

### 📊 Histórico e Análise
- **Página de Histórico Completa**: Visualize todos os dados armazenados
- **Cards de Resumo**: Total gasto, arquivos enviados e categorias
- **Gráfico de Rosca (Donut)**: Distribuição percentual por categoria com total no centro
- **Gráfico de Barras**: Valores absolutos por categoria
- **Tabela Detalhada**: Todos os registros com data, empresa, categoria, valor e CNPJ
- **Busca em Tempo Real**: Filtre por empresa, categoria, CNPJ ou qualquer texto

### 🤖 Assistente Financeiro IA
- **Consultas Inteligentes**: Faça perguntas em linguagem natural sobre seus gastos
- **Análise por Período**: "Quanto gastei em 2025?", "Qual meu maior gasto?"
- **Análise por Categoria**: "Quanto gastei em alimentação?", "Qual categoria mais cara?"
- **Contexto Temporal**: Agrupamento automático por ano e categoria
- **Respostas Detalhadas**: Valores exatos, percentuais e insights relevantes

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Conta AWS com acesso aos serviços:
  - AWS Textract
  - AWS Rekognition
  - AWS Bedrock (Claude 3 Haiku)
- Credenciais AWS (Access Key e Secret Key)

## 🚀 Início Rápido

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/financeai.git
cd financeai
```

### 2. Configure as credenciais AWS

Copie o arquivo de exemplo e adicione suas credenciais:

```bash
cp .env.docker.example .env.docker
```

Edite o arquivo `.env.docker` com suas credenciais:

```env
AWS_ACCESS_KEY_ID=sua_access_key_aqui
AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
AWS_REGION=us-east-1
PORT=5080
```

### 3. Execute com Docker (Recomendado)

#### Opção 1: Usando scripts PowerShell (Windows)

```powershell
# Iniciar aplicação
.\docker-start.ps1

# Ver logs
.\docker-logs.ps1

# Parar aplicação
.\docker-stop.ps1
```

#### Opção 2: Comandos Docker diretos

```bash
# Build e start
docker-compose up --build -d

# Ver logs
docker-compose logs -f app

# Parar
docker-compose down
```

A aplicação estará disponível em: **http://localhost:5080**

### 4. Acesse a aplicação

1. **Página Principal**: http://localhost:5080
   - Upload e análise de documentos
   - Dashboard com resumo financeiro

2. **Página de Histórico**: http://localhost:5080/history
   - Visualização de todos os dados
   - Gráficos interativos
   - Assistente financeiro IA

## 🎯 Como Usar

### 📤 Análise de Documentos
1. Acesse http://localhost:5080 no navegador
2. Clique em **"Escolher Arquivos"** e selecione suas notas fiscais/comprovantes
3. Clique em **"Processar Documentos"**
4. Aguarde a análise (pode levar alguns segundos por documento)
5. Visualize o resumo financeiro completo com:
   - 💰 Total gasto
   - 📊 Gráfico de distribuição por categoria
   - 📋 Detalhes de cada documento processado

### 📊 Histórico e Análise de Dados
1. Clique no botão **"📊 Ver Histórico"** no topo da página
2. Visualize os **cards de resumo**:
   - 💵 Total gasto acumulado
   - 📁 Quantidade de arquivos enviados
   - 🏷️ Número de categorias diferentes
3. Analise os **gráficos interativos**:
   - 🍩 **Gráfico de Rosca**: Distribuição percentual com total no centro
   - 📊 **Gráfico de Barras**: Valores absolutos por categoria
4. Use a **tabela de registros**:
   - 🔍 Busca em tempo real por empresa, categoria ou CNPJ
   - 📅 Ordenação por data
   - 💳 Detalhes completos de cada transação

### 🤖 Assistente Financeiro IA
1. Na página de histórico, localize a seção **"Assistente Financeiro IA"**
2. Digite perguntas em linguagem natural, como:
   - "Quanto gastei em 2025?"
   - "Qual foi meu maior gasto?"
   - "Quanto gastei em alimentação?"
   - "Qual categoria tem mais gastos?"
   - "Mostre os gastos de dezembro"
3. Clique em **"🔍 Perguntar"** ou pressione Enter
4. Receba respostas inteligentes com:
   - 💡 Análise detalhada dos seus gastos
   - 📈 Valores exatos e percentuais
   - 📊 Comparações entre categorias e períodos

### 🗄️ Gerenciamento do Banco de Dados

#### Scripts PowerShell (Windows)
```powershell
# Fazer backup do banco
.\database-backup.ps1

# Ver estatísticas
.\database-stats.ps1
```

#### Scripts Bash (Linux/Mac)
```bash
# Fazer backup do banco
./database-backup.sh

# Restaurar backup
./database-restore.sh backup_20250123_120000.db

# Acessar shell SQLite
./database-shell.sh

# Ver estatísticas
./database-stats.sh
```

## 🏗️ Arquitetura

### Multi-Container Docker

O projeto utiliza uma arquitetura moderna com **2 containers isolados**:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  (financeai-network)                     │
│                                                          │
│  ┌──────────────────────┐    ┌────────────────────────┐ │
│  │  financeai-app       │    │  financeai-database    │ │
│  │  (Flask API)         │◄───┤  (SQLite)              │ │
│  │  Port: 5080          │    │  Volume: database-vol  │ │
│  └──────────────────────┘    └────────────────────────┘ │
│           │                                              │
└───────────┼──────────────────────────────────────────────┘
            │
            ▼
      http://localhost:5080
```

**Benefícios:**
- ✅ **Isolamento**: Banco de dados separado da aplicação
- ✅ **Persistência**: Dados mantidos em volume Docker
- ✅ **Segurança**: Comunicação interna via rede Docker
- ✅ **Escalabilidade**: Fácil adicionar novos serviços

Veja detalhes completos em: [`ARQUITETURA_MULTI_CONTAINER.md`](ARQUITETURA_MULTI_CONTAINER.md)

### Estrutura do Projeto

```
financeai/
├── 📱 app.py                      # Backend Flask (rotas e endpoints)
├── 🔧 services/                   # Camada de serviços
│   ├── __init__.py
│   ├── aws_service.py            # Inicialização dos clientes AWS
│   ├── textract_service.py       # Extração de texto (AWS Textract)
│   ├── rekognition_service.py    # Detecção de logos (AWS Rekognition)
│   ├── bedrock_service.py        # Análise com IA (AWS Bedrock)
│   ├── document_processor.py     # Orquestrador de processamento
│   ├── database_service.py       # Gerenciamento do banco SQLite
│   └── ai_agent_service.py       # Agente de IA para consultas
├── 🎨 templates/
│   ├── index.html                # Página principal (upload)
│   └── history.html              # Página de histórico
├── � static/
│   ├── css/
│   │   ├── styles.css            # Estilos principais
│   │   └── history.css           # Estilos do histórico
│   └── js/
│       ├── app.js                # JavaScript principal
│       ├── charts.js             # Módulo de gráficos (ApexCharts)
│       ├── fileUpload.js         # Upload de arquivos
│       ├── config.js             # Configurações e cores
│       └── history.js            # Lógica da página de histórico
├── 💾 data/                       # Banco de dados SQLite
│   └── expenses.db               # Dados persistidos
├── 📤 uploads/                    # Pasta temporária para uploads
├── 🐳 Docker/
│   ├── Dockerfile                # Container da aplicação
│   ├── Dockerfile.database       # Container do banco
│   ├── docker-compose.yml        # Orquestração
│   └── init-database.sh          # Script de inicialização
├── 🛠️ Scripts/
│   ├── docker-start.ps1          # Iniciar containers (Windows)
│   ├── docker-stop.ps1           # Parar containers (Windows)
│   ├── docker-logs.ps1           # Ver logs (Windows)
│   ├── database-backup.ps1       # Backup do banco (Windows)
│   ├── database-backup.sh        # Backup do banco (Linux/Mac)
│   ├── database-restore.sh       # Restaurar backup
│   ├── database-shell.sh         # Acessar shell SQLite
│   └── database-stats.sh         # Estatísticas do banco
├── 📋 requirements.txt            # Dependências Python
├── ⚙️ .env.docker                 # Credenciais AWS (não versionado)
├── 📝 .env.docker.example         # Exemplo de configuração
├── 🚫 .gitignore                  # Arquivos ignorados pelo Git
└── 📖 README.md                   # Este arquivo
```

## 🎨 Categorias de Gastos

O sistema classifica automaticamente os gastos nas seguintes categorias:

| Categoria | Ícone | Exemplos |
|-----------|-------|----------|
| Alimentação | 🍔 | Restaurantes, supermercados, delivery |
| Transporte | � | Combustível, Uber, estacionamento |
| Lazer | � | Cinema, streaming, eventos |
| Saúde | � | Farmácia, consultas, exames |
| Educação | � | Cursos, livros, mensalidades |
| Moradia | 🏠 | Aluguel, condomínio, contas |
| Transferência | � | PIX, TED, DOC |
| Investimento | 📈 | Ações, fundos, renda fixa |
| Outros | 📦 | Demais categorias |

## 🛠️ Tecnologias

### Backend
- **Python 3.11** - Linguagem principal
- **Flask 3.0** - Framework web minimalista e poderoso
- **Boto3 1.34** - SDK oficial da AWS para Python
- **SQLite** - Banco de dados relacional embutido

### Frontend
- **HTML5/CSS3** - Interface responsiva e moderna
- **JavaScript ES6+** - Lógica do cliente
- **ApexCharts 3.x** - Biblioteca de visualização de dados interativa

### AWS Services
- **AWS Bedrock** - Claude 3 Haiku para análise com IA generativa
- **AWS Textract** - Extração de texto e dados estruturados de documentos
- **AWS Rekognition** - Detecção de logos e análise de imagens

### DevOps & Infraestrutura
- **Docker 24+** - Containerização da aplicação
- **Docker Compose** - Orquestração de múltiplos containers
- **Multi-stage builds** - Otimização de imagens Docker

### Bibliotecas Python
```txt
flask==3.0.0
boto3==1.34.34
python-dotenv==1.0.0
Pillow==10.2.0
PyPDF2==3.0.1
werkzeug==3.0.1
requests==2.31.0
```

## 🎨 Categorias de Gastos

O sistema classifica automaticamente os gastos usando IA (Claude 3 Haiku) nas seguintes categorias:

| Categoria | Ícone | Cor | Exemplos |
|-----------|-------|-----|----------|
| **Alimentação** | 🍔 | Verde | Restaurantes, supermercados, delivery, padarias |
| **Transporte** | 🚗 | Azul | Combustível, Uber, estacionamento, pedágio |
| **Lazer** | 🎮 | Laranja | Cinema, streaming, eventos, jogos |
| **Saúde** | 💊 | Vermelho | Farmácia, consultas, exames, plano de saúde |
| **Educação** | 📚 | Roxo | Cursos, livros, mensalidades, material escolar |
| **Moradia** | 🏠 | Dourado | Aluguel, condomínio, água, luz, internet |
| **Transferência** | 💸 | Teal | PIX, TED, DOC, transferências bancárias |
| **Investimento** | 📈 | Azul Escuro | Ações, fundos, renda fixa, criptomoedas |
| **Outros** | 📦 | Cinza | Demais categorias não especificadas |

## 🔒 Segurança e Boas Práticas

### Proteção de Credenciais
- ✅ Arquivo `.env.docker` no `.gitignore` para proteger credenciais AWS
- ✅ Variáveis de ambiente isoladas por container
- ✅ Sem hardcoding de credenciais no código

### Processamento de Arquivos
- ✅ Arquivos processados e removidos automaticamente após análise
- ✅ Limite de 50MB por upload para prevenir abusos
- ✅ Validação rigorosa de tipos de arquivo permitidos
- ✅ Pasta `uploads/` temporária, não persistida

### Banco de Dados
- ✅ SQLite em volume Docker isolado
- ✅ Sem armazenamento de documentos originais
- ✅ Apenas metadados e resultados de análise
- ✅ Scripts de backup automático disponíveis

### Containers
- ✅ Containers isolados com comunicação via rede interna
- ✅ Usuário não-root nos containers
- ✅ Health checks para monitoramento
- ✅ Restart automático em caso de falha

## 📊 API Endpoints

### Principais Rotas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Página principal (upload) |
| `GET` | `/history` | Página de histórico |
| `POST` | `/process` | Processar documentos |
| `GET` | `/api/history` | Obter todos os registros (JSON) |
| `POST` | `/api/ai-query` | Consultar assistente IA |
| `GET` | `/health` | Health check da aplicação |

### Exemplo de Uso da API

```bash
# Health check
curl http://localhost:5080/health

# Obter histórico (JSON)
curl http://localhost:5080/api/history

# Consultar assistente IA
curl -X POST http://localhost:5080/api/ai-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Quanto gastei em alimentação?"}'
```

## 📝 Notas Importantes

### Requisitos AWS
- ✅ Conta AWS ativa com billing configurado
- ✅ Permissões IAM para:
  - `bedrock:InvokeModel` (Claude 3 Haiku)
  - `textract:AnalyzeDocument`
  - `rekognition:DetectLabels`
- ✅ Modelo Claude 3 Haiku habilitado no Bedrock (região us-east-1)

### Formatos Suportados
- **Documentos**: PDF, DOC, DOCX
- **Imagens**: JPG, JPEG, PNG
- **Tamanho máximo**: 50MB por arquivo
- **Upload múltiplo**: Até 10 arquivos simultâneos

### Configurações
- **Porta padrão**: 5080 (configurável via `.env.docker`)
- **Região AWS**: us-east-1 (configurável)
- **Modelo IA**: Claude 3 Haiku (econômico e rápido)
- **Banco de dados**: SQLite (sem configuração necessária)

### Custos AWS Estimados
- **Textract**: ~$1.50 por 1000 páginas
- **Rekognition**: ~$1.00 por 1000 imagens
- **Bedrock (Claude 3 Haiku)**: ~$0.25 por 1M tokens de entrada
- **Estimativa**: ~$0.01-0.05 por documento processado

## 📚 Documentação Adicional

O projeto inclui documentação detalhada em arquivos separados:

- 📖 [`ARQUITETURA_MULTI_CONTAINER.md`](ARQUITETURA_MULTI_CONTAINER.md) - Arquitetura detalhada dos containers
- 🎨 [`GUIA_VISUAL_CORES.md`](GUIA_VISUAL_CORES.md) - Paleta de cores e design system
- 🗄️ [`GUIA_SCRIPTS_DATABASE.md`](GUIA_SCRIPTS_DATABASE.md) - Scripts de gerenciamento do banco
- 🚀 [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md) - Guia de início rápido
- ✅ [`CHECKLIST_PRE_DEPLOY.md`](CHECKLIST_PRE_DEPLOY.md) - Checklist antes do deploy
- 🔧 [`COMANDOS_UTEIS.md`](COMANDOS_UTEIS.md) - Comandos úteis do Docker

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 🐛 Troubleshooting

### Erro de credenciais AWS
**Sintoma**: `Unable to locate credentials` ou `Access Denied`

**Solução**:
```bash
# 1. Verifique se o arquivo .env.docker existe
ls -la .env.docker

# 2. Confirme que as credenciais estão corretas
cat .env.docker

# 3. Reconstrua os containers
docker-compose down
docker-compose up --build -d
```

### Erro ao processar documentos
**Sintoma**: `Error processing document` ou timeout

**Solução**:
- Verifique se os serviços AWS estão habilitados na sua região
- Confirme que o modelo Claude 3 Haiku está disponível no Bedrock
- Teste com um documento menor primeiro
- Verifique os logs: `docker-compose logs -f app`

### Docker não inicia
**Sintoma**: Containers não sobem ou ficam em estado `Restarting`

**Solução**:
```bash
# 1. Pare todos os containers
docker-compose down

# 2. Remova volumes antigos (CUIDADO: apaga dados)
docker-compose down -v

# 3. Reconstrua do zero
docker-compose build --no-cache
docker-compose up -d

# 4. Verifique os logs
docker-compose logs -f
```

### Banco de dados corrompido
**Sintoma**: Erros ao acessar histórico ou salvar dados

**Solução**:
```bash
# 1. Faça backup do banco atual
./database-backup.sh

# 2. Acesse o shell do banco
./database-shell.sh

# 3. Execute verificação de integridade
PRAGMA integrity_check;

# 4. Se necessário, restaure um backup
./database-restore.sh backup_YYYYMMDD_HHMMSS.db
```

### Assistente IA não responde
**Sintoma**: Erro ao fazer perguntas ou respostas vazias

**Solução**:
- Verifique se há dados no banco: acesse `/history`
- Confirme que o modelo Bedrock está acessível
- Verifique os logs: `docker logs financeai-app --tail 50`
- Teste com perguntas simples: "Qual o total gasto?"

### Porta 5080 já em uso
**Sintoma**: `Port 5080 is already allocated`

**Solução**:
```bash
# Opção 1: Pare o serviço que está usando a porta
# Windows
netstat -ano | findstr :5080
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5080
kill -9 <PID>

# Opção 2: Altere a porta no .env.docker
PORT=5081
docker-compose up -d
```

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique a seção de [Troubleshooting](#-troubleshooting)
2. Consulte a [documentação da AWS](https://docs.aws.amazon.com/)
3. Abra uma [issue](../../issues) neste repositório

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e demonstração de integração com AWS AI Services.

---



## 🤝 Contribuindo

Contribuições são muito bem-vindas! Este projeto está aberto para melhorias e novas funcionalidades.

### Como Contribuir

1. **Fork o projeto**
2. **Clone seu fork**: `git clone https://github.com/seu-usuario/financeai.git`
3. **Crie uma branch**: `git checkout -b feature/MinhaNovaFeature`
4. **Commit suas alterações**: `git commit -m 'feat: Adiciona MinhaNovaFeature'`
5. **Push para a branch**: `git push origin feature/MinhaNovaFeature`
6. **Abra um Pull Request**

### Padrões de Commit

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Formatação
- `refactor:` Refatoração de código
- `test:` Testes
- `chore:` Manutenção

### Ideias para Contribuição

- 🌐 Suporte a múltiplos idiomas
- 📧 Notificações por email
- 📱 Versão mobile responsiva
- 📊 Mais tipos de gráficos
- 🔐 Autenticação de usuários
- 💾 Suporte a PostgreSQL/MySQL
- 📤 Exportação de relatórios (PDF, Excel)
- 🔄 Integração com APIs bancárias
- 🎯 Metas de gastos por categoria

## 📞 Suporte e Contato

### Precisa de Ajuda?

1. 📖 **Documentação**: Leia os arquivos `.md` na raiz do projeto
2. 🐛 **Issues**: [Abra uma issue](../../issues) no GitHub
3. 💬 **Discussões**: Use a aba [Discussions](../../discussions)

### Links Úteis

- [Documentação AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Documentação AWS Textract](https://docs.aws.amazon.com/textract/)
- [Documentação AWS Rekognition](https://docs.aws.amazon.com/rekognition/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

## ⭐ Mostre seu Apoio

Se este projeto foi útil para você:
- ⭐ Dê uma estrela no GitHub
- 🐛 Reporte bugs e sugira melhorias
- 🤝 Contribua com código
- 📢 Compartilhe com outros desenvolvedores

## 📄 Licença

Este projeto está sob a licença MIT. Desenvolvido para fins educacionais e demonstração de integração com AWS AI Services.

---

<div align="center">


[⬆ Voltar ao topo](#-financeai---análise-inteligente-de-gastos)

</div>
