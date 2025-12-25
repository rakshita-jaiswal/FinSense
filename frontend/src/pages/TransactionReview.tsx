import { useState, useEffect } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Check, AlertCircle, Sparkles, ArrowRight, RotateCcw, Clock, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { categories } from '@/data/mockData';
import { useSubscription } from '@/contexts/subscription-context';

const INITIAL_TRANSACTIONS = [
  {
    id: '1',
    vendor: 'Sysco Boston',
    amount: 342.50,
    date: '2025-01-15',
    category: 'Inventory - Food & Supplies',
    confidence: 0.98,
    status: 'auto-approved' as const,
    aiReason: 'Sysco is your regular food distributor. Pattern matches 47 previous transactions.',
  },
  {
    id: '2',
    vendor: 'Amazon Business',
    amount: 127.43,
    date: '2025-01-14',
    category: 'Office Supplies',
    confidence: 0.83,
    status: 'needs-review' as const,
    aiReason: 'Amazon purchases vary. Past items: cleaning supplies (60%), office supplies (40%).',
  },
  {
    id: '3',
    vendor: 'Uber',
    amount: 65.00,
    date: '2025-01-13',
    category: 'Travel',
    confidence: 0.72,
    status: 'needs-review' as const,
    aiReason: 'Higher than typical Uber rides ($15-25). Verify if business travel or meals.',
  },
  {
    id: '4',
    vendor: 'Home Depot',
    amount: 847.00,
    date: '2025-01-13',
    category: 'Repairs & Maintenance',
    confidence: 0.78,
    status: 'needs-review' as const,
    aiReason: 'Unusual vendor for you. Large amount suggests equipment or facility repair.',
  },
  {
    id: '5',
    vendor: 'Office Depot',
    amount: 234.56,
    date: '2025-01-12',
    category: 'Office Supplies',
    confidence: 0.81,
    status: 'needs-review' as const,
    aiReason: 'First purchase from Office Depot. Verify if this is office supplies or equipment.',
  },
  {
    id: '6',
    vendor: 'Restaurant Supply Co',
    amount: 1240.00,
    date: '2025-01-11',
    category: 'Equipment',
    confidence: 0.75,
    status: 'needs-review' as const,
    aiReason: 'Large purchase. Could be equipment or inventory. Please verify category.',
  },
  {
    id: '7',
    vendor: 'Square Payroll',
    amount: 4200.00,
    date: '2025-01-10',
    category: 'Payroll',
    confidence: 0.99,
    status: 'auto-approved' as const,
    aiReason: 'Regular bi-weekly payroll payment. Matches historical pattern.',
  },
  {
    id: '8',
    vendor: 'Gas & Electric',
    amount: 324.80,
    date: '2025-01-09',
    category: 'Utilities',
    confidence: 0.96,
    status: 'auto-approved' as const,
    aiReason: 'Monthly utility bill. Amount is 15% higher than last month.',
  },
];

export default function TransactionReview() {
  const navigate = useNavigate();
  const { hasAccess } = useSubscription();

  // Load transactions from localStorage or use initial data
  const [transactions, setTransactions] = useState(() => {
    const saved = localStorage.getItem('finsense_transactions');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return INITIAL_TRANSACTIONS;
      }
    }
    return INITIAL_TRANSACTIONS;
  });

  // Save transactions to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('finsense_transactions', JSON.stringify(transactions));
  }, [transactions]);

  const needsReview = transactions.filter(t => t.status === 'needs-review');
  const autoApproved = transactions.filter(t => t.status === 'auto-approved');
  const highRisk = transactions.filter(t => t.status === 'high-risk');

  const handleReset = () => {
    setTransactions(INITIAL_TRANSACTIONS);
    localStorage.removeItem('finsense_transactions_reviewed');
    localStorage.removeItem('finsense_success_banner_seen');
    toast.success('Demo reset! Fresh transactions loaded.');
  };

  const handleApprove = (id: string) => {
    setTransactions(transactions.map(t => 
      t.id === id ? { ...t, status: 'auto-approved' as const } : t
    ));
    toast.success('Transaction approved');
  };

  const handleUpdateCategory = (id: string, category: string) => {
    setTransactions(transactions.map(t => 
      t.id === id ? { ...t, category, status: 'auto-approved' as const } : t
    ));
    toast.success('Category updated. AI will learn from this.');
  };

  const handleReviewLater = () => {
    // Save current state and go to dashboard
    toast.info(`${needsReview.length} transactions saved for later review`);
    navigate('/dashboard');
  };

  const handleAllSet = () => {
    if (needsReview.length > 0) {
      toast.error(`Please review ${needsReview.length} remaining transactions first`);
      return;
    }
    
    // Mark that user has reviewed all transactions
    localStorage.setItem('finsense_transactions_reviewed', 'true');
    toast.success('All transactions reviewed! 🎉');
    navigate('/dashboard');
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600';
    if (confidence >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getThresholdMessage = (confidence: number) => {
    if (confidence >= 0.9) return 'Meets auto-approval threshold (90%)';
    if (confidence >= 0.7) return 'Below auto-approval threshold (90%)';
    return 'Below review threshold (70%)';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <div className="flex items-center justify-between mb-3">
              <h1 className="text-4xl font-bold text-gray-900">Review Your Transactions</h1>
              <Button
                variant="outline"
                size="sm"
                onClick={handleReset}
                className="rounded-xl"
              >
                <RotateCcw className="h-4 w-4 mr-2" />
                Reset Demo
              </Button>
            </div>
            <p className="text-lg text-gray-600">
              We categorized <strong>127 transactions</strong>. <strong>{autoApproved.length} auto-approved</strong> · <strong>{needsReview.length} require review</strong> · <strong>{highRisk.length} high-risk manual</strong>.
            </p>
          </div>

          {/* Progress Stats */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <Check className="h-6 w-6 text-green-600" />
                    <p className="text-4xl font-bold text-green-600">{autoApproved.length}</p>
                  </div>
                  <p className="text-sm text-gray-600">Auto-approved</p>
                  <p className="text-xs text-gray-500 mt-1">High confidence (90%+)</p>
                </div>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <AlertCircle className="h-6 w-6 text-yellow-600" />
                    <p className="text-4xl font-bold text-yellow-600">{needsReview.length}</p>
                  </div>
                  <p className="text-sm text-gray-600">Require review</p>
                  <p className="text-xs text-gray-500 mt-1">Medium confidence</p>
                </div>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <AlertCircle className="h-6 w-6 text-red-600" />
                    <p className="text-4xl font-bold text-red-600">{highRisk.length}</p>
                  </div>
                  <p className="text-sm text-gray-600">High-risk manual</p>
                  <p className="text-xs text-gray-500 mt-1">Requires verification</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Needs Review Section */}
          {needsReview.length > 0 && (
            <Card className="mb-8 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-yellow-600" />
                  Review These ({needsReview.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {needsReview.map((transaction, index) => (
                  <div
                    key={transaction.id}
                    className="border-2 border-yellow-200 rounded-xl p-6 bg-yellow-50/50 animate-fade-in-up"
                    style={{ animationDelay: `${0.05 * index}s` }}
                  >
                    {/* Transaction Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h4 className="text-xl font-bold text-gray-900 mb-1">{transaction.vendor}</h4>
                        <p className="text-sm text-gray-600">{transaction.date}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-gray-900">${transaction.amount.toFixed(2)}</p>
                        {hasAccess ? (
                          <>
                            <p className={`text-sm font-medium ${getConfidenceColor(transaction.confidence)}`}>
                              {Math.round(transaction.confidence * 100)}% confident
                            </p>
                            <p className="text-xs text-gray-500 mt-0.5">
                              {getThresholdMessage(transaction.confidence)}
                            </p>
                          </>
                        ) : (
                          <button
                            onClick={() => navigate('/pricing')}
                            className="text-sm font-medium text-teal-600 hover:text-teal-700 hover:underline"
                          >
                            Upgrade to see confidence
                          </button>
                        )}
                      </div>
                    </div>

                    {/* AI Explanation */}
                    <div className="bg-white rounded-lg p-4 mb-4">
                      <div className="flex items-start gap-2">
                        <Sparkles className="h-5 w-5 text-purple-600 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="text-sm font-medium text-gray-900 mb-1">AI Analysis:</p>
                          <p className="text-sm text-gray-700">{transaction.aiReason}</p>
                        </div>
                      </div>
                    </div>

                    {/* Category & Actions */}
                    <div className="flex items-center gap-3">
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-700 mb-2 block">Category:</label>
                        <Select
                          value={transaction.category}
                          onValueChange={(value) => handleUpdateCategory(transaction.id, value)}
                        >
                          <SelectTrigger className="h-12 rounded-xl">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            {categories.map((cat) => (
                              <SelectItem key={cat.id} value={cat.name}>
                                <div className="flex items-center gap-2">
                                  <span>{cat.name}</span>
                                  {cat.highImpact && (
                                    <TooltipProvider>
                                      <Tooltip>
                                        <TooltipTrigger asChild>
                                          <Badge variant="destructive" className="text-xs px-1.5 py-0">
                                            High Impact
                                          </Badge>
                                        </TooltipTrigger>
                                        <TooltipContent>
                                          <p className="text-xs">Errors in this category are treated as high-risk and always require review.</p>
                                        </TooltipContent>
                                      </Tooltip>
                                    </TooltipProvider>
                                  )}
                                </div>
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="pt-7">
                        <Button
                          size="lg"
                          className="bg-teal-500 hover:bg-teal-600 rounded-xl h-12 px-6"
                          onClick={() => handleApprove(transaction.id)}
                        >
                          <Check className="h-5 w-5 mr-2" />
                          Approve
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* All Done Message */}
          {needsReview.length === 0 && (
            <Card className="mb-8 animate-fade-in-up bg-green-50 border-green-200" style={{ animationDelay: '0.2s' }}>
              <CardContent className="pt-6 text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Check className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-2xl font-bold text-green-900 mb-2">All Done! 🎉</h3>
                <p className="text-green-700 mb-4">
                  You've reviewed all transactions. Great job!
                </p>
              </CardContent>
            </Card>
          )}

          {/* Auto-Approved Summary */}
          <Card className="mb-8 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Check className="h-5 w-5 text-green-600" />
                Auto-Approved ({autoApproved.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {autoApproved.slice(0, 3).map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between p-4 border rounded-lg bg-green-50/50"
                  >
                    <div className="flex items-center gap-3">
                      <Check className="h-5 w-5 text-green-600" />
                      <div>
                        <p className="font-semibold">{transaction.vendor}</p>
                        <p className="text-sm text-gray-600">{transaction.date}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-lg">${transaction.amount.toFixed(2)}</p>
                      <Badge variant="secondary" className="text-xs">{transaction.category}</Badge>
                    </div>
                  </div>
                ))}
                {autoApproved.length > 3 && (
                  <p className="text-sm text-gray-600 text-center pt-2">
                    + {autoApproved.length - 3} more auto-approved
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex justify-between animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <Button
              size="lg"
              variant="outline"
              className="rounded-xl px-8"
              onClick={handleReviewLater}
            >
              <Clock className="h-5 w-5 mr-2" />
              Review Later
            </Button>
            <Button
              size="lg"
              className="bg-teal-500 hover:bg-teal-600 rounded-xl px-8"
              onClick={handleAllSet}
              disabled={needsReview.length > 0}
            >
              {needsReview.length > 0 ? `Review ${needsReview.length} More` : "All Set! I'm Done"}
              <ArrowRight className="h-5 w-5 ml-2" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}