import React, { useState, useCallback } from 'react';
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
  Alert,
  TextField,
  Paper,
  Divider
} from '@mui/material';
import MyLocationIcon from '@mui/icons-material/MyLocation';
import SearchIcon from '@mui/icons-material/Search';
import { useGeolocation } from '../hooks/useGeolocation';
import { getNearbyPlaces, searchPlacesByText } from '../services/narrativeService';

const LocationsPage = () => {
  const { latitude, longitude, error: geoError, getCurrentPosition } = useGeolocation();
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [places, setPlaces] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchPlaces = useCallback(async (type, params) => {
    setIsLoading(true);
    setApiError(null);
    setPlaces([]);
    try {
      const data = type === 'nearby'
        ? await getNearbyPlaces(params)
        : await searchPlacesByText(params);
        
      setPlaces(data.sites || []);
      if (!data.sites || data.sites.length === 0) {
        setApiError('No he encontrado lugares mágicos con esa búsqueda. ¿Probamos otra?');
      }
    } catch (err) {
      setApiError('¡Oh, no! Mis bigotes se han cruzado y no pude buscar lugares.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleFindMeClick = () => {
    getCurrentPosition();
  };
  
  React.useEffect(() => {
    if (latitude && longitude) {
      fetchPlaces('nearby', { latitude, longitude });
    }
  }, [latitude, longitude, fetchPlaces]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      fetchPlaces('search', { query: searchQuery });
    }
  };

  return (
    <Container maxWidth="lg">
      <Paper sx={{ p: {xs: 2, md: 4}, mb: 4, backgroundColor: 'rgba(255,255,255,0.8)', backdropFilter: 'blur(10px)', borderRadius: 4 }}>
        {/* <-- CAMBIO CLAVE 1: Título centrado y con mejor contraste --> */}
        <Typography 
          variant="h3" 
          gutterBottom 
          textAlign="center"
          sx={{ 
            color: 'primary.dark', 
            textShadow: '1px 1px 3px rgba(0,0,0,0.1)',
            fontWeight: 900
          }}
        >
          Explorador de Lugares Mágicos
        </Typography>
        {/* <-- CAMBIO CLAVE 2: Eliminamos la prop 'item' de todos los Grid hijos --> */}
        <Grid container spacing={2} alignItems="center" justifyContent="center">
          <Grid xs={12} md={5}>
            <Typography variant="h6" textAlign="center" gutterBottom sx={{color: 'primary.dark'}}>Encuentra secretos cerca de ti</Typography>
            <Button
              fullWidth
              variant="contained"
              color="secondary"
              onClick={handleFindMeClick}
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <MyLocationIcon />}
              sx={{ py: 1.5 }}
            >
              Usar mi ubicación
            </Button>
          </Grid>
          <Grid xs={12} md={2} textAlign="center">
            <Divider orientation="vertical" sx={{ display: { xs: 'none', md: 'block' }, height: '100%', borderColor: 'primary.dark' }}>O</Divider>
            <Divider sx={{ display: { xs: 'block', md: 'none' }, my: 2, color: 'primary.dark' }}>O</Divider>
          </Grid>
          <Grid xs={12} md={5}>
            <Typography variant="h6" textAlign="center" gutterBottom sx={{color: 'primary.dark'}}>O busca un lugar específico</Typography>
            <Box component="form" onSubmit={handleSearchSubmit} sx={{ display: 'flex' }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Ej: Palacio de Cristal, Templo de Debod..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: '20px 0 0 20px', backgroundColor: 'white' } }}
              />
              <Button type="submit" variant="contained" sx={{ borderRadius: '0 20px 20px 0', px: 3 }} disabled={isLoading}>
                <SearchIcon />
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {geoError && <Alert severity="warning" sx={{ mt: 2, backgroundColor: 'rgba(255,255,255,0.8)' }}>{geoError}. Puedes buscar por texto.</Alert>}
      {apiError && <Alert severity="info" sx={{ mt: 2, backgroundColor: 'rgba(255,255,255,0.8)' }}>{apiError}</Alert>}
      
      <Grid container spacing={4} justifyContent="center">
        {isLoading ? (
          Array.from(new Array(6)).map((_, index) => (
            <Grid xs={12} sm={6} md={4} key={index}>
              <Card sx={{ height: '100%' }}><Skeleton variant="rectangular" height={200} /><CardContent><Skeleton /><Skeleton width="60%" /></CardContent></Card>
            </Grid>
          ))
        ) : (
          places.map((place) => (
            <Grid xs={12} sm={6} md={4} key={place.place_id}>
              <Card className="magic-card" sx={{ height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'rgba(255,255,255,0.9)' }}>
                {place.photo_url ? (
                  <CardMedia
                    component="img"
                    height="200"
                    image={place.photo_url}
                    alt={place.name}
                    onError={(e) => { e.target.onerror = null; e.target.src = `/images/ratoncito.jpg`; }}
                    sx={{ objectFit: 'cover' }}
                  />
                ) : (
                  // <-- CAMBIO CLAVE 3: Un 'placeholder' cuando no hay foto -->
                  <Box sx={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'primary.light' }}>
                    <img src="/images/ratoncito.png" alt="Ratoncito Pérez" style={{ height: '60%', opacity: 0.5 }} />
                  </Box>
                )}
                <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                  <Typography gutterBottom variant="h5" component="h2" sx={{fontWeight: 'bold', color: 'primary.dark'}}>
                    {place.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ flexGrow: 1 }}>
                    {place.address}
                  </Typography>
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
