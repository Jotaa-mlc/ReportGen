import pandas as pd

PRODUTOS_DCCVE_QUERY = """
SELECT
    p.Cod_barra           AS "cod_barra",
    p.Descricao           AS "descricao",
    p.Vlr_ultima_compra   AS "compra",
    p.Vlr_ultimo_custo    AS "custo",
    p.Vlr_normal          AS "venda",
    p.Estoque_atual       AS "estoque",
    MAX(ep.Data_entrada)  AS "data_ultima_compra",
    c.Nome                AS "ultimo_fornecedor"

FROM Produtos p
JOIN Entradas_produtos_itens epi ON p.Cod_barra = epi.Cod_barra 
JOIN Entradas_produtos ep ON epi.Seq_entrada = ep.Seq_entrada 
JOIN Clientes c ON ep.Cpf_cnpj = c.Cpf_cnpj 

WHERE 
    p.Cod_barra IN ({placeholders}) 
    AND p.Sit_produto = 'Ativo' 
    AND ep.Sit_lancamento = 1

GROUP BY p.Cod_barra
ORDER BY p.Descricao
"""

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

  AND p.Sit_pedido IN (
        'Fechado'
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