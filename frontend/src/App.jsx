import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import theme from './styles/theme';
import './styles/global.css';

import HomePage from './pages/HomePage';
import AdventurePage from './pages/AdventurePage';
import LocationsPage from './pages/LocationsPage';
import AppLayout from './components/AppLayout';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          minHeight: '100vh',
          // Mantenemos el fondo mágico global
          backgroundImage: 'url(/images/magic-bg.png)',
          backgroundRepeat: 'repeat',
        }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            {/* Rutas que usan el layout con navegación */}
            <Route element={<AppLayout />}>
              <Route path="/aventura" element={<AdventurePage />} />
              <Route path="/lugares" element={<LocationsPage />} />
            </Route>
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
