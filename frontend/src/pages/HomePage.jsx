import React from 'react';
import { Container, Typography, Box, Button, Avatar } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const HomePage = () => {
  return (
    <Container
      maxWidth="100%"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        textAlign: 'center',
        background: 'linear-gradient(180deg, #3f51b5 0%, #002984 100%)',
        color: 'white',
        p: 4,
      }}
    >
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 120, damping: 15, delay: 0.2 }}
      >
        <Avatar
          src="/images/ratoncito.png"
          alt="Ratoncito Pérez"
          sx={{
            width: 200,
            height: 200,
            mb: 4,
            border: '5px solid white',
            boxShadow: '0 8px 30px rgba(0,0,0,0.4)',
          }}
        />
      </motion.div>

      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ type: 'spring', delay: 0.5, duration: 0.8 }}
      >
        <Typography
          variant="h2"
          component="h1"
          gutterBottom
          className="magic-text"
          sx={{ fontWeight: 'bold' }}
        >
          Madrid Mágico con el Ratoncito Pérez
        </Typography>
        <Typography variant="h5" sx={{ mb: 5, maxWidth: '600px' }}>
          ¡Hola, aventurero! Soy el Ratoncito Pérez y seré tu guía en un viaje inolvidable por los secretos de Madrid.
        </Typography>
        <Button
          component={RouterLink}
          to="/aventura"
          variant="contained"
          color="secondary"
          size="large"
          sx={{
            px: 6,
            py: 1.5,
            fontSize: '1.2rem',
            borderRadius: '50px',
            boxShadow: '0 5px 15px rgba(245, 0, 87, .4)',
            transition: 'transform 0.2s',
            '&:hover': {
                transform: 'scale(1.05)'
            }
          }}
        >
          ¡Comenzar la Aventura!
        </Button>
      </motion.div>
    </Container>
  );
};

export default HomePage;
