import { useState, useCallback, useEffect } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Building2, CreditCard, Shield, Clock, Check, ArrowRight, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useSubscription } from '@/contexts/subscription-context';
import { usePlaidLink } from 'react-plaid-link';
import { API_ENDPOINTS, apiRequest } from '@/lib/api';
import type { PlaidLinkToken, StripeAuthResponse } from '@/types';

export default function ConnectAccounts() {
  const navigate = useNavigate();
  const { hasAccess } = useSubscription();
  const [connecting, setConnecting] = useState<string | null>(null);
  const [selectedSource, setSelectedSource] = useState<string | null>(null);
  const [linkToken, setLinkToken] = useState<string | null>(null);
  const [isLoadingToken, setIsLoadingToken] = useState(false);

  const sources = [
    {
      id: 'square',
      name: 'Square POS',
      description: 'Connect your Square account to sync sales and payments',
      icon: CreditCard,
      color: 'bg-teal-500',
      recommended: true,
      features: [
        'Automatic transaction import',
        'Real-time sales data',
        '90 days of history',
        'Payment details included',
      ],
    },
    {
      id: 'stripe',
      name: 'Stripe',
      description: 'Connect your Stripe account for payment processing data',
      icon: Zap,
      color: 'bg-purple-500',
      recommended: false,
      features: [
        'Payment transactions sync',
        'Customer payment data',
        '90 days of history',
        'Subscription tracking',
      ],
    },
    {
      id: 'bank',
      name: 'Bank Account',
      description: 'Connect your business checking account',
      icon: Building2,
      color: 'bg-blue-500',
      recommended: false,
      features: [
        'All business transactions',
        'Balance tracking',
        '90 days of history',
        '12,000+ banks supported',
      ],
    },
  ];

  // Fetch Plaid link token when component mounts
  useEffect(() => {
    const fetchLinkToken = async () => {
      try {
        setIsLoadingToken(true);
        const response = await apiRequest<PlaidLinkToken>(
          API_ENDPOINTS.plaidCreateLinkToken,
          { method: 'POST' }
        );
        setLinkToken(response.link_token);
      } catch (error) {
        console.error('Error fetching link token:', error);
        // Don't show error toast - we'll handle mock mode in the connect handler
      } finally {
        setIsLoadingToken(false);
      }
    };

    fetchLinkToken();
  }, []);

  // Handle successful Plaid Link
  const onPlaidSuccess = useCallback(async (public_token: string, metadata: any) => {
    try {
      setConnecting('bank');
      
      // Exchange public token for access token
      await apiRequest(API_ENDPOINTS.plaidExchangeToken, {
        method: 'POST',
        body: JSON.stringify({ public_token }),
      });

      // Fetch transactions from Plaid
      const transactionsResponse = await apiRequest(
        API_ENDPOINTS.plaidTransactions,
        { method: 'GET' }
      );

      console.log('Plaid connection successful:', metadata);
      console.log('Transactions fetched:', transactionsResponse);

      setSelectedSource('bank');
      setConnecting(null);
      toast.success('Bank account connected successfully!');
    } catch (error) {
      console.error('Error exchanging token:', error);
      toast.error('Failed to complete bank connection');
      setConnecting(null);
    }
  }, []);

  // Handle Plaid Link exit
  const onPlaidExit = useCallback((error: any, metadata: any) => {
    console.log('Plaid Link exited:', error, metadata);
    setConnecting(null);
    
    if (error) {
      toast.error('Bank connection cancelled or failed');
    }
  }, []);

  // Initialize Plaid Link
  const { open: openPlaidLink, ready: plaidReady } = usePlaidLink({
    token: linkToken,
    onSuccess: onPlaidSuccess,
    onExit: onPlaidExit,
  });

  const handleConnect = async (id: string, name: string) => {
    if (id === 'bank') {
      // Use real Plaid Link (sandbox or production)
      if (!plaidReady || !linkToken) {
        toast.error('Bank connection not ready. Please try again.');
        return;
      }
      
      setConnecting(id);
      openPlaidLink();
    } else if (id === 'stripe') {
      // Use Stripe OAuth for Stripe connections
      try {
        setConnecting(id);
        
        // Get Stripe authorization URL
        const response = await apiRequest<StripeAuthResponse>(
          API_ENDPOINTS.stripeAuthorize,
          { method: 'GET' }
        );
        
        // Redirect to Stripe OAuth
        window.location.href = response.authorization_url;
      } catch (error) {
        console.error('Error initiating Stripe connection:', error);
        toast.error('Failed to connect to Stripe');
        setConnecting(null);
      }
    } else {
      // Simulate connection for other sources (Square)
      setConnecting(id);
      await new Promise(resolve => setTimeout(resolve, 2000));
      setSelectedSource(id);
      setConnecting(null);
      toast.success(`${name} connected successfully! (Using sample data)`);
    }
  };

  const handleContinue = () => {
    if (!selectedSource) {
      toast.error('Please connect an account to continue');
      return;
    }
    navigate('/sync-progress');
  };

  // Check for Stripe OAuth callback
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const stripeStatus = params.get('stripe');
    const stripeMessage = params.get('message');

    if (stripeStatus === 'mock') {
      // Handle mock Stripe connection - just mark as connected
      setSelectedSource('stripe');
      toast.success('Stripe account connected successfully! (Using sample data)');
      // Clean up URL
      window.history.replaceState({}, '', '/connect-accounts');
    } else if (stripeStatus === 'success') {
      setSelectedSource('stripe');
      toast.success('Stripe account connected successfully!');
      // Clean up URL
      window.history.replaceState({}, '', '/connect-accounts');
    } else if (stripeStatus === 'error') {
      toast.error(`Stripe connection failed: ${stripeMessage || 'Unknown error'}`);
      // Clean up URL
      window.history.replaceState({}, '', '/connect-accounts');
    }
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-6">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-6 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Connect Your Account</h1>
            <p className="text-base text-gray-600 mb-1">
              Choose one source to get started. We'll sync your transactions in under 60 seconds.
            </p>
            <div className="flex items-center justify-center gap-4 text-xs text-gray-600 mt-3">
              <div className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-teal-600" />
                <span>Bank-level encryption</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-teal-600" />
                <span>Syncs in 45 seconds</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="h-5 w-5 text-teal-600" />
                <span>Read-only access</span>
              </div>
            </div>
          </div>

          {/* Source Selection Cards */}
          <div className="grid md:grid-cols-3 gap-5 mb-6">
            {sources.map((source, index) => {
              const isSelected = selectedSource === source.id;
              const isConnecting = connecting === source.id;
              const Icon = source.icon;

              return (
                <Card 
                  key={source.id}
                  className={`relative overflow-hidden transition-all duration-300 hover:shadow-xl animate-fade-in-up ${
                    isSelected ? 'border-2 border-teal-500 shadow-lg' : ''
                  }`}
                  style={{ animationDelay: `${0.1 * index}s` }}
                >
                  {source.recommended && (
                    <div className="absolute top-4 right-4">
                      <div className="bg-teal-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                        RECOMMENDED
                      </div>
                    </div>
                  )}
                  
                  <CardHeader className="pb-4">
                    <div className="flex items-start gap-3">
                      <div className={`${source.color} p-3 rounded-xl`}>
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                      <div className="flex-1">
                        <CardTitle className="text-lg mb-1">{source.name}</CardTitle>
                        <p className="text-xs text-gray-600">{source.description}</p>
                      </div>
                    </div>
                  </CardHeader>

                  <CardContent className="pt-2">
                    {isSelected ? (
                      <div className="flex items-center justify-between p-3 bg-teal-50 rounded-xl mb-3">
                        <div className="flex items-center gap-2">
                          <Check className="h-5 w-5 text-teal-600" />
                          <span className="font-medium text-teal-900">Connected</span>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setSelectedSource(null)}
                        >
                          Disconnect
                        </Button>
                      </div>
                    ) : (
                      <Button
                        className="w-full h-10 rounded-xl mb-3"
                        onClick={() => handleConnect(source.id, source.name)}
                        disabled={isConnecting || selectedSource !== null || (source.id === 'bank' && (!plaidReady || isLoadingToken))}
                      >
                        {isConnecting ? 'Connecting...' : 
                         source.id === 'bank' && isLoadingToken ? 'Loading...' :
                         'Connect Account'}
                      </Button>
                    )}

                    {/* Features */}
                    <div className="space-y-1.5">
                      {source.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-xs text-gray-600">
                          <Check className="h-3 w-3 text-teal-600 flex-shrink-0" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Security Notice */}
          <Card className="mb-6 bg-blue-50 border-blue-200 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <CardContent className="pt-5 pb-5">
              <div className="flex items-start gap-3">
                <Shield className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-blue-900 mb-1 text-sm">Your data is secure</h3>
                  <p className="text-xs text-blue-800 mb-2">
                    We use bank-level 256-bit encryption and never store your login credentials.
                    All connections are read-only. Bank connections are powered by Plaid.
                  </p>
                  <div className="flex items-center gap-3 text-[10px] text-blue-700">
                    <span>✓ SOC 2 Type II Certified</span>
                    <span>✓ GDPR Compliant</span>
                    <span>✓ PCI DSS Level 1</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Action Button */}
          <div className="flex justify-between items-center mb-20 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <p className="text-xs text-gray-500">
              You can connect additional sources later from Settings
            </p>
            <Button
              className="bg-teal-500 hover:bg-teal-600 rounded-xl px-6 h-10"
              onClick={handleContinue}
              disabled={!selectedSource}
            >
              Continue to Sync
              <ArrowRight className="h-5 w-5 ml-2" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}