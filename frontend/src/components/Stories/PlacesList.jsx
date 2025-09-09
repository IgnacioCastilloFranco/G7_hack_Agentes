import React from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  CardMedia, 
  Typography, 
  Chip, 
  Skeleton,
  Rating,
  CardActionArea
} from '@mui/material';
import { motion } from 'framer-motion';

const PlacesList = ({ places, isLoading, error, onSelectPlace }) => {
  
  const formatDistance = (distance) => {
    if (!distance) return '';
    if (distance < 1000) {
      return `${Math.round(distance)}m`;
    }
    return `${(distance / 1000).toFixed(1)}km`;
  };

  const getTypeIcon = (types) => {
    if (!types) return '🏛️';
    
    if (types.includes('museum')) return '🏛️';
    if (types.includes('church') || types.includes('place_of_worship')) return '⛪';
    if (types.includes('art_gallery')) return '🎨';
    if (types.includes('library')) return '📚';
    if (types.includes('university')) return '🎓';
    if (types.includes('tourist_attraction')) return '🏰';
    
    return '🏛️';
  };

  if (error) {
    return (
      <Box sx={{ textAlign: 'center', py: 4, color: 'error.main' }}>
        <Typography variant="h6">❌ {error}</Typography>
      </Box>
    );
  }

  if (isLoading) {
    return (
      <Box sx={{ py: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
          🔍 Buscando lugares mágicos...
        </Typography>
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, 1fr)',
            md: 'repeat(3, 1fr)'
          }, 
          gap: 3 
        }}>
          {Array.from(new Array(6)).map((_, index) => (
            <Card key={index}>
              <Skeleton variant="rectangular" height={140} />
              <CardContent>
                <Skeleton height={24} width="60%" />
                <Skeleton height={16} width="90%" />
                <Skeleton height={16} width="40%" />
              </CardContent>
            </Card>
          ))}
        </Box>
      </Box>
    );
  }

  if (!places || places.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="h6">
          No se encontraron lugares culturales e históricos. ¡Prueba con otra búsqueda!
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom className="magic-text">
        🏛️ Lugares para Historias Mágicas
      </Typography>
      <Typography variant="body2" paragraph>
        Selecciona un lugar para iniciar un chat con el Ratoncito Pérez sobre ese sitio
      </Typography>
      
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: {
          xs: '1fr',
          sm: 'repeat(2, 1fr)',
          md: 'repeat(3, 1fr)'
        }, 
        gap: 3 
      }}>
        {places.map((place, index) => (
          <Card 
            key={place.place_id || index}
            className="magic-card place-card-magic"
            component={motion.div}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            sx={{ 
              height: '100%', 
              display: 'flex', 
              flexDirection: 'column',
              position: 'relative',
              overflow: 'hidden',
              cursor: 'pointer',
              '&:hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
              }
            }}
            onClick={() => onSelectPlace(place)}
          >
            <CardActionArea sx={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
              {place.photo_url ? (
                <CardMedia
                  component="img"
                  height={160}
                  image={place.photo_url}
                  alt={place.name}
                  sx={{ objectFit: 'cover' }}
                />
              ) : (
                <Box 
                  sx={{ 
                    height: 160, 
                    bgcolor: 'primary.light', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    fontSize: '3rem'
                  }}
                >
                  {getTypeIcon(place.types)}
                </Box>
              )}
              
              <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                <Box sx={{ mb: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
                    {getTypeIcon(place.types)} {place.name}
                  </Typography>
                  {place.distance && (
                    <Chip 
                      label={formatDistance(place.distance)}
                      size="small"
                      color="primary"
                      sx={{ ml: 1 }}
                    />
                  )}
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  📍 {place.address}
                </Typography>
                
                {place.rating && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Rating
                      value={place.rating}
                      precision={0.5}
                      readOnly
                      size="small"
                    />
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      ({place.rating})
                    </Typography>
                  </Box>
                )}
                
                <Typography 
                  variant="body2" 
                  sx={{ 
                    mt: 'auto',
                    fontStyle: 'italic',
                    color: 'text.secondary'
                  }}
                >
                  Click para chatear con el Ratoncito sobre este lugar
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default PlacesList;