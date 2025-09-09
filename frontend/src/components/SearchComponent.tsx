import React, { useState } from 'react';
import './components.css';

interface SearchComponentProps {
  onSearch: (query: string) => void;
  loading?: boolean;
  placeholder?: string;
}

const SearchComponent: React.FC<SearchComponentProps> = ({ 
  onSearch, 
  loading = false, 
  placeholder = "Buscar lugares mágicos en Madrid..." 
}) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  const popularSearches = [
    '🎨 Museo del Prado',
    '👑 Palacio Real',
    '🌳 Parque del Retiro',
    '🏛️ Plaza Mayor',
    '☀️ Puerta del Sol',
    '🏺 Templo de Debod',
    '🎭 Teatro Real',
    '🏟️ Santiago Bernabéu'
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setError(null);
      onSearch(query.trim());
    } else {
      setError('Por favor, introduce un término de búsqueda');
    }
  };

  const handleClear = () => {
    setQuery('');
    setError(null);
  };

  const handlePopularSearch = (searchTerm: string) => {
    const cleanTerm = searchTerm.replace(/^[🎨👑🌳🏛️☀️🏺🎭🏟️]\s/u, ''); // Remove emoji prefix
    setQuery(cleanTerm);
    setError(null);
    onSearch(cleanTerm);
  };

  return (
    <div className="search-component">
      <h3>🔍 Buscar Lugares Mágicos</h3>
      
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className="search-input"
        />
        <button 
          type="submit" 
          disabled={loading || !query.trim()}
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Buscando...
            </>
          ) : (
            '🔍 Buscar'
          )}
        </button>
        {query && (
          <button 
            type="button" 
            onClick={handleClear}
            style={{
              background: 'linear-gradient(135deg, #6c757d 0%, #495057 100%)',
              minWidth: 'auto',
              padding: '0.75rem'
            }}
          >
            ✖️
          </button>
        )}
      </form>

      {error && (
        <div style={{ color: '#dc2626', fontSize: '0.9rem', textAlign: 'center' }}>
          ⚠️ {error}
        </div>
      )}

      <div>
        <h4 style={{ margin: '1rem 0 0.75rem 0', fontSize: '0.95rem', color: '#4a5568', textAlign: 'center' }}>
          ✨ Lugares populares que el Ratoncito Pérez recomienda:
        </h4>
        <div className="search-tags">
          {popularSearches.map((search, index) => (
            <button
              key={index}
              onClick={() => handlePopularSearch(search)}
              disabled={loading}
              className="search-tag"
            >
              {search}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchComponent;