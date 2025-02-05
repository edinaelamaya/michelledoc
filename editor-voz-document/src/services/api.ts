import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Configuración inicial de Axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

// Interceptor para añadir token JWT y logging
api.interceptors.request.use((config) => {
  console.log('Sending request to:', config.url, 'with data:', config.data);
  const token = localStorage.getItem('voice_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const AuthService = {
  login: async (credentials: { username: string; password: string }) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: { 
    username: string; 
    email: string;
    password: string; 
  }) => {
    try {
      console.log('Attempting to register user:', { ...userData, password: '****' });
      const response = await api.post('/auth/register', userData);
      console.log('Registration successful:', response.data);
      return response.data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  }
};

export const DocumentService = {
  createDocument: async (document: { title: string; content: string }) => {
    const response = await api.post('/api/documents', document);
    return response.data;
  },

  getDocuments: async () => {
    const response = await api.get('/api/documents');
    return response.data;
  },

  getDocument: async (id: number) => {
    const response = await api.get(`/api/documents/${id}`);
    return response.data;
  },

  updateDocument: async (id: number, document: { title: string; content: string }) => {
    const response = await api.put(`/api/documents/${id}`, document);
    return response.data;
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
