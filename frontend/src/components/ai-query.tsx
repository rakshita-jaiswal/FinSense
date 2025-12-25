import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Sparkles } from 'lucide-react';

export function AIQuery() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const exampleQueries = [
    'How much did I spend on coffee supplies last month?',
    'What was my profit in December?',
    'Can I afford to hire a part-time barista?',
    'Show me my biggest expenses this quarter',
  ];

  const handleQuery = () => {
    if (!query.trim()) return;

    setLoading(true);
    // Simulate AI response
    setTimeout(() => {
      setResponse(
        `Based on your financial data, here's what I found:\n\nYou spent $3,847 on coffee supplies last month (December 2024). This is 12% higher than November ($3,435), likely due to increased holiday demand. Your top suppliers were:\n\n• Sysco Boston: $2,450 (64%)\n• Local Roasters Co: $897 (23%)\n• Wholesale Coffee Supply: $500 (13%)\n\nWould you like me to break this down by week or compare to the same period last year?`
      );
      setLoading(false);
    }, 1500);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-purple-500" />
          Ask FinSense Anything
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Get instant answers about your finances in plain English
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="e.g., How much did I spend on supplies last month?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
            />
            <Button onClick={handleQuery} disabled={loading}>
              <Send className="h-4 w-4" />
            </Button>
          </div>

          {response && (
            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-sm whitespace-pre-line">{response}</p>
            </div>
          )}

          {!response && (
            <div>
              <p className="text-sm font-medium mb-2">Try asking:</p>
              <div className="space-y-2">
                {exampleQueries.map((example, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="w-full justify-start text-left h-auto py-2"
                    onClick={() => setQuery(example)}
                  >
                    {example}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}