@echo off
echo.
echo ⚡ CodeBuddy Setup (MySQL + Windows)
echo =====================================

python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

if not exist .env (
    copy .env.example .env
    echo.
    echo ⚠️  Edit .env with your MySQL credentials before continuing!
    echo    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
    echo.
    pause
)

python manage.py makemigrations auth_app projects social admin_app support
python manage.py migrate
python manage.py seed_data

echo.
echo Done! Run: python manage.py runserver
echo Open:      http://127.0.0.1:8000
pause
