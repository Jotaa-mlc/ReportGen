from datetime import date, datetime, timedelta
from pathlib import Path
import pandas as pd

from core.config.settings import (
    ERP_SQLITE_DB,
    INPUT_DIR,
    ENCODING,
    OUTPUT_DIR
) 

from report.compras.settings import (
    MESES_VENDAS,
    XLSX_OUTPUT_FILE
)

from core.db.connection import get_connection


from report.compras.builder import (
    build_vendas_pivot,
    merge_report_data
)

from report.compras.queries import (
    load_produtos,
    load_vendas
)

from report.compras.export import export_report

# =========================
# INPUT
# =========================

def load_cod_barras(input_file_name):
    input_file = Path(INPUT_DIR / input_file_name)
    if not input_file.is_file():
        raise FileNotFoundError("Input file not found")

    return pd.read_csv(
        input_file,
        delimiter=';',
        encoding=ENCODING
    )['cod_barra'].tolist()

# =========================
# DATAS
# =========================

def build_period():

    data_inicio = date.today() - timedelta(days=30*MESES_VENDAS)

    # data_inicio = (
    #     today
    #     - pd.DateOffset(months=MESES_VENDAS)
    # ).strftime('%Y-%m')
    return data_inicio.strftime('%Y-%m')

# =========================
# MAIN
# =========================

def main(input_file_name):
    
    cod_barras = load_cod_barras(input_file_name)

    data_inicio = build_period()

    conn = get_connection(ERP_SQLITE_DB)

    produtos_df = load_produtos(
        conn,
        cod_barras
    )
    
    #produtos_df['data_ultima_compra'] = pd.to_datetime(produtos_df['data_ultima_compra'], errors='coerce').dt.date
    
    vendas_df = load_vendas(
        conn,
        cod_barras,
        data_inicio
    )

    pivot_df = build_vendas_pivot(
        vendas_df
    )

    final_df = merge_report_data(
        produtos_df,
        pivot_df
    )
    

    timestamp = datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    output_filename = f"{timestamp} {XLSX_OUTPUT_FILE}"
    export_report(final_df, OUTPUT_DIR / output_filename)

    conn.close()


if __name__ == '__main__':

    main(input_file_name='multi.csv')