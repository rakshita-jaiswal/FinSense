import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Lock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface FeatureLockOverlayProps {
  title: string;
  description: string;
  features: string[];
}

export function FeatureLockOverlay({ title, description, features }: FeatureLockOverlayProps) {
  const navigate = useNavigate();

  return (
    <div className="absolute inset-0 flex items-center justify-center z-10 bg-background/80 backdrop-blur-sm">
      <Card className="max-w-md w-full mx-4 shadow-2xl border-2 border-teal-500">
        <CardContent className="pt-6 text-center">
          <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Lock className="w-8 h-8 text-teal-600" />
          </div>
          <h3 className="text-xl font-bold mb-2">{title}</h3>
          <p className="text-muted-foreground mb-6">{description}</p>
          
          <div className="space-y-2 mb-6 text-left">
            {features.map((feature, index) => (
              <div key={index} className="flex items-start gap-3">
                <div className="w-5 h-5 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-teal-600 text-xs">✓</span>
                </div>
                <p className="text-sm">{feature}</p>
              </div>
            ))}
          </div>

          <Button
            size="lg"
            className="w-full bg-teal-500 hover:bg-teal-600 rounded-xl mb-3"
            onClick={() => navigate('/pricing')}
          >
            Upgrade to Premium
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="w-full rounded-xl"
            onClick={() => navigate('/dashboard')}
          >
            Back to Dashboard
          </Button>
          <p className="text-xs text-muted-foreground mt-3">
            $29/month • Cancel anytime
          </p>
        </CardContent>
      </Card>
    </div>
  );
}