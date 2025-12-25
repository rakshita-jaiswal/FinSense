import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';

interface Indicator {
  icon: LucideIcon;
  value: string;
  label: string;
  sublabel: string;
  color: string;
  bgColor: string;
}

interface KeyIndicatorsProps {
  indicators: Indicator[];
}

export function KeyIndicators({ indicators }: KeyIndicatorsProps) {
  return (
    <Card className="mb-8 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
      <CardHeader>
        <CardTitle>Key Indicators</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {indicators.map((indicator, index) => (
            <div key={index} className={`${indicator.bgColor} rounded-xl p-6`}>
              <indicator.icon className={`h-8 w-8 ${indicator.color} mb-4`} />
              <h4 className="text-3xl font-bold mb-2">{indicator.value}</h4>
              <p className="text-sm font-medium text-gray-900">{indicator.label}</p>
              <p className="text-xs text-gray-600 mt-1">{indicator.sublabel}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}