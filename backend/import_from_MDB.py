import os
import re
import sqlite3
import subprocess
import pandas as pd
from backend.core.config.settings import (
    MDB_PATH,
    SCHEMA_FILE,
    SQLITE_DB,
    TABLE_DIR,
    ENCODING,
)

# =========================
# FLAGS
# =========================

RECREATE_SCHEMA = True

# tabelas que terão limpeza texto
TABLES_TO_CLEAN = [
    "Produtos",
]

# =========================
# UTIL
# =========================

def run(cmd):
    return subprocess.check_output(cmd).decode()


def get_tables():
    out = run(["mdb-tables", "-1", MDB_PATH])
    return [t.strip() for t in out.splitlines() if t.strip()]


# =========================
# SCHEMA (mdb-schema)
# =========================
        
def generate_schema():
    print("Gerando schema...")
    schema = run(["mdb-schema", MDB_PATH, "sqlite"])
    with open(SCHEMA_FILE, "w") as f:
        f.write(schema)

def ensure_schema():
    if RECREATE_SCHEMA or not os.path.exists(SCHEMA_FILE):
        generate_schema()
    else:
        print("[OK] usando schema existente")

def parse_schema(schema_path):
    tables = {}
    current_table = None

    with open(schema_path, "r") as f:
        for line in f:
            line = line.strip()

            # detectar CREATE TABLE
            match = re.match(r'CREATE TABLE [`"]?(.+?)[`"]?\s*$', line)
            if match:
                current_table = match.group(1)
                tables[current_table] = {}
                continue

            # fim da tabela
            if line.startswith(");"):
                current_table = None
                continue

            # colunas
            if current_table and line.startswith("`"):
                parts = line.strip(",").split()

                col = parts[0].strip("`")
                typ = parts[1].upper()

                tables[current_table][col] = typ

    return tables


# =========================
# MAPEAMENTO DE TIPOS
# =========================

def map_types(sql_types):
    dtype_map = {}
    date_cols = []

    for col, typ in sql_types.items():
        if "INT" in typ:
            dtype_map[col] = "Int64"
        elif "REAL" in typ or "FLOAT" in typ or "DOUBLE" in typ:
            dtype_map[col] = "float"
        elif "DATE" in typ or "TIME" in typ:
            date_cols.append(col)
        else:
            dtype_map[col] = "string"

    return dtype_map, date_cols


# =========================
# EXPORTAÇÃO
# =========================

def export_table(table):
    csv_path = os.path.join(TABLE_DIR, f"{table}.csv")
    with open(csv_path, "w") as f:
        subprocess.run(["mdb-export", MDB_PATH, table], stdout=f)
    return csv_path

def export_all_tables(schema):
    exported = {}
    for table in schema:
        print(f"[EXPORT] {table}")
        try:
            csv_path = export_table(table)
            exported[table] = csv_path
            
        except Exception as e:
            print(f"[ERRO EXPORT] {table}: {e}")
    return exported

# =========================
# IMPORTAÇÃO
# =========================

def load_dataframe(csv_path, dtype_map, date_cols):
    df = pd.read_csv(
        csv_path,
        dtype=dtype_map,
        encoding=ENCODING,
        on_bad_lines="skip"
    )

    for col in date_cols:
        df[col] = pd.to_datetime(
             df[col],
        format="%m/%d/%y %H:%M:%S",
        errors="coerce"
        )

        # normaliza para ISO
        df[col] = df[col].apply(
            lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
            if pd.notnull(x)
            else None
        )
    
    return df

def load_all_dataframes(schema, exported_csvs):
    tables = {}
    for table, cols in schema.items():
        print(f"[LOAD] {table}")
        try:
            dtype_map, date_cols = map_types(cols)
            df = load_dataframe(
                exported_csvs[table],
                dtype_map,
                date_cols
            )
            tables[table] = df
            print(f"Linhas: {len(df)}")

        except Exception as e:
            print(f"[ERRO LOAD] {table}: {e}")
    return tables

def save_to_sqlite(df, table, conn):
    df.to_sql(table, conn, if_exists="replace", index=False)

def export_to_sqlite(tables, sqlite_path):
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)
    conn = sqlite3.connect(sqlite_path)
    for table_name, df in tables.items():
        print(f"[SQLITE] {table_name}")
        try:
            save_to_sqlite(
                df,
                table_name,
                conn
            )

            validate(table_name, conn)

        except Exception as e:
            print(f"[ERRO SQLITE] {table_name}: {e}")

    check_integrity(conn)
    conn.close()
    
# =========================
# VALIDAÇÃO
# =========================

def clean_text_columns_in_tables(
    tables: dict,
    target_tables: list[str]
) -> dict:
    """
    Limpa caracteres problemáticos de colunas TEXT
    apenas nas tabelas especificadas.

    Parâmetros
    ----------
    tables : dict
        Dict no formato:
        {
            "Produtos": dataframe,
            "Pedidos": dataframe,
            ...
        }

    target_tables : list[str]
        Lista das tabelas que devem ser limpas.

    Retorna
    -------
    dict
        Mesmo dict com os DataFrames modificados.
    """

    for table_name in target_tables:
        if table_name not in tables:
            print(f"[WARN] tabela não encontrada: {table_name}")
            continue

        df = tables[table_name]

        # detectar colunas texto
        text_cols = df.select_dtypes(include=["object", "string"]).columns

        # limpar colunas
        for col in text_cols:
            df[col] = (
                df[col]
                .fillna("") # evitar NaN -> "nan"
                .astype(str) 
                .str.replace(r'[\r\n\t]+', ' ', regex=True) # remove \r \n \t
                .str.replace(r'[\x00-\x1F\x7F]', '', regex=True) # remove caracteres controle
                .str.replace(r'\s+', ' ', regex=True) # normaliza espaços
                .str.strip()
            )

        tables[table_name] = df
        print(f"[OK] texto limpo: {table_name}")

    return tables

def validate(table, conn):
    mdb_count = run(["mdb-count", MDB_PATH, table]).strip()

    cur = conn.cursor()
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    sqlite_count = str(cur.fetchone()[0])

    status = "OK" if mdb_count == sqlite_count else "⚠️ DIFERENÇA"
    print(f"[{status}] {table}: MDB={mdb_count} | SQLite={sqlite_count}")


def check_integrity(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA integrity_check;")
    print("\nIntegridade:", cur.fetchone()[0])
    

# =========================
# MAIN
# =========================

def main():
    ensure_schema()
    schema = parse_schema(SCHEMA_FILE)
    print(f"\nTabelas encontradas: {len(schema)}")

    exported_csvs = export_all_tables(schema)

    tables = load_all_dataframes(
        schema,
        exported_csvs
    )

    tables = clean_text_columns_in_tables(
        tables,
        TABLES_TO_CLEAN
    )

    export_to_sqlite(
        tables,
        SQLITE_DB
    )
    print("\n✔️ Concluído!")


if __name__ == "__main__":
    main()