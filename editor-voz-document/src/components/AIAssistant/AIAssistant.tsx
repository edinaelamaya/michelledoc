import { useState } from 'react';
import { useVoice } from '../../contexts/VoiceContext';
import './AIAssistant.styles.css';

interface AIAssistantProps {
  onGenerate: (text: string) => void;
}

export const AIAssistant = ({ onGenerate }: AIAssistantProps) => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const { transcript } = useVoice();

  const handleAIGenerate = async () => {
    try {
      setIsProcessing(true);
      // Aquí iría tu llamada a la API de IA (OpenAI, Cohere, etc.)
      const response = await fetch('TU_API_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      
      const data = await response.json();
      onGenerate(data.text);
      setPrompt('');
    } catch (error) {
      console.error('Error al generar texto:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="ai-assistant">
      <div className="ai-header">
        <h3>Asistente de IA</h3>
        <div className="ai-status">
          {isProcessing ? 'Procesando...' : 'Listo para ayudar'}
        </div>
      </div>

      <div className="ai-input-container">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe lo que quieres que escriba la IA..."
          className="ai-prompt-input"
        />
        <button 
          onClick={handleAIGenerate}
          disabled={isProcessing || !prompt}
          className="ai-generate-button"
        >
          <i className="bi bi-magic"></i>
          Generar
        </button>
      </div>

      <div className="ai-commands">
        <p>Comandos de voz:</p>
        <span>Di "Generar [tu descripción]"</span>
        <span>Di "Continuar texto" para expandir</span>
      </div>
    </div>
  );
};