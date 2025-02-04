import { useState, useEffect } from 'react';
import { TextEditor } from '../components/TextEditor/TextEditor';
import { DocumentList } from '../components/DocumentList/DocumentList';
import { VoiceIndicator } from '../components/VoiceIndicator/VoiceIndicator';

// Datos quemados de ejemplo
const mockDocuments = [
  {
    id: '1',
    title: 'Mi Primer Documento',
    content: 'Este es un documento de ejemplo creado con voz',
    createdAt: '2023-10-20'
  },
  {
    id: '2',
    title: 'Notas Importantes',
    content: 'Recordar implementar la funcionalidad de IA',
    createdAt: '2023-10-21'
  }
];


export const Dashboard = () => {
  const [documents, setDocuments] = useState(mockDocuments);
  const [currentDoc, setCurrentDoc] = useState('');

  useEffect(() => {
    localStorage.setItem('documents', JSON.stringify(mockDocuments));
  }, []);
  

  const handleCreateDocument = () => {
    const newDoc = {
      id: Date.now().toString(),
      title: `Documento ${documents.length + 1}`,
      content: currentDoc,
      createdAt: new Date().toLocaleDateString()
    };
    setDocuments([...documents, newDoc]);
    setCurrentDoc('');
  };

  return (
    <div className="dashboard-container">
      <VoiceIndicator />
      
      <div className="editor-section">
        <h2>Nuevo Documento</h2>
        <TextEditor 
          content={currentDoc} 
          onChange={setCurrentDoc} 
        />
        <button 
          onClick={handleCreateDocument}
          className="create-button"
        >
          Crear Documento (o decir "Guardar documento")
        </button>
      </div>

      <div className="document-list-section">
        <h2>Tus Documentos</h2>
        <DocumentList documents={documents} />
      </div>
    </div>
  );
};