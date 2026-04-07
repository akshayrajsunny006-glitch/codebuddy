#!/bin/bash
echo ""
echo "⚡ CodeBuddy Setup (MySQL)"
echo "=========================="

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required. Install from https://python.org"
    exit 1
fi
echo "✓ $(python3 --version)"

# Virtual environment
[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "→ Installing requirements..."
pip install -r requirements.txt -q

# .env setup
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "┌─────────────────────────────────────────┐"
    echo "│  ⚠️  Configure your MySQL credentials    │"
    echo "│  Edit the .env file before continuing   │"
    echo "└─────────────────────────────────────────┘"
    echo ""
    echo "  DB_NAME=codebuddy_db"
    echo "  DB_USER=root"
    echo "  DB_PASSWORD=your_password"
    echo "  DB_HOST=127.0.0.1"
    echo "  DB_PORT=3306"
    echo ""
    read -p "Press Enter after editing .env to continue..."
fi

echo "→ Running migrations..."
python manage.py makemigrations auth_app projects social admin_app support --no-input -q
python manage.py migrate --no-input

echo "→ Seeding demo data..."
python manage.py seed_data

echo ""
echo "▶  python manage.py runserver"
echo "   Open: http://127.0.0.1:8000"
