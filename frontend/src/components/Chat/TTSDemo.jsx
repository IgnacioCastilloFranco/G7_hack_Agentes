import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from '@mui/material';
import { VolumeUp, Settings } from '@mui/icons-material';
import { ttsService } from '../../services/ttsService';

const TTSDemo = () => {
  const [text, setText] = useState('¡Hola! Soy el Ratoncito Pérez y ahora puedo hablar contigo con mi voz mágica.');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  // Configuraciones de voz con el ID específico
  const [voiceSettings, setVoiceSettings] = useState({
    voice_id: 'iFhPOZcajR7W3sDL39qJ',
    stability: 0.6,
    similarity_boost: 0.8,
    speed: 1.0
  });
  const [model, setModel] = useState('eleven_multilingual_v2');

  const handlePlayAudio = async () => {
    if (!text.trim()) {
      setError('Por favor, escribe algo para que el Ratoncito pueda decir');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await ttsService.playText(text, {
        voice_id: voiceSettings.voice_id,
        model_id: model,
        stability: voiceSettings.stability,
        similarity_boost: voiceSettings.similarity_boost,
        speed: voiceSettings.speed
      });
      setSuccess(true);
    } catch (err) {
      console.error('Error en TTS Demo:', err);
      setError('No pude generar el audio. ¿Mis cuerdas vocales mágicas están funcionando?');
    } finally {
      setIsLoading(false);
    }
  };

  const updateVoiceSetting = (key, value) => {
    setVoiceSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const availableModels = [
    { value: 'eleven_multilingual_v2', label: 'Multilingüe v2 (Recomendado)' },
    { value: 'eleven_monolingual_v1', label: 'Monolingüe v1' },
    { value: 'eleven_multilingual_v1', label: 'Multilingüe v1' }
  ];

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Settings sx={{ mr: 1, color: 'primary.main' }} />
        <Typography variant="h6" color="primary">
          🎭 Configurador de Voz del Ratoncito
        </Typography>
      </Box>

      {/* Campo de texto */}
      <TextField
        fullWidth
        multiline
        rows={3}
        label="Texto para el Ratoncito"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Escribe lo que quieres que diga el Ratoncito Pérez..."
        sx={{ mb: 3 }}
        disabled={isLoading}
      />

      {/* Configuraciones de voz */}
      <Typography variant="subtitle1" gutterBottom sx={{ mt: 2, mb: 2 }}>
        ⚙️ Configuración de Voz
      </Typography>

      {/* Modelo de voz */}
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>Modelo de Voz</InputLabel>
        <Select
          value={model}
          label="Modelo de Voz"
          onChange={(e) => setModel(e.target.value)}
          disabled={isLoading}
        >
          {availableModels.map((modelOption) => (
            <MenuItem key={modelOption.value} value={modelOption.value}>
              {modelOption.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Controles deslizantes */}
      <Box sx={{ mb: 2 }}>
        <Typography gutterBottom>Estabilidad: {voiceSettings.stability}</Typography>
        <Slider
          value={voiceSettings.stability}
          onChange={(_, value) => updateVoiceSetting('stability', value)}
          min={0}
          max={1}
          step={0.1}
          disabled={isLoading}
          sx={{ mb: 2 }}
        />
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography gutterBottom>Similitud: {voiceSettings.similarity_boost}</Typography>
        <Slider
          value={voiceSettings.similarity_boost}
          onChange={(_, value) => updateVoiceSetting('similarity_boost', value)}
          min={0}
          max={1}
          step={0.1}
          disabled={isLoading}
          sx={{ mb: 2 }}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <Typography gutterBottom>Velocidad: {voiceSettings.speed}</Typography>
        <Slider
          value={voiceSettings.speed}
          onChange={(_, value) => updateVoiceSetting('speed', value)}
          min={0.5}
          max={2.0}
          step={0.1}
          disabled={isLoading}
          sx={{ mb: 2 }}
        />
      </Box>

      {/* Información del ID de voz */}
      <Alert severity="info" sx={{ mb: 2 }}>
        <Typography variant="body2">
          <strong>ID de Voz:</strong> {voiceSettings.voice_id}
          <br />
          Esta es la voz específica del Ratoncito Pérez configurada para la aplicación.
        </Typography>
      </Alert>

      {/* Botón de reproducción */}
      <Button
        fullWidth
        variant="contained"
        color="primary"
        onClick={handlePlayAudio}
        disabled={isLoading || !text.trim()}
        startIcon={isLoading ? <CircularProgress size={20} /> : <VolumeUp />}
        sx={{ mb: 2, py: 1.5 }}
      >
        {isLoading ? 'Generando voz mágica...' : 'Escuchar con la voz del Ratoncito'}
      </Button>

      {/* Mensajes de estado */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          ¡Audio generado exitosamente! 🎉
        </Alert>
      )}

      {/* Información adicional */}
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        💡 <strong>Consejos:</strong>
        <br />• Estabilidad alta = voz más consistente
        <br />• Similitud alta = más parecido a la voz original
        <br />• Velocidad 1.0 = velocidad normal
      </Typography>
    </Paper>
  );
};

export default TTSDemo;