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


export const sendReactChatMessage = async (message, history = []) => {
  try {
    const response = await api.post('/ratoncito/chat/react', {
      message: message,
      chat_history: history.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }))
    });
    return response.data;
  } catch (error) {
    console.error('Error sending React chat message:', error);
    throw error;
  }
};