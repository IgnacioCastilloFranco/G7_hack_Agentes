import api from './api';

/**
 * Esta es ahora la ÚNICA función que necesitamos para comunicarnos con el backend.
 * Envía un mensaje al agente del Ratoncito Pérez y gestiona la sesión.
 * @param {string} message - El mensaje del usuario.
 * @param {string} sessionId - El ID único para la sesión de chat actual.
 * @returns {Promise<object>} La respuesta del agente.
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