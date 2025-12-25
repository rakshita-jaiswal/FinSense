import React, { createContext, useContext, useState, useEffect } from 'react';
import { API_ENDPOINTS, apiRequest } from '@/lib/api';
import { useAuth } from './auth-context';

interface SubscriptionStatus {
  hasAccess: boolean;
  isTrialActive: boolean;
  trialEndsAt: string | null;
  plan: string;
}

interface SubscriptionContextType {
  hasAccess: boolean;
  isTrialActive: boolean;
  trialEndsAt: string | null;
  plan: string;
  loading: boolean;
  startTrial: () => Promise<void>;
  refreshStatus: () => Promise<void>;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export function SubscriptionProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [status, setStatus] = useState<SubscriptionStatus>({
    hasAccess: false, // Default to false for free plan (no premium access)
    isTrialActive: false,
    trialEndsAt: null,
    plan: 'free',
  });
  const [loading, setLoading] = useState(false);

  // Fetch subscription status when user is authenticated
  const fetchStatus = async () => {
    if (!user) {
      // Reset to default when logged out
      setStatus({
        hasAccess: false,
        isTrialActive: false,
        trialEndsAt: null,
        plan: 'free',
      });
      return;
    }

    try {
      setLoading(true);
      const data = await apiRequest<SubscriptionStatus>(
        API_ENDPOINTS.subscriptionStatus
      );
      setStatus(data);
    } catch (error) {
      console.error('Failed to fetch subscription status:', error);
      // Default to free plan on error
      setStatus({
        hasAccess: false,
        isTrialActive: false,
        trialEndsAt: null,
        plan: 'free',
      });
    } finally {
      setLoading(false);
    }
  };

  // Fetch status on mount and when user changes
  useEffect(() => {
    fetchStatus();
  }, [user]);

  const startTrial = async () => {
    try {
      setLoading(true);
      await apiRequest<{ message: string; trialEndsAt: string }>(
        API_ENDPOINTS.startTrial,
        {
          method: 'POST',
        }
      );
      
      // Refresh status after starting trial
      await fetchStatus();
    } catch (error) {
      console.error('Failed to start trial:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const refreshStatus = async () => {
    await fetchStatus();
  };

  return (
    <SubscriptionContext.Provider
      value={{
        hasAccess: status.hasAccess,
        isTrialActive: status.isTrialActive,
        trialEndsAt: status.trialEndsAt,
        plan: status.plan,
        loading,
        startTrial,
        refreshStatus,
      }}
    >
      {children}
    </SubscriptionContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useSubscription() {
  const context = useContext(SubscriptionContext);
  if (context === undefined) {
    throw new Error('useSubscription must be used within a SubscriptionProvider');
  }
  return context;
}