import React from 'react';
import { useGeolocation } from '../hooks/useGeolocation';
import './components.css';

interface LocationComponentProps {
  onLocationChange?: (latitude: number, longitude: number) => void;
}

const LocationComponent: React.FC<LocationComponentProps> = ({ onLocationChange }) => {
  const { latitude, longitude, error, loading, getCurrentPosition } = useGeolocation({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 300000, // 5 minutes
  });

  const handleGetLocation = () => {
    getCurrentPosition();
  };

  React.useEffect(() => {
    if (latitude !== null && longitude !== null && onLocationChange) {
      onLocationChange(latitude, longitude);
    }
  }, [latitude, longitude, onLocationChange]);

  return (
    <div className="location-component">
      <h3>📍 Tu Ubicación</h3>
      
      <button 
        onClick={handleGetLocation} 
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="loading-spinner"></span>
            Obteniendo ubicación...
          </>
        ) : (
          '📍 Obtener mi ubicación'
        )}
      </button>

      {error && (
        <div className="location-status" style={{ color: '#dc2626' }}>
          ❌ Error: {error}
        </div>
      )}

      {latitude !== null && longitude !== null && (
        <div className="location-coordinates">
          <div><strong>📍 Coordenadas encontradas:</strong></div>
          <div>Latitud: {latitude.toFixed(6)}</div>
          <div>Longitud: {longitude.toFixed(6)}</div>
        </div>
      )}
    </div>
  );
};

export default LocationComponent;