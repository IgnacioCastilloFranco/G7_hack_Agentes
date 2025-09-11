import React, { useState, useCallback, useMemo } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import theme from './styles/theme';
import './styles/global.css';

import HomePage from './pages/HomePage';
import AdventurePage from './pages/AdventurePage';
import LocationsPage from './pages/LocationsPage';
import AppLayout from './components/Layout/AppLayout';

const MagicBubbles = () => {
  const bubbles = useMemo(() => 
    Array.from({ length: 15 }).map((_, i) => {
      const size = `${Math.random() * (120 - 20) + 20}px`;
      const left = `${Math.random() * 100}%`;
      const animationDuration = `${Math.random() * (30 - 15) + 15}s`;
      const animationDelay = `${Math.random() * 10}s`;
      return (
        <div
          key={i}
          className="bubble"
          style={{ width: size, height: size, left, animationDuration, animationDelay }}
        />
      );
    }), []);
  return <div className="bubbles-container">{bubbles}</div>;
};

const AppContent = () => {
  const location = useLocation();
  const [sessionKey, setSessionKey] = useState(Date.now());

  const handleRestartChat = useCallback(() => {
    setSessionKey(Date.now());
  }, []);

  // --- CAMBIO CLAVE: Lógica de fondos más específica ---
  // El fondo de cielo simple se aplica a /aventura y /lugares
  const showMagicBackground = ['/aventura', '/lugares'].includes(location.pathname);
  // Las burbujas (que consumen más) solo se aplican a /lugares
  const showBubbles = location.pathname === '/lugares';

  return (
    <Box className={showMagicBackground ? "magic-background" : ""} sx={{ minHeight: '100vh' }}>
      {/* Las burbujas solo se renderizan en las páginas que queremos */}
      {showBubbles && <MagicBubbles />}
      
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route element={<AppLayout onRestartChat={handleRestartChat} />}>
          <Route path="/aventura" element={<AdventurePage key={sessionKey} />} />
          <Route path="/lugares" element={<LocationsPage />} />
        </Route>
      </Routes>
    </Box>
  );
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;