/* =================================================
   PÁGINA DE HISTÓRICO - JAVASCRIPT
================================================= */

class HistoryPage {
    constructor() {
        this.analyses = [];
        this.statistics = {};
        this.donutChart = null;
        this.barChart = null;
        this.init();
    }

    async init() {
        console.log('🚀 Inicializando página de histórico');
        await this.loadData();
        this.setupEventListeners();
    }

    async loadData() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();

            if (data.success) {
                this.analyses = data.analyses;
                this.statistics = data.statistics;

                this.updateSummaryCards();
                this.renderCharts();
                this.renderTable();
            } else {
                this.showNoData();
            }
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.showNoData();
        }
    }

    updateSummaryCards() {
        document.getElementById('totalGasto').textContent =
            this.formatCurrency(this.statistics.total_gasto);

        document.getElementById('totalArquivos').textContent =
            this.statistics.total_arquivos;

        document.getElementById('totalCategorias').textContent =
            Object.keys(this.statistics.categorias).length;
    }

    /* =================================================
       CHARTS
    ================================================= */

    renderCharts() {
        const categorias = this.statistics.categorias;

        const rawLabels = Object.keys(categorias);
        const values = rawLabels.map(cat => categorias[cat].valor);

        const labels = rawLabels.map(cat => this.formatCategoryLabel(cat));
        const colors = rawLabels.map(cat => this.getCategoryColor(cat));

        this.renderDonutChart(labels, values, colors);
        this.renderBarChart(labels, values, colors);
    }

    renderDonutChart(labels, values, colors) {
        const totalGasto = this.statistics.total_gasto;

        const options = {
            series: values,
            chart: {
                type: 'donut',
                height: 400,
                fontFamily: 'Inter, sans-serif'
            },
            labels: labels,
            colors: colors,
            legend: {
                position: 'bottom',
                fontSize: '14px'
            },
            dataLabels: {
                enabled: true,
                formatter: val => val.toFixed(1) + '%'
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '65%',
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: 'Total',
                                fontSize: '18px',
                                fontWeight: 600,
                                formatter: () =>
                                    'R$ ' + totalGasto.toFixed(2).replace('.', ',')
                            }
                        }
                    }
                }
            },
            tooltip: {
                y: {
                    formatter: val => this.formatCurrency(val)
                }
            }
        };

        if (this.donutChart) this.donutChart.destroy();

        this.donutChart = new ApexCharts(
            document.querySelector("#donutChart"),
            options
        );
        this.donutChart.render();
    }

    renderBarChart(labels, values, colors) {
        const options = {
            series: [{
                name: 'Valor',
                data: values
            }],
            chart: {
                type: 'bar',
                height: 400,
                fontFamily: 'Inter, sans-serif',
                toolbar: { show: false }
            },
            plotOptions: {
                bar: {
                    borderRadius: 8,
                    distributed: true,
                    columnWidth: '60%'
                }
            },
            colors: colors,
            dataLabels: { enabled: false },
            legend: { show: false },
            xaxis: {
                categories: labels,
                labels: { style: { fontSize: '12px' } }
            },
            yaxis: {
                labels: {
                    formatter: val => 'R$ ' + val.toFixed(0)
                }
            },
            tooltip: {
                y: {
                    formatter: val => this.formatCurrency(val)
                }
            }
        };

        if (this.barChart) this.barChart.destroy();

        this.barChart = new ApexCharts(
            document.querySelector("#barChart"),
            options
        );
        this.barChart.render();
    }

    /* =================================================
       TABELA
    ================================================= */

    renderTable(data = null) {
        const analyses = data || this.analyses;
        const tbody = document.getElementById('tableBody');

        if (analyses.length === 0) {
            this.showNoData();
            return;
        }

        tbody.innerHTML = '';

        analyses.forEach(analysis => {
            const color = this.getCategoryColor(analysis.categoria);
            const label = this.formatCategoryLabel(analysis.categoria);
            const icon = this.getCategoryIcon(analysis.categoria);

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${this.formatDateTime(analysis.created_at)}</td>
                <td>${analysis.filename}</td>
                <td>${analysis.empresa}</td>
                <td>
                    <span class="category-badge"
                          style="background:${color}20;color:${color};border:1px solid ${color}40;">
                        ${icon} ${label}
                    </span>
                </td>
                <td class="valor-cell">${this.formatCurrency(analysis.valor)}</td>
                <td>${analysis.cnpj}</td>
                <td>${analysis.data_documento}</td>
            `;
            tbody.appendChild(row);
        });

        document.getElementById('tableContainer').style.display = 'block';
        document.getElementById('noData').style.display = 'none';
    }

    showNoData() {
        document.getElementById('tableContainer').style.display = 'none';
        document.getElementById('noData').style.display = 'block';
    }

    /* =================================================
       EVENTOS
    ================================================= */

    setupEventListeners() {
        document.getElementById('searchInput')
            .addEventListener('input', e => this.filterTable(e.target.value));

        document.getElementById('aiQueryBtn')
            .addEventListener('click', () => this.askAI());

        document.getElementById('aiQuery')
            .addEventListener('keypress', e => {
                if (e.key === 'Enter') this.askAI();
            });
    }

    filterTable(query) {
        const q = query.toLowerCase();
        const filtered = this.analyses.filter(a =>
            a.empresa.toLowerCase().includes(q) ||
            a.categoria.toLowerCase().includes(q) ||
            a.cnpj.toLowerCase().includes(q) ||
            a.filename.toLowerCase().includes(q)
        );
        this.renderTable(filtered);
    }

    /* =================================================
       AGENTE DE IA
    ================================================= */

    async askAI() {
        const input = document.getElementById('aiQuery');
        const query = input.value.trim();

        if (!query) {
            alert('Por favor, digite uma pergunta');
            return;
        }

        const responseDiv = document.getElementById('aiResponse');
        responseDiv.innerHTML = '<div class="loading">🤔 Pensando...</div>';
        responseDiv.style.display = 'block';

        try {
            const response = await fetch('/api/ai-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();

            if (data.success) {
                responseDiv.innerHTML = `
                    <div class="ai-answer">
                        <strong>💡 Resposta do Assistente:</strong>
                        <p>${data.answer.replace(/\n/g, '<br>')}</p>
                    </div>
                `;
            } else {
                responseDiv.innerHTML = `
                    <div class="ai-error">
                        ❌ Erro: ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Erro ao consultar IA:', error);
            responseDiv.innerHTML = `
                <div class="ai-error">
                    ❌ Erro ao processar sua pergunta. Tente novamente.
                </div>
            `;
        }
    }

    /* =================================================
       UTILITÁRIOS
    ================================================= */

    normalizeCategory(category) {
        return category
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '');
    }

    formatCategoryLabel(category) {
        const map = {
            alimentacao: 'Alimentação',
            transporte: 'Transporte',
            lazer: 'Lazer',
            saude: 'Saúde',
            educacao: 'Educação',
            moradia: 'Moradia',
            transferencia: 'Transferência',
            investimento: 'Investimento',
            outros: 'Outros'
        };
        return map[this.normalizeCategory(category)] || category;
    }

    getCategoryColor(category) {
        const colors = {
            alimentacao: '#19aa20ff',
            transporte: '#1565C0',
            lazer: '#a86604ff',
            saude: '#C62828',
            educacao: '#6A1B9A',
            moradia: '#948a05ff',
            transferencia: '#008679ff',
            investimento: '#263c61ff',
            outros: '#9E9E9E'
        };
        return colors[this.normalizeCategory(category)] || '#9E9E9E';
    }

    getCategoryIcon(category) {
        const icons = {
            alimentacao: '🍔',
            transporte: '🚗',
            lazer: '🎮',
            saude: '💊',
            educacao: '📚',
            moradia: '🏠',
            transferencia: '💸',
            investimento: '📈',
            outros: '📦'
        };
        return icons[this.normalizeCategory(category)] || '📦';
    }

    formatCurrency(value) {
        return 'R$ ' + value.toFixed(2).replace('.', ',');
    }

    formatDateTime(dateString) {
        const d = new Date(dateString);
        return d.toLocaleDateString('pt-BR') + ' ' +
               d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }
}

/* =================================================
   INIT
================================================= */

document.addEventListener('DOMContentLoaded', () => {
    new HistoryPage();
});
