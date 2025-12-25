import { Button } from '@/components/ui/button';
import { Sparkles, TrendingUp, MessageSquare, BarChart3 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Index() {
  const navigate = useNavigate();

  const features = [
    {
      icon: <TrendingUp className="h-5 w-5 text-teal-600" />,
      title: 'Smart Tracking',
    },
    {
      icon: <Sparkles className="h-5 w-5 text-teal-600" />,
      title: 'AI-Powered',
    },
    {
      icon: <BarChart3 className="h-5 w-5 text-teal-600" />,
      title: 'Real-Time',
    },
  ];

  return (
    <div className="h-screen bg-gradient-to-b from-teal-50 to-cyan-50 overflow-hidden flex flex-col">
      {/* Hero Section - Full screen centered */}
      <section className="flex-1 container mx-auto px-4 lg:px-8 flex items-center justify-center">
        <div className="max-w-2xl mx-auto text-center w-full">
          <div className="space-y-5 relative">
            {/* Animated background circles */}
            <div className="absolute top-0 left-1/4 w-48 h-48 bg-teal-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float-slow" />
            <div className="absolute bottom-0 right-1/4 w-48 h-48 bg-cyan-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float-fast" />

            {/* Logo with animations */}
            <div className="flex justify-center animate-fade-in relative z-10">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-teal-500 to-teal-600 rounded-3xl flex items-center justify-center shadow-2xl animate-scale-in">
                  <TrendingUp className="w-10 h-10 text-white" strokeWidth={2.5} />
                </div>
                <div className="absolute -top-1.5 -left-1.5 w-8 h-8 bg-teal-400 rounded-full flex items-center justify-center animate-float-slow shadow-lg">
                  <BarChart3 className="w-4 h-4 text-white" />
                </div>
                <div className="absolute -top-1.5 -right-1.5 w-8 h-8 bg-cyan-400 rounded-full flex items-center justify-center animate-float-fast shadow-lg">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-8 h-8 bg-teal-300 rounded-full flex items-center justify-center animate-float-slow shadow-lg">
                  <MessageSquare className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>

            {/* Title */}
            <div className="animate-fade-in-up relative z-10" style={{ animationDelay: '0.2s' }}>
              <h1 className="text-5xl md:text-6xl font-bold text-teal-600 mb-2.5">FinSense</h1>
              <p className="text-xl text-teal-600 font-medium mb-2.5">AI-Driven Finance for SMBs</p>
              <p className="text-base text-gray-600 max-w-xl mx-auto">
                Automated financial decisions with human oversight.
              </p>
            </div>

            {/* Features - Equal spacing */}
            <div className="flex justify-center items-start gap-16 animate-fade-in-up relative z-10 max-w-lg mx-auto" style={{ animationDelay: '0.3s' }}>
              {features.map((feature, index) => (
                <div key={index} className="flex flex-col items-center w-24">
                  <div className="w-14 h-14 bg-teal-100 rounded-2xl flex items-center justify-center mb-2 hover:bg-teal-200 transition-colors">
                    {feature.icon}
                  </div>
                  <p className="text-sm font-medium text-gray-700 text-center">{feature.title}</p>
                </div>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col gap-2.5 max-w-md mx-auto animate-fade-in-up relative z-10" style={{ animationDelay: '0.4s' }}>
              <Button
                size="lg"
                className="w-full text-base h-12 bg-teal-500 hover:bg-teal-600 transition-all duration-300 hover:scale-105 rounded-2xl shadow-xl hover:shadow-2xl"
                onClick={() => navigate('/signup')}
              >
                Get Started
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="w-full text-base h-12 border-2 bg-white hover:bg-gray-50 transition-all duration-300 hover:scale-105 rounded-2xl shadow-lg"
                onClick={() => navigate('/signin')}
              >
                Sign In
              </Button>
            </div>

            <p className="text-sm text-gray-600 animate-fade-in relative z-10 max-w-md mx-auto" style={{ animationDelay: '0.5s' }}>
              Join thousands of small business owners who save hours on bookkeeping
            </p>
          </div>
        </div>
      </section>

      {/* Footer - Minimal */}
      <footer className="py-2.5 bg-transparent">
        <div className="container mx-auto px-4 lg:px-8 text-center">
          <p className="text-sm text-gray-600">
            by <span className="text-teal-600 font-medium">Rakshita Jaiswal</span>
          </p>
        </div>
      </footer>
    </div>
  );
}