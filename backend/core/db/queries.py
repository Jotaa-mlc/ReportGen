PRODUTOS_DCCVE_QUERY = """
SELECT
    pr.Cod_barra           AS "cod_barra",
    pr.Descricao           AS "descricao",
    pr.Vlr_ultima_compra   AS "compra",
    pr.Vlr_ultimo_custo    AS "custo",
    pr.Vlr_normal          AS "venda",
    pr.Estoque_atual       AS "estoque"

FROM Produtos pr

WHERE pr.Cod_barra IN ({placeholders}) AND pr.Sit_produto = 'Ativo' 
"""