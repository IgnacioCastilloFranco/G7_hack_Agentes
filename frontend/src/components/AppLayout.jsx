import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box, Avatar } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import PlaceIcon from '@mui/icons-material/Place';

// Este componente envuelve las páginas de Aventura y Lugares para darles un menú común.
const AppLayout = () => {
  const navLinkStyle = ({ isActive }) => ({
    color: isActive ? '#f50057' : 'white',
    textDecoration: 'none',
    display: 'flex',
    alignItems: 'center',
    padding: '8px 16px',
    borderRadius: '20px',
    backgroundColor: isActive ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
    transition: 'background-color 0.3s',
  });

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: 'primary.dark', boxShadow: '0 4px 12px rgba(0,0,0,0.3)' }}>
        <Toolbar>
          <Avatar src="/images/ratoncito.png" sx={{ mr: 2, border: '2px solid white' }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            Aventura Mágica
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button component={NavLink} to="/aventura" style={navLinkStyle}>
              <ChatIcon sx={{ mr: 1 }} />
              Chat
            </Button>
            <Button component={NavLink} to="/lugares" style={navLinkStyle}>
              <PlaceIcon sx={{ mr: 1 }} />
              Lugares
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      {/* El <Outlet> renderizará el componente de la ruta hija (AdventurePage o LocationsPage) */}
      <main style={{ flexGrow: 1, padding: '16px' }}>
        <Outlet />
      </main>
    </>
  );
};

export default AppLayout;