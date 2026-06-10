import datetime

import pandas as pd

from pathlib import Path

from backend.core.config.settings import (
    SQLITE_DB,
    INPUT_DIR,
    ENCODING
)

from backend.report.compras.settings import (
    MESES_VENDAS,
    XLSX_OUTPUT_FILE
)

from backend.core.db.connection import get_connection


from backend.report.compras.builder import (
    build_vendas_pivot,
    merge_report_data
)

from backend.report.compras.queries import (
    load_produtos,
    load_vendas
)

from backend.report.compras.export import export_report

# =========================
# INPUT
# =========================

def load_cod_barras(input_file_name):
    input_file = Path(INPUT_DIR / input_file_name)
    if not input_file.is_file():
        raise FileNotFoundError("Input file not found")

    return pd.read_csv(
        input_file,
        encoding=ENCODING
    )['codigo_barra'].tolist()

# =========================
# DATAS
# =========================

def build_period():

    today = datetime.datetime.now()

    data_fim = today.strftime('%Y-%m')

    data_inicio = (
        today
        - pd.DateOffset(months=MESES_VENDAS)
    ).strftime('%Y-%m')

    return data_inicio, data_fim

# =========================
# MAIN
# =========================

def main(input_file_name):
    
    cod_barras = load_cod_barras(input_file_name)

    data_inicio, data_fim = build_period()

    conn = get_connection(SQLITE_DB)

    produtos_df = load_produtos(
        conn,
        cod_barras
    )

    vendas_df = load_vendas(
        conn,
        cod_barras,
        data_inicio,
        data_fim
    )

    pivot_df = build_vendas_pivot(
        vendas_df
    )

    final_df = merge_report_data(
        produtos_df,
        pivot_df
    )

    full_output_file = datetime.datetime.now().strftime('%Y-%m-%d %Hh %Mm %Ss') + ' ' + XLSX_OUTPUT_FILE
    export_report(final_df, full_output_file)

    conn.close()


if __name__ == '__main__':

    main()