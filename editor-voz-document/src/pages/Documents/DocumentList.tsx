import { Link } from 'react-router-dom';
import { useVoice } from '../../contexts/VoiceContext';
import '../../components/DocumentList/DocumentList.styles.css';

const mockDocuments = [
  { id: '1', title: 'Proyecto Final', content: '...', date: '2024-03-15' },
  { id: '2', title: 'Notas Reunión', content: '...', date: '2024-03-14' },
];

export default function DocumentList() {
  const { transcript } = useVoice();

  return (
    <div className="documents-container">
      <div className="voice-instructions">
        <h2>Comandos de voz disponibles:</h2>
        <div className="voice-commands">
          <span>Di "Nuevo documento" para crear</span>
          <span>Di "Abrir documento [número]" para abrir</span>
          <span>Di "Buscar [término]" para filtrar</span>
        </div>
      </div>

      <div className="documents-header">
        <h1>Mis Documentos</h1>
        <Link to="/documents/new" className="new-document-button">
          <i className="bi bi-plus-lg"></i>
          Nuevo Documento
        </Link>
      </div>

      <div className="documents-grid">
        {mockDocuments.map((doc, index) => (
          <div key={doc.id} className="document-card">
            <i className="bi bi-file-text document-icon"></i>
            <div className="document-info">
              <h3>{doc.title}</h3>
              <p className="document-preview">{doc.content.substring(0, 80)}...</p>
              <div className="document-footer">
                <span className="document-date">
                  <i className="bi bi-calendar"></i> {doc.date}
                </span>
                <Link to={`/documents/${doc.id}`} className="open-button">
                  <i className="bi bi-box-arrow-up-right"></i> Abrir
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}