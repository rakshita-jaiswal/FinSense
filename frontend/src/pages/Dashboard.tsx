import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DollarSign, TrendingUp, CreditCard, CheckCircle, ArrowRight, Sparkles, X, AlertCircle, Wallet, Activity, Zap, Lock } from 'lucide-react';
import { FinAIChatPopup } from '@/components/finai-chat-popup';
import { Header } from '@/components/header';
import { useNavigate } from 'react-router-dom';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { expenseBreakdown, revenueTrend, mockTransactions } from '@/data/mockData';
import { useSubscription } from '@/contexts/subscription-context';

export default function Dashboard() {
  const navigate = useNavigate();
  const { hasAccess } = useSubscription();
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);
  const [pendingReviews, setPendingReviews] = useState(0);
  const [timeRange, setTimeRange] = useState('last-month');

  // Generate chart data based on selected time range
  const getChartData = () => {
    switch (timeRange) {
      case 'past-24hrs':
        return [
          { date: '12 AM', revenue: 0, expenses: 0 },
          { date: '4 AM', revenue: 0, expenses: 0 },
          { date: '8 AM', revenue: 120, expenses: 45 },
          { date: '12 PM', revenue: 380, expenses: 120 },
          { date: '4 PM', revenue: 520, expenses: 180 },
          { date: '8 PM', revenue: 230, expenses: 90 },
        ];
      case 'last-week':
        return [
          { date: 'Mon', revenue: 980, expenses: 450 },
          { date: 'Tue', revenue: 1050, expenses: 520 },
          { date: 'Wed', revenue: 1120, expenses: 680 },
          { date: 'Thu', revenue: 1180, expenses: 740 },
          { date: 'Fri', revenue: 1350, expenses: 820 },
          { date: 'Sat', revenue: 1420, expenses: 650 },
          { date: 'Sun', revenue: 920, expenses: 380 },
        ];
      case 'past-quarter':
        return [
          { date: 'Oct', revenue: 28500, expenses: 18200 },
          { date: 'Nov', revenue: 31200, expenses: 19800 },
          { date: 'Dec', revenue: 35400, expenses: 21500 },
        ];
      case 'past-year':
        return [
          { date: 'Jan', revenue: 32500, expenses: 19800 },
          { date: 'Feb', revenue: 29800, expenses: 18200 },
          { date: 'Mar', revenue: 34200, expenses: 20500 },
          { date: 'Apr', revenue: 31800, expenses: 19200 },
          { date: 'May', revenue: 35600, expenses: 21800 },
          { date: 'Jun', revenue: 38200, expenses: 23400 },
          { date: 'Jul', revenue: 36800, expenses: 22100 },
          { date: 'Aug', revenue: 33500, expenses: 20800 },
          { date: 'Sep', revenue: 37400, expenses: 22900 },
          { date: 'Oct', revenue: 35900, expenses: 21600 },
          { date: 'Nov', revenue: 39200, expenses: 24100 },
          { date: 'Dec', revenue: 42500, expenses: 25800 },
        ];
      case 'last-month':
      default:
        return [
          { date: 'Nov 1', revenue: 980, expenses: 450 },
          { date: 'Nov 5', revenue: 1050, expenses: 520 },
          { date: 'Nov 10', revenue: 1120, expenses: 680 },
          { date: 'Nov 15', revenue: 1180, expenses: 740 },
          { date: 'Nov 20', revenue: 1250, expenses: 820 },
          { date: 'Nov 25', revenue: 1320, expenses: 780 },
          { date: 'Nov 30', revenue: 1400, expenses: 650 },
        ];
    }
  };

  // Generate expense breakdown based on selected time range
  const getExpenseBreakdown = () => {
    switch (timeRange) {
      case 'past-24hrs':
        return [
          { category: 'Inventory', amount: 165, percentage: 37, color: '#3b82f6' },
          { category: 'Payroll', amount: 0, percentage: 0, color: '#f59e0b' },
          { category: 'Utilities', amount: 0, percentage: 0, color: '#06b6d4' },
          { category: 'Equipment & Maintenance', amount: 45, percentage: 10, color: '#ef4444' },
          { category: 'Marketing', amount: 0, percentage: 0, color: '#ec4899' },
          { category: 'Other', amount: 235, percentage: 53, color: '#10b981' },
        ].filter(item => item.amount > 0);
      case 'last-week':
        return [
          { category: 'Payroll', amount: 4200, percentage: 42, color: '#f59e0b' },
          { category: 'Inventory', amount: 2974, percentage: 30, color: '#3b82f6' },
          { category: 'Rent', amount: 0, percentage: 0, color: '#8b5cf6' },
          { category: 'Equipment & Maintenance', amount: 1240, percentage: 12, color: '#ef4444' },
          { category: 'Utilities', amount: 570, percentage: 6, color: '#06b6d4' },
          { category: 'Marketing', amount: 240, percentage: 2, color: '#ec4899' },
          { category: 'Other', amount: 796, percentage: 8, color: '#10b981' },
        ].filter(item => item.amount > 0);
      case 'past-quarter':
        return [
          { category: 'Payroll', amount: 25200, percentage: 36, color: '#f59e0b' },
          { category: 'Inventory', amount: 17922, percentage: 26, color: '#3b82f6' },
          { category: 'Rent', amount: 8400, percentage: 12, color: '#8b5cf6' },
          { category: 'Equipment & Maintenance', amount: 7416, percentage: 11, color: '#ef4444' },
          { category: 'Utilities', amount: 4710, percentage: 7, color: '#06b6d4' },
          { category: 'Marketing', amount: 3720, percentage: 5, color: '#ec4899' },
          { category: 'Other', amount: 2132, percentage: 3, color: '#10b981' },
        ];
      case 'past-year':
        return [
          { category: 'Payroll', amount: 100800, percentage: 36, color: '#f59e0b' },
          { category: 'Inventory', amount: 71688, percentage: 26, color: '#3b82f6' },
          { category: 'Rent', amount: 33600, percentage: 12, color: '#8b5cf6' },
          { category: 'Equipment & Maintenance', amount: 29664, percentage: 11, color: '#ef4444' },
          { category: 'Utilities', amount: 18840, percentage: 7, color: '#06b6d4' },
          { category: 'Marketing', amount: 14880, percentage: 5, color: '#ec4899' },
          { category: 'Other', amount: 8528, percentage: 3, color: '#10b981' },
        ];
      case 'last-month':
      default:
        return [
          { category: 'Payroll', amount: 8400, percentage: 35, color: '#f59e0b' },
          { category: 'Inventory', amount: 5974, percentage: 25, color: '#3b82f6' },
          { category: 'Rent', amount: 2800, percentage: 12, color: '#8b5cf6' },
          { category: 'Equipment & Maintenance', amount: 2472, percentage: 10, color: '#ef4444' },
          { category: 'Utilities', amount: 1570, percentage: 7, color: '#06b6d4' },
          { category: 'Marketing', amount: 1240, percentage: 5, color: '#ec4899' },
          { category: 'Other', amount: 1544, percentage: 6, color: '#10b981' },
        ];
    }
  };

  const chartData = getChartData();
  const expenseBreakdownData = getExpenseBreakdown();

  useEffect(() => {
    // Check if user just completed transaction review
    const hasReviewedTransactions = localStorage.getItem('finsense_transactions_reviewed') === 'true';
    const hasSeenBanner = localStorage.getItem('finsense_success_banner_seen') === 'true';
    
    if (hasReviewedTransactions && !hasSeenBanner) {
      setShowSuccessBanner(true);
    }

    // Check for pending reviews
    const saved = localStorage.getItem('finsense_transactions');
    if (saved) {
      try {
        const transactions = JSON.parse(saved);
        const needsReview = transactions.filter((t: { status: string }) => t.status === 'needs-review').length;
        setPendingReviews(needsReview);
      } catch (e) {
        // If error, use default from mockTransactions
        const needsReview = mockTransactions.filter(t => t.status === 'needs-review').length;
        setPendingReviews(needsReview);
      }
    } else {
      // Use default from mockTransactions
      const needsReview = mockTransactions.filter(t => t.status === 'needs-review').length;
      setPendingReviews(needsReview);
    }
  }, []);

  const handleCloseBanner = () => {
    setShowSuccessBanner(false);
    localStorage.setItem('finsense_success_banner_seen', 'true');
  };

  // Calculate real stats from transactions
  const revenue = mockTransactions
    .filter(t => t.category === 'Revenue')
    .reduce((sum, t) => sum + Math.abs(t.amount), 0);
  
  const expenses = mockTransactions
    .filter(t => t.category !== 'Revenue')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const profit = revenue - expenses;
  const cashBalance = 24596;

  const stats = [
    {
      title: 'Monthly Revenue',
      value: `$${revenue.toLocaleString()}`,
      change: '+12.5%',
      isPositive: true,
      icon: DollarSign,
      color: 'bg-teal-500',
    },
    {
      title: 'Net Profit',
      value: `$${profit.toLocaleString()}`,
      change: '+8.2%',
      isPositive: true,
      icon: TrendingUp,
      color: 'bg-green-500',
    },
    {
      title: 'Total Expenses',
      value: `$${expenses.toLocaleString()}`,
      change: '+15.3%',
      isPositive: false,
      icon: CreditCard,
      color: 'bg-blue-500',
    },
    {
      title: 'Cash Balance',
      value: `$${cashBalance.toLocaleString()}`,
      change: '+3.1%',
      isPositive: true,
      icon: Wallet,
      color: 'bg-purple-500',
    },
  ];

  const recentActivity = mockTransactions.slice(0, 5).map(t => ({
    vendor: t.vendor,
    amount: Math.abs(t.amount),
    category: t.category,
    status: t.status,
    time: new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    isRevenue: t.category === 'Revenue',
  }));

  return (
    <div className="min-h-screen bg-gray-50 bg-mesh-gradient">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Success Banner */}
          {showSuccessBanner && (
            <Card className="mb-8 bg-gradient-to-r from-teal-500 to-cyan-500 border-0 shadow-2xl animate-fade-in-up">
              <CardContent className="pt-6 pb-6 relative">
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute top-4 right-4 text-white hover:bg-white/20"
                  onClick={handleCloseBanner}
                >
                  <X className="h-5 w-5" />
                </Button>
                <div className="flex items-start gap-6">
                  <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <Sparkles className="h-8 w-8 text-white" />
                  </div>
                  <div className="flex-1 text-white">
                    <h3 className="text-2xl font-bold mb-2">🎉 You just did 2 hours of work in 2 minutes!</h3>
                    <p className="text-lg text-white/90 mb-4">
                      All your transactions are categorized and ready for tax time. No more spreadsheets, no more guessing.
                    </p>
                    <div className="flex items-center gap-6 text-sm">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        <span>{mockTransactions.length} transactions categorized</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        <span>95% auto-approved</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        <span>Tax-ready books</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <Card key={index} className="animate-fade-in-up shine-effect hover:shadow-xl transition-all duration-300 border-0 shadow-lg" style={{ animationDelay: `${index * 0.1}s` }}>
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-2">{stat.title}</p>
                      <h3 className="text-3xl font-bold">{stat.value}</h3>
                    </div>
                    <div className={`${stat.color} p-3 rounded-xl animate-float-slow shadow-lg`}>
                      <stat.icon className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {stat.isPositive ? (
                      <TrendingUp className="h-4 w-4 text-green-600" />
                    ) : (
                      <TrendingUp className="h-4 w-4 text-red-600 rotate-180" />
                    )}
                    <span className={`text-sm font-medium ${stat.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                      {stat.change}
                    </span>
                    <span className="text-sm text-gray-600">vs last month</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Decision Engine Health Panel - Premium Only */}
          {hasAccess && (
            <Card className="mb-8 border-0 bg-gradient-to-br from-teal-50 to-cyan-50 animate-fade-in-up shadow-xl shine-effect" style={{ animationDelay: '0.4s' }}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5 text-teal-600" />
                  Decision Engine Health
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <p className="text-3xl font-bold text-gray-900">72%</p>
                    </div>
                    <p className="text-sm text-gray-600">Auto-approval rate</p>
                    <p className="text-xs text-gray-500 mt-1">High confidence decisions</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <AlertCircle className="h-5 w-5 text-yellow-600" />
                      <p className="text-3xl font-bold text-gray-900">23%</p>
                    </div>
                    <p className="text-sm text-gray-600">Review rate</p>
                    <p className="text-xs text-gray-500 mt-1">Medium confidence</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <AlertCircle className="h-5 w-5 text-red-600" />
                      <p className="text-3xl font-bold text-gray-900">5%</p>
                    </div>
                    <p className="text-sm text-gray-600">Manual rate</p>
                    <p className="text-xs text-gray-500 mt-1">High-risk cases</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <Zap className="h-5 w-5 text-teal-600" />
                      <p className="text-3xl font-bold text-gray-900">1.9s</p>
                    </div>
                    <p className="text-sm text-gray-600">Avg decision latency</p>
                    <p className="text-xs text-gray-500 mt-1">Real-time processing</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Review More Alert */}
          {pendingReviews > 0 && (
            <Card className="mb-8 border-yellow-200 bg-yellow-50 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <AlertCircle className="h-6 w-6 text-yellow-600 flex-shrink-0 mt-1" />
                  <div className="flex-1">
                    <h3 className="font-semibold text-yellow-900 mb-1">
                      {pendingReviews} Transaction{pendingReviews > 1 ? 's' : ''} Need Review
                    </h3>
                    <p className="text-sm text-yellow-800 mb-3">
                      Some transactions need your attention to ensure accurate categorization.
                    </p>
                    <Button 
                      size="sm" 
                      className="bg-yellow-600 hover:bg-yellow-700"
                      onClick={() => navigate('/transaction-review')}
                    >
                      Review More ({pendingReviews})
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Revenue vs Expenses Chart */}
            <Card className="lg:col-span-2 animate-fade-in-up relative border-0 shadow-xl hover:shadow-2xl transition-all duration-300" style={{ animationDelay: '0.5s' }}>
              <div className={!hasAccess ? 'opacity-20 blur-sm' : ''}>
                <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>
                    Revenue vs Expenses (
                    {timeRange === 'past-24hrs' && 'Past 24 hrs'}
                    {timeRange === 'last-week' && 'Last week'}
                    {timeRange === 'last-month' && 'Last month'}
                    {timeRange === 'past-quarter' && 'Past quarter'}
                    {timeRange === 'past-year' && 'Past year'}
                    )
                  </CardTitle>
                  <Select value={timeRange} onValueChange={setTimeRange}>
                    <SelectTrigger className="w-[160px]">
                      <SelectValue placeholder="Select time range" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="past-24hrs">Past 24 hrs</SelectItem>
                      <SelectItem value="last-week">Last week</SelectItem>
                      <SelectItem value="last-month">Last month</SelectItem>
                      <SelectItem value="past-quarter">Past quarter</SelectItem>
                      <SelectItem value="past-year">Past year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={350}>
                  <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => `$${value}`} />
                    <Tooltip 
                      formatter={(value: number) => `$${value.toLocaleString()}`}
                      contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="revenue" 
                      stroke="#10b981" 
                      strokeWidth={2}
                      fill="url(#colorRevenue)"
                      name="Revenue"
                    />
                    <Area 
                      type="monotone" 
                      dataKey="expenses" 
                      stroke="#ef4444" 
                      strokeWidth={2}
                      fill="url(#colorExpenses)"
                      name="Expenses"
                    />
                  </AreaChart>
                </ResponsiveContainer>
                </CardContent>
              </div>
              {!hasAccess && (
                <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
                  <div className="text-center p-6 bg-white rounded-xl shadow-2xl pointer-events-auto">
                    <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Lock className="w-8 h-8 text-teal-600" />
                    </div>
                    <h3 className="text-lg font-bold mb-2">Premium Feature</h3>
                    <p className="text-gray-600 mb-4">Upgrade to view revenue vs expense trends</p>
                    <Button
                      className="bg-teal-500 hover:bg-teal-600"
                      onClick={() => navigate('/pricing')}
                    >
                      Upgrade to Premium
                    </Button>
                  </div>
                </div>
              )}
            </Card>

            {/* Expense Breakdown Pie Chart */}
            <Card className="animate-fade-in-up relative border-0 shadow-xl hover:shadow-2xl transition-all duration-300" style={{ animationDelay: '0.6s' }}>
              <div className={!hasAccess ? 'opacity-20 blur-sm' : ''}>
                <CardHeader>
                <CardTitle>Expense Breakdown</CardTitle>
              </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={expenseBreakdownData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ payload }) => `${payload.percentage}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="amount"
                    >
                      {expenseBreakdownData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value: number) => `$${value.toLocaleString()}`}
                      contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-4 space-y-2">
                  {expenseBreakdownData.slice(0, 4).map((item, index) => (
                    <div key={index} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: item.color }}
                        />
                        <span className="text-gray-700">{item.category}</span>
                      </div>
                      <span className="font-semibold">${item.amount.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
                </CardContent>
              </div>
              {!hasAccess && (
                <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
                  <div className="text-center p-6 bg-white rounded-xl shadow-2xl pointer-events-auto">
                    <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Lock className="w-8 h-8 text-teal-600" />
                    </div>
                    <h3 className="text-lg font-bold mb-2">Premium Feature</h3>
                    <p className="text-gray-600 mb-4">Upgrade to view expense breakdown</p>
                    <Button
                      className="bg-teal-500 hover:bg-teal-600"
                      onClick={() => navigate('/pricing')}
                    >
                      Upgrade to Premium
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          </div>

          {/* Recent Activity */}
          <Card className="mb-8 animate-fade-in-up border-0 shadow-xl" style={{ animationDelay: '0.7s' }}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold">Recent Transactions</h2>
                <Button 
                  variant="ghost" 
                  className="text-teal-600"
                  onClick={() => navigate('/transactions')}
                >
                  View All <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
              <div className="space-y-3">
                {recentActivity.map((activity, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-4 border rounded-xl hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 ${activity.isRevenue ? 'bg-green-100' : 'bg-teal-100'} rounded-full flex items-center justify-center`}>
                        {activity.status === 'needs-review' ? (
                          <AlertCircle className="h-5 w-5 text-yellow-600" />
                        ) : (
                          <CheckCircle className={`h-5 w-5 ${activity.isRevenue ? 'text-green-600' : 'text-teal-600'}`} />
                        )}
                      </div>
                      <div>
                        <h4 className="font-semibold">{activity.vendor}</h4>
                        <div className="flex items-center gap-2">
                          <p className="text-sm text-gray-600">{activity.time}</p>
                          <span className="text-xs px-2 py-0.5 bg-gray-100 rounded-full">
                            {activity.category}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`text-lg font-bold ${activity.isRevenue ? 'text-green-600' : 'text-gray-900'}`}>
                        {activity.isRevenue ? '+' : '-'}${activity.amount.toFixed(2)}
                      </p>
                      {!hasAccess && (
                        <button
                          onClick={() => navigate('/pricing')}
                          className="text-xs font-medium text-teal-600 hover:text-teal-700 hover:underline mt-1"
                        >
                          Upgrade to see confidence
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

        </div>
      </main>

      {/* Floating Chat Button */}
      <FinAIChatPopup />
    </div>
  );
}