import { Link } from 'react-router-dom';
import './DocumentList.styles.css';
interface Document {
    id: string;
    title: string;
    content: string;
    createdAt: string;
  }
  
  export const DocumentList = ({ documents }: { documents: Document[] }) => {
    return (
        
      <div className="document-grid">
        {documents.map((doc) => (
          <div key={doc.id} className="document-card">
            <h3>{doc.title}</h3>
            <div className="document-preview">
              {doc.content.substring(0, 100)}...
            </div>
            <div className="document-meta">
              <span>📅 {doc.createdAt}</span>
              <button className="open-document">
                Abrir Documento
              </button>
            </div>
            <Link to={`/documents/${doc.id}`} className="open-document">
                Abrir Documento
            </Link>
          </div>
          
        ))}
      </div>
    );
  };