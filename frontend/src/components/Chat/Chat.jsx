import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  Container,
  CircularProgress 
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ChatMessage from './ChatMessage';
import ErrorMessage from '../UI/ErrorMessage'; 

import { sendReactChatMessage } from '../../services/chatService';

const Chat = ({ initialContext }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(''); 
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (initialContext && initialContext.message && messages.length === 0) {
      setMessages([{ sender: 'ratoncito', text: initialContext.message }]);
    }
  }, [initialContext, messages.length]);

  const handleSendMessage = async (e) => {
    e.preventDefault(); 
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    const newMessages = [...messages, userMessage];
    
    setMessages(newMessages);
    const currentInput = input; 
    setInput(''); 
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendReactChatMessage(currentInput, newMessages);
      setMessages(prev => [...prev, { sender: 'ratoncito', text: response.response }]);
    } catch (err) {
      setError("¡Uy! Mis antenas mágicas no funcionan bien. ¿Podemos intentarlo de nuevo?");
      setInput(currentInput);
      setMessages(messages);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    const lastUserMessage = messages.filter(m => m.sender === 'user').pop();
    if (lastUserMessage) {
      setInput(lastUserMessage.text);
      setMessages(prev => prev.filter(m => m.sender === 'user'));
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '85vh', p: 0 }}>
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
        {/* Header del Chat */}
        <Box sx={{ p: 2, borderBottom: '1px solid rgba(0,0,0,0.1)', textAlign: 'center' }}>
          <Typography variant="h6" fontWeight="bold" className="magic-text">
            Aventura con el Ratoncito Pérez
          </Typography>
        </Box>
        
        {/* Área de Mensajes */}
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
              <CircularProgress size={24} />
            </Box>
          )}
          
          {error && <ErrorMessage message={error} onRetry={handleRetry} />}
          
          <div ref={messagesEndRef} />
        </Box>
        
        {/* Área de Input */}
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
            sx={{ mr: 1 }}
            size="small"
            autoComplete="off"
          />
          <Button 
            variant="contained" 
            color="primary" 
            type="submit"
            disabled={isLoading || !input.trim()}
            sx={{ borderRadius: '50%', minWidth: '50px', height: '50px' }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat;