#!/usr/bin/env python
"""
Bwave Bank - Complete Initialization and Startup Script
This script handles all initialization tasks and starts the Flask application.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def install_dependencies():
    """Install required Python packages"""
    print_header("STEP 1: Installing Dependencies")
    
    requirements_file = Path('requirements.txt')
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        print("📦 Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--quiet'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def initialize_database():
    """Create database and tables"""
    print_header("STEP 2: Initializing Database")
    
    try:
        from app import app, db
        from app.models.user import User, Transaction, ProfileChangeLog
        from app.models.user.features import Beneficiary, TransactionLimit, Notification
        
        with app.app_context():
            # Check if database exists
            db_path = Path('instance/banking.db')
            if db_path.exists():
                print("ℹ️  Database already exists")
            else:
                print("🗄️  Creating database...")
                db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create all tables
            print("📋 Creating/updating database tables...")
            db.create_all()
            print("✅ Database initialized successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_admin_user():
    """Create admin user if doesn't exist"""
    print_header("STEP 3: Setting up Admin Account")
    
    try:
        from app import app, db, bcrypt
        from app.models.user import User
        
        with app.app_context():
            # Check if admin exists
            admin = User.query.filter_by(role='admin').first()
            
            if admin:
                print(f"ℹ️  Admin already exists: {admin.email}")
                return True
            
            # Create admin user
            print("👤 Creating admin user...")
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            
            admin = User(
                full_name='System Administrator',
                email='admin@bwavebank.com',
                password=hashed_password,
                balance=0,
                role='admin',
                status='approved'
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Email: admin@bwavebank.com")
            print(f"   Password: admin123")
            print(f"   ⚠️  Please change the password after first login!")
            return True
            
    except Exception as e:
        print(f"❌ Admin creation failed: {e}")
        return False

def start_application():
    """Start the Flask application"""
    print_header("STEP 4: Starting Application")
    
    try:
        from app import app
        
        print("🚀 Starting Bwave Bank application...")
        print(f"📍 Access the application at: http://127.0.0.1:5000")
        print(f"🔐 Admin panel: http://127.0.0.1:5000/admin/dashboard")
        print("\n⚠️  Press Ctrl+C to stop the server\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False

def main():
    """Main initialization and startup sequence"""
    print("\n" + "🏦 " + "="*54 + " 🏦")
    print("   BWAVE BANK - Complete Initialization & Startup")
    print("🏦 " + "="*54 + " 🏦")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n❌ Initialization failed at dependency installation")
        sys.exit(1)
    
    # Step 2: Initialize database
    if not initialize_database():
        print("\n❌ Initialization failed at database setup")
        sys.exit(1)
    
    # Step 3: Create admin user
    if not create_admin_user():
        print("\n❌ Initialization failed at admin creation")
        sys.exit(1)
    
    # Step 4: Start application
    print_header("Initialization Complete!")
    print("✅ All systems ready!")
    print("🎉 Bwave Bank is ready to use!\n")
    
    start_application()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Startup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
