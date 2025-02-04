import { useVoiceCommands } from '../hooks/useVoiceCommands';

export const VoiceInput = ({ onInput }: { onInput: (text: string) => void }) => {
  const { transcript, isListening, startListening, stopListening } = useVoiceCommands();

  return (
    <div className="voice-controls">
      <button 
        onClick={isListening ? stopListening : startListening}
        className={isListening ? 'listening' : ''}
      >
        {isListening ? '🛑 Detener' : '🎤 Hablar'}
      </button>
      <div className="transcript">{transcript}</div>
    </div>
  );
};