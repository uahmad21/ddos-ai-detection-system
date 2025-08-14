# 🚀 DDoS AI Detection System - Deployment Guide

This guide will help you deploy the DDoS AI Detection System to Render.com for online access.

## 📋 Prerequisites

1. **GitHub Account** - You'll need to push your code to GitHub
2. **Render.com Account** - Free account for hosting
3. **Basic Git knowledge** - To push code changes

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Navigate to your project directory:**
   ```bash
   cd df_defence
   ```

2. **Initialize Git repository (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `ddos-ai-detection-system`
   - Make it public
   - Don't initialize with README

2. **Push your code to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ddos-ai-detection-system.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render.com

1. **Go to Render.com:**
   - Visit [render.com](https://render.com)
   - Sign up/Sign in with your GitHub account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `ddos-ai-detection-system` repository

3. **Configure the Service:**
   - **Name:** `ddos-ai-detection-system`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements_production.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn dl_ids.wsgi:application`
   - **Plan:** Free

4. **Environment Variables:**
   - `DJANGO_SETTINGS_MODULE`: `dl_ids.settings_production`
   - `SECRET_KEY`: Leave empty (Render will generate one)

5. **Click "Create Web Service"**

### Step 4: Wait for Deployment

- Render will automatically build and deploy your application
- This process takes 5-10 minutes
- You'll see build logs in real-time

### Step 5: Access Your Application

Once deployment is complete, you'll get a URL like:
```
https://ddos-ai-detection-system.onrender.com
```

## 🔑 Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`
- **Login URL:** `https://your-app.onrender.com/admin/`

## 📱 What's Available Online

### Main Features:
- **Dashboard:** `/` - Main application interface
- **Admin Panel:** `/admin/` - Django admin interface
- **Model Tuning:** `/model-tuning/` - AI model management
- **Traffic Logs:** `/traffic-log/` - Network traffic analysis

### Demo Capabilities:
- View pre-trained AI models
- Analyze uploaded network data
- Monitor system performance
- Access admin features

## ⚠️ Important Notes

1. **DDoS Middleware Disabled:** Packet capture is disabled for cloud deployment
2. **Demo Mode:** This is a demonstration version, not for production security
3. **Free Tier Limitations:** Render free tier has some restrictions
4. **Model Files:** Pre-trained models are included in the deployment

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails:**
   - Check the build logs in Render dashboard
   - Ensure all files are committed to GitHub
   - Verify Python version compatibility

2. **App Won't Start:**
   - Check start command: `gunicorn dl_ids.wsgi:application`
   - Verify environment variables are set correctly

3. **Static Files Not Loading:**
   - Ensure `python manage.py collectstatic` runs during build
   - Check `STATIC_ROOT` setting

4. **Database Issues:**
   - SQLite database is created automatically
   - Migrations run during build process

## 🔄 Updating Your App

To update your deployed application:

1. **Make changes to your code**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Render automatically redeploys** when it detects changes

## 📞 Support

If you encounter issues:
1. Check Render.com build logs
2. Verify all files are properly committed
3. Ensure environment variables are set correctly
4. Check Django error logs in Render dashboard

## 🎉 Success!

Once deployed, you can:
- Share the URL with others for demonstrations
- Access the system from anywhere
- Show off the AI-powered DDoS detection capabilities
- Use it for educational and research purposes

**Your DDoS AI Detection System is now live on the internet! 🌐**
