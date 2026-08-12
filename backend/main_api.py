# api.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import datetime

# Importando o seu framework
from core.config.settings import SQLITE_DB
from core.db.connection import get_connection
# from reports.familias_produtos.queries import load_entradas_fornecedores
# from reports.familias_produtos.builder import build_familias_df
# from reports.familias_produtos.export import export_familias_report

app = FastAPI(title="ReportGen API")

# Configurando CORS para o React conseguir acessar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, coloque "http://localhost:5173" (Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _remover_arquivo_temporario(path: str):
    """Remove o arquivo excel após o download para não lotar o servidor"""
    if os.path.exists(path):
        os.remove(path)

@app.get("/api/familias/preview")
def get_familias_preview():
    """Retorna os dados em JSON para preencher a tabela no React"""
    conn = get_connection(SQLITE_DB)
    try:
        entradas_df = {} #load_entradas_fornecedores(conn)
        final_df = {} #build_familias_df(entradas_df)
        
        # Converte o DataFrame para uma lista de dicionários (JSON amigável)
        # Limitamos a 100 linhas para o preview ficar leve na tela
        preview_data = {} #final_df.head(100).to_dict(orient="records")
        return {"data": preview_data}
    finally:
        conn.close()

@app.get("/api/familias/exportar")
def exportar_familias_excel(background_tasks: BackgroundTasks):
    """Gera o Excel e envia como arquivo para download direto no navegador"""
    conn = get_connection(SQLITE_DB)
    try:
        entradas_df = {} #load_entradas_fornecedores(conn)
        final_df = {} #build_familias_df(entradas_df)
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')
        file_name = f"Familias_{timestamp}.xlsx"
        
        # No FastAPI é melhor salvar em um diretório temporário (ex: /tmp ou na pasta do app)
        output_path = os.path.join("temp", file_name)
        os.makedirs("temp", exist_ok=True)
        
        # Usa sua função de exportação
        # export_familias_report(final_df, output_path)
        
        # Agenda a exclusão do arquivo após o usuário terminar o download
        background_tasks.add_task(_remover_arquivo_temporario, output_path)
        
        return FileResponse(
            path=output_path, 
            filename=file_name,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    finally:
        conn.close()