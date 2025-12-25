import { useState, useEffect, useRef, useMemo } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Check, Loader2, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function SyncProgress() {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [transactionCount, setTransactionCount] = useState(0);
  const stepRefs = useRef<(HTMLDivElement | null)[]>([]);

  const steps = useMemo(() => [
    { label: 'Connecting to your accounts', impact: 'Establishes secure data pipeline', duration: 1000 },
    { label: 'Fetching transaction history', impact: 'Builds decision dataset', duration: 2000 },
    { label: 'Normalizing vendor names', impact: 'Improves decision accuracy', duration: 1500 },
    { label: 'Removing duplicates', impact: 'Prevents false positives', duration: 1000 },
    { label: 'AI categorizing transactions', impact: 'Generates confidence-scored decisions', duration: 2500 },
    { label: 'Finalizing your dashboard', impact: 'Prepares actionable insights', duration: 1000 },
  ], []);

  // Auto-scroll to current step
  useEffect(() => {
    if (stepRefs.current[currentStep]) {
      stepRefs.current[currentStep]?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [currentStep]);

  useEffect(() => {
    let stepIndex = 0;
    let progressValue = 0;

    const runStep = () => {
      if (stepIndex >= steps.length) {
        setProgress(100);
        setTimeout(() => navigate('/transaction-review'), 1000);
        return;
      }

      setCurrentStep(stepIndex);
      const step = steps[stepIndex];
      const increment = 100 / steps.length;
      const stepDuration = step.duration;
      const updateInterval = 50;
      const progressPerUpdate = increment / (stepDuration / updateInterval);

      const interval = setInterval(() => {
        progressValue += progressPerUpdate;
        setProgress(Math.min(progressValue, (stepIndex + 1) * increment));

        // Simulate transaction counting
        if (stepIndex === 1) {
          setTransactionCount(prev => Math.min(prev + 23, 487));
        }
      }, updateInterval);

      setTimeout(() => {
        clearInterval(interval);
        stepIndex++;
        runStep();
      }, stepDuration);
    };

    runStep();
  }, [navigate, steps]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-16">
        <div className="max-w-2xl mx-auto">
          <Card className="animate-fade-in-up">
            <CardContent className="pt-12 pb-12">
              {/* Icon */}
              <div className="flex justify-center mb-8">
                <div className="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center animate-pulse">
                  <Sparkles className="h-10 w-10 text-teal-600" />
                </div>
              </div>

              {/* Title */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-3">
                  Syncing Your Financial Data
                </h1>
                <p className="text-gray-600">
                  This usually takes 45-60 seconds. We're importing your transaction history and preparing your dashboard.
                </p>
              </div>

              {/* Progress Bar */}
              <div className="mb-8">
                <Progress value={progress} className="h-3" />
                <p className="text-center text-sm text-gray-600 mt-2">
                  {Math.round(progress)}% complete
                </p>
              </div>

              {/* Transaction Counter */}
              {transactionCount > 0 && (
                <div className="text-center mb-8 animate-fade-in">
                  <p className="text-4xl font-bold text-teal-600 mb-2">
                    {transactionCount}
                  </p>
                  <p className="text-sm text-gray-600">transactions imported</p>
                </div>
              )}

              {/* Steps */}
              <div className="space-y-4 max-h-[400px] overflow-y-auto scrollbar-hide">
                {steps.map((step, index) => {
                  const isComplete = index < currentStep;
                  const isCurrent = index === currentStep;

                  return (
                    <div
                      key={index}
                      ref={(el) => (stepRefs.current[index] = el)}
                      className={`flex items-center gap-3 p-4 rounded-xl transition-all duration-500 ${
                        isCurrent ? 'bg-teal-50 scale-105 shadow-md' : isComplete ? 'bg-gray-50' : 'bg-white'
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-300 ${
                        isComplete ? 'bg-teal-500' : isCurrent ? 'bg-teal-100' : 'bg-gray-200'
                      }`}>
                        {isComplete ? (
                          <Check className="h-5 w-5 text-white" />
                        ) : isCurrent ? (
                          <Loader2 className="h-5 w-5 text-teal-600 animate-spin" />
                        ) : (
                          <span className="text-sm text-gray-500">{index + 1}</span>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className={`font-medium transition-colors duration-300 ${
                          isCurrent ? 'text-teal-900' : isComplete ? 'text-gray-700' : 'text-gray-400'
                        }`}>
                          {step.label}
                        </div>
                        <div className={`text-xs transition-colors duration-300 mt-0.5 ${
                          isCurrent ? 'text-teal-700' : isComplete ? 'text-gray-500' : 'text-gray-400'
                        }`}>
                          {step.impact}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Info Box */}
              <div className="mt-8 p-4 bg-blue-50 rounded-xl">
                <p className="text-sm text-blue-900 text-center">
                  <strong>Did you know?</strong> Our AI will automatically categorize 95% of your transactions 
                  with high confidence, saving you hours of manual work.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Custom scrollbar hide styles */}
      <style>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
        .scrollbar-hide {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
}