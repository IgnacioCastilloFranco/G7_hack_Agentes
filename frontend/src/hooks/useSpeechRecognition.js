import { useState, useEffect, useRef } from 'react';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const isSupported = !!SpeechRecognition;

export const useSpeechRecognition = () => {
  const [isListening, setIsListening] = useState(false);
  const [text, setText] = useState('');
  const recognitionRef = useRef(null);

  useEffect(() => {
    if (!isSupported) {
      console.warn('El reconocimiento de voz no está soportado en este navegador.');
      return;
    }

    recognitionRef.current = new SpeechRecognition();
    const recognition = recognitionRef.current;
    
    recognition.continuous = false; 
    recognition.lang = 'es-ES';     
    recognition.interimResults = false; 

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.error('Error en el reconocimiento de voz:', event.error);
      setIsListening(false);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim();
      setText(transcript);
    };

  }, []); 

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setText(''); 
      recognitionRef.current.start();
    }
  };

  return {
    isListening,
    text,
    startListening,
    isSupported,
  };
};