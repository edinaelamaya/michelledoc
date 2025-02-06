import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useVoice } from '../../contexts/VoiceContext';
import { DocumentService } from '../../services/api';
import '../../components/DocumentList/DocumentList.styles.css';

interface Document {
  id: string;
  title: string;
  content: string;
  created_at: string;
}

export default function DocumentList() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const { transcript } = useVoice();

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const docs = await DocumentService.getDocuments();
        setDocuments(docs);
      } catch (error) {
        console.error('Error fetching documents:', error);
      }
    };
    fetchDocuments();
  }, []);

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
        {documents.map((doc) => (
          <div key={doc.id} className="document-card">
            <i className="bi bi-file-text document-icon"></i>
            <div className="document-info">
              <h3>{doc.title}</h3>
              <p className="document-preview">{doc.content.substring(0, 80)}...</p>
              <div className="document-footer">
                <span className="document-date">
                  <i className="bi bi-calendar"></i> {new Date(doc.created_at).toLocaleDateString()}
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