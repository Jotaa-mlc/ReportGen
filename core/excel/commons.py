import pandas as pd
from pathlib import Path
from core.config.settings import  XLSX_DIR
from xlsxwriter.workbook import Worksheet

def create_writer(output_file: Path) -> pd.ExcelWriter:
    return pd.ExcelWriter(
        XLSX_DIR / output_file,
        engine='xlsxwriter'
    )

def export_dataframe(writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str = 'Relatório') -> None:
    df.to_excel(
        writer,
        sheet_name=sheet_name,
        index=False
    )

def build_column_map(columns):

    return {

        key: idx

        for idx, key
        in enumerate(columns.keys())
    }

def apply_column_formats(
    worksheet: Worksheet,
    formats: dict,
    columns_config: dict,
    column_map: dict
):
    """
    Aplica largura e formato padrão das colunas.

    Parameters
    ----------
    worksheet : Worksheet

    formats : dict
        Dict de formatos xlsxwriter.

    columns_config : dict
        Dict declarativo das colunas.

    column_map : dict
        Map:
            key -> índice da coluna
    """

    for key, config in columns_config.items():

        col_num = column_map[key]

        if config.get("type") == "default_value":

            continue
        
        width = config.get("width")

        format_name = config.get("format")

        cell_format = (
            formats.get(format_name)
            if format_name
            else None
        )

        worksheet.set_column(
            col_num,
            col_num,
            width,
            cell_format
        )

def write_columns_from_config(
    worksheet: Worksheet,
    dataframe: pd.DataFrame,
    formats: dict,
    context: dict,
    start_col: int = 0
): 

    column_map = build_column_map(context["columns"])

    # ==================================================
    # HEADERS
    # ==================================================

    for idx, (key, config) in enumerate(
        context["columns"].items()
    ):

        col_num = start_col + idx

        column_map[key] = col_num

        worksheet.write(
            0,
            col_num,
            config.get("title", ""),
            formats["header"]
        )

        if "width" in config:

            worksheet.set_column(
                col_num,
                col_num,
                config["width"]
            )

    # ==================================================
    # APPLY COLUMN FORMATS
    # ==================================================
    
    apply_column_formats(
        worksheet=worksheet,
        formats=formats,
        columns_config=context["columns"],
        column_map=column_map
    )

    # ==================================================
    # ROWS
    # ==================================================

    for row in range(1, len(dataframe) + 1):

        excel_row = row + 1

        row_context = {
            **context,
            "row": row,
            "excel_row": excel_row,
            "column_map": column_map
        }

        for key, config in context["columns"].items():

            col_num = column_map[key]

            col_type = config.get("type")

            fmt = formats.get(
                config.get("format")
            )

            # ==========================================
            # FORMULA
            # ==========================================

            if col_type == "formula":

                formula = config["formula"](
                    row_context
                )

                worksheet.write_formula(
                    row,
                    col_num,
                    formula,
                    fmt,
                    config.get("value")
                )

            # ==========================================
            # SPARKLINE
            # ==========================================

            elif col_type == "sparkline":

                spark_cfg = config["formula"](
                    row_context
                )

                worksheet.add_sparkline(
                    row,
                    col_num,
                    spark_cfg
                )

            # ==========================================
            # DEFAULT VALUES
            # ==========================================
            
            elif col_type == "default_value":

                value = config.get("default", "")
                row_input = config.get("row_input")

                worksheet.write(
                    row_input,
                    col_num,
                    value,
                    fmt
                )