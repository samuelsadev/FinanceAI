# 📁 Estrutura de Arquivos Estáticos

Esta pasta contém todos os arquivos estáticos (CSS e JavaScript) da aplicação, organizados de forma modular e funcional.

## 📂 Estrutura

```
static/
├── css/
│   └── styles.css          # Estilos globais da aplicação
└── js/
    ├── config.js           # Configurações e constantes
    ├── charts.js           # Gerenciamento de gráficos
    ├── fileUpload.js       # Upload e processamento de arquivos
    └── app.js              # Aplicação principal
```

## 🎨 CSS (styles.css)

Organizado em seções:
- **Reset e Configurações Globais**: Estilos base
- **Layout Principal**: Grid e estrutura
- **Componentes**: Cards, botões, legendas
- **Upload Section**: Área de upload de arquivos
- **Results Section**: Exibição de resultados
- **Loading**: Spinner e estados de carregamento
- **Responsivo**: Media queries para diferentes telas

## 📜 JavaScript

### config.js
Contém todas as configurações e constantes:
- `CATEGORY_COLORS`: Cores das categorias
- `CATEGORY_ICONS`: Ícones das categorias
- `CHART_CONFIG`: Configurações dos gráficos
- `API_ENDPOINTS`: Endpoints da API

### charts.js
Classe `ChartManager` responsável por:
- `renderPieChart()`: Renderiza gráfico de pizza
- `renderBarChart()`: Renderiza gráfico de barras
- `renderLegend()`: Renderiza legenda customizada
- `renderAll()`: Renderiza todos os gráficos
- `destroy()`: Limpa os gráficos

### fileUpload.js
Classe `FileUploadManager` responsável por:
- `handleFileSelect()`: Gerencia seleção de arquivos
- `displaySelectedFiles()`: Exibe arquivos selecionados
- `processFiles()`: Envia arquivos para processamento
- `displayResults()`: Exibe resultados do processamento
- `displayDetails()`: Exibe detalhes de cada arquivo
- `showError()`: Exibe mensagens de erro

### app.js
Classe `App` principal que:
- `init()`: Inicializa a aplicação
- `checkHealth()`: Verifica status da API
- `setupEventListeners()`: Configura eventos globais
- Métodos utilitários: `formatCurrency()`, `formatDate()`, `capitalize()`

## 🔄 Fluxo de Execução

1. **Carregamento da Página**
   - `config.js` carrega constantes
   - `charts.js` inicializa ChartManager
   - `fileUpload.js` inicializa FileUploadManager
   - `app.js` inicializa App e verifica saúde da API

2. **Seleção de Arquivos**
   - Usuário seleciona arquivos
   - `FileUploadManager.handleFileSelect()` processa
   - Arquivos são exibidos na tela

3. **Processamento**
   - Usuário clica em "Processar"
   - `FileUploadManager.processFiles()` envia para API
   - Loading é exibido

4. **Exibição de Resultados**
   - API retorna dados processados
   - `ChartManager.renderAll()` renderiza gráficos
   - `FileUploadManager.displayDetails()` exibe detalhes

## 🎯 Benefícios da Organização

- ✅ **Modularidade**: Cada arquivo tem responsabilidade única
- ✅ **Manutenibilidade**: Fácil localizar e modificar código
- ✅ **Reutilização**: Classes podem ser reutilizadas
- ✅ **Testabilidade**: Funções isoladas são mais fáceis de testar
- ✅ **Escalabilidade**: Fácil adicionar novas funcionalidades
- ✅ **Legibilidade**: Código organizado e documentado

## 🔧 Como Adicionar Novas Funcionalidades

### Adicionar Nova Categoria
1. Edite `config.js`:
   - Adicione cor em `CATEGORY_COLORS`
   - Adicione ícone em `CATEGORY_ICONS`

### Adicionar Novo Gráfico
1. Edite `charts.js`:
   - Crie novo método na classe `ChartManager`
   - Adicione chamada em `renderAll()`

### Adicionar Nova Funcionalidade de Upload
1. Edite `fileUpload.js`:
   - Adicione novo método na classe `FileUploadManager`
   - Configure event listeners necessários

## 📝 Convenções de Código

- **Nomes de Classes**: PascalCase (ex: `ChartManager`)
- **Nomes de Métodos**: camelCase (ex: `renderPieChart`)
- **Constantes**: UPPER_SNAKE_CASE (ex: `CATEGORY_COLORS`)
- **Comentários**: Seções delimitadas com `/* === */`
- **JSDoc**: Documentação de métodos com `@param` e `@returns`
