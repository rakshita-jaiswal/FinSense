import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Bell, Lock, CreditCard } from 'lucide-react';
import { toast } from 'sonner';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSubscription } from '@/contexts/subscription-context';

export default function Settings() {
  const navigate = useNavigate();
  const { isTrialActive, trialEndsAt, plan } = useSubscription();
  const [notifications, setNotifications] = useState({
    cashFlow: true,
    transactions: true,
    weekly: false,
  });

  const handlePasswordUpdate = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Password updated successfully!');
  };

  const handleUpgrade = () => {
    navigate('/pricing');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
            <p className="text-gray-600">Manage your account and preferences</p>
          </div>

          {/* Notifications */}
          <Card className="mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <Bell className="h-5 w-5 text-teal-600" />
                <CardTitle>Notifications</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base">Cash Flow Alerts</Label>
                  <p className="text-sm text-gray-600">Get notified about upcoming shortfalls</p>
                </div>
                <Switch 
                  checked={notifications.cashFlow}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, cashFlow: checked })}
                />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base">Transaction Reviews</Label>
                  <p className="text-sm text-gray-600">Daily summary of transactions needing review</p>
                </div>
                <Switch 
                  checked={notifications.transactions}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, transactions: checked })}
                />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base">Weekly Reports</Label>
                  <p className="text-sm text-gray-600">Receive weekly financial summaries</p>
                </div>
                <Switch 
                  checked={notifications.weekly}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, weekly: checked })}
                />
              </div>
            </CardContent>
          </Card>

          {/* Security */}
          <Card className="mb-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <Lock className="h-5 w-5 text-teal-600" />
                <CardTitle>Security</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <form onSubmit={handlePasswordUpdate} className="space-y-4">
                <div>
                  <Label htmlFor="current-password">Current Password</Label>
                  <Input
                    id="current-password"
                    type="password"
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <div>
                  <Label htmlFor="new-password">New Password</Label>
                  <Input
                    id="new-password"
                    type="password"
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <div>
                  <Label htmlFor="confirm-password">Confirm New Password</Label>
                  <Input
                    id="confirm-password"
                    type="password"
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <Button type="submit" className="bg-teal-500 hover:bg-teal-600 rounded-xl">
                  Update Password
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Billing */}
          <Card className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <CreditCard className="h-5 w-5 text-teal-600" />
                <CardTitle>Billing</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-teal-50 rounded-xl p-4 mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold">
                    Current Plan: {isTrialActive ? 'Free (Trial Active)' : 'Free'}
                  </span>
                  <span className="text-teal-600 font-bold">$0/month</span>
                </div>
                {isTrialActive && trialEndsAt && (
                  <p className="text-sm text-gray-600">
                    Trial ends: {new Date(trialEndsAt).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                )}
                {!isTrialActive && (
                  <p className="text-sm text-gray-600">Free plan - Upgrade to unlock premium features</p>
                )}
              </div>
              <Button
                variant="outline"
                className="w-full rounded-xl hover:bg-teal-50 hover:text-teal-700 hover:border-teal-500"
                onClick={handleUpgrade}
              >
                Upgrade to Premium Plan
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}