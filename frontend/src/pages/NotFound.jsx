import '../css/NotFound.css';

function NotFound() {
    return (
        <div id="not-found-page">
            <h2>404</h2>
            <h1>Página Não Encontrada</h1>
            <p>Desculpe, a página que você está procurando não existe.</p>
            <p>Você pode voltar para a <a href="/">página inicial</a>.</p>
        </div>
    );
}

export default NotFound;