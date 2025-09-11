import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Divider,
  Grid,
  Chip,
  Alert
} from '@mui/material';
import { VolumeUp, AutoAwesome, Settings } from '@mui/icons-material';
import AudioButton from './AudioButton';
import TTSDemo from './TTSDemo';
import { useTTS } from '../../hooks/useTTS';

/**
 * Componente showcase que demuestra todas las funcionalidades TTS
 * implementadas para el Ratoncito Pérez
 */
const TTSShowcase = () => {
  const { isLoading, isPlaying, error } = useTTS();

  const demoTexts = {
    greeting: '¡Hola! Soy el Ratoncito Pérez y estoy aquí para ayudarte con todas tus preguntas sobre Madrid.',
    story: 'Había una vez un ratoncito muy especial que vivía en el Palacio Real de Madrid. Este ratoncito conocía todos los secretos y maravillas de la ciudad...',
    info: 'El Museo del Prado es uno de los museos más importantes del mundo, con obras maestras de Velázquez, Goya y El Greco.',
    fun: '¿Sabías que en Madrid hay más de 40 museos? ¡Es como un tesoro gigante de cultura esperando a ser descubierto!'
  };

  const features = [
    {
      title: 'Botón de Audio Inteligente',
      description: 'Cada mensaje del Ratoncito incluye un botón para escuchar el texto con su voz mágica',
      icon: <VolumeUp />,
      color: 'primary'
    },
    {
      title: 'Reproducción Automática',
      description: 'Opción para reproducir automáticamente cada respuesta del Ratoncito',
      icon: <AutoAwesome />,
      color: 'secondary'
    },
    {
      title: 'Configuración Avanzada',
      description: 'Control completo sobre velocidad, estabilidad y similitud de la voz',
      icon: <Settings />,
      color: 'success'
    }
  ];

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        🎭 Showcase TTS - Ratoncito Pérez
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>¡Funcionalidad TTS Completamente Integrada!</strong> 
          El sistema de texto a voz está ahora disponible en todo el chat. 
          Cada respuesta del Ratoncito Pérez puede ser escuchada con su voz mágica.
        </Typography>
      </Alert>

      <Grid container spacing={3}>
        {/* Características principales */}
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            ✨ Características Implementadas
          </Typography>
          <Grid container spacing={2}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ height: '100%', border: '1px solid', borderColor: 'divider' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Chip 
                        icon={feature.icon} 
                        label={feature.title}
                        color={feature.color}
                        variant="outlined"
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Demos de texto */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🎯 Prueba Rápida de Textos
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Haz clic en los botones para escuchar diferentes tipos de mensajes del Ratoncito:
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {Object.entries(demoTexts).map(([key, text]) => (
                  <Box key={key} sx={{ 
                    p: 2, 
                    border: '1px solid', 
                    borderColor: 'divider', 
                    borderRadius: 1,
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: 2
                  }}>
                    <AudioButton 
                      text={text} 
                      size="medium" 
                      color="primary" 
                      showProgress={true}
                    />
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="subtitle2" sx={{ textTransform: 'capitalize', mb: 0.5 }}>
                        {key === 'greeting' ? 'Saludo' : 
                         key === 'story' ? 'Historia' :
                         key === 'info' ? 'Información' : 'Diversión'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {text.length > 100 ? `${text.substring(0, 100)}...` : text}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Demo avanzado */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ⚙️ Configuración Avanzada
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Experimenta con diferentes configuraciones de voz:
              </Typography>
              <TTSDemo />
            </CardContent>
          </Card>
        </Grid>

        {/* Estado actual */}
        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              🚀 Estado del Sistema
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
              <Chip 
                label={isLoading ? 'Generando Audio...' : 'Sistema Listo'}
                color={isLoading ? 'warning' : 'success'}
                variant={isLoading ? 'filled' : 'outlined'}
              />
              <Chip 
                label={isPlaying ? 'Reproduciendo' : 'En Pausa'}
                color={isPlaying ? 'primary' : 'default'}
                variant={isPlaying ? 'filled' : 'outlined'}
              />
              {error && (
                <Chip 
                  label={`Error: ${error}`}
                  color="error"
                  variant="filled"
                />
              )}
            </Box>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TTSShowcase;