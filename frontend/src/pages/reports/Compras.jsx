import { useState, useRef } from 'react';
import '../../css/reports/Compras.css';


function Compras() {
    // 1. Estado para as colunas dinâmicas da API (inicialmente vazio ou com valores padrão)
    const [dynamicColumns, setDynamicColumns] = useState([
        'Descrição', 'Último Fornecedor', 'Data Últ. Compra', 'Preço Médio' // Exemplo de colunas
    ]);

    // 2. Adicionado 'apiData' em cada linha para armazenar o retorno da API
    const [tableData, setTableData] = useState([
        { id: 1, cod_barra: '', qte: '', apiData: {} },
        { id: 2, cod_barra: '', qte: '', apiData: {} },
        { id: 3, cod_barra: '', qte: '', apiData: {} }
    ]);

    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    // Ref para armazenar os timers de cada campo independentemente
    const debounceTimers = useRef({});

    const handleChangeItem = (id, e) => {
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

    return (
        <div className='report-subpage compras'>
            <h2>Relatório de Compras</h2>
            <div className='filters'>
                <div className='date-filters'>
                    <label>
                        Data de Início:
                        <input type="date" id="start-date" value={startDate} onChange={handleChangeDate} />
                    </label>
                    <label>
                        Data de Fim:
                        <input type="date" id="end-date" value={endDate} onChange={handleChangeDate} />
                    </label>
                </div>
                
                <button type="button" className="btn btn-primary">Exportar Relatório</button>
            </div>
            <div className='report-content'>
                <div className="table-responsive table-scroll-container mt-4">
                    <table className="table table-striped table-bordered mb-0">
                        <thead className="table-light">
                            <tr>
                                {/* Classes CSS específicas para congelar as colunas */}
                                <th className="sticky-col col-1">Código</th>
                                <th className="sticky-col col-2">Qte</th>
                                
                                {/* 4. Renderizando as colunas dinâmicas */}
                                {dynamicColumns.map((colName, index) => (
                                    <th key={index}>{colName}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.map((row) => (
                                <tr key={row.id}>
                                    <td className="sticky-col col-1">
                                        <input
                                            type="text"
                                            name="cod_barra"
                                            className="form-control form-control-sm"
                                            value={row.cod_barra}
                                            onChange={(e) => handleChangeItem(row.id, e)}
                                            placeholder="Digite..."
                                        />
                                    </td>
                                    <td className="sticky-col col-2">
                                        <input
                                            type="number"
                                            name="qte"
                                            className="form-control form-control-sm"
                                            value={row.qte}
                                            onChange={(e) => handleChangeItem(row.id, e)}
                                            placeholder="Qte..."
                                        />
                                    </td>
                                    
                                    {/* 5. Renderizando as células dinâmicas baseadas no apiData */}
                                    {dynamicColumns.map((colName, index) => (
                                        <td key={index} className="api-data-cell">
                                            {/* Se a API ainda não preencheu, mostra um traço ou vazio */}
                                            {row.apiData[colName] || '-'}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Compras;