import React, { useState } from 'react';
import { Box, Typography, Chip, Paper } from '@mui/material';

const CategoryFilter = ({ onCategorySelect, selectedCategories = [] }) => {
  const categories = [
    { id: 'all', label: '🌟 Todos', emoji: '🌟' },
    { id: 'museum', label: '🏛️ Museos', emoji: '🏛️' },
    { id: 'church', label: '⛪ Iglesias', emoji: '⛪' },
    { id: 'tourist_attraction', label: '🏰 Atracciones', emoji: '🏰' },
    { id: 'art_gallery', label: '🎨 Galerías', emoji: '🎨' },
    { id: 'library', label: '📚 Bibliotecas', emoji: '📚' },
    { id: 'university', label: '🎓 Universidades', emoji: '🎓' },
    { id: 'park', label: '🌳 Parques', emoji: '🌳' },
    { id: 'restaurant', label: '🍽️ Restaurantes', emoji: '🍽️' },
  ];

  const handleCategoryClick = (categoryId) => {
    if (categoryId === 'all') {
      onCategorySelect([]);
    } else {
      const newSelected = selectedCategories.includes(categoryId)
        ? selectedCategories.filter(id => id !== categoryId)
        : [...selectedCategories, categoryId];
      onCategorySelect(newSelected);
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 2, mb: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
      <Typography variant="subtitle2" gutterBottom>
        🏷️ Filtrar por categorías:
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {categories.map((category) => (
          <Chip
            key={category.id}
            label={category.label}
            onClick={() => handleCategoryClick(category.id)}
            variant={
              category.id === 'all' && selectedCategories.length === 0
                ? 'filled'
                : selectedCategories.includes(category.id)
                ? 'filled'
                : 'outlined'
            }
            color={
              category.id === 'all' && selectedCategories.length === 0
                ? 'primary'
                : selectedCategories.includes(category.id)
                ? 'primary'
                : 'default'
            }
            sx={{
              '&:hover': {
                bgcolor: selectedCategories.includes(category.id) ? 'primary.dark' : 'primary.light',
                color: 'white'
              }
            }}
          />
        ))}
      </Box>
    </Paper>
  );
};

export default CategoryFilter;