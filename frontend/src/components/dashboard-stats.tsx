import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, DollarSign, Clock } from 'lucide-react';

interface DashboardStatsProps {
  monthlyProfit: number;
  profitChange: number;
  timeSaved: number;
  pendingReviews: number;
}

export function DashboardStats({ monthlyProfit, profitChange, timeSaved, pendingReviews }: DashboardStatsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Monthly Profit</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">${monthlyProfit.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground flex items-center mt-1">
            {profitChange >= 0 ? (
              <>
                <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
                <span className="text-green-500">+{profitChange}%</span>
              </>
            ) : (
              <>
                <TrendingDown className="h-3 w-3 mr-1 text-red-500" />
                <span className="text-red-500">{profitChange}%</span>
              </>
            )}
            <span className="ml-1">from last month</span>
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Time Saved</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{timeSaved} hours</div>
          <p className="text-xs text-muted-foreground mt-1">
            This month vs manual bookkeeping
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Pending Reviews</CardTitle>
          <div className="h-4 w-4 rounded-full bg-yellow-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{pendingReviews}</div>
          <p className="text-xs text-muted-foreground mt-1">
            Transactions need your attention
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Accuracy Rate</CardTitle>
          <div className="h-4 w-4 rounded-full bg-green-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">95%</div>
          <p className="text-xs text-muted-foreground mt-1">
            AI categorization accuracy
          </p>
        </CardContent>
      </Card>
    </div>
  );
}