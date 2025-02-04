import { useVoice } from '../../contexts/VoiceContext';
import './VoiceIndicator.styles.css';

export const VoiceIndicator = () => {
  const { isListening, transcript } = useVoice();

  return (
    <div className="voice-indicator-container">
      <div className={`voice-status ${isListening ? 'listening' : ''}`}>
        <div className="mic-icon">
          {isListening ? '🎤' : '🎤'}
        </div>
        <div className="pulse-effect"></div>
      </div>
      
      <div className="transcript-box">
        <p>{transcript || "Di un comando..."}</p>
      </div>
    </div>
  );
};