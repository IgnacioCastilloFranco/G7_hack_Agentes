import { useState, useCallback } from 'react'
import './App.css'
import LocationComponent from './components/LocationComponent'
import SearchComponent from './components/SearchComponent'
import SitesList from './components/SitesList'
import { apiService, type Site } from './services/api'

function App() {
  const [sites, setSites] = useState<Site[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [currentLocation, setCurrentLocation] = useState<{lat: number, lng: number} | null>(null)

  const handleLocationChange = useCallback(async (latitude: number, longitude: number) => {
    setCurrentLocation({ lat: latitude, lng: longitude })
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiService.getNearBySites({
        latitude,
        longitude,
        radius: 2000 // 2km radius
      })
      
      if (response.success) {
        setSites(response.sites)
      } else {
        setError(response.message || 'Error al obtener sitios cercanos')
      }
    } catch (err) {
      setError('Error de conexión al buscar sitios cercanos')
      console.error('Error fetching nearby sites:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const handleSearch = useCallback(async (query: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiService.searchSites({
        query,
        location: currentLocation ? `${currentLocation.lat},${currentLocation.lng}` : undefined
      })
      
      if (response.success) {
        setSites(response.sites)
      } else {
        setError(response.message || 'Error al buscar sitios')
      }
    } catch (err) {
      setError('Error de conexión al buscar sitios')
      console.error('Error searching sites:', err)
    } finally {
      setLoading(false)
    }
  }, [currentLocation])



  return (
    <div className="app">
      <header className="app-header">
        <h1>🐭 Ratoncito Pérez - Guía Mágico de Madrid</h1>
        <p>Descubre los lugares más mágicos de Madrid con tu guía favorito</p>
      </header>
      
      <main className="app-main">
        <div className="controls-section">
          <LocationComponent onLocationChange={handleLocationChange} />
          <SearchComponent onSearch={handleSearch} loading={loading} />
        </div>
        
        <div className="results-section">
          <SitesList 
            sites={sites}
            loading={loading}
            error={error}
          />
        </div>
      </main>
      
      <footer className="app-footer">
        <p>✨ Con amor, el Ratoncito Pérez ✨</p>
      </footer>
    </div>
  )
}

export default App
