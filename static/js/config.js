/* =================================================
   CONFIGURAÇÕES GLOBAIS
================================================= */

const CATEGORY_COLORS = {
  alimentacao:   '#19aa20ff', // verde → comida, natural, saudável
  transporte:    '#1565C0', // azul → mobilidade, confiança
  lazer:         '#a86604ff', // amarelo → diversão, energia
  saude:         '#C62828', // vermelho → saúde, atenção, cuidado
  educacao:      '#6A1B9A', // roxo → conhecimento, aprendizado
  moradia:       '#948a05ff', // marrom → casa, terra, estabilidade
  transferencia: '#008679ff', // teal → neutro/operacional
  investimento:  '#263c61ff', // azul escuro → dinheiro, seriedade
  outros:        '#9E9E9E'  // cinza → categoria genérica
};

// Ícones das categorias
const CATEGORY_ICONS = {
    'alimentacao': '🍔',
    'transporte': '🚗',
    'lazer': '🎮',
    'saude': '💊',
    'educacao': '📚',
    'moradia': '🏠',
    'transferencia': '💸',
    'investimento': '📈',
    'outros': '📦'
};

// Configurações dos gráficos
const CHART_CONFIG = {
    pie: {
        width: 300,
        height: 300,
        dataLabels: {
            enabled: true,
            formatter: (val) => val.toFixed(1) + '%'
        }
    },
    bar: {
        height: 300,
        toolbar: {
            show: false
        }
    }
};

// Endpoints da API
const API_ENDPOINTS = {
    process: '/process',
    health: '/health'
};

// Atualizado em 23/01/2025 - Paleta Variada para melhor visualização
