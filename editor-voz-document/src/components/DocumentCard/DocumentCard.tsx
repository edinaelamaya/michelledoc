import { Link } from 'react-router-dom';
import './DocumentCard.styles.css';

interface DocumentCardProps {
  id: string;
  title: string;
  content: string;
  date: string;
}

export const DocumentCard = ({ id, title, content, date }: DocumentCardProps) => {
  return (
    <div className="document-card">
      <div className="card-header">
        <h3>{title}</h3>
        <span className="document-date">{date}</span>
      </div>
      <p className="document-preview">{content.substring(0, 100)}...</p>
      <div className="card-actions">
        <Link to={`/documents/${id}`} className="open-link">
          <i className="bi bi-pencil"></i>
          Editar
        </Link>
        <button className="delete-btn">
          <i className="bi bi-trash"></i>
        </button>
      </div>
    </div>
  );
};