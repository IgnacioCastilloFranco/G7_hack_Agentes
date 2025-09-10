import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import theme from './styles/theme';
import './styles/global.css';

// NUESTRA NUEVA PÁGINA PRINCIPAL
import AdventurePage from './pages/AdventurePage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        minHeight: '100vh',
        background: 'linear-gradient(180deg, #e0c3fc 0%, #8ec5fc 100%)' // Un fondo mágico
      }}>
        
        <AdventurePage />
      </Box>
    </ThemeProvider>
  );
}

export default App;