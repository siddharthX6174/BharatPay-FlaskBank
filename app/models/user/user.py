from app import app, db
from sqlalchemy import Numeric
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(16), unique=True, nullable=True)  # Permanent account number (not required for admin)
    card_number = db.Column(db.String(16), unique=True, nullable=True)  # Primary card number (not required for admin)
    balance = db.Column(Numeric(12, 2), default=0.00)  # Start with zero balance
    
    # Profile fields
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Role and status
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    profile_update_pending = db.Column(db.Boolean, default=False)  # Profile changes awaiting approval
    
    # Relationships with cascades
    beneficiaries = db.relationship('Beneficiary', back_populates='user', cascade="all, delete-orphan")
    transaction_limit = db.relationship('TransactionLimit', back_populates='user', uselist=False, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', back_populates='user', cascade="all, delete-orphan")
    profile_changes = db.relationship('ProfileChangeLog', foreign_keys='ProfileChangeLog.user_id', back_populates='user', cascade="all, delete-orphan")
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.user_id', back_populates='user', cascade="all, delete-orphan")
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)



def insert_hyphens(value):
    value = re.sub(r'\s', '', value) # Remove any existing whitespace
    return re.sub(r'\d{4}(?!$)', '\\g<0>-', value)

app.jinja_env.filters['insert_hyphens'] = insert_hyphens