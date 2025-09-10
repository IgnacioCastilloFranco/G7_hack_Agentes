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

export const sendReactChatMessage = async (message) => {
  try {
    const response = await api.post('/ratoncito/chat/react', { message });
    return response.data;
  } catch (error) {
    console.error('Error sending React chat message:', error);
    throw error;
  }
};