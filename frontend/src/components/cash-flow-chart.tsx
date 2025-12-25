import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { CashFlowDataPoint } from '@/types';

interface CashFlowChartProps {
  data: CashFlowDataPoint[];
  safetyThreshold?: number;
}

export function CashFlowChart({ data, safetyThreshold = 7000 }: CashFlowChartProps) {
  const formattedData = data.map((point) => ({
    ...point,
    displayDate: new Date(point.date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    }),
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cash Flow Forecast (14 Days)</CardTitle>
        <p className="text-sm text-muted-foreground">
          Predicted balance based on your historical patterns and upcoming expenses
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="displayDate"
              tick={{ fontSize: 12 }}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}K`}
            />
            <Tooltip
              formatter={(value: number) => [`$${value.toLocaleString()}`, 'Balance']}
              labelFormatter={(label) => `Date: ${label}`}
            />
            <ReferenceLine
              y={safetyThreshold}
              stroke="#ef4444"
              strokeDasharray="3 3"
              label={{ value: 'Safety Threshold', position: 'right', fontSize: 12 }}
            />
            <Line
              type="monotone"
              dataKey="balance"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={(props) => {
                const { cx, cy, payload } = props;
                return (
                  <circle
                    cx={cx}
                    cy={cy}
                    r={4}
                    fill={payload.predicted ? '#94a3b8' : '#3b82f6'}
                    stroke="white"
                    strokeWidth={2}
                  />
                );
              }}
            />
          </LineChart>
        </ResponsiveContainer>
        <div className="mt-4 flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span>Actual</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-slate-400" />
            <span>Predicted</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-0.5 bg-red-500 border-dashed" />
            <span>Safety Threshold</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}