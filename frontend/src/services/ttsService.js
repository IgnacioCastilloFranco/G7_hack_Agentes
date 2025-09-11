import api from './api';

/**
 * Servicio para convertir texto a voz usando ElevenLabs
 */
export class TTSService {
  constructor() {
    this.audioCache = new Map(); // Cache para evitar regenerar audios
    this.audioStorage = new Map(); // Storage para URLs de audios guardados
  }

  /**
   * Genera un nombre único para el archivo de audio
   * @param {string} text - Texto del audio
   * @returns {string} Nombre del archivo
   */
  generateAudioFileName(text) {
    const hash = btoa(text.substring(0, 50)).replace(/[^a-zA-Z0-9]/g, '').substring(0, 10);
    const timestamp = Date.now();
    return `ratoncito_${hash}_${timestamp}.mp3`;
  }

  /**
   * Guarda el audio en la carpeta local
   * @param {Blob} audioBlob - Blob del audio
   * @param {string} fileName - Nombre del archivo
   * @returns {string} URL del archivo guardado
   */
  saveAudioLocally(audioBlob, fileName) {
    const audioUrl = URL.createObjectURL(audioBlob);
    this.audioStorage.set(fileName, audioUrl);
    return audioUrl;
  }

  /**
   * Convierte texto a audio y retorna un blob
   * @param {string} text - Texto a convertir
   * @param {object} options - Opciones de voz
   * @returns {Promise<Blob>} Blob del audio
   */
  async textToSpeech(text, options = {}) {
    try {
      // Verificar cache
      const cacheKey = `${text}_${JSON.stringify(options)}`;
      if (this.audioCache.has(cacheKey)) {
        return this.audioCache.get(cacheKey);
      }

      const response = await api.post('/ratoncito/speak', {
        text,
        voice_id: options.voice_id || 'iFhPOZcajR7W3sDL39qJ', // ID de voz específico del Ratoncito Pérez
        model_id: options.model_id || 'eleven_multilingual_v2',
        stability: options.stability || 0.6,
        similarity_boost: options.similarity_boost || 0.8,
        speed: options.speed || 1.0
      }, {
        responseType: 'blob' // Importante para recibir el archivo de audio
      });

      const audioBlob = response.data;
      
      // Generar nombre de archivo y guardar localmente
      const fileName = this.generateAudioFileName(text);
      this.saveAudioLocally(audioBlob, fileName);
      
      // Guardar en cache (máximo 10 audios)
      if (this.audioCache.size >= 10) {
        const firstKey = this.audioCache.keys().next().value;
        this.audioCache.delete(firstKey);
      }
      this.audioCache.set(cacheKey, audioBlob);

      console.log(`Audio guardado: ${fileName}`);
      return audioBlob;
    } catch (error) {
      console.error('Error en TTS:', error);
      throw new Error('No se pudo generar el audio. ¿Está el Ratoncito durmiendo?');
    }
  }

  /**
   * Reproduce un texto directamente
   * @param {string} text - Texto a reproducir
   * @param {object} options - Opciones de voz
   * @returns {Promise<HTMLAudioElement>} Elemento de audio
   */
  async playText(text, options = {}) {
    try {
      const audioBlob = await this.textToSpeech(text, options);
      const audioUrl = URL.createObjectURL(audioBlob);
      
      const audio = new Audio(audioUrl);
      
      // Limpiar URL cuando termine la reproducción
      audio.addEventListener('ended', () => {
        URL.revokeObjectURL(audioUrl);
      });
      
      await audio.play();
      return audio;
    } catch (error) {
      console.error('Error reproduciendo audio:', error);
      throw error;
    }
  }

  /**
   * Obtiene las voces disponibles
   * @returns {Promise<Array>} Lista de voces
   */
  async getAvailableVoices() {
    try {
      const response = await api.get('/ratoncito/voices');
      return response.data.voices || [];
    } catch (error) {
      console.error('Error obteniendo voces:', error);
      return [];
    }
  }

  /**
   * Limpia el cache de audios
   */
  clearCache() {
    this.audioCache.clear();
  }

  /**
   * Limpia los audios almacenados localmente
   */
  clearStoredAudios() {
    // Revocar todas las URLs para liberar memoria
    for (const url of this.audioStorage.values()) {
      URL.revokeObjectURL(url);
    }
    this.audioStorage.clear();
  }

  /**
   * Obtiene la lista de audios guardados
   * @returns {Array} Lista de nombres de archivos de audio
   */
  getStoredAudios() {
    return Array.from(this.audioStorage.keys());
  }
}

// Instancia singleton del servicio
export const ttsService = new TTSService();

// Función de conveniencia para uso directo
export const playRatoncitoAudio = async (text, options = {}) => {
  return await ttsService.playText(text, options);
};

export default ttsService;