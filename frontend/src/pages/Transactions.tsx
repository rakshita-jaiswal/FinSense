import { useState, useEffect } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Filter, Download, Check, AlertCircle, Edit2 } from 'lucide-react';
import { categories } from '@/data/mockData';
import { Transaction } from '@/types';
import { useSubscription } from '@/contexts/subscription-context';
import { useNavigate } from 'react-router-dom';

const INITIAL_TRANSACTIONS = [
  {
    id: '1',
    date: '2025-01-15',
    vendor: 'Sysco Boston',
    amount: 342.50,
    category: 'Inventory - Food & Supplies',
    confidence: 0.95,
    status: 'auto-approved' as const,
    explanation: 'Categorized as Inventory because Sysco is your regular food distributor, and the $342 amount matches your typical Tuesday morning delivery.',
    paymentMethod: 'Business Debit',
    originalDescription: 'SYSCO BOSTON MA',
    decisionSource: 'Model' as const,
  },
  {
    id: '2',
    date: '2025-01-15',
    vendor: 'Property Management Co',
    amount: 2800.00,
    category: 'Rent',
    confidence: 0.98,
    status: 'auto-approved' as const,
    explanation: 'Categorized as Rent because this $2,800 charge occurs on the 1st of every month to your property management company.',
    paymentMethod: 'Business Checking',
    decisionSource: 'Rule' as const,
  },
  {
    id: '3',
    date: '2025-01-14',
    vendor: 'Amazon',
    amount: 127.43,
    category: 'Office Supplies',
    confidence: 0.83,
    status: 'needs-review' as const,
    explanation: 'Categorized as Office Supplies because your past Amazon purchases have been small operational items like paper products and cleaning supplies.',
    paymentMethod: 'Business Credit Card',
    originalDescription: 'AMZN MKTP US*XV3...',
    decisionSource: 'Model' as const,
  },
  {
    id: '4',
    date: '2025-01-14',
    vendor: 'Square Payroll',
    amount: 4200.00,
    category: 'Payroll',
    confidence: 0.99,
    status: 'auto-approved' as const,
    explanation: 'Categorized as Payroll because this is your bi-weekly Square Payroll payment for 5 employees.',
    paymentMethod: 'Business Checking',
    decisionSource: 'Rule' as const,
  },
  {
    id: '5',
    date: '2025-01-13',
    vendor: 'Uber',
    amount: 65.00,
    category: 'Travel',
    confidence: 0.72,
    status: 'needs-review' as const,
    explanation: 'This $65 charge is higher than your typical Uber rides ($15-25), suggesting a longer trip. Please verify if this is Travel or Meals & Entertainment.',
    paymentMethod: 'Business Credit Card',
    decisionSource: 'Model' as const,
  },
  {
    id: '6',
    date: '2025-01-13',
    vendor: 'Home Depot',
    amount: 847.00,
    category: 'Repairs & Maintenance',
    confidence: 0.78,
    status: 'needs-review' as const,
    explanation: 'You typically buy from BuildPro, not Home Depot, so this is likely a special repair. The $847 amount suggests equipment or facility maintenance.',
    paymentMethod: 'Business Credit Card',
    decisionSource: 'Model' as const,
  },
  {
    id: '7',
    date: '2025-01-12',
    vendor: 'Square Sales',
    amount: 920.00,
    category: 'Revenue',
    confidence: 0.99,
    status: 'auto-approved' as const,
    explanation: 'Daily revenue from Square POS transactions.',
    paymentMethod: 'Square',
    decisionSource: 'Rule' as const,
  },
  {
    id: '8',
    date: '2025-01-12',
    vendor: 'National Grid',
    amount: 245.00,
    category: 'Utilities',
    confidence: 0.96,
    status: 'auto-approved' as const,
    explanation: 'Monthly utility bill from National Grid. This is 15% higher than last month - worth checking if usage increased.',
    paymentMethod: 'Business Checking',
    decisionSource: 'Rule' as const,
  },
];

export default function Transactions() {
  const navigate = useNavigate();
  const { hasAccess } = useSubscription();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [editingId, setEditingId] = useState<string | null>(null);

  // Load transactions from localStorage or use initial data
  const [transactions, setTransactions] = useState<Transaction[]>(() => {
    const saved = localStorage.getItem('finsense_transactions');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // Map the saved data to match Transaction type
        return parsed.map((t: {
          id: string;
          date: string;
          vendor: string;
          amount: number;
          category: string;
          confidence: number;
          status: string;
          aiReason?: string;
          explanation?: string;
          decisionSource?: string;
        }) => ({
          id: t.id,
          date: t.date,
          vendor: t.vendor,
          amount: t.amount,
          category: t.category,
          confidence: t.confidence,
          status: t.status,
          explanation: t.aiReason || t.explanation || '',
          paymentMethod: 'Business Account',
          decisionSource: t.decisionSource || 'Model',
        }));
      } catch (e) {
        return INITIAL_TRANSACTIONS;
      }
    }
    return INITIAL_TRANSACTIONS;
  });

  // Save to localStorage whenever transactions change
  useEffect(() => {
    localStorage.setItem('finsense_transactions', JSON.stringify(
      transactions.map(t => ({
        id: t.id,
        vendor: t.vendor,
        amount: t.amount,
        date: t.date,
        category: t.category,
        confidence: t.confidence,
        status: t.status,
        aiReason: t.explanation,
      }))
    ));
  }, [transactions]);

  const filteredTransactions = transactions.filter((t) => {
    const matchesSearch = t.vendor.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         t.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || t.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const handleUpdateTransaction = (id: string, updates: Partial<Transaction>) => {
    setTransactions((prev) =>
      prev.map((t) => (t.id === id ? { ...t, ...updates } : t))
    );
  };

  const getStatusBadge = (transaction: Transaction) => {
    if (transaction.status === 'auto-approved') {
      return <Badge className="bg-green-500"><Check className="h-3 w-3 mr-1" />Auto-approved</Badge>;
    }
    if (transaction.status === 'needs-review') {
      return <Badge className="bg-yellow-500"><AlertCircle className="h-3 w-3 mr-1" />Needs Review</Badge>;
    }
    return <Badge variant="outline">Manual</Badge>;
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600';
    if (confidence >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50">
      <Header />

      {/* Main Content */}
      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Transactions</h1>
            <p className="text-gray-600">Review and manage your categorized transactions</p>
          </div>

          {/* Filters */}
          <Card className="mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <CardContent className="pt-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    placeholder="Search transactions..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 h-12 rounded-xl transition-all duration-300 focus:scale-105"
                  />
                </div>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-full md:w-48 h-12 rounded-xl">
                    <Filter className="h-4 w-4 mr-2" />
                    <SelectValue placeholder="Filter by status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Transactions</SelectItem>
                    <SelectItem value="auto-approved">Auto-approved</SelectItem>
                    <SelectItem value="needs-review">Needs Review</SelectItem>
                    <SelectItem value="manual">Manual</SelectItem>
                  </SelectContent>
                </Select>
                <Button className="h-12 rounded-xl bg-teal-500 hover:bg-teal-600 transition-all duration-300 hover:scale-105">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Total Transactions</div>
                <div className="text-2xl font-bold">{transactions.length}</div>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.25s' }}>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Auto-approved</div>
                <div className="text-2xl font-bold text-green-600">
                  {transactions.filter((t) => t.status === 'auto-approved').length}
                </div>
              </CardContent>
            </Card>
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Needs Review</div>
                <div className="text-2xl font-bold text-yellow-600">
                  {transactions.filter((t) => t.status === 'needs-review').length}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Transactions List */}
          <Card className="animate-fade-in-up" style={{ animationDelay: '0.35s' }}>
            <CardHeader>
              <CardTitle>All Transactions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredTransactions.map((transaction, index) => (
                  <div
                    key={transaction.id}
                    className="border rounded-xl p-4 hover:bg-teal-50/50 transition-all duration-300 animate-fade-in-up"
                    style={{ animationDelay: `${0.05 * index}s` }}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="font-semibold">{transaction.vendor}</h4>
                          {getStatusBadge(transaction)}
                        </div>
                        <p className="text-sm text-gray-600">
                          {new Date(transaction.date).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          })}
                          {' • '}
                          {transaction.paymentMethod}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold">
                          ${Math.abs(transaction.amount).toFixed(2)}
                        </p>
                        {hasAccess ? (
                          <p className={`text-xs font-medium ${getConfidenceColor(transaction.confidence)}`}>
                            {Math.round(transaction.confidence * 100)}% confident
                          </p>
                        ) : (
                          <button
                            onClick={() => navigate('/pricing')}
                            className="text-xs font-medium text-teal-600 hover:text-teal-700 hover:underline"
                          >
                            Upgrade to see confidence
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="mt-3 space-y-2">
                      {editingId === transaction.id ? (
                        <div className="flex items-center gap-2">
                          <Select
                            value={transaction.category}
                            onValueChange={(value) => {
                              handleUpdateTransaction(transaction.id, {
                                category: value,
                                status: 'manual',
                              });
                              setEditingId(null);
                            }}
                          >
                            <SelectTrigger className="flex-1">
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              {categories.map((cat) => (
                                <SelectItem key={cat.id} value={cat.name}>
                                  {cat.name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setEditingId(null)}
                          >
                            Cancel
                          </Button>
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="text-sm font-medium">Category:</span>
                              <Badge variant="secondary">{transaction.category}</Badge>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => setEditingId(transaction.id)}
                              className="transition-all duration-300 hover:scale-105"
                            >
                              <Edit2 className="h-3 w-3 mr-1" />
                              Edit
                            </Button>
                          </div>
                        </div>
                      )}

                      <div className="bg-teal-50/50 rounded-lg p-3">
                        <p className="text-xs text-gray-600 mb-1 font-medium">
                          AI Explanation:
                        </p>
                        <p className="text-sm">{transaction.explanation}</p>
                      </div>

                      {transaction.status === 'needs-review' && (
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            className="flex-1 bg-teal-500 hover:bg-teal-600 transition-all duration-300 hover:scale-105"
                            onClick={() =>
                              handleUpdateTransaction(transaction.id, {
                                status: 'auto-approved',
                              })
                            }
                          >
                            <Check className="h-4 w-4 mr-1" />
                            Looks Good
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="flex-1 transition-all duration-300 hover:scale-105"
                            onClick={() => setEditingId(transaction.id)}
                          >
                            <Edit2 className="h-4 w-4 mr-1" />
                            Change Category
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}