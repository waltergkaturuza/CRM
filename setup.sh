#!/bin/bash

# Intelligent CRM Setup Script
# This script sets up the complete CRM system

set -e

echo "🚀 Setting up Intelligent CRM System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.9+ is required but not installed."
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $python_version found"
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js 18+ is required but not installed."
        exit 1
    fi
    
    node_version=$(node --version)
    print_success "Node.js $node_version found"
}

# Check if PostgreSQL is installed
check_postgres() {
    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL is not installed. Please install PostgreSQL 13+"
        print_warning "You can install it using:"
        print_warning "  - Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
        print_warning "  - macOS: brew install postgresql"
        print_warning "  - Windows: Download from https://www.postgresql.org/download/"
    else
        postgres_version=$(psql --version | cut -d' ' -f3)
        print_success "PostgreSQL $postgres_version found"
    fi
}

# Check if Redis is installed
check_redis() {
    if ! command -v redis-server &> /dev/null; then
        print_warning "Redis is not installed. Please install Redis 6+"
        print_warning "You can install it using:"
        print_warning "  - Ubuntu/Debian: sudo apt-get install redis-server"
        print_warning "  - macOS: brew install redis"
        print_warning "  - Windows: Download from https://redis.io/download"
    else
        redis_version=$(redis-server --version | head -n1 | cut -d' ' -f3)
        print_success "Redis $redis_version found"
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Python dependencies installed"
}

# Setup Node.js dependencies
setup_node_env() {
    print_status "Setting up Node.js dependencies..."
    
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Node.js dependencies installed"
    else
        print_success "Node.js dependencies already installed"
    fi
}

# Setup environment file
setup_env() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your configuration"
    else
        print_success "Environment file already exists"
    fi
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    # Check if database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw crm_db; then
        print_success "Database 'crm_db' already exists"
    else
        print_status "Creating database 'crm_db'..."
        createdb crm_db
        print_success "Database created"
    fi
    
    # Run migrations
    source venv/bin/activate
    python manage.py migrate
    print_success "Database migrations completed"
    
    # Initialize CRM data
    python manage.py init_crm
    print_success "CRM system initialized"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p media/avatars
    mkdir -p staticfiles
    
    print_success "Directories created"
}

# Main setup function
main() {
    echo "🔍 Checking system requirements..."
    check_python
    check_node
    check_postgres
    check_redis
    
    echo ""
    echo "📦 Setting up dependencies..."
    setup_python_env
    setup_node_env
    
    echo ""
    echo "⚙️  Configuring environment..."
    setup_env
    create_directories
    
    echo ""
    echo "🗄️  Setting up database..."
    setup_database
    
    echo ""
    print_success "🎉 CRM system setup completed!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Start Redis server: redis-server"
    echo "3. Start Celery worker: celery -A config worker -l info"
    echo "4. Start Celery beat: celery -A config beat -l info"
    echo "5. Start Django server: python manage.py runserver"
    echo "6. Start Next.js server: npm run dev"
    echo ""
    echo "🌐 Access the application:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000/api"
    echo "  - Admin Panel: http://localhost:8000/admin"
    echo ""
    echo "👤 Default admin credentials:"
    echo "  - Email: admin@crm.com"
    echo "  - Password: admin123"
    echo ""
    echo "📚 Documentation: README.md"
}

# Run main function
main "$@"
