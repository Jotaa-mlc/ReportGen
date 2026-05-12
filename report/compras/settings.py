from report.compras import formulas

# =========================
# CONFIG
# =========================

MESES_VENDAS = 12
MESES_SUGESTAO = 3
XLSX_OUTPUT_FILE = 'Relatório de Compras.xlsx'
INPUT_FILE = 'produtos_compras.csv'

BASE_COLUMNS = {

    "cod_barra": {
        "title": "Código barra",
        "type": "format_only",
        "width": 14
    },

    "descricao": {
        "title": "Descrição do produto",
        "type": "format_only",
        "width": 50
    },

    "compra": {
        "title": "R$ Compra",
        "type": "format_only",
        "format": "money",
        "width": 10
    },
    
    "custo": {
        "title": "R$ Custo",
        "type": "format_only",
        "format": "money",
        "width": 10
    },
    
    "venda": {
        "title": "R$ Venda",
        "type": "format_only",
        "format": "money",
        "width": 10
    },
    
    "estoque": {
        "title": "Estoque",
        "type": "format_only",
        "format": "decimal",
        "width": 10
    }
}

EXTRA_COLUMNS = {

    "sparkline_vendas": {
        "title": "Vendas Mes",
        "type": "sparkline",
        "width": 18,
        "formula": formulas.sparkline_config,
    },

    "media_vendas": {
        "title": "Média Ult Ano/Mes",
        "type": "formula",
        "format": "decimal",
        "width": 14,
        "formula": formulas.media_formula,
    },

    "estoque_mes": {
        "title": "Estq/Mes",
        "type": "formula",
        "format": "decimal",
        "width": 12,
        "formula": formulas.estoque_mes_formula,
    },

    "sugestao": {
        "title": "Sugestão",
        "type": "formula",
        "format": "integer",
        "width": 12,
        "formula": formulas.sugestao_formula,
    },

    "estoque_sugestao": {
        "title": "Est+Sug/Mes",
        "type": "formula",
        "format": "decimal",
        "width": 14,
        "formula": formulas.estoque_sugestao_formula,
    },

    "estoque_compra": {
        "title": "Est+Comp/Mes",
        "type": "formula",
        "format": "decimal",
        "width": 14,
        "formula": formulas.estoque_compra_formula,
    },

    "qte_orcamento": {
        "title": "Qte Orçamento",
        "type": "formula",
        "format": "integer",
        "width": 14,
        "formula": formulas.qte_orcamento_formula,
        "value": 0
    },

    "variacao_orcamento": {
        "title": "~Orçamento",
        "type": "formula",
        "format": "percent",
        "width": 16,
        "formula": formulas.variacao_orcamento_formula,
        "value": 0
    },

    "input_sugestao": {
        "title": "",
        "type": "default_value",
        "format": "integer",
        "width": 12,
        "row_input": 0,
        "default": MESES_SUGESTAO
    },

    "input_label": {
        "title": "",
        "type": "default_value",
        "format": "header",
        "width": 22,
        "row_input": 0,
        "default": "◀ Meses para Sugestão"
        
    }
}

ORC_COLUMNS = {
    "cod_barra":{
        "title": "Cód de barra",
        "type": "value",
        "format": "integer",
    },
    "qte_orcada":{
        "title": "Qte Orçada",
        "type": "value",
        "format": "integer",
    },
    "vlr_uni":{
        "title": "Vlr Uni",
        "type": "value",
        "format": "decimal",
    },
    "ipi_perc":{
        "title": "%IPI",
        "type": "value",
        "format": "decimal",
    },
    "ipi_valor":{
        "title": "R$ IPI",
        "type": "value",
        "format": "money",
    },
    "icms_perc":{
        "title": "%ICMS",
        "type": "value",
        "format": "decimal",
    },
    "total_item":{
        "title": "Total Item",
        "type": "value",
        "format": "money",
    }
}

CUSTOM_FORMATS = {
    "zero_vendas": {
        "bg_color": "#D9D9D9",
        "font_color": "#808080"
    },
    
    "estoque_critico": {
        "bg_color": "#FFC7CE"
    }
}