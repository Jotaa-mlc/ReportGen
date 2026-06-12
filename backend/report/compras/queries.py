import pandas as pd
from core.db.queries import PRODUTOS_DCCVE_QUERY

VENDAS_QUERY = """
SELECT
    pi.Cod_barra          AS cod_barra,

    strftime('%Y-%m', p.Data_pedido) AS mes,

    SUM(pi.Quantidade) AS total_quantidade

FROM Pedidos_itens pi

JOIN Pedidos p
    ON pi.Num_pedido = p.Num_pedido

WHERE p.Data_pedido >= ?
  AND p.Data_pedido < ?

  AND p.Documentos IN (
        'Pedido',
        'Remessa p/Vendas'
    )

  AND cod_barra IN ({placeholders})

GROUP BY
    cod_barra,
    mes

ORDER BY
    mes,
    cod_barra
"""

def load_produtos(conn, cod_barras):

    placeholders = ','.join(
        ['?'] * len(cod_barras)
    )

    query = PRODUTOS_DCCVE_QUERY.format(
        placeholders=placeholders
    )

    return pd.read_sql_query(
        query,
        conn,
        params=cod_barras
    )



def load_vendas(
    conn,
    cod_barras,
    data_inicio,
    data_fim
):

    placeholders = ','.join(
        ['?'] * len(cod_barras)
    )

    query = VENDAS_QUERY.format(
        placeholders=placeholders
        
    )

    params = (
        [data_inicio, data_fim]
        + cod_barras
    )

    return pd.read_sql_query(
        query,
        conn,
        params=params
    )