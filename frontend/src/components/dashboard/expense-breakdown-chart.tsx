import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ExpenseCategory {
  category: string;
  amount: number;
  color: string;
}

interface ExpenseBreakdownChartProps {
  expenses: ExpenseCategory[];
}

export function ExpenseBreakdownChart({ expenses }: ExpenseBreakdownChartProps) {
  const [hoveredSegment, setHoveredSegment] = useState<number | null>(null);
  const total = expenses.reduce((sum, e) => sum + e.amount, 0);

  return (
    <Card className="animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
      <CardHeader>
        <CardTitle>Expense Breakdown</CardTitle>
        <p className="text-sm text-gray-600 mt-1">This month's categories</p>
      </CardHeader>
      <CardContent>
        <div className="relative w-64 h-64 mx-auto mb-6">
          <svg viewBox="0 0 100 100" className="transform -rotate-90">
            {expenses.map((expense, index) => {
              const percentage = (expense.amount / total) * 100;
              const offset = expenses.slice(0, index).reduce((sum, e) => sum + (e.amount / total) * 100, 0);
              return (
                <circle
                  key={index}
                  cx="50"
                  cy="50"
                  r="40"
                  fill="none"
                  stroke={expense.color}
                  strokeWidth="20"
                  strokeDasharray={`${percentage * 2.51} ${251 - percentage * 2.51}`}
                  strokeDashoffset={-offset * 2.51}
                  className="cursor-pointer transition-all duration-300"
                  style={{
                    opacity: hoveredSegment === null || hoveredSegment === index ? 1 : 0.3,
                    strokeWidth: hoveredSegment === index ? '24' : '20',
                  }}
                  onMouseEnter={() => setHoveredSegment(index)}
                  onMouseLeave={() => setHoveredSegment(null)}
                />
              );
            })}
          </svg>
          
          {/* Center Tooltip */}
          {hoveredSegment !== null && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="bg-white rounded-2xl shadow-2xl p-6 text-center border-2 animate-scale-in">
                <p className="text-2xl font-bold text-gray-900 mb-1">
                  {expenses[hoveredSegment].category}
                </p>
                <p className="text-xl font-semibold text-gray-700">
                  ${expenses[hoveredSegment].amount.toLocaleString()} ({((expenses[hoveredSegment].amount / total) * 100).toFixed(1)}%)
                </p>
              </div>
            </div>
          )}
        </div>
        
        <div className="space-y-2">
          {expenses.map((expense, index) => (
            <div 
              key={index} 
              className="flex items-center justify-between p-2 rounded-lg transition-all duration-300 cursor-pointer"
              style={{
                backgroundColor: hoveredSegment === index ? `${expense.color}10` : 'transparent',
              }}
              onMouseEnter={() => setHoveredSegment(index)}
              onMouseLeave={() => setHoveredSegment(null)}
            >
              <div className="flex items-center gap-2">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: expense.color }}
                />
                <span className="text-sm font-medium">{expense.category}</span>
              </div>
              <span className="text-sm font-semibold">${expense.amount.toLocaleString()}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}