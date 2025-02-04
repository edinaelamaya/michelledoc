import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { VoiceProvider } from './contexts/VoiceContext';
import  Layout  from './components/Layout/Layout';
import HomePage from './pages/Documents/HomePage';
import DocumentList from './pages/Documents/DocumentList';
import DocumentEdit from './pages/Documents/DocumentEditor';
import {Login} from './pages/Auth/Login';
import {Register} from './pages/Auth/Register';
import Profile from './pages/Profile/Profile';

function App() {
  return (
    <BrowserRouter>
      <VoiceProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

            <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/documents" element={<DocumentList />} />
            <Route path="/documents/:id" element={<DocumentEdit />} />
            <Route path="/documents/new" element={<DocumentEdit />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Routes>
      </VoiceProvider>
    </BrowserRouter>
  );
}
export default App