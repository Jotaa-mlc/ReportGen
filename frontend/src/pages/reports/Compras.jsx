import '../../css/reports/Compras.css';


function Compras() {
    return (
        <div className='report-subpage compras'>
            <h2>Relatório de Compras</h2>
            <div className='filters'>
                <label>
                    Data de Início:
                    <input type="date" name="start-date" />
                </label>
                <label>
                    Data de Fim:
                    <input type="date" name="end-date" />
                </label>
                <button type="button" className="btn btn-primary">Gerar Relatório</button>
            </div>
            <p>Aqui virá a sua tabela e o botão de exportar que implementamos na API!</p>
        </div>
    );
}

export default Compras;