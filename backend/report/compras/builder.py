def build_vendas_pivot(vendas_df):

    pivot_df = vendas_df.pivot_table(
        index='cod_barra',
        columns='mes',
        values='total_quantidade',
        aggfunc='sum',
        fill_value=0
    )

    pivot_df.reset_index(inplace=True)

    return pivot_df



def merge_report_data(prod_df, pivot_df):

    final_df = prod_df.merge(
        pivot_df,
        left_on='cod_barra',
        right_on='cod_barra',
        how='left'
    )


    final_df.fillna(0, inplace=True)

    return final_df