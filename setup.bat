@echo off
REM Intelligent CRM Setup Script for Windows
REM This script sets up the complete CRM system on Windows

echo 🚀 Setting up Intelligent CRM System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.9+ is required but not installed.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [SUCCESS] Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js 18+ is required but not installed.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [SUCCESS] Node.js found

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] PostgreSQL is not installed.
    echo Please install PostgreSQL 13+ from https://www.postgresql.org/download/windows/
)

REM Check if Redis is installed
redis-server --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Redis is not installed.
    echo Please install Redis from https://github.com/microsoftarchive/redis/releases
)

echo.
echo 📦 Setting up dependencies...

REM Setup Python virtual environment
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [SUCCESS] Virtual environment already exists
)

call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Python dependencies installed

REM Setup Node.js dependencies
if not exist "node_modules" (
    npm install
    echo [SUCCESS] Node.js dependencies installed
) else (
    echo [SUCCESS] Node.js dependencies already installed
)

echo.
echo ⚙️  Configuring environment...

REM Setup environment file
if not exist ".env" (
    copy env.example .env
    echo [SUCCESS] Environment file created from template
    echo [WARNING] Please edit .env file with your configuration
) else (
    echo [SUCCESS] Environment file already exists
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "media\avatars" mkdir media\avatars
if not exist "staticfiles" mkdir staticfiles
echo [SUCCESS] Directories created

echo.
echo 🗄️  Setting up database...

REM Check if database exists and create if needed
psql -lqt | findstr /C:"crm_db" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Creating database 'crm_db'...
    createdb crm_db
    echo [SUCCESS] Database created
) else (
    echo [SUCCESS] Database 'crm_db' already exists
)

REM Run migrations
call venv\Scripts\activate.bat
python manage.py migrate
echo [SUCCESS] Database migrations completed

REM Initialize CRM data
python manage.py init_crm
echo [SUCCESS] CRM system initialized

echo.
echo [SUCCESS] 🎉 CRM system setup completed!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your configuration
echo 2. Start Redis server: redis-server
echo 3. Start Celery worker: celery -A config worker -l info
echo 4. Start Celery beat: celery -A config beat -l info
echo 5. Start Django server: python manage.py runserver
echo 6. Start Next.js server: npm run dev
echo.
echo 🌐 Access the application:
echo   - Frontend: http://localhost:3000
echo   - Backend API: http://localhost:8000/api
echo   - Admin Panel: http://localhost:8000/admin
echo.
echo 👤 Default admin credentials:
echo   - Email: admin@crm.com
echo   - Password: admin123
echo.
echo 📚 Documentation: README.md
echo.
pause
