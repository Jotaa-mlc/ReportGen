# Usa uma imagem oficial do Python leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do backend
COPY . .

# Comando para iniciar o servidor
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]