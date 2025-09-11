import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Skeleton,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import MyLocationIcon from '@mui/icons-material/MyLocation';
import { useGeolocation } from '../hooks/useGeolocation';
import { getNearbyPlaces } from '../services/narrativeService';

const LocationsPage = () => {
  const { latitude, longitude, error: geoError, getCurrentPosition } = useGeolocation();
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [places, setPlaces] = useState([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      if (latitude && longitude) {
        setIsLoading(true);
        setApiError(null);
        try {
          const data = await getNearbyPlaces({ latitude, longitude });
          setPlaces(data.sites || []);
        } catch (err) {
          setApiError('¡Oh, no! No pude encontrar lugares mágicos cerca. Mis bigotes deben estar cruzados.');
        } finally {
          setIsLoading(false);
        }
      }
    };
    fetchPlaces();
  }, [latitude, longitude]);

  const handleFindMeClick = () => {
    setPlaces([]); 
    getCurrentPosition();
  };

  return (
    <Container>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" className="magic-text" gutterBottom>
          Lugares Mágicos Cercanos
        </Typography>
        <Typography variant="h6" sx={{ color: 'text.secondary', mb: 2 }}>
          ¡Pulsa el botón para que pueda usar mi magia y encontrar los secretos que te rodean!
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleFindMeClick}
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <MyLocationIcon />}
        >
          {isLoading ? 'Buscando...' : 'Encuéntrame'}
        </Button>
      </Box>

      {geoError && <Alert severity="error" sx={{ mt: 2 }}>{geoError}</Alert>}
      {apiError && <Alert severity="error" sx={{ mt: 2 }}>{apiError}</Alert>}

      {!latitude && !isLoading && (
         <Box sx={{textAlign: 'center', mt: 4}}>
            <img src="/images/ratoncito_map.png" alt="Ratoncito con un mapa" style={{maxWidth: '250px', opacity: 0.7}}/>
            <Typography variant="h6" color="text.secondary">
                Estoy esperando tus coordenadas para empezar la búsqueda...
            </Typography>
         </Box>
      )}

      <Grid container spacing={4}>
        {isLoading && places.length === 0 ? (
          Array.from(new Array(6)).map((_, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card><Skeleton variant="rectangular" height={200} /><CardContent><Skeleton /><Skeleton width="60%" /></CardContent></Card>
            </Grid>
          ))
        ) : (
          places.map((place) => (
            <Grid item xs={12} sm={6} md={4} key={place.place_id}>
              <Card className="magic-card" sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={place.photo_url || `https://placehold.co/600x400/3f51b5/white?text=${place.name.charAt(0)}`}
                  alt={place.name}
                  onError={(e) => { e.target.onerror = null; e.target.src = `https://placehold.co/600x400/3f51b5/white?text=${place.name.charAt(0)}`; }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="h2" sx={{fontWeight: 'bold'}}>
                    {place.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {place.address}
                  </Typography>
                   <Box sx={{mt: 1}}>
                    <Typography variant="caption" color="secondary">
                        {Math.round(place.distance)} metros de distancia
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
};

export default LocationsPage;