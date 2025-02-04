import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useVoice } from '../../contexts/VoiceContext';
import './Navbar.styles.css';

interface NavbarProps {
  onMenuToggle: () => void;
}

export const Navbar = ({ onMenuToggle }: NavbarProps) => {
  const { user, logout } = useAuth();
  const { isListening } = useVoice();

  return (
    <nav className={`navbar ${isListening ? 'voice-active' : ''}`}>
      <div className="navbar-left">
        <button 
          className="hamburger-btn"
          onClick={onMenuToggle}
          aria-label="Menú"
        >
          <i className="bi bi-list"></i>
        </button>
        <Link to="/" className="app-logo">
          <span>Michelle</span>Doc
        </Link>
      </div>

      <div className="navbar-right">
        {user && (
          <button 
            onClick={logout}
            className="logout-btn"
            aria-label="Cerrar sesión"
          >
            <i className="bi bi-box-arrow-right"></i>
            Salir
          </button>
        )}
      </div>
    </nav>
  );
};