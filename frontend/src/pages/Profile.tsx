import { useState, useEffect } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Building2, Mail, Phone, User as UserIcon, Upload, Trash2, Crown, Check, Sparkles } from 'lucide-react';
import { useAuth } from '@/contexts/auth-context';
import { useSubscription } from '@/contexts/subscription-context';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';

export default function Profile() {
  const navigate = useNavigate();
  const { user, updateProfile, logout } = useAuth();
  const { hasAccess, isTrialActive } = useSubscription();
  const [formData, setFormData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    businessName: user?.businessName || '',
    industry: user?.industry || '',
    employees: user?.employees?.toString() || '',
    revenue: user?.monthlyRevenue?.toString() || '',
  });
  const [avatarUrl, setAvatarUrl] = useState<string>('');
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  // Update form data when user data changes
  useEffect(() => {
    if (user) {
      setFormData({
        firstName: user.firstName || '',
        lastName: user.lastName || '',
        email: user.email || '',
        phone: user.phone || '',
        businessName: user.businessName || '',
        industry: user.industry || '',
        employees: user.employees?.toString() || '',
        revenue: user.monthlyRevenue?.toString() || '',
      });
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateProfile({
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        businessName: formData.businessName,
        phone: formData.phone,
        industry: formData.industry,
        employees: formData.employees ? parseInt(formData.employees) : undefined,
        monthlyRevenue: formData.revenue ? parseFloat(formData.revenue.replace(/[$,]/g, '')) : undefined,
      });
      toast.success('Profile updated successfully!');
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarUrl(reader.result as string);
        toast.success('Profile photo updated!');
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDeleteAccount = () => {
    toast.success('Account deleted successfully');
    setTimeout(() => {
      logout();
    }, 1000);
  };

  const initials = `${formData.firstName.charAt(0)}${formData.lastName.charAt(0)}`.toUpperCase();

  const premiumFeatures = [
    { name: 'AI-powered auto-categorization (95% accuracy)', upcoming: false },
    { name: 'Transaction confidence scores', upcoming: false },
    { name: 'Smart transaction review workflow', upcoming: false },
    { name: 'FinSense AI chat for financial insights', upcoming: false },
    { name: 'Revenue vs expense trend charts', upcoming: false },
    { name: 'Expense breakdown pie charts', upcoming: false },
    { name: 'Financial reports with filters', upcoming: false },
    { name: 'Receipt upload interface', upcoming: true },
    { name: 'Export data functionality', upcoming: true },
    { name: 'Priority customer support', upcoming: true },
  ];

  return (
    <div className="min-h-screen bg-gray-50 bg-mesh-gradient">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Profile</h1>
            <p className="text-gray-600">Manage your personal and business information</p>
          </div>

          {/* Profile Picture */}
          <Card className="mb-6 animate-fade-in-up shadow-lg hover:shadow-xl transition-all duration-300" style={{ animationDelay: '0.1s' }}>
            <CardContent className="pt-6">
              <div className="flex items-center gap-6">
                <Avatar className="w-24 h-24">
                  {avatarUrl ? (
                    <AvatarImage src={avatarUrl} alt="Profile" />
                  ) : (
                    <AvatarFallback className="bg-teal-100 text-teal-600 text-2xl">
                      {initials}
                    </AvatarFallback>
                  )}
                </Avatar>
                <div>
                  <h3 className="font-semibold text-lg mb-1">{formData.firstName} {formData.lastName}</h3>
                  <p className="text-gray-600 mb-3">{formData.email}</p>
                  <div className="flex gap-2">
                    <label htmlFor="avatar-upload">
                      <Button type="button" variant="outline" className="rounded-xl" asChild>
                        <span className="cursor-pointer">
                          <Upload className="h-4 w-4 mr-2" />
                          Change Photo
                        </span>
                      </Button>
                    </label>
                    <input
                      id="avatar-upload"
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={handleImageUpload}
                      aria-label="Upload profile photo"
                    />
                    {avatarUrl && (
                      <Button
                        type="button"
                        variant="outline"
                        className="rounded-xl"
                        onClick={() => {
                          setAvatarUrl('');
                          toast.success('Profile photo removed');
                        }}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <form onSubmit={handleSubmit}>
            {/* Personal Information */}
            <Card className="mb-6 animate-fade-in-up shadow-lg hover:shadow-xl transition-all duration-300" style={{ animationDelay: '0.2s' }}>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <UserIcon className="h-5 w-5 text-teal-600" />
                  <CardTitle>Personal Information</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="first-name">First Name</Label>
                    <Input
                      id="first-name"
                      value={formData.firstName}
                      onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                      className="mt-1.5 h-12 rounded-xl"
                    />
                  </div>
                  <div>
                    <Label htmlFor="last-name">Last Name</Label>
                    <Input
                      id="last-name"
                      value={formData.lastName}
                      onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                      className="mt-1.5 h-12 rounded-xl"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="email">
                    <Mail className="inline h-4 w-4 mr-2" />
                    Email
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <div>
                  <Label htmlFor="phone">
                    <Phone className="inline h-4 w-4 mr-2" />
                    Phone
                  </Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Business Information */}
            <Card className="mb-6 animate-fade-in-up shadow-lg hover:shadow-xl transition-all duration-300" style={{ animationDelay: '0.3s' }}>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Building2 className="h-5 w-5 text-teal-600" />
                  <CardTitle>Business Information</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="business-name">Business Name</Label>
                  <Input
                    id="business-name"
                    value={formData.businessName}
                    onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <div>
                  <Label htmlFor="industry">Industry</Label>
                  <Input
                    id="industry"
                    value={formData.industry}
                    onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                    className="mt-1.5 h-12 rounded-xl"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="employees">Number of Employees</Label>
                    <Input
                      id="employees"
                      type="number"
                      value={formData.employees}
                      onChange={(e) => setFormData({ ...formData, employees: e.target.value })}
                      className="mt-1.5 h-12 rounded-xl"
                    />
                  </div>
                  <div>
                    <Label htmlFor="revenue">Monthly Revenue</Label>
                    <Input
                      id="revenue"
                      value={formData.revenue}
                      onChange={(e) => setFormData({ ...formData, revenue: e.target.value })}
                      className="mt-1.5 h-12 rounded-xl"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Upgrade Plan Section */}
            {!hasAccess && (
              <Card className="mb-6 animate-fade-in-up border-2 border-teal-500 bg-gradient-to-br from-teal-50 to-cyan-50 shadow-xl shine-effect" style={{ animationDelay: '0.4s' }}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center">
                        <Crown className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-xl">Upgrade to Premium</CardTitle>
                        <p className="text-sm text-gray-600 mt-1">Unlock all features for $29/month</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-teal-600">$29</div>
                      <div className="text-sm text-gray-600">/month</div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-teal-600" />
                      Premium Features
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {premiumFeatures.map((feature, index) => (
                        <div key={index} className="flex items-start gap-2">
                          <div className="w-5 h-5 bg-teal-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <Check className="w-3 h-3 text-white" />
                          </div>
                          <span className="text-sm text-gray-700">
                            {feature.name}
                            {feature.upcoming && (
                              <span className="ml-2 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                                Upcoming
                              </span>
                            )}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Button
                      type="button"
                      size="lg"
                      className="flex-1 bg-teal-500 hover:bg-teal-600 rounded-xl h-12"
                      onClick={() => navigate('/pricing')}
                    >
                      <Crown className="h-5 w-5 mr-2" />
                      Upgrade Now
                    </Button>
                    <Button
                      type="button"
                      size="lg"
                      variant="outline"
                      className="rounded-xl h-12 px-6"
                      onClick={() => navigate('/pricing')}
                    >
                      View Details
                    </Button>
                  </div>
                  <p className="text-xs text-center text-gray-600 mt-3">
                    14-day free trial • No credit card required • Cancel anytime
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Current Plan Status (if trial active) */}
            {isTrialActive && (
              <Card className="mb-6 animate-fade-in-up bg-green-50 border-green-200" style={{ animationDelay: '0.4s' }}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <Check className="h-5 w-5 text-green-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-green-900">Trial Active</h4>
                        <p className="text-sm text-green-700">You have access to all premium features</p>
                      </div>
                    </div>
                    <Button
                      type="button"
                      variant="outline"
                      className="rounded-xl"
                      onClick={() => navigate('/pricing')}
                    >
                      View Plans
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            <div className="flex justify-between animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
              <Button 
                type="button"
                variant="destructive" 
                className="rounded-xl px-8"
                onClick={() => setShowDeleteDialog(true)}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete Account
              </Button>
              <Button type="submit" className="bg-teal-500 hover:bg-teal-600 rounded-xl px-8">
                Save Changes
              </Button>
            </div>
          </form>
        </div>
      </main>

      {/* Delete Account Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your account and remove all your data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction 
              onClick={handleDeleteAccount}
              className="bg-red-600 hover:bg-red-700"
            >
              Delete Account
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}