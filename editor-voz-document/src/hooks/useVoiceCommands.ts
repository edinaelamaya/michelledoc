import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

export const useVoiceCommands = () => {
  const navigate = useNavigate();
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(true);

  const processCommand = useCallback((command: string) => {
    const cleanCommand = command.toLowerCase().trim();
    // Dentro de processCommand
    if (cleanCommand.includes('guardar documento')) {
        const saveEvent = new Event('saveDocument');
        window.dispatchEvent(saveEvent);
    }
    
    if (cleanCommand.includes('nuevo documento')) {
        const newDocEvent = new Event('newDocument');
        window.dispatchEvent(newDocEvent);
    }

    if (cleanCommand.includes('nuevo documento')) {
        navigate('/new-document');
    }
    
    if (cleanCommand.includes('formato negrita')) {
        document.execCommand('bold');
    }
    
    if (cleanCommand.includes('formato cursiva')) {
        document.execCommand('italic');
    }
    
    if (cleanCommand.includes('guardar documento')) {
        window.dispatchEvent(new Event('saveDocument'));
    }
    
    // Comandos de navegación
    if (cleanCommand.includes('iniciar sesión')) navigate('/login');
    if (cleanCommand.includes('registrarse')) navigate('/register');
    if (cleanCommand.includes('documentos')) navigate('/dashboard');
    if (cleanCommand.includes('perfil')) navigate('/profile');
    
    return cleanCommand;
  }, [navigate]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.error('Speech recognition no soportado');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = (event) => {
      const current = event.resultIndex;
      const transcript = event.results[current][0].transcript;
      setTranscript(transcript);
      processCommand(transcript);
    };

    recognition.onerror = (event) => {
      console.error('Error de reconocimiento:', event.error);
    };

    recognition.start();
    
    return () => {
      recognition.stop();
    };
  }, [processCommand]);

  return { 
    transcript,
    isListening,
    resetTranscript: () => setTranscript('')
  };
};