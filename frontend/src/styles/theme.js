import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#3f51b5', // Azul mágico
      light: '#757de8',
      dark: '#002984',
    },
    secondary: {
      main: '#f50057', // Rosa mágico
      light: '#ff5983',
      dark: '#bb002f',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    magic: {
      light: '#e3f2fd', 
      main: '#90caf9', 
      dark: '#42a5f5', 
      contrastText: '#000',
    },
  },
  typography: {
    fontFamily: '"Nunito", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 30,
          textTransform: 'none',
          fontWeight: 600,
          padding: '8px 16px',
        },
        containedPrimary: {
          background: 'linear-gradient(45deg, #3f51b5 30%, #7986cb 90%)',
          boxShadow: '0 3px 5px 2px rgba(63, 81, 181, .3)',
          '&:hover': {
            background: 'linear-gradient(45deg, #303f9f 30%, #5c6bc0 90%)',
            boxShadow: '0 4px 6px 2px rgba(63, 81, 181, .4)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          overflow: 'hidden',
        },
      },
    },
  },
});

export default theme;