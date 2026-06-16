# ReportGen 📊

Um sistema de geração de relatórios interativos dividido em uma API robusta (Python) e uma interface dinâmica (React).

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python, FastAPI, Pandas, SQLite (via pyodbc/sqlite3).
* **Frontend:** React, Vite, React Router DOM, CSS nativo.

## 🚀 O que o sistema já faz (Features Atuais)
* **Relatório de Compras:** Cruza dados de produtos com o histórico de entradas e vendas, gera uma tabela dinâmica (Pivot) e exporta abas customizadas no Excel.
* **Relatório de Famílias (Em dev):** Agrupa produtos por fornecedor baseado em regras de negócio de strings (Hifens ou Regex) e exibe os dados na interface web.

## ⚙️ Como rodar o projeto localmente

### 1. Rodando a API (Backend)
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main_api:app --reload
\`\`\`
*A API ficará disponível em http://localhost:8000*

### 2. Rodando a Interface (Frontend)
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
*O painel ficará disponível em http://localhost:5173*