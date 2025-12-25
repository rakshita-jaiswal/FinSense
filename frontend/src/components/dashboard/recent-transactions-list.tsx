import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { LucideIcon } from 'lucide-react';

interface Transaction {
  id: string;
  vendor: string;
  category: string;
  amount: number;
  time: string;
  confidence: number;
  icon: LucideIcon;
  isRevenue: boolean;
}

interface RecentTransactionsListProps {
  transactions: Transaction[];
}

export function RecentTransactionsList({ transactions }: RecentTransactionsListProps) {
  const navigate = useNavigate();

  return (
    <Card id="recent-transactions" className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Recent Transactions</CardTitle>
          <p className="text-sm text-gray-600 mt-1">AI-categorized with confidence scores</p>
        </div>
        <Button 
          id="transactions-link"
          variant="ghost" 
          className="text-teal-600" 
          onClick={() => navigate('/transactions')}
        >
          View All <ArrowRight className="h-4 w-4 ml-1" />
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="flex items-center justify-between p-4 border rounded-xl hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 ${transaction.confidence >= 90 ? 'bg-teal-100' : 'bg-gray-100'} rounded-full flex items-center justify-center`}>
                  <transaction.icon className={`h-5 w-5 ${transaction.confidence >= 90 ? 'text-teal-600' : 'text-gray-600'}`} />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-semibold">{transaction.vendor}</h4>
                    <span className="px-2 py-0.5 bg-teal-100 text-teal-700 text-xs rounded-full font-medium">
                      {transaction.category}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{transaction.time}</p>
                </div>
              </div>
              <div className="text-right">
                <p className={`text-lg font-bold ${transaction.isRevenue ? 'text-green-600' : 'text-gray-900'}`}>
                  {transaction.isRevenue ? '+' : ''}${transaction.amount.toFixed(2)}
                </p>
                <p className="text-xs text-gray-600">{transaction.confidence}% confidence</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}