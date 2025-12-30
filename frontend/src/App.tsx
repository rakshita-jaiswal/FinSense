import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SubscriptionProvider } from "@/contexts/subscription-context";
import { AuthProvider } from "@/contexts/auth-context";
import { ScrollToTop } from "@/components/scroll-to-top";
import SignUp from "./pages/SignUp";
import SignIn from "./pages/SignIn";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import AIAssistant from "./pages/AIAssistant";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import Pricing from "./pages/Pricing";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import ConnectAccounts from "./pages/ConnectAccounts";
import SyncProgress from "./pages/SyncProgress";
import TransactionReview from "./pages/TransactionReview";
import Notifications from "./pages/Notifications";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <AuthProvider>
        <SubscriptionProvider>
          <TooltipProvider>
            <ScrollToTop />
            <Toaster />
            <Sonner />
            <Routes>
              <Route path="/FinSense" element={<Index />} />
              <Route path="/welcome" element={<Navigate to="/" replace />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/connect-accounts" element={<ConnectAccounts />} />
              <Route path="/sync-progress" element={<SyncProgress />} />
              <Route path="/transaction-review" element={<TransactionReview />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/transactions" element={<Transactions />} />
              <Route path="/ai-assistant" element={<AIAssistant />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/pricing" element={<Pricing />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </TooltipProvider>
        </SubscriptionProvider>
      </AuthProvider>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
