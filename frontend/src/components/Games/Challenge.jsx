import React from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Paper,
  Avatar,
  Grid,
  Chip
} from '@mui/material';
import { motion } from 'framer-motion';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';

const Challenge = ({ challenges, location, onNewGame }) => {
  return (
    <Box sx={{ mb: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
      >
        <Card className="magic-card" variant="outlined">
          <CardContent>
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography variant="h5" component="h2" sx={{ color: 'primary.main' }}>
                Retos Mágicos en {location}
              </Typography>
              <Chip 
                label={`${challenges.length} retos`}
                color="secondary"
                size="small"
              />
            </Box>
            
            <Paper 
              sx={{ 
                p: 2, 
                mb: 3, 
                bgcolor: 'magic.light',
                borderRadius: 2 
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar 
                  src="/images/ratoncito.png" 
                  alt="Ratoncito" 
                  sx={{ mr: 2, bgcolor: 'primary.main' }}
                >
                  🐭
                </Avatar>
                <Typography variant="body1">
                  ¡Por mis bigotitos! Aquí tienes algunos retos divertidos para hacer en {location}. 
                  ¡Recuerda siempre estar acompañado de un adulto!
                </Typography>
              </Box>
            </Paper>
            
            <Grid container spacing={3}>
              {challenges.map((challenge, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.2 }}
                  >
                    <Card 
                      variant="outlined" 
                      sx={{ 
                        height: '100%', 
                        display: 'flex', 
                        flexDirection: 'column',
                        position: 'relative',
                        overflow: 'hidden',
                        '&::after': {
                          content: '""',
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          width: '100%',
                          height: '4px',
                          background: index === 0 
                            ? 'linear-gradient(90deg, #f50057, #ff4081)'
                            : index === 1
                              ? 'linear-gradient(90deg, #3f51b5, #7986cb)'
                              : 'linear-gradient(90deg, #ff9800, #ffb74d)'
                        }
                      }}
                    >
                      <CardContent sx={{ flexGrow: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <AutoFixHighIcon sx={{ mr: 1, color: 'secondary.main' }} />
                          <Typography variant="h6" gutterBottom>
                            {challenge.title}
                          </Typography>
                        </Box>
                        <Typography variant="body2" paragraph>
                          {challenge.instructions}
                        </Typography>
                        <Paper 
                          sx={{ 
                            p: 1.5, 
                            bgcolor: 'magic.light', 
                            mt: 'auto',
                            borderRadius: 1
                          }}
                        >
                          <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                            <strong>Conexión mágica:</strong> {challenge.magic_connection}
                          </Typography>
                        </Paper>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={onNewGame}
              >
                Elegir otro reto
              </Button>
            </Box>
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Challenge;