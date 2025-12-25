/**
 * API configuration and utilities
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  // Auth endpoints
  signup: `${API_BASE_URL}/api/v1/auth/signup`,
  login: `${API_BASE_URL}/api/v1/auth/login`,
  logout: `${API_BASE_URL}/api/v1/auth/logout`,
  me: `${API_BASE_URL}/api/v1/auth/me`,
  updateProfile: `${API_BASE_URL}/api/v1/auth/profile`,
  deleteAccount: `${API_BASE_URL}/api/v1/auth/account`,
  
  // Subscription endpoints
  subscriptionStatus: `${API_BASE_URL}/api/v1/subscription/status`,
  startTrial: `${API_BASE_URL}/api/v1/subscription/start-trial`,
  
  // Plaid endpoints
  plaidCreateLinkToken: `${API_BASE_URL}/api/plaid/create_link_token`,
  plaidExchangeToken: `${API_BASE_URL}/api/plaid/exchange_public_token`,
  plaidTransactions: `${API_BASE_URL}/api/plaid/transactions`,
  
  // Stripe endpoints
  stripeAuthorize: `${API_BASE_URL}/api/stripe/authorize`,
  stripeAccount: `${API_BASE_URL}/api/stripe/account`,
  stripeCharges: `${API_BASE_URL}/api/stripe/charges`,
  stripePaymentIntents: `${API_BASE_URL}/api/stripe/payment-intents`,
  stripeDisconnect: `${API_BASE_URL}/api/stripe/disconnect`,
  
  // AI Chat endpoints
  aiChatConversations: `${API_BASE_URL}/api/v1/ai-chat/conversations`,
  aiChatQuickQuery: `${API_BASE_URL}/api/v1/ai-chat/quick-query`,
  aiChatSamplePrompts: `${API_BASE_URL}/api/v1/ai-chat/sample-prompts`,
  aiChatCacheStats: `${API_BASE_URL}/api/v1/ai-chat/cache-stats`,
} as const;

/**
 * Get authorization header with JWT token
 */
export function getAuthHeader(): Record<string, string> {
  const token = localStorage.getItem('finsense_token');
  if (!token) {
    return {};
  }
  return {
    'Authorization': `Bearer ${token}`,
  };
}

/**
 * Make an authenticated API request
 */
export async function apiRequest<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const headers = {
    'Content-Type': 'application/json',
    ...getAuthHeader(),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}