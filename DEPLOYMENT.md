# 🚀 CodeBuddy Deployment Guide - Render

## Prerequisites
- GitHub account (for version control)
- Render account (free tier available)
- Remote MySQL database (or use Render's PostgreSQL)

## Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/codebuddy.git
git branch -M main
git push -u origin main
```

## Step 2: Set Up Remote MySQL Database
If using existing MySQL:
- Ensure database is accessible from the internet
- Note: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`

**OR switch to PostgreSQL on Render:**
- Create PostgreSQL database on Render
- Update `requirements.txt` to use `psycopg2-binary` instead of `mysqlclient`

## Step 3: Create Render Web Service
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: codebuddy
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`
   - **Plan**: Free (or paid for better uptime)

## Step 4: Set Environment Variables
In Render dashboard, add under "Environment":
```
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com
DB_NAME=codebuddy_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=your-mysql-host.com
DB_PORT=3306
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

## Step 5: Deploy
Click "Create Web Service" and wait for build to complete. Check logs for errors.

## Step 6: Run Initial Setup (if needed)
Once deployment is successful:
- Database should migrate automatically
- Run seed_data: Use Render's shell or SSH

## Troubleshooting

### Connection Refused
- Verify MySQL host is accessible from Render (whitelist Render IPs)
- Check credentials in environment variables

### Static Files Not Loading
- Static files are collected with `collectstatic --noinput`
- Verify `STATIC_ROOT` path in settings

### Migration Failures
- Check database connectivity
- Verify all environment variables are set

## Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Verify database backups
- [ ] Enable HTTPS (automatic on Render)
- [ ] Monitor application logs

## Alternative: Use Render's PostgreSQL
If you prefer PostgreSQL instead of MySQL:
1. Create PostgreSQL database on Render
2. Update `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
3. Update settings.py database config
4. Redeploy

## Local Testing Before Deploy
```bash
DEBUG=False python manage.py runserver
```

---
For more info: https://render.com/docs/deploy-django
