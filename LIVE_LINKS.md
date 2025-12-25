# 🌐 FinSense Live Links & Deployment

## 📍 Repository
**GitHub Repository**: [https://github.com/rakshita-jaiswal/FinSense](https://github.com/rakshita-jaiswal/FinSense)

---

## 🚀 Quick Deploy Links

### One-Click Deployments

#### Deploy Frontend to Vercel (Recommended)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rakshita-jaiswal/FinSense&project-name=finsense&repository-name=finsense&root-directory=frontend&build-command=npm%20run%20build&output-directory=dist)

**Steps:**
1. Click the button above
2. Sign in with GitHub
3. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable: `VITE_API_URL` (your backend URL)
5. Click "Deploy"

**Your live link will be**: `https://finsense-[random].vercel.app`

---

#### Deploy Frontend to Netlify
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/rakshita-jaiswal/FinSense)

**Steps:**
1. Click the button above
2. Sign in with GitHub
3. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
4. Add environment variables
5. Click "Deploy site"

**Your live link will be**: `https://finsense-[random].netlify.app`

---

#### Deploy Frontend to GitHub Pages

**Option 1: Automatic Deployment (GitHub Actions)**

The repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages on every push to main.

**Setup:**
1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: "GitHub Actions"
3. Push to main branch - deployment happens automatically!

**Your live link will be**: `https://rakshita-jaiswal.github.io/FinSense`

**Option 2: Manual Deployment**

**On macOS/Linux:**
```bash
./deploy-github-pages.sh
```

**On Windows:**
```bash
deploy-github-pages.bat
```

**Or manually:**
```bash
cd frontend
npm install
GITHUB_PAGES=true npm run build
npm install --save-dev gh-pages
npx gh-pages -d dist
```

Then enable GitHub Pages:
1. Go to: https://github.com/rakshita-jaiswal/FinSense/settings/pages
2. Source: "Deploy from a branch"
3. Branch: `gh-pages` / `root`
4. Click "Save"

**Your live link will be**: `https://rakshita-jaiswal.github.io/FinSense`

---

## 🔧 Backend Deployment Options

### Deploy to Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Name: `finsense-api`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env`
6. Click "Create Web Service"

**Your API will be**: `https://finsense-api.onrender.com`

---

### Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `rakshita-jaiswal/FinSense`
4. Configure:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

**Your API will be**: `https://finsense-api.up.railway.app`

---

### Deploy to Fly.io
```bash
cd backend
fly launch
fly deploy
```

---

## 🔗 Expected Live URLs

Once deployed, your FinSense application will be accessible at:

### Frontend Options:
- **Vercel**: `https://finsense-[random].vercel.app`
- **Netlify**: `https://finsense-[random].netlify.app`
- **GitHub Pages**: `https://rakshita-jaiswal.github.io/FinSense`

### Backend Options:
- **Render**: `https://finsense-api.onrender.com`
- **Railway**: `https://finsense-api.up.railway.app`
- **Fly.io**: `https://finsense-api.fly.dev`

---

## ⚙️ Environment Configuration

### Frontend Environment Variables
```env
VITE_API_URL=https://your-backend-url.com
VITE_PLAID_ENV=sandbox
```

### Backend Environment Variables
```env
MONGODB_URL=your_mongodb_connection_string
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Plaid
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENV=sandbox

# Stripe
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key
```

---

## 📋 Post-Deployment Checklist

- [ ] Frontend is deployed and accessible
- [ ] Backend API is deployed and accessible
- [ ] Environment variables are configured
- [ ] Frontend can connect to backend API
- [ ] CORS is properly configured in backend
- [ ] Database connection is working
- [ ] Authentication flow works
- [ ] Plaid integration works (if configured)
- [ ] Stripe payments work (if configured)
- [ ] AI assistant responds (if configured)

---

## 🐛 Troubleshooting

### Frontend Issues

**404 on page refresh:**
- Vercel/Netlify: Automatically handled
- GitHub Pages: Ensure `vercel.json` rewrites are configured

**API calls failing:**
- Check `VITE_API_URL` environment variable
- Verify CORS settings in backend
- Check browser console for errors

**Build fails:**
- Verify Node.js version (18+)
- Clear `node_modules` and reinstall
- Check for TypeScript errors

### Backend Issues

**Database connection fails:**
- Verify MongoDB connection string
- Check IP whitelist in MongoDB Atlas
- Ensure database user has proper permissions

**API not responding:**
- Check logs in deployment platform
- Verify port configuration
- Check environment variables

**CORS errors:**
- Add frontend URL to CORS origins in backend
- Verify `Access-Control-Allow-Origin` headers

---

## 📚 Additional Resources

- [Full Deployment Guide](DEPLOYMENT_GUIDE.md)
- [MongoDB Setup](MONGODB_SETUP_GUIDE.md)
- [Plaid Integration](PLAID_INTEGRATION.md)
- [Stripe Setup](STRIPE_SETUP_GUIDE.md)
- [Gemini AI Setup](backend/GEMINI_AI_SETUP.md)

---

## 🆘 Support

If you encounter issues:
1. Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. Review deployment platform logs
3. Open an issue: [GitHub Issues](https://github.com/rakshita-jaiswal/FinSense/issues)

---

## 📝 Notes

- **Free Tier Limitations**: Most platforms have free tiers with limitations
- **Cold Starts**: Free tier backends may have cold start delays
- **Database**: Consider MongoDB Atlas free tier for database hosting
- **Domain**: You can add custom domains on most platforms

---

**Last Updated**: December 2024