// import api from './api';

// export const createGame = async (gameRequest) => {
//   try {
//     const response = await api.post('/activities/games', gameRequest);
//     return response.data;
//   } catch (error) {
//     console.error('Error creating game:', error);
//     throw error;
//   }
// };

// export const verifyAnswer = async (gameId, answer) => {
//   try {
//     const response = await api.post('/activities/games/verify', { 
//       game_id: gameId, 
//       answer 
//     });
//     return response.data;
//   } catch (error) {
//     console.error('Error verifying answer:', error);
//     throw error;
//   }
// };

// export const getTrivia = async (location, count = 3, ageRange = "7-12") => {
//   try {
//     const response = await api.get(`/activities/trivia/${location}?count=${count}&age_range=${ageRange}`);
//     return response.data;
//   } catch (error) {
//     console.error('Error getting trivia:', error);
//     throw error;
//   }
// };

// export const getChallenges = async (location, ageRange = "7-12") => {
//   try {
//     const response = await api.get(`/activities/challenges/${location}?age_range=${ageRange}`);
//     return response.data;
//   } catch (error) {
//     console.error('Error getting challenges:', error);
//     throw error;
//   }
// };