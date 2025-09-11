import React from 'react';
import { Alert, Box, Button, Typography } from '@mui/material';
import { motion } from 'framer-motion';

const ErrorMessage = ({ error, onRetry }) => {
  const errorMessage = error?.response?.data?.detail || error?.message || "¡Ups! Algo salió mal";
  
  return (
    <Box
      component={motion.div}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      sx={{ my: 2 }}
    >
      <Alert 
        severity="error" 
        sx={{ 
          borderRadius: 2,
          boxShadow: '0 2px 8px rgba(244, 67, 54, 0.2)'
        }}
      >
        <Typography variant="body1">
          ¡Por mis bigotitos! Ha ocurrido un problema mágico:
        </Typography>
        <Typography variant="body2" sx={{ fontStyle: 'italic', my: 1 }}>
          {errorMessage}
        </Typography>
        
        {onRetry && (
          <Button 
            variant="contained" 
            size="small" 
            onClick={onRetry}
            sx={{ mt: 1 }}
          >
            Intentar de nuevo
          </Button>
        )}
      </Alert>
    </Box>
  );
};

export default ErrorMessage;