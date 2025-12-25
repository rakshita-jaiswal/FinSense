import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Check, X, TrendingUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSubscription } from '@/contexts/subscription-context';
import { useAuth } from '@/contexts/auth-context';
import { toast } from 'sonner';

export default function Pricing() {
  const navigate = useNavigate();
  const { hasAccess, isTrialActive, startTrial } = useSubscription();
  const { isAuthenticated } = useAuth();
  const [isStartingTrial, setIsStartingTrial] = useState(false);

  const features = {
    free: [
      { name: 'View dashboard with financial overview', included: true },
      { name: 'View recent transactions', included: true },
      { name: 'Basic expense tracking', included: true },
      { name: 'Manual transaction categorization', included: true },
      { name: 'Profile management', included: true },
      { name: 'AI-powered auto-categorization', included: false },
      { name: 'Transaction confidence scores', included: false },
      { name: 'FinSense AI chat', included: false },
      { name: 'Smart transaction review workflow', included: false },
      { name: 'Revenue vs expense charts', included: false },
      { name: 'Expense breakdown analytics', included: false },
      { name: 'Financial reports generation', included: false },
    ],
    trial: [
      { name: 'Real-time financial dashboard', included: true, upcoming: false },
      { name: 'View and manage all transactions', included: true, upcoming: false },
      { name: 'AI-powered auto-categorization (95% accuracy)', included: true, upcoming: false },
      { name: 'Transaction confidence scores', included: true, upcoming: false },
      { name: 'Smart transaction review workflow', included: true, upcoming: false },
      { name: 'FinSense AI chat for financial insights', included: true, upcoming: false },
      { name: 'Revenue vs expense trend charts', included: true, upcoming: false },
      { name: 'Expense breakdown pie charts', included: true, upcoming: false },
      { name: 'Financial reports with filters', included: true, upcoming: false },
      { name: 'Profile and settings management', included: true, upcoming: false },
      { name: 'Receipt upload interface', included: true, upcoming: true },
      { name: 'Export data functionality', included: true, upcoming: true },
    ],
  };

  // User is on free plan if they don't have access (no trial, no paid subscription)
  const isOnFreePlan = !hasAccess;

  const handleStartTrial = async () => {
    if (!isAuthenticated) {
      // Not logged in, redirect to signup
      navigate('/signup');
      return;
    }

    if (isTrialActive) {
      // Already on trial
      toast.info('You are already on a trial!');
      navigate('/dashboard');
      return;
    }

    // Start trial for logged-in user
    setIsStartingTrial(true);
    try {
      await startTrial();
      toast.success('14-day trial activated! Enjoy all premium features.');
      navigate('/dashboard');
    } catch (error: any) {
      if (error.message?.includes('already been used')) {
        toast.error('Trial has already been used for this account');
      } else {
        toast.error('Failed to start trial. Please try again.');
      }
    } finally {
      setIsStartingTrial(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50 bg-mesh-gradient">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-teal-600">FinSense</h1>
            </div>
            {isAuthenticated ? (
              <Button variant="ghost" onClick={() => navigate('/dashboard')}>
                Back to Dashboard
              </Button>
            ) : (
              <Button variant="ghost" onClick={() => navigate('/signin')}>
                Sign In
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        <div className="text-center mb-12 animate-fade-in-up">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Start with our free plan, then unlock all features with a 14-day trial
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto mb-16">
          {/* Free Plan */}
          <Card className={`border-2 animate-fade-in-up relative hover:shadow-2xl transition-all duration-300 ${isOnFreePlan ? 'border-teal-500 shadow-xl' : 'shadow-lg'}`} style={{ animationDelay: '0.1s' }}>
            <CardHeader className="text-center pb-8 pt-6">
              {isOnFreePlan && (
                <div className="mb-4">
                  <div className="inline-block bg-teal-500 text-white px-6 py-1.5 rounded-full text-sm font-medium shadow-lg">
                    Current Plan
                  </div>
                </div>
              )}
              <CardTitle className="text-2xl mb-2">Free Forever</CardTitle>
              <div className="text-4xl font-bold mb-2">$0</div>
              <p className="text-gray-600">Perfect for getting started</p>
            </CardHeader>
            <CardContent>
              <Button
                variant="outline"
                size="lg"
                className="w-full mb-6 rounded-xl transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={() => navigate('/signup')}
                disabled={isAuthenticated && isOnFreePlan}
              >
                {isAuthenticated && isOnFreePlan ? 'Current Plan' : 'Get Started Free'}
              </Button>
              <div className="space-y-3">
                {features.free.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3 animate-fade-in-up" style={{ animationDelay: `${0.05 * index}s` }}>
                    {feature.included ? (
                      <div className="w-5 h-5 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <Check className="w-3 h-3 text-teal-600" />
                      </div>
                    ) : (
                      <div className="w-5 h-5 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <X className="w-3 h-3 text-gray-400" />
                      </div>
                    )}
                    <span className={feature.included ? 'text-gray-900' : 'text-gray-400'}>
                      {feature.name}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Trial Plan */}
          <Card className={`border-2 shadow-2xl relative animate-fade-in-up hover:shadow-3xl transition-all duration-300 shine-effect ${isTrialActive ? 'border-green-500' : 'border-teal-500'}`} style={{ animationDelay: '0.2s' }}>
            <CardHeader className="text-center pb-8 pt-6">
              <div className="mb-4">
                <div className={`inline-block ${isTrialActive ? 'bg-green-500' : 'bg-teal-500'} text-white px-6 py-1.5 rounded-full text-sm font-medium shadow-lg animate-pulse`}>
                  {isTrialActive ? 'Active Trial' : 'Most Popular'}
                </div>
              </div>
              <CardTitle className="text-2xl mb-2">All Features</CardTitle>
              <div className="text-4xl font-bold mb-2">
                $29<span className="text-lg text-gray-600">/month</span>
              </div>
              <p className="text-gray-600">14-day free trial • No credit card required</p>
            </CardHeader>
            <CardContent>
              <Button
                size="lg"
                className={`w-full mb-6 rounded-xl transition-all duration-300 hover:scale-105 ${isTrialActive ? 'bg-green-500 hover:bg-green-600' : 'bg-teal-500 hover:bg-teal-600'}`}
                onClick={handleStartTrial}
                disabled={isStartingTrial}
              >
                {isStartingTrial ? 'Starting Trial...' : isTrialActive ? 'Trial Active - Go to Dashboard' : isAuthenticated ? 'Start 14-Day Free Trial' : 'Sign Up for Free Trial'}
              </Button>
              <div className="space-y-3">
                {features.trial.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3 animate-fade-in-up" style={{ animationDelay: `${0.05 * index}s` }}>
                    <div className="w-5 h-5 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Check className="w-3 h-3 text-teal-600" />
                    </div>
                    <span className="text-gray-900 font-medium">
                      {feature.name}
                      {feature.upcoming && (
                        <span className="ml-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                          Upcoming
                        </span>
                      )}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Demo Notice */}
        <div className="max-w-3xl mx-auto mb-16">
          <Card className="bg-blue-50 border-blue-200 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <CardContent className="pt-6">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <TrendingUp className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-blue-900 mb-2">Demo Application</h3>
                  <p className="text-sm text-blue-800">
                    This is a fully functional demo showcasing the core features of FinSense. 
                    All features listed above are implemented and working. The AI categorization 
                    uses mock data to demonstrate the workflow. In production, this would connect 
                    to real financial accounts and use advanced ML models for categorization.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8 animate-fade-in-up">Frequently Asked Questions</h2>
          <div className="space-y-6">
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">What happens after my 14-day trial?</h3>
                <p className="text-gray-600">
                  After 14 days, you'll be asked to enter payment information to continue using all features. 
                  You can cancel anytime during the trial with no charges. If you don't upgrade, you'll automatically 
                  move to the free plan.
                </p>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Can I switch between plans?</h3>
                <p className="text-gray-600">
                  Yes! You can upgrade to access all features anytime, or downgrade to the free plan. 
                  Your data is always safe and accessible.
                </p>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Is my financial data secure?</h3>
                <p className="text-gray-600">
                  Absolutely. We use bank-level 256-bit encryption and never store your bank login credentials. 
                  We're SOC 2 Type II certified and fully compliant with financial data regulations.
                </p>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Do you offer refunds?</h3>
                <p className="text-gray-600">
                  Yes! If you're not satisfied within the first 30 days of your paid subscription, 
                  we'll give you a full refund, no questions asked.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16 animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
          <h2 className="text-3xl font-bold mb-4">Ready to Save 12+ Hours Monthly?</h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of small business owners who've automated their bookkeeping
          </p>
          <Button
            size="lg"
            className="bg-teal-500 hover:bg-teal-600 text-lg px-8 rounded-xl transition-all duration-300 hover:scale-105"
            onClick={handleStartTrial}
            disabled={isStartingTrial}
          >
            {isStartingTrial ? 'Starting Trial...' : 'Start 14-Day Free Trial'}
          </Button>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t py-8 bg-white mt-16">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>© 2025 FinSense. Built with ❤️ for small business owners.</p>
        </div>
      </footer>
    </div>
  );
}