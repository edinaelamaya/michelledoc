import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
// import { useAuth } from '../../contexts/AuthContext';
import { useVoice } from '../../contexts/VoiceContext';
import './Register.styles.css';
import { AuthService } from '../../services/api';

export const Register = () => {
  const [userData, setUserData] = useState({
    username: '',
    password: '',
    email: ''
  });
  const [error, setError] = useState('');
  const { transcript } = useVoice();
  const navigate = useNavigate();

  useEffect(() => {
    const processCommand = () => {
      const command = transcript.toLowerCase();
      const userMatch = command.match(/usuario\s(.+)/);
      const passMatch = command.match(/contraseña\s(.+)/);
      const emailMatch = command.match(/correo\s(.+)/);
      
      if (userMatch) setUserData(prev => ({ ...prev, username: userMatch[1] }));
      if (passMatch) setUserData(prev => ({ ...prev, password: passMatch[1] }));
      if (emailMatch) setUserData(prev => ({ ...prev, email: emailMatch[1] }));
      if (command.includes('registrar')) handleSubmit();
    };

    processCommand();
  }, [transcript]);

  const handleSubmit = async () => {
    try {
      // Validaciones básicas
      if (!userData.username || !userData.email || !userData.password) {
        setError('Todos los campos son requeridos');
        return;
      }

      // Llamada al API de registro
      const response = await AuthService.register({
        username: userData.username,
        email: userData.email,
        password: userData.password
      });

      if (response) {
        // Registro exitoso
        navigate('/login', { 
          state: { message: 'Registro exitoso. Por favor inicia sesión.' }
        });
      }
    } catch (error: any) {
      // Manejo de errores específicos
      const errorMessage = error.response?.data?.detail || 'Error en el registro';
      setError(errorMessage);
    }
  };

  return (
    <div className="register-container">
      <div className="register-content">
        <div className="voice-instructions">
          <h1>Crea tu cuenta</h1>
          <p className="voice-guide">Comandos de voz disponibles:</p>
          <div className="voice-commands">
            <span>Di "Usuario [tu nombre]"</span>
            <span>Di "Correo [tu@email.com]"</span>
            <span>Di "Contraseña [tu clave]"</span>
            <span>Di "Registrar" para continuar</span>
          </div>
        </div>

        <form className="register-form">
          <div className="input-group">
            <label>Usuario</label>
            <input
              type="text"
              value={userData.username}
              onChange={(e) => setUserData(prev => ({ ...prev, username: e.target.value }))}
            />
          </div>

          <div className="input-group">
            <label>Correo electrónico</label>
            <input
              type="email"
              value={userData.email}
              onChange={(e) => setUserData(prev => ({ ...prev, email: e.target.value }))}
            />
          </div>

          <div className="input-group">
            <label>Contraseña</label>
            <input
              type="password"
              value={userData.password}
              onChange={(e) => setUserData(prev => ({ ...prev, password: e.target.value }))}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="button"
            onClick={handleSubmit}
            className="register-button"
          >
            Registrarse con Voz
          </button>

          <div className="auth-links">
            <p>¿Ya tienes una cuenta?</p>
            <Link to="/login" className="login-link">
              Ingresar con voz
            </Link>
          </div>
        </form>
      </div>
      
      <div className="register-graphics">
        <div className="gradient-overlay" />
        <div className="voice-animation">
          <div className="pulse-circle"></div>
          <div className="pulse-circle delay-1"></div>
          <div className="pulse-circle delay-2"></div>
          <div className="mic-icon">🎤</div>
        </div>
        <p className="graphics-text">Tu voz es tu llave de acceso</p>
      </div>
    </div>
  );
};