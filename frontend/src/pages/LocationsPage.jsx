import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Skeleton
} from '@mui/material';
import MagicAnimation from '../components/UI/MagicAnimation';
import ErrorMessage from '../components/UI/ErrorMessage';

// Mock data - esto se reemplazaría con llamadas a la API
const locations = [
  {
    id: 'palacio-real',
    name: 'Palacio Real',
    description: 'Residencia oficial de la Familia Real Española',
    image: 'https://images.unsplash.com/photo-1574556462575-eb106a5865a0?auto=format&w=800'
  },
  {
    id: 'plaza-mayor',
    name: 'Plaza Mayor',
    description: 'Plaza porticada del siglo XVII en el centro de Madrid',
    image: 'https://images.unsplash.com/photo-1543783207-ec64e4d95325?auto=format&w=800'
  },
  {
    id: 'retiro',
    name: 'Parque del Retiro',
    description: 'Histórico parque y jardines con un lago para barcas',
    image: 'https://images.unsplash.com/photo-1551884831-bbf3cdc6469e?auto=format&w=800'
  },
  {
    id: 'puerta-del-sol',
    name: 'Puerta del Sol',
    description: 'Plaza emblemática en el corazón de Madrid',
    image: 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&w=800'
  },
  {
    id: 'gran-via',
    name: 'Gran Vía',
    description: 'La calle más famosa de Madrid, llena de tiendas y teatros',
    image: 'https://images.unsplash.com/photo-1578305698944-874fa44d04c9?auto=format&w=800'
  },
  {
    id: 'templo-debod',
    name: 'Templo de Debod',
    description: 'Antiguo templo egipcio reconstruido en Madrid',
    image: 'https://images.unsplash.com/photo-1590992236406-48c1e0583063?auto=format&w=800'
  }
];

const LocationsPage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [places, setPlaces] = useState([]);
  
  useEffect(() => {
    setIsLoading(true);
    
    // Aquí se llamaría a la api real, pero simplemente simulamos un retardo
    setTimeout(() => {
      setPlaces(locations);
      setIsLoading(false);
    }, 1000);
  }, []);
  
  return (
    <MagicAnimation>
      <Container>
        <Box sx={{ mb: 4 }}>
          <Typography 
            variant="h3" 
            className="magic-text"
            align="center"
            gutterBottom
          >
            Lugares Mágicos de Madrid
          </Typography>
          <Typography 
            variant="body1" 
            align="center" 
            sx={{ mb: 4 }}
          >
            Explora los lugares más emblemáticos y mágicos de Madrid con el Ratoncito Pérez
          </Typography>
        </Box>
        
        {error ? (
          <ErrorMessage error={error} />
        ) : (
          <Grid container spacing={4}>
            {isLoading ? (
              Array.from(new Array(6)).map((_, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card sx={{ height: '100%' }}>
                    <Skeleton variant="rectangular" height={140} />
                    <CardContent>
                      <Skeleton height={28} width="80%" />
                      <Skeleton height={20} width="100%" />
                      <Skeleton height={20} width="60%" />
                    </CardContent>
                  </Card>
                </Grid>
              ))
            ) : (
              places.map((location) => (
                <Grid 
                  item 
                  xs={12} 
                  sm={6} 
                  md={4} 
                  key={location.id}
                >
                  <Card className="magic-card" sx={{ height: '100%' }}>
                    <CardMedia
                      component="img"
                      height={200}
                      image={location.image}
                      alt={location.name}
                    />
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="h2">
                        {location.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {location.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))
            )}
          </Grid>
        )}
      </Container>
    </MagicAnimation>
  );
};

export default LocationsPage;