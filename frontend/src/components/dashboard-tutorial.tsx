import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { X, ArrowRight, ArrowLeft, Sparkles } from 'lucide-react';

interface TutorialStep {
  title: string;
  description: string;
  target: string;
  highlight?: boolean;
  position?: 'top' | 'bottom' | 'left' | 'center';
}

const tutorialSteps: TutorialStep[] = [
  {
    title: 'Welcome to FinSense! 🎉',
    description: "Let's take a quick 2-minute tour to show you how to save 12+ hours monthly on bookkeeping.",
    target: 'dashboard-header',
    position: 'center',
  },
  {
    title: 'Your Financial Overview',
    description: 'See your revenue, profit, expenses, and cash balance at a glance. All updated in real-time from your connected accounts.',
    target: 'dashboard-stats',
    highlight: true,
    position: 'bottom',
  },
  {
    title: 'Ask FinSense AI',
    description: 'Click here to chat with FinSense AI! Ask about profits, spending patterns, or get instant financial insights in plain English.',
    target: 'ask-ai-assistant',
    highlight: true,
    position: 'left',
  },
  {
    title: 'More Quick Actions',
    description: 'Upload receipts, generate reports, or export data - all in just a few clicks.',
    target: 'quick-actions',
    highlight: true,
    position: 'left',
  },
  {
    title: 'Review Transactions',
    description: 'Check transactions that need your attention. Most are auto-approved, but you can review and correct any that need it.',
    target: 'transactions-link',
    highlight: true,
    position: 'bottom',
  },
  {
    title: "You're All Set! 🚀",
    description: "That's it! Start exploring your dashboard. Remember, every correction you make teaches the AI to be even more accurate.",
    target: 'dashboard-header',
    position: 'center',
  },
];

interface DashboardTutorialProps {
  onComplete: () => void;
  onSkip: () => void;
}

export function DashboardTutorial({ onComplete, onSkip }: DashboardTutorialProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [modalPosition, setModalPosition] = useState({ top: '50%', left: '50%', transform: 'translate(-50%, -50%)' });

  const step = tutorialSteps[currentStep];

  // Handle highlighting and positioning when step changes
  useEffect(() => {
    const updateHighlightAndPosition = () => {
      // Remove all existing highlights
      document.querySelectorAll('.tutorial-highlight').forEach(el => {
        el.classList.remove('tutorial-highlight');
      });

      if (step.highlight) {
        const element = document.getElementById(step.target);
        
        if (element) {
          // First, scroll the element into view
          const viewportHeight = window.innerHeight;
          const rect = element.getBoundingClientRect();
          
          // Calculate scroll position to center element in viewport
          const elementTop = rect.top + window.pageYOffset;
          const elementHeight = rect.height;
          const scrollToPosition = elementTop - (viewportHeight / 2) + (elementHeight / 2);
          
          // Scroll immediately
          window.scrollTo({
            top: Math.max(0, scrollToPosition),
            behavior: 'smooth',
          });
          
          // Wait for scroll to complete, then add highlight and position modal
          setTimeout(() => {
            // Add highlight
            element.classList.add('tutorial-highlight');
            
            // Get fresh element position after scroll
            const newRect = element.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Calculate modal position
            let newPosition = { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' };
            
            if (step.position === 'bottom') {
              // Position modal below the highlighted element
              const topPosition = newRect.bottom + scrollTop + 30;
              
              newPosition = {
                top: `${topPosition}px`,
                left: '50%',
                transform: 'translateX(-50%)',
              };
              
            } else if (step.position === 'top') {
              // Position modal above the highlighted element
              const modalHeight = 400;
              const topPosition = newRect.top + scrollTop - modalHeight - 30;
              
              newPosition = {
                top: `${topPosition}px`,
                left: '50%',
                transform: 'translateX(-50%)',
              };
              
            } else if (step.position === 'left') {
              // Position modal to the left of the highlighted element
              const elementCenterY = newRect.top + scrollTop + (newRect.height / 2);
              const leftPosition = newRect.left - 600; // 550px modal width + 50px gap
              
              newPosition = {
                top: `${elementCenterY}px`,
                left: leftPosition > 50 ? `${leftPosition}px` : '50px',
                transform: 'translateY(-50%)',
              };
            }
            
            setModalPosition(newPosition);
          }, 800); // Wait 800ms for smooth scroll to complete
        } else {
          console.warn(`Tutorial: Element with id "${step.target}" not found`);
        }
      } else {
        // For non-highlighted steps (center position)
        setModalPosition({ top: '50%', left: '50%', transform: 'translate(-50%, -50%)' });
        
        // Scroll to top for welcome/completion messages
        window.scrollTo({
          top: 0,
          behavior: 'smooth',
        });
      }
    };

    // Delay to ensure DOM is ready
    const timer = setTimeout(updateHighlightAndPosition, 200);

    return () => {
      clearTimeout(timer);
      // Remove all highlights on cleanup
      document.querySelectorAll('.tutorial-highlight').forEach(el => {
        el.classList.remove('tutorial-highlight');
      });
    };
  }, [currentStep, step]);

  const handleNext = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/60 z-40 animate-fade-in" />

      {/* Tutorial Card - Absolute Position (moves with scroll) */}
      <div 
        className="absolute z-50 p-4 pointer-events-none transition-all duration-700 ease-in-out"
        style={{
          top: modalPosition.top,
          left: modalPosition.left,
          transform: modalPosition.transform,
          maxWidth: '90vw',
          width: '550px',
        }}
      >
        <Card className="shadow-2xl pointer-events-auto animate-scale-in">
          <CardContent className="pt-6">
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-teal-600" />
                <span className="text-sm font-medium text-gray-600">
                  Step {currentStep + 1} of {tutorialSteps.length}
                </span>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={onSkip}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* Content */}
            <h3 className="text-2xl font-bold text-gray-900 mb-3">{step.title}</h3>
            <p className="text-gray-600 mb-6 text-base leading-relaxed">{step.description}</p>

            {/* Progress Dots */}
            <div className="flex items-center justify-center gap-2 mb-6">
              {tutorialSteps.map((_, index) => (
                <div
                  key={index}
                  className={`h-2 rounded-full transition-all ${
                    index === currentStep
                      ? 'w-8 bg-teal-500'
                      : index < currentStep
                      ? 'w-2 bg-teal-300'
                      : 'w-2 bg-gray-300'
                  }`}
                />
              ))}
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between">
              <Button
                variant="ghost"
                onClick={handlePrevious}
                disabled={currentStep === 0}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>
              <Button
                className="bg-teal-500 hover:bg-teal-600"
                onClick={handleNext}
              >
                {currentStep === tutorialSteps.length - 1 ? 'Finish' : 'Next'}
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </div>

            {/* Skip Link */}
            <button
              onClick={onSkip}
              className="w-full text-center text-sm text-gray-500 hover:text-gray-700 mt-3"
            >
              Skip tutorial
            </button>
          </CardContent>
        </Card>
      </div>

      {/* Tutorial Highlight Styles */}
      <style>{`
        .tutorial-highlight {
          position: relative;
          z-index: 45 !important;
          box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.8), 0 0 0 8px rgba(20, 184, 166, 0.4) !important;
          border-radius: 12px;
          animation: pulse-highlight 2s ease-in-out infinite;
        }

        @keyframes pulse-highlight {
          0%, 100% {
            box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.8), 0 0 0 8px rgba(20, 184, 166, 0.4) !important;
          }
          50% {
            box-shadow: 0 0 0 6px rgba(20, 184, 166, 0.9), 0 0 0 12px rgba(20, 184, 166, 0.5) !important;
          }
        }
      `}</style>
    </>
  );
}