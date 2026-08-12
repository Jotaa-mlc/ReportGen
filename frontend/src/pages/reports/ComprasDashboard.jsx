import React, { useState } from 'react';
import { Box, Typography, Paper, Button, Stack } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import AddIcon from '@mui/icons-material/Add'; 
import VisibilityIcon from '@mui/icons-material/Visibility';

export default function ComprasDashboard() {
  const navigate = useNavigate();

  const columns = [
    { field: 'id', headerName: 'ID Análise', width: 110 },
    { field: 'data_criacao', headerName: 'Data de Criação', width: 150 },
    { field: 'usuario', headerName: 'Criado Por', width: 150 },
    { field: 'filtros_aplicados', headerName: 'Filtros (Período / Meses)', flex: 1 },
    {
      field: 'acoes',
      headerName: 'Ações',
      width: 150,
      sortable: false,
      renderCell: (params) => (
        <Button 
          variant="outlined" 
          size="small" 
          startIcon={<VisibilityIcon />}
          onClick={() => navigate(`/compras/${params.row.id}`)}
        >
          Visualizar
        </Button>
      )
    }
  ];

  // Placeholder simulando respostas do seu banco permanente (configuracoes_relatorios)
  const [rows] = useState([
    { id: 1, data_criacao: '2026-06-15', usuario: 'João Silva', filtros_aplicados: '01/01 a 31/03 - 3 Meses' },
    { id: 2, data_criacao: '2026-06-20', usuario: 'Maria Souza', filtros_aplicados: '10/04 a 10/05 - 1 Mês' },
  ]);

  return (
    <Box sx={{ width: '100%' }}>
      
      {/* Topo com Título e Botão de Ação */}
      <Stack direction="row" sx={{justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" fontWeight="bold">
          Histórico de Análises de Compras
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<AddIcon />}
          onClick={() => navigate('/compras/nova')} // Redireciona para gerar uma nova
        >
          Nova Análise
        </Button>
      </Stack>

      {/* Grid de Dados */}
      <Paper sx={{ height: 450, width: '100%', p: 2 }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSizeOptions={[5, 10, 25]}
          initialState={{
            pagination: { paginationModel: { pageSize: 10 } },
          }}
          disableRowSelectionOnClick
        />
      </Paper>
    </Box>
  );
}