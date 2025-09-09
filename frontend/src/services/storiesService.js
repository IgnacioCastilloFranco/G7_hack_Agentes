import api from './api';

export const getLocationInfo = async (locationName) => {
  try {
    const response = await api.get(`/narrative/locations/${locationName}`);
    return response.data;
  } catch (error) {
    console.error('Error getting location info:', error);
    throw error;
  }
};

export const createStory = async (storyRequest) => {
  try {
    const response = await api.post('/narrative/stories', storyRequest);
    return response.data;
  } catch (error) {
    console.error('Error creating story:', error);
    throw error;
  }
};

export const getLocationLegends = async (locationName) => {
  try {
    const response = await api.get(`/narrative/legends/${locationName}`);
    return response.data;
  } catch (error) {
    console.error('Error getting legends:', error);
    throw error;
  }
};