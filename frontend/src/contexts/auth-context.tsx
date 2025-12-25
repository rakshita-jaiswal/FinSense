import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_ENDPOINTS, apiRequest } from '@/lib/api';

interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  businessName: string;
  phone?: string;
  industry?: string;
  employees?: number;
  monthlyRevenue?: number;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  updateProfile: (updates: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Load user from backend on mount if token exists
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('finsense_token');
      if (token) {
        try {
          const response = await apiRequest<{ user: any }>(API_ENDPOINTS.me);
          const userData: User = {
            id: response.user.id,
            email: response.user.email,
            firstName: response.user.first_name,
            lastName: response.user.last_name,
            businessName: response.user.business_name,
            phone: response.user.phone,
            industry: response.user.industry,
            employees: response.user.employees,
            monthlyRevenue: response.user.monthly_revenue,
          };
          setUser(userData);
        } catch (error) {
          console.error('Failed to load user:', error);
          localStorage.removeItem('finsense_token');
        }
      }
      setIsLoading(false);
    };
    
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiRequest<{ access_token: string; user: any }>(
        API_ENDPOINTS.login,
        {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        }
      );
      
      // Store token
      localStorage.setItem('finsense_token', response.access_token);
      
      // Set user data
      const userData: User = {
        id: response.user.id,
        email: response.user.email,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        businessName: response.user.business_name,
        phone: response.user.phone,
        industry: response.user.industry,
        employees: response.user.employees,
        monthlyRevenue: response.user.monthly_revenue,
      };
      setUser(userData);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiRequest(API_ENDPOINTS.logout, { method: 'POST' });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setUser(null);
      localStorage.removeItem('finsense_token');
      localStorage.removeItem('finsense_trial_active');
      navigate('/signin');
    }
  };

  const updateProfile = async (updates: Partial<User>) => {
    if (!user) return;
    
    try {
      // Convert camelCase to snake_case for API
      const apiUpdates: any = {};
      if (updates.firstName !== undefined) apiUpdates.first_name = updates.firstName;
      if (updates.lastName !== undefined) apiUpdates.last_name = updates.lastName;
      if (updates.businessName !== undefined) apiUpdates.business_name = updates.businessName;
      if (updates.phone !== undefined) apiUpdates.phone = updates.phone;
      if (updates.industry !== undefined) apiUpdates.industry = updates.industry;
      if (updates.employees !== undefined) apiUpdates.employees = updates.employees;
      if (updates.monthlyRevenue !== undefined) apiUpdates.monthly_revenue = updates.monthlyRevenue;
      
      const response = await apiRequest<{ user: any }>(
        API_ENDPOINTS.updateProfile,
        {
          method: 'PUT',
          body: JSON.stringify(apiUpdates),
        }
      );
      
      const updatedUser: User = {
        id: response.user.id,
        email: response.user.email,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        businessName: response.user.business_name,
        phone: response.user.phone,
        industry: response.user.industry,
        employees: response.user.employees,
        monthlyRevenue: response.user.monthly_revenue,
      };
      setUser(updatedUser);
    } catch (error) {
      console.error('Profile update failed:', error);
      throw error;
    }
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, isLoading, login, logout, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}