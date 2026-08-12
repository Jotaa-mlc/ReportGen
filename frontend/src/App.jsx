import React from 'react';
import { 
  BrowserRouter,
  Routes,
  Route,
  Link,
  useLocation
} from 'react-router-dom';
import { 
  Box, 
  Toolbar, 
  CssBaseline, 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemText, 
  Typography, 
  Divider 
} from '@mui/material';

// Componentes Globais
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';
import NotFound from './pages/NotFound.jsx';

// Páginas de Relatórios
import Home from './pages/Home.jsx'; // Antigo Reports.jsx (Dashboard principal)
import Dashboard from './pages/Dashboard.jsx'; // Tela de cartões de relatórios
import ComprasDashboard from './pages/reports/ComprasDashboard.jsx'; // Nova tela de histórico
import Compras from './pages/reports/Compras.jsx'; // Tela detalhada com a tabela
import FamiliasProdutos from './pages/reports/FamiliasProdutos.jsx';
import FornecedorProdutos from './pages/reports/FornecedorProdutos.jsx';
import FornecedorFamilias from './pages/reports/FornecedorFamilias.jsx';

import './css/App.css';

const drawerWidth = 260;

// Criamos um subcomponente interno para termos acesso ao hook useLocation() do Router
function AppContent() {
  const location = useLocation();
  
  const menuItems = [
    { title: 'Dashboard', path: '/' },
    { title: 'Análise de Compras', path: '/compras' },
    { title: 'Famílias de Produtos', path: '/familias-produtos' },
    { title: 'Fornecedor x Produtos', path: '/fornecedor-produtos' },
    { title: 'Fornecedor x Famílias', path: '/fornecedor-familias' },
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      
      <Header />
      
      {/* Esse Toolbar atua como um 'espaçador' vertical global para o conteúdo que vem depois */}
      <Toolbar /> 

      {/* Container de Layout de duas colunas */}
      <Box sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1 }}>
        
        {/* Menu Lateral (Sidebar) fixo à esquerda */}
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          {/* O SEGREDO AQUI: Esse Toolbar empurra o conteúdo da sidebar para baixo da AppBar */}
          
          <Box sx={{ p: 3 }}>
            <Toolbar /> 
            <Typography variant="h6" fontWeight="bold" color="primary">
              Módulo Relatórios
            </Typography>
          </Box>
          <Divider />
          
          <List>
            {menuItems.map((item) => {
              // Verifica se a rota atual corresponde ao link do menu
              const isSelected = item.path === '/' 
                ? location.pathname === '/' 
                : location.pathname.startsWith(item.path);

              return (
                <ListItem key={item.title} disablePadding>
                  <ListItemButton 
                    component={Link} 
                    to={item.path}
                    selected={isSelected}
                  >
                    <ListItemText primary={item.title} />
                  </ListItemButton>
                </ListItem>
              );
            })}
          </List>
        </Drawer>

        {/* Área Principal Dinâmica (com padding aplicado aqui para as páginas não colarem nas bordas) */}
        <Box 
          component="main" 
          sx={{ 
            flexGrow: 1, 
            p: 3, 
            width: `calc(100% - ${drawerWidth}px)`,
            bgcolor: 'background.default' 
          }}
        >
          <Routes>
            {/* Rota raiz do módulo (Mostra os cartões/menu visual) */}
            <Route path="/" element={<Home />} />
            <Route index element={<Dashboard />} />
            
            {/* Histórico/Listagem das análises de compras */}
            <Route path="/compras" element={<ComprasDashboard />} />
            
            {/* Detalhe de uma análise específica (/compras/1, /compras/2, etc.) */}
            <Route path="/compras/:id" element={<Compras />} />
            
            {/* Outros Relatórios */}
            <Route path="/familias-produtos" element={<FamiliasProdutos />} />
            <Route path="/fornecedor-produtos" element={<FornecedorProdutos />} />
            <Route path="/fornecedor-familias" element={<FornecedorFamilias />} />

            <Route path="*" element={<NotFound />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}

// O componente raiz inicializa o Router
function App() {
  return (
    <BrowserRouter>
      <CssBaseline />
      <AppContent />
    </BrowserRouter>
  );
}

export default App;

// import Header from './components/Header.jsx';
// import Footer from './components/Footer.jsx';
// import NotFound from './pages/NotFound.jsx';

// import Home from './pages/Home.jsx';
// import Dashboard from './pages/Dashboard.jsx';
// import Compras from './pages/reports/Compras.jsx';
// import FamiliasProdutos from './pages/reports/FamiliasProdutos.jsx';
// import FornecedorProdutos from './pages/reports/FornecedorProdutos.jsx';
// import FornecedorFamilias from './pages/reports/FornecedorFamilias.jsx';

// import './css/App.css';
// import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
// import { Box, Toolbar, CssBaseline, Drawer, List, ListItem, ListItemButton, ListItemText, Typography, Divider } from '@mui/material';

// function App() {
//   const drawerWidth = 260; // Largura do menu lateral
  
//   // Lista de links para facilitar a manutenção
//   const menuItems = [
//     { title: 'Dashboard', path: '/' }, // Rota raiz do módulo
//     { title: 'Análise de Compras', path: '/compras' },
//     { title: 'Famílias de Produtos', path: '/familias-produtos' },
//     { title: 'Fornecedor x Produtos', path: '/fornecedor-produtos' },
//     { title: 'Fornecedor x Famílias', path: '/fornecedor-familias' },
//   ];
//   return (
//     <BrowserRouter>
//       <CssBaseline /> {/* Normaliza o CSS da página toda pro padrão MUI */}
//       <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        
//         <Header />

//         {/* Esse Toolbar atua como um 'espaçador' da altura exata do Header */}
//         <Toolbar /> 

//         {/* Menu Lateral (Sidebar) fixo à esquerda */}
//         <Box sx={{ display: 'flex', flexDirection: 'row', flexGrow: 1, p: 3 }}>
//           <Drawer
//             variant="permanent"
//             sx={{
//               width: drawerWidth,
//               flexShrink: 0,
//               [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
//             }}
//           >
//             <Box sx={{ p: 3 }}>
//               <Typography variant="h6" fontWeight="bold" color="primary">
//                 Módulo Relatórios
//               </Typography>
//             </Box>
//             <Divider />
            
//             <List>
//               {menuItems.map((item) => (
//                 <ListItem key={item.title} disablePadding>
//                   <ListItemButton 
//                     component={Link} 
//                     to={item.path}
//                     // Deixa o botão destacado se for a rota atual
//                     //selected={location.pathname === item.path || location.pathname === `${item.path}/`}
//                   >
//                     <ListItemText primary={item.title} />
//                   </ListItemButton>
//                 </ListItem>
//               ))}
//             </List>
//           </Drawer>
//           {/* Área Principal Dinâmica */}
//           <Box component="main" sx={{ display: 'flex', flexGrow: 1 }}>
//             <Routes>
//               <Route path="/" element={<Home />} />
//               <Route index element={<Dashboard />} />
              
//               {/* Sub-rotas de Compras */}
//               <Route path="compras">
//                 <Route index element={<Compras />} />
//                 {/* <Route path=":id" element={<Compras />} /> */}
//               </Route>
                

//               <Route path="*" element={<NotFound />} />
//             </Routes>
//           </Box>
//         </Box>
        
//         {/* <Footer /> Opcional: Se quiser que ele fique fixo no final */}
//       </Box>
//     </BrowserRouter>
//   )
// }

// export default App