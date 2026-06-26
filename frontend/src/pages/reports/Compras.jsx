import React, { useState, useRef } from 'react';
// Importações do MUI
import { Box, Button, TextField, Paper, Typography, Stack } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { DataGrid } from '@mui/x-data-grid';

import { formatarNumero2Casas, formatarMoedaBR, parseDataAPI, formatarDataBR } from "../../utils/formaters"

// Formato padrão para colunas de tipo numérico (quantidade, compra, custo, venda, estoque, sugestão)
const columnsCCVE = {
    type: 'number',
    width: 80,
    valueFormatter: formatarNumero2Casas,
}

// 1. Definição das Colunas
const columns = [
    { 
        field: 'cod_barra',
        headerName: 'Cód. Barras',
        editable: true,
        width: 150 
    },
    { 
        field: 'quantidade',
        headerName: 'Qte',
        editable: true,
        ...columnsCCVE
    },
    { 
        field: 'descricao',
        headerName: 'Descrição', 
        flex: 1 
    },
    { 
        field: 'compra',
        headerName: 'Compra', 
        ...columnsCCVE
    },
    { 
        field: 'custo',
        headerName: 'Custo', 
        ...columnsCCVE
    },
    { 
        field: 'venda',
        headerName: 'Venda', 
        ...columnsCCVE
    },
    { 
        field: 'estoque',
        headerName: 'Estoque', 
        ...columnsCCVE
    },
    { 
        field: 'ultimo_fornecedor',
        headerName: 'Últ. Fornecedor', 
        width: 180
    },
    { 
        field: 'data_ultima_compra',
        headerName: 'Últ. Compra', 
        type: 'date', 
        width: 110, 
        valueGetter: parseDataAPI,
        valueFormatter: formatarDataBR
    },
    { 
        field: 'sugestao_compra_api',
        headerName: 'Sugestão', 
        ...columnsCCVE 
    },
];



const handleAtualizarDados = (id, e) => {
    const { name, value } = e.target;

    setTableData(prevData =>
        prevData.map(row =>
            row.id === id ? { ...row, [name]: value } : row
        )
    );

    // Debounce (só executa quando parar de digitar)
    const timerKey = `${id}-${name}`;
    if (debounceTimers.current[timerKey]) clearTimeout(debounceTimers.current[timerKey]);

    debounceTimers.current[timerKey] = setTimeout(() => {
        console.log(`Digitação finalizada - Linha ID: ${id} | Campo: ${name} | Valor Final: ${value}`);
        
    }, 500); // 500 milissegundos de atraso após a última tecla
};

const handleChangeDate = (e) => {
    const { id, value } = e.target;
    let currentStartDate = startDate;
    let currentEndDate = endDate;

    if (id === 'start-date') {
        setStartDate(value);
        currentStartDate = value;
    } else if (id === 'end-date') {
        setEndDate(value);
        currentEndDate = value;
    }

    if (currentStartDate && currentEndDate && currentStartDate > currentEndDate) {
        alert("A data de início não pode ser posterior à data de fim.");
        if (id === 'start-date') {
            setStartDate('');
            currentStartDate = '';
        } else {
            setEndDate('');
            currentEndDate = '';
        }
    }

    // Exibindo as variáveis salvas
    console.log(`Data Início: ${currentStartDate} | Data Fim: ${currentEndDate}`);
};

export default function Compras() {

        // filtros para o relatório
        const [dtInicio, setDtInicio] = useState('');
        const [dtFim, setDtFim] = useState('');
        const [mesesSugestao, setMesesSugestao] = useState(1);
        const [itensSelecionados, setItensSelecionados] = useState([]);
        // 
        const [isLoading, setIsLoading] = useState(false); 
        const [apiResponse, setApiResponse] = useState(null); 
        
        // Ref para armazenar os timers de cada campo independentemente
        const debounceTimers = useRef({});

        // 2. O Estado com seu JSON de Placeholder
        const [rows, setRows] = useState([
                { id: 1, cod_barra: "7891020304050", quantidade: 100, descricao: "Bomba Hidráulica de Engrenagem", ultimo_fornecedor: "HidroPeças S.A.", data_ultima_compra: "2026-03-15", estoque: 15, media_vendas: 15.0, compra: 401.25, custo: 450.50, venda: 890.00, sugestao_compra_api: 20,},
                { id: 2, cod_barra: "7895566778899", quantidade: 2, descricao: "Válvula Direcional 4/3 Vias", ultimo_fornecedor: "Válvulas Brasil", data_ultima_compra: "2025-11-20", estoque: 80, media_vendas: 4.0, compra: 100.00, custo: 120.00, venda: 250.00, sugestao_compra_api: 20,},
                { id: 3, cod_barra: "1234567890123", quantidade: 20, descricao: "Filtro de Sucção 100 Microns", ultimo_fornecedor: "Filtros Express", data_ultima_compra: "2026-05-10", estoque: 5, media_vendas: 10.0, compra: 25.00, custo: 45.90, venda: 95.00, sugestao_compra_api: 20,}
        ]);

    return (
        <Box sx={{ width: '100%', p: 3 }}>
            {/* Container dos Filtros (Substitui a div padrão e dá um fundo com sombra) */}
            <Paper sx={{ p: 3, mb: 3 }}>
                
                {/* Cabeçalho do Relatório */}
                <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
                Análise de Compras
                </Typography>

                {/* Alinhamento dos Filtros (O Stack substitui as flex-box do Bootstrap) */}
                <Stack 
                direction={{ xs: 'column', md: 'row' }} // Fica em coluna no celular e em linha no PC
                spacing={2} 
                sx={{ 
                    mt: 2,
                    alignItems:"center" 
                }}
                >
                    <TextField
                        label="Data de Início"
                        type="date"
                        value={dtInicio}
                        onChange={(e) => setDtInicio(e.target.value)}
                        // InputLabelProps shrink garante que o label não fique em cima da data
                        slotProps={{
                            inputLabel: { shrink: true }
                        }}
                        size="small"
                        fullWidth
                        sx={{ maxWidth: 200 }}
                    />

                    <TextField
                        label="Data de Fim"
                        type="date"
                        value={dtFim}
                        onChange={(e) => setDtFim(e.target.value)}
                        slotProps={{
                            inputLabel: { shrink: true }
                        }}
                        size="small"
                        fullWidth
                        sx={{ maxWidth: 200 }}
                    />

                    <TextField
                        label="Meses para Sugestão"
                        type="number"
                        value={mesesSugestao}
                        onChange={(e) => setMesesSugestao(e.target.value)}
                        size="small"
                        slotProps={{
                            htmlInput: { min: 1 }
                        }} // Evita valores negativos
                        fullWidth
                        sx={{ maxWidth: 150 }}
                    />

                    {/* Botão de Refresh */}
                    <Button 
                        variant="contained" 
                        color="primary" 
                        startIcon={<RefreshIcon />} 
                        onClick={handleAtualizarDados}
                        sx={{ height: 40 }} // Iguala a altura com os textfields "small"
                    >
                        Atualizar
                    </Button>
                </Stack>
            </Paper>
            {/* A Tabela */}
            <Box sx={{ height: 600, width: '100%', mt: 2 }}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSizeOptions={[10, 25, 50]}
                    initialState={{
                        pagination: { paginationModel: { pageSize: 10 } },
                    }}
                    checkboxSelection
                    disableRowSelectionOnClick
                    />
            </Box>
        </Box>
    );
}