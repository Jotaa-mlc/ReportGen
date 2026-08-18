from xlsxwriter.utility import xl_col_to_name as col

# =====================
# RANGES
# =====================

def vendas_range(ctx):
    cols = ctx["column_map"]
    first_col = cols[ctx["month_columns"][0]]
    last_col = cols[ctx["month_columns"][-1]]
    row = ctx["excel_row"]

    return (
        f"{col(first_col)}{row}:"
        f"{col(last_col)}{row}"
    )

# =====================
# SPARKLINE
# =====================

def sparkline_config(ctx):

    return {
        "range": vendas_range(ctx),
        "type": "column"
    }

# =====================
# MÉDIA
# =====================

def media_formula(ctx):

    return (
        f'=AVERAGE({vendas_range(ctx)})'
    )

# =====================
# ESTQ / MES
# =====================

def estoque_mes_formula(ctx):

    row = ctx["excel_row"]

    column_map = ctx["column_map"]

    estoque_col = column_map["estoque"]

    media_col = column_map["media_vendas"]

    return (
        f'=IFERROR('
        f'{col(estoque_col)}{row}'
        f'/'
        f'{col(media_col)}{row}'
        f',0)'
    )

# =====================
# SUGESTÃO
# =====================

def sugestao_formula(ctx):

    input_row = 1
    arround_to = 5
    row = ctx["excel_row"]
    
    cols = ctx["column_map"]

    input_col = cols["input_sugestao"]

    media_col = cols["media_vendas"]

    estoque_col = cols["estoque"]

    return (
        f'=IF(({col(input_col)}${input_row}*'
        f'{col(media_col)}{row}) - {col(estoque_col)}{row} >= {arround_to}/2,'
        f'MROUND(({col(input_col)}${input_row}*'
        f'{col(media_col)}{row}-'
        f'{col(estoque_col)}{row}'
        f'),{arround_to})'
        f',"")'
    )

# =====================
# EST + SUG
# =====================

def estoque_sugestao_formula(ctx):

    row = ctx["excel_row"]

    cols = ctx["column_map"]

    estoque_col = cols["estoque"]

    sugestao_col = cols["sugestao"]

    media_col = cols["media_vendas"]

    return (
        f'=IF({col(sugestao_col)}{row}<>"",'
        f'({col(estoque_col)}{row}+'
        f'{col(sugestao_col)}{row}'
        f')/'
        f'{col(media_col)}{row}'
        f',"")'
    )

# =====================
# EST + COMP
# =====================

def estoque_compra_formula(ctx):

    row = ctx["excel_row"]

    cols = ctx["column_map"]

    estoque_col = cols["estoque"]

    input_col = cols["input_sugestao"]

    media_col = cols["media_vendas"]

    return (
        f'=IF({col(input_col)}{row}<>"",'
        f'({col(estoque_col)}{row}+'
        f'{col(input_col)}{row}'
        f')/'
        f'{col(media_col)}{row}'
        f',"")'
    )

# =====================
# QTE ORÇAMENTO
# =====================

def qte_orcamento_formula(ctx):

    row = ctx["excel_row"]

    codigo_col = ctx["column_map"]["cod_barra"]

    return (
        f'=IFERROR('
        f'VLOOKUP('
        f'{col(codigo_col)}{row},'
        f'\'Orçamento\'!A:B,'
        f'2,0'
        f'),"")'
    )

# =====================
# VLR ORÇAMENTO
# =====================

def vlr_orcamento_formula(ctx):

    row = ctx["excel_row"]

    codigo_col = ctx["column_map"]["cod_barra"]

    return (
        f'=IFERROR('
        f'VLOOKUP('
        f'{col(codigo_col)}{row},'
        f'\'Orçamento\'!A:C,'
        f'3,0'
        f'),"")'
    )
    
# =====================
# VLR ESPERADO ORÇAMENTO
# =====================

def vlr_esperado_orcamento_formula(ctx):
    
    row = ctx["excel_row"]

    custo_col = ctx["column_map"]["custo"]
    vlr_orcamento_col = ctx["column_map"]["vlr_orcamento"]
    input_sugestao_col = ctx["column_map"]["input_sugestao"]

    return (
        f'=IFERROR('
        f'IF('
        f'{col(vlr_orcamento_col)}{row}<>"",'
        f'{col(vlr_orcamento_col)}{row} * {col(input_sugestao_col)}{row},'
        f'{col(custo_col)}{row} * {col(input_sugestao_col)}{row}'
        f'),"")'
    )

# =====================
# VAR ORÇAMENTO
# =====================

def variacao_orcamento_formula(ctx):

    row = ctx["excel_row"]

    cols = ctx["column_map"]

    codigo_col = cols["cod_barra"]

    compra_col = cols["compra"]

    return (
        f'=IFERROR(('
        f'VLOOKUP('
        f'{col(codigo_col)}{row},'
        f'\'Orçamento\'!A:C,'
        f'3,0'
        f')/'
        f'{col(compra_col)}{row}'
        f')-1,"")'
    )
    
def default_input_sugestao(ctx):
    row = ctx["excel_row"]
    qte_orcamento_col = ctx["column_map"]["qte_orcamento"]
    qte_sugestao_col = ctx["column_map"]["sugestao"]
    

    return f'=IF({col(qte_orcamento_col)}{row}="",{col(qte_sugestao_col)}{row},{col(qte_orcamento_col)}{row})'