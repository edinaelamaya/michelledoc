import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Configuración inicial de Axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('voice_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const AuthService = {
  login: async (credentials: { username: string; password: string }) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: { username: string; password: string; voiceSample?: string }) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  }
};

export const DocumentService = {
  createDocument: async (document: { title: string; content: string }) => {
    const response = await api.post('/documents', document);
    return response.data;
  },

  getDocuments: async () => {
    const response = await api.get('/documents');
    return response.data;
  },

  updateDocument: async (id: string, data: any) => {
    // Implementación mock
    const documents = JSON.parse(localStorage.getItem('documents') || '[]');
    const index = documents.findIndex((doc: any) => doc.id === id);
    if (index >= 0) {
      documents[index] = { ...documents[index], ...data };
      localStorage.setItem('documents', JSON.stringify(documents));
    }
    return { data: { success: true } };
  }
};

export const VoiceService = {
  processVoiceCommand: async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const response = await api.post('/voice/process', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }
};

export const OpenAIService = {
    generateText: async (data: { prompt: string; max_tokens: number }) => {
      // Implementación real usaría la API de OpenAI
      return {
        text: `Texto generado por IA basado en: "${data.prompt}".\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam...`,
        tokens_used: data.max_tokens
      };
    }
  };
