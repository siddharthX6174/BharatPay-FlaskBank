from app import app, db, bcrypt
from app.models.user import User
import random

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        
        if admin:
            print(f"Admin already exists: {admin.email}")
            return
        
        # Create admin user (admin doesn't need account/card numbers)
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
        print(f"Email: admin@bwavebank.com")
        print(f"Password: admin123")
        print(f"\n⚠️  Please change the password after first login!")

if __name__ == '__main__':
    create_admin()
