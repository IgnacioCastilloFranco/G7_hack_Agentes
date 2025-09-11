import React from 'react';
import { IconButton, Tooltip, CircularProgress, LinearProgress, Box } from '@mui/material';
import { VolumeUp, VolumeOff, Pause } from '@mui/icons-material';
import { useTTS } from '../../hooks/useTTS';

const AudioButton = ({ text, size = 'small', color = 'primary', showProgress = false }) => {
  const { isLoading, isPlaying, error, progress, toggle } = useTTS({
    voice_id: 'iFhPOZcajR7W3sDL39qJ',
    stability: 0.6,
    similarity_boost: 0.8,
    speed: 1.0
  });

  const handleClick = () => {
    if (!text || text.trim() === '') {
      return;
    }
    toggle(text);
  };

  const getIcon = () => {
    if (isLoading) {
      return <CircularProgress size={size === 'small' ? 16 : 20} color={color} />;
    }
    if (error) {
      return <VolumeOff />;
    }
    if (isPlaying) {
      return <Pause />;
    }
    return <VolumeUp />;
  };

  const getTooltip = () => {
    if (isLoading) return 'Generando audio mágico...';
    if (error) return `Error: ${error}`;
    if (isPlaying) return 'Pausar voz del Ratoncito';
    return 'Escuchar con la voz del Ratoncito Pérez';
  };

  const buttonContent = (
    <IconButton
      onClick={handleClick}
      disabled={isLoading || !text?.trim()}
      size={size}
      color={error ? 'error' : color}
      sx={{
        opacity: error ? 0.5 : 1,
        backgroundColor: error ? 'error.light' : `${color}.light`,
        border: `2px solid ${error ? 'error.main' : `${color}.main`}`,
        '&:hover': {
          backgroundColor: error ? 'error.main' : `${color}.main`,
          opacity: 0.9,
          transform: 'scale(1.1)'
        },
        transition: 'all 0.2s ease-in-out',
        '&:disabled': {
          opacity: 0.3
        },
        margin: '4px'
      }}
    >
      {getIcon()}
    </IconButton>
  );

  if (showProgress && (isLoading || isPlaying)) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 60 }}>
        <Tooltip title={getTooltip()} arrow>
          {buttonContent}
        </Tooltip>
        {(isLoading || isPlaying) && (
          <LinearProgress 
            variant={isLoading ? 'indeterminate' : 'determinate'}
            value={progress}
            sx={{ 
              width: '100%', 
              mt: 0.5, 
              height: 2,
              borderRadius: 1,
              '& .MuiLinearProgress-bar': {
                backgroundColor: color === 'primary' ? 'primary.main' : `${color}.main`
              }
            }}
          />
        )}
      </Box>
    );
  }

  return (
    <Tooltip title={getTooltip()} arrow>
      {buttonContent}
    </Tooltip>
  );
};

export default AudioButton;