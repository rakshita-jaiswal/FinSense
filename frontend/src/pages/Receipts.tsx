import { useState } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Upload, Search, Sparkles, FileText, Eye, Download, Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function Receipts() {
  const [searchQuery, setSearchQuery] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const mockReceipts = [
    {
      id: '1',
      vendor: 'Coffee Supplier Co.',
      date: 'Jan 29, 2025',
      amount: 842.50,
      confidence: 98,
      category: 'Supplies',
      type: 'coffee',
    },
    {
      id: '2',
      vendor: 'Office Depot',
      date: 'Jan 28, 2025',
      amount: 156.32,
      confidence: 87,
      category: 'Office Supplies',
      type: 'office',
    },
    {
      id: '3',
      vendor: 'Restaurant Supply Co.',
      date: 'Jan 26, 2025',
      amount: 1240.50,
      confidence: 96,
      category: 'Supplies',
      type: 'restaurant',
    },
    {
      id: '4',
      vendor: 'Tech Supplies USA',
      date: 'Jan 24, 2025',
      amount: 523.99,
      confidence: 92,
      category: 'Equipment',
      type: 'tech',
    },
    {
      id: '5',
      vendor: 'Gas & Electric Co.',
      date: 'Jan 23, 2025',
      amount: 324.80,
      confidence: 100,
      category: 'Utilities',
      type: 'utility',
    },
    {
      id: '6',
      vendor: 'Wholesale Food Dist.',
      date: 'Jan 21, 2025',
      amount: 2150.00,
      confidence: 95,
      category: 'Inventory',
      type: 'food',
    },
  ];

  const filteredReceipts = mockReceipts.filter((receipt) =>
    receipt.vendor.toLowerCase().includes(searchQuery.toLowerCase()) ||
    receipt.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    // Handle file upload
  };

  const getReceiptGradient = (type: string) => {
    const gradients: Record<string, string> = {
      coffee: 'from-amber-100 to-orange-100',
      office: 'from-blue-100 to-cyan-100',
      restaurant: 'from-rose-100 to-pink-100',
      tech: 'from-purple-100 to-indigo-100',
      utility: 'from-green-100 to-emerald-100',
      food: 'from-yellow-100 to-amber-100',
    };
    return gradients[type] || 'from-gray-100 to-slate-100';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Receipt Manager</h1>
            <p className="text-gray-600">Upload receipts and let AI automatically extract and categorize expenses</p>
          </div>

          {/* Search Bar */}
          <div className="mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                placeholder="Search receipts by vendor, amount, or category..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 h-14 rounded-xl text-base"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Receipt Grid */}
            <div className="lg:col-span-2">
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredReceipts.map((receipt, index) => (
                  <Card 
                    key={receipt.id} 
                    className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer animate-fade-in-up group"
                    style={{ animationDelay: `${0.1 * index}s` }}
                  >
                    <div className={`aspect-[4/3] overflow-hidden bg-gradient-to-br ${getReceiptGradient(receipt.type)} relative`}>
                      {/* Receipt Icon Placeholder */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                          <FileText className="h-20 w-20 text-gray-400 mx-auto mb-3" strokeWidth={1.5} />
                          <div className="space-y-1 px-4">
                            <div className="h-2 bg-gray-300 rounded w-32 mx-auto"></div>
                            <div className="h-2 bg-gray-300 rounded w-24 mx-auto"></div>
                            <div className="h-2 bg-gray-300 rounded w-28 mx-auto"></div>
                            <div className="h-3 bg-gray-400 rounded w-20 mx-auto mt-3"></div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Hover Actions */}
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                        <Button size="sm" className="bg-teal-500 hover:bg-teal-600">
                          <Eye className="h-4 w-4 mr-1" />
                          View
                        </Button>
                        <Button size="sm" variant="secondary">
                          <Download className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="destructive">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <CardContent className="pt-4">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-lg">{receipt.vendor}</h3>
                        <Badge className="bg-teal-100 text-teal-700 hover:bg-teal-100">
                          {receipt.category}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{receipt.date}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold">${receipt.amount.toFixed(2)}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-teal-500 rounded-full"
                              style={{ width: `${receipt.confidence}%` }}
                            />
                          </div>
                          <span className="text-xs text-gray-600">{receipt.confidence}%</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Right Column - Upload & Stats */}
            <div className="space-y-6">
              {/* Upload Card */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Upload className="h-5 w-5 text-teal-600" />
                    <div>
                      <CardTitle>Upload Receipt</CardTitle>
                      <p className="text-sm text-gray-600 mt-1">AI will process automatically</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div
                    className={`border-2 border-dashed rounded-2xl p-8 text-center transition-colors ${
                      dragActive ? 'border-teal-500 bg-teal-50' : 'border-gray-300'
                    }`}
                    onDragEnter={() => setDragActive(true)}
                    onDragLeave={() => setDragActive(false)}
                    onDragOver={(e) => e.preventDefault()}
                    onDrop={handleDrop}
                  >
                    <div className="w-16 h-16 bg-teal-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                      <Upload className="h-8 w-8 text-teal-600" />
                    </div>
                    <h3 className="font-semibold mb-2">Drag & drop receipts here</h3>
                    <p className="text-sm text-gray-600 mb-4">or click to browse files</p>
                    <p className="text-xs text-gray-500">Supports JPG, PNG, PDF</p>
                  </div>
                  <Button className="w-full mt-4 bg-teal-500 hover:bg-teal-600 rounded-xl h-12">
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Receipt
                  </Button>
                </CardContent>
              </Card>

              {/* How it Works */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Sparkles className="h-5 w-5 text-teal-600" />
                    <CardTitle>How it works</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-xs font-bold text-teal-600">1</span>
                    </div>
                    <p className="text-sm text-gray-600">Upload receipt image or PDF</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-xs font-bold text-teal-600">2</span>
                    </div>
                    <p className="text-sm text-gray-600">AI extracts vendor, amount, date</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-xs font-bold text-teal-600">3</span>
                    </div>
                    <p className="text-sm text-gray-600">Auto-categorizes based on history</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-xs font-bold text-teal-600">4</span>
                    </div>
                    <p className="text-sm text-gray-600">Creates transaction entry</p>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Stats */}
              <Card className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
                <CardHeader>
                  <CardTitle>Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">This Month</span>
                    <span className="font-bold">47 receipts</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Total Amount</span>
                    <span className="font-bold">$12,847</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Avg. Processing</span>
                    <span className="font-bold">2.3 sec</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}