// import React, { useState, useEffect, useRef } from 'react';
// import { 
//   Box, 
//   Paper, 
//   TextField, 
//   Button, 
//   Typography, 
//   Avatar,
//   CircularProgress,
//   Divider
// } from '@mui/material';
// import { motion } from 'framer-motion';
// import SendIcon from '@mui/icons-material/Send';
// import { getPlaceChatResponse } from '../../services/narrativeService';
// import ReactMarkdown from 'react-markdown';

// const PlaceChat = ({ place, onClose }) => {
//   const [message, setMessage] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const chatContainerRef = useRef(null);
  
//   // Iniciamos chat automáticamente cuando se abre, pero no me convence
//   useEffect(() => {
//     if (place && chatHistory.length === 0) {
//       handleInitialMessage();
//     }
//   }, [place]);
  
//   // Auto-scroll al mensaje más reciente, hay que mejorarlo
//   useEffect(() => {
//     if (chatContainerRef.current) {
//       chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
//     }
//   }, [chatHistory]);
  
//   const handleInitialMessage = async () => {
//     setIsLoading(true);
//     try {
//       const response = await getPlaceChatResponse({
//         place_id: place.place_id,
//         place_name: place.name,
//         user_message: `¡Hola Ratoncito! Cuéntame sobre ${place.name}`,
//         chat_history: []
//       });
      
//       setChatHistory([
//         {
//           role: 'user',
//           content: `¡Hola Ratoncito! Cuéntame sobre ${place.name}`
//         },
//         {
//           role: 'assistant',
//           content: response.response
//         }
//       ]);
//     } catch (err) {
//       setError('No he podido obtener información sobre este lugar');
//     } finally {
//       setIsLoading(false);
//     }
//   };
  
//   const handleSendMessage = async () => {
//     if (!message.trim()) return;
    
//     // Añadir mensaje del usuario
//     const updatedHistory = [
//       ...chatHistory,
//       { role: 'user', content: message }
//     ];
    
//     setChatHistory(updatedHistory);
//     setMessage('');
//     setIsLoading(true);
    
//     try {
//       const response = await getPlaceChatResponse({
//         place_id: place.place_id,
//         place_name: place.name,
//         user_message: message,
//         chat_history: updatedHistory
//       });
      
//       setChatHistory([
//         ...updatedHistory,
//         { role: 'assistant', content: response.response }
//       ]);
//     } catch (err) {
//       setError('Error al comunicarse con el Ratoncito');
//       setChatHistory([
//         ...updatedHistory,
//         { 
//           role: 'assistant', 
//           content: "¡Por mis bigotitos! Parece que me he quedado sin palabras. ¿Puedes intentarlo de nuevo?" 
//         }
//       ]);
//     } finally {
//       setIsLoading(false);
//     }
//   };
  
//   return (
//     <Paper 
//       elevation={3} 
//       component={motion.div}
//       initial={{ opacity: 0, y: 20 }}
//       animate={{ opacity: 1, y: 0 }}
//       sx={{ 
//         p: 2, 
//         height: '100%', 
//         display: 'flex', 
//         flexDirection: 'column',
//         bgcolor: 'background.default'
//       }}
//     >
//       <Box sx={{ 
//         display: 'flex', 
//         alignItems: 'center', 
//         pb: 1, 
//         borderBottom: '1px solid', 
//         borderColor: 'divider',
//         mb: 2
//       }}>
//         <Avatar 
//           src="/images/ratoncito.png" 
//           alt="Ratoncito Pérez"
//           sx={{ mr: 2 }}
//         />
//         <Box>
//           <Typography variant="h6">
//             Chat Mágico: {place.name}
//           </Typography>
//           <Typography variant="caption" color="text.secondary">
//             Pregunta al Ratoncito sobre este lugar mágico
//           </Typography>
//         </Box>
//       </Box>
      
//       {/* Contenedor de mensajes */}
//       <Box 
//         ref={chatContainerRef}
//         sx={{ 
//           flexGrow: 1, 
//           overflow: 'auto',
//           display: 'flex',
//           flexDirection: 'column',
//           gap: 2,
//           mb: 2,
//           p: 1
//         }}
//       >
//         {chatHistory.map((msg, index) => (
//           <Box 
//             key={index} 
//             sx={{ 
//               alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
//               maxWidth: '80%'
//             }}
//             component={motion.div}
//             initial={{ opacity: 0, y: 10 }}
//             animate={{ opacity: 1, y: 0 }}
//           >
//             <Paper
//               elevation={1}
//               sx={{
//                 p: 2,
//                 bgcolor: msg.role === 'user' ? 'primary.light' : 'magic.light',
//                 color: msg.role === 'user' ? 'white' : 'text.primary',
//                 borderRadius: 2
//               }}
//             >
//               {msg.role === 'assistant' ? (
//                 <ReactMarkdown>{msg.content}</ReactMarkdown>
//               ) : (
//                 <Typography>{msg.content}</Typography>
//               )}
//             </Paper>
//           </Box>
//         ))}
        
//         {isLoading && (
//           <Box 
//             sx={{ 
//               display: 'flex', 
//               alignItems: 'center', 
//               alignSelf: 'flex-start',
//               p: 2
//             }}
//           >
//             <CircularProgress size={20} sx={{ mr: 2 }} />
//             <Typography variant="body2">El Ratoncito está escribiendo...</Typography>
//           </Box>
//         )}
//       </Box>
      
//       {error && (
//         <Box sx={{ mb: 2 }}>
//           <Typography color="error" variant="body2">
//             {error}
//           </Typography>
//         </Box>
//       )}
      
//       {/* Entrada de mensaje */}
//       <Box sx={{ display: 'flex', gap: 1 }}>
//         <TextField
//           fullWidth
//           placeholder="Pregunta algo al Ratoncito Pérez..."
//           value={message}
//           onChange={(e) => setMessage(e.target.value)}
//           onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
//           disabled={isLoading}
//         />
//         <Button
//           variant="contained"
//           color="primary"
//           onClick={handleSendMessage}
//           disabled={!message.trim() || isLoading}
//           endIcon={<SendIcon />}
//         >
//           Enviar
//         </Button>
//       </Box>
      
//       <Box sx={{ mt: 2, textAlign: 'center' }}>
//         <Button 
//           variant="text" 
//           color="inherit" 
//           size="small" 
//           onClick={onClose}
//         >
//           Volver a los lugares
//         </Button>
//       </Box>
//     </Paper>
//   );
// };

// export default PlaceChat;