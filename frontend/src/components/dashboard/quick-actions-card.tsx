import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useNavigate } from 'react-router-dom';
import { LucideIcon } from 'lucide-react';

interface QuickAction {
  id: string;
  icon: LucideIcon;
  title: string;
  description: string;
  route: string | null;
}

interface QuickActionsCardProps {
  actions: QuickAction[];
}

export function QuickActionsCard({ actions }: QuickActionsCardProps) {
  const navigate = useNavigate();

  const handleAction = (route: string | null) => {
    if (route) {
      navigate(route);
    }
  };

  return (
    <Card id="quick-actions" className="animate-fade-in-up" style={{ animationDelay: '0.7s' }}>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {actions.map((action, index) => (
          <button
            key={index}
            id={action.id}
            onClick={() => handleAction(action.route)}
            className="w-full flex items-start gap-4 p-4 border rounded-xl hover:bg-teal-50 hover:border-teal-500 transition-all duration-300 text-left"
          >
            <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <action.icon className="h-5 w-5 text-teal-600" />
            </div>
            <div>
              <h4 className="font-semibold mb-1">{action.title}</h4>
              <p className="text-sm text-gray-600">{action.description}</p>
            </div>
          </button>
        ))}
      </CardContent>
    </Card>
  );
}