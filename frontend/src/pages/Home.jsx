import React from 'react';
import { Link, Outlet, useLocation } from "react-router-dom";
import { Box, Drawer, List, ListItem, ListItemButton, ListItemText, Typography, Divider } from '@mui/material';

const drawerWidth = 260; // Largura do menu lateral

export default function Reports() {
  const location = useLocation(); // Usado para saber qual página está ativa

  // Lista de links para facilitar a manutenção
  const menuItems = [
    { title: 'Dashboard', path: '/' }, // Rota raiz do módulo
    { title: 'Análise de Compras', path: '/compras' },
    { title: 'Famílias de Produtos', path: '/familias-produtos' },
    { title: 'Fornecedor x Produtos', path: '/fornecedor-produtos' },
    { title: 'Fornecedor x Famílias', path: '/fornecedor-familias' },
  ];

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      
      {/* Menu Lateral (Sidebar) fixo à esquerda */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Box sx={{ p: 3 }}>
          <Typography variant="h6" fontWeight="bold" color="primary">
            Módulo Relatórios
          </Typography>
        </Box>
        <Divider />
        
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.title} disablePadding>
              <ListItemButton 
                component={Link} 
                to={item.path}
                // Deixa o botão destacado se for a rota atual
                selected={location.pathname === item.path || location.pathname === `${item.path}/`}
              >
                <ListItemText primary={item.title} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>

      {/* Área Principal onde as páginas (como Compras.jsx) vão renderizar */}
      <Box 
        component="main" 
        sx={{ 
          flexGrow: 1, 
          bgcolor: 'background.default', 
          p: 3,
          overflow: 'auto' // Permite rolagem apenas no conteúdo, não no menu
        }}
      >
        <Outlet />
      </Box>

    </Box>
  );
}