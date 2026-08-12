import pandas as pd
from pathlib import Path
from core.config.settings import  OUTPUT_DIR
from xlsxwriter.workbook import Worksheet

def create_writer(output_file: Path) -> pd.ExcelWriter:
    return pd.ExcelWriter(
        OUTPUT_DIR / output_file,
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
): 

    column_map = build_column_map(context["columns"])

    # ==================================================
    # HEADERS
    # ==================================================

    for col_num, (key, config) in enumerate(
        context["columns"].items()
    ):
        
        column_map[key] = col_num

        worksheet.write(
            0,
            col_num,
            config.get("title", ""),
            formats["header"]
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

            # ==========================================
            # FORMULA
            # ==========================================

            if "formula" in col_type:

                formula = config["formula"](
                    row_context
                )

                worksheet.write_formula(
                    row,
                    col_num,
                    formula,
                    config.get("value")
                )

            # ==========================================
            # SPARKLINE
            # ==========================================

            if "sparkline" in col_type:

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
            
            if "default_value" in col_type:

                value = config.get("default", "")
                row = config.get("row_input_default")

                worksheet.write(
                    row,
                    col_num,
                    value
                )