import React from 'react';
import { Box, Container, Typography, Link, Grid, Divider } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: 'primary.dark',
        color: 'white',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={3} justifyContent="space-between">
          <Grid item xs={12} sm={6} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              🐭 Ratoncito Pérez
            </Typography>
            <Typography variant="body2">
              El guardián mágico de Madrid, ayudando a familias a descubrir la magia de la ciudad.
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              Enlaces Rápidos
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              <Link href="/" color="inherit" underline="hover">Inicio</Link>
              <Link href="/chat" color="inherit" underline="hover">Charla con el Ratoncito</Link>
              <Link href="/stories" color="inherit" underline="hover">Historias Mágicas</Link>
              <Link href="/games" color="inherit" underline="hover">Juegos y Acertijos</Link>
            </Box>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.2)' }} />
        
        <Typography variant="body2" align="center">
          © {new Date().getFullYear()} Ratoncito Pérez - Aventura Familiar
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;