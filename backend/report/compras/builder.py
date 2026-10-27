import pandas as pd
import numpy as np


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
    
    final_df = handle_nulls(final_df)

    return final_df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Tratar as colunas Numéricas
    cols_numericas = df.select_dtypes(include=[np.number]).columns
    df[cols_numericas] = df[cols_numericas].fillna(0)

    # 2. Tratar as colunas de Texto (Strings/Objects)
    # cols_texto = df.select_dtypes(include=['object', 'string']).columns
    # df[cols_texto] = df[cols_texto].fillna("")

    return df