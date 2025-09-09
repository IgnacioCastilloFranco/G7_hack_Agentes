import React from 'react';
import type { SiteInfo } from '../services/api';

interface SitesListProps {
  sites: SiteInfo[];
  isLoading: boolean;
  error?: string | null;
  onSiteClick?: (site: SiteInfo) => void;
}

const SitesList: React.FC<SitesListProps> = ({ sites, isLoading, error, onSiteClick }) => {
  const formatDistance = (distance?: number): string => {
    if (!distance) return '';
    if (distance < 1000) {
      return `${Math.round(distance)}m`;
    }
    return `${(distance / 1000).toFixed(1)}km`;
  };

  const getTypeIcon = (types?: string[]): string => {
    if (!types) return '🏛️';
    
    if (types.includes('museum')) return '🏛️';
    if (types.includes('church') || types.includes('place_of_worship')) return '⛪';
    if (types.includes('art_gallery')) return '🎨';
    if (types.includes('library')) return '📚';
    if (types.includes('university')) return '🎓';
    if (types.includes('tourist_attraction')) return '🏰';
    
    return '🏛️';
  };

  if (error) {
    return (
      <div className="error">
        <p>❌ {error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>🔍 Buscando lugares mágicos cerca de ti...</p>
      </div>
    );
  }

  if (sites.length === 0) {
    return (
      <div className="no-sites">
        <p>No se encontraron sitios culturales e históricos en esta área. ¡Prueba en otra ubicación!</p>
      </div>
    );
  }

  return (
    <div className="sites-list">
      <h3>🏛️ Sitios Culturales e Históricos Encontrados</h3>
      <div className="sites-grid">
        {sites.map((site, index) => (
          <div 
            key={site.place_id || index} 
            className={`site-card ${onSiteClick ? 'clickable' : ''}`}
            onClick={() => onSiteClick?.(site)}
            style={{ cursor: onSiteClick ? 'pointer' : 'default' }}
          >
            <div className="site-header">
              <div className="site-title">
                <span className="site-icon">{getTypeIcon(site.types)}</span>
                <h4>{site.name}</h4>
              </div>
              <div className="site-meta">
                {site.distance && (
                  <span className="site-distance">{formatDistance(site.distance)}</span>
                )}
                {site.rating && (
                  <div className="site-rating">
                    <span className="stars">{'⭐'.repeat(Math.round(site.rating))}</span>
                    <span className="rating-number">({site.rating})</span>
                  </div>
                )}
              </div>
            </div>
            <p className="site-address">📍 {site.address}</p>
            <p className="site-description">{site.description}</p>
            {site.photo_url && (
              <img 
                src={site.photo_url} 
                alt={site.name}
                className="site-photo"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SitesList;