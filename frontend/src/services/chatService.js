import api from './api';

export const sendChatMessage = async (message) => {
  try {
    const response = await api.post('/ratoncito/chat/simple', { message });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};


export const sendReactChatMessage = async (message, history = [], siteContext = null) => {
  try {
    const payload = {
      message: message,
      chat_history: history.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }))
    };
    
    // Si hay contexto del sitio, añadirlo al mensaje
    if (siteContext && siteContext.name) {
      payload.message = `[Contexto: ${siteContext.name}] ${message}`;
    }
    
    const response = await api.post('/ratoncito/chat/react', payload);
    return response.data;
  } catch (error) {
    console.error('Error sending React chat message:', error);
    throw error;
  }
};