import { useState } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { FileText, Download, Mail, Calendar, TrendingUp, TrendingDown } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Reports() {
  const [reportPeriod, setReportPeriod] = useState('this-month');
  const [reportType, setReportType] = useState('profit-loss');
  const [activeTab, setActiveTab] = useState('trends');
  const [exportFormat, setExportFormat] = useState('pdf');
  const [includeOptions, setIncludeOptions] = useState({
    transactionDetails: true,
    receiptImages: false,
    chartsGraphs: false,
    executiveSummary: true,
    taxReady: true,
  });

  const revenueData = [
    { month: 'Jul', revenue: 42000, profit: 14000 },
    { month: 'Aug', revenue: 45000, profit: 15500 },
    { month: 'Sep', revenue: 43000, profit: 13000 },
    { month: 'Oct', revenue: 47000, profit: 16000 },
    { month: 'Nov', revenue: 46000, profit: 15000 },
    { month: 'Dec', revenue: 52000, profit: 18000 },
    { month: 'Jan', revenue: 50000, profit: 17500 },
  ];

  const categoryData = [
    { category: 'Supplies', transactions: 28, change: 12.5, amount: 13437, percentage: 45 },
    { category: 'Rent', transactions: 1, change: 0, amount: 5972, percentage: 20 },
    { category: 'Utilities', transactions: 8, change: 8.3, amount: 4479, percentage: 15 },
    { category: 'Office Supplies', transactions: 12, change: -5.2, amount: 2389, percentage: 8 },
    { category: 'Miscellaneous', transactions: 15, change: 15.7, amount: 3585, percentage: 12 },
  ];

  const recentExports = [
    { name: 'Jan 2025 Report', date: 'Jan 30, 2025' },
    { name: 'Q4 2024 Tax Summary', date: 'Jan 15, 2025' },
    { name: 'Dec 2024 Report', date: 'Jan 5, 2025' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Reports & Analytics</h1>
            <p className="text-gray-600">Generate tax-ready financial reports and analyze spending patterns</p>
          </div>

          {/* Filters */}
          <Card className="mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                <div>
                  <Label className="mb-2 block">Report Period</Label>
                  <Select value={reportPeriod} onValueChange={setReportPeriod}>
                    <SelectTrigger className="h-12 rounded-xl">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="this-month">This Month</SelectItem>
                      <SelectItem value="last-month">Last Month</SelectItem>
                      <SelectItem value="this-quarter">This Quarter</SelectItem>
                      <SelectItem value="this-year">This Year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label className="mb-2 block">Date Range</Label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type="text"
                      value="Jan 01 - Dec 06, 2025"
                      readOnly
                      className="w-full h-12 pl-10 pr-4 border rounded-xl"
                    />
                  </div>
                </div>
                <div>
                  <Label className="mb-2 block">Report Type</Label>
                  <Select value={reportType} onValueChange={setReportType}>
                    <SelectTrigger className="h-12 rounded-xl">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="profit-loss">Profit & Loss</SelectItem>
                      <SelectItem value="cash-flow">Cash Flow</SelectItem>
                      <SelectItem value="expense-breakdown">Expense Breakdown</SelectItem>
                      <SelectItem value="tax-summary">Tax Summary</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="mt-4 flex justify-end">
                <Button className="bg-teal-500 hover:bg-teal-600 rounded-xl px-8">
                  Apply Filters
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Charts */}
            <div className="lg:col-span-2 space-y-6">
              {/* Tabs */}
              <div className="flex gap-2 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                {['Trends', 'Comparison', 'Distribution'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab.toLowerCase())}
                    className={`px-6 py-3 rounded-xl font-medium transition-all ${
                      activeTab === tab.toLowerCase()
                        ? 'bg-white shadow-sm'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>

              {/* Revenue & Profit Trend */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
                <CardHeader>
                  <CardTitle>Revenue & Profit Trend</CardTitle>
                  <p className="text-sm text-gray-600 mt-1">7-month financial performance</p>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={revenueData}>
                      <defs>
                        <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#14b8a6" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`} />
                      <Tooltip formatter={(value: number) => `$${value.toLocaleString()}`} />
                      <Area 
                        type="monotone" 
                        dataKey="revenue" 
                        stroke="#14b8a6" 
                        strokeWidth={2}
                        fill="url(#colorRevenue)"
                        dot={{ fill: '#14b8a6', r: 4 }}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="profit" 
                        stroke="#3b82f6" 
                        strokeWidth={2}
                        fill="url(#colorProfit)"
                        dot={{ fill: '#3b82f6', r: 4 }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                  <div className="flex justify-center gap-6 mt-4">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-blue-500" />
                      <span className="text-sm">Profit</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-teal-500" />
                      <span className="text-sm">Revenue</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Category Breakdown */}
              
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
                <CardHeader>
                  <CardTitle>Category Breakdown</CardTitle>
                  <p className="text-sm text-gray-600 mt-1">Detailed expense analysis by category</p>
                </CardHeader>
                <CardContent className="space-y-6">
                  {categoryData.map((category, index) => (
                    <div key={index}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className="font-semibold">{category.category}</span>
                          <span className="text-sm text-gray-600">{category.transactions} transactions</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="flex items-center gap-1">
                            {category.change > 0 ? (
                              <TrendingUp className="h-4 w-4 text-red-600" />
                            ) : (
                              <TrendingDown className="h-4 w-4 text-green-600" />
                            )}
                            <span className={`text-sm font-medium ${category.change > 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {Math.abs(category.change)}%
                            </span>
                          </div>
                          <span className="font-bold">${category.amount.toLocaleString()}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-teal-500 rounded-full"
                            style={{ width: `${category.percentage}%` }}
                          />
                        </div>
                        <span className="text-sm text-gray-600 w-12 text-right">{category.percentage}%</span>
                      </div>
                    </div>
                  ))}
                  <div className="pt-4 border-t">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-lg">Total Expenses</span>
                      <span className="font-bold text-2xl">$29,862</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Right Column - Export Options */}
            <div className="space-y-6">
              {/* Export Report */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-teal-600" />
                    <div>
                      <CardTitle>Export Report</CardTitle>
                      <p className="text-sm text-gray-600 mt-1">Download tax-ready reports</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label className="mb-3 block font-semibold">Format</Label>
                    <div className="space-y-2">
                      {[
                        { value: 'pdf', label: 'PDF Report', desc: 'Formatted financial report' },
                        { value: 'csv', label: 'CSV Export', desc: 'Spreadsheet data' },
                        { value: 'excel', label: 'Excel Workbook', desc: 'Multi-sheet workbook' },
                      ].map((format) => (
                        <button
                          key={format.value}
                          onClick={() => setExportFormat(format.value)}
                          className={`w-full flex items-start gap-3 p-3 border rounded-xl transition-all text-left ${
                            exportFormat === format.value
                              ? 'border-teal-500 bg-teal-50'
                              : 'hover:bg-gray-50'
                          }`}
                        >
                          <FileText className="h-5 w-5 text-teal-600 mt-0.5" />
                          <div>
                            <p className="font-medium">{format.label}</p>
                            <p className="text-xs text-gray-600">{format.desc}</p>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <Label className="mb-3 block font-semibold">Include</Label>
                    <div className="space-y-3">
                      {[
                        { key: 'transactionDetails', label: 'Transaction Details' },
                        { key: 'receiptImages', label: 'Receipt Images' },
                        { key: 'chartsGraphs', label: 'Charts & Graphs' },
                        { key: 'executiveSummary', label: 'Executive Summary' },
                        { key: 'taxReady', label: 'Tax-Ready Format' },
                      ].map((option) => (
                        <div key={option.key} className="flex items-center gap-2">
                          <Checkbox
                            id={option.key}
                            checked={includeOptions[option.key as keyof typeof includeOptions]}
                            onCheckedChange={(checked) =>
                              setIncludeOptions({ ...includeOptions, [option.key]: checked })
                            }
                          />
                          <Label htmlFor={option.key} className="cursor-pointer">
                            {option.label}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <Button className="w-full bg-teal-500 hover:bg-teal-600 rounded-xl h-12">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Report
                  </Button>
                  <Button variant="outline" className="w-full rounded-xl h-12">
                    <Mail className="h-4 w-4 mr-2" />
                    Email to Accountant
                  </Button>
                </CardContent>
              </Card>

              {/* Tax-Ready Reports */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
                <CardHeader>
                  <CardTitle>Tax-Ready Reports</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    All exports include IRS-compliant formatting with categorized expenses, deductible items highlighted, and receipt documentation attached.
                  </p>
                </CardContent>
              </Card>

              {/* Recent Exports */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.7s' }}>
                <CardHeader>
                  <CardTitle>Recent Exports</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {recentExports.map((export_, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-xl hover:bg-gray-50">
                      <div>
                        <p className="font-medium text-sm">{export_.name}</p>
                        <p className="text-xs text-gray-600">{export_.date}</p>
                      </div>
                      <Button variant="ghost" size="sm">
                        Download
                      </Button>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}