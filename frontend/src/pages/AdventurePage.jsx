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
import { sendMessageToRatoncito } from '../services/chatService';

const ChatMessage = ({ message, isUser }) => (
    <Box sx={{ display: 'flex', alignItems: 'flex-end', justifyContent: isUser ? 'flex-end' : 'flex-start', mb: 2, gap: 1 }}>
        {!isUser && <Avatar src="/images/ratoncito.png" sx={{ width: 40, height: 40 }} />}
        <Paper
            elevation={3}
            sx={{
                p: '10px 15px',
                borderRadius: isUser ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
                backgroundColor: isUser ? 'primary.main' : 'secondary.light',
                color: 'white',
                maxWidth: '80%',
            }}
        >
            <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>{message}</Typography>
        </Paper>
    </Box>
);

const AdventurePage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(''); 
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setSessionId(crypto.randomUUID());

    setMessages([
      { sender: 'ratoncito', text: '¡Hola, valiente aventurero! ✨ Soy el Ratoncito Pérez. Estoy listo para desvelar los secretos de Madrid contigo.' }
    ]);
    
  }, []); 

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
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
    <Container maxWidth="md" sx={{ height: 'calc(100vh - 120px)', p: 0 }}>
      <Paper 
        elevation={12} 
        sx={{ 
          height: '100%', 
          display: 'flex', 
          flexDirection: 'column',
          borderRadius: 4,
          backgroundColor: 'rgba(255, 255, 255, 0.7)',
          backdropFilter: 'blur(5px)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
        }}
      >
        <Box sx={{ p: 2, flexGrow: 1, overflowY: 'auto' }}>
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg.text} isUser={msg.sender === 'user'} />
          ))}
          {isLoading && <ChatMessage message="..." isUser={false} />}
          {error && <Typography color="error" sx={{p: 2, textAlign: 'center'}}>{error}</Typography>}
          <div ref={messagesEndRef} />
        </Box>
        
        <Box component="form" onSubmit={handleSendMessage} sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Escribe tu nombre y edad..."
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            autoComplete="off"
            sx={{ mr: 1, '& .MuiOutlinedInput-root': { borderRadius: '20px', backgroundColor: 'white' } }}
          />
          <Button variant="contained" color="primary" type="submit" disabled={isLoading || !input.trim()} sx={{ borderRadius: '50%', width: '56px', height: '56px', minWidth: '56px' }}>
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default AdventurePage;