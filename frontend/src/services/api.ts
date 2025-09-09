const API_BASE_URL = 'http://localhost:8000/ratoncito';

export interface Site {
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  description?: string;
  rating?: number;
  photo_url?: string;
  place_id?: string;
}

export interface SitesResponse {
  sites: Site[];
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

export type { Site };

class ApiService {
  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
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
      body: JSON.stringify(request),
    });
  }

  async searchSites(request: SiteSearchRequest): Promise<SitesResponse> {
    return this.makeRequest<SitesResponse>('/sites/search', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async chatWithReactAgent(message: string, location?: string, context?: any): Promise<any> {
    return this.makeRequest('/chat/react', {
      method: 'POST',
      body: JSON.stringify({
        message,
        location,
        context,
      }),
    });
  }

  async chatWithSimpleAgent(message: string, location?: string): Promise<any> {
    return this.makeRequest('/chat/simple', {
      method: 'POST',
      body: JSON.stringify({
        message,
        location,
      }),
    });
  }

  async compareAgents(message: string, location?: string): Promise<any> {
    const params = new URLSearchParams({ message });
    if (location) {
      params.append('location', location);
    }
    
    return this.makeRequest(`/compare?${params.toString()}`);
  }
}

export const apiService = new ApiService();