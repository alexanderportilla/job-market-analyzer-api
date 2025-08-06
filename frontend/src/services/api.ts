const API_BASE_URL = 'http://127.0.0.1:8001';

export interface JobOffer {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
  scraped_at: string;
}

export interface TechnologyStat {
  technology: string;
  count: number;
  percentage: number;
}

export interface DashboardStats {
  total_offers: number;
  unique_companies: number;
  recent_offers: number;
  unique_technologies: number;
  monthly_trend: Array<{
    month: string;
    offers: number;
  }>;
  last_updated: string;
}

export interface RecentActivity {
  company: string;
  position: string;
  time: string;
  url: string;
}

export interface CompanyStat {
  company: string;
  offer_count: number;
}

export interface LocationStat {
  location: string;
  offer_count: number;
}

export interface SearchFilters {
  q?: string;
  company?: string;
  location?: string;
  technology?: string;
  min_salary?: number;
  max_salary?: number;
  job_type?: string;
  experience_level?: string;
  sort_by?: string;
  sort_order?: string;
}

export interface SearchResult {
  offers: JobOffer[];
  total: number;
  page: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface SalaryTrends {
  average_salaries: Record<string, Record<string, number>>;
  trends: Array<{
    month: string;
    avg_salary: number;
  }>;
}

export interface ExperienceAnalysis {
  total_offers: number;
  junior: { count: number; percentage: number };
  mid: { count: number; percentage: number };
  senior: { count: number; percentage: number };
}

export interface MarketInsights {
  market_growth: {
    current_month: number;
    previous_month: number;
    growth_rate: number;
    trend: string;
  };
  hot_technologies: Array<{
    technology: string;
    demand_score: number;
    trend: string;
  }>;
  market_sentiment: string;
  recommendations: string[];
}

export interface JobAlert {
  alert_id: string;
  email: string;
  keywords: string[];
  location?: string;
  company?: string;
  frequency: string;
  status: string;
  created_at: string;
  message: string;
}

export interface Notification {
  type: string;
  title: string;
  description: string;
  timestamp: string;
  priority: string;
}

export interface NotificationsResponse {
  notifications: Notification[];
  unread_count: number;
  last_updated: string;
}

export interface MarketReport {
  report_period: string;
  generated_at: string;
  summary: {
    total_offers: number;
    unique_companies: number;
    unique_locations: number;
    top_technologies: TechnologyStat[];
    top_companies: CompanyStat[];
    top_locations: LocationStat[];
  };
  insights: string[];
  recommendations: string[];
}

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      console.error(`API Error for ${url}:`, error);
      throw new Error(`Failed to connect to API at ${url}. Make sure the backend server is running.`);
    }
  }

  // Dashboard endpoints
  async getDashboardStats(): Promise<DashboardStats> {
    return this.request<DashboardStats>('/dashboard/stats/');
  }

  async getRecentActivity(): Promise<RecentActivity[]> {
    return this.request<RecentActivity[]>('/dashboard/recent-activity/');
  }

  // Job offers endpoints
  async getAllOffers(skip: number = 0, limit: number = 100): Promise<JobOffer[]> {
    return this.request<JobOffer[]>(`/offers/?skip=${skip}&limit=${limit}`);
  }

  async searchOffers(filters: SearchFilters, skip: number = 0, limit: number = 20): Promise<SearchResult> {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    return this.request<SearchResult>(`/offers/search/?${params.toString()}`);
  }

  // Technology statistics
  async getTechnologyStats(): Promise<TechnologyStat[]> {
    return this.request<TechnologyStat[]>('/stats/technologies/');
  }

  // Analytics endpoints
  async getCompanyStats(): Promise<CompanyStat[]> {
    return this.request<CompanyStat[]>('/analytics/company-stats/');
  }

  async getLocationStats(): Promise<LocationStat[]> {
    return this.request<LocationStat[]>('/analytics/location-stats/');
  }

  async getSalaryTrends(): Promise<SalaryTrends> {
    return this.request<SalaryTrends>('/analytics/salary-trends/');
  }

  async getExperienceAnalysis(): Promise<ExperienceAnalysis> {
    return this.request<ExperienceAnalysis>('/analytics/experience-analysis/');
  }

  async getMarketInsights(): Promise<MarketInsights> {
    return this.request<MarketInsights>('/analytics/market-insights/');
  }

  // Alerts endpoints
  async createJobAlert(
    email: string,
    keywords: string[],
    location?: string,
    company?: string,
    frequency: string = 'daily'
  ): Promise<JobAlert> {
    return this.request<JobAlert>('/alerts/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        keywords,
        location,
        company,
        frequency,
      }),
    });
  }

  async getAlertJobs(alertId: string): Promise<any> {
    return this.request(`/alerts/${alertId}/jobs/`);
  }

  // Notifications endpoints
  async getRecentNotifications(): Promise<NotificationsResponse> {
    return this.request<NotificationsResponse>('/notifications/recent/');
  }

  // Export endpoints
  async exportJobs(format: string = 'json', filters?: any): Promise<any> {
    const params = new URLSearchParams();
    params.append('format', format);
    
    if (filters) {
      params.append('filters', JSON.stringify(filters));
    }
    
    return this.request(`/export/jobs/?${params.toString()}`);
  }

  // Reports endpoints
  async generateMarketReport(period: string = '30d'): Promise<MarketReport> {
    return this.request<MarketReport>(`/reports/market-summary/?period=${period}`);
  }

  // Scraping endpoint
  async triggerScraping(pages: number = 1): Promise<any> {
    return this.request('/scrape/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pages }),
    });
  }

  // Health check
  async healthCheck(): Promise<any> {
    return this.request('/health/');
  }

  // Test endpoint
  async testConnection(): Promise<any> {
    return this.request('/test');
  }
}

export const apiService = new ApiService(); 