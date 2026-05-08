import sqlite3
import pandas as pd
from xlsxwriter.utility import xl_col_to_name
import datetime
import dateutil.relativedelta
from config import xlsx_formats
from config.xlsx_formats import build_formats
from config.settings import (
    SQLITE_DB,
    XLSX_DIR,
    ENCODING,
    ROOT_DIR
)

# =========================
# CONFIGURAÇÃO DO RELATÓRIO
# =========================

MESES_VENDAS = 12
MESES_SUGESTAO = 3

COD_BARRAS = pd.read_csv(
    ROOT_DIR / "input/produtos_compras.csv",
    encoding=ENCODING
)["Cod_barra"].tolist()

# =========================
# DATAS
# =========================

TODAY = datetime.datetime.now()

OUTPUT_XLSX = XLSX_DIR / (
    f"{TODAY.strftime('%Y-%m-%d %Hh%M')} "
    f"Relatório de compras.xlsx"
)

DATA_FIM = TODAY.strftime("%Y-%m")

DATA_INICIO = (
    TODAY
    - dateutil.relativedelta.relativedelta(
        months=MESES_VENDAS
    )
).strftime("%Y-%m")

# =========================
# SQLITE
# =========================

conn = sqlite3.connect(SQLITE_DB)

# =========================
# PRODUTOS
# =========================

placeholders = ",".join(["?"] * len(COD_BARRAS))

prod_query = f"""
SELECT
    pr.Cod_barra           AS "Código barra",
    pr.Descricao           AS "Descrição do produto",
    pr.Vlr_ultima_compra   AS "R$ Compra",
    pr.Vlr_ultimo_custo    AS "R$ Custo",
    pr.Vlr_normal          AS "R$ Venda",
    pr.Estoque_atual       AS "Estoque"

FROM Produtos pr

WHERE pr.Cod_barra IN ({placeholders})
"""

prod_df = pd.read_sql_query(
    prod_query,
    conn,
    params=COD_BARRAS
)

# =========================
# VENDAS MENSAIS
# =========================

vendas_query = f"""
SELECT
    pi.Cod_barra,

    strftime(
        '%Y-%m',
        p.Data_pedido
    ) AS mes,

    SUM(pi.Quantidade)
        AS total_quantidade

FROM Pedidos_itens pi

JOIN Pedidos p
    ON pi.Num_pedido = p.Num_pedido

WHERE p.Data_pedido >= ?
  AND p.Data_pedido < ?
  AND p.Documentos IN (
        'Pedido',
        'Remessa p/Vendas'
    )

  AND pi.Cod_barra IN ({placeholders})

GROUP BY
    pi.Cod_barra,
    mes

ORDER BY
    mes,
    pi.Cod_barra
"""

params = (
    [DATA_INICIO, DATA_FIM]
    + COD_BARRAS
)

vendas_df = pd.read_sql_query(
    vendas_query,
    conn,
    params=params
)

# =========================
# PIVOT
# =========================

pivot_df = vendas_df.pivot_table(
    index="Cod_barra",
    columns="mes",
    values="total_quantidade",
    aggfunc="sum",
    fill_value=0
)

pivot_df.reset_index(inplace=True)

# =========================
# MERGE
# =========================

final_df = prod_df.merge(
    pivot_df,
    left_on="Código barra",
    right_on="Cod_barra",
    how="left"
)

final_df.drop(
    columns=["Cod_barra"],
    inplace=True
)

final_df.fillna(0, inplace=True)

# =========================
# XLSXWRITER
# =========================

writer = pd.ExcelWriter(
    OUTPUT_XLSX,
    engine="xlsxwriter"
)

final_df.to_excel(
    writer,
    sheet_name="Relatório",
    index=False
)

workbook = writer.book
workbook.set_calc_mode("auto")
xlsx_formats = build_formats(workbook)
worksheet = writer.sheets["Relatório"]

# =========================
# ABA ORÇAMENTO
# =========================

orc_ws = workbook.add_worksheet("Orçamento")

orc_headers = [
    "Cód de barra",
    "Qte Orçada",
    "Vlr Uni",
    "%IPI",
    "R$ IPI",
    "%ICMS",
    "Total Item"
]

for col, title in enumerate(orc_headers):
    orc_ws.write(
        0,
        col,
        title,
        xlsx_formats["header"]
    )

# largura colunas
orc_ws.set_column(0, 0, 18)
orc_ws.set_column(1, 1, 14)

orc_ws.set_column(
    2,
    6,
    14,
    xlsx_formats["money"]
)

# freeze
orc_ws.freeze_panes(1, 1)

# filtro
orc_ws.autofilter(
    0,
    0,
    len(final_df),
    len(orc_headers) - 1
)

# =========================
# ABA RELATÓRIO
# =========================

# =========================
# CABEÇALHO
# =========================

for col_num, value in enumerate(final_df.columns):
    worksheet.write(
        0,
        col_num,
        value,
        xlsx_formats["header"]
    )

# =========================
# COLUNAS MENSAIS
# =========================

headers = list(final_df.columns)

mes_cols = []

for idx, h in enumerate(headers):
    if isinstance(h, str) and h.startswith("20"):
        mes_cols.append(idx)

first_mes_col = mes_cols[0]
last_mes_col = mes_cols[-1]

# =========================
# COLUNAS EXTRAS
# =========================

extra_cols = [
    "Vendas Mes",
    "Média Ult Ano/Mes",
    "Estq/Mes",
    "Sugestão",
    "Est+Sug/Mes",
    "Est+Comp/Mes",
    "Qte Orçamento",
    "~Orçamento",
    "",
    "◀ Meses para Sugestão"
]

start_extra = len(headers)

for i, title in enumerate(extra_cols):

    worksheet.write(
        0,
        start_extra + i,
        title,
        xlsx_formats["header"]
    )

# valor padrão
worksheet.write(
    0,
    start_extra + 8,
    MESES_SUGESTAO,
    xlsx_formats["integer"]
)

# =========================
# LINHAS
# =========================

for row in range(1, len(final_df) + 1):

    excel_row = row + 1

    # =====================
    # RANGE DE VENDAS
    # =====================

    start_letter = xl_col_to_name(first_mes_col)
    end_letter   = xl_col_to_name(last_mes_col)

    vendas_range = (
        f"Relatório!"
        f"{start_letter}{excel_row}:"
        f"{end_letter}{excel_row}"
    )

    # =====================
    # COLUNAS FIXAS
    # =====================

    estoque_col = headers.index("Estoque")

    media_col      = start_extra + 1
    estq_mes_col   = start_extra + 2
    sugestao_col   = start_extra + 3
    est_sug_col    = start_extra + 4
    est_comp_col   = start_extra + 5
    qte_orcamento_col  = start_extra + 6
    var_orcamento_col = start_extra + 7
    input_col      = start_extra + 8

    # =====================
    # SPARKLINE
    # =====================

    worksheet.add_sparkline(
        row,
        start_extra,
        {
            "range": vendas_range,
            "type": "column"
        }
    )

    # =====================
    # MÉDIA
    # =====================

    worksheet.write_formula(
        row,
        media_col,
        (
            f"=AVERAGE("
            f"{start_letter}{excel_row}:"
            f"{end_letter}{excel_row}"
            f")"
        ),
        xlsx_formats["decimal"]
    )

    # =====================
    # ESTQ / MES
    # =====================

    worksheet.write_formula(
        row,
        estq_mes_col,
        (
            f"="
            f"{xl_col_to_name(estoque_col)}{excel_row}"
            f"/"
            f"{xl_col_to_name(media_col)}{excel_row}"
        ),
        xlsx_formats["decimal"]
    )

    # =====================
    # SUGESTÃO
    # =====================

    worksheet.write_formula(
        row,
        sugestao_col,
        (
            f"=ROUND(("
            f"{xl_col_to_name(input_col)}$1*"
            f"{xl_col_to_name(media_col)}{excel_row}-"
            f"{xl_col_to_name(estoque_col)}{excel_row}"
            f")/5,0)*5"
        ),
        xlsx_formats["integer"]
    )

    # =====================
    # EST + SUG
    # =====================

    worksheet.write_formula(
        row,
        est_sug_col,
        (
            f"=("
            f"{xl_col_to_name(estoque_col)}{excel_row}+"
            f"{xl_col_to_name(sugestao_col)}{excel_row}"
            f")/"
            f"{xl_col_to_name(media_col)}{excel_row}"
        ),
        xlsx_formats["decimal"]
    )

    # =====================
    # EST + COMP
    # =====================

    worksheet.write_formula(
        row,
        est_comp_col,
        (
            f"=("
            f"{xl_col_to_name(estoque_col)}{excel_row}+"
            f"{xl_col_to_name(input_col)}{excel_row}"
            f")/"
            f"{xl_col_to_name(media_col)}{excel_row}"
        ),
        xlsx_formats["decimal"]
    )
    
    # =====================
    # QTE ORÇAMENTO
    # =====================

    worksheet.write_formula(
        row,
        qte_orcamento_col,
        (
            f'=IFERROR(VLOOKUP(A{excel_row},\'Orçamento\'!A:B,2,0),0)'
        ),
        xlsx_formats["integer"],
        0
    )
    
    # =====================
    # VARIAÇÃO ORÇAMENTO
    # =====================

    worksheet.write_formula(
        row,
        var_orcamento_col,
        (
            f'=IFERROR((VLOOKUP(A{excel_row},\'Orçamento\'!A:C,3,0)/C{excel_row})-1,0)'
        ),
        xlsx_formats["percent"],
        0
    )
# =========================
# FORMATAÇÃO CONDICIONAL
# =========================

for i in range(1, len(final_df) + 1):

    # =====================
    # VALORES DA LINHA
    # =====================

    valores = final_df.iloc[
        i - 1,
        first_mes_col:last_mes_col + 1
    ]

    todos_zero = (valores == 0).all()

    # =====================
    # LINHA SEM VENDAS
    # =====================

    if todos_zero:

        worksheet.conditional_format(
            i,
            first_mes_col,
            i,
            last_mes_col,
            {
                "type": "no_blanks",
                "format": xlsx_formats["zero"]
            }
        )

    # =====================
    # LINHA COM VENDAS
    # =====================

    else:

        worksheet.conditional_format(
            i,
            first_mes_col,
            i,
            last_mes_col,
            {
                "type": "data_bar"
            }
        )

# estoque crítico
worksheet.conditional_format(
    1,
    estq_mes_col,
    len(final_df),
    estq_mes_col,
    {
        "type": "cell",
        "criteria": "<",
        "value": 1,
        "format": workbook.add_format({
            "bg_color": "#FFC7CE"
        })
    }
)

# variação orçamento

worksheet.conditional_format(
    1,
    var_orcamento_col,
    len(final_df),
    var_orcamento_col,
    {
        "type": "3_color_scale"
    }
)

# =========================
# FORMATAÇÃO COLUNAS
# =========================

worksheet.set_column(0, 0, 18)
worksheet.set_column(1, 1, 40)

worksheet.set_column(2, 4, 12, xlsx_formats["money"])

worksheet.set_column(5, 5, 10, xlsx_formats["decimal"])

worksheet.set_column(
    first_mes_col,
    last_mes_col,
    10,
    xlsx_formats["integer"]
)

worksheet.set_column(
    start_extra,
    start_extra,
    18
)

worksheet.set_column(
    start_extra + 1,
    start_extra + 5,
    14,
    xlsx_formats["decimal"]
)

worksheet.set_column(
    qte_orcamento_col,
    qte_orcamento_col,
    14,
    xlsx_formats["integer"]
)

worksheet.set_column(
    var_orcamento_col,
    var_orcamento_col,
    16,
    xlsx_formats["percent"]
)

worksheet.set_column(
    input_col,
    input_col + 1,
    18,
    xlsx_formats["integer"]
)

# =========================
# FREEZE PANES
# =========================

worksheet.freeze_panes(
    1,
    2
)

# =========================
# FILTRO
# =========================

worksheet.autofilter(
    0,
    0,
    len(final_df),
    start_extra + len(extra_cols)
)

# =========================
# FECHAR
# =========================

writer.close()

conn.close()

print(
    f"Relatório salvo em:\n"
    f"{OUTPUT_XLSX}"
)