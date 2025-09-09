import React, { useState } from 'react';
import { 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  CardActionArea,
  Typography,
  Button,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select
} from '@mui/material';
import { motion } from 'framer-motion';
import QuizIcon from '@mui/icons-material/Quiz';
import ExtensionIcon from '@mui/icons-material/Extension';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

const MADRID_LOCATIONS = [
  "Plaza Mayor",
  "Palacio Real",
  "Parque del Retiro",
  "Puerta del Sol",
  "Gran Vía",
  "Plaza de Cibeles",
  "Templo de Debod",
  "Museo del Prado",
  "Estadio Santiago Bernabéu",
  "Mercado de San Miguel"
];

const GAME_TYPES = [
  { value: 'riddle', label: 'Acertijos mágicos', icon: <ExtensionIcon />, description: 'Resuelve misterios y adivinanzas' },
  { value: 'trivia', label: 'Trivia madrileña', icon: <QuizIcon />, description: 'Pon a prueba tus conocimientos' },
  { value: 'challenge', label: 'Retos divertidos', icon: <EmojiEventsIcon />, description: 'Actividades para hacer en familia' }
];

const GameSelector = ({ onGameSelect }) => {
  const [location, setLocation] = useState('');
  const [gameType, setGameType] = useState('');
  const [ageRange, setAgeRange] = useState('7-12');
  const [difficulty, setDifficulty] = useState('medium');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    onGameSelect({
      type: gameType,
      params: {
        location,
        ageRange,
        difficulty,
      }
    });
  };
  
  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
      <Card className="magic-card" variant="outlined" sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            Elige tu aventura mágica
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required sx={{ mb: 2 }}>
                <InputLabel>Lugar mágico</InputLabel>
                <Select
                  value={location}
                  label="Lugar mágico"
                  onChange={(e) => setLocation(e.target.value)}
                >
                  {MADRID_LOCATIONS.map(loc => (
                    <MenuItem key={loc} value={loc}>{loc}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Edad</InputLabel>
                <Select
                  value={ageRange}
                  label="Edad"
                  onChange={(e) => setAgeRange(e.target.value)}
                >
                  <MenuItem value="4-6">4-6 años</MenuItem>
                  <MenuItem value="7-12">7-12 años</MenuItem>
                  <MenuItem value="13-15">13-15 años</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Dificultad</InputLabel>
                <Select
                  value={difficulty}
                  label="Dificultad"
                  onChange={(e) => setDifficulty(e.target.value)}
                >
                  <MenuItem value="easy">Fácil</MenuItem>
                  <MenuItem value="medium">Medio</MenuItem>
                  <MenuItem value="hard">Difícil</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Tipo de juego
              </Typography>
              <Grid container spacing={2}>
                {GAME_TYPES.map((type) => (
                  <Grid item xs={12} key={type.value}>
                    <Card 
                      variant={gameType === type.value ? "elevation" : "outlined"}
                      sx={{ 
                        cursor: 'pointer',
                        bgcolor: gameType === type.value ? 'primary.light' : 'background.paper',
                        color: gameType === type.value ? 'white' : 'inherit',
                        transition: '0.3s',
                      }}
                      onClick={() => setGameType(type.value)}
                    >
                      <CardActionArea>
                        <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                          <Box sx={{ mr: 2 }}>
                            {type.icon}
                          </Box>
                          <Box>
                            <Typography variant="h6">{type.label}</Typography>
                            <Typography variant="body2">{type.description}</Typography>
                          </Box>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Grid>
          </Grid>
          
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <Button 
              type="submit" 
              variant="contained" 
              size="large"
              disabled={!location || !gameType}
              sx={{ px: 4, py: 1 }}
            >
              ¡Comenzar Aventura!
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default GameSelector;