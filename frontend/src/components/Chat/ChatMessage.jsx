import React from 'react';
import { Box, Paper, Typography, Avatar } from '@mui/material';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import AudioButton from './AudioButton';

const messageVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const ChatMessage = ({ message, isUser }) => {
  return (
    <Box
      component={motion.div}
      variants={messageVariants}
      initial="hidden"
      animate="visible"
      transition={{ duration: 0.3 }}
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      {!isUser && (
        <Avatar
          src="/images/ratoncito.png"
          alt="Ratoncito Pérez"
          sx={{ 
            mr: 1, 
            bgcolor: 'primary.main',
            width: 40, 
            height: 40,
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}
        >
          🐭
        </Avatar>
      )}

      <Paper
        elevation={2}
        className={isUser ? '' : 'magic-card'}
        sx={{
          maxWidth: '70%',
          p: 2,
          borderRadius: '16px',
          bgcolor: isUser ? 'primary.light' : 'background.paper',
          color: isUser ? 'white' : 'text.primary',
          borderTopRightRadius: isUser ? 0 : '16px',
          borderTopLeftRadius: isUser ? '16px' : 0,
          position: 'relative',
          '&::after': isUser ? {} : {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '2px',
            background: 'linear-gradient(90deg, #3f51b5, #f50057)',
            borderTopLeftRadius: '16px',
            borderTopRightRadius: '16px',
          }
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
          <Box sx={{ flex: 1 }}>
            <ReactMarkdown>
              {message}
            </ReactMarkdown>
          </Box>
          {!isUser && (
            <AudioButton 
              text={message} 
              size="small" 
              color="primary"
              showProgress={true}
            />
          )}
        </Box>
      </Paper>

      {isUser && (
        <Avatar
          sx={{ 
            ml: 1, 
            bgcolor: 'secondary.main',
            width: 40, 
            height: 40
          }}
        >
          👤
        </Avatar>
      )}
    </Box>
  );
};

export default ChatMessage;