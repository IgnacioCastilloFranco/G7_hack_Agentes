import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ message = "¡Por mis bigotitos! Estoy pensando..." }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 3,
      }}
      component={motion.div}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <CircularProgress
        sx={{ 
          color: 'secondary.main',
          '& .MuiCircularProgress-circle': {
            strokeLinecap: 'round',
          }
        }}
      />
      <Typography
        variant="body1"
        sx={{ mt: 2, fontStyle: 'italic' }}
        className="magic-text"
      >
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingSpinner;