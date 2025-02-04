import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthService } from '../services/api';

interface AuthContextType {
  user: any;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const profile = await AuthService.getProfile();
        setUser(profile);
      } catch (error) {
        localStorage.removeItem('voice_token');
      }
    };
    checkAuth();
  }, []);

  const login = async (credentials: { username: string; password: string }) => {
    const data = await AuthService.login(credentials);
    localStorage.setItem('voice_token', data.token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('voice_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);