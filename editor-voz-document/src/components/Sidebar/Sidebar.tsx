import { Link } from 'react-router-dom';
import { useVoice } from '../../contexts/VoiceContext';
import './Sidebar.styles.css';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar = ({ isOpen}: SidebarProps) => {
  const { transcript } = useVoice();

  return (
    <aside className='sidebar '>
      <nav className="sidebar-nav">
        <Link to="/" className={transcript.includes('inicio') ? 'active' : ''}>
          <i className="bi bi-house"></i>
          Inicio
        </Link>
        <Link 
          to="/documents" 
          className={transcript.includes('documentos') ? 'active' : ''}
        >
          <i className="bi bi-files"></i>
          Mis Documentos
        </Link>
        <Link 
          to="/profile" 
          className={transcript.includes('perfil') ? 'active' : ''}
        >
          <i className="bi bi-person"></i>
          Perfil
        </Link>
      </nav>
    </aside>
  );
};