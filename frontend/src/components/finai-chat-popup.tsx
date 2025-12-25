import { useState } from 'react';
import { Bot } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function FinAIChatPopup() {
  const navigate = useNavigate();
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className="fixed bottom-8 right-8 z-50"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Message Tooltip - Only show on hover */}
      {isHovered && (
        <div className="absolute bottom-0 right-20 animate-fade-in">
          <div className="bg-white rounded-xl shadow-2xl border-2 border-teal-500 p-3 relative whitespace-nowrap">
            <p className="text-sm font-medium text-gray-900">
              Need help? Ask FinSense
            </p>
          </div>
          {/* Arrow pointing to button */}
          <div className="absolute top-1/2 -right-2 transform -translate-y-1/2">
            <div className="w-0 h-0 border-t-8 border-t-transparent border-b-8 border-b-transparent border-l-8 border-l-teal-500"></div>
            <div className="w-0 h-0 border-t-8 border-t-transparent border-b-8 border-b-transparent border-l-8 border-l-white absolute top-0 -left-[7px]"></div>
          </div>
        </div>
      )}

      {/* Floating Chat Button */}
      <button
        onClick={() => navigate('/ai-assistant')}
        className="w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 animate-pulse"
        aria-label="Open FinSense AI"
      >
        <Bot className="h-7 w-7 text-white" />
      </button>
    </div>
  );
}