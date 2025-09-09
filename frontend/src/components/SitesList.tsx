import React from 'react';
import { type Site } from '../services/api';
import './components.css';

interface SitesListProps {
  sites: Site[];
  loading: boolean;
  error: string | null;
}

const SitesList: React.FC<SitesListProps> = ({ sites, loading, error }) => {
  if (loading) {
    return (
      <div className="sites-list-loading">
        <div className="loading-spinner large"></div>
        <p>El Ratoncito Pérez está buscando lugares mágicos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="sites-list-error">
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🐭💫</div>
        <p>¡Ups! El Ratoncito Pérez encontró un problemita:</p>
        <p style={{ fontWeight: 'bold', color: '#dc2626' }}>{error}</p>
        <p style={{ fontSize: '0.9rem', marginTop: '1rem' }}>¡Inténtalo de nuevo en un ratito!</p>
      </div>
    );
  }

  if (sites.length === 0) {
    return (
      <div className="sites-list-empty">
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🐭🔍</div>
        <p>¡El Ratoncito Pérez no encontró lugares con ese nombre!</p>
        <p style={{ fontSize: '0.9rem', color: '#6b7280' }}>Prueba buscando algo como "Palacio Real" o "Museo del Prado"</p>
      </div>
    );
  }

  return (
    <div className="sites-list">
      <h3>🏛️ Lugares Mágicos Encontrados ({sites.length})</h3>
      <div className="sites-grid">
        {sites.map((site, index) => (
          <div key={index} className="site-card">
            <div className="site-header">
              <h4>📍 {site.name}</h4>
              {site.rating && (
                <div className="site-rating">
                  <span className="stars">{'⭐'.repeat(Math.floor(site.rating))}</span>
                  <span className="rating-number">{site.rating}</span>
                </div>
              )}
            </div>
            
            <div className="site-details">
              {site.address && (
                <div className="site-detail">
                  <span className="detail-icon">🏠</span>
                  <span className="detail-text">{site.address}</span>
                </div>
              )}
              
              {site.description && (
                <div className="site-detail">
                  <span className="detail-icon">📝</span>
                  <span className="detail-text">{site.description}</span>
                </div>
              )}
            </div>
            
            <div className="site-actions">
              <a 
                href={`https://www.google.com/maps?q=${site.latitude},${site.longitude}`}
                target="_blank"
                rel="noopener noreferrer"
                className="maps-button"
              >
                🗺️ Ver en Google Maps
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SitesList;