#!/bin/bash

# FinSense GitHub Pages Deployment Script
# This script helps deploy the frontend to GitHub Pages

echo "🚀 FinSense GitHub Pages Deployment"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Navigate to frontend
cd frontend

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔨 Building for GitHub Pages..."
GITHUB_PAGES=true npm run build

echo ""
echo "📤 Deploying to GitHub Pages..."

# Check if gh-pages is installed
if ! npm list gh-pages > /dev/null 2>&1; then
    echo "Installing gh-pages..."
    npm install --save-dev gh-pages
fi

# Deploy
npx gh-pages -d dist

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your site will be available at:"
echo "https://rakshita-jaiswal.github.io/FinSense"
echo ""
echo "Note: It may take a few minutes for GitHub Pages to update."
echo ""
echo "To enable GitHub Pages:"
echo "1. Go to: https://github.com/rakshita-jaiswal/FinSense/settings/pages"
echo "2. Under 'Source', select 'Deploy from a branch'"
echo "3. Select branch 'gh-pages' and folder '/ (root)'"
echo "4. Click 'Save'"