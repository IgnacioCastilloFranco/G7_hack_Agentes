// import React, { useState, useEffect } from 'react';
// import { Container, Typography, Box } from '@mui/material';
// import MagicAnimation from '../components/UI/MagicAnimation';
// import LoadingSpinner from '../components/UI/LoadingSpinner';
// import ErrorMessage from '../components/UI/ErrorMessage';
// import GameSelector from '../components/Games/GameSelector';
// import Riddle from '../components/Games/Riddle';
// import Trivia from '../components/Games/Trivia';
// import Challenge from '../components/Games/Challenge';
// import { createGame, getTrivia, getChallenges } from '../services/gameService';

// const GamesPage = () => {
//   const [gameParams, setGameParams] = useState(null);
//   const [gameData, setGameData] = useState(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState(null);
  
//   useEffect(() => {
//     if (gameParams) {
//       loadGame();
//     }
//   }, [gameParams]);
  
//   const loadGame = async () => {
//     if (!gameParams) return;
    
//     setIsLoading(true);
//     setError(null);
    
//     try {
//       switch (gameParams.type) {
//         case 'riddle':
//           const riddleGame = await createGame({
//             location: gameParams.params.location,
//             age_range: gameParams.params.ageRange,
//             difficulty: gameParams.params.difficulty,
//             game_type: 'riddle'
//           });
//           setGameData({ type: 'riddle', data: riddleGame });
//           break;
          
//         case 'trivia':
//           const triviaQuestions = await getTrivia(
//             gameParams.params.location, 
//             5, // 5 preguntas
//             gameParams.params.ageRange
//           );
//           setGameData({ 
//             type: 'trivia', 
//             data: { 
//               questions: triviaQuestions,
//               location: gameParams.params.location
//             }
//           });
//           break;
          
//         case 'challenge':
//           const challenges = await getChallenges(
//             gameParams.params.location,
//             gameParams.params.ageRange
//           );
//           setGameData({ 
//             type: 'challenge', 
//             data: { 
//               challenges: challenges.challenges,
//               location: gameParams.params.location 
//             }
//           });
//           break;
          
//         default:
//           throw new Error("Tipo de juego no soportado");
//       }
//     } catch (err) {
//       setError(err);
//     } finally {
//       setIsLoading(false);
//     }
//   };
  
//   const handleGameSelect = (params) => {
//     setGameParams(params);
//   };
  
//   const handleNewGame = () => {
//     setGameData(null);
//     setGameParams(null);
//   };
  
//   const renderGame = () => {
//     if (!gameData) return null;
    
//     switch (gameData.type) {
//       case 'riddle':
//         return <Riddle game={gameData.data} onNewGame={handleNewGame} />;
//       case 'trivia':
//         return (
//           <Trivia 
//             questions={gameData.data.questions} 
//             location={gameData.data.location}
//             onNewGame={handleNewGame} 
//           />
//         );
//       case 'challenge':
//         return (
//           <Challenge 
//             challenges={gameData.data.challenges} 
//             location={gameData.data.location}
//             onNewGame={handleNewGame} 
//           />
//         );
//       default:
//         return null;
//     }
//   };
  
//   return (
//     <MagicAnimation>
//       <Container>
//         <Box sx={{ mb: 4, textAlign: 'center' }}>
//           <Typography 
//             variant="h3" 
//             className="magic-text"
//             gutterBottom
//           >
//             Juegos y Acertijos Mágicos
//           </Typography>
//           <Typography variant="body1" sx={{ mb: 4 }}>
//             ¡Por mis bigotes! Tengo algunos juegos mágicos para ti. 
//             Pon a prueba tus conocimientos sobre Madrid con estos divertidos retos.
//           </Typography>
//         </Box>
        
//         {!gameData && !isLoading && <GameSelector onGameSelect={handleGameSelect} />}
        
//         {isLoading && (
//           <LoadingSpinner message="¡Por mis bigotitos! Estoy preparando un juego mágico para ti..." />
//         )}
        
//         {error && (
//           <ErrorMessage 
//             error={error} 
//             onRetry={() => loadGame()}
//           />
//         )}
        
//         {!isLoading && !error && renderGame()}
//       </Container>
//     </MagicAnimation>
//   );
// };

// export default GamesPage;