import { useState, useCallback, useRef, useEffect } from 'react';
import { ttsService } from '../services/ttsService';

/**
 * Hook personalizado para manejar Text-to-Speech
 * @param {Object} defaultOptions - Opciones por defecto para TTS
 * @returns {Object} Estado y funciones para TTS
 */
export const useTTS = (defaultOptions = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  
  const audioRef = useRef(null);
  const currentTextRef = useRef('');

  // Opciones por defecto
  const options = {
    voice_id: 'iFhPOZcajR7W3sDL39qJ',
    stability: 0.6,
    similarity_boost: 0.8,
    speed: 1.0,
    model_id: 'eleven_multilingual_v2',
    ...defaultOptions
  };

  /**
   * Reproduce un texto
   */
  const speak = useCallback(async (text, customOptions = {}) => {
    if (!text || text.trim() === '') {
      setError('No hay texto para reproducir');
      return false;
    }

    // Si ya está reproduciendo el mismo texto, pausar
    if (isPlaying && currentTextRef.current === text) {
      pause();
      return true;
    }

    setIsLoading(true);
    setError(null);
    setProgress(0);
    currentTextRef.current = text;

    try {
      // Detener audio anterior si existe
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }

      // Generar nuevo audio
      const audioBlob = await ttsService.textToSpeech(text, {
        ...options,
        ...customOptions
      });

      const audioUrl = URL.createObjectURL(audioBlob);
      audioRef.current = new Audio(audioUrl);

      // Configurar eventos del audio
      audioRef.current.addEventListener('loadstart', () => {
        setIsLoading(true);
      });

      audioRef.current.addEventListener('canplay', () => {
        setIsLoading(false);
      });

      audioRef.current.addEventListener('play', () => {
        setIsPlaying(true);
        setError(null);
      });

      audioRef.current.addEventListener('pause', () => {
        setIsPlaying(false);
      });

      audioRef.current.addEventListener('ended', () => {
        setIsPlaying(false);
        setProgress(100);
        URL.revokeObjectURL(audioUrl);
        currentTextRef.current = '';
      });

      audioRef.current.addEventListener('timeupdate', () => {
        if (audioRef.current) {
          const progress = (audioRef.current.currentTime / audioRef.current.duration) * 100;
          setProgress(progress || 0);
        }
      });

      audioRef.current.addEventListener('error', (e) => {
        console.error('Error reproduciendo audio:', e);
        setError('Error reproduciendo el audio');
        setIsPlaying(false);
        setIsLoading(false);
        URL.revokeObjectURL(audioUrl);
      });

      // Reproducir
      await audioRef.current.play();
      return true;

    } catch (err) {
      console.error('Error en TTS:', err);
      setError(err.message || 'Error generando audio');
      setIsLoading(false);
      setIsPlaying(false);
      return false;
    }
  }, [options, isPlaying]);

  /**
   * Pausa la reproducción actual
   */
  const pause = useCallback(() => {
    if (audioRef.current && !audioRef.current.paused) {
      audioRef.current.pause();
    }
  }, []);

  /**
   * Reanuda la reproducción
   */
  const resume = useCallback(() => {
    if (audioRef.current && audioRef.current.paused) {
      audioRef.current.play().catch(err => {
        console.error('Error reanudando audio:', err);
        setError('Error reanudando la reproducción');
      });
    }
  }, []);

  /**
   * Detiene completamente la reproducción
   */
  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setProgress(0);
    }
  }, []);

  /**
   * Cambia el volumen (0-1)
   */
  const setVolume = useCallback((volume) => {
    if (audioRef.current) {
      audioRef.current.volume = Math.max(0, Math.min(1, volume));
    }
  }, []);

  /**
   * Limpia recursos al desmontar
   */
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        if (audioRef.current.src) {
          URL.revokeObjectURL(audioRef.current.src);
        }
      }
    };
  }, []);

  return {
    // Estado
    isLoading,
    isPlaying,
    error,
    progress,
    
    // Funciones
    speak,
    pause,
    resume,
    stop,
    setVolume,
    
    // Utilidades
    canSpeak: !isLoading,
    currentText: currentTextRef.current,
    
    // Función de conveniencia para toggle play/pause
    toggle: useCallback((text, customOptions) => {
      if (isPlaying && currentTextRef.current === text) {
        pause();
      } else {
        speak(text, customOptions);
      }
    }, [speak, pause, isPlaying])
  };
};

export default useTTS;