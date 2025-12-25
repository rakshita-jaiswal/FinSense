import { useState } from 'react';
import { Header } from '@/components/header';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Send, Sparkles, TrendingUp, DollarSign, Calendar, AlertCircle, Target, Activity, Bot, ArrowLeft } from 'lucide-react';
import { useSubscription } from '@/contexts/subscription-context';
import { FeatureLockOverlay } from '@/components/feature-lock-overlay';
import { API_ENDPOINTS, apiRequest } from '@/lib/api';
import { toast } from 'sonner';

export default function AIAssistant() {
  const { hasAccess } = useSubscription();
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const exampleQueries = [
    {
      icon: Sparkles,
      text: 'How are decision patterns calculated?',
      category: 'methodology',
    },
    {
      icon: Target,
      text: 'How are confidence scores analyzed?',
      category: 'methodology',
    },
    {
      icon: Activity,
      text: 'How are transaction classifications investigated?',
      category: 'methodology',
    },
    {
      icon: AlertCircle,
      text: 'Why was this transaction reviewed?',
      category: 'decision',
    },
    {
      icon: Target,
      text: 'Which decisions had the lowest confidence last week?',
      category: 'decision',
    },
    {
      icon: Activity,
      text: 'Show transactions auto-approved near the threshold',
      category: 'decision',
    },
    {
      icon: DollarSign,
      text: 'How much did I spend on supplies last month?',
      category: 'financial',
    },
    {
      icon: TrendingUp,
      text: 'What was my profit in November?',
      category: 'financial',
    },
    {
      icon: Calendar,
      text: 'Show me my biggest expenses this quarter',
      category: 'financial',
    },
  ];

  const handleSend = async () => {
    if (!query.trim() || isLoading) return;

    const userQuery = query.trim();
    setMessages([...messages, { role: 'user', content: userQuery }]);
    setQuery('');
    setIsLoading(true);

    try {
      if (!conversationId) {
        // Create new conversation
        const response = await apiRequest<any>(
          API_ENDPOINTS.aiChatConversations,
          {
            method: 'POST',
            body: JSON.stringify({
              initial_message: userQuery
            })
          }
        );
        
        setConversationId(response.id);
        setMessages([
          { role: 'user', content: userQuery },
          { role: 'assistant', content: response.messages[1].content }
        ]);
      } else {
        // Add message to existing conversation
        const response = await apiRequest<any>(
          `${API_ENDPOINTS.aiChatConversations}/${conversationId}/messages`,
          {
            method: 'POST',
            body: JSON.stringify({
              message: userQuery
            })
          }
        );
        
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: response.content }
        ]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to get AI response. Please try again.');
      // Remove the user message if request failed
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setQuery('');
    setConversationId(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-4 relative">
        {!hasAccess && (
          <FeatureLockOverlay
            title="FinSense AI is a Premium Feature"
            description="Unlock intelligent financial insights and decision analysis with our AI-powered assistant."
            features={[
              'Ask questions about your financial data',
              'Understand decision patterns and confidence scores',
              'Get instant insights on spending and revenue',
              'Analyze transaction classifications',
              'Receive personalized financial recommendations',
            ]}
          />
        )}
        <div className="max-w-7xl mx-auto">
          {/* Back Button - Only show when there are messages */}
          {messages.length > 0 && (
            <div className="mb-3 flex justify-end animate-fade-in-up">
              <Button
                variant="outline"
                onClick={handleReset}
                className="flex items-center gap-2 hover:bg-gray-100"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
            </div>
          )}

          {/* Welcome Section - Only show when no messages */}
          {messages.length === 0 && (
            <>
              {/* Welcome Message with Robot */}
              <div className="mb-4 animate-fade-in-up">
                <Card className="border-0 shadow-lg bg-gradient-to-br from-teal-50 via-cyan-50 to-blue-50">
                  <CardContent className="pt-4 pb-4">
                    <div className="flex items-center gap-4">
                      <div className="relative flex-shrink-0">
                        <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                          <Bot className="h-8 w-8 text-white" />
                        </div>
                        <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-ping"></div>
                        <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
                      </div>
                      <div className="flex-1">
                        <h2 className="text-xl font-bold text-gray-900 mb-1">
                          👋 Hi! I'm FinSense
                        </h2>
                        <p className="text-sm text-gray-700">
                          Your Decision Insight Assistant. I can help you understand decision patterns, analyze confidence scores, and investigate transaction classifications.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Example Queries */}
              <div className="space-y-8 animate-fade-in-up">
                <div>
                  <h3 className="text-base font-semibold mb-4 text-gray-800 flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-teal-600" />
                    System Methodology
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {exampleQueries.filter(q => q.category === 'methodology').map((example, index) => (
                      <button
                        key={index}
                        onClick={() => setQuery(example.text)}
                        className="flex items-center gap-3 p-4 border-2 rounded-xl hover:bg-teal-50 hover:border-teal-400 hover:shadow-md transition-all text-left group"
                      >
                        <div className="w-12 h-12 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center flex-shrink-0">
                          <example.icon className="h-6 w-6 text-teal-600" />
                        </div>
                        <span className="text-sm font-medium text-gray-700 group-hover:text-teal-700 leading-snug">{example.text}</span>
                    </button>
                  ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-base font-semibold mb-4 text-gray-800 flex items-center gap-2">
                    <Target className="h-5 w-5 text-teal-600" />
                    Decision Analysis
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {exampleQueries.filter(q => q.category === 'decision').map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(example.text)}
                      className="flex items-center gap-3 p-4 border-2 rounded-xl hover:bg-teal-50 hover:border-teal-400 hover:shadow-md transition-all text-left group"
                    >
                      <div className="w-12 h-12 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center flex-shrink-0">
                        <example.icon className="h-6 w-6 text-teal-600" />
                      </div>
                      <span className="text-sm font-medium text-gray-700 group-hover:text-teal-700 leading-snug">{example.text}</span>
                    </button>
                  ))}
                  </div>
                </div>
                <div>
                  <h3 className="text-base font-semibold mb-4 text-gray-800 flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-green-600" />
                    Financial Insights
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {exampleQueries.filter(q => q.category === 'financial').map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(example.text)}
                      className="flex items-center gap-3 p-4 border-2 rounded-xl hover:bg-green-50 hover:border-green-400 hover:shadow-md transition-all text-left group"
                    >
                      <div className="w-12 h-12 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center flex-shrink-0">
                        <example.icon className="h-6 w-6 text-green-600" />
                      </div>
                      <span className="text-sm font-medium text-gray-700 group-hover:text-green-700 leading-snug">{example.text}</span>
                    </button>
                  ))}
                  </div>
                </div>
              </div>

              {/* Input Section */}
              <div className="mt-8">
                <div className="flex gap-3">
                  <Input
                    placeholder="Ask about decisions, confidence scores, or classifications..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
                    disabled={isLoading}
                    className="h-12 rounded-xl text-sm border-2 focus:border-teal-400"
                  />
                  <Button
                    onClick={handleSend}
                    disabled={isLoading}
                    className="h-12 px-7 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 rounded-xl disabled:opacity-50"
                  >
                    {isLoading ? (
                      <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                    ) : (
                      <Send className="h-5 w-5" />
                    )}
                  </Button>
                </div>
              </div>
            </>
          )}

          {/* Chat Messages - Only show when there are messages */}
          {messages.length > 0 && (
            <>
              <div className="space-y-6 mb-6 animate-fade-in-up">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {message.role === 'assistant' && (
                      <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-500 rounded-full flex items-center justify-center flex-shrink-0 mr-3 mt-1">
                        <Bot className="h-5 w-5 text-white" />
                      </div>
                    )}
                    <div
                      className={`max-w-[75%] rounded-2xl p-5 shadow-lg ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-teal-500 to-cyan-500 text-white'
                          : 'bg-white border-2 border-gray-100'
                      }`}
                    >
                      <p className="text-sm whitespace-pre-line leading-relaxed">{message.content}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Input Section for conversation */}
              <div className="flex gap-3">
                <Input
                  placeholder="Ask a follow-up question..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
                  disabled={isLoading}
                  className="h-12 rounded-xl text-sm border-2 focus:border-teal-400"
                />
                <Button
                  onClick={handleSend}
                  disabled={isLoading}
                  className="h-12 px-7 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 rounded-xl disabled:opacity-50"
                >
                  {isLoading ? (
                    <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )}
                </Button>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}