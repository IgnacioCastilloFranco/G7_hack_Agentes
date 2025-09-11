import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Button, Box, IconButton, Tooltip } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import PlaceIcon from '@mui/icons-material/Place';
import ReplayIcon from '@mui/icons-material/Replay';

// Este componente envuelve las páginas de Aventura y Lugares para darles un menú común.
const AppLayout = ({ onRestartChat }) => {
  const navigate = useNavigate();

  // Estilos para los enlaces de navegación, para que se vea cuál está activo
  const navLinkStyle = ({ isActive }) => ({
    color: 'white',
    textDecoration: 'none',
    display: 'flex',
    alignItems: 'center',
    padding: '8px 16px',
    borderRadius: '20px',
    backgroundColor: isActive ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
    transition: 'all 0.3s ease',
    border: '1px solid transparent',
    '&:hover': {
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
      borderColor: 'rgba(255, 255, 255, 0.5)',
    }
  });

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: 'primary.dark', boxShadow: '0 4px 12px rgba(0,0,0,0.3)' }}>
        <Toolbar>
          <Tooltip title="Volver al Inicio">
            <Box
              component="img"
              src="/images/ratoncito.png" // Tu imagen del ratoncito
              sx={{ height: 40, mr: 2, cursor: 'pointer' }}
              onClick={() => navigate('/')} // Al hacer clic, vuelve a la página principal
              alt="Inicio"
            />
          </Tooltip>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', sm: 'flex' }, gap: 2 }}>
            <Button component={NavLink} to="/aventura" sx={navLinkStyle}>
              <ChatIcon sx={{ mr: 1 }} />
              Chat Mágico
            </Button>
            <Button component={NavLink} to="/lugares" sx={navLinkStyle}>
              <PlaceIcon sx={{ mr: 1 }} />
              Explorar Lugares
            </Button>
          </Box>
          <Tooltip title="Reiniciar Aventura">
            {/* El botón que reinicia el chat, llama a la función que le pasamos desde App.jsx */}
            <IconButton color="inherit" onClick={onRestartChat}>
              <ReplayIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>
      <main style={{ flexGrow: 1, padding: '16px' }}>
        {/* El <Outlet> es un marcador de posición donde se renderizará la página actual (Chat o Lugares) */}
        <Outlet />
      </main>
    </>
  );
};

export default AppLayout;
