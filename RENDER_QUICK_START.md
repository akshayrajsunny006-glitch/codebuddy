# 🚀 CodeBuddy Render Deployment - Quick Setup

## Your GitHub Repo
✅ **Repository**: https://github.com/akshayrajsunny006-glitch/codebuddy

---

## Render Deployment (5 minutes)

### Step 1: Connect Render to GitHub (1 minute)
1. Visit: https://dashboard.render.com
2. Sign in with GitHub
3. Grant Render permission to access your repositories

### Step 2: Create Web Service (2 minutes)
1. Click **"New +"** → **"Web Service"**
2. Find `codebuddy` repository and select it
3. Click **"Connect"**

### Step 3: Configure Service (2 minutes)

| Setting | Value |
|---------|-------|
| **Name** | `codebuddy` |
| **Environment** | `Python 3` |
| **Region** | Choose your region |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `python manage.py runserver 0.0.0.0:$PORT` |
| **Plan** | Free tier (or paid for better performance) |

### Step 4: Add Environment Variables (2 minutes)
Click **"Add Environment Variable"** for each:

```
DEBUG = False
SECRET_KEY = your-super-secret-key-12345-change-this
ALLOWED_HOSTS = codebuddy.onrender.com
DB_NAME = codebuddy_db
DB_USER = root
DB_PASSWORD = your-mysql-password
DB_HOST = your-mysql-host.example.com
DB_PORT = 3306
CSRF_TRUSTED_ORIGINS = https://codebuddy.onrender.com
```

> ⚠️ **Important**: Replace the values with YOUR actual database credentials

### Step 5: Deploy!
Click **"Create Web Service"** and wait ~3-5 minutes for deployment.

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and synced
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web Service created
- [ ] All environment variables added
- [ ] Build and deployment successful
- [ ] Application accessible at render URL

---

## 🔐 Security Notes

**Never commit these to Git:**
- `.env` file (already in .gitignore ✓)
- Database passwords
- SECRET_KEY

**Environment Variables must be set in Render dashboard**, not in code.

---

## 📊 Post-Deployment

Once deployed:
1. Visit your app URL: `https://codebuddy.onrender.com` (or similar)
2. Check Render logs for any errors
3. Test login with demo account: `arjun@iitd.ac.in` / `arjun123`
4. Monitor performance in Render dashboard

---

## ❌ If Deployment Fails

**Check these:**
1. Build logs in Render dashboard
2. Database connectivity (MySQL accessible from render?)
3. Environment variables are correct
4. `DEBUG=False` is set

**Common Issues:**
- "Connection refused" → Database host unreachable
- "ModuleNotFoundError" → Missing dependency in requirements.txt
- "Static files 404" → Run `collectstatic` manually

---

## 🎉 Success!

Once running, you have:
- ✅ Live CodeBuddy application
- ✅ Automatic HTTPS
- ✅ Automatic restarts on crashes
- ✅ Easy rollback to previous deployments
- ✅ Python/Django friendly hosting

---

**Need help? Check:**
- Render docs: https://render.com/docs/deploy-django
- Django docs: https://docs.djangoproject.com/en/6.0/
- This file: [DEPLOYMENT.md](./DEPLOYMENT.md)
