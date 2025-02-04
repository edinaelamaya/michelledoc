import { Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};