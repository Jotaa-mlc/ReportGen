from xlsxwriter.workbook import Worksheet
from pandas import DataFrame
from xlsxwriter.utility import xl_col_to_name as col 
from core.excel.commons import build_column_map



def format_report(worksheet: Worksheet, formats: dict, df: DataFrame, context: dict):
    # =========================
    # FORMATAÇÃO CONDICIONAL
    # =========================
    column_map = build_column_map(context["columns"])
    
    first_mes_col = column_map[context["month_columns"][0]]
    last_mes_col = column_map[context["month_columns"][-1]]
    estoque_col = column_map["estoque"]
    variacao_orcamento_col = column_map["variacao_orcamento"]
    qte_orcamento_col = column_map["qte_orcamento"]
    input_sugestao_col = column_map["input_sugestao"]

    # zero vendas
    worksheet.conditional_format(
        1,
        first_mes_col,
        len(df),
        last_mes_col,
        {
            "type": "formula",
            "criteria": f'=SUM(${col(first_mes_col)}2:${col(last_mes_col)}2)=0',
            "format": formats["zero_vendas"]
        }
    )

    # vendas
    worksheet.conditional_format(
        1,
        first_mes_col,
        len(df),
        last_mes_col,
        {
            "type": "data_bar"
        }
    )
    
    # estoque crítico
    worksheet.conditional_format(
        1,
        estoque_col,
        len(df),
        estoque_col,
        {
            "type": "cell",
            "criteria": "<",
            "value": 1,
            "format": formats["estoque_critico"]
        }
    )

    # variação orçamento
    worksheet.conditional_format(
        1,
        variacao_orcamento_col,
        len(df),
        variacao_orcamento_col,
        {
            "type": "3_color_scale",
            'min_color': "#63BE7B",
            'mid_color': "#FFEB84",
            'max_color': "#F8696B"
        }
    )
    
    # qte orçamento diferente de qte pedida
    worksheet.conditional_format(
        1,
        input_sugestao_col,
        len(df),
        input_sugestao_col,
        {
            "type": "formula",
            "criteria": f'=${col(input_sugestao_col)}2<>{col(qte_orcamento_col)}2',
            "format": formats["orcamento_diferente"]
        }
    )
    
    # =========================
    # FREEZE PANES
    # =========================

    worksheet.freeze_panes(
        1,
        6
    )

    # =========================
    # FILTRO
    # =========================

    worksheet.autofilter(
        0,
        0,
        len(df),
        len(column_map) - 1
    )