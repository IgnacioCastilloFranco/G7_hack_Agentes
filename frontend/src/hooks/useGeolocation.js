import { useState } from 'react';

export const useGeolocation = (options = {}) => {
  const [state, setState] = useState({
    latitude: null,
    longitude: null,
    error: null,
    loading: false,
  });

  const getCurrentPosition = () => {
    if (!navigator.geolocation) {
      setState(prev => ({
        ...prev,
        error: 'La geolocalización no está soportada por este navegador',
        loading: false,
      }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));

    const defaultOptions = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 300000, // 5 minutos
      ...options,
    };

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setState({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          error: null,
          loading: false,
        });
      },
      (error) => {
        let errorMessage = 'Error desconocido al obtener la ubicación';
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Permiso denegado para acceder a la ubicación';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Información de ubicación no disponible';
            break;
          case error.TIMEOUT:
            errorMessage = 'Tiempo de espera agotado al obtener la ubicación';
            break;
          default:
            break;
        }
        
        setState({
          latitude: null,
          longitude: null,
          error: errorMessage,
          loading: false,
        });
      },
      defaultOptions
    );
  };

  return {
    ...state,
    getCurrentPosition,
  };
};