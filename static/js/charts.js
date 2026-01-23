/* =================================================
   MÓDULO DE GRÁFICOS
================================================= */

class ChartManager {
    constructor() {
        this.pieChart = null;
        this.barChart = null;
    }

    /**
     * Renderiza o gráfico de rosca (donut)
     * @param {Object} categorias - Dados das categorias
     */
    renderPieChart(categorias) {
        const labels = Object.keys(categorias).map(
            c => c.charAt(0).toUpperCase() + c.slice(1)
        );

        const values = Object.values(categorias).map(c => c.valor);
        const colors = Object.keys(categorias).map(c => CATEGORY_COLORS[c] || '#BCC8C3');

        const options = {
            chart: {
                type: 'donut', // ✅ trocado de pie para donut
                width: CHART_CONFIG.pie.width,
                height: CHART_CONFIG.pie.height,
                animations: {
                    enabled: true,
                    easing: 'easeinout',
                    speed: 800
                }
            },
            labels: labels,
            series: values,
            colors: colors,
            legend: {
                show: false
            },
            dataLabels: CHART_CONFIG.pie.dataLabels,
            tooltip: {
                y: {
                    formatter: (val) => 'R$ ' + val.toFixed(2).replace('.', ',')
                }
            },

            // ✅ Configuração do donut (rosca)
            plotOptions: {
                pie: {
                    donut: {
                        size: '68%', // ajuste: 60% (mais grosso) | 75% (mais fino)
                        labels: {
                            show: true,
                            name: {
                                show: true
                            },
                            value: {
                                show: true,
                                formatter: (val) =>
                                    'R$ ' + Number(val).toFixed(2).replace('.', ',')
                            },
                            total: {
                                show: true,
                                label: 'Total',
                                formatter: () => {
                                    const total = values.reduce((acc, v) => acc + v, 0);
                                    return 'R$ ' + total.toFixed(2).replace('.', ',');
                                }
                            }
                        }
                    }
                }
            },

            responsive: [{
                breakpoint: 600,
                options: {
                    chart: {
                        width: 220,
                        height: 220
                    },
                    plotOptions: {
                        pie: {
                            donut: {
                                size: '72%'
                            }
                        }
                    }
                }
            }]
        };

        // Destruir gráfico anterior se existir
        if (this.pieChart) {
            this.pieChart.destroy();
        }

        // Criar novo gráfico
        this.pieChart = new ApexCharts(
            document.querySelector("#pieChart"),
            options
        );

        this.pieChart.render();
    }

    /**
     * Renderiza o gráfico de barras
     * @param {Object} categorias - Dados das categorias
     */
    renderBarChart(categorias) {
        const labels = Object.keys(categorias).map(c => {
            const icon = CATEGORY_ICONS[c] || '📦';
            const name = c.charAt(0).toUpperCase() + c.slice(1);
            return `${icon} ${name}`;
        });

        const values = Object.values(categorias).map(c => c.valor);
        const colors = Object.keys(categorias).map(c => CATEGORY_COLORS[c] || '#BCC8C3');

        const options = {
            chart: {
                type: 'bar',
                height: CHART_CONFIG.bar.height,
                toolbar: CHART_CONFIG.bar.toolbar,
                animations: {
                    enabled: true,
                    easing: 'easeinout',
                    speed: 800
                }
            },
            series: [{
                name: 'Valor Gasto',
                data: values
            }],
            xaxis: {
                categories: labels,
                labels: {
                    style: {
                        fontSize: '13px'
                    }
                }
            },
            yaxis: {
                labels: {
                    formatter: (val) => 'R$ ' + val.toFixed(2)
                }
            },
            colors: colors,
            plotOptions: {
                bar: {
                    borderRadius: 8,
                    distributed: true,
                    horizontal: false
                }
            },
            dataLabels: {
                enabled: false
            },
            tooltip: {
                y: {
                    formatter: (val) => 'R$ ' + val.toFixed(2).replace('.', ',')
                }
            },
            legend: {
                show: false
            }
        };

        // Destruir gráfico anterior se existir
        if (this.barChart) {
            this.barChart.destroy();
        }

        // Criar novo gráfico
        this.barChart = new ApexCharts(
            document.querySelector("#barChart"),
            options
        );

        this.barChart.render();
    }

    /**
     * Renderiza a legenda customizada
     * @param {Object} categorias - Dados das categorias
     */
    renderLegend(categorias) {
        const legend = document.getElementById('legend');
        legend.innerHTML = '';

        Object.entries(categorias).forEach(([nome, dados]) => {
            const icon = CATEGORY_ICONS[nome] || '📦';
            const color = CATEGORY_COLORS[nome] || '#BCC8C3';
            const categoryName = nome.charAt(0).toUpperCase() + nome.slice(1);

            const item = document.createElement('div');
            item.className = 'legend-item';

            item.innerHTML = `
                <div class="legend-color" style="background:${color}"></div>
                <div class="legend-info">
                    <strong>${icon} ${categoryName}</strong>
                    <small>R$ ${dados.valor.toFixed(2).replace('.', ',')}</small>
                </div>
                <div class="legend-percent">${dados.percentual.toFixed(1)}%</div>
            `;

            legend.appendChild(item);
        });
    }

    /**
     * Renderiza todos os gráficos
     * @param {Object} categorias - Dados das categorias
     */
    renderAll(categorias) {
        this.renderPieChart(categorias);   // agora é donut por dentro ✅
        this.renderLegend(categorias);
        this.renderBarChart(categorias);
    }

    /**
     * Limpa todos os gráficos
     */
    destroy() {
        if (this.pieChart) {
            this.pieChart.destroy();
            this.pieChart = null;
        }
        if (this.barChart) {
            this.barChart.destroy();
            this.barChart = null;
        }
    }
}

// Exportar instância global
const chartManager = new ChartManager();
