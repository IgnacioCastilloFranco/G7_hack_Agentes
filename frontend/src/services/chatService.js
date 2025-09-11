import api from './api';

/**
 * @param {string} message - 
 * @param {string} sessionId - 
 * @returns {Promise<object>} 
 */
export const sendMessageToRatoncito = async (message, sessionId) => {
  try {
    const response = await api.post('/ratoncito/chat', {
      message: message,
      session_id: sessionId,
    });
    return response.data;
  } catch (error) {
    console.error('Error al enviar el mensaje al Ratoncito Pérez:', error);
    throw error;
  }
};

export const speakText = async (text) => {
  try {
    const response = await api.post('/ratoncito/speak', 
      { text: text },
      { responseType: 'blob' }
    );
    
    const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
    return URL.createObjectURL(audioBlob);

  } catch (error) {
    console.error('Error al generar el audio:', error);
    throw error;
  }
};
