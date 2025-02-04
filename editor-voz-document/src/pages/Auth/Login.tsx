import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useVoice } from '../../contexts/VoiceContext';
import './Login.styles.css';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isAuthenticated } = useAuth();
  const { transcript } = useVoice();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) navigate('/');
  }, [isAuthenticated]);

  useEffect(() => {
    const processVoiceCommand = () => {
      const command = transcript.toLowerCase();
      const userMatch = command.match(/usuario\s(.+)/);
      const passMatch = command.match(/contraseña\s(.+)/);
      
      if (userMatch) setUsername(userMatch[1]);
      if (passMatch) setPassword(passMatch[1]);
      if (command.includes('ingresar')) handleSubmit();
    };

    processVoiceCommand();
  }, [transcript]);

  const handleSubmit = async () => {
    try {
      await login({ username, password });
    } catch (error) {
      setError('Credenciales incorrectas');
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="voice-instructions">
          <h1>Bienvenido de vuelta</h1>
          <p className="voice-guide">Comandos de voz disponibles:</p>
          <div className="voice-commands">
            <span>Di "Usuario [tu nombre]"</span>
            <span>Di "Contraseña [tu clave]"</span>
            <span>Di "Ingresar" para continuar</span>
          </div>
        </div>

        <form className="login-form">
          <div className="input-group">
            <label>Usuario</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Dicta tu usuario"
            />
          </div>

          <div className="input-group">
            <label>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Dicta tu contraseña"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="button"
            onClick={handleSubmit}
            className="login-button"
          >
            Ingresar con Voz
          </button>

          <div className="auth-links">
            <p>¿No tienes una cuenta?</p>
            <Link to="/register" className="register-link">
              Registrarse con voz
            </Link>
          </div>
        </form>
      </div>
      
      <div className="login-graphics">
        <div className="gradient-overlay" />
        <div className="voice-animation">
          <div className="pulse-circle"></div>
          <div className="pulse-circle delay-1"></div>
          <div className="pulse-circle delay-2"></div>
          <div className="mic-icon">🎤</div>
        </div>
        <p className="graphics-text">Habla para comenzar</p>
      </div>
    </div>
  );
};