import { Link, Outlet } from "react-router-dom";
import "../css/Reports.css";

function Reports() {
    return (
        <div className="reports-page">
            <ul className="nav nav-pills flex-column">
                <li className="nav-item"><Link className="nav-link" to="/reports">Relatórios</Link></li>
                <li className="nav-item"><Link className="nav-link" to="compras">Compras</Link></li>
                <li className="nav-item"><Link className="nav-link" to="familias-produtos">Familias de Produtos</Link></li>
                <li className="nav-item"><Link className="nav-link" to="fornecedor-produtos">Fornecedor x Produtos</Link></li>
            </ul>
            <div className="content">
                <Outlet />
            </div>
        </div>
    );
}

export default Reports;