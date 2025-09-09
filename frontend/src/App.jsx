import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import theme from './styles/theme';
import './styles/global.css';

// Layouts
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';

// Pages
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import GamesPage from './pages/GamePage'; 
import StoriesPage from './pages/StoriesPage';
import LocationsPage from './pages/LocationsPage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Header />
          <Box sx={{ flexGrow: 1, py: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/games" element={<GamesPage />} />
              <Route path="/stories" element={<StoriesPage />} />
              <Route path="/locations" element={<LocationsPage />} />
            </Routes>
          </Box>
          <Footer />
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;