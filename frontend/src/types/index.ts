export interface Transaction {
  id: string;
  date: string;
  vendor: string;
  amount: number;
  category: string;
  confidence: number;
  status: 'auto-approved' | 'needs-review' | 'manual';
  explanation: string;
  paymentMethod: string;
  originalDescription?: string;
  decisionSource?: 'Model' | 'Rule' | 'Manual override';
}

export interface Category {
  id: string;
  name: string;
  type: 'expense' | 'revenue' | 'cogs';
  color: string;
  highImpact?: boolean;
}

export interface CashFlowDataPoint {
  date: string;
  balance: number;
  predicted?: boolean;
}

export interface BusinessProfile {
  name: string;
  industry: string;
  monthlyRevenue: number;
  employees: number;
  connectedAccounts: string[];
}

export interface Alert {
  id: string;
  type: 'warning' | 'info' | 'success';
  title: string;
  message: string;
  date: string;
  actionable?: boolean;
}

export interface PlaidLinkToken {
  link_token: string;
  expiration: string;
}

export interface PlaidAccount {
  access_token: string;
  item_id: string;
}

export interface PlaidTransaction {
  transaction_id: string;
  date: string;
  name: string;
  amount: number;
  category?: string[];
  merchant_name?: string;
  payment_channel: string;
}

export interface StripeAuthResponse {
  authorization_url: string;
}

export interface StripeAccountInfo {
  stripe_user_id: string;
  account_name: string;
  email?: string;
}

export interface StripeCharge {
  charge_id: string;
  amount: number;
  currency: string;
  status: string;
  created: string;
  description?: string;
  customer_email?: string;
  payment_method_type: string;
}

export interface StripePaymentIntent {
  payment_intent_id: string;
  amount: number;
  currency: string;
  status: string;
  created: string;
  description?: string;
  customer_email?: string;
}