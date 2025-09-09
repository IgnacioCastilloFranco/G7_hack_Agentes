import React from 'react';
import type { SiteInfo, HistoricalContextResponse } from '../services/api';

interface HistoricalModalProps {
  site: SiteInfo | null;
  historicalContext: HistoricalContextResponse | null;
  isLoading: boolean;
  onClose: () => void;
}

const HistoricalModal: React.FC<HistoricalModalProps> = ({
  site,
  historicalContext,
  isLoading,
  onClose
}) => {
  if (!site) return null;

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content">
        <div className="modal-header">
          <h2>🏛️ {site.name}</h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        
        <div className="modal-body">
          <div className="site-basic-info">
            <p className="site-address">📍 {site.address}</p>
            {site.rating && (
              <div className="site-rating">
                <span className="stars">{'⭐'.repeat(Math.round(site.rating))}</span>
                <span className="rating-number">({site.rating})</span>
              </div>
            )}
          </div>
          
          <div className="historical-context">
            <h3>📚 Contexto Histórico y Cultural</h3>
            
            {isLoading ? (
              <div className="loading-context">
                <div className="loading-spinner"></div>
                <p>🔍 El Ratoncito Pérez está buscando información mágica...</p>
              </div>
            ) : historicalContext ? (
              <div className="context-content">
                {historicalContext.success ? (
                  <div className="context-text">
                    {historicalContext.context.split('\n').map((paragraph, index) => (
                      <p key={index}>{paragraph}</p>
                    ))}
                  </div>
                ) : (
                  <div className="context-error">
                    <p>❌ {historicalContext.message || 'No se pudo obtener información histórica'}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="context-placeholder">
                <p>Haz clic en "Obtener Información" para conocer la historia de este lugar.</p>
              </div>
            )}
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default HistoricalModal;