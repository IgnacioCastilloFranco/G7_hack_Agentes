import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Chip, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import CircularProgress from '@mui/material/CircularProgress';

const SearchComponent = ({ onSearch, loading = false }) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState(null);

  const popularSearches = [
    { label: 'Museo del Prado', emoji: '🎨' },
    { label: 'Palacio Real', emoji: '👑' },
    { label: 'Parque del Retiro', emoji: '🌳' },
    { label: 'Plaza Mayor', emoji: '🏛️' },
    { label: 'Puerta del Sol', emoji: '☀️' },
    { label: 'Templo de Debod', emoji: '🏺' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setError(null);
      onSearch(query.trim());
    } else {
      setError('Por favor, introduce un término de búsqueda');
    }
  };

  const handleClear = () => {
    setQuery('');
    setError(null);
  };

  const handlePopularSearch = (searchTerm) => {
    setQuery(searchTerm);
    setError(null);
    onSearch(searchTerm);
  };

  return (
    <Box 
      component={motion.div}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      sx={{ mb: 4 }}
    >
      <Typography variant="h6" gutterBottom>
        🔍 Buscar Lugares Mágicos
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', mb: 2 }}>
          <TextField
            fullWidth
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar lugares mágicos en Madrid..."
            disabled={loading}
            sx={{ mr: 1 }}
          />
          <Button 
            type="submit" 
            variant="contained" 
            color="secondary"
            disabled={loading || !query.trim()}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </Button>
          {query && (
            <Button 
              onClick={handleClear}
              variant="outlined" 
              color="inherit"
              sx={{ ml: 1 }}
              disabled={loading}
            >
              <ClearIcon />
            </Button>
          )}
        </Box>
      </Box>

      {error && (
        <Typography color="error" variant="body2" sx={{ mb: 2 }}>
          ⚠️ {error}
        </Typography>
      )}

      <Paper 
        elevation={0} 
        sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2 }}
      >
        <Typography variant="subtitle2" gutterBottom>
          ✨ Lugares populares que el Ratoncito Pérez recomienda:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {popularSearches.map((search, index) => (
            <Chip
              key={index}
              label={`${search.emoji} ${search.label}`}
              onClick={() => handlePopularSearch(search.label)}
              disabled={loading}
              sx={{ '&:hover': { bgcolor: 'primary.light', color: 'white' } }}
              variant="outlined"
            />
          ))}
        </Box>
      </Paper>
    </Box>
  );
};

export default SearchComponent;