from xlsxwriter.utility import xl_col_to_name



def apply_header_format(
    worksheet,
    dataframe,
    formats
):

    for col_num, value in enumerate(dataframe.columns):

        worksheet.write(
            0,
            col_num,
            value,
            formats['header']
        )



def freeze_layout(worksheet):

    worksheet.freeze_panes(1, 2)



def apply_autofilter(worksheet, dataframe):

    worksheet.autofilter(
        0,
        0,
        len(dataframe),
        len(dataframe.columns) - 1
    )



def auto_width(worksheet, dataframe):

    for idx, col in enumerate(dataframe.columns):

        max_len = max(
            dataframe[col].astype(str).map(len).max(),
            len(str(col))
        )

        worksheet.set_column(
            idx,
            idx,
            min(max_len + 2, 40)
        )