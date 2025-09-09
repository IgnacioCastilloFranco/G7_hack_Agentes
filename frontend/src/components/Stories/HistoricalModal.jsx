import React, { useState } from 'react';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  Typography, 
  Box, 
  CircularProgress,
  Rating,
  Alert,
  IconButton,
  TextField,
  Tabs,
  Tab
} from '@mui/material';
import { motion } from 'framer-motion';
import CloseIcon from '@mui/icons-material/Close';
import ChatIcon from '@mui/icons-material/Chat';
import HistoryIcon from '@mui/icons-material/History';
import ReactMarkdown from 'react-markdown';

const HistoricalModal = ({ site, historicalContext, isLoading, onClose }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);

  if (!site) return null;

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSendMessage = async () => {
    if (!userMessage.trim()) return;

    const newMessage = { role: 'user', content: userMessage };
    setChatMessages(prev => [...prev, newMessage]);
    setUserMessage('');
    setIsChatLoading(true);

    try {
      // Por ahora, tenemos respuesta simulada pero aquí es donde llamaríamos a la api de chat
      setTimeout(() => {
        const ratresponse = {
          role: 'ratoncito',
          content: `¡Por mis bigotitos! Me encanta hablar sobre ${site.name}. ${userMessage.includes('historia') ? 'Su historia es fascinante...' : '¿Sabías que este lugar tiene secretos mágicos?'} ¿Qué más te gustaría saber?`
        };
        setChatMessages(prev => [...prev, ratresponse]);
        setIsChatLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error en chat:', error);
      setIsChatLoading(false);
    }
  };

  return (
    <Dialog 
      open={!!site} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      maxHeight="90vh"
      PaperProps={{
        component: motion.div,
        initial: { opacity: 0, y: 50 },
        animate: { opacity: 1, y: 0 },
        transition: { duration: 0.3 },
        sx: { height: '80vh' }
      }}
    >
      <DialogTitle 
        sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          pb: 0
        }}
      >
        <Box>
          <Typography variant="h6">
            🏛️ {site.name}
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.8 }}>
            📍 {site.address}
          </Typography>
        </Box>
        <IconButton 
          onClick={onClose}
          sx={{ color: 'white' }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: '#667eea' }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          sx={{ 
            '& .MuiTab-root': { color: 'white' },
            '& .Mui-selected': { color: 'white !important' },
            '& .MuiTabs-indicator': { backgroundColor: 'white' }
          }}
        >
          <Tab icon={<HistoryIcon />} label="Historia" />
          <Tab icon={<ChatIcon />} label="Chat con Ratoncito" />
        </Tabs>
      </Box>
      
      <DialogContent sx={{ p: 0, flex: 1, overflow: 'hidden' }}>
        {activeTab === 0 && (
          <Box sx={{ p: 3, height: '100%', overflow: 'auto' }}>
            {site.rating && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Rating value={site.rating} precision={0.5} readOnly size="small" />
                <Typography variant="body2">({site.rating})</Typography>
              </Box>
            )}
            
            <Typography variant="h6" gutterBottom sx={{ color: '#374151' }}>
              📚 Información Histórica y Cultural
            </Typography>
            
            {isLoading ? (
              <Box sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                py: 4 
              }}>
                <CircularProgress sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary">
                  🔍 El Ratoncito Pérez está buscando información mágica...
                </Typography>
              </Box>
            ) : historicalContext ? (
              <Box sx={{ 
                bgcolor: '#f9fafb', 
                borderRadius: 2, 
                p: 2,
                borderLeft: '4px solid #667eea'
              }}>
                {historicalContext.success ? (
                  <ReactMarkdown>{historicalContext.context}</ReactMarkdown>
                ) : (
                  <Alert severity="error">
                    {historicalContext.message || 'No se pudo obtener información histórica'}
                  </Alert>
                )}
              </Box>
            ) : (
              <Box sx={{ 
                bgcolor: '#f3f4f6', 
                borderRadius: 2, 
                p: 2, 
                textAlign: 'center' 
              }}>
                <Typography color="text.secondary">
                  La información histórica se cargará automáticamente...
                </Typography>
              </Box>
            )}
          </Box>
        )}

        {activeTab === 1 && (
          <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
              {chatMessages.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body2" color="text.secondary">
                    🐭 ¡Hola! Soy el Ratoncito Pérez. ¿Qué te gustaría saber sobre {site.name}?
                  </Typography>
                </Box>
              ) : (
                chatMessages.map((message, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                      mb: 1
                    }}
                  >
                    <Box
                      sx={{
                        maxWidth: '80%',
                        p: 2,
                        borderRadius: 2,
                        bgcolor: message.role === 'user' ? 'primary.main' : 'grey.100',
                        color: message.role === 'user' ? 'white' : 'text.primary'
                      }}
                    >
                      <Typography variant="body2">{message.content}</Typography>
                    </Box>
                  </Box>
                ))
              )}
              {isChatLoading && (
                <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1 }}>
                  <Box sx={{ maxWidth: '80%', p: 2, borderRadius: 2, bgcolor: 'grey.100' }}>
                    <CircularProgress size={16} />
                  </Box>
                </Box>
              )}
            </Box>
            
            <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  size="small"
                  placeholder="Pregunta algo sobre este lugar..."
                  value={userMessage}
                  onChange={(e) => setUserMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  disabled={isChatLoading}
                />
                <Button 
                  variant="contained" 
                  onClick={handleSendMessage}
                  disabled={!userMessage.trim() || isChatLoading}
                >
                  Enviar
                </Button>
              </Box>
            </Box>
          </Box>
        )}
      </DialogContent>
      
      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onClose} variant="outlined" color="inherit">
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default HistoricalModal;