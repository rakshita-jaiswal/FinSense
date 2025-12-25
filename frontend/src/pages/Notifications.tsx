import { useState } from 'react';
import { Header } from '@/components/header';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle, AlertCircle, Info, X, Bell } from 'lucide-react';

export default function Notifications() {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'success',
      title: 'Transaction Categorized',
      message: '5 new transactions have been automatically categorized',
      time: '2 minutes ago',
      read: false,
    },
    {
      id: 2,
      type: 'warning',
      title: 'Review Required',
      message: '3 transactions need your review for accurate categorization',
      time: '1 hour ago',
      read: false,
    },
    {
      id: 3,
      type: 'info',
      title: 'Monthly Report Ready',
      message: 'Your November financial report is ready to view',
      time: '3 hours ago',
      read: true,
    },
    {
      id: 4,
      type: 'success',
      title: 'Account Connected',
      message: 'Your bank account has been successfully connected',
      time: '1 day ago',
      read: true,
    },
    {
      id: 5,
      type: 'info',
      title: 'New Feature Available',
      message: 'Check out our new AI-powered expense forecasting feature',
      time: '2 days ago',
      read: true,
    },
  ]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = (id: number) => {
    setNotifications(notifications.map(n => 
      n.id === id ? { ...n, read: true } : n
    ));
  };

  const markAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })));
  };

  const deleteNotification = (id: number) => {
    setNotifications(notifications.filter(n => n.id !== id));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-6 w-6 text-green-600" />;
      case 'warning':
        return <AlertCircle className="h-6 w-6 text-yellow-600" />;
      case 'info':
        return <Info className="h-6 w-6 text-blue-600" />;
      default:
        return <Bell className="h-6 w-6 text-gray-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 bg-mesh-gradient">
      <Header />

      <main className="container mx-auto px-4 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 animate-fade-in-up">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Notifications</h1>
            <p className="text-gray-600">Stay updated with your financial activities</p>
          </div>

          {/* Actions Bar */}
          <div className="flex items-center justify-between mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <div className="flex items-center gap-2">
              {unreadCount > 0 && (
                <span className="text-sm text-gray-600">
                  {unreadCount} unread notification{unreadCount > 1 ? 's' : ''}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              {unreadCount > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={markAllAsRead}
                  className="rounded-xl"
                >
                  Mark all as read
                </Button>
              )}
              {notifications.length > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearAll}
                  className="rounded-xl text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  Clear all
                </Button>
              )}
            </div>
          </div>

          {/* Notifications List */}
          {notifications.length === 0 ? (
            <Card className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <CardContent className="py-16 text-center">
                <Bell className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No notifications</h3>
                <p className="text-gray-600">You're all caught up! Check back later for updates.</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-3">
              {notifications.map((notification, index) => (
                <Card
                  key={notification.id}
                  className={`animate-fade-in-up hover:shadow-lg transition-all duration-300 ${
                    !notification.read ? 'border-l-4 border-l-teal-500 bg-teal-50/30' : ''
                  }`}
                  style={{ animationDelay: `${0.1 * (index + 2)}s` }}
                >
                  <CardContent className="p-6">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-4 mb-2">
                          <div className="flex items-center gap-3">
                            <h3 className="font-semibold text-lg text-gray-900">
                              {notification.title}
                            </h3>
                            {!notification.read && (
                              <span className="px-2 py-0.5 bg-teal-500 text-white text-xs rounded-full font-medium">
                                New
                              </span>
                            )}
                          </div>
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="text-gray-400 hover:text-red-600 transition-colors"
                            title="Delete notification"
                          >
                            <X className="h-5 w-5" />
                          </button>
                        </div>
                        <p className="text-gray-600 mb-3">
                          {notification.message}
                        </p>
                        <div className="flex items-center justify-between">
                          <p className="text-sm text-gray-400">
                            {notification.time}
                          </p>
                          {!notification.read && (
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => markAsRead(notification.id)}
                              className="text-teal-600 hover:text-teal-700 hover:bg-teal-50"
                            >
                              Mark as read
                            </Button>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}