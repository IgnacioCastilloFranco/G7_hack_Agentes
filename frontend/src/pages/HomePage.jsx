import React from 'react';
import { Container, Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const HomePage = () => {
  return (
    <Container
      maxWidth="100%"
      sx={{
        height: '100vh',
        p: 0,
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: 'url(../public/images/madrid.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'blur(3px) brightness(0.9)', 
          transform: 'scale(1.05)', 
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'radial-gradient(circle, rgba(0, 41, 132, 0.3) 0%, rgba(63, 81, 181, 0.6) 100%)',
        }}
      />

      <Box sx={{ position: 'relative', zIndex: 1, textAlign: 'center', color: 'white' }}>
        <motion.div
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 80, damping: 10, delay: 0.2 }}
        >
          <Box
            component="img"
            src="../public/images/titulo.png" 
            alt="Secretos de Madrid con Pérez"
            sx={{
              width: { xs: '90%', sm: '70%', md: '500px' },
              maxWidth: '500px',
              height: 'auto',
              filter: 'drop-shadow(0 10px 15px rgba(0,0,0,0.4))'
            }}
          />
        </motion.div>

        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: 'spring', delay: 0.6, duration: 0.8 }}
        >
          <Button
            component={RouterLink}
            to="/aventura"
            variant="contained"
            size="large"
            className="magic-button"
            sx={{
              marginTop: '32px',
              px: { xs: 4, sm: 6 },
              py: 1.5,
              fontSize: { xs: '1rem', sm: '1.2rem' },
              borderRadius: '50px',
            }}
          >
            ¡Comenzar la Aventura!
          </Button>
        </motion.div>
      </Box>

      <motion.div
        initial={{ x: 200, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 50, delay: 1 }}
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          zIndex: 2
        }}
      >
        <Box
          component="img"
          src="/images/ratoncito.png"
          alt="Ratoncito Pérez"
          sx={{
            width: { xs: '100px', sm: '150px' },
            height: 'auto',
            filter: 'drop-shadow(0 5px 10px rgba(0,0,0,0.3))'
          }}
        />
      </motion.div>
    </Container>
  );
};

export default HomePage;
