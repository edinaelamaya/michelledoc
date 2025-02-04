import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useVoice } from '../../contexts/VoiceContext';
// import './Profile.styles.css';

export default function Profile() {
  const { user } = useAuth();
  const { transcript } = useVoice();
  const [profileData, setProfileData] = useState({
    email: '',
    voiceSample: ''
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        email: user.email || '',
        voiceSample: user.voiceSample || ''
      });
    }
  }, [user]);

  useEffect(() => {
    const command = transcript.toLowerCase();
    if (command.includes('actualizar perfil')) handleSubmit();
  }, [transcript]);

  const handleSubmit = () => {
    // Lógica de actualización
  };

  return (
    <div className="profile-container">
      <h1>Configuración de Perfil</h1>
      
      <div className="profile-section">
        <div className="voice-sample">
          <h3>Muestra de Voz Registrada</h3>
          <audio controls src={profileData.voiceSample} />
        </div>

        <form className="profile-form">
          <div className="input-group">
            <label>Correo electrónico</label>
            <input
              type="email"
              value={profileData.email}
              onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
            />
          </div>

          <button 
            type="button"
            onClick={handleSubmit}
            className="update-button"
          >
            Actualizar Perfil
          </button>
        </form>
      </div>
    </div>
  );
}