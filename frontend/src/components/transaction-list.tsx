import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, AlertCircle, Edit2 } from 'lucide-react';
import { Transaction } from '@/types';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { categories } from '@/data/mockData';

interface TransactionListProps {
  transactions: Transaction[];
  onUpdateTransaction: (id: string, updates: Partial<Transaction>) => void;
}

export function TransactionList({ transactions, onUpdateTransaction }: TransactionListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);

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
    <Card>
      <CardHeader>
        <CardTitle>Recent Transactions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {transactions.map((transaction) => (
            <div
              key={transaction.id}
              className="border rounded-lg p-4 hover:bg-accent/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-semibold">{transaction.vendor}</h4>
                    {getStatusBadge(transaction)}
                  </div>
                  <p className="text-sm text-muted-foreground">
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
                    {transaction.amount < 0 ? '-' : ''}${Math.abs(transaction.amount).toFixed(2)}
                  </p>
                  <p className={`text-xs font-medium ${getConfidenceColor(transaction.confidence)}`}>
                    {Math.round(transaction.confidence * 100)}% confident
                  </p>
                </div>
              </div>

              <div className="mt-3 space-y-2">
                {editingId === transaction.id ? (
                  <div className="flex items-center gap-2">
                    <Select
                      value={transaction.category}
                      onValueChange={(value) => {
                        onUpdateTransaction(transaction.id, {
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
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">Category:</span>
                      <Badge variant="secondary">{transaction.category}</Badge>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingId(transaction.id)}
                    >
                      <Edit2 className="h-3 w-3 mr-1" />
                      Edit
                    </Button>
                  </div>
                )}

                <div className="bg-muted/50 rounded p-3">
                  <p className="text-xs text-muted-foreground mb-1 font-medium">
                    AI Explanation:
                  </p>
                  <p className="text-sm">{transaction.explanation}</p>
                </div>

                {transaction.status === 'needs-review' && (
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      className="flex-1"
                      onClick={() =>
                        onUpdateTransaction(transaction.id, {
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
                      className="flex-1"
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
  );
}