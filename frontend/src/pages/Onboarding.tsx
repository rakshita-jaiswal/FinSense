import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ThumbsUp, BarChart3, ClipboardList, Camera, MessageSquare } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const steps = [
  {
    icon: ThumbsUp,
    title: 'Welcome to FinSense!',
    description: "Let's take a quick tour of your\nnew AI-powered finance assistant",
  },
  {
    icon: BarChart3,
    title: 'Real-time Dashboard',
    description: 'Track your revenue, profit, and expenses in real-time.\nYour AI assistant automatically categorizes transactions.',
  },
  {
    icon: ClipboardList,
    title: 'Smart Transaction List',
    description: 'All your transactions auto-categorized with AI.\nReview, edit, and approve with confidence scores.',
  },
  {
    icon: Camera,
    title: 'Receipt Upload',
    description: 'Simply snap a photo or drop receipts.\nOur AI extracts all details automatically.',
  },
  {
    icon: MessageSquare,
    title: 'Ask FinSense Anything',
    description: 'Chat with your AI assistant using natural language.\nAsk about profits, trends, or get tax-ready reports.',
  },
];

export default function Onboarding() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentStep(currentStep + 1);
        setIsTransitioning(false);
      }, 300);
    } else {
      navigate('/connect-accounts');
    }
  };

  const handleSkip = () => {
    navigate('/connect-accounts');
  };

  const CurrentIcon = steps[currentStep].icon;

  return (
    <div className="h-screen overflow-hidden bg-gradient-to-b from-teal-50 to-cyan-50 flex flex-col">
      {/* Progress Bar - Fixed at top */}
      <div className="flex-shrink-0 px-4 pt-6 pb-4 animate-fade-in">
        <div className="max-w-3xl mx-auto">
          <div className="h-2 bg-white rounded-full overflow-hidden shadow-sm">
            <div
              className="h-full bg-teal-500 transition-all duration-500 ease-out"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            />
          </div>
          <p className="text-center text-sm text-gray-600 mt-2">
            Step {currentStep + 1} of {steps.length}
          </p>
        </div>
      </div>

      {/* Content Card - Centered and scrollable if needed */}
      <div className="flex-1 flex items-center justify-center px-4 pb-8 overflow-y-auto">
        <div className={`w-full max-w-3xl bg-white rounded-3xl shadow-xl p-8 md:p-12 transition-all duration-300 ${
          isTransitioning ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
        }`}>
          <div className="text-center space-y-6">
            {/* Icon */}
            <div className="flex justify-center animate-fade-in-up">
              <div className="w-24 h-24 bg-teal-100 rounded-3xl flex items-center justify-center transition-all duration-500 hover:scale-110 hover:rotate-6 animate-bounce-slow">
                <CurrentIcon className="w-12 h-12 text-teal-600 animate-pulse-slow" strokeWidth={2} />
              </div>
            </div>

            {/* Title */}
            <h2 className="text-3xl font-bold text-gray-900 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              {steps[currentStep].title}
            </h2>

            {/* Description */}
            <p className="text-lg text-gray-600 whitespace-pre-line max-w-xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              {steps[currentStep].description}
            </p>

            {/* Placeholder Visual */}
            <div className="py-8 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              {currentStep === 0 && (
                <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
                  {[1, 2, 3, 4].map((i) => (
                    <div 
                      key={i} 
                      className="h-16 bg-gradient-to-br from-teal-100 to-teal-50 rounded-xl animate-fade-in-up shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105" 
                      style={{ animationDelay: `${0.1 * i}s` }}
                    />
                  ))}
                </div>
              )}
              {currentStep === 1 && (
                <div className="max-w-md mx-auto space-y-3">
                  {[1, 2, 3, 4].map((i) => (
                    <div 
                      key={i} 
                      className="h-12 bg-gradient-to-r from-teal-100 to-teal-50 rounded-xl animate-slide-in-left shadow-sm hover:shadow-md transition-all duration-300 hover:translate-x-2" 
                      style={{ animationDelay: `${0.1 * i}s` }}
                    />
                  ))}
                </div>
              )}
              {currentStep === 2 && (
                <div className="max-w-md mx-auto space-y-3">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-3 animate-slide-in-right hover:bg-teal-50 p-3 rounded-xl transition-all duration-300" style={{ animationDelay: `${0.1 * i}s` }}>
                      <div className="w-10 h-10 bg-teal-100 rounded-full animate-pulse-slow" />
                      <div className="flex-1 space-y-2">
                        <div className="h-4 bg-gray-200 rounded w-3/4 animate-shimmer" />
                        <div className="h-3 bg-gray-100 rounded w-1/2" />
                      </div>
                      <div className="w-20 h-8 bg-teal-100 rounded-lg animate-pulse-slow" />
                    </div>
                  ))}
                </div>
              )}
              {currentStep === 3 && (
                <div className="max-w-sm mx-auto animate-scale-in">
                  <div className="border-2 border-dashed border-teal-300 rounded-2xl p-12 bg-teal-50/50 transition-all duration-300 hover:border-teal-500 hover:bg-teal-50 hover:scale-105 cursor-pointer">
                    <Camera className="w-12 h-12 text-teal-400 mx-auto animate-bounce" />
                  </div>
                </div>
              )}
              {currentStep === 4 && (
                <div className="max-w-md mx-auto space-y-3">
                  <div className="h-12 bg-teal-100 rounded-xl w-3/4 animate-slide-in-left" />
                  <div className="h-12 bg-gray-100 rounded-xl w-2/3 ml-auto animate-slide-in-right" style={{ animationDelay: '0.1s' }} />
                  <div className="h-12 bg-teal-100 rounded-xl w-4/5 animate-slide-in-left" style={{ animationDelay: '0.2s' }} />
                </div>
              )}
            </div>

            {/* Buttons */}
            <div className="flex gap-4 justify-center pt-4 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <Button
                variant="outline"
                size="lg"
                onClick={handleSkip}
                className="px-8 rounded-xl border-2 transition-all duration-300 hover:scale-105 hover:border-teal-500"
              >
                Skip Tour
              </Button>
              <Button
                size="lg"
                onClick={handleNext}
                className="px-8 bg-teal-500 hover:bg-teal-600 rounded-xl transition-all duration-300 hover:scale-105 shadow-lg hover:shadow-xl"
              >
                {currentStep === steps.length - 1 ? 'Get Started' : 'Next'}
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Step Indicators - Fixed at bottom */}
      <div className="flex-shrink-0 pb-6 animate-fade-in" style={{ animationDelay: '0.5s' }}>
        <div className="flex justify-center gap-2">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`h-2 rounded-full transition-all duration-300 ${
                index === currentStep
                  ? 'w-8 bg-teal-500'
                  : index < currentStep
                  ? 'w-2 bg-teal-300'
                  : 'w-2 bg-gray-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}