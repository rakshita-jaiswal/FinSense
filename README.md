# FinSense 💰

A comprehensive financial management platform for tracking expenses, managing transactions, and gaining AI-powered financial insights.

## 🌐 Live Demo

**Frontend**: Deploy using one of these options:
- **Vercel** (Recommended): [Deploy Now](https://vercel.com/new/clone?repository-url=https://github.com/rakshita-jaiswal/FinSense)
- **Netlify**: [Deploy Now](https://app.netlify.com/start/deploy?repository=https://github.com/rakshita-jaiswal/FinSense)
- **GitHub Pages**: See [Deployment Guide](DEPLOYMENT_GUIDE.md)

**Repository**: [https://github.com/rakshita-jaiswal/FinSense](https://github.com/rakshita-jaiswal/FinSense)

## ✨ Features

### Core Features
- 🔐 **User Authentication** - Secure sign-up and login with JWT
- 💳 **Account Management** - Connect and manage multiple financial accounts
- 📊 **Transaction Tracking** - Automatic transaction categorization and tracking
- 📈 **Dashboard Analytics** - Visual insights into spending patterns
- 🤖 **AI Assistant** - Gemini-powered financial advice and insights
- 💰 **Subscription Management** - Tiered pricing with Stripe integration
- 🔄 **Plaid Integration** - Secure bank account connections
- 📱 **Responsive Design** - Works seamlessly on all devices

### Advanced Features
- Real-time transaction syncing
- Custom category management
- Cash flow analysis
- Expense breakdown charts
- Profit trend visualization
- AI-powered chat for financial queries
- Feature restrictions based on subscription tier

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Radix UI + Tailwind CSS
- **State Management**: TanStack Query
- **Routing**: React Router v6
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Payment Processing**: Stripe
- **Banking Integration**: Plaid
- **AI Integration**: Google Gemini AI

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.9+
- MongoDB instance
- Plaid account (for banking features)
- Stripe account (for payments)
- Google Gemini API key (for AI features)

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Add your environment variables
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your environment variables (see .env.example)

# Start the server
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

## 📦 Project Structure

```
FinSense/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   ├── hooks/           # Custom hooks
│   │   ├── lib/             # Utilities and API client
│   │   └── types/           # TypeScript type definitions
│   ├── public/              # Static assets
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── auth/                # Authentication logic
│   ├── models/              # Database models
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic services
│   ├── main.py              # Application entry point
│   └── requirements.txt
│
└── DEPLOYMENT_GUIDE.md      # Detailed deployment instructions
```

## 🌍 Deployment

### Quick Deploy Options

#### Deploy to Vercel (Frontend)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rakshita-jaiswal/FinSense)

1. Click the button above
2. Configure root directory as `frontend`
3. Add environment variables
4. Deploy!

#### Deploy to Netlify (Frontend)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/rakshita-jaiswal/FinSense)

#### Deploy Backend
- **Render**: [Deploy Guide](DEPLOYMENT_GUIDE.md#option-1-deploy-backend-to-render)
- **Railway**: [Deploy Guide](DEPLOYMENT_GUIDE.md#option-2-deploy-backend-to-railway)
- **Heroku**: [Deploy Guide](DEPLOYMENT_GUIDE.md#option-3-deploy-backend-to-heroku)

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🔑 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_PLAID_ENV=sandbox
```

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017/finsense
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Plaid Configuration
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENV=sandbox

# Stripe Configuration
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key
```

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [MongoDB Setup](MONGODB_SETUP_GUIDE.md) - Database configuration
- [Plaid Integration](PLAID_INTEGRATION.md) - Banking integration setup
- [Stripe Setup](STRIPE_SETUP_GUIDE.md) - Payment processing setup
- [Gemini AI Setup](backend/GEMINI_AI_SETUP.md) - AI assistant configuration
- [Feature Restrictions](FEATURE_RESTRICTIONS_PLAN.md) - Subscription tier features

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Radix UI](https://www.radix-ui.com/) for accessible UI components
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Plaid](https://plaid.com/) for banking integration
- [Stripe](https://stripe.com/) for payment processing
- [Google Gemini](https://ai.google.dev/) for AI capabilities

## 📧 Contact

For questions or support, please open an issue on GitHub:
[https://github.com/rakshita-jaiswal/FinSense/issues](https://github.com/rakshita-jaiswal/FinSense/issues)

---

Made with ❤️ by the FinSense Team