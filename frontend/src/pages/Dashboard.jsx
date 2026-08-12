import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Grid, Card, CardContent, CardActions, Button, Paper } from '@mui/material';

export default function ReportsDashboard() {
  const navigate = useNavigate();

  const relatorios = [
    {
      id: 1,
      titulo: 'Análise de Compras',
      descricao: 'Avalie sugestões de reposição baseadas no histórico de vendas.',
      rota: '/reports/compras'
    },
    {
      id: 2,
      titulo: 'Famílias de Produtos',
      descricao: 'Análise detalhada por agrupamento de famílias cadastradas.',
      rota: '/reports/familias-produtos'
    },
    // Você pode adicionar os outros aqui
  ];

  return (
    <Box sx={{ width: '100%' }}>
      <Paper sx={{ p: 3, mb: 4, backgroundColor: 'primary.light', color: 'white' }}>
        <Typography variant="h4" component="h1" fontWeight="bold">
          Central de Relatórios
        </Typography>
        <Typography variant="subtitle1" sx={{ mt: 1 }}>
          Selecione abaixo o módulo que deseja acessar.
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {relatorios.map((relatorio) => (
          <Grid item xs={12} md={4} key={relatorio.id}>
            <Card elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2" fontWeight="bold">
                  {relatorio.titulo}
                </Typography>
                <Typography color="text.secondary">
                  {relatorio.descricao}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" variant="contained" onClick={() => navigate(relatorio.rota)}>
                  Acessar
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}