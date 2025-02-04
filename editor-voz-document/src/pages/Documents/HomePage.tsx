import { useState, useEffect } from 'react';
import { useVoice } from '../../contexts/VoiceContext';
import { TextEditor } from '../../components/TextEditor/TextEditor';
import { AIAssistant } from '../../components/AIAssistant/AIAssistant';
import './HomePage.styles.css';

export default function HomePage() {
  const [content, setContent] = useState('');
  const { transcript } = useVoice();

  useEffect(() => {
    if (transcript) {
      setContent(prev => `${prev} ${transcript}`);
    }
  }, [transcript]);

  return (
    <div className="home-container">
      <div className="editor-header">
        <h1>Nuevo Documento</h1>
        <AIAssistant onGenerate={(text) => setContent(prev => prev + text)} />
      </div>
      
      <TextEditor content={content} onChange={setContent} />
      
      <div className="voice-commands-hint">
        <p>Comandos disponibles:</p>
        <ul>
          <li>"Guardar documento"</li>
          <li>"Formato negrita"</li>
          <li>"Nuevo documento"</li>
          <li>"Mis documentos"</li>
        </ul>
      </div>
    </div>
  );
}