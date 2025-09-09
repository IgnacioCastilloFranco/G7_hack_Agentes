const API_BASE_URL = 'http://localhost:8000/ratoncito';

export interface SiteInfo {
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  description: string;
  rating?: number;
  photo_url?: string;
  place_id?: string;
  distance?: number;
  types?: string[];
}

export interface SitesResponse {
  sites: SiteInfo[];
  success: boolean;
  message?: string;
}

export interface LocationRequest {
  latitude: number;
  longitude: number;
  radius?: number;
}

export interface SiteSearchRequest {
  query: string;
  location?: string;
}

class ApiService {
  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(url, mergedOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getNearBySites(request: LocationRequest): Promise<SitesResponse> {
    return this.makeRequest<SitesResponse>('/sites/nearby', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async getNearbyPlaces(latitude: number, longitude: number, radius: number = 5000): Promise<SiteInfo[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/sites/nearby`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude,
          longitude,
          radius
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.message || 'Error fetching nearby places');
      }

      return data.sites || [];
    } catch (error) {
      console.error('Error in getNearbyPlaces:', error);
      throw error;
    }
  }

  async searchSites(request: SiteSearchRequest): Promise<SitesResponse> {
    return this.makeRequest<SitesResponse>('/sites/search', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async chatWithReactAgent(message: string, location?: string, context?: object): Promise<object> {
    return this.makeRequest('/chat/react', {
      method: 'POST',
      body: JSON.stringify({ message, location, context })
    });
  }

  async chatWithSimpleAgent(message: string, location?: string): Promise<object> {
    return this.makeRequest('/chat/simple', {
      method: 'POST',
      body: JSON.stringify({ message, location })
    });
  }

  async compareAgents(message: string, location?: string): Promise<object> {
    return this.makeRequest('/chat/compare', {
      method: 'POST',
      body: JSON.stringify({ message, location })
    });
  }
}

export const apiService = new ApiService();