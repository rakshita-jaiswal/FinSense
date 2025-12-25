import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { TrendingUp, Mail, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSubscription } from '@/contexts/subscription-context';
import { API_ENDPOINTS, apiRequest } from '@/lib/api';
import { toast } from 'sonner';

export default function SignUp() {
  const navigate = useNavigate();
  const { startTrial } = useSubscription();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    businessName: '',
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({
    firstName: '',
    lastName: '',
    businessName: '',
    email: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string) => {
    // Password must be at least 8 characters and contain:
    // - At least one uppercase letter
    // - At least one lowercase letter
    // - At least one number
    // - At least one special character
    const minLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    
    return {
      isValid: minLength && hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar,
      minLength,
      hasUpperCase,
      hasLowerCase,
      hasNumber,
      hasSpecialChar
    };
  };

  const validateForm = () => {
    const newErrors = {
      firstName: '',
      lastName: '',
      businessName: '',
      email: '',
      password: '',
    };

    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }

    if (!formData.businessName.trim()) {
      newErrors.businessName = 'Business name is required';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else {
      const passwordValidation = validatePassword(formData.password);
      if (!passwordValidation.isValid) {
        const missing = [];
        if (!passwordValidation.minLength) missing.push('8 characters');
        if (!passwordValidation.hasUpperCase) missing.push('uppercase letter');
        if (!passwordValidation.hasLowerCase) missing.push('lowercase letter');
        if (!passwordValidation.hasNumber) missing.push('number');
        if (!passwordValidation.hasSpecialChar) missing.push('special character');
        newErrors.password = `Password must include: ${missing.join(', ')}`;
      }
    }

    setErrors(newErrors);
    return !Object.values(newErrors).some(error => error !== '');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Call backend signup API
      const response = await apiRequest<{ access_token: string; user: any }>(
        API_ENDPOINTS.signup,
        {
          method: 'POST',
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            first_name: formData.firstName,
            last_name: formData.lastName,
            business_name: formData.businessName,
          }),
        }
      );

      // Store token
      localStorage.setItem('finsense_token', response.access_token);
      
      toast.success('Account created successfully!');
      
      // Reload the page to trigger auth context to load user data
      window.location.href = '/connect-accounts';
    } catch (error) {
      console.error('Signup failed:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to create account');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-cyan-50 bg-animated flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        {/* Logo */}
        <div className="flex justify-center mb-8 animate-fade-in">
          <div className="w-20 h-20 bg-gradient-to-br from-teal-500 to-teal-600 rounded-2xl flex items-center justify-center shadow-2xl transition-all duration-300 hover:scale-110 animate-float-slow">
            <TrendingUp className="w-10 h-10 text-white" strokeWidth={2.5} />
          </div>
        </div>

        {/* Title */}
        <div className="text-center mb-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Create your account</h1>
          <p className="text-gray-600">Get started with our free plan • No credit card required</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 animate-scale-in glass-effect" style={{ animationDelay: '0.2s' }}>
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
                <Label htmlFor="firstName" className="text-sm font-medium text-gray-700">
                  First name
                </Label>
                <Input
                  id="firstName"
                  placeholder="Enter your first name"
                  value={formData.firstName}
                  onChange={(e) => {
                    setFormData({ ...formData, firstName: e.target.value });
                    setErrors({ ...errors, firstName: '' });
                  }}
                  className={`mt-1.5 h-12 rounded-xl border-2 transition-all duration-300 focus:scale-105 ${
                    errors.firstName ? 'border-red-500 focus:border-red-500' : 'focus:border-teal-500'
                  }`}
                />
                {errors.firstName && (
                  <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                    <AlertCircle className="h-3 w-3" />
                    {errors.firstName}
                  </p>
                )}
              </div>
              <div className="animate-fade-in-up" style={{ animationDelay: '0.35s' }}>
                <Label htmlFor="lastName" className="text-sm font-medium text-gray-700">
                  Last name
                </Label>
                <Input
                  id="lastName"
                  placeholder="Enter your last name"
                  value={formData.lastName}
                  onChange={(e) => {
                    setFormData({ ...formData, lastName: e.target.value });
                    setErrors({ ...errors, lastName: '' });
                  }}
                  className={`mt-1.5 h-12 rounded-xl border-2 transition-all duration-300 focus:scale-105 ${
                    errors.lastName ? 'border-red-500 focus:border-red-500' : 'focus:border-teal-500'
                  }`}
                />
                {errors.lastName && (
                  <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                    <AlertCircle className="h-3 w-3" />
                    {errors.lastName}
                  </p>
                )}
              </div>
            </div>

            <div className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <Label htmlFor="businessName" className="text-sm font-medium text-gray-700">
                Business name
              </Label>
              <Input
                id="businessName"
                placeholder="Enter your business name"
                value={formData.businessName}
                onChange={(e) => {
                  setFormData({ ...formData, businessName: e.target.value });
                  setErrors({ ...errors, businessName: '' });
                }}
                className={`mt-1.5 h-12 rounded-xl border-2 transition-all duration-300 focus:scale-105 ${
                  errors.businessName ? 'border-red-500 focus:border-red-500' : 'focus:border-teal-500'
                }`}
              />
              {errors.businessName && (
                <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                  <AlertCircle className="h-3 w-3" />
                  {errors.businessName}
                </p>
              )}
            </div>

            <div className="animate-fade-in-up" style={{ animationDelay: '0.45s' }}>
              <Label htmlFor="email" className="text-sm font-medium text-gray-700">
                Email
              </Label>
              <div className="relative mt-1.5">
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email address"
                  value={formData.email}
                  onChange={(e) => {
                    setFormData({ ...formData, email: e.target.value });
                    setErrors({ ...errors, email: '' });
                  }}
                  className={`h-12 rounded-xl pr-10 border-2 transition-all duration-300 focus:scale-105 ${
                    errors.email ? 'border-red-500 focus:border-red-500' : 'focus:border-teal-500'
                  }`}
                />
                <Mail className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-teal-500" />
              </div>
              {errors.email && (
                <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                  <AlertCircle className="h-3 w-3" />
                  {errors.email}
                </p>
              )}
            </div>

            <div className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
              <Label htmlFor="password" className="text-sm font-medium text-gray-700">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="Min 8 chars with uppercase, number & special char"
                value={formData.password}
                onChange={(e) => {
                  setFormData({ ...formData, password: e.target.value });
                  setErrors({ ...errors, password: '' });
                }}
                className={`mt-1.5 h-12 rounded-xl border-2 transition-all duration-300 focus:scale-105 ${
                  errors.password ? 'border-red-500 focus:border-red-500' : 'focus:border-teal-500'
                }`}
              />
              {errors.password && (
                <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                  <AlertCircle className="h-3 w-3" />
                  {errors.password}
                </p>
              )}
            </div>

            <div className="animate-fade-in-up" style={{ animationDelay: '0.55s' }}>
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-12 bg-teal-500 hover:bg-teal-600 text-white rounded-xl text-base font-medium transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Creating account...' : 'Create account'}
              </Button>
            </div>
          </form>
        </div>

        {/* Sign In Link */}
        <p className="text-center mt-6 text-sm text-gray-600 animate-fade-in" style={{ animationDelay: '0.6s' }}>
          Already have an account?{' '}
          <button
            onClick={() => navigate('/signin')}
            className="text-teal-600 font-medium hover:underline transition-all duration-300"
          >
            Sign in
          </button>
        </p>
      </div>
    </div>
  );
}