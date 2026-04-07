#!/bin/bash
# run_on_deploy.sh - Run migrations on Render deployment
# Render will execute this automatically if configured

echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Deployment setup complete!"
