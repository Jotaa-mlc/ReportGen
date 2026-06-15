import './../css/Header.css';
import logo from './../assets/Logo Hidraucenter.png';

function Header() {
    return (
        <header>
            <img src={logo} alt="Hidraucenter Logo" className="logo" />
        </header>
    );
}

export default Header;