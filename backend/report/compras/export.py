from pathlib import Path

from pandas import DataFrame
from core.excel.commons import create_writer, export_dataframe, write_columns_from_config
from core.excel.formats import build_formats
from report.compras.settings import BASE_COLUMNS, EXTRA_COLUMNS, ORC_COLUMNS, CUSTOM_FORMATS
from report.compras.format import format_report


def build_report_columns(base_columns, dataframe, extra_columns):

    report_columns = dict(base_columns)

    month_columns = []

    for column in dataframe.columns:

        if (
            isinstance(column, str)
            and len(column) == 7
            and column[4] == "-"
        ):

            month_columns.append(column)

            report_columns[column] = {
                "title": column,
                "type": "data",
                "format": "integer",
                "width": 10
            }

    return {
        "columns": {**report_columns, **extra_columns},
        "month_columns": month_columns
    }

def export_report(final_df: DataFrame, output_file: Path) -> None:

    writer = create_writer(output_file)
    export_dataframe(
        writer,
        final_df
    )
    
    workbook = writer.book
    formats = build_formats(workbook, CUSTOM_FORMATS) # type: ignore
    report_worksheet = writer.sheets['Relatório']
    ctx=build_report_columns(BASE_COLUMNS, final_df, EXTRA_COLUMNS)
    write_columns_from_config(
        worksheet=report_worksheet,
        dataframe=final_df,
        formats=formats,
        context=ctx
    )
    
    format_report(
        worksheet=report_worksheet,
        formats=formats,
        df=final_df,
        context=ctx
    )
    
    orcamento_worksheet = workbook.add_worksheet("Orçamento") # type: ignore
    write_columns_from_config(
        worksheet=orcamento_worksheet,
        dataframe=DataFrame(),  # Passar um DataFrame vazio, pois os dados serão preenchidos manualmente
        formats=formats,
        context={
            "columns": ORC_COLUMNS
        }
    )


    writer.close()