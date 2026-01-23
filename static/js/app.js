/* =================================================
   APLICAÇÃO PRINCIPAL
================================================= */

class App {
    constructor() {
        this.init();
    }

    /**
     * Inicializa a aplicação
     */
    init() {
        console.log('🚀 Aplicação inicializada');
        this.checkHealth();
        this.setupEventListeners();
    }

    /**
     * Verifica o status da API
     */
    async checkHealth() {
        try {
            const response = await fetch(API_ENDPOINTS.health);
            const data = await response.json();
            
            if (data.status === 'ok') {
                console.log('✓ API conectada com sucesso');
                console.log('✓ AWS inicializada:', data.aws_initialized);
            } else {
                console.warn('⚠ API com problemas');
            }
        } catch (error) {
            console.error('✗ Erro ao conectar com a API:', error);
        }
    }

    /**
     * Configura event listeners globais
     */
    setupEventListeners() {
        // Prevenir comportamento padrão de drag and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        // Adicionar suporte para drag and drop (futuro)
        // this.setupDragAndDrop();
    }

    /**
     * Previne comportamentos padrão
     * @param {Event} e - Evento
     */
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    /**
     * Formata valor monetário
     * @param {number} value - Valor numérico
     * @returns {string} Valor formatado
     */
    static formatCurrency(value) {
        return 'R$ ' + value.toFixed(2).replace('.', ',');
    }

    /**
     * Formata data
     * @param {string} dateString - String de data
     * @returns {string} Data formatada
     */
    static formatDate(dateString) {
        if (!dateString || dateString === 'N/A') return 'N/A';
        
        try {
            const [day, month, year] = dateString.split('/');
            return `${day}/${month}/${year}`;
        } catch {
            return dateString;
        }
    }

    /**
     * Capitaliza primeira letra
     * @param {string} str - String
     * @returns {string} String capitalizada
     */
    static capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Inicializar aplicação quando o DOM estiver pronto
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new App();
});
