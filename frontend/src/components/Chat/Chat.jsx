import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  Container,
  IconButton
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ChatMessage from './ChatMessage';
import LoadingSpinner from '../UI/LoadingSpinner';
import ErrorMessage from '../UI/ErrorMessage';
import { sendChatMessage } from '../../services/chatService';

const Chat = () => {
  const [messages, setMessages] = useState([
    { 
      text: "¡Por mis bigotitos! ¡Hola pequeños aventureros! Soy el Ratoncito Pérez, guardián mágico de Madrid. ¿Estáis listos para una aventura?", 
      isUser: false 
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto scroll al último mensaje
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Añadir mensaje del usuario
    const userMessage = { text: inputValue, isUser: true };
    setMessages([...messages, userMessage]);
    setInputValue('');
    setError(null);
    setIsLoading(true);

    try {
      // Llamar al API
      const response = await sendChatMessage(inputValue);
      
      // Añadir respuesta del Ratoncito
      setMessages(prev => [...prev, { 
        text: response.response, 
        isUser: false 
      }]);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    // Recuperar el último mensaje del usuario
    const lastUserMessage = [...messages].reverse()
      .find(message => message.isUser)?.text;
      
    if (lastUserMessage) {
      setInputValue(lastUserMessage);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper 
        elevation={3} 
        sx={{ 
          height: '70vh', 
          display: 'flex', 
          flexDirection: 'column',
          overflow: 'hidden',
          borderRadius: 3,
          border: '1px solid rgba(63, 81, 181, 0.2)',
          boxShadow: '0 8px 20px rgba(0, 0, 0, 0.1)'
        }}
        className="magic-card"
      >
        {/* Header */}
        <Box 
          sx={{ 
            p: 2, 
            borderBottom: '1px solid rgba(0, 0, 0, 0.1)',
            background: 'linear-gradient(90deg, #3f51b5, #7986cb)',
            color: 'white'
          }}
        >
          <Typography variant="h6" fontWeight="bold">
            Charla con el Ratoncito Pérez
          </Typography>
          <Typography variant="body2">
            ¡Pregúntame lo que quieras sobre Madrid!
          </Typography>
        </Box>
        
        {/* Messages container */}
        <Box 
          sx={{ 
            p: 2, 
            flexGrow: 1, 
            overflowY: 'auto',
            bgcolor: 'background.default'
          }}
        >
          {messages.map((message, index) => (
            <ChatMessage 
              key={index} 
              message={message.text} 
              isUser={message.isUser} 
            />
          ))}
          
          {isLoading && <LoadingSpinner />}
          {error && <ErrorMessage error={error} onRetry={handleRetry} />}
          
          <div ref={messagesEndRef} />
        </Box>
        
        {/* Input area */}
        <Box 
          component="form" 
          onSubmit={handleSendMessage}
          sx={{ 
            p: 2, 
            borderTop: '1px solid rgba(0, 0, 0, 0.1)',
            bgcolor: 'background.paper',
            display: 'flex'
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Escribe tu mensaje aquí..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            sx={{ mr: 1 }}
            size="small"
          />
          <Button 
            variant="contained" 
            color="primary" 
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            endIcon={<SendIcon />}
          >
            Enviar
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat;