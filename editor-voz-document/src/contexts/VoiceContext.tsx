import { createContext, useContext } from 'react';
import { useVoiceCommands } from '../hooks/useVoiceCommands';

export const VoiceContext = createContext<ReturnType<typeof useVoiceCommands>>(
  {} as ReturnType<typeof useVoiceCommands>
);

export const VoiceProvider = ({ children }: { children: React.ReactNode }) => {
  const voice = useVoiceCommands();
  return <VoiceContext.Provider value={voice}>{children}</VoiceContext.Provider>;
};

export const useVoice = () => useContext(VoiceContext);