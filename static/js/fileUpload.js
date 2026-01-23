/* =================================================
   MÓDULO DE UPLOAD DE ARQUIVOS
================================================= */

class FileUploadManager {
    constructor() {
        this.selectedFiles = [];
        this.fileInput = null;
        this.processBtn = null;
        this.selectedFilesDiv = null;
        this.loading = null;
        this.results = null;
        
        this.init();
    }

    /**
     * Inicializa os elementos e eventos
     */
    init() {
        // Elementos DOM
        this.fileInput = document.getElementById('fileInput');
        this.processBtn = document.getElementById('processBtn');
        this.selectedFilesDiv = document.getElementById('selectedFiles');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');

        // Event listeners
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        if (this.processBtn) {
            this.processBtn.addEventListener('click', () => this.processFiles());
        }
    }

    /**
     * Manipula a seleção de arquivos
     * @param {Event} e - Evento de mudança
     */
    handleFileSelect(e) {
        this.selectedFiles = Array.from(e.target.files);
        this.displaySelectedFiles();
        this.processBtn.disabled = this.selectedFiles.length === 0;
    }

    /**
     * Exibe os arquivos selecionados
     */
    displaySelectedFiles() {
        if (this.selectedFiles.length === 0) {
            this.selectedFilesDiv.innerHTML = '';
            return;
        }

        this.selectedFilesDiv.innerHTML = '<h4 style="margin-bottom: 10px;">Arquivos Selecionados:</h4>';
        
        this.selectedFiles.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                📄 ${file.name} 
                <span style="color: #666;">(${this.formatFileSize(file.size)})</span>
            `;
            this.selectedFilesDiv.appendChild(fileItem);
        });
    }

    /**
     * Formata o tamanho do arquivo
     * @param {number} bytes - Tamanho em bytes
     * @returns {string} Tamanho formatado
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    /**
     * Processa os arquivos enviados
     */
    async processFiles() {
        if (this.selectedFiles.length === 0) return;

        const formData = new FormData();
        this.selectedFiles.forEach(file => {
            formData.append('files[]', file);
        });

        // UI feedback
        this.processBtn.disabled = true;
        this.loading.style.display = 'block';
        this.results.style.display = 'none';

        try {
            const response = await fetch(API_ENDPOINTS.process, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data);
            } else {
                this.showError(data.error || 'Erro desconhecido ao processar arquivos');
            }
        } catch (error) {
            this.showError('Erro ao processar arquivos: ' + error.message);
        } finally {
            this.loading.style.display = 'none';
            this.processBtn.disabled = false;
        }
    }

    /**
     * Exibe os resultados do processamento
     * @param {Object} data - Dados retornados pela API
     */
    displayResults(data) {
        // Atualizar estatísticas
        document.getElementById('totalFiles').textContent = data.total_arquivos;
        document.getElementById('totalAmount').textContent = 
            `R$ ${data.total_gasto.toFixed(2).replace('.', ',')}`;
        document.getElementById('totalCategories').textContent = 
            Object.keys(data.categorias).length;

        // Renderizar gráficos
        chartManager.renderAll(data.categorias);

        // Exibir detalhes
        this.displayDetails(data.detalhes);

        // Mostrar resultados
        this.results.style.display = 'block';
        this.results.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Exibe os detalhes de cada arquivo processado
     * @param {Array} detalhes - Array com detalhes dos arquivos
     */
    displayDetails(detalhes) {
        const container = document.getElementById('detailsContainer');
        container.innerHTML = '';

        console.log('📊 Detalhes recebidos:', detalhes);

        detalhes.forEach((detalhe, index) => {
            console.log(`📄 Arquivo ${index + 1}:`, detalhe);
            
            if (!detalhe.success) return;

            const analysis = detalhe.analysis || {};
            const categoria = analysis.categoria || 'outros';
            const icon = CATEGORY_ICONS[categoria] || '📦';
            const color = CATEGORY_COLORS[categoria] || '#BCC8C3';
            const instituicao = analysis.instituicao || 'N/A';

            const card = document.createElement('div');
            card.className = 'detail-card';
            card.style.borderLeftColor = color;

            card.innerHTML = `
                <h4>📄 ${detalhe.filename}</h4>
                <span class="category-badge" style="background: ${color}; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 10px 0;">
                    ${icon} ${categoria.charAt(0).toUpperCase() + categoria.slice(1)}
                </span>
                <div class="detail-info">
                    <div class="info-item">
                        <div class="info-label">🏢 Instituição/Comércio</div>
                        <div class="info-value" style="font-weight: bold; color: #0F4F32;">${instituicao}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">💰 Valor</div>
                        <div class="info-value">R$ ${analysis.valor || '0,00'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📅 Data</div>
                        <div class="info-value">${analysis.data || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">🆔 CNPJ</div>
                        <div class="info-value">${analysis.cnpj || 'N/A'}</div>
                    </div>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: white; border-radius: 5px;">
                    <div class="info-label">📝 Descrição</div>
                    <div class="info-value">${analysis.descricao || 'N/A'}</div>
                </div>
                ${detalhe.extracted_text ? `
                <details style="margin-top: 10px;">
                    <summary style="cursor: pointer; padding: 10px; background: #f8faf9; border-radius: 5px; font-weight: bold; color: #0F4F32;">
                        📄 Ver Texto Extraído
                    </summary>
                    <div style="margin-top: 10px; padding: 10px; background: #f8faf9; border-radius: 5px; max-height: 150px; overflow-y: auto;">
                        <div class="info-value" style="font-size: 0.85em; color: #637E72; white-space: pre-wrap;">${detalhe.extracted_text}</div>
                    </div>
                </details>
                ` : ''}
            `;

            container.appendChild(card);
        });
    }

    /**
     * Exibe mensagem de erro
     * @param {string} message - Mensagem de erro
     */
    showError(message) {
        alert('❌ ' + message);
    }
}

// Inicializar quando o DOM estiver pronto
let fileUploadManager;
document.addEventListener('DOMContentLoaded', () => {
    fileUploadManager = new FileUploadManager();
});
