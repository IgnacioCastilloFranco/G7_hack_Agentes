import api from './api';

export const getNearbyPlaces = async ({ latitude, longitude, radius = 5000 }) => {
  try {
    const response = await api.post('/narrative/places/nearby', {
      latitude,
      longitude,
      radius
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearby places:', error);
    throw error;
  }
};

export const searchPlacesByText = async ({ query, latitude = null, longitude = null }) => {
  try {
    const response = await api.post('/narrative/places/search', {
      query,
      latitude,
      longitude
    });
    return response.data;
  } catch (error) {
    console.error('Error searching places:', error);
    throw error;
  }
};

export const getPopularPlaces = async () => {
  try {
    const response = await api.get('/narrative/places/popular');
    return response.data;
  } catch (error) {
    console.error('Error fetching popular places:', error);
    throw error;
  }
};

export const getPlaceChatResponse = async ({ place_id, place_name, user_message, chat_history = [] }) => {
  try {
    const response = await api.post('/narrative/places/chat', {
      place_id,
      place_name,
      user_message,
      chat_history
    });
    return response.data;
  } catch (error) {
    console.error('Error in place chat:', error);
    throw error;
  }
};