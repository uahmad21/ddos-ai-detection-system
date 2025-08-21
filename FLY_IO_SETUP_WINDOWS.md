# 🚁 Fly.io Deployment Guide for Windows

## 🎯 **What You'll Get:**
- **Fast website** (much faster than Render.com)
- **No cold starts** 
- **Professional hosting**
- **Demo attack simulation** working perfectly

## 📥 **Step 1: Download Fly CLI (Windows)**

1. **Go to:** https://fly.io/docs/hands-on/install-flyctl/
2. **Click:** "Download for Windows"
3. **Run** the downloaded `.exe` file
4. **Follow** the installation prompts

## 🔐 **Step 2: Login to Fly**

1. **Open Command Prompt** (or PowerShell)
2. **Type:** `fly auth login`
3. **Click the link** that appears
4. **Sign up** with GitHub (free account)
5. **Authorize** Fly.io

## 🚀 **Step 3: Deploy Your App**

1. **Navigate to your project:**
```bash
cd C:\Users\SUAhm\Downloads\ddos_ai-main\ddos_ai-main\df_defence
```

2. **Initialize Fly app:**
```bash
fly launch
```

3. **Answer the questions:**
- **App name:** `ddos-ai-detection-system` (or press Enter for default)
- **Region:** Press Enter for default (iad = Virginia, USA)
- **Database:** Press Enter for "No"
- **Deploy now:** Press Enter for "Yes"

4. **Wait** for deployment to complete

## 🌐 **Step 4: Get Your Website URL**

1. **Check status:**
```bash
fly status
```

2. **Your website will be:** `https://your-app-name.fly.dev`

## 🎬 **Step 5: Demo Your System**

### **Login Credentials:**
- **Username:** `admin` / **Password:** `admin123`
- **Username:** `demo` / **Password:** `demo123`
- **Username:** `user` / **Password:** `user123`
- **Username:** `test` / **Password:** `test123`

### **What You Can Show:**
1. **Login system** - Works perfectly
2. **Dashboard** - Shows demo attack data
3. **Traffic monitoring** - Displays blocked IPs
4. **IP rules** - Shows blocked suspicious IPs
5. **Model training** - Simulates AI model training
6. **Attack detection** - Shows where attacks would appear

## 🔄 **Update Your App Later:**

```bash
cd C:\Users\SUAhm\Downloads\ddos_ai-main\ddos_ai-main\df_defence
fly deploy
```

## 🆘 **If Something Goes Wrong:**

1. **Check logs:**
```bash
fly logs
```

2. **Restart app:**
```bash
fly restart
```

3. **Check status:**
```bash
fly status
```

## 🎉 **You're Done!**

Your DDoS AI Detection System will be:
- **Fast** (no more slow loading)
- **Professional** (looks like real production)
- **Demo-ready** (perfect for your colleague)
- **Always online** (no cold starts)

**This is exactly what you need for your demonstration!** 🚀
