// import React, { useState, useCallback } from 'react';
// import { Container, Typography, Box, Paper, Divider, Button } from '@mui/material';
// import { getNearbyPlaces, searchPlacesByText, getPopularPlaces } from '../services/narrativeService';
// import LocationComponent from '../components/Location/LocationComponent';
// import SearchComponent from '../components/Location/SearchComponent';
// import CategoryFilter from '../components/Location/CategoryFilter';
// import PlacesList from '../components/Stories/PlacesList';
// import HistoricalModal from '../components/Stories/HistoricalModal';

// const StoriesPage = () => {
//   const [places, setPlaces] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [currentLocation, setCurrentLocation] = useState(null);
  
//   // Estados para el modal
//   const [selectedPlace, setSelectedPlace] = useState(null);
//   const [historicalContext, setHistoricalContext] = useState(null);
//   const [loadingContext, setLoadingContext] = useState(false);
  
//   // Estados para la interfaz
//   const [initialLoad, setInitialLoad] = useState(true); 
//   const [selectedCategories, setSelectedCategories] = useState([]); 

//   const handleLoadPopularPlaces = async () => {
//     setIsLoading(true);
//     setInitialLoad(false); 
//     try {
//       const response = await getPopularPlaces();
//       if (response.success) {
//         setPlaces(response.sites);
//         setError(null);
//       } else {
//         setError("Error cargando lugares populares");
//       }
//     } catch (err) {
//       console.error("Error:", err);
//       setError("Error de conexión al servidor");
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleLocationChange = useCallback(async (latitude, longitude) => {
//     setCurrentLocation({ lat: latitude, lng: longitude });
//     setInitialLoad(false); 
//     setIsLoading(true);
    
//     try {
//       const response = await getNearbyPlaces({
//         latitude,
//         longitude,
//         radius: 5000
//       });
      
//       if (response.success) {
//         setPlaces(response.sites);
//         setError(null);
//       } else {
//         setError("No se encontraron lugares cercanos");
//       }
//     } catch (err) {
//       console.error("Error:", err);
//       setError("Error de conexión");
//     } finally {
//       setIsLoading(false);
//     }
//   }, []);

//   const handleSearch = useCallback(async (query) => {
//     setInitialLoad(false);
//     setIsLoading(true);
    
//     try {
//       const response = await searchPlacesByText({
//         query,
//         latitude: currentLocation?.lat,
//         longitude: currentLocation?.lng
//       });
      
//       if (response.success) {
//         setPlaces(response.sites);
//         setError(null);
//       } else {
//         setError("No se encontraron resultados");
//       }
//     } catch (err) {
//       console.error("Error:", err);
//       setError("Error de búsqueda");
//     } finally {
//       setIsLoading(false);
//     }
//   }, [currentLocation]);

//   const handleSelectPlace = useCallback(async (place) => {
//     setSelectedPlace(place);
//     setLoadingContext(true);
//     setHistoricalContext(null);
    
//     try {
//       const response = await getSiteHistoricalContext({
//         site_name: place.name,
//         site_address: place.address
//       });
      
//       setHistoricalContext(response);
//     } catch (err) {
//       console.error('Error obteniendo contexto histórico:', err);
//       setHistoricalContext({
//         context: 'Error al obtener información histórica',
//         success: false,
//         site_name: place.name,
//         message: 'No se pudo conectar con el servicio'
//       });
//     } finally {
//       setLoadingContext(false);
//     }
//   }, []);

//   const handleClosePlaceChat = () => {
//     setSelectedPlace(null);
//     setHistoricalContext(null);
//   };

//   const filterPlacesByCategory = (places, categories) => {
//     if (categories.length === 0) return places;
    
//     return places.filter(place => 
//       place.types && place.types.some(type => categories.includes(type))
//     );
//   };

//   const scrollToLocation = () => {
//     document.querySelector('[data-location-section]')?.scrollIntoView({ 
//       behavior: 'smooth' 
//     });
//   };

//   return (
//     <Container maxWidth="lg">
//       <Box sx={{ my: 4 }}>
//         <Typography variant="h3" component="h1" gutterBottom align="center">
//           Historias Mágicas de Madrid
//         </Typography>
        
//         {!selectedPlace ? (
//           <>
//             {/* Sección de controles */}
//             <Paper 
//               elevation={3} 
//               sx={{ p: 3, mb: 4 }} 
//               data-location-section
//             >
//               <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
//                 <Box sx={{ flex: 1 }}>
//                   <LocationComponent onLocationChange={handleLocationChange} />
//                 </Box>
//                 <Divider orientation="vertical" flexItem sx={{ display: { xs: 'none', md: 'block' } }} />
//                 <Divider sx={{ display: { xs: 'block', md: 'none' } }} />
//                 <Box sx={{ flex: 1 }}>
//                   <SearchComponent onSearch={handleSearch} loading={isLoading} />
//                 </Box>
//               </Box>
//             </Paper>

//             {!initialLoad && (
//               <CategoryFilter 
//                 selectedCategories={selectedCategories}
//                 onCategorySelect={setSelectedCategories}
//               />
//             )}

//             {initialLoad ? (
//               <Box sx={{ textAlign: 'center', py: 6 }}>
//                 <Typography variant="h4" gutterBottom className="magic-text">
//                   🐭✨ ¡Hola! Soy el Ratoncito Pérez
//                 </Typography>
//                 <Typography variant="h6" gutterBottom sx={{ mb: 4, color: 'text.secondary' }}>
//                   ¡Descubre lugares mágicos de Madrid conmigo!
//                 </Typography>
                
//                 <Box sx={{ 
//                   display: 'flex', 
//                   gap: 2, 
//                   justifyContent: 'center', 
//                   flexWrap: 'wrap',
//                   mb: 4 
//                 }}>
//                   <Button 
//                     variant="contained" 
//                     color="primary" 
//                     size="large"
//                     onClick={handleLoadPopularPlaces}
//                     disabled={isLoading}
//                     sx={{ 
//                       fontSize: '1.1rem',
//                       py: 1.5,
//                       px: 3,
//                       borderRadius: 3
//                     }}
//                   >
//                     🌟 Ver Lugares Populares
//                   </Button>
//                   <Button 
//                     variant="outlined" 
//                     color="secondary" 
//                     size="large"
//                     onClick={scrollToLocation}
//                     sx={{ 
//                       fontSize: '1.1rem',
//                       py: 1.5,
//                       px: 3,
//                       borderRadius: 3
//                     }}
//                   >
//                     📍 Buscar Cerca de Ti
//                   </Button>
//                 </Box>

//                 <Box sx={{ 
//                   bgcolor: 'background.paper',
//                   p: 3,
//                   borderRadius: 2,
//                   border: '2px dashed #d1d5db',
//                   maxWidth: 600,
//                   mx: 'auto'
//                 }}>
//                   <Typography variant="body1" sx={{ mb: 2 }}>
//                     💡 <strong>¿Cómo funciona?</strong>
//                   </Typography>
//                   <Typography variant="body2" color="text.secondary">
//                     • 📍 <strong>Detecta tu ubicación</strong> para encontrar lugares cercanos<br/>
//                     • 🔍 <strong>Busca lugares específicos</strong> escribiendo el nombre<br/>
//                     • 🏛️ <strong>Explora lugares populares</strong> de Madrid<br/>
//                     • 📚 <strong>Descubre historias mágicas</strong> sobre cada lugar
//                   </Typography>
//                 </Box>
//               </Box>
//             ) : (
//               <PlacesList 
//                 places={filterPlacesByCategory(places, selectedCategories)}
//                 isLoading={isLoading}
//                 error={error}
//                 onSelectPlace={handleSelectPlace}
//               />
//             )}
//           </>
//         ) : (
//           <HistoricalModal
//             site={selectedPlace}
//             historicalContext={historicalContext}
//             isLoading={loadingContext}
//             onClose={handleClosePlaceChat}
//           />
//         )}
//       </Box>
//     </Container>
//   );
// };

// export default StoriesPage;