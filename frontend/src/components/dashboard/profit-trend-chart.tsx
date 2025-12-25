import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ProfitDataPoint {
  date: string;
  profit: number;
}

interface ProfitTrendChartProps {
  data: ProfitDataPoint[];
}

interface TooltipProps {
  active?: boolean;
  payload?: Array<{
    value: number;
    payload: {
      date: string;
    };
  }>;
}

const CustomTooltip = ({ active, payload }: TooltipProps) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 rounded-lg shadow-lg border">
        <p className="text-sm font-semibold">{payload[0].payload.date}</p>
        <p className="text-sm text-gray-600">Profit: ${payload[0].value.toLocaleString()}</p>
      </div>
    );
  }
  return null;
};

export function ProfitTrendChart({ data }: ProfitTrendChartProps) {
  return (
    <Card className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Profit Trend</CardTitle>
          <p className="text-sm text-gray-600 mt-1">Daily profit over the last 30 days</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-teal-50 rounded-lg">
          <TrendingUp className="h-4 w-4 text-teal-600" />
          <span className="text-sm font-medium text-teal-600">+8.2%</span>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#14b8a6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              stroke="#9ca3af"
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
              stroke="#9ca3af"
            />
            <Tooltip content={<CustomTooltip />} />
            <Area 
              type="monotone" 
              dataKey="profit" 
              stroke="#14b8a6" 
              strokeWidth={3}
              fill="url(#colorProfit)"
              dot={{ fill: '#14b8a6', strokeWidth: 2, r: 5 }}
              activeDot={{ r: 7 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}