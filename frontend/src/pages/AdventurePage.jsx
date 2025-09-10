import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, Grow, Container, Paper, Divider } from '@mui/material';
import { motion } from 'framer-motion';

import LocationComponent from '../components/Location/LocationComponent';
import SearchComponent from '../components/Location/SearchComponent';
import PlacesList from '../components/Stories/PlacesList'; 
import Chat from '../components/Chat/Chat'; 

import { getNearbyPlaces, searchPlacesByText } from '../services/narrativeService';

const AdventurePage = () => {
  const [stage, setStage] = useState('welcome'); 
  
  const [places, setPlaces] = useState([]);
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(false);
  const [placesError, setPlacesError] = useState(null);

  const [chatContext, setChatContext] = useState(null); 

  const handleStartAdventure = () => {
    setStage('location_selection');
  };

  const handleLocationDetected = async (lat, lng) => {
    console.log('🎯 AdventurePage: Ubicación detectada', lat, lng);
  setStage('places_display'); 
  setIsLoadingPlaces(true);
  setPlacesError(null);
  try {
    console.log('🔍 Llamando a getNearbyPlaces con:', { latitude: lat, longitude: lng });
    const result = await getNearbyPlaces({ latitude: lat, longitude: lng });
    console.log('✅ Resultado de getNearbyPlaces:', result);
    setPlaces(result.sites || []);
    if (!result.sites || result.sites.length === 0) {
      console.warn('⚠️ No se encontraron sites en el resultado');
    }
  } catch (error) {
    console.error('❌ Error en handleLocationDetected:', error);
    setPlacesError('No pude encontrar lugares mágicos cerca de ti. ¡Inténtalo de nuevo!');
  } finally {
    setIsLoadingPlaces(false);
  }
};

  const handleSearch = async (query) => {
  console.log('🎯 AdventurePage: Búsqueda iniciada con query:', query);
  setStage('places_display'); 
  setIsLoadingPlaces(true);
  setPlacesError(null);
  try {
    console.log('🔍 Llamando a searchPlacesByText con:', { query });
    const result = await searchPlacesByText({ query });
    console.log('✅ Resultado de searchPlacesByText:', result);
    setPlaces(result.sites || []);
    if (!result.sites || result.sites.length === 0) {
      console.warn('⚠️ No se encontraron sites en la búsqueda');
    }
  } catch (error) {
    console.error('❌ Error en handleSearch:', error);
    setPlacesError(`No encontré nada para "${query}". ¿Probamos con otro nombre?`);
  } finally {
    setIsLoadingPlaces(false);
  }
};

  const handlePlaceSelected = (place) => {
    setChatContext({
      type: 'place_chat_start',
      data: place,
      message: `¡Por mis bigotitos! Has elegido ${place.name}. Es un lugar fascinante. ¿Qué te gustaría saber sobre él?`
    });
    setStage('chatting'); 
  };

  const renderStage = () => {
    switch (stage) {
      case 'welcome':
        return (
          <Grow in={true}>
            <Box textAlign="center" color="white">
              <motion.div initial={{ scale: 0.5, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.7 }}>
                <Typography variant="h2" component="h1" gutterBottom className="magic-text">
                  La Aventura del Ratoncito Pérez
                </Typography>
                <Typography variant="h5" sx={{ mb: 4 }}>
                  🐭✨ ¡Descubre los secretos mágicos de Madrid conmigo!
                </Typography>
                <Button variant="contained" color="secondary" size="large" onClick={handleStartAdventure}>
                  Comenzar la Aventura
                </Button>
              </motion.div>
            </Box>
          </Grow>
        );
      
      case 'location_selection':
        return (
          <Grow in={true}>
            <Container maxWidth="md">
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4, textAlign: 'center', backgroundColor: 'rgba(255, 255, 255, 0.9)', backdropFilter: 'blur(5px)' }}>
                <Typography variant="h4" gutterBottom className="magic-text">¿Dónde empezamos?</Typography>
                <Box sx={{ my: 3 }}>
                  <LocationComponent onLocationChange={handleLocationDetected} />
                </Box>
                <Divider>O</Divider>
                <Box sx={{ mt: 3 }}>
                  <SearchComponent onSearch={handleSearch} />
                </Box>
              </Paper>
            </Container>
          </Grow>
        );

      case 'places_display':
        return (
          <Container maxWidth="lg">
            <PlacesList 
              places={places}
              isLoading={isLoadingPlaces}
              error={placesError}
              onSelectPlace={handlePlaceSelected} 
            />
          </Container>
        );

      case 'chatting':
        return (
            <Chat initialContext={chatContext} />
        );

      default:
        return null;
    }
  };

  return (
    <Box
      sx={{
        flexGrow: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 3,
        minHeight: '100vh'
      }}
    >
      {renderStage()}
    </Box>
  );
};

export default AdventurePage;