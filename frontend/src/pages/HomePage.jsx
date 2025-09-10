import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia,
  CardActionArea,
  Avatar
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import ChatIcon from '@mui/icons-material/Chat';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import PlaceIcon from '@mui/icons-material/Place';
import MagicAnimation from '../components/UI/MagicAnimation';

const features = [
  {
    title: 'Charla con el Ratoncito',
    description: '¡Habla directamente con el Ratoncito Pérez y resuelve tus dudas sobre Madrid!',
    icon: <ChatIcon fontSize="large" />,
    color: '#3f51b5',
    link: '/chat'
  },
  {
    title: 'Historias Mágicas',
    description: 'Descubre fascinantes historias sobre los lugares más emblemáticos de Madrid.',
    icon: <AutoStoriesIcon fontSize="large" />,
    color: '#f50057',
    link: '/stories'
  },
  {
    title: 'Juegos y Acertijos',
    description: 'Pon a prueba tus conocimientos con divertidos juegos sobre la ciudad.',
    icon: <SportsEsportsIcon fontSize="large" />,
    color: '#ff9100',
    link: '/games'
  },
  {
    title: 'Lugares Mágicos',
    description: 'Explora los rincones más mágicos y sorprendentes de Madrid con tu familia.',
    icon: <PlaceIcon fontSize="large" />,
    color: '#4caf50',
    link: '/locations'
  }
];

const HomePage = () => {
  return (
    <MagicAnimation>
      <Box
        sx={{
          bgcolor: 'background.paper',
          pt: 8,
          pb: 6,
          position: 'relative',
          overflow: 'hidden',
          backgroundImage: 'url(/images/madrid-skyline.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          color: 'white',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.6)',
          }
        }}
      >
        <Container maxWidth="md" sx={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
                <motion.div
                initial={{ scale: 0, rotate: -10 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ 
                    type: "spring",
                    stiffness: 260,
                    damping: 20,
                    duration: 0.8 
                }}
                >
                <Avatar
                    src="/images/ratoncito.png"
                    alt="Ratoncito Pérez"
                    sx={{ 
                    width: 180, 
                    height: 180, 
                    border: '5px solid white',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
                    bgcolor: 'primary.main'
                    }}
                />
                </motion.div>
            </Box>

            <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Typography
                variant="h2"
                align="center"
                gutterBottom
                className="magic-text"
                sx={{ 
                    fontWeight: 'bold',
                    textAlign: 'center',
                    maxWidth: '90%'
                }}
                >
                Madrid Mágico con el Ratoncito Pérez
                </Typography>
                
                <Typography 
                variant="h5" 
                align="center" 
                color="inherit" 
                paragraph
                sx={{
                    textAlign: 'center',
                    maxWidth: '80%',
                    mx: 'auto'
                }}
                >
                Descubre Madrid de una forma mágica y divertida con tu guía especial,
                el Ratoncito Pérez. ¡Historias, juegos y aventuras para toda la familia!
                </Typography>
            </Box>

            <Box
                sx={{
                mt: 4,
                display: 'flex',
                justifyContent: 'center',
                }}
            >
                <Button 
                variant="contained" 
                color="secondary" 
                size="large"
                component={RouterLink}
                to="/chat"
                sx={{ 
                    px: 4,
                    py: 1.5,
                }}
                >
                ¡Comenzar Aventura!
                </Button>
            </Box>
            </Container>
      </Box>

      <Container sx={{ py: 8 }}>
        <Typography 
          variant="h3" 
          component="h2" 
          align="center"
          className="magic-text"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Descubre la Magia
        </Typography>

        {/* Contenedor centrado para las tarjetas */}
        <Box sx={{ display: 'flex', justifyContent: 'center' }}>
          <Grid container spacing={4} sx={{ maxWidth: '1100px' }} justifyContent="center">
            {features.map((feature, index) => (
              <Grid 
                item 
                key={feature.title} 
                xs={12} 
                sm={6} 
                md={6}
                lg={3}
                component={motion.div}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 + 0.2, duration: 0.5 }}
              >
                <Card 
                  className="magic-card" 
                  sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column',
                    minHeight: '280px' // Altura mínima consistente
                  }}
                >
                  <CardActionArea 
                    component={RouterLink} 
                    to={feature.link}
                    sx={{ 
                      flexGrow: 1, 
                      display: 'flex', 
                      flexDirection: 'column',
                      height: '100%' 
                    }}
                  >
                    <Box 
                      sx={{ 
                        bgcolor: feature.color,
                        color: 'white',
                        p: 3,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      {feature.icon}
                    </Box>
                    <CardContent sx={{ 
                      flexGrow: 1, 
                      display: 'flex', 
                      flexDirection: 'column',
                      justifyContent: 'space-between',
                      p: 3 
                    }}>
                      <Typography 
                        gutterBottom 
                        variant="h5" 
                        component="h2" 
                        sx={{ fontWeight: 'bold' }}
                      >
                        {feature.title}
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        {feature.description}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </MagicAnimation>
  );
};

export default HomePage;