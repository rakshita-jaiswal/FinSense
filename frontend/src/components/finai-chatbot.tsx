import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Send, TrendingUp, DollarSign, Calendar } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function FinAIChatbot() {
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState('');

  const quickQuestions = [
    {
      icon: DollarSign,
      text: 'Monthly profit?',
      query: 'What was my profit this month?',
    },
    {
      icon: TrendingUp,
      text: 'Top expenses?',
      query: 'Show me my biggest expenses',
    },
    {
      icon: Calendar,
      text: 'Last month?',
      query: 'How much did I spend last month?',
    },
  ];

  const handleQuickQuestion = (query: string) => {
    navigate('/ai-assistant', { state: { query } });
  };

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      navigate('/ai-assistant', { state: { query: inputValue } });
    }
  };

  return (
    <Card id="finai-chatbot" className="overflow-hidden animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
      <CardContent className="p-0">
        {/* Header */}
        <div className="bg-gradient-to-br from-teal-500 to-teal-600 p-6 text-white">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold">FinAI</h3>
              <p className="text-xs text-teal-50">Your AI Finance Assistant</p>
            </div>
          </div>
          <p className="text-sm text-teal-50">
            Ask me anything about your finances in plain English
          </p>
        </div>

        {/* Chat Area */}
        <div className="p-6 bg-gray-50">
          {/* Bot Message */}
          <div className="flex items-start gap-3 mb-4">
            <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center flex-shrink-0">
              <Sparkles className="h-4 w-4 text-teal-600" />
            </div>
            <div className="flex-1 bg-white rounded-2xl rounded-tl-none p-4 shadow-sm">
              <p className="text-sm text-gray-700">
                Hi! I'm FinAI. I can help you understand your finances, analyze spending patterns, and answer questions about your business.
              </p>
            </div>
          </div>

          {/* Quick Questions */}
          <div className="space-y-2 mb-4">
            <p className="text-xs font-medium text-gray-600 px-1">Quick questions:</p>
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question.query)}
                className="w-full flex items-center gap-3 p-3 bg-white rounded-xl hover:bg-teal-50 hover:border-teal-500 border border-gray-200 transition-all text-left group"
              >
                <div className="w-8 h-8 bg-teal-100 rounded-lg flex items-center justify-center group-hover:bg-teal-200 transition-colors">
                  <question.icon className="h-4 w-4 text-teal-600" />
                </div>
                <span className="text-sm font-medium text-gray-700">{question.text}</span>
              </button>
            ))}
          </div>

          {/* Input Area */}
          <div className="flex gap-2">
            <Input
              placeholder="Ask me anything..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              className="flex-1 rounded-xl border-2 focus:border-teal-500"
            />
            <Button
              onClick={handleSendMessage}
              className="bg-teal-500 hover:bg-teal-600 rounded-xl px-4"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-white border-t">
          <button
            onClick={() => navigate('/ai-assistant')}
            className="text-xs text-teal-600 hover:text-teal-700 font-medium"
          >
            Open full chat →
          </button>
        </div>
      </CardContent>
    </Card>
  );
}