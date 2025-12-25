# FinSense Deployment Guide

## GitHub Repository Setup

The repository is already configured at: **https://github.com/rakshita-jaiswal/FinSense**

## Live Deployment Options

### Option 1: Deploy Frontend to Vercel (Recommended)

FinSense is pre-configured for Vercel deployment with the `vercel.json` file.

#### Steps:

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your repository: `rakshita-jaiswal/FinSense`
   - Configure build settings:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   - Add environment variables (if needed):
     - `VITE_API_URL`: Your backend API URL
   - Click "Deploy"

3. **Your live link will be**: `https://finsense-[random].vercel.app`

### Option 2: Deploy Frontend to GitHub Pages

#### Steps:

1. **Install gh-pages** (in frontend directory):
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

2. **Update package.json** to add homepage and deploy scripts:
   ```json
   {
     "homepage": "https://rakshita-jaiswal.github.io/FinSense",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     }
   }
   ```

3. **Update vite.config.ts** to set base path:
   ```typescript
   export default defineConfig({
     base: '/FinSense/',
     // ... rest of config
   })
   ```

4. **Deploy**:
   ```bash
   npm run deploy
   ```

5. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `gh-pages` / `root`
   - Save

6. **Your live link will be**: `https://rakshita-jaiswal.github.io/FinSense`

### Option 3: Deploy Frontend to Netlify

#### Steps:

1. **Push to GitHub** (if not already done)

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Sign in with GitHub
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select `rakshita-jaiswal/FinSense`
   - Configure build settings:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`
   - Add environment variables (if needed)
   - Click "Deploy site"

3. **Your live link will be**: `https://finsense-[random].netlify.app`

## Backend Deployment

### Option 1: Deploy Backend to Render

1. Go to [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Add environment variables from `.env`
6. Deploy

### Option 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Deploy

### Option 3: Deploy Backend to Heroku

1. Install Heroku CLI
2. Create `Procfile` in backend directory:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create finsense-api
   git subtree push --prefix backend heroku main
   ```

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.com
VITE_PLAID_ENV=sandbox
```

### Backend (.env)
```env
MONGODB_URL=your_mongodb_connection_string
SECRET_KEY=your_secret_key
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
STRIPE_SECRET_KEY=your_stripe_secret_key
```

## Post-Deployment Checklist

- [ ] Frontend is accessible via live URL
- [ ] Backend API is running and accessible
- [ ] Frontend can communicate with backend API
- [ ] Environment variables are properly set
- [ ] Database connection is working
- [ ] Authentication flow works
- [ ] Payment integration works (if applicable)
- [ ] All features are functional

## Troubleshooting

### Frontend Issues
- **404 on refresh**: Ensure `vercel.json` or `_redirects` file is configured
- **API calls failing**: Check CORS settings in backend
- **Build fails**: Check Node version compatibility

### Backend Issues
- **Database connection fails**: Verify MongoDB connection string
- **API not responding**: Check port configuration and firewall rules
- **Environment variables missing**: Ensure all required vars are set

## Quick Deploy Commands

### Frontend (Vercel)
```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Frontend (GitHub Pages)
```bash
cd frontend
npm run deploy
```

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/rakshita-jaiswal/FinSense/issues

## License

[Add your license information here]