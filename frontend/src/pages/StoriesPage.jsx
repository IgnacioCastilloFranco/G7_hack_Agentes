import React, { useState, useEffect, useCallback } from 'react';
import { Container, Typography, Box, Paper, Divider } from '@mui/material';
import { useGeolocation } from '../hooks/useGeolocation';
import { getNearbyPlaces, searchPlacesByText, getPopularPlaces } from '../services/narrativeService';
import LocationComponent from '../components/Location/LocationComponent';
import SearchComponent from '../components/Location/SearchComponent';
import PlacesList from '../components/Stories/PlacesList';
import PlaceChat from '../components/Stories/PlaceChat';

const StoriesPage = () => {
  const [places, setPlaces] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [selectedPlace, setSelectedPlace] = useState(null);

  // Cargar lugares populares al inicio
  useEffect(() => {
    const loadPopularPlaces = async () => {
      if (!selectedPlace) {
        setIsLoading(true);
        try {
          const response = await getPopularPlaces();
          if (response.success) {
            setPlaces(response.sites);
          } else {
            setError("Error cargando lugares populares");
          }
        } catch (err) {
          console.error("Error:", err);
          setError("Error de conexión al servidor");
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadPopularPlaces();
  }, [selectedPlace]);

  // Manejar cambio de ubicación
  const handleLocationChange = useCallback(async (latitude, longitude) => {
    setCurrentLocation({ lat: latitude, lng: longitude });
    setIsLoading(true);
    try {
      const response = await getNearbyPlaces({
        latitude,
        longitude,
        radius: 5000
      });
      
      if (response.success) {
        setPlaces(response.sites);
      } else {
        setError("No se encontraron lugares cercanos");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Error de conexión");
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Manejar búsqueda
  const handleSearch = useCallback(async (query) => {
    setIsLoading(true);
    try {
      const response = await searchPlacesByText({
        query,
        latitude: currentLocation?.lat,
        longitude: currentLocation?.lng
      });
      
      if (response.success) {
        setPlaces(response.sites);
      } else {
        setError("No se encontraron resultados");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Error de búsqueda");
    } finally {
      setIsLoading(false);
    }
  }, [currentLocation]);

  // Seleccionar un lugar
  const handleSelectPlace = (place) => {
    setSelectedPlace(place);
  };
  
  // Cerrar chat de lugar
  const handleClosePlaceChat = () => {
    setSelectedPlace(null);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Historias Mágicas de Madrid
        </Typography>
        
        {!selectedPlace ? (
          <>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                <Box sx={{ flex: 1 }}>
                  <LocationComponent onLocationChange={handleLocationChange} />
                </Box>
                <Divider orientation="vertical" flexItem sx={{ display: { xs: 'none', md: 'block' } }} />
                <Divider sx={{ display: { xs: 'block', md: 'none' } }} />
                <Box sx={{ flex: 1 }}>
                  <SearchComponent onSearch={handleSearch} loading={isLoading} />
                </Box>
              </Box>
            </Paper>

            <PlacesList 
              places={places}
              isLoading={isLoading}
              error={error}
              onSelectPlace={handleSelectPlace}
            />
          </>
        ) : (
          <Box sx={{ height: '70vh' }}>
            <PlaceChat
              place={selectedPlace}
              onClose={handleClosePlaceChat}
            />
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default StoriesPage;