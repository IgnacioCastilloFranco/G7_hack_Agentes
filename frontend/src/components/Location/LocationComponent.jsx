import React, { useEffect } from 'react';
import { Box, Button, Typography, Alert, CircularProgress } from '@mui/material';
import { useGeolocation } from '../../hooks/useGeolocation';
import { motion } from 'framer-motion';
import MyLocationIcon from '@mui/icons-material/MyLocation';

const LocationComponent = ({ onLocationChange }) => {
  const { latitude, longitude, error, loading, getCurrentPosition } = useGeolocation({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 300000, // 5 minutos
  });

  const handleGetLocation = () => {
    getCurrentPosition();
  };

  useEffect(() => {
    if (latitude !== null && longitude !== null && onLocationChange) {
      onLocationChange(latitude, longitude);
    }
  }, [latitude, longitude, onLocationChange]);

  return (
    <Box 
      component={motion.div}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <Typography variant="h6" gutterBottom>
        📍 Tu Ubicación Mágica
      </Typography>
      
      <Button 
        variant="contained"
        color="primary"
        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <MyLocationIcon />}
        onClick={handleGetLocation}
        disabled={loading}
        fullWidth
        sx={{ mb: 2 }}
      >
        {loading ? 'Buscando tu ubicación...' : '📍 Detectar mi ubicación'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {latitude !== null && longitude !== null && (
        <Box 
          sx={{ 
            p: 2, 
            border: '1px solid', 
            borderColor: 'primary.light',
            borderRadius: 2,
            bgcolor: 'background.paper'
          }}
        >
          <Typography variant="subtitle2" gutterBottom>
            <strong>📍 ¡Ubicación encontrada!</strong>
          </Typography>
          <Typography variant="body2">
            Latitud: {latitude.toFixed(6)}
          </Typography>
          <Typography variant="body2">
            Longitud: {longitude.toFixed(6)}
          </Typography>
          <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
            ✨ El Ratoncito Pérez está buscando lugares mágicos cerca de ti...
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default LocationComponent;