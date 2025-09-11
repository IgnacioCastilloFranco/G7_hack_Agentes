import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Container,
  Avatar,
  IconButton,
  Tooltip
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { motion, AnimatePresence } from 'framer-motion';
import { sendMessageToRatoncito } from '../services/chatService';

const ChatMessage = ({ message, isUser }) => {
  const messageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <motion.div
      variants={messageVariants}
      initial="hidden"
      animate="visible"
      style={{
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        marginBottom: '16px',
        gap: '8px',
      }}
    >
      {!isUser && <Avatar src="/images/ratoncito.png" sx={{ width: 40, height: 40, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }} />}
      <Paper
        elevation={3}
        sx={{
          p: '10px 15px',
          borderRadius: isUser ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
          backgroundColor: isUser ? 'primary.main' : 'white',
          color: isUser ? 'white' : 'primary.dark',
          maxWidth: '80%',
          wordWrap: 'break-word',
        }}
      >
        <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{message}</Typography>
      </Paper>
    </motion.div>
  );
};

// Componente principal del Chat 
const AdventurePage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Generamos un id único.
    setSessionId(crypto.randomUUID());
    setMessages([
      { sender: 'ratoncito', text: '¡Hola, valiente aventurero! ✨ Soy el Ratoncito Pérez. Estoy listo para desvelar los secretos de Madrid contigo. ¿Cómo te llamas y cuántos años tienes?' }
    ]);
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100); 

    return () => clearTimeout(timer);
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !sessionId) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);

    const currentInput = input;
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessageToRatoncito(currentInput, sessionId);
      setMessages(prev => [...prev, { sender: 'ratoncito', text: response.response }]);
    } catch (err) {
      setError("¡Uy! Mis antenas mágicas no funcionan bien. ¿Podemos intentarlo de nuevo?");
      setInput(currentInput);
      setMessages(prev => prev.filter(m => m !== userMessage));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: { xs: 'calc(100vh - 112px)', md: 'calc(100vh - 128px)' }, p: 0 }}>
      <Paper
        elevation={12}
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          borderRadius: 4,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
        }}
      >
        <Box sx={{ p: { xs: 1, sm: 2 }, flexGrow: 1, overflowY: 'auto' }}>
          <AnimatePresence>
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg.text} isUser={msg.sender === 'user'} />
            ))}
          </AnimatePresence>
          {isLoading && <ChatMessage message="..." isUser={false} />}
          {error && <Typography color="error.main" sx={{ p: 2, textAlign: 'center' }}>{error}</Typography>}
          <div ref={messagesEndRef} />
        </Box>

        <Box component="form" onSubmit={handleSendMessage} sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Saluda al ratoncito..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            autoComplete="off"
            sx={{ mr: 1, '& .MuiOutlinedInput-root': { borderRadius: '20px', backgroundColor: 'white' } }}
          />
          <Tooltip title="Enviar Mensaje">
            <IconButton color="primary" type="submit" disabled={isLoading || !input.trim()} sx={{ backgroundColor: 'primary.main', color: 'white', '&:hover': { backgroundColor: 'primary.dark' } }}>
              <SendIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Paper>
    </Container>
  );
};

export default AdventurePage;
