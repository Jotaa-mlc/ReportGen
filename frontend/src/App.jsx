import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';
import NotFound from './pages/NotFound.jsx';

import Reports from './pages/Reports.jsx';
import ReportsDashboard from './pages/reports/Dashboard.jsx';
import Compras from './pages/reports/Compras.jsx';
import FamiliasProdutos from './pages/reports/FamiliasProdutos.jsx';
import FornecedorProdutos from './pages/reports/FornecedorProdutos.jsx';
import FornecedorFamilias from './pages/reports/FornecedorFamilias.jsx';

import './css/App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {

  return (
    <div className="app-container">
      <Header />
      
      <BrowserRouter>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Reports />}>
              <Route index element={<ReportsDashboard />} />
              <Route path="compras" element={<Compras />} />
              <Route path="compras/:id" element={<Compras />} />
              <Route path="familias-produtos" element={<FamiliasProdutos />} />
              <Route path="fornecedor-produtos" element={<FornecedorProdutos />} />
              <Route path="fornecedor-familias" element={<FornecedorFamilias />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </BrowserRouter>
      
      <Footer />
    </div>
  )
}

export default App
