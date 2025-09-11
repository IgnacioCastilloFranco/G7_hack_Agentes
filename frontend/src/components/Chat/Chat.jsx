import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  Container,
  CircularProgress,
  Avatar 
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

// Importamos el nuevo servicio unificado
import { sendMessageToRatoncito } from '../../services/chatService';
import AudioButton from './AudioButton';

// Componente para mostrar cada mensaje en el chat
const ChatMessage = ({ message, isUser }) => (
    <Box sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', mb: 2, alignItems: 'flex-start' }}>
        {!isUser && (
            <Avatar 
                src="/images/ratoncito.png" 
                alt="Ratoncito Pérez" 
                sx={{ width: 40, height: 40, mr: 1, mt: 0.5 }}
            />
        )}
        <Box sx={{ display: 'flex', flexDirection: 'column', maxWidth: '80%' }}>
            <Paper
                elevation={3}
                sx={{
                    p: '10px 15px',
                    borderRadius: isUser ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
                    backgroundColor: isUser ? 'primary.main' : 'secondary.main',
                    color: 'white',
                }}
            >
                {/* Usamos pre-wrap para respetar los saltos de línea del backend */}
                <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{message}</Typography>
            </Paper>
            {!isUser && (
                 <Box sx={{ 
                     mt: 1, 
                     ml: 1, 
                     display: 'flex', 
                     justifyContent: 'flex-start',
                     backgroundColor: 'rgba(25, 118, 210, 0.1)',
                     borderRadius: '8px',
                     padding: '4px'
                 }}>
                     <AudioButton 
                         text={message} 
                         size="medium" 
                         color="primary" 
                         showProgress={true}
                     />
                 </Box>
             )}
        </Box>
    </Box>
);

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(''); 
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  // Estado para almacenar el ID de sesión único
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Generamos un ID de sesión único cuando el componente se monta
  useEffect(() => {
    setSessionId(crypto.randomUUID());
  }, []);
  
  // Efecto para enviar un saludo inicial al backend y empezar la conversación
  useEffect(() => {
    const startConversation = async (sid) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await sendMessageToRatoncito("hola", sid);
            setMessages([{ sender: 'ratoncito', text: response.response }]);
        } catch {
            setError("¡Uy! No encuentro al Ratoncito Pérez. ¿Estará buscando dientes?");
        } finally {
            setIsLoading(false);
        }
    };

    if (sessionId && messages.length === 0) {
        startConversation(sessionId);
    }
  }, [sessionId]); // Se ejecuta solo cuando sessionId está listo

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault(); 
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    
    const currentInput = input; 
    setInput(''); 
    setIsLoading(true);
    setError(null);

    try {
      // Usamos la nueva función del servicio, pasando el mensaje y el sessionId
      const response = await sendMessageToRatoncito(currentInput, sessionId);
      setMessages(prev => [...prev, { sender: 'ratoncito', text: response.response }]);
    } catch {
      setError("¡Uy! Mis antenas mágicas no funcionan bien. ¿Podemos intentarlo de nuevo?");
      // Devolvemos el input al usuario para que no lo pierda
      setInput(currentInput);
      setMessages(prev => prev.slice(0, -1)); // Eliminamos el mensaje que falló
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '80vh', p: 0, maxHeight: '700px' }}>
      <Paper 
        elevation={12} 
        sx={{ 
          height: '100%', 
          display: 'flex', 
          flexDirection: 'column',
          borderRadius: 4,
          backgroundColor: 'rgba(255, 255, 255, 0.85)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
        }}
      >
        <Box sx={{ p: 2, flexGrow: 1, overflowY: 'auto' }}>
          {messages.map((msg, index) => (
            <ChatMessage 
              key={index} 
              message={msg.text} 
              isUser={msg.sender === 'user'} 
            />
          ))}
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start', m: 2 }}>
              <CircularProgress size={24} color="secondary" />
            </Box>
          )}
          {error && <Typography color="error" sx={{p: 2}}>{error}</Typography>}
          <div ref={messagesEndRef} />
        </Box>
        
        <Box 
          component="form" 
          onSubmit={handleSendMessage}
          sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center' }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Escribe tu mensaje aquí..."
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            autoComplete="off"
            sx={{ mr: 1, '& .MuiOutlinedInput-root': { borderRadius: '20px' } }}
          />
          <Button 
            variant="contained" 
            color="primary" 
            type="submit"
            disabled={isLoading || !input.trim()}
            sx={{ borderRadius: '50%', width: '56px', height: '56px' }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat;
