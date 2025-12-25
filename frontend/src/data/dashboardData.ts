import { 
  DollarSign, 
  TrendingUp, 
  Wallet, 
  CreditCard,
  Activity,
  Target,
  TrendingDown,
  Upload,
  FileText,
  Download,
  MessageSquare,
  CheckCircle,
  Clock
} from 'lucide-react';

export const stats = [
  {
    title: 'Total Revenue',
    value: '$48,294',
    change: '+12.5%',
    isPositive: true,
    icon: DollarSign,
    color: 'bg-teal-500',
  },
  {
    title: 'Net Profit',
    value: '$18,432',
    change: '+8.2%',
    isPositive: true,
    icon: TrendingUp,
    color: 'bg-teal-500',
  },
  {
    title: 'Total Expenses',
    value: '$29,862',
    change: '+15.3%',
    isPositive: true,
    icon: CreditCard,
    color: 'bg-teal-500',
  },
  {
    title: 'Cash Balance',
    value: '$124,596',
    change: '-2.4%',
    isPositive: false,
    icon: Wallet,
    color: 'bg-teal-500',
  },
];

export const profitData = [
  { date: 'Jan 1', profit: 12000 },
  { date: 'Jan 5', profit: 15000 },
  { date: 'Jan 10', profit: 13500 },
  { date: 'Jan 15', profit: 18000 },
  { date: 'Jan 20', profit: 16500 },
  { date: 'Jan 25', profit: 19500 },
  { date: 'Jan 30', profit: 18500 },
];

export const keyIndicators = [
  {
    icon: TrendingUp,
    value: '+12.5%',
    label: 'Revenue Growth',
    sublabel: 'vs last month',
    color: 'text-teal-500',
    bgColor: 'bg-teal-50',
  },
  {
    icon: Activity,
    value: '1,247',
    label: 'Customer Count',
    sublabel: '+18% increase',
    color: 'text-teal-500',
    bgColor: 'bg-teal-50',
  },
  {
    icon: TrendingDown,
    value: '$38.72',
    label: 'Avg. Transaction',
    sublabel: '-3.2% from last week',
    color: 'text-teal-500',
    bgColor: 'bg-teal-50',
  },
  {
    icon: Target,
    value: '87%',
    label: 'Monthly Target',
    sublabel: 'On track to meet goal',
    color: 'text-teal-500',
    bgColor: 'bg-teal-50',
  },
];

export const quickActions = [
  {
    id: 'upload-receipt',
    icon: Upload,
    title: 'Upload Receipt',
    description: 'AI will categorize automatically',
    route: '/receipts',
  },
  {
    id: 'ask-ai-assistant',
    icon: MessageSquare,
    title: 'Ask FinSense AI',
    description: 'Get instant financial insights',
    route: '/ai-assistant',
  },
  {
    id: 'generate-report',
    icon: FileText,
    title: 'Generate Report',
    description: 'Export tax-ready financials',
    route: '/reports',
  },
  {
    id: 'export-data',
    icon: Download,
    title: 'Export Data',
    description: 'Download as CSV or PDF',
    route: null,
  },
];

export const recentTransactions = [
  {
    id: '1',
    vendor: 'Coffee Supplier Co.',
    category: 'Supplies',
    amount: 842.50,
    time: 'Today, 10:24 AM',
    confidence: 98,
    icon: CheckCircle,
    isRevenue: false,
  },
  {
    id: '2',
    vendor: 'Square Payment',
    category: 'Revenue',
    amount: 1250.00,
    time: 'Today, 9:15 AM',
    confidence: 100,
    icon: CheckCircle,
    isRevenue: true,
  },
  {
    id: '3',
    vendor: 'Electric Company',
    category: 'Utilities',
    amount: 324.80,
    time: 'Yesterday, 3:42 PM',
    confidence: 95,
    icon: CheckCircle,
    isRevenue: false,
  },
  {
    id: '4',
    vendor: 'Office Depot',
    category: 'Office Supplies',
    amount: 156.32,
    time: 'Yesterday, 11:20 AM',
    confidence: 87,
    icon: Clock,
    isRevenue: false,
  },
  {
    id: '5',
    vendor: 'PayPal Transfer',
    category: 'Revenue',
    amount: 2100.00,
    time: 'Jan 28, 4:15 PM',
    confidence: 100,
    icon: CheckCircle,
    isRevenue: true,
  },
];

export const expenseBreakdown = [
  { category: 'Supplies', amount: 12500, color: '#10b981' },
  { category: 'Utilities', amount: 8200, color: '#3b82f6' },
  { category: 'Payroll', amount: 15000, color: '#f97316' },
  { category: 'Marketing', amount: 6800, color: '#a855f7' },
  { category: 'Equipment', amount: 4500, color: '#ec4899' },
  { category: 'Other', amount: 4162, color: '#06b6d4' },
];