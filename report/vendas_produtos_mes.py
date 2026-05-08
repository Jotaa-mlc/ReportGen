import sqlite3
import pandas as pd

# =========================
# CONFIGURAÇÃO
# =========================

DB_PATH = "banco.db"
OUTPUT_XLSX = "vendas_mensais.xlsx"

DATA_INICIO = "2024-01-01"
DATA_FIM    = "2026-05-01"


# =========================
# CONEXÃO
# =========================

conn = sqlite3.connect(DB_PATH)

# =========================
# CONSULTA BASE
# =========================

query = """
SELECT
    pi.Cod_barra,
    strftime('%Y-%m', p.Data_pedido) AS mes,
    SUM(pi.Quantidade) AS total_quantidade
FROM Pedidos_itens pi
JOIN Pedidos p
    ON pi.Num_pedido = p.Num_pedido
WHERE p.Data_pedido >= ?
  AND p.Data_pedido < ?
  AND p.Documentos IN ('Pedido','Remessa p/Vendas')
  AND p.Sit_pedido = 'Fechado'
GROUP BY
    pi.Cod_barra,
    mes
ORDER BY
    mes,
    pi.Cod_barra
"""

df = pd.read_sql_query(
    query,
    conn,
    params=(DATA_INICIO, DATA_FIM)
)

# =========================
# PIVOT
# =========================

pivot_df = df.pivot_table(
    index="Cod_barra",
    columns="mes",
    values="total_quantidade",
    aggfunc="sum",
    fill_value=0
)

# opcional: ordenar colunas
pivot_df = pivot_df.sort_index(axis=1)

# opcional: transformar índice em coluna
pivot_df.reset_index(inplace=True)

# =========================
# EXPORTAÇÃO XLSX
# =========================

with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
    pivot_df.to_excel(
        writer,
        sheet_name="Vendas Mensais",
        index=False
    )

print(f"Arquivo exportado: {OUTPUT_XLSX}")

conn.close()