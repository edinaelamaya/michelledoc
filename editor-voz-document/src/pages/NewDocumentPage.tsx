import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextEditor } from '../components/TextEditor/TextEditor';
import { VoiceIndicator } from '../components/VoiceIndicator/VoiceIndicator';
import { AIAssistant } from '../components/IAAssistant/AIAssistant';
import { DocumentService } from '../services/api';

export const NewDocumentPage = () => {
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const navigate = useNavigate();

  const handleSave = async () => {
    await DocumentService.createDocument({
      title: title || 'Documento sin título',
      content
    });
    navigate('/');
  };

  return (
    <div className="document-page">
      <VoiceIndicator />
      <AIAssistant onGenerate={(text) => setContent(prev => prev + text)} />
      
      <div className="document-header">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Título del documento"
          className="document-title"
        />
        <button onClick={handleSave} className="save-button">
          💾 Guardar
        </button>
      </div>

      <TextEditor content={content} onChange={setContent} />
    </div>
  );
};