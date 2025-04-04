# Hospital Management System - Frontend

## Netlify Deployment Guide

### Prerequisites
1. A GitHub account
2. A Netlify account
3. Your project pushed to a GitHub repository

### Deployment Steps

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Initialize git in your project if not already done:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin your-repository-url
     git push -u origin main
     ```

2. **Deploy to Netlify**
   - Log in to your Netlify account
   - Click "New site from Git"
   - Choose GitHub and select your repository
   - Configure build settings:
     - Base directory: `frontend`
     - Build command: `npm run build`
     - Publish directory: `.next`
   - Click "Deploy site"

3. **Environment Variables**
   - In Netlify dashboard, go to Site settings > Build & deploy > Environment
   - Add your environment variables from your `.env` file

### Important Notes
- The `netlify.toml` file is already configured for Next.js deployment
- Make sure your API endpoints in the frontend code are pointing to the correct production backend URL
- The site will be automatically redeployed when you push changes to the main branch