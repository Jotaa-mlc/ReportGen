-- Ativar as Foreign Keys na conexão atual
PRAGMA foreign_keys = ON;

-- Tabela de Configurações de Relatórios
CREATE TABLE IF NOT EXISTS configuracoes_relatorios ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome_relatorio TEXT NOT NULL, 
    tabela_relatorio TEXT NOT NULL, 
    dt_criacao DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS analise_compra ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_relatorio INTEGER NOT NULL, 
    descricao TEXT, 
    meses_sugestao INTEGER DEFAULT 1, 
    dt_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_relatorio) REFERENCES configuracoes_relatorios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS analise_compra_itens ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_analise_compra INTEGER NOT NULL, 
    cod_barra TEXT NOT NULL, -- Validação de existência desse código será feita no Python/API
    quantidade INTEGER DEFAULT 0, 
    sugestao_compra INTEGER DEFAULT 0,
    FOREIGN KEY (id_analise_compra) REFERENCES analise_compra(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cotacao_compra ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_fornecedor TEXT NOT NULL, 
    descricao TEXT, 
    dt_criacao DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS cotacao_compra_itens ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_cotacao_compra INTEGER NOT NULL, 
    cod_fornecedor TEXT NOT NULL, 
    quantidade INTEGER NOT NULL, 
    preco_unitario REAL NOT NULL, 
    FOREIGN KEY (id_cotacao_compra) REFERENCES cotacao_compra(id) ON DELETE CASCADE
);

-- Tabela de Junção (Relação N:M entre Análise e Cotação)
CREATE TABLE IF NOT EXISTS analise_cotacao (
    id_analise_compra INTEGER NOT NULL,
    id_cotacao_compra INTEGER NOT NULL,
    PRIMARY KEY (id_analise_compra, id_cotacao_compra),
    FOREIGN KEY (id_analise_compra) REFERENCES analise_compra(id) ON DELETE CASCADE,
    FOREIGN KEY (id_cotacao_compra) REFERENCES cotacao_compra(id) ON DELETE CASCADE
);

-- Tabela auxiliar de Vendas Mensais
CREATE TABLE IF NOT EXISTS vendas_mensais ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cod_barra TEXT NOT NULL, 
    mes_referencia TEXT NOT NULL, 
    quantidade_vendida INTEGER DEFAULT 0, 
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP 
);

-- Criação de Índices para Performance
CREATE INDEX IF NOT EXISTS idx_vendas_produto_mes ON vendas_mensais(cod_barra, mes_referencia);