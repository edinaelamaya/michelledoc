import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TextEditor } from '../../components/TextEditor/TextEditor';
import { VoiceIndicator } from '../../components/VoiceIndicator/VoiceIndicator';
import { AIAssistant } from '../../components/AIAssistant/AIAssistant';
import { DocumentService } from '../../services/api';
import { useVoice } from '../../contexts/VoiceContext';
import './DocumentEditor.styles.css';

export default function DocumentEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { transcript, resetTranscript } = useVoice();
  const [document, setDocument] = useState({
    id: '',
    title: 'Nuevo Documento',
    content: '',
    createdAt: new Date().toISOString()
  });

  useEffect(() => {
    const fetchDocument = async () => {
      const docs = await DocumentService.getDocuments();
      const foundDoc = docs.find((doc: any) => doc.id === id);
      if (foundDoc) setDocument(foundDoc);
    };
    fetchDocument();
  }, [id]);

  useEffect(() => {
    const processVoiceCommand = () => {
      const titleMatch = transcript.match(/título\s(.+)/i);
      if (titleMatch) {
        setDocument(prev => ({ ...prev, title: titleMatch[1] }));
        resetTranscript();
      }
      if (transcript.includes('guardar documento')) {
        handleSaveDocument();
        resetTranscript();
      }
    };

    processVoiceCommand();
  }, [transcript]);

  const handleSaveDocument = async () => {
    try {
      if (document.id) {
        await DocumentService.updateDocument(parseInt(document.id), {
          title: document.title,
          content: document.content
        });
      } else {
        await DocumentService.createDocument({
          title: document.title,
          content: document.content
        });
      }
      navigate('/');
    } catch (error) {
      console.error('Error al guardar:', error);
    }
  };

  const handleAIGenerated = (text: string) => {
    setDocument(prev => ({
      ...prev,
      content: prev.content + '\n' + text
    }));
  };

  return (
    <div className="document-editor">
      <div className="voice-instructions">
        <h2>Comandos de voz disponibles:</h2>
        <div className="voice-commands">
          <span>Di "Título [nuevo título]" para cambiar el nombre</span>
          <span>Di "Guardar documento" para guardar</span>
          <span>Di "Generar [descripción]" para usar IA</span>
        </div>
      </div>

      <div className="editor-header">
        <input
          type="text"
          value={document.title}
          onChange={(e) => setDocument(prev => ({ ...prev, title: e.target.value }))}
          className="document-title-input"
          placeholder="Título del documento"
        />
        <button onClick={handleSaveDocument} className="save-button">
          <i className="bi bi-save"></i> Guardar
        </button>
      </div>

      <div className="editor-container">
        <TextEditor
          content={document.content}
          onChange={(content) => setDocument(prev => ({ ...prev, content }))}
        />
        <AIAssistant onGenerate={handleAIGenerated} />
      </div>
      
      <VoiceIndicator />
    </div>
  );
}